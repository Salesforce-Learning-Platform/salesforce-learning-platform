# 🏔️ Heap Sort

## Sorting in Place With a Max-Heap

The [Heaps and Priority Queues](../heaps-and-priority-queues/README.md) module showed that repeatedly popping a heap yields items in sorted order, and gave a simple `heap_sort` that needs O(n) extra space for the heap ([heap-fundamentals.md](../heaps-and-priority-queues/heap-fundamentals.md)). This file finishes the story with the classic **in-place** version, which sorts inside the original array with O(1) extra space and a guaranteed O(n log n) running time — the one property that [merge sort](merge-sort.md) (extra memory) and [quick sort](quick-sort.md) (quadratic worst case) each lack.

The trick is to keep two regions in the same array and to use a **max**-heap, so that the largest item can be parked at the far end:

```
 index:   0 ........................ end-1 | end ..................... n-1
          [  max-heap (still unsorted)    ] [  sorted, in final positions  ]
```

1. **Build** a max-heap out of the whole array. A max-heap stores each parent at least as large as its children, so the largest item is at index 0.
2. **Repeat `n − 1` times:** swap the root (the maximum) with the last item of the heap region, shrink the heap region by one (the maximum is now in its final position), and **sift** the new root down to repair the heap.

The heap lives in the array using the usual index arithmetic: the children of index `i` are `2i + 1` and `2i + 2`.

```python
def sift_down(items, root, end, key):
    """Move items[root] down until the subtree rooted there is a max-heap, looking only at items[:end]."""
    while True:
        child = 2 * root + 1                                  # the left child
        if child >= end:
            return                                            # root has no children inside the heap
        if child + 1 < end and key(items[child]) < key(items[child + 1]):
            child += 1                                        # the right child is larger: compare against that one
        if not key(items[root]) < key(items[child]):
            return                                            # root >= its larger child: the heap property holds
        items[root], items[child] = items[child], items[root]
        root = child

def heap_sort(items, key=None):
    key = key or (lambda x: x)
    n = len(items)
    for root in range(n // 2 - 1, -1, -1):                    # phase 1: build the heap, starting at the last parent
        sift_down(items, root, n, key)
    for end in range(n - 1, 0, -1):                           # phase 2: move the maximum to the end, shrink the heap
        items[0], items[end] = items[end], items[0]
        sift_down(items, 0, end, key)

def trace_heap_sort(values):
    items = list(values)
    n = len(items)
    identity = lambda x: x
    lines = [f"start                 {items}"]
    for root in range(n // 2 - 1, -1, -1):
        sift_down(items, root, n, identity)
    lines.append(f"max-heap built        {items}")
    for end in range(n - 1, 0, -1):
        items[0], items[end] = items[end], items[0]
        sift_down(items, 0, end, identity)
        lines.append(f"{items[end]} moved to slot {end}     {items[:end]} | {items[end:]}")
    return "\n".join(lines)

print(trace_heap_sort([5, 3, 8, 1, 9, 2]))
```

```text
start                 [5, 3, 8, 1, 9, 2]
max-heap built        [9, 5, 8, 1, 3, 2]
9 moved to slot 5     [8, 5, 2, 1, 3] | [9]
8 moved to slot 4     [5, 3, 2, 1] | [8, 9]
5 moved to slot 3     [3, 1, 2] | [5, 8, 9]
3 moved to slot 2     [2, 1] | [3, 5, 8, 9]
2 moved to slot 1     [1] | [2, 3, 5, 8, 9]
```

In the trace, the part to the right of the `|` is the sorted region and grows by one slot at every step. After the build, the root `9` is the maximum; the first extraction swaps it with the last item, `2`, then sifts `2` down until the remaining five items form a heap again (`8` rises to the root). Notice that nothing is ever allocated: the sorted region and the heap share one array.

## 🏗️ Phase 1: Building the Heap in O(n)

