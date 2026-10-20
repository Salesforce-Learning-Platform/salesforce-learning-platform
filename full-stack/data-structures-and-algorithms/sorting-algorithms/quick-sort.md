# ⚡ Quick Sort

## Partition First, Then Recurse

Quick sort, invented by Tony Hoare in 1959 and published in 1961, is the other great divide-and-conquer sort. Where [merge sort](merge-sort.md) splits the list blindly in half and does its real work *afterwards* (merging), quick sort does its
work *first*:

1. **Choose a pivot** — some item from the list.
2. **Partition:** rearrange the list so that everything smaller than the pivot is on its left and everything larger is on its right. The pivot is now in its **final sorted position**.
3. **Recurse** on the left part and on the right part. There is nothing to combine afterwards: when both sides are sorted, the whole list is.

```
 [ 8  3  1  7  0  10  2 ]      pivot = 2
        partition
 [ 1  0 ]  2  [ 7  3  10  8 ]  <- 2 is already in its final position
   sort        sort
```

Quick sort sorts **in place** (no merge buffer), has a very tight inner loop, and is among the fastest general-purpose sorts in practice. Its catch is that the *quality of the pivot decides everything*: a poor pivot makes the two sides lopsided and the running time
O(n²). This file implements quick sort with several pivot choices, measures what each does on different inputs, shows how to cope with duplicates and deep recursion, and adds **quickselect**, which finds the k-th smallest item without sorting everything.
All outputs were produced by running the code on CPython 3.9.

## 🧱 Partitioning (Lomuto's Scheme)

The simplest partition scheme moves the pivot out of the way (to the end), then scans once from left to right, keeping a *boundary* between "items smaller than the pivot" and "the rest". Each smaller item is swapped across the boundary; finally the pivot is
swapped into place between the two groups.

```python
import random

def pivot_last(items, low, high, key):
    return high

def pivot_first(items, low, high, key):
    return low

def pivot_middle(items, low, high, key):
    return (low + high) // 2

def pivot_random(items, low, high, key):
    return random.randint(low, high)

def pivot_median_of_three(items, low, high, key):                 # the median of the first, middle, and last items
    middle = (low + high) // 2
    return sorted([low, middle, high], key=lambda i: key(items[i]))[1]

def partition(items, low, high, key, choose):
    """Partition items[low..high] around a chosen pivot; return the pivot's final index."""
    pivot_index = choose(items, low, high, key)
    items[pivot_index], items[high] = items[high], items[pivot_index]        # move the pivot to the end
    pivot_key = key(items[high])
    boundary = low                                                            # items[low:boundary] are all < pivot
    for i in range(low, high):
        if key(items[i]) < pivot_key:
            items[i], items[boundary] = items[boundary], items[i]
            boundary += 1
    items[boundary], items[high] = items[high], items[boundary]               # put the pivot between the two groups
    return boundary

data = [8, 3, 1, 7, 0, 10, 2]
where = partition(data, 0, len(data) - 1, key=lambda x: x, choose=pivot_last)
print(data, where)                       # [1, 0, 2, 7, 3, 10, 8] 2
```

With the last item (`2`) as pivot, the partition left `[1, 0]` before it, `[7, 3, 10, 8]` after it, and returned the pivot's final index, 2. Neither side is sorted yet, but every item on the left is smaller than every item on the right,
so each side can be sorted independently. A partition makes exactly `n − 1` comparisons — each item is compared with the pivot once.

## 🔁 The Sort Itself

```python
def quick_sort(items, key=None, choose=pivot_random):
    key = key or (lambda x: x)

    def sort(low, high):
        while low < high:
            p = partition(items, low, high, key, choose)
            if p - low < high - p:                  # recurse into the SMALLER part, loop on the larger one:
                sort(low, p - 1)                    # this keeps the recursion depth at most log2(n)
                low = p + 1
            else:
                sort(p + 1, high)
                high = p - 1

    sort(0, len(items) - 1)

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

values = [38, 27, 43, 3, 9, 82, 10]
quick_sort(values)
print(values)                                       # [3, 9, 10, 27, 38, 43, 82]
print(check_sort(as_pure(quick_sort)))              # (True, False)
```

