# 🐢 Elementary Sorts: Bubble, Selection, and Insertion

## Three Simple Algorithms, All Quadratic — and Different in Useful Ways

Bubble sort, selection sort, and insertion sort are the first sorting algorithms most people meet. They are short, they sort **in place**, and they all take O(n²) time in the worst case — far too slow for large
inputs. They are worth studying anyway, for three reasons: they are easy to get right and to reason about, the differences between them (stability, adaptivity, number of writes) are exactly the vocabulary from
[sorting-fundamentals.md](sorting-fundamentals.md), and one of them, insertion sort, is a real building block: Python's own sort uses a binary variant of it for short stretches of data.

All three are written here to sort a list **in place** and to accept an optional `key`, as Python's sort does. All outputs were produced by running the code on CPython 3.9.

Two helpers used throughout: a wrapper that lets the harness treat an in-place sort as "returns a new sorted list", and the test harness from [sorting-fundamentals.md](sorting-fundamentals.md), repeated here
so this file runs on its own.

```python
import random

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

## 🫧 Bubble Sort

**Idea:** sweep through the list comparing each pair of neighbours and swapping any pair that is out of order. After one sweep, the largest item has "bubbled" to the end; after the next sweep, the second-largest
is in place; and so on. Each sweep can ignore the already-placed tail.

```python
def bubble_sort(items, key=None):
    key = key or (lambda x: x)
    for end in range(len(items) - 1, 0, -1):          # items[end + 1:] is already in its final place
        swapped = False
        for i in range(end):
            if key(items[i + 1]) < key(items[i]):     # strictly less: equal neighbours are never swapped (that is what keeps it stable)
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        if not swapped:
            break                                     # a whole sweep with no swap: the list is sorted, stop early
