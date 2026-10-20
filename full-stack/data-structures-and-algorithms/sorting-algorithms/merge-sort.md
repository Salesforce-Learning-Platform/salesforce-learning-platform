# 🧬 Merge Sort

## Divide, Conquer, Merge

Merge sort is the standard example of **divide and conquer**, and the first sorting algorithm in this module to break the quadratic barrier. Its idea fits in three lines:

1. **Divide:** split the list into two halves.
2. **Conquer:** sort each half (recursively; a list of 0 or 1 items is already sorted).
3. **Combine:** **merge** the two sorted halves into one sorted list.

The work is all in the merge step, and merging two *already sorted* lists is easy and fast: keep a pointer at the front of each list and repeatedly take the smaller of the two front items. That takes one pass — `O(a + b)` time
for lists of lengths `a` and `b`. Because the list is halved at every level, the recursion is only about `log₂ n` levels deep, and each level does about `n` work in total (the picture drawn in
[recursion-tree.md](../recursion/recursion-tree.md)), giving **O(n log n) in every case** — best, average, and worst. This file implements merge sort in two ways, checks its comparison counts against the theory,
and uses the merge idea for three further jobs: counting inversions, sorting data too large for memory, and sorting linked lists. All outputs were produced by running the code on CPython 3.9.

```python
import random

def check_sort(sort_function, trials=300):
    """Return (correct, stable) for sort_function(items, key) -> a new sorted list."""
    random.seed(0)
    correct = stable = True
    for _ in range(trials):
        keys = [random.randint(0, 5) for _ in range(random.randint(0, 20))]       # few distinct keys: many ties
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
```

(The harness from [sorting-fundamentals.md](sorting-fundamentals.md), repeated so this file runs on its own.)

## 🔗 The Merge Step

```python
def merge(left, right, key):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(right[j]) < key(left[i]):         # take from the right only if STRICTLY smaller: ties go to the left list...
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])               # ...which keeps equal items in their original order: this makes merge sort stable
            i += 1
    merged.extend(left[i:])                      # one list ran out; the rest of the other is already in order
    merged.extend(right[j:])
    return merged

print(merge([1, 4, 7], [2, 3, 9, 10], key=lambda x: x))      # [1, 2, 3, 4, 7, 9, 10]
```

Two details carry the algorithm's guarantees. Merging uses at most `a + b − 1` comparisons (the last item of one list needs no comparison), and the merge is **stable** because ties are always resolved in favour of the left list, whose
items came earlier in the input.

## 📉 Top-Down Merge Sort

```python
def merge_sort(items, key=None):
    key = key or (lambda x: x)
    if len(items) <= 1:
        return list(items)                       # base case: 0 or 1 items are already sorted
    middle = len(items) // 2
    left = merge_sort(items[:middle], key)       # conquer: sort each half
    right = merge_sort(items[middle:], key)
    return merge(left, right, key)               # combine

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))    # [3, 9, 10, 27, 38, 43, 82]
```

Tracing the recursion on seven numbers shows the splitting down to single items and the merging back up:

```python
def traced(items, depth=0):
    pad = "    " * depth
    if len(items) <= 1:
        return list(items)
    middle = len(items) // 2
    print(f"{pad}split {items} -> {items[:middle]} | {items[middle:]}")
    left, right = traced(items[:middle], depth + 1), traced(items[middle:], depth + 1)
    result = merge(left, right, key=lambda x: x)
    print(f"{pad}merge {left} + {right} -> {result}")
    return result

traced([38, 27, 43, 3, 9, 82, 10])
```

```text
split [38, 27, 43, 3, 9, 82, 10] -> [38, 27, 43] | [3, 9, 82, 10]
    split [38, 27, 43] -> [38] | [27, 43]
        split [27, 43] -> [27] | [43]
        merge [27] + [43] -> [27, 43]
    merge [38] + [27, 43] -> [27, 38, 43]
    split [3, 9, 82, 10] -> [3, 9] | [82, 10]
        split [3, 9] -> [3] | [9]
        merge [3] + [9] -> [3, 9]
        split [82, 10] -> [82] | [10]
        merge [82] + [10] -> [10, 82]
    merge [3, 9] + [10, 82] -> [3, 9, 10, 82]
merge [27, 38, 43] + [3, 9, 10, 82] -> [3, 9, 10, 27, 38, 43, 82]
```

