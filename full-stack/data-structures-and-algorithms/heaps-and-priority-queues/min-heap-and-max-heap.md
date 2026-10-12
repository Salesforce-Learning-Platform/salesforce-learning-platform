# ↕️ Min-Heaps and Max-Heaps

## The Same Structure, Pointing Either Way

A **min-heap** keeps the *smallest* item at the root (every parent ≤ its children). A **max-heap** keeps the *largest* item at the root (every parent ≥ its children). Everything else about them —
the array layout, sift up and sift down, the costs — is identical; only the direction of the comparison differs. Which one you need depends on the question: "the cheapest", "the earliest", "the
nearest" want a min-heap; "the largest", "the highest score", "the heaviest" want a max-heap.

Python's standard library provides the `heapq` module, which implements **min-heap operations on a plain list**. This file tours it, shows how to get max-heap behaviour (and how to order tuples
and objects, which is where most heap bugs hide), and checks the result against brute-force definitions. All outputs were produced by running the code on CPython 3.9.

## 🧰 The `heapq` Module

The Python documentation describes `heapq` as an implementation of the heap queue algorithm, in which min-heaps are binary trees where every parent has a value less than or equal to any of its
children (the *heap invariant*), stored in a list. Heaps are ordinary lists that you pass to `heapq` functions:

```python
import heapq

heap = []
for value in [5, 3, 8, 1, 9, 2]:
    heapq.heappush(heap, value)            # O(log n)
print(heap)                                # [1, 3, 2, 5, 9, 8]  — a heap, NOT a sorted list
print(heap[0])                             # 1      — the smallest item is always at index 0
print(heapq.heappop(heap), heap)           # 1 [2, 3, 8, 5, 9]    — pop the smallest: O(log n)

numbers = [9, 4, 7, 1, 8, 2]
heapq.heapify(numbers)                     # rearrange an existing list into a heap, in place, in O(n)
print(numbers)                             # [1, 4, 2, 9, 8, 7]
print([heapq.heappop(numbers) for _ in range(len(numbers))])    # [1, 2, 4, 7, 8, 9]
```

The module's main functions:

| Function | What it does | Cost |
|----------|--------------|------|
| `heapq.heappush(heap, item)` | Add an item | O(log n) |
| `heapq.heappop(heap)` | Remove and return the smallest item | O(log n) |
| `heap[0]` | Look at the smallest without removing it | O(1) |
| `heapq.heapify(list)` | Turn a list into a heap in place | O(n) |
| `heapq.heappushpop(heap, item)` | Push, then pop the smallest — faster than doing both separately | O(log n) |
| `heapq.heapreplace(heap, item)` | Pop the smallest, then push — the heap size stays the same | O(log n) |
| `heapq.nsmallest(k, iterable, key=None)` / `nlargest` | The `k` smallest / largest items | about O(n log k) |
| `heapq.merge(*sorted_iterables)` | Lazily merge sorted inputs into one sorted stream | O(n log m) for `m` inputs |

`heappushpop` and `heapreplace` differ in order: `heappushpop` pushes first, so if the new item is smaller than the current minimum, it comes straight back out; `heapreplace` pops first, so it
always returns the old minimum even if the new item is smaller.

```python
h = [3, 5, 8]
heapq.heapify(h)
print(heapq.heappushpop(h, 1), h)          # 1 [3, 5, 8]    — 1 was pushed and immediately popped: the heap is unchanged
h = [3, 5, 8]
heapq.heapify(h)
print(heapq.heapreplace(h, 1), h)          # 3 [1, 5, 8]    — the old minimum 3 is returned; 1 takes its place
```

These two are the right tools for **keeping the `k` largest items**: hold them in a min-heap of size `k`; for each new item, if it beats the smallest of the kept items, `heapreplace` swaps it in
(used in [heap-problems.md](heap-problems.md)).

### `nsmallest`, `nlargest`, and `merge`

```python
data = [5, 1, 8, 3, 9, 2, 7]
print(heapq.nsmallest(3, data))            # [1, 2, 3]
print(heapq.nlargest(3, data))             # [9, 8, 7]
words = ["pear", "fig", "banana", "kiwi", "apple"]
print(heapq.nsmallest(2, words, key=len))  # ['fig', 'pear']       — the two shortest words
print(list(heapq.merge([1, 4, 9], [2, 3, 10], [0, 5])))     # [0, 1, 2, 3, 4, 5, 9, 10]
```