```

The `swapped` flag is a small but important optimization: on a list that is already sorted, the first sweep finds nothing to swap and the algorithm stops after `n − 1` comparisons. Narrating the sweeps on a small list:

```python
def bubble_sweeps(values):
    items = list(values)
    states = []
    for end in range(len(items) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if items[i + 1] < items[i]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        states.append(list(items))
        if not swapped:
            break
    return states

for number, state in enumerate(bubble_sweeps([5, 1, 4, 2, 8]), start=1):
    print(f"after sweep {number}: {state}")
```

```text
after sweep 1: [1, 4, 2, 5, 8]
after sweep 2: [1, 2, 4, 5, 8]
after sweep 3: [1, 2, 4, 5, 8]
```

After sweep 1 the largest value, `8`, was already at the end and `5` has bubbled up next to it; sweep 2 finishes the job; sweep 3 finds nothing to swap and stops. **Properties:** stable; adaptive thanks to the flag
(O(n) on sorted input); O(n²) comparisons and swaps in the average and worst cases. It does the most data movement of the three and is almost never the right choice outside teaching.

## 🎯 Selection Sort

**Idea:** find the smallest item in the unsorted part and swap it into the next position of the sorted part. The sorted part grows from the left, one item at a time.

```python
def selection_sort(items, key=None):
    key = key or (lambda x: x)
    for i in range(len(items) - 1):
        smallest = i
        for j in range(i + 1, len(items)):
            if key(items[j]) < key(items[smallest]):
                smallest = j
        if smallest != i:
            items[i], items[smallest] = items[smallest], items[i]       # at most ONE swap per position
```

**Properties:** it always does exactly `n(n − 1)/2` comparisons, whatever the input — it is **not adaptive**, and sorted input is no faster than random input. But it performs at most **n − 1 swaps**, the fewest of the
three, which matters when writing an item is expensive (for example, flash memory with limited write cycles). It is **not stable**: the long-distance swap can carry an item past equal ones, as shown in
[sorting-fundamentals.md](sorting-fundamentals.md).

## 🃏 Insertion Sort

**Idea:** the way many people sort a hand of playing cards. Keep the left part of the list sorted; take the next item and slide it left past every larger item until it fits, shifting those larger items one place right.

```python
def insertion_sort(items, key=None):
    key = key or (lambda x: x)
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and key(current) < key(items[j]):     # shift larger items right, making a gap
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current                              # drop the item into the gap

def insertion_states(values):
    items = list(values)
    states = []
    for i in range(1, len(items)):
        current, j = items[i], i - 1
        while j >= 0 and current < items[j]:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current
        states.append((current, list(items)))
    return states

for current, state in insertion_states([5, 1, 4, 2, 8]):
    print(f"insert {current}: {state}")
```

```text
insert 1: [1, 5, 4, 2, 8]
insert 4: [1, 4, 5, 2, 8]
insert 2: [1, 2, 4, 5, 8]
insert 8: [1, 2, 4, 5, 8]
```

**Properties:** **stable** (an item stops sliding as soon as it meets an item that is not strictly greater); **in place**; and strongly **adaptive**. The number of shifts equals the number of **inversions** — pairs of items
that are in the wrong order — so a nearly sorted list needs very little work: O(n + inversions). It is also **online**: it can sort items as they arrive. In the worst case (reverse order) every item slides all the way left, giving O(n²).

A variation, **binary insertion sort**, finds each insertion point with binary search, cutting the comparisons to O(n log n); the shifting still costs O(n²) time, but shifting memory is very cheap compared to comparing
objects. This is the version Python's sort uses: according to the CPython source notes (`Objects/listsort.txt`), Timsort extends short runs to a minimum length using a stable binary insertion sort, and for
inputs shorter than 64 elements it uses binary insertion sort for the whole array.

## ✅ Verifying the Three Sorts

All three were checked with the harness: correct on 300 random inputs, and stability reported honestly:

```python
for name, sort in [("bubble", bubble_sort), ("selection", selection_sort), ("insertion", insertion_sort)]:
    print(f"{name:10} (correct, stable) = {check_sort(as_pure(sort))}")
```

```text
bubble     (correct, stable) = (True, True)
selection  (correct, stable) = (True, False)
insertion  (correct, stable) = (True, True)
```

Bubble and insertion sort are stable; selection sort is correct but not stable. The harness also confirmed that none of them modified their input list beyond the intended copy.

## 🔢 Counting the Work: Comparisons and Writes

Big-O hides the differences between three algorithms with the same bound. To see them, count what each one does: the number of **comparisons** (using a wrapper that counts every `<`) and the number of **writes** to the
list (using a `list` subclass that counts every assignment — a swap is two writes). The test inputs have 1,000 items and come in five shapes:

```python
class Counted:
    count = 0
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.count += 1
        return self.value < other.value

class TrackedList(list):
    writes = 0

    def __setitem__(self, index, value):
        TrackedList.writes += 1
        super().__setitem__(index, value)

def measure(sort_in_place, values):
    items = TrackedList(Counted(v) for v in values)
    Counted.count = TrackedList.writes = 0
    sort_in_place(items)
    assert [c.value for c in items] == sorted(values)
    return Counted.count, TrackedList.writes

random.seed(2)
n = 1000
nearly = list(range(n))
for _ in range(10):                                   # ascending, but with ten random swaps
    a, b = random.randrange(n), random.randrange(n)
    nearly[a], nearly[b] = nearly[b], nearly[a]
shapes = {
    "random": random.sample(range(n), n),
    "ascending": list(range(n)),
    "descending": list(range(n, 0, -1)),
    "nearly sorted": nearly,
    "all equal": [7] * n,
}

print(f"{'input (n = 1000)':>16} | {'bubble: cmp / writes':>22} | {'selection: cmp / writes':>25} | {'insertion: cmp / writes':>25}")
for label, values in shapes.items():
    cells = []
    for sort in (bubble_sort, selection_sort, insertion_sort):
        comparisons, writes = measure(sort, values)
        cells.append(f"{comparisons:>11,} / {writes:>9,}")
    print(f"{label:>16} | " + " | ".join(cells))
```

```text
input (n = 1000) |   bubble: cmp / writes |   selection: cmp / writes |   insertion: cmp / writes
          random |     498,419 /   518,014 |     499,500 /     1,986 |     259,999 /   260,006
       ascending |         999 /         0 |     499,500 /         0 |         999 /       999
      descending |     499,500 /   999,000 |     499,500 /     1,000 |     499,500 /   500,499
   nearly sorted |     449,414 /     9,980 |     499,500 /        20 |       5,989 /     5,989
       all equal |         999 /         0 |     499,500 /         0 |         999 /       999
```

How to read the table:

- **Selection sort is the same on every row** for comparisons (499,500 = n(n − 1)/2): it ignores the input's shape. But its writes stay tiny (about `2n` or less), since it swaps at most once per position — and on
  already-sorted input it writes nothing.
- **Bubble sort** is fast (`n − 1` comparisons, no writes) only when the data is already sorted or all equal. On random data it makes about `n²/2` comparisons and about `n²/2` writes; on descending data, `n²/2` comparisons and
  nearly `n²` writes (every swap is two writes) — the most of any of the three. It is also *not* much helped by nearly sorted data: an item that must move **left** travels only one place per sweep, so the early-exit flag
  rarely triggers (449,414 comparisons in the nearly-sorted row).
- **Insertion sort** does about half the comparisons and writes of bubble sort on random data, and **very little work on nearly sorted data**: ten random swaps cost only about six thousand operations, against about half a
  million for selection sort. Its work depends on how many inversions the input has.

That relationship is exact, and can be checked: bubble sort swaps once per inversion, and insertion sort shifts once per inversion.

```python
def inversions(values):                                # brute force: pairs that are in the wrong order
    return sum(1 for i in range(len(values)) for j in range(i + 1, len(values)) if values[i] > values[j])

random.seed(4)
for _ in range(200):
    values = random.sample(range(100), random.randint(0, 40))
    count = inversions(values)
    _, bubble_writes = measure(bubble_sort, values)
    _, insertion_writes = measure(insertion_sort, values)
    assert bubble_writes == 2 * count                                       # one swap (two writes) per inversion
    assert insertion_writes == count + max(len(values) - 1, 0)              # one shift per inversion + one final write per item
print("bubble swaps = inversions and insertion shifts = inversions on 200 random lists")
```

```text
bubble swaps = inversions and insertion shifts = inversions on 200 random lists
```

## ⏱️ Measured Running Time

Quadratic growth shows up in the clock too. Each time `n` doubles, the time roughly quadruples (random input, best of three runs, in milliseconds), compared with Python's built-in `sorted` for reference:

```python
import timeit

print(f"{'n':>6} | {'bubble':>9} | {'selection':>9} | {'insertion':>9} | {'sorted()':>9}   (ms)")
for n in (250, 500, 1_000, 2_000):
    values = random.sample(range(10 * n), n)
    cells = []
    for sort in (bubble_sort, selection_sort, insertion_sort):
        cells.append(min(timeit.repeat(lambda: sort(list(values)), number=1, repeat=3)) * 1000)
    builtin = min(timeit.repeat(lambda: sorted(values), number=1, repeat=3)) * 1000
    print(f"{n:>6,} | {cells[0]:9.1f} | {cells[1]:9.1f} | {cells[2]:9.1f} | {builtin:9.3f}")
```

Output:

```
     n |    bubble | selection | insertion |  sorted()   (ms)
   250 |       4.1 |       2.9 |       2.1 |     0.007
   500 |      16.4 |      11.2 |       8.8 |     0.015
 1,000 |      71.8 |      44.4 |      34.1 |     0.034
 2,000 |     280.2 |     181.3 |     139.3 |     0.089
```

At 2,000 items the quadratic sorts take 140 to 280 milliseconds, while the built-in sort takes under a tenth of one — and the gap widens fast: extrapolating the quadratic growth, a million items would take insertion sort roughly
ten hours and bubble sort about twice that.
Insertion sort is consistently the quickest of the three here; bubble sort is the slowest.

## 🧭 Which One, If Any?

| | Bubble | Selection | Insertion |
|--|--------|-----------|-----------|
| Best case | O(n) (with the early-exit flag) | O(n²) | **O(n)** |
| Average / worst | O(n²) | O(n²) | O(n²) |
| Extra space | O(1) | O(1) | O(1) |
| Stable | **Yes** | No | **Yes** |
| Adaptive | Yes | No | **Yes** |
| Writes | Many | **At most n − 1 swaps** | Many (shifts) |
| Real use | Teaching | When writes are very costly | Small or nearly sorted data; inside hybrid sorts |

**Practical advice:** for small lists or nearly sorted data, insertion sort is a fine choice; for everything else use a real O(n log n) algorithm ([merge sort](merge-sort.md), [quick sort](quick-sort.md)) or Python's `sorted`. Bubble
sort is almost never right, but it is a popular interview warm-up, and recognising "sorted already → stop" is the one idea worth keeping from it.

## Common Mistakes

- **Using `<=` instead of `<`** in the comparison, which makes equal items swap or shift and destroys stability.
- **Off-by-one errors in the loop bounds** (`range(len(items) - 1)` for bubble and selection; starting insertion sort at index 1).
- **Forgetting the early-exit flag** in bubble sort, so a sorted list still costs O(n²).
- **Assuming selection sort is adaptive or stable** — it is neither.
- **Shifting items by repeated swapping in insertion sort**, which writes about three times as much as the shift-and-drop method.
- **Calling a quadratic sort on large data** — fine for 100 items, painful for 100,000.

## ➡️ Next

Continue to [merge-sort.md](merge-sort.md) to break the quadratic barrier with divide and conquer, reaching O(n log n) in every case.