Leaves are already one-item heaps, so the build starts at the last item that has a child — index `n // 2 − 1` — and sifts each parent down, working back to the root. This is Floyd's heap construction. It costs **O(n)**, not O(n log n): most nodes sit near the bottom of the tree and sift down only a step or two; only a few nodes near the top sift a long way. The bound is `2n` comparisons: a node at height `h` needs at most `2h` comparisons, and at most `n / 2^(h+1)` nodes (rounded up) have height `h`. (The [heap-fundamentals.md](../heaps-and-priority-queues/heap-fundamentals.md) file measured this against building by repeated pushes.)

## 🔁 Phase 2: Extracting the Maximum

Each of the `n − 1` extractions swaps the root with the last heap item and sifts it down. The sift-down follows one root-to-leaf path of at most `log₂ n` levels, and at each level it makes two comparisons (the two children against each other, then the larger child against the item being sifted). That makes at most about `2 log₂ n` comparisons per extraction, so phase 2 costs O(n log n) in every case. The next block counts the real number of comparisons in each phase, and relates it to the minimum any comparison sort needs, `⌈log₂ n!⌉` (see [sorting-fundamentals.md](sorting-fundamentals.md)):

```python
import math
import random

class Counted:
    count = 0
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.count += 1
        return self.value < other.value

def lower_bound(n):
    return math.ceil(sum(math.log2(k) for k in range(2, n + 1)))

def heap_sort_phases(values):
    """Sort `values` with heap_sort and return (comparisons in phase 1, comparisons in phase 2)."""
    items = [Counted(v) for v in values]
    key = lambda x: x
    n = len(items)
    Counted.count = 0
    for root in range(n // 2 - 1, -1, -1):
        sift_down(items, root, n, key)
    build = Counted.count
    for end in range(n - 1, 0, -1):
        items[0], items[end] = items[end], items[0]
        sift_down(items, 0, end, key)
    assert [c.value for c in items] == sorted(values)
    return build, Counted.count - build

random.seed(5)
print(f"{'n':>8} | {'build':>9} | {'build / n':>9} | {'extract':>10} | {'total':>10} | {'total / minimum':>15}")
for n in (100, 1_000, 10_000, 100_000):
    build, extract = heap_sort_phases(random.sample(range(10 * n), n))
    print(f"{n:>8,} | {build:>9,} | {build / n:>9.2f} | {extract:>10,} | {build + extract:>10,} | {(build + extract) / lower_bound(n):>15.2f}")
```

```text
       n |     build | build / n |    extract |      total | total / minimum
     100 |       175 |      1.75 |        859 |      1,034 |            1.97
   1,000 |     1,864 |      1.86 |     14,978 |     16,842 |            1.97
  10,000 |    18,837 |      1.88 |    216,634 |    235,471 |            1.99
 100,000 |   188,324 |      1.88 |  2,831,489 |  3,019,813 |            1.99
```

Three facts stand out:

- **Phase 1 is linear:** between 1.75 and 1.9 comparisons per item at every size, under the `2n` ceiling.
- **Phase 2 dominates:** it makes roughly 1.3 to 1.7 times `log₂ n` comparisons per item at these sizes (the bound is `2 log₂ n`).
- **Heap sort uses about twice the minimum number of comparisons.** [Merge sort](merge-sort.md) came within about 2% of the minimum on random data and [quick sort](quick-sort.md) within about 30%; this top-down heap sort needs about 100% more. A variant called *bottom-up heapsort* saves many of these comparisons, although a 2008 re-evaluation found it no faster than the top-down version for integer keys, presumably because modern branch prediction makes the avoided comparisons cheap ([Wikipedia: Heapsort](https://en.wikipedia.org/wiki/Heapsort)).

## 🔬 Properties: Stability, Input Shape, and Space

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

print(check_sort(as_pure(heap_sort)))                       # (True, False)

random.seed(6)
n = 1_000
shapes = {
    "random": random.sample(range(10 * n), n),
    "ascending": list(range(n)),
    "descending": list(range(n, 0, -1)),
    "all equal": [7] * n,
    "5 distinct values": [random.randint(0, 4) for _ in range(n)],
}
print(f"{'input (n = 1000)':>18} | {'comparisons':>11}")
for shape, values in shapes.items():
    build, extract = heap_sort_phases(values)
    print(f"{shape:>18} | {build + extract:>11,}")
```

```text
(True, False)
  input (n = 1000) | comparisons
            random |      16,841
         ascending |      17,583
        descending |      15,965
         all equal |       2,994
 5 distinct values |      14,132
```

- **Not stable.** The long-distance swaps in the extraction phase reorder equal items (the harness reports `(True, False)`: correct but not stable). To sort records by one field while keeping ties in their original order, use a stable sort such as [merge sort](merge-sort.md) or Python's own.
- **Not adaptive.** Sorted input costs as much as random input (ascending is even slightly more expensive here); the heap is rebuilt from scratch regardless. Contrast this with [insertion sort](elementary-sorts.md).
- **All-equal input is the one cheap case:** about `3n` comparisons, because with equal keys every sift-down stops after its first level (at most two comparisons). Wikipedia lists the same best case, O(n) for equal keys ([Wikipedia: Heapsort](https://en.wikipedia.org/wiki/Heapsort)).
- **In place and non-recursive:** O(1) extra space and no recursion depth to worry about.

## 🆚 Heap Sort Among the n log n Sorts

| | Heap sort | [Merge sort](merge-sort.md) | [Quick sort](quick-sort.md) |
|--|-----------|------------|------------|
| Worst-case time | **O(n log n)** | **O(n log n)** | O(n²) |
| Extra space | **O(1)** | O(n) (arrays) | O(log n) |
| Stable | No | **Yes** | No |
| Comparisons (random data, relative to the minimum) | about 2× | about 1.02× | about 1.3× |
| Memory access pattern | Scattered | Sequential | Sequential |

Heap sort is the only one of the three that guarantees both O(n log n) time and O(1) extra space, which is why *introsort* — the hybrid mentioned in [quick-sort.md](quick-sort.md) — switches to heap sort when quick sort's recursion gets too deep. Its weakness is **poor locality of reference**: the sift-down jumps from `i` to `2i + 1`, far across the array, so on real hardware it is typically slower than a well-implemented quick sort — Wikipedia puts the gap at a factor of 2 to 3 ([Wikipedia: Heapsort](https://en.wikipedia.org/wiki/Heapsort)). The timing benchmark in [choosing-a-sorting-algorithm.md](choosing-a-sorting-algorithm.md) shows what this looks like in Python, where interpreter overhead hides much of the hardware effect.

## ✅ Verification

The in-place `heap_sort` was compared with `sorted` on thousands of random lists (including empty, single-item, and many-duplicate lists), and its output was checked with the `key` parameter against a stable reference ordering of the keys:

```python
random.seed(8)
for _ in range(5_000):
    values = [random.randint(0, 12) for _ in range(random.randint(0, 40))]
    copy = list(values)
    heap_sort(copy)
    assert copy == sorted(values)
    records = [(v, position) for position, v in enumerate(values)]
    heap_sort(records, key=lambda r: r[0])
    assert [r[0] for r in records] == sorted(values)
print("heap_sort agrees with sorted() on 5,000 random lists")
```

```text
heap_sort agrees with sorted() on 5,000 random lists
```

## Common Mistakes

- **Using a min-heap for an ascending in-place sort.** To place the largest item at the end of the array you need a **max**-heap. (`heapq` only provides a min-heap, which is one reason the in-place version is written by hand.)
- **Letting `sift_down` look past the heap region.** After each extraction the sorted region is part of the array but not of the heap; the `end` bound must shrink with it.
- **Starting the build at the wrong index.** The last parent is `n // 2 − 1`; starting at `n − 1` wastes work, and stopping before index 0 leaves the root unrepaired.
- **Wrong child arithmetic.** In a zero-based array the children of `i` are `2i + 1` and `2i + 2` (the `2i` and `2i + 1` formulas belong to one-based arrays).
- **Expecting stability or adaptivity.** Heap sort offers neither.

## ➡️ Next

Continue to [cyclic-sort.md](cyclic-sort.md) for a very different kind of sort: when the values are the integers 1 to n, they can be placed directly in their correct positions in O(n) time — and the technique solves a family of "find the missing number" problems.
