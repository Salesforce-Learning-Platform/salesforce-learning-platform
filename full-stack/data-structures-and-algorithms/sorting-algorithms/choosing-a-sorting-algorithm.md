# 🧭 Choosing a Sorting Algorithm

## Putting the Module Together

You have now met the whole family: the quadratic [elementary sorts](elementary-sorts.md), the three O(n log n) comparison sorts — [merge sort](merge-sort.md), [quick sort](quick-sort.md), and [heap sort](heap-sort.md) — and the special-purpose [cyclic sort](cyclic-sort.md). This closing file does three things. It lays the algorithms side by side. It adds the last two members of the family, **counting sort** and **radix sort**, which beat the `n log n` limit by not comparing items at all. And it answers the practical question — *which one should I use?* — with measurements rather than slogans.

All outputs below were produced by running the code on CPython 3.9. Timings come from one machine and will differ on yours; look at the **ratios and the ordering**, not the absolute numbers.

## 📋 The Properties at a Glance

| Algorithm | Best | Average | Worst | Extra space | Stable | Worth remembering |
|-----------|------|---------|-------|-------------|--------|-------------------|
| [Bubble sort](elementary-sorts.md) (early exit) | O(n) | O(n²) | O(n²) | O(1) | Yes | Teaching tool; almost never the right choice |
| [Selection sort](elementary-sorts.md) | O(n²) | O(n²) | O(n²) | O(1) | No | At most `n − 1` swaps |
| [Insertion sort](elementary-sorts.md) | O(n) | O(n²) | O(n²) | O(1) | Yes | Best for tiny or nearly sorted input |
| [Merge sort](merge-sort.md) | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Predictable; linked lists; external sorting |
| [Quick sort](quick-sort.md) (random pivot) | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Fast in place; use 3-way partitioning for duplicates |
| [Heap sort](heap-sort.md) | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Guaranteed time *and* in place |
| [Cyclic sort](cyclic-sort.md) | O(n) | O(n) | O(n) | O(1) | n/a | Only for the values `1..n` |
| Counting sort (below) | O(n + k) | O(n + k) | O(n + k) | O(n + k) | Yes | Integer keys in `0..k−1` |
| Radix sort, LSD (below) | O(d(n + b)) | O(d(n + b)) | O(d(n + b)) | O(n + b) | Yes | `d` digits in base `b` |
| **Timsort** (Python's `sorted`) | O(n) | O(n log n) | O(n log n) | up to n/2 pointers | Yes | Adaptive, stable, fast in C |

Timsort's description in the CPython source is "an adaptive, stable, natural mergesort", and its temporary array may need up to `N // 2` pointers ([CPython `listsort.txt`](https://github.com/python/cpython/blob/main/Objects/listsort.txt)). The O(n) best case is the already-sorted (or reversed) input, which needs only `n − 1` comparisons ([sorting-fundamentals.md](sorting-fundamentals.md) measured this).

## 🧮 Beyond `n log n`: Counting Sort and Radix Sort

Every comparison sort needs at least `⌈log₂ n!⌉` comparisons ([sorting-fundamentals.md](sorting-fundamentals.md)), but that limit only applies to algorithms that learn about the data *solely by comparing two items*. If the keys are small integers, you can learn much more from a key than "bigger or smaller": you can use it as an index.

### Counting Sort

To sort items whose keys are integers in `0..k−1`: count how many items have each key; turn the counts into **starting positions** (the starting position of key `v` is the number of items with a smaller key); then place each item at the next free position of its key, scanning the input left to right so that equal keys keep their input order — which makes counting sort **stable**.

```python
import itertools
import random

def counting_sort(items, key, k):
    """Stable sort of items whose key(item) is an integer in range(k). O(n + k) time and space."""
    counts = [0] * (k + 1)
    for item in items:
        counts[key(item) + 1] += 1                 # counts[v + 1] = how many items have key v
    for v in range(k):
        counts[v + 1] += counts[v]                 # now counts[v] = how many items have a key < v = where key v starts
    result = [None] * len(items)
    for item in items:                             # left to right: equal keys keep their input order
        result[counts[key(item)]] = item
        counts[key(item)] += 1
    return result

keys = [2, 0, 2, 3, 0, 1]
tally = [keys.count(v) for v in range(4)]
print("count of each key:        ", tally)
print("where each key starts:    ", list(itertools.accumulate(tally, initial=0))[:4])
records = [("b", 2), ("a", 0), ("c", 2), ("d", 3), ("e", 0), ("f", 1)]
print(counting_sort(records, key=lambda r: r[1], k=4))
```

```text
count of each key:         [2, 1, 2, 1]
where each key starts:     [0, 2, 3, 5]
[('a', 0), ('e', 0), ('f', 1), ('b', 2), ('c', 2), ('d', 3)]
```

The records with key 0 (`a`, `e`) and key 2 (`b`, `c`) come out in their original order. The cost is O(n + k): one pass over the items, one over the `k` counters, one more over the items. That is wonderful when `k` is about the size of `n` or smaller, and terrible when it is not — the counters array alone has `k + 1` entries (the measurement below shows the damage).

### Radix Sort

Counting sort needs `k` counters, so it cannot handle large numbers directly: 32-bit integers would need billions. **Radix sort** sorts by one digit at a time, from the **least significant digit** to the most significant, using a *stable* sort (counting sort) for each digit. After the pass on a digit, the items are ordered by their last `i` digits; because every pass is stable, ties on the current digit preserve the order established by the less significant digits. With `d` digits in base `b`, the cost is `d` passes of O(n + b).

```python
def radix_sort(numbers, base=10):
    """LSD radix sort for non-negative integers."""
    numbers = list(numbers)
    if not numbers:
        return numbers
    largest = max(numbers)
    place = 1
    while largest // place > 0:                    # one stable counting-sort pass per digit
        numbers = counting_sort(numbers, key=lambda x: (x // place) % base, k=base)
        place *= base
    return numbers

print(radix_sort([170, 45, 75, 90, 802, 24, 2, 66]))
```

```text
[2, 24, 45, 66, 75, 90, 170, 802]
```

Negative numbers can be handled by subtracting the minimum first and adding it back at the end. The base is a tuning knob: a larger base means fewer passes but a bigger counters array per pass — the benchmarks below compare base 10 with base 256.

Counting and radix sort are two members of a larger family of non-comparison sorts; [Wikipedia: Counting sort](https://en.wikipedia.org/wiki/Counting_sort), [Radix sort](https://en.wikipedia.org/wiki/Radix_sort), and [Pigeonhole sort](https://en.wikipedia.org/wiki/Pigeonhole_sort) describe them and their relatives (such as bucket sort).

## 🧰 Condensed Implementations for the Race

The race below needs every sort in one place. These are compact versions of the algorithms from the earlier files; each returns the sorted list so they can be timed uniformly. (Quick sort here uses a random pivot and the three-way partition from [quick-sort.md](quick-sort.md), so that it copes with duplicates.)

```python
def insertion_sort(items):
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and current < items[j]:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current
    return items

def merge_sort(items):
    if len(items) <= 1:
        return list(items)
    middle = len(items) // 2
    left, right = merge_sort(items[:middle]), merge_sort(items[middle:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if right[j] < left[i]:                     # strictly less: equal items are taken from the left first (stable)
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def quick_sort(items):
    def sort(low, high):
        while low < high:
            pivot = items[random.randint(low, high)]
            lt, i, gt = low, low, high
            while i <= gt:
                if items[i] < pivot:
                    items[lt], items[i] = items[i], items[lt]
                    lt += 1
                    i += 1
                elif pivot < items[i]:
                    items[i], items[gt] = items[gt], items[i]
                    gt -= 1
                else:
                    i += 1
            if lt - low < high - gt:
                sort(low, lt - 1)
                low = gt + 1
            else:
                sort(gt + 1, high)
                high = lt - 1
    sort(0, len(items) - 1)
    return items

def sift_down(items, root, end):
    while True:
        child = 2 * root + 1
        if child >= end:
            return
        if child + 1 < end and items[child] < items[child + 1]:
            child += 1
        if not items[root] < items[child]:
            return
        items[root], items[child] = items[child], items[root]
        root = child

def heap_sort(items):
    n = len(items)
    for root in range(n // 2 - 1, -1, -1):
        sift_down(items, root, n)
    for end in range(n - 1, 0, -1):
        items[0], items[end] = items[end], items[0]
        sift_down(items, 0, end)
    return items

random.seed(1)
for _ in range(2_000):
    values = [random.randint(0, 50) for _ in range(random.randint(0, 40))]
    expected = sorted(values)
    assert insertion_sort(list(values)) == merge_sort(values) == quick_sort(list(values)) == heap_sort(list(values)) == expected
    assert radix_sort(values) == counting_sort(values, key=lambda x: x, k=51) == expected
print("all condensed versions agree with sorted() on 2,000 random lists")
```

```text
all condensed versions agree with sorted() on 2,000 random lists
```

## 🏁 The Race: Five Input Shapes

Each algorithm sorts a copy of the same 2,000-item list in five shapes: random, already ascending, descending, nearly sorted (20 random swaps from sorted), and only ten distinct values. Best of three runs, in milliseconds:

```python
import timeit

def best_ms(sort, data, repeat=3):
    return min(timeit.repeat(lambda: sort(list(data)), number=1, repeat=repeat)) * 1000

random.seed(2)
n = 2_000
ascending = list(range(n))
nearly_sorted = list(ascending)
for _ in range(20):
    a, b = random.sample(range(n), 2)
    nearly_sorted[a], nearly_sorted[b] = nearly_sorted[b], nearly_sorted[a]
shapes = {
    "random": random.sample(range(10 * n), n),
    "ascending": ascending,
    "descending": ascending[::-1],
    "nearly sorted": nearly_sorted,
    "10 distinct values": [random.randint(0, 9) for _ in range(n)],
}
contestants = [("insertion", insertion_sort), ("merge", merge_sort), ("quick", quick_sort), ("heap", heap_sort), ("sorted()", sorted)]

print(f"{'n = 2000':>20} | " + " | ".join(f"{name:>9}" for name, _ in contestants) + "   (ms)")
for shape, data in shapes.items():
    print(f"{shape:>20} | " + " | ".join(f"{best_ms(sort, data):9.2f}" for _, sort in contestants))
```

Output:

```
            n = 2000 | insertion |     merge |     quick |      heap |  sorted()   (ms)
              random |     78.46 |      3.34 |      3.60 |      3.42 |      0.10
           ascending |      0.18 |      2.23 |      3.54 |      3.67 |      0.01
          descending |    151.40 |      2.30 |      3.48 |      3.26 |      0.01
       nearly sorted |      1.89 |      2.82 |      3.57 |      3.69 |      0.02
  10 distinct values |     71.68 |      3.33 |      0.62 |      3.16 |      0.07
```

What the table says:

- **Insertion sort is the fastest hand-written sort on sorted and nearly sorted input** (it is adaptive: O(n + inversions)), and hopeless on random or reversed input, where it is about 20 to 65 times slower than the `n log n` sorts.
- **Merge, quick, and heap sort are within about 10% of one another on random data.** The hardware effect that, according to Wikipedia, typically makes heap sort 2–3 times slower than a well-implemented quick sort ([heap-sort.md](heap-sort.md)) is not visible here: interpreter overhead per step dwarfs memory-access costs.
- **Duplicates are quick sort's best case with a three-way partition:** with ten distinct values it finishes several times faster than merge sort, because equal items are never revisited.
- **`sorted()` wins every row, by a factor of roughly 10 to 200 over the best hand-written sort.** On the ascending and descending shapes it needs only `n − 1` comparisons because Timsort finds one long run, and the whole sort is done at C speed.

## 📈 At Scale: 100,000 Items, and Where Non-Comparison Sorts Fit

```python
random.seed(3)                                                 # timed with best_ms (defined above, built on timeit)
n = 100_000
spread = random.sample(range(10 * n), n)                       # distinct values up to a million
narrow = [random.randint(0, 999) for _ in range(n)]            # values in 0..999: heavy duplicates, small range

print(f"{'n = 100,000':>34} | {'time (ms)':>9}")
for label, sort, data in [
    ("merge sort, distinct values", merge_sort, spread),
    ("quick sort, distinct values", quick_sort, spread),
    ("heap sort, distinct values", heap_sort, spread),
    ("radix sort base 10, distinct values", radix_sort, spread),
    ("radix sort base 256, distinct values", lambda numbers: radix_sort(numbers, base=256), spread),
    ("sorted(), distinct values", sorted, spread),
    ("counting sort, values in 0..999", lambda numbers: counting_sort(numbers, key=lambda x: x, k=1_000), narrow),
    ("3-way quick sort, values in 0..999", quick_sort, narrow),
    ("sorted(), values in 0..999", sorted, narrow),
]:
    print(f"{label:>34} | {best_ms(sort, data):9.1f}")
```

Output:

```
                       n = 100,000 | time (ms)
       merge sort, distinct values |     262.8
       quick sort, distinct values |     273.3
        heap sort, distinct values |     304.0
radix sort base 10, distinct values |     183.7
radix sort base 256, distinct values |      92.4
         sorted(), distinct values |      12.0
   counting sort, values in 0..999 |      19.6
3-way quick sort, values in 0..999 |     129.7
        sorted(), values in 0..999 |       7.9
```

- Radix sort **beats the comparison sorts** — three passes of base 256 take about a third of the time of the n log n sorts, and base 256 is about twice as fast as base 10 (three passes instead of six). It is the one algorithm here whose running time does not grow with `log n`.
- Counting sort on a small range is the fastest hand-written entry, and far ahead of the comparison sorts.
- **Yet `sorted()` still wins** every row: running at C speed beats a better algorithm running in the interpreter. Algorithm choice matters most when you cannot lean on a built-in.

And here is the catch for counting sort — its cost includes the size of the *range*:

```python
random.seed(4)                                                 # timed with best_ms (defined above, built on timeit)
n = 1_000
wide = [random.randint(0, 9_999_999) for _ in range(n)]       # only 1,000 items, but their range is ten million

print(f"counting sort, k = 10,000,000: {best_ms(lambda numbers: counting_sort(numbers, key=lambda x: x, k=10_000_000), wide, repeat=1):10.2f} ms")
print(f"sorted():                      {best_ms(sorted, wide):10.2f} ms")
```

Output:

```
counting sort, k = 10,000,000:     703.02 ms
sorted():                            0.04 ms
```

The counters array has ten million entries, and the cost is O(n + k) with `k` dominating. Counting sort fits only when the range of keys is comparable to — or smaller than — the number of items.

## 🐍 Sorting in Python: The Practical Toolkit

In real Python code you will almost always reach for `sorted()` or `list.sort()`. The details worth knowing, each verified below against the [Python documentation](https://docs.python.org/3/library/stdtypes.html#list.sort) and the [Sorting Techniques HOWTO](https://docs.python.org/3/howto/sorting.html):

- `sorted()` returns a **new** list; `list.sort()` sorts **in place and returns `None`**.
- Both are **stable** and use only `<` comparisons.
- The `key` function is called **once per item**; its results are cached for the whole sort.
- Because the sort is stable, you can sort by several criteria in successive passes — **least important key first** — or with one tuple key.
- `reverse=True` keeps equal items in their original order; reversing the finished list does not.

```python
from functools import cmp_to_key
from operator import itemgetter
import bisect
import heapq

numbers = [5, 2, 3, 1, 4]
print(sorted(numbers), numbers)                                      # [1, 2, 3, 4, 5] [5, 2, 3, 1, 4]
result = numbers.sort()
print(result, numbers)                                               # None [1, 2, 3, 4, 5]

students = [("Ana", "B", 20), ("Ben", "A", 22), ("Cara", "B", 19), ("Dev", "A", 20), ("Eli", "B", 20)]
by_name = sorted(students, key=itemgetter(0))
by_grade_then_name = sorted(by_name, key=itemgetter(1))              # stable: names stay alphabetical inside each grade
print(by_grade_then_name)
print(sorted(students, key=lambda s: (s[1], -s[2], s[0])))           # (one pass: grade ascending, age descending, then name)

records = [("a", 1), ("b", 1), ("c", 2)]
print(sorted(records, key=itemgetter(1), reverse=True))              # [('c', 2), ('a', 1), ('b', 1)]
print(sorted(records, key=itemgetter(1))[::-1])                      # [('c', 2), ('b', 1), ('a', 1)]

calls = []
def noisy_key(x):
    calls.append(x)
    return -x
print(sorted([3, 1, 2], key=noisy_key), len(calls))                  # [3, 2, 1] 3

def by_length_then_alphabet(a, b):                                   # an old-style comparison function
    if len(a) != len(b):
        return len(a) - len(b)
    return (a > b) - (a < b)
print(sorted(["pear", "fig", "apple", "kiwi", "date"], key=cmp_to_key(by_length_then_alphabet)))      # ['fig', 'date', 'kiwi', 'pear', 'apple']

words = ["banana", "Cherry", "apple"]
print(sorted(words), sorted(words, key=str.casefold))               # ['Cherry', 'apple', 'banana'] ['apple', 'banana', 'Cherry']

try:
    sorted([3, "a", 1])
except TypeError as error:
    print(error)                                                     # '<' not supported between instances of 'str' and 'int'

data = [7, 2, 9, 4, 1, 8, 2]
print(heapq.nsmallest(3, data), heapq.nlargest(3, data))            # [1, 2, 2] [9, 8, 7]
print(list(heapq.merge([1, 4, 7], [2, 5, 8], [3, 6, 9])))           # [1, 2, 3, 4, 5, 6, 7, 8, 9]

ordered = [10, 20, 30, 40]
bisect.insort(ordered, 25)                                           # binary search for the position, then an O(n) insertion
print(ordered)                                                       # [10, 20, 25, 30, 40]
```

```text
[1, 2, 3, 4, 5] [5, 2, 3, 1, 4]
None [1, 2, 3, 4, 5]
[('Ben', 'A', 22), ('Dev', 'A', 20), ('Ana', 'B', 20), ('Cara', 'B', 19), ('Eli', 'B', 20)]
[('Ben', 'A', 22), ('Dev', 'A', 20), ('Ana', 'B', 20), ('Eli', 'B', 20), ('Cara', 'B', 19)]
[('c', 2), ('a', 1), ('b', 1)]
[('c', 2), ('b', 1), ('a', 1)]
[3, 2, 1] 3
['fig', 'date', 'kiwi', 'pear', 'apple']
['Cherry', 'apple', 'banana'] ['apple', 'banana', 'Cherry']
'<' not supported between instances of 'str' and 'int'
[1, 2, 2] [9, 8, 7]
[1, 2, 3, 4, 5, 6, 7, 8, 9]
[10, 20, 25, 30, 40]
```

Notice what each tool is for: `heapq.nsmallest` / `nlargest` for the *top k* ([heap-problems.md](../heaps-and-priority-queues/heap-problems.md)), `heapq.merge` for combining already-sorted streams (the engine of external sorting in [merge-sort.md](merge-sort.md)), and `bisect.insort` for keeping a list sorted as items arrive (each insertion is O(n) because of the shifting, but the search is O(log n) — see the Searching Algorithms module).

## 🧭 The Decision Guide

| If you need… | Use | Why |
|--------------|-----|-----|
| To sort data in Python | `sorted()` / `list.sort()` | Timsort at C speed: stable, adaptive, hard to beat |
| To sort by several fields | Stable passes (least important first) or a tuple `key` | Python's sort is guaranteed stable |
| A tiny list, or one that is almost sorted | [Insertion sort](elementary-sorts.md) | O(n + inversions); Timsort uses binary insertion sort for short runs |
| Guaranteed O(n log n) *and* stability | [Merge sort](merge-sort.md) | Predictable; also the choice for linked lists and for data on disk |
| Guaranteed O(n log n) *and* O(1) extra space | [Heap sort](heap-sort.md) | The only one with both guarantees (or introsort in practice) |
| Fast average-case sorting in place | [Quick sort](quick-sort.md), random pivot (3-way if there are many duplicates) | Tight inner loop, O(log n) stack when recursing on the smaller side |
| The k smallest or largest items | `heapq.nsmallest` / `nlargest`, or quickselect | Avoids sorting everything |
| The median or the k-th item | [Quickselect](quick-sort.md) | Expected linear time |
| The values `1..n`, or "which is missing or duplicated?" | [Cyclic placement](cyclic-sort.md) | O(n) time, O(1) space |
| Integer keys in a small range | Counting sort | O(n + k), stable |
| Fixed-width integers or equal-length strings in bulk | Radix sort | O(d(n + b)), no comparisons |
| More data than memory | External merge sort ([merge-sort.md](merge-sort.md)) | Sorted chunks merged with `heapq.merge` |
| An interview answer | Be ready to write merge sort and quick sort's partition, state complexities, explain stability, and say why `n log n` is the barrier for comparison sorts and how counting sort sidesteps it | These are the standard follow-ups |

## ✅ Verification

The counting and radix sorts were checked beyond the quick assertion above: against `sorted` on random lists of many shapes, for stability with the same harness used throughout this module, and radix sort with several bases:

```python
def as_pure(sort_in_place):
    def pure(items, key=None):
        result = list(items)
        sort_in_place(result, key)
        return result
    return pure

def check_sort(sort_function, trials=300):
    """Return (correct, stable) for sort_function(items, key) -> a new sorted list."""
    random.seed(0)
    correct = stable = True
    for _ in range(trials):
        keys = [random.randint(0, 5) for _ in range(random.randint(0, 20))]
        records = [(k, position) for position, k in enumerate(keys)]
        original = list(records)
        result = sort_function(records, key=lambda r: r[0])
        if records != original:
            correct = False
        if [r[0] for r in result] != sorted(keys):
            correct = False
        if result != sorted(original, key=lambda r: r[0]):
            stable = False
    return correct, stable

print(check_sort(lambda items, key: counting_sort(items, key, k=6)))               # (True, True)

random.seed(10)
for _ in range(3_000):
    values = [random.randint(0, random.choice([1, 10, 1_000, 1_000_000])) for _ in range(random.randint(0, 60))]
    expected = sorted(values)
    for base in (2, 10, 16, 256):
        assert radix_sort(values, base) == expected
    if values and max(values) <= 1_000:                                         # counting sort needs a small key range
        assert counting_sort(values, key=lambda x: x, k=max(values) + 1) == expected
print("radix sort (bases 2, 10, 16, 256) and counting sort agree with sorted() on 3,000 random lists")
```

```text
(True, True)
radix sort (bases 2, 10, 16, 256) and counting sort agree with sorted() on 3,000 random lists
```

## Common Mistakes

- **Writing your own sort when `sorted()` will do.** In Python it is faster, stable, and tested. Hand-written sorts are for learning, interviews, and structures without a built-in sort.
- **Writing `data = data.sort()`.** `list.sort()` returns `None`; the list was sorted in place and `data` is now `None`.
- **Assuming a sort is stable when it is not.** Selection sort, quick sort, and heap sort can reorder equal items; sorting by one field after another only works with a stable sort.
- **Using counting sort with a huge key range.** Its cost includes `k`; ten million counters for a thousand items is a bad trade.
- **Using a comparison sort's bound against a non-comparison sort.** The `n log n` limit applies to algorithms that only compare; counting, radix, and cyclic sort use extra knowledge about the keys.
- **Choosing by the best case.** An algorithm that is O(n) on sorted input (insertion sort) can still be O(n²) on the data you actually get; decide with the *worst* case or the *expected* input in mind.

## Module Summary

This module followed one question — how do we put things in order? — from first principles to practice. [Sorting Fundamentals](sorting-fundamentals.md) defined the vocabulary — stability, in-place, adaptive — and proved, by exhaustive search for small `n`, that no comparison sort can beat `⌈log₂ n!⌉` comparisons. [Elementary Sorts](elementary-sorts.md) built bubble, selection, and insertion sort and measured where each is good: selection sort's few writes, insertion sort's speed on nearly sorted input. [Merge Sort](merge-sort.md) showed divide and conquer with a guaranteed `n log n`, counted inversions, sorted data that does not fit in memory, and sorted linked lists. [Quick Sort](quick-sort.md) showed how the choice of pivot decides everything, how to survive duplicates and deep recursion, and how the same partition finds the k-th item in linear time. [Heap Sort](heap-sort.md) sorted in place with a guaranteed worst case. [Cyclic Sort](cyclic-sort.md) used values as addresses to sort permutations in O(n) and to find missing and duplicated numbers. This file added counting and radix sort and compared everything.

Carry these ideas forward:

- Know the **lower bound**: comparison sorts need about `n log₂ n` comparisons; beating it requires extra knowledge about the keys.
- **Stability** matters whenever you sort by one field after another, and only some algorithms provide it.
- **Divide and conquer** (merge sort), **partitioning** (quick sort and quickselect), **heaps** (heap sort and top-k), and **values as indexes** (cyclic, counting, and radix sort) are reusable problem-solving patterns well beyond sorting.
- In Python, **use the built-in sort**, and know why it works so well: Timsort is adaptive, stable, and implemented in C.
- Sorted data unlocks fast searching, which is the subject of the next module.

## ➡️ Next

Continue to the Searching Algorithms module, where sorted data pays off: binary search finds an item among a million in about twenty steps, and the same halving idea solves a surprising range of problems that have nothing to do with lists.