The harness (from [sorting-fundamentals.md](sorting-fundamentals.md), repeated so this file runs alone) reports quick sort as correct but **not stable**: the partition swaps items across long distances, which can reorder equal items — the same reason selection
sort is unstable. (A stable quick sort exists, but it gives up the in-place property; see below.)

The loop-on-the-larger-part trick matters in Python. Recursing into both halves makes the recursion depth as bad as the *imbalance* of the partitions, which can reach `n`. This is fine for random data and a disaster for
a bad pivot choice, as the next sections show.

## 🎯 The Pivot Decides Everything

Quick sort's work is balanced only if the pivot lands near the *middle* of the sorted order. If it keeps landing at the *edge* — the smallest or largest item — each partition removes just one item, and the total cost becomes
`(n − 1) + (n − 2) + … = n(n − 1)/2` comparisons: O(n²), no better than bubble sort. Common pivot choices:

- **First or last item:** simplest — and quadratic on already **sorted** or reverse-sorted input, which is common in real data.
- **Middle item:** handles sorted and reversed input well, but is still beaten by specially constructed inputs.
- **Random item:** the expected cost is O(n log n) for *every* input, because no input can be bad for a randomly chosen pivot (only unlucky random choices are bad, and they are extremely rare).
- **Median of three** (first, middle, last): picks a reasonable pivot cheaply; good on sorted input, but still has bad inputs.

The comparison counts for 1,000 items in four shapes show it plainly:

```python
class Counted:
    count = 0
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.count += 1
        return self.value < other.value

def comparisons(sorter, values):
    items = [Counted(v) for v in values]
    Counted.count = 0
    sorter(items)
    assert [c.value for c in items] == sorted(values)
    return Counted.count

random.seed(5)
n = 1000
shapes = {
    "random": random.sample(range(10 * n), n),
    "ascending": list(range(n)),
    "descending": list(range(n, 0, -1)),
    "all equal": [7] * n,
}
strategies = {"last": pivot_last, "first": pivot_first, "middle": pivot_middle, "random": pivot_random, "median of three": pivot_median_of_three}

print(f"{'pivot choice':>15} | " + " | ".join(f"{shape:>10}" for shape in shapes))
for name, choose in strategies.items():
    row = [comparisons(lambda items, choose=choose: quick_sort(items, choose=choose), values) for values in shapes.values()]
    print(f"{name:>15} | " + " | ".join(f"{c:>10,}" for c in row))
```

```text
   pivot choice |     random |  ascending | descending |  all equal
           last |     11,990 |    499,500 |    499,500 |    499,500
          first |     11,592 |    499,500 |    499,500 |    499,500
         middle |     10,345 |      7,987 |      8,406 |    499,500
         random |     10,610 |     10,771 |     10,605 |    499,500
median of three |     10,948 |      9,009 |     16,026 |    501,498
```

Compare each cell with `n(n − 1)/2 = 499,500` (the quadratic case) and `n·log₂ n ≈ 10,000` (the good case):

- **Last** and **first** pivots hit 499,500 on ascending and descending input — the quadratic worst case. Real data is often partly sorted, so these choices are risky.
- The **middle** pivot is excellent on ascending and descending data, and the **random** pivot is good on every shape.
- **Median of three** is good on random and ascending input, but needs 16,026 comparisons on the descending input — about 50% more than the random pivot — and specially built inputs can defeat it. (Its counts include the two or three comparisons spent choosing the median in every partition.)
- **All equal items** defeat every one of these strategies: when every item equals the pivot, none is "smaller", so each partition removes only the pivot. The fix is the three-way partition, below.

**Rule of thumb:** use a random pivot (or median of three on random-order data) unless you have a reason not to.

### The Average Case

