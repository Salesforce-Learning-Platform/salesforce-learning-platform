# ✂️ Insertion and Deletion

## Where You Change an Array Matters

[time-complexity.md](../time-and-space-complexity/time-complexity.md) stated that adding to the
*end* of an array is cheap while adding to the *front* is not. This file shows exactly why, by
writing the shifting out by hand, measuring the difference, and covering the standard ways around
it.

## 🧱 The Root Cause: Elements Must Stay Contiguous

[array-fundamentals.md](array-fundamentals.md) established that an array's elements occupy one
unbroken block, and that index arithmetic depends on that. So there can be no gap when an element is
removed and no overlap when one is added — every element **after** the change point has to move.

```python
def insert_at(items, index, value):
    items.append(None)                          # make room at the end
    for i in range(len(items) - 1, index, -1):  # shift right, starting from the back
        items[i] = items[i - 1]
    items[index] = value
```

Inserting `99` at index 1 of `[10, 20, 30, 40]`, one step at a time:

```
start:               [10, 20, 30, 40]
make room:           [10, 20, 30, 40,  _ ]
shift 40 right:      [10, 20, 30, 40, 40]
shift 30 right:      [10, 20, 30, 30, 40]
shift 20 right:      [10, 20, 20, 30, 40]
write 99 at index 1: [10, 99, 20, 30, 40]
```

Deletion is the mirror image — shift the later elements left to close the gap:

```python
def delete_at(items, index):
    removed = items[index]
    for i in range(index, len(items) - 1):      # shift left over the gap
        items[i] = items[i + 1]
    items.pop()                                  # drop the now-duplicated last slot
    return removed
```

The number of shifts is the number of elements after the change point: `n - index`. Inserting at the
end shifts nothing (O(1) amortized); inserting at index 0 shifts all `n` elements (O(n)); inserting
in the middle shifts about half of them — still O(n), because Big-O drops the constant factor.

## 📋 What the Built-Ins Cost

| Operation | Python | Cost |
|-----------|--------|------|
| Add at the end | `items.append(x)` | O(1) amortized |
| Remove from the end | `items.pop()` | O(1) |
| Insert at position `i` | `items.insert(i, x)` | O(n) |
| Remove at position `i` | `items.pop(i)` or `del items[i]` | O(n) |
| Remove the first matching value | `items.remove(x)` | O(n) to find it, then O(n) to shift |

These match the [Python Wiki's time-complexity table](https://wiki.python.org/moin/TimeComplexity)
for `list`: append O(1), pop-last O(1), pop-intermediate O(n), insert O(n), delete-item O(n).

## ⏱️ Measuring It

This script times each operation at three list sizes. Each call is paired with a `pop()` so the
list's size stays constant between runs, and `deque` is Python's double-ended queue (covered below):

```python
import timeit
from collections import deque

for size in (10_000, 100_000, 1_000_000):
    items = list(range(size))
    queue = deque(range(size))

    def append_end():
        items.append(0)
        items.pop()              # restore the size after each timed call

    def insert_front():
        items.insert(0, 0)
        items.pop()

    def appendleft():
        queue.appendleft(0)
        queue.pop()

    timings = []
    for fn in (append_end, insert_front, appendleft):
        best = min(timeit.repeat(fn, number=300, repeat=5)) / 300
        timings.append(f"{best * 1e6:9.3f}")
    print(f"{size:>9,} | {timings[0]} | {timings[1]} | {timings[2]}")
```

```
     size |    append | insert(0) | appendleft      (µs per operation)
   10,000 |     0.096 |     3.073 |     0.100
  100,000 |     0.092 |    27.773 |     0.090
1,000,000 |     0.080 |   279.755 |     0.076
```

(One run on a laptop with CPython 3.9; the heading line was added by hand, and `appendleft` means
`deque.appendleft`. Absolute numbers will differ on your machine — the *trend* is the point.)
Growing the list tenfold leaves `append` flat but makes `insert(0, ...)` roughly ten times slower:
O(1) versus O(n), visible in real timings.

## 🛠️ Ways Around the Cost

### Need fast operations at both ends? Use a deque

`collections.deque` supports appends and pops from either side in O(1), as the
[Python documentation](https://docs.python.org/3/library/collections.html) states — the flat
`appendleft` column above. The trade-off, also from the documentation: indexed access is O(1) at
the ends but slows to O(n) in the middle, so use a plain list when you need fast random access.

### Don't care about order? Delete in O(1) by swapping

```python
def remove_unordered(items, index):
    items[index] = items[-1]    # overwrite the target with the last element
    items.pop()                  # then drop the last slot — O(1), nothing shifts
```

Only valid when element order carries no meaning (a bag of tasks, a pool of IDs). It also works
when `index` *is* the last position: the element overwrites itself and is then popped.

### Removing many elements? Filter once instead of deleting repeatedly

```python
items = [x for x in items if x != target]    # one O(n) pass
```

Calling `items.remove(target)` in a loop pays an O(n) shift every time — O(n²) overall when many
elements match. A single filtering pass keeps the whole job O(n).

### Keeping a sorted array sorted? Find fast, but insert is still O(n)

```python
import bisect

sorted_scores = [55, 62, 70, 85, 91]
bisect.insort(sorted_scores, 78)
print(sorted_scores)     # [55, 62, 70, 78, 85, 91]
```

`insort` locates the position with binary search (the same idea as `binary_search` in
[what-are-algorithms.md](../introduction-to-data-structures-and-algorithms/what-are-algorithms.md)),
but the [`bisect` documentation](https://docs.python.org/3/library/bisect.html) itself notes that the
O(log n) search is dominated by the O(n) insertion step. If you insert into a sorted collection
constantly, a different structure is the better fit — a balanced search tree if you need full sorted
order, or a heap if you only ever need the smallest (or largest) element; both are covered later in
this domain.

## 🧪 Edge-Case Behavior Worth Knowing (Python)

```python
x = [1, 2]
x.insert(100, 9)      # index past the end is allowed: appends -> [1, 2, 9]

y = [1, 2]
y.insert(-100, 9)     # index far below zero is allowed: inserts at the front -> [9, 1, 2]

[].pop()              # IndexError: pop from empty list
[1].remove(5)         # ValueError: list.remove(x): x not in list
```

`insert` clamps an out-of-range index instead of raising an error, while `pop` and `remove` raise
exceptions on empty input and missing values — so check first, or handle the exception.

## Common Mistakes

- **Using `insert(0, x)` or `pop(0)` in a loop** to treat a list as a queue — every call is O(n);
  use `collections.deque` instead.
- **Calling `remove` repeatedly to delete many items**, which silently becomes O(n²).
- **Expecting `remove` to delete every match** — it removes only the *first* one.
- **Deleting while iterating forward** over the same list, which skips elements (see
  [traversal.md](traversal.md)).
- **Assuming `bisect.insort` makes sorted insertion cheap** — the search is O(log n), the shifting
  still makes the call O(n).

## ➡️ Next

Continue to [two-pointer-technique.md](two-pointer-technique.md) to see how two indexes moving
through an array can replace nested loops, and can even compact an array in place without any
repeated shifting.