Read the indented lines as the call tree: the splits go down the left side first, and every `merge` line shows two sorted lists combining into a bigger one. The tree has about `log₂ 7 ≈ 3` levels of splitting.

## ⬆️ Bottom-Up Merge Sort (No Recursion)

The same algorithm can run iteratively: start by treating every item as a sorted run of length 1, merge adjacent pairs into runs of length 2, then 4, then 8, and so on until one run covers the whole list. This avoids recursion
altogether (so no recursion-limit worries) and shows what the recursion was really doing. It alternates between two buffers:

```python
def merge_sort_bottom_up(items, key=None):
    key = key or (lambda x: x)
    n = len(items)
    source, target = list(items), [None] * n
    width = 1                                                  # current run length
    while width < n:
        for start in range(0, n, 2 * width):                   # merge each pair of adjacent runs
            middle, end = min(start + width, n), min(start + 2 * width, n)
            i, j, k = start, middle, start
            while i < middle and j < end:
                if key(source[j]) < key(source[i]):
                    target[k] = source[j]
                    j += 1
                else:
                    target[k] = source[i]
                    i += 1
                k += 1
            while i < middle:                                  # leftovers from the left run
                target[k] = source[i]
                i += 1
                k += 1
            while j < end:                                     # leftovers from the right run
                target[k] = source[j]
                j += 1
                k += 1
        source, target = target, source                        # the merged output becomes the next round's input
        width *= 2
    return source

print(merge_sort_bottom_up([38, 27, 43, 3, 9, 82, 10]))       # [3, 9, 10, 27, 38, 43, 82]
print(check_sort(merge_sort), check_sort(merge_sort_bottom_up))        # (True, True) (True, True)
```

Both versions pass the harness: correct, and **stable**. A further check compares them on thousands of random lists, below.

## 🔢 How Many Comparisons?

For the top-down version, merging two sorted halves of sizes `⌊n/2⌋` and `⌈n/2⌉` takes at most `n − 1` comparisons, so the worst case satisfies `W(n) = W(⌊n/2⌋) + W(⌈n/2⌉) + n − 1`. That solves to
`W(n) = n⌈log₂ n⌉ − 2^⌈log₂ n⌉ + 1`. The tests below check this formula against the recurrence and, for every possible input order of up to 8 items, against the *actual* worst case found by trying all permutations:

```python
import itertools
import math

class Counted:
    count = 0
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.count += 1
        return self.value < other.value

def comparisons(sort, values):
    items = [Counted(v) for v in values]
    Counted.count = 0
    result = sort(items)
    assert [c.value for c in result] == sorted(values)
    return Counted.count

def worst_case(n):                                                      # the closed form
    return 0 if n <= 1 else n * math.ceil(math.log2(n)) - 2 ** math.ceil(math.log2(n)) + 1

def worst_case_recurrence(n):
    return 0 if n <= 1 else worst_case_recurrence(n // 2) + worst_case_recurrence(n - n // 2) + n - 1

assert all(worst_case(n) == worst_case_recurrence(n) for n in range(1, 500))
for n in range(1, 9):                                                   # try EVERY ordering of n items
    actual = max(comparisons(merge_sort, p) for p in itertools.permutations(range(n)))
    assert actual == worst_case(n), (n, actual, worst_case(n))
print("worst-case formula matches the recurrence (n < 500) and exhaustive search over all orderings (n <= 8)")
```

```text
worst-case formula matches the recurrence (n < 500) and exhaustive search over all orderings (n <= 8)
```

Now the measurement on larger inputs. The table compares merge sort's comparisons on random, ascending, and descending input with the information-theoretic minimum `⌈log₂ n!⌉` (from
[sorting-fundamentals.md](sorting-fundamentals.md)) and with the worst-case formula:

```python
def lower_bound(n):
    return math.ceil(sum(math.log2(k) for k in range(2, n + 1)))

random.seed(3)
print(f"{'n':>8} | {'ceil(log2 n!)':>13} | {'random':>10} | {'ascending':>10} | {'descending':>10} | {'worst case':>10}")
for n in (1_000, 10_000, 100_000):
    print(f"{n:>8,} | {lower_bound(n):>13,} | {comparisons(merge_sort, random.sample(range(n * 10), n)):>10,} | "
          f"{comparisons(merge_sort, range(n)):>10,} | {comparisons(merge_sort, range(n, 0, -1)):>10,} | {worst_case(n):>10,}")
```