With a random pivot, the pivot is equally likely to land at any position, and a partition costs `n − 1` comparisons, so the expected number of comparisons for `n` distinct items satisfies `C(n) = (n − 1) + (2/n)·(C(0) + C(1) + … + C(n − 1))`. The solution is
`C(n) = 2(n + 1)Hₙ − 4n`, where `Hₙ` is the n-th harmonic number — approximately `2n ln n ≈ 1.39 n log₂ n` ([Wikipedia: Quicksort](https://en.wikipedia.org/wiki/Quicksort) derives the `2n ln n` form). This table averages 30 random lists per size and compares the
measurement with the formula and with the information-theoretic minimum `⌈log₂ n!⌉`:

```python
import math

def harmonic(n):
    return sum(1 / k for k in range(1, n + 1))

def lower_bound(n):
    return math.ceil(sum(math.log2(k) for k in range(2, n + 1)))

print(f"{'n':>7} | {'measured average':>16} | {'2(n+1)H(n) - 4n':>15} | {'ceil(log2 n!)':>13} | {'measured / minimum':>18}")
for n in (100, 1_000, 10_000):
    average = sum(comparisons(quick_sort, random.sample(range(10 * n), n)) for _ in range(30)) / 30
    formula = 2 * (n + 1) * harmonic(n) - 4 * n
    print(f"{n:>7,} | {average:>16,.0f} | {formula:>15,.0f} | {lower_bound(n):>13,} | {average / lower_bound(n):>18.2f}")
```

```text
      n | measured average | 2(n+1)H(n) - 4n | ceil(log2 n!) | measured / minimum
    100 |              640 |             648 |           525 |               1.22
  1,000 |           11,041 |          10,986 |         8,530 |               1.29
 10,000 |          156,855 |         155,772 |       118,459 |               1.32
```

The measurement matches the formula, and quick sort makes roughly 20–30% more comparisons than the theoretical minimum at these sizes (the ratio creeps up towards 1.39 as `n` grows). That is noticeably more than [merge sort](merge-sort.md), which needs only
about 2% more than the minimum at `n = 1,000`; quick sort makes up for it with a tight inner loop and in-place data movement.

## 📚 Recursion Depth

A textbook quick sort recurses into **both** sides. With a bad pivot on sorted data, the left or right part has `n − 1` items, so the recursion goes `n` levels deep. Python's default limit is about 1,000 frames, so the textbook version simply crashes:

```python
def naive_quick_sort(items, low, high):
    if low >= high:
        return
    p = partition(items, low, high, lambda x: x, pivot_last)
    naive_quick_sort(items, low, p - 1)           # recurse on BOTH sides, even the huge one
    naive_quick_sort(items, p + 1, high)

for size in (500, 900, 1_100, 2_000):
    ordered = list(range(size))
    try:
        naive_quick_sort(ordered, 0, size - 1)
        print(f"{size:>5} sorted items: ok")
    except RecursionError:
        print(f"{size:>5} sorted items: RecursionError")

big = list(range(3_000))
quick_sort(big, choose=pivot_last)                # same bad pivot, but loops on the larger part
print("3,000 sorted items with the smaller-part-first version:", big == sorted(big))
```

```text
  500 sorted items: ok
  900 sorted items: ok
 1100 sorted items: RecursionError
 2000 sorted items: RecursionError
3,000 sorted items with the smaller-part-first version: True
```

The exact size at which the naive version fails depends on the interpreter's recursion limit (`sys.getrecursionlimit()`, 1,000 by default) and on how deep the call stack already is, but 1,100 sorted items is past the default limit. The smaller-part-first version
recurses only into the smaller part (which has at most half the items) and loops on the larger, so the stack never exceeds about `log₂ n` frames — even with the worst pivot. (It is still *slow* with that pivot, since the work remains quadratic, but it no longer crashes.)

## 🟰 Many Equal Items: Three-Way Partitioning

The "all equal" column above shows quick sort's second weakness: duplicates. The fix is to partition into **three** groups — smaller than, equal to, and larger than the pivot — and recurse only on the first and last. This is the *Dutch national flag*
problem. Items equal to the pivot are done and never revisited.

```python
def quick_sort_3way(items, key=None):
    key = key or (lambda x: x)

    def sort(low, high):
        while low < high:
            pivot_key = key(items[random.randint(low, high)])
            lt, i, gt = low, low, high              # items[low:lt] < pivot; items[lt:i] == pivot; items[gt+1:high+1] > pivot
            while i <= gt:
                k = key(items[i])
                if k < pivot_key:
                    items[lt], items[i] = items[i], items[lt]
                    lt += 1
                    i += 1
                elif pivot_key < k:
                    items[i], items[gt] = items[gt], items[i]
                    gt -= 1
                else:
                    i += 1                          # equal to the pivot: leave it in the middle group
            if lt - low < high - gt:                # recurse only on the strictly smaller and strictly larger groups
                sort(low, lt - 1)
                low = gt + 1
            else:
                sort(gt + 1, high)
                high = lt - 1

    sort(0, len(items) - 1)

print(f"{'input (n = 1000)':>17} | {'2-way, random pivot':>19} | {'3-way, random pivot':>19}")
for shape, values in shapes.items():
    print(f"{shape:>17} | {comparisons(quick_sort, values):>19,} | {comparisons(quick_sort_3way, values):>19,}")
```

```text
 input (n = 1000) | 2-way, random pivot | 3-way, random pivot
           random |              11,639 |              19,404
        ascending |              11,730 |              16,714
       descending |              11,606 |              18,000
        all equal |             499,500 |               2,000
```

On all-equal input, the three-way version needs exactly `2n` comparisons — a single pass, two comparisons per item — instead of 499,500. The price is visible in the other rows: an item that is not smaller than the pivot is compared with it a second time (to tell
"equal" from "larger"), so on distinct data the three-way version makes about 1.5 times as many comparisons (1.4 to 1.7 times in the table). Use it when duplicates are likely (sorting by a category, grade, or age); skip it when keys are mostly distinct. Timsort, which
Python's `sorted` uses, is merge-based and does not suffer from duplicates in this way. (The random-pivot column differs a little from the earlier table because every run draws different random pivots.)

## 🔀 A Second Partition Scheme: Hoare's

Hoare's original partition uses two indexes that start at the ends and move toward each other. The left index skips items that are already smaller than the pivot, the right index skips items that are already larger, and when both have stopped on a misplaced item
the two items are swapped. The pivot is *not* guaranteed to end up in its final position; the function returns a split point `p`, and the recursion covers `[low..p]` and `[p+1..high]`.

```python
def quick_sort_hoare(items, key=None):
    key = key or (lambda x: x)

    def partition(low, high):
        pivot_key = key(items[(low + high) // 2])      # the lower middle item as the pivot (see the note below)
        i, j = low - 1, high + 1
        while True:
            i += 1
            while key(items[i]) < pivot_key:           # move i right past items that belong on the left
                i += 1
            j -= 1
            while pivot_key < key(items[j]):           # move j left past items that belong on the right
                j -= 1
            if i >= j:
                return j                               # the indexes met or crossed: [low..j] and [j+1..high] are partitioned
            items[i], items[j] = items[j], items[i]    # both are on the wrong side: swap them

    def sort(low, high):
        while low < high:
            p = partition(low, high)
            if p - low < high - p:
                sort(low, p)
                low = p + 1
            else:
                sort(p + 1, high)
                high = p

    sort(0, len(items) - 1)

class TrackedList(list):
    writes = 0

    def __setitem__(self, index, value):
        TrackedList.writes += 1
        super().__setitem__(index, value)

def cost(sort_in_place, values):
    """Return (comparisons, element writes) used to sort `values`; a swap is two writes."""
    items = TrackedList(Counted(v) for v in values)
    Counted.count = TrackedList.writes = 0
    sort_in_place(items)
    assert [c.value for c in items] == sorted(values)
    return Counted.count, TrackedList.writes

print(f"{'n = 1000':>10} | {'Lomuto, middle pivot':>22} | {'Hoare, middle pivot':>22}")
print(f"{'':>10} | {'comparisons':>11} {'writes':>10} | {'comparisons':>11} {'writes':>10}")
for shape, values in shapes.items():
    lomuto_comparisons, lomuto_writes = cost(lambda a: quick_sort(a, choose=pivot_middle), values)
    hoare_comparisons, hoare_writes = cost(quick_sort_hoare, values)
    print(f"{shape:>10} | {lomuto_comparisons:>11,} {lomuto_writes:>10,} | {hoare_comparisons:>11,} {hoare_writes:>10,}")
```

```text
  n = 1000 |   Lomuto, middle pivot |    Hoare, middle pivot
           | comparisons     writes | comparisons     writes
    random |      10,345     14,088 |      14,150      4,684
 ascending |       7,987      9,920 |      10,975          0
descending |       8,406     11,012 |      10,976      1,000
 all equal |     499,500      3,996 |      11,862      9,864
```

Reading the table:

- **Writes.** On random data, Hoare's scheme wrote about a third as often as Lomuto's (4,684 versus 14,088) — in line with the general statement that it does three times fewer swaps on average
  ([Wikipedia: Quicksort](https://en.wikipedia.org/wiki/Quicksort)). On ascending input it wrote nothing at all: with the middle item as pivot, both indexes stop on that item at once and no swap is needed.
- **Equal items.** The indexes *stop* on items equal to the pivot and swap them, which splits an all-equal list evenly. Hoare's scheme needs about `n log₂ n` comparisons for it (11,862) instead of 499,500, at the price of 9,864 needless writes. Three-way
  partitioning avoids both the comparisons and the swaps.
- **Comparisons.** On random data Hoare's scheme made *more* comparisons here (14,150 versus 10,345) but far fewer writes. Which one matters more depends on whether comparing or moving items is the expensive part.

> **Pivot choice matters in Hoare's scheme.** The pivot must come from the *lower* middle (`(low + high) // 2`) or from the front. Take the last item as the pivot of the two-item range `[0, 1]`: the left index stops at position 1 (the pivot itself, since `1 < 1`
> is false), the right index also stops at position 1, the indexes have met, and the function returns the split point `p == high`. The recursion on `[low..p]` then receives the whole range again and never makes progress. (In a two-item range the upper middle *is* the last item, so it fails the same way.)

## 🧪 A Stable Quick Sort (With Extra Space)

Quick sort is unstable *because partitioning happens in place*. Building the three groups with list comprehensions that preserve input order gives a stable version — at the cost of O(n) extra memory, which gives up quick sort's main advantage:

```python
def quick_sort_functional(items, key=None):
    key = key or (lambda x: x)
    if len(items) <= 1:
        return list(items)
    pivot_key = key(items[random.randrange(len(items))])
    smaller = [x for x in items if key(x) < pivot_key]
    equal = [x for x in items if not key(x) < pivot_key and not pivot_key < key(x)]       # in original order
    larger = [x for x in items if pivot_key < key(x)]
    return quick_sort_functional(smaller, key) + equal + quick_sort_functional(larger, key)

print(check_sort(quick_sort_functional))                      # (True, True)
print(check_sort(as_pure(quick_sort_3way)), check_sort(as_pure(quick_sort_hoare)))      # (True, False) (True, False)
```

## 🎲 Quickselect: The k-th Smallest Without Sorting

If you only need the median, or the 10th smallest, sorting everything is wasteful. After one partition, the pivot is in its final position `p`. If `p` is the position you want, you are done; if you want something to its left, continue
**only on the left part**; otherwise only on the right. Ignoring the other side makes the expected work `n + n/2 + n/4 + … = O(n)`. The idea is also due to Hoare, who published it in 1961 as "Algorithm 65: Find"
([Wikipedia: Quickselect](https://en.wikipedia.org/wiki/Quickselect)).

```python
def quickselect(items, k, key=None):
    """The k-th smallest item (k = 0 is the smallest) in expected O(n) time. Does not modify the input."""
    key = key or (lambda x: x)
    items = list(items)
    if not 0 <= k < len(items):
        raise IndexError("k must satisfy 0 <= k < len(items)")
    low, high = 0, len(items) - 1
    while low < high:
        p = partition(items, low, high, key, pivot_random)
        if k == p:
            return items[p]
        if k < p:
            high = p - 1                                       # the answer is in the left part
        else:
            low = p + 1                                        # ...or in the right part
    return items[low]

print(quickselect([7, 10, 4, 3, 20, 15], 2))                  # 7     — the 3rd smallest
print(quickselect([5, 5, 5, 5], 3))                           # 5

random.seed(11)
print(f"{'n':>8} | {'runs':>4} | {'average comparisons per item':>28} | {'best run':>8} | {'worst run':>9}")
for n, runs in ((1_000, 200), (10_000, 100), (100_000, 30)):
    per_item = []
    for _ in range(runs):
        values = [Counted(v) for v in random.sample(range(10 * n), n)]
        Counted.count = 0
        quickselect(values, n // 2)                           # the median is the most expensive rank to find
        per_item.append(Counted.count / n)
    print(f"{n:>8,} | {runs:>4} | {sum(per_item) / len(per_item):>28.2f} | {min(per_item):>8.2f} | {max(per_item):>9.2f}")
```

```text
7
5
       n | runs | average comparisons per item | best run | worst run
   1,000 |  200 |                         3.37 |     1.59 |      6.92
  10,000 |  100 |                         3.40 |     1.58 |      5.56
 100,000 |   30 |                         3.32 |     1.75 |      5.41
```

Finding the median takes about 3.3 to 3.4 comparisons per item on average — **linear**, and the same at every size — whereas sorting needs more than ten per item at these sizes. A single run varies a lot, as the best-run and worst-run columns show, but the average is stable.
The theory agrees: for the median with random pivots the expected cost is about `(2 + 2 ln 2)·n ≈ 3.39·n` comparisons, and other ranks are cheaper ([Wikipedia: Quickselect](https://en.wikipedia.org/wiki/Quickselect)).

The worst case is O(n²) with unlucky pivots. The **median of medians** pivot rule guarantees O(n), but its overhead is high, so it is generally used only as a fallback — in *introselect*, which runs quickselect and switches to median of medians if progress is poor
([Wikipedia: Quickselect](https://en.wikipedia.org/wiki/Quickselect)). The same idea answers "top k" questions as an alternative to the heap approach in [heap-problems.md](../heaps-and-priority-queues/heap-problems.md): quickselect is O(n) expected for a single `k` but
needs the whole list in memory, while a heap of size `k` costs O(n log k) and works on a stream.

## ✅ Verification

Every variant was compared with Python's `sorted` on thousands of random lists, with many duplicates (the three-way version's reason for being), and every value of `k` was tried for quickselect:

```python
random.seed(12)
for _ in range(3000):
    values = [random.randint(0, 9) for _ in range(random.randint(0, 40))]
    expected = sorted(values)
    for name, choose in strategies.items():
        copy = list(values)
        quick_sort(copy, choose=choose)
        assert copy == expected, name
    for sorter in (quick_sort_3way, quick_sort_hoare):
        copy = list(values)
        sorter(copy)
        assert copy == expected
    assert quick_sort_functional(values) == expected
    for k in range(len(values)):
        assert quickselect(values, k) == expected[k]
for bad_k in (-1, 3):
    try:
        quickselect([1, 2, 3], bad_k)
        raise AssertionError("expected an IndexError")
    except IndexError:
        pass
print("all pivot strategies, 3-way, Hoare, functional quick sort and quickselect agree with sorted() on 3,000 random lists")
```

```text
all pivot strategies, 3-way, Hoare, functional quick sort and quickselect agree with sorted() on 3,000 random lists
```

## 🌍 Quick Sort in Practice

Pure quick sort has an O(n²) worst case, so serious library implementations harden it. **Introsort** (introspective sort) starts as quick sort, switches to [heap sort](heap-sort.md) if the recursion gets too deep (which guarantees O(n log n)), and switches to insertion
sort for small partitions; per Wikipedia, some C++ standard library implementations use it, such as the GNU C++ library with a depth limit of `2·log₂ n`
([Wikipedia: Introsort](https://en.wikipedia.org/wiki/Introsort)). Python's `sorted` is not quick sort; it is Timsort, a stable merge-based hybrid.

## ⚖️ Summary

| | Quick sort |
|--|-----------|
| Best / average time | O(n log n) (about 1.39 n log₂ n comparisons with a random pivot) |
| Worst-case time | **O(n²)** — a bad pivot sequence; rare with a random pivot |
| Extra space | O(log n) for the stack when recursing into the smaller part first |
| Stable | **No** (a functional version is, with O(n) extra space) |
| Adaptive | No |
| Handles duplicates | Poorly, unless three-way partitioning is used |
| Strengths | In place, fast in practice, sequential memory access, easily extended to quickselect |

## Common Mistakes

- **Always using the first or last item as the pivot** and then sorting already-sorted data.
- **Recursing into both sides without limiting depth**, causing `RecursionError` on adversarial or sorted input.
- **Ignoring duplicates**, so that a list with few distinct values takes O(n²).
- **Off-by-one errors in the partition boundaries**, especially mixing up Lomuto's and Hoare's conventions (Hoare's returns a split point, not the pivot's final index).
- **Assuming quick sort is stable**, or using it when stability is required.
- **Sorting a list to find the k-th element** when quickselect (or a heap) would do the job in linear time.

## ➡️ Next

Continue to [heap-sort.md](heap-sort.md), the third O(n log n) sort: it sorts in place with a guaranteed worst case — the combination that merge sort and quick sort each give up one half of.