The documentation says `nsmallest` and `nlargest` perform best for smaller values of `n`; for larger values it is more efficient to use `sorted()`, and when `n == 1` use `min()` or `max()`. A
measurement on a million random floats shows exactly that (milliseconds, best of two runs):

```python
import random
import timeit

random.seed(3)
big = [random.random() for _ in range(1_000_000)]
print(f"{'k':>9} | {'sorted(data)[:k]':>16} | {'heapq.nsmallest':>15}   (ms)")
for k in (1, 10, 1_000, 100_000, 1_000_000):
    t_sorted = min(timeit.repeat(lambda: sorted(big)[:k], number=1, repeat=2)) * 1000
    t_heap = min(timeit.repeat(lambda: heapq.nsmallest(k, big), number=1, repeat=2)) * 1000
    print(f"{k:>9,} | {t_sorted:16.1f} | {t_heap:15.1f}")
```

Output:

```
        k | sorted(data)[:k] | heapq.nsmallest   (ms)
        1 |            134.8 |             6.7
       10 |            131.0 |            13.2
    1,000 |            137.2 |            15.6
  100,000 |            133.4 |           242.5
1,000,000 |            138.9 |           138.1
```

For small `k`, `nsmallest` is about ten times faster than sorting the whole list (it keeps a heap of size `k`, so O(n log k)); at `k = 100,000` it is slower than sorting; and at `k` equal to the whole list
the two are the same, because `nsmallest` falls back to sorting. Moral: use a heap to pick out a *few* extremes, not to sort most of the data.

## ⬆️ Getting a Max-Heap

On Python versions before 3.14, `heapq` provides only min-heap functions. (According to the documentation, Python 3.14 added a parallel set of max-heap functions — `heapify_max`, `heappush_max`,
`heappop_max`, and so on. The examples here were run on Python 3.9 and use techniques that work on every version.) There are two standard ways to get max-heap behaviour from a min-heap.

### Technique 1: Negate Numbers

The largest number is the one whose negation is smallest. Store `-x`, and negate again when you read:

```python
class MaxHeap:
    """A max-heap of numbers built on heapq's min-heap functions."""

    def __init__(self, items=()):
        self._heap = [-x for x in items]
        heapq.heapify(self._heap)

    def push(self, value):
        heapq.heappush(self._heap, -value)

    def pop(self):
        return -heapq.heappop(self._heap)

    def peek(self):
        return -self._heap[0]

    def __len__(self):
        return len(self._heap)

top = MaxHeap([5, 3, 8, 1])
top.push(10)
print(top.peek(), len(top))                           # 10 5
print([top.pop() for _ in range(len(top))])           # [10, 8, 5, 3, 1]
```

This works for any numbers, including floats and (with care) mixed signs. It does not work for strings or arbitrary objects, which cannot be negated.

### Technique 2: Reverse the Comparison

For values that can be compared but not negated (strings, tuples, custom objects), wrap each item in a small class whose `<` is flipped. Then the heap's "smallest" is the wrapper's "largest":

```python
class Reversed:
    """Wrap a value so that a min-heap treats the LARGEST value as the smallest."""
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return other.value < self.value          # the comparison is flipped

heap = []
for word in ["pear", "fig", "banana", "kiwi"]:
    heapq.heappush(heap, Reversed(word))
print([heapq.heappop(heap).value for _ in range(len(heap))])    # ['pear', 'kiwi', 'fig', 'banana']
```

The words come out in descending alphabetical order. The heap only ever uses `<`, so defining `__lt__` is enough.

## 🎫 Prioritizing Tuples and Objects

Real heaps usually store *tasks with priorities*, not bare numbers. The convention is to push **tuples** `(priority, item)`, because Python compares tuples element by element: first the priorities, and
only if they tie, the items.

```python
tasks = []
heapq.heappush(tasks, (2, "write report"))
heapq.heappush(tasks, (1, "fix outage"))
heapq.heappush(tasks, (3, "lunch"))
print(heapq.heappop(tasks))                 # (1, 'fix outage')
print(heapq.heappop(tasks))                 # (2, 'write report')
```

For a **max-priority** order, negate the priority: push `(-priority, item)`.

### The Tie Trap

When two tuples have equal priorities, Python falls through to comparing the *second* elements. If those cannot be compared — dictionaries, custom objects without `__lt__` — the push raises an error:

```python
tasks = []
heapq.heappush(tasks, (1, {"name": "a"}))
try:
    heapq.heappush(tasks, (1, {"name": "b"}))      # TypeError: '<' not supported between instances of 'dict' and 'dict'
except TypeError as error:
    print(error)
```

