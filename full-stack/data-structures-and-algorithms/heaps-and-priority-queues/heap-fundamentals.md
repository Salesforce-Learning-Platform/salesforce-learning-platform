# 🏔️ Heap Fundamentals

## Fast Access to the Smallest Item, Without Full Sorting

Many programs repeatedly need "the smallest item right now": the next task to run, the nearest unvisited city, the lowest-priced offer, the earliest event. A sorted array finds the
smallest in O(1) but needs O(n) to insert a new item (shifting). An unsorted array inserts in O(1) but needs O(n) to find the smallest. A
[balanced BST](../binary-search-trees/balanced-bsts.md) does both in O(log n), but with considerable machinery. A **heap** is the lightweight answer: it gives the smallest item in **O(1)**
and supports insertion and removal of the smallest in **O(log n)**, using nothing but a plain array.

The trick is to demand *less* order than a sorted structure. A heap does not keep all items sorted; it only guarantees that **no parent is larger than its children**. This file
defines the heap property, shows how a heap lives in an array, builds one from scratch (`push`, `pop`, and a linear-time `heapify`), measures why that linear time matters,
and uses a heap to sort. All outputs were produced by running the code on CPython 3.9.

## 📐 The Heap Property

A **min-heap** is a [complete binary tree](../trees/binary-trees.md) in which **every node's key is less than or equal to the keys of its children**. (A max-heap reverses the
inequality; see [min-heap-and-max-heap.md](min-heap-and-max-heap.md).) Two consequences:

- The **minimum is always at the root** — every other node has an ancestor chain leading up to it, and keys only grow going down.
- There is **no ordering between siblings** or between "cousins": `9` may sit above `12` in one branch while an unrelated `10` sits elsewhere. That is why a heap is cheaper to maintain than a BST.

```
              2                      As an array (level by level):
           /     \
         5         3                  index:  0  1  2  3  4  5  6  7
        / \       / \                 value:  2  5  3  9  6  8  4  11
       9   6     8   4
      /
     11                               parent of i = (i - 1) // 2     children: 2i + 1 and 2i + 2
```

Because the tree is **complete** (every level full except possibly the last, filled left to right), it needs no pointers: node `i` lives at `array[i]`, its parent at `(i − 1) // 2`, and its
children at `2i + 1` and `2i + 2` — the array layout described in [binary-trees.md](../trees/binary-trees.md). A heap is therefore a Python
list plus two small repair routines.

## 🔧 Two Repair Operations: Sift Up and Sift Down

Inserting or removing an item can break the heap property in exactly one place, and each repair walks **one path** of the tree, which has only about log₂ n nodes:

- **Sift up (after inserting).** Add the new item at the end of the array (the next free spot of the bottom level, keeping the tree complete). If it is smaller than its parent, swap them; repeat
  until it is not smaller than its parent or reaches the root.
- **Sift down (after removing the minimum).** Take the last item and put it at the root (again keeping the tree complete). If it is larger than its smaller child, swap with that child; repeat until
  it is no larger than both children or reaches a leaf.

```
Start (array [2, 5, 3, 9, 6, 8, 4, 11]):

              2
           /     \
         5         3
        / \       / \
       9   6     8   4
      /
     11

push(1): append 1 at index 8, then sift it up
  1 < its parent 9  → swap;   1 < its parent 5 → swap;   1 < its parent 2 → swap;   it is the root.
  Result [1, 2, 3, 5, 6, 8, 4, 11, 9]:

              1
           /     \
         2         3
        / \       / \
       5   6     8   4
      / \
     11  9

pop() from the START heap: remove 2, move the last item (11) to the root, then sift it down
  children of 11 are 5 and 3 → swap with the smaller (3);   then its children are 8 and 4 → swap with the smaller (4);   it is now a leaf.
  Result [3, 5, 4, 9, 6, 8, 11]:

              3
           /     \
         5         4
        / \       / \
       9   6     8   11
```

Each step moves the item one level, so both operations take **O(log n)** time. Rather than swapping at every step, the code below moves the *other* items and writes the traveller once at the end
(fewer assignments).

## 🧱 A Min-Heap in Python