```text
       n | ceil(log2 n!) |     random |  ascending | descending | worst case
   1,000 |         8,530 |      8,717 |      4,932 |      5,044 |      8,977
  10,000 |       118,459 |    120,476 |     64,608 |     69,008 |    123,617
 100,000 |     1,516,705 |  1,536,067 |    815,024 |    853,904 |  1,568,929
```

On random data merge sort uses only about 1–2% more comparisons than the theoretical minimum — it is close to optimal. On already ordered input (ascending or descending) it needs roughly half as many comparisons as on random input: with
sorted halves, the merge runs out of one list quickly. It never exceeds the worst-case figure, and that figure is less than twice the best case in every row, which is why merge sort's running time is so predictable. (Python's own sort goes
further: it detects ordered runs and needs only `n − 1` comparisons, as shown earlier.)

The final correctness check pits the two implementations against Python's `sorted` on thousands of random lists, with many duplicates:

```python
random.seed(8)
for _ in range(3000):
    values = [random.randint(0, 9) for _ in range(random.randint(0, 40))]
    assert merge_sort(values) == merge_sort_bottom_up(values) == sorted(values)
print("top-down, bottom-up, and sorted() agree on 3,000 random lists")
```

```text
top-down, bottom-up, and sorted() agree on 3,000 random lists
```

## 🔄 Counting Inversions

An **inversion** is a pair of items that are in the wrong order relative to each other (the same quantity that governed insertion sort in [elementary-sorts.md](elementary-sorts.md)). The number of inversions measures how far a list is from sorted,
and appears in ranking comparisons (how different are your movie rankings from mine?). Brute force checks every pair, O(n²). Merge sort counts them in **O(n log n)** with one observation: during a merge, whenever an item from the *right* half is
placed before the remaining items of the *left* half, it is smaller than every one of them, and that creates exactly `len(left) − i` inversions at once.

```python
def count_inversions(values):
    """Return (sorted list, number of inversions) in O(n log n)."""
    if len(values) <= 1:
        return list(values), 0
    middle = len(values) // 2
    left, left_count = count_inversions(values[:middle])
    right, right_count = count_inversions(values[middle:])
    merged, cross = [], 0
    i = j = 0
    while i < len(left) and j < len(right):
        if right[j] < left[i]:
            merged.append(right[j])
            j += 1
            cross += len(left) - i               # right[j] is smaller than ALL remaining left items: that many new inversions
        else:
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, left_count + right_count + cross

print(count_inversions([2, 4, 1, 3, 5])[1])      # 3     — the pairs (2,1), (4,1), (4,3)
print(count_inversions([5, 4, 3, 2, 1])[1])      # 10    — every pair: 5·4/2
print(count_inversions([1, 2, 3])[1])            # 0
```

A comparison with the brute-force count, for correctness and for speed:

```python
import timeit

def brute_force_inversions(values):
    return sum(1 for i in range(len(values)) for j in range(i + 1, len(values)) if values[i] > values[j])

for _ in range(1000):
    values = [random.randint(0, 9) for _ in range(random.randint(0, 30))]
    assert count_inversions(values)[1] == brute_force_inversions(values)

print(f"{'n':>6} | {'brute force O(n²)':>17} | {'merge-sort count':>16}   (ms)")
for n in (500, 1_000, 2_000, 4_000):
    values = random.sample(range(10 * n), n)
    brute = min(timeit.repeat(lambda: brute_force_inversions(values), number=1, repeat=3)) * 1000
    fast = min(timeit.repeat(lambda: count_inversions(values), number=1, repeat=3)) * 1000
    print(f"{n:>6,} | {brute:>17.1f} | {fast:>16.1f}")
```

Output:

```
     n | brute force O(n²) | merge-sort count   (ms)
   500 |               5.3 |              0.8
 1,000 |              21.7 |              1.7
 2,000 |              83.7 |              3.7
 4,000 |             334.1 |              8.2
```

The brute-force time quadruples with every doubling of `n`; the merge-sort count roughly doubles. The same trick — "count how many items are *jumped over* while merging" — solves a family of problems about counting pairs.

## 💾 Sorting Data Too Big for Memory (External Sorting)