```text
'<' not supported between instances of 'dict' and 'dict'
```

Even when items *can* be compared (say, strings), ties are then broken alphabetically, which is rarely the order you want. The standard cure, also recommended in the `heapq` documentation's notes on
priority queues, is a **tie-breaker counter**: put an ever-increasing number between the priority and the item. No two counters are equal, so the item is never compared, and equal priorities come out in
insertion order (first in, first out):

```python
import itertools

counter = itertools.count()
tasks = []
for priority, name in [(2, "b"), (1, "a"), (2, "c"), (1, "d")]:
    heapq.heappush(tasks, (priority, next(counter), {"name": name}))
print([heapq.heappop(tasks)[2]["name"] for _ in range(len(tasks))])     # ['a', 'd', 'b', 'c']
```

Priority 1 items (`a`, `d`) come first, in the order they were added, and then the priority 2 items (`b`, `c`), also in insertion order. The same counter idea is built into the priority queue of the next file.

## ✅ Verification

The `MaxHeap` and the `Reversed` wrapper are checked against sorting, and `heapq.nsmallest` / `nlargest` / `merge` against their documented equivalents (`sorted(...)[:n]`), on random inputs:

```python
import random

random.seed(4)
for _ in range(5000):
    items = [random.randint(-20, 20) for _ in range(random.randint(0, 30))]

    mh = MaxHeap(items)
    assert [mh.pop() for _ in range(len(mh))] == sorted(items, reverse=True)

    words = ["".join(random.choice("abc") for _ in range(random.randint(1, 3))) for _ in range(random.randint(0, 20))]
    h = []
    for w in words:
        heapq.heappush(h, Reversed(w))
    assert [heapq.heappop(h).value for _ in range(len(h))] == sorted(words, reverse=True)

    k = random.randint(0, 10)
    assert heapq.nsmallest(k, items) == sorted(items)[:k]
    assert heapq.nlargest(k, items) == sorted(items, reverse=True)[:k]
    assert heapq.nsmallest(k, items, key=abs) == sorted(items, key=abs)[:k]          # ties keep first-come order, like sorted

    streams = [sorted(random.randint(0, 9) for _ in range(random.randint(0, 6))) for _ in range(random.randint(1, 4))]
    assert list(heapq.merge(*streams)) == sorted(x for s in streams for x in s)
print("MaxHeap, Reversed, nsmallest, nlargest and merge agree with sorting on 5,000 random inputs")
```

```text
MaxHeap, Reversed, nsmallest, nlargest and merge agree with sorting on 5,000 random inputs
```

## ⚖️ Min-Heap or Max-Heap?

| You need the… | Use | Typical use |
|---------------|-----|-------------|
| Smallest / earliest / cheapest / nearest first | Min-heap (`heapq` directly) | Task schedulers, Dijkstra's shortest path, merging sorted streams |
| Largest / highest / heaviest first | Max-heap (negate or reverse) | "Top scorer" queues, simulations with the biggest item first |
| The `k` **largest** items of a stream | A **min**-heap of size `k` | Top-k queries ([heap-problems.md](heap-problems.md)) |
| The `k` **smallest** items of a stream | A **max**-heap of size `k` | Nearest-k queries |
| The median of a stream | One of each ([heap-problems.md](heap-problems.md)) | Running statistics |

The counter-intuitive row: to keep the `k` *largest* items you use a *min*-heap, because the item you may need to throw away is the smallest of the ones kept — and that is exactly what a min-heap hands you in O(1).

## Common Mistakes

- **Treating the heap list as sorted** (printing or slicing it and expecting order). Only `heap[0]` is meaningful; pop to get the order.
- **Calling `heapq` functions on a list that is not a heap** — `heappush` and `heappop` assume the invariant; call `heapify` first on arbitrary lists.
- **Modifying a heap's list directly** (`heap[2] = x`, `heap.sort()` is fine but `heap.remove(x)` is not) and breaking the invariant. Use the `heapq` functions.
- **Pushing tuples with uncomparable second elements** and hitting the tie `TypeError`; add a counter.
- **Negating the priority but forgetting to negate it back** when reading the value.
- **Using `nsmallest`/`nlargest` with a large `k`**, which is slower than sorting.
- **Forgetting that `heapq` is a min-heap only on Python before 3.14**, and expecting a `max_heap` helper to exist.

## ➡️ Next

Continue to [priority-queues.md](priority-queues.md) to see the abstract data type that heaps implement, compare it with the alternatives (with measurements), and build a priority queue with stable ordering and priority updates.