```python
class MinHeap:
    def __init__(self, items=()):
        self._data = list(items)
        for i in range(len(self._data) // 2 - 1, -1, -1):     # heapify: sift down every internal node, last one first
            self._sift_down(i)

    def __len__(self):
        return len(self._data)

    def peek(self):                                           # O(1): the minimum is always at index 0
        if not self._data:
            raise IndexError("peek at empty heap")
        return self._data[0]

    def push(self, item):                                     # O(log n)
        self._data.append(item)                               # keeps the tree complete
        self._sift_up(len(self._data) - 1)

    def pop(self):                                            # O(log n): remove and return the minimum
        data = self._data
        if not data:
            raise IndexError("pop from empty heap")
        smallest = data[0]
        last = data.pop()                                     # take the last item off the end...
        if data:
            data[0] = last                                    # ...put it at the root...
            self._sift_down(0)                                # ...and repair downward
        return smallest

    def _sift_up(self, i):
        data = self._data
        item = data[i]
        while i > 0:
            parent = (i - 1) // 2
            if data[parent] <= item:
                break                                         # the heap property holds here
            data[i] = data[parent]                            # pull the parent down
            i = parent
        data[i] = item

    def _sift_down(self, i):
        data = self._data
        n = len(data)
        item = data[i]
        while True:
            child = 2 * i + 1                                 # the left child
            if child >= n:
                break                                         # no children: i is a leaf
            if child + 1 < n and data[child + 1] < data[child]:
                child += 1                                    # the right child is smaller: use it
            if data[child] >= item:
                break                                         # the heap property holds here
            data[i] = data[child]                             # pull the smaller child up
            i = child
        data[i] = item

def is_min_heap(items):                                       # check the property on a plain list
    return all(items[(i - 1) // 2] <= items[i] for i in range(1, len(items)))

heap = MinHeap()
for value in [5, 3, 8, 1, 9, 2]:
    heap.push(value)
print(heap.peek(), len(heap))                                 # 1 6
print([heap.pop() for _ in range(len(heap))])                 # [1, 2, 3, 5, 8, 9]
print(heap._data, is_min_heap(heap._data))                    # [] True
```

Observe the two phrases that define the structure: after a `push`, the new item is **sifted up**; after a `pop`, the last item is moved to the root and **sifted down**. In `_sift_down`, always compare against
the *smaller* child — swapping with the larger one would leave the smaller child sitting beneath a bigger parent and break the heap property. Popping repeatedly returns the items in
ascending order, even though the underlying list is never fully sorted.

A heap's internal list is **not sorted**. After pushing `5, 3, 8, 1, 9, 2` it looks like `[1, 3, 2, 5, 9, 8]`: the smallest is first, but `3` precedes `2`. Only the parent-versus-child rule holds.

The two pictures above can be checked against the real class:

```python
start = [2, 5, 3, 9, 6, 8, 4, 11]
after_push = MinHeap(start)                                   # `start` is already a valid heap, so heapify leaves it alone
after_push.push(1)
after_pop = MinHeap(start)
removed = after_pop.pop()
print(MinHeap(start)._data)                                   # [2, 5, 3, 9, 6, 8, 4, 11]
print(after_push._data)                                       # [1, 2, 3, 5, 6, 8, 4, 11, 9]
print(removed, after_pop._data)                               # 2 [3, 5, 4, 9, 6, 8, 11]
```

## 🏗️ Building a Heap: `n` Pushes or `heapify`?

To make a heap from `n` items there are two approaches:

1. **Push one at a time.** Each push is O(log n), so the total looks like O(n log n).
2. **Heapify (Floyd's method).** Dump all items into the list, then fix it from the bottom up: sift down every internal node, starting from the last one and working back to the root. This is what the
   constructor above does.

Heapify turns out to be **O(n)**, not O(n log n). The reason is that most nodes are near the bottom, where sifting down is cheap: about half the nodes are leaves (no work), a quarter can move at most one level,
an eighth at most two, and so on — the total work is `n/4·1 + n/8·2 + n/16·3 + … ≤ n`. The measurement below counts the comparisons used by both methods on random data and on a deliberately hostile
order (descending values, which force every pushed item to travel all the way to the root). A small wrapper class counts every comparison the heap makes:

```python
import math
import random

class Counted:
    count = 0                                                 # a class-wide comparison counter
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.count += 1
        return self.value < other.value

    def __le__(self, other):
        Counted.count += 1
        return self.value <= other.value

    def __gt__(self, other):
        Counted.count += 1
        return self.value > other.value

    def __ge__(self, other):
        Counted.count += 1
        return self.value >= other.value

random.seed(1)
print(f"{'n':>8} | {'input order':>11} | {'n pushes':>10} | {'heapify':>9} | {'2n':>9} | {'n·log2(n)':>10}")
for n in (1_000, 10_000, 100_000):
    for order in ("random", "descending"):
        values = list(range(n))
        if order == "random":
            random.shuffle(values)
        else:
            values.sort(reverse=True)

        Counted.count = 0
        pushed = MinHeap()
        for value in values:
            pushed.push(Counted(value))
        by_pushes = Counted.count

        Counted.count = 0
        MinHeap([Counted(value) for value in values])
        by_heapify = Counted.count
        print(f"{n:>8,} | {order:>11} | {by_pushes:>10,} | {by_heapify:>9,} | {2 * n:>9,} | {int(n * math.log2(n)):>10,}")
```

Output:

```
       n | input order |   n pushes |   heapify |        2n |  n·log2(n)
   1,000 |      random |      2,272 |     1,871 |     2,000 |      9,965
   1,000 |  descending |      7,987 |     1,982 |     2,000 |      9,965
  10,000 |      random |     22,490 |    18,707 |    20,000 |    132,877
  10,000 |  descending |    113,631 |    19,982 |    20,000 |    132,877
 100,000 |      random |    227,943 |   188,160 |   200,000 |  1,660,964
 100,000 |  descending |  1,468,946 |   199,978 |   200,000 |  1,660,964
```

Reading the table:

- **`heapify` stays below `2n` comparisons for every `n` and every order** — it truly is linear, and it does not depend on the input order.
- **`n` pushes on random data is also cheap** (about 2.3 comparisons per item), because a random new item usually stays near the bottom.
- **`n` pushes on descending data costs close to `n·log₂ n`**, because every new item is smaller than everything above it and must sift all the way up. At 100,000 items that is about seven times more
  comparisons than `heapify` needs.

So when you already have all the items, build the heap with `heapify` (Python's `heapq.heapify`, or a constructor like the one above); use `push` when items arrive over time.

## 🔬 Verification

The heap is tested against Python's own `heapq` module (a mature min-heap on lists), with the heap property checked after every operation:

```python
import heapq

random.seed(2)
mine, reference = MinHeap(), []
for step in range(50000):
    if random.random() < 0.55 or not reference:
        value = random.randint(0, 1000)
        mine.push(value)
        heapq.heappush(reference, value)
    else:
        assert mine.pop() == heapq.heappop(reference)
    assert len(mine) == len(reference) and is_min_heap(mine._data)
    if reference:
        assert mine.peek() == reference[0]

for _ in range(3000):
    items = [random.randint(0, 50) for _ in range(random.randint(0, 40))]
    built = MinHeap(items)                                    # Floyd's heapify
    assert is_min_heap(built._data)
    assert [built.pop() for _ in range(len(built))] == sorted(items)
print("50,000 random push/pop operations agree with heapq; heapify and pop-all always produce sorted output")
```

```text
50,000 random push/pop operations agree with heapq; heapify and pop-all always produce sorted output
```

## 🔀 Heap Sort

Since popping a heap always returns the smallest remaining item, repeatedly popping yields a sorted sequence. This is **heap sort**: heapify (O(n)), then `n` pops (O(log n) each).

```python
def heap_sort(items):
    heap = MinHeap(items)                                     # O(n) to build
    return [heap.pop() for _ in range(len(heap))]             # n pops at O(log n) each

print(heap_sort([7, 2, 9, 4, 1, 8, 2]))                       # [1, 2, 2, 4, 7, 8, 9]
```

Total **O(n log n)** time regardless of the input order — there is no bad case like a quicksort's — and this version needs O(n) extra space for the heap. The classic *in-place* heap sort, which sorts within the
original array by building a **max**-heap and swapping the maximum to the end, is covered in [heap-sort.md](../sorting-algorithms/heap-sort.md) with the other sorting algorithms.

## ⚖️ Heap Operations at a Glance

| Operation | Cost | Notes |
|-----------|------|-------|
| Peek at the minimum | **O(1)** | `data[0]` |
| Push | O(log n) worst case; O(1) on average for random input | Sift up |
| Pop the minimum | O(log n) | Sift down |
| Build from `n` items (`heapify`) | **O(n)** | Faster than `n` pushes in the worst case |
| Find an arbitrary item | O(n) | A heap does not support fast search |
| Remove or change an arbitrary item | O(n) to find it, then O(log n) | See [priority-queues.md](priority-queues.md) for the lazy workaround |
| Sorted order of all items | O(n log n) | Pop everything |
| Space | O(n) | A plain list, no pointers |

## 🆚 Heap or BST?

| | Heap | Balanced BST |
|--|------|--------------|
| Minimum | **O(1)** | O(log n) |
| Insert | O(log n) | O(log n) |
| Remove the minimum | O(log n) | O(log n) |
| Search for a key | O(n) | **O(log n)** |
| Next larger key / range query | not supported | **O(log n)** |
| Memory layout | Compact array | Pointer-based nodes |
| Implementation | Short | Long (rotations) |

If you only need the best item repeatedly, use a heap. If you also need arbitrary search, neighbours, or ranges, use a balanced tree.

## Common Mistakes

- **Believing the heap's list is sorted.** Only the root is guaranteed to be the minimum.
- **Sifting down against the larger child** (or comparing with only one child), which breaks the heap property.
- **Forgetting to handle a missing right child** in `_sift_down` (`child + 1 < n`).
- **Searching a heap for a value** — it is O(n); use a set or dictionary alongside if you need membership.
- **Building a heap with `n` pushes when you already have the data**, instead of `heapify`.
- **Using 1-based index formulas with a 0-based array** (children of `i` are `2i + 1` and `2i + 2` when the root is index 0).

## ➡️ Next

Continue to [min-heap-and-max-heap.md](min-heap-and-max-heap.md) to see Python's built-in `heapq` module, how to get a max-heap from a min-heap, and how to heap-order tuples and objects.