Merge sort's merging step works on **streams**, reading each input once from front to back. That makes it the foundation of **external sorting**, used when the data does not fit in memory (a database sorting a huge table):
read a chunk that fits in memory, sort it, write it out as a "run", repeat; then merge all the runs in a single pass. The Python standard library already has the lazy k-way merge (see [heap-problems.md](../heaps-and-priority-queues/heap-problems.md)):

```python
import heapq

def external_sort(stream, chunk_size):
    """Sort an iterable by sorting chunks of at most chunk_size items, then merging the sorted chunks lazily."""
    runs, chunk = [], []
    for value in stream:
        chunk.append(value)
        if len(chunk) == chunk_size:
            runs.append(sorted(chunk))           # in a real system, each sorted run would be written to disk
            chunk = []
    if chunk:
        runs.append(sorted(chunk))
    return heapq.merge(*runs)                    # yields one item at a time: the result is never fully in memory

data = [random.randint(0, 99) for _ in range(1000)]
print(list(external_sort(iter(data), chunk_size=64)) == sorted(data))         # True
print(list(external_sort(iter([]), chunk_size=10)))                           # []
```

With memory for `M` items and `n` items in total, there are about `n / M` runs; the merge reads each item once, so the sort needs only a few passes over the data on disk
([Wikipedia: External sorting](https://en.wikipedia.org/wiki/External_sorting)).

## 🔗 Merge Sort on Linked Lists

Merge sort suits [linked lists](../linked-lists/common-linked-list-problems.md) particularly well. Arrays need an O(n) buffer for merging, and splitting needs random access; a linked list can be merged by *relinking* nodes (no extra
memory) and split with the slow/fast-pointer trick, so the only extra space is the O(log n) recursion stack. Quick sort and heap sort, by contrast, rely on random access.

```python
class Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def build(values):
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head

def to_list(head):
    values = []
    while head is not None:
        values.append(head.value)
        head = head.next
    return values

def merge_lists(a, b):
    dummy = tail = Node(None)
    while a is not None and b is not None:
        if b.value < a.value:
            tail.next, b = b, b.next
        else:
            tail.next, a = a, a.next             # ties come from the first list: stable
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next

def merge_sort_linked(head):
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next                 # slow ends on the last node of the first half
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    second, slow.next = slow.next, None          # cut the list into two halves
    return merge_lists(merge_sort_linked(head), merge_sort_linked(second))

print(to_list(merge_sort_linked(build([4, 2, 7, 1, 9, 3]))))     # [1, 2, 3, 4, 7, 9]
for _ in range(2000):
    values = [random.randint(0, 20) for _ in range(random.randint(0, 25))]
    assert to_list(merge_sort_linked(build(values))) == sorted(values)
```

## 🆚 Strengths and Weaknesses

| | Merge sort |
|--|-----------|
| Time | **O(n log n)** best, average, and worst case |
| Extra space | O(n) for arrays (the merge buffer); O(log n) for linked lists |
| Stable | **Yes** (with the strict `<` in the merge) |
| Adaptive | No (basic form); its relatives, natural merge sort and Timsort, are |
| Access pattern | Sequential: ideal for linked lists, files, and external memory |
| Parallelizable | Yes: the two halves are independent |

The cost is the O(n) buffer: for an in-memory array of numbers, [quick sort](quick-sort.md) sorts in place and is often faster in practice. Choose merge sort when you need a **stable** sort, a **guaranteed** O(n log n),
sequential access, or a sort of linked data.

## Common Mistakes

- **Using `<=` in the merge when taking from the right** (or testing the left with `>`), which breaks stability.
- **Forgetting the leftover items** after one list is exhausted.
- **Computing the middle incorrectly** (for odd lengths) and recursing on the same size forever — `items[:middle]` and `items[middle:]` must both be strictly shorter than `items`.
- **Merging into a list created inside every call** and not noticing the O(n) allocation per level — it is inherent to the array version, but should not become O(n²).
- **Counting inversions with `<=`**, which counts equal items as inversions.
- **Worrying about the recursion limit**: merge sort halves the problem each time, so its recursion is only about `log₂ n` levels deep — about 20 even for a million items.

## ➡️ Next

Continue to [quick-sort.md](quick-sort.md) to see the other great divide-and-conquer sort, which does its work *before* the recursion (partitioning) instead of after, sorts in place, and is the fastest general-purpose sort in many settings.
