# 🎫 Priority Queues

## Serve the Most Important Item First

An ordinary [queue](../stacks-and-queues/queue-fundamentals.md) serves items in the order they arrived. A **priority queue** serves them in order of **priority**, whatever order they arrived in: the
emergency room treats the most critical patient first, the operating system runs the highest-priority process first, and a shortest-path algorithm explores the nearest unvisited city first.

A priority queue is an **abstract data type** — a description of behaviour, not of storage — with these operations:

| Operation | Meaning |
|-----------|---------|
| `push(item, priority)` | Add an item with a priority |
| `pop()` | Remove and return the item with the **best** priority (smallest number first, by the convention used here) |
| `peek()` | Look at the best item without removing it |
| `len()` | How many items are waiting |
| *(optional)* `update` / `remove` | Change an item's priority, or cancel it |

A [heap](heap-fundamentals.md) is the standard way to implement it. This file compares the alternatives with measurements, shows Python's ready-made `queue.PriorityQueue`, builds a `StablePriorityQueue` with
**stable ordering** and **priority updates**, and uses it for two applications. All outputs were produced by running the code on CPython 3.9.

## 📊 Three Ways to Build One

| Implementation | `push` | `pop` best item | Idea |
|----------------|--------|-----------------|------|
| Unsorted list | O(1) | O(n) | Append; scan for the minimum when popping |
| Sorted list | O(n) | O(1) (from the right end) | Keep sorted with `bisect.insort`; the best item is at the end |
| **Binary heap** | **O(log n)** | **O(log n)** | Neither extreme: partial order, cheap in both directions |

The heap's advantage is balance: when pushes and pops are mixed (as they usually are), neither of the others can match O(log n) for both. The measurement below pushes `n` random numbers into each
and then pops them all. It includes the C-implemented `heapq`, and also a heap written in pure Python (the same algorithm as the `MinHeap` in [heap-fundamentals.md](heap-fundamentals.md)), because
the *implementation language* matters as much as the algorithm at moderate sizes:

```python
import bisect
import heapq
import random
import timeit

def with_unsorted_list(values):
    items = list(values)
    while items:
        best = min(items)                      # O(n) scan to find the best item
        items.remove(best)                     # and O(n) to remove it

def with_sorted_list(values):
    items = []
    for v in values:
        bisect.insort(items, -v)               # keep sorted by negated value, so the smallest value is at the end
    while items:
        items.pop()                            # O(1): remove from the right end

def with_heapq(values):
    heap = []
    for v in values:
        heapq.heappush(heap, v)
    while heap:
        heapq.heappop(heap)

def with_python_heap(values):                  # the MinHeap algorithm, written out in pure Python
    data = []
    for v in values:                           # push: append, then sift up
        data.append(v)
        i = len(data) - 1
        while i > 0 and data[(i - 1) // 2] > v:
            data[i] = data[(i - 1) // 2]
            i = (i - 1) // 2
        data[i] = v
    while data:                                # pop: move the last item to the root, then sift down
        last = data.pop()
        if data:
            n, i = len(data), 0
            while True:
                child = 2 * i + 1
                if child >= n:
                    break
                if child + 1 < n and data[child + 1] < data[child]:
                    child += 1
                if data[child] >= last:
                    break
                data[i] = data[child]
                i = child
            data[i] = last

random.seed(1)
print(f"{'n':>8} | {'unsorted list':>13} | {'sorted list':>11} | {'pure-Python heap':>16} | {'heapq':>7}   (ms)")
for n in (2_000, 8_000, 32_000, 128_000):
    values = [random.random() for _ in range(n)]
    cells = []
    for fn in (with_unsorted_list, with_sorted_list, with_python_heap, with_heapq):
        if fn is with_unsorted_list and n > 8_000:
            cells.append(f"{'(skipped)':>13}")           # quadratic: it would take many seconds
        else:
            width = 13 if fn is with_unsorted_list else 11 if fn is with_sorted_list else 16 if fn is with_python_heap else 7
            cells.append(f"{min(timeit.repeat(lambda: fn(values), number=1, repeat=2)) * 1000:{width}.1f}")
    print(f"{n:>8,} | " + " | ".join(cells))
```

Output:

```
       n | unsorted list | sorted list | pure-Python heap |   heapq   (ms)
   2,000 |          18.4 |         0.6 |              3.1 |     0.4
   8,000 |         299.4 |         6.0 |             15.4 |     1.9
  32,000 |     (skipped) |        75.7 |             71.9 |     9.1
 128,000 |     (skipped) |      1165.8 |            336.7 |    44.4
```

What the measurements say:

- **The unsorted list is quadratic** — 8,000 items already take about 300 ms, and the time grows by about 16× for every 4× more items. It is the clear loser.
- **The sorted list is much faster than you might expect at small sizes**, because `bisect.insort` shifts memory in fast C code. But it is quadratic too, so it falls behind as `n` grows.
- **A pure-Python heap loses at small sizes** (Python-level loops are slow) **but wins from tens of thousands of items on**, because its time grows by only about 5× per 4× more items (`n log n`), while the sorted list's grows by 10× to 15× and heads toward 16× (`n²`). The two draw level around 32,000 items; at 128,000 the heap is more than three times faster.
- **`heapq` is fastest everywhere**, because the heap operations run in C.

Big-O says which implementation wins as `n` grows; constants decide where the crossover happens. In practice: use `heapq`.

## 🧵 Python's `queue.PriorityQueue`

The standard library offers a ready-made priority queue in the `queue` module. It is a thread-safe wrapper around a `heapq` list — designed for threads that exchange work, such as a producer thread
adding tasks and worker threads taking them. Its documentation says the lowest-valued entries are retrieved first, and that entries are typically tuples of the form `(priority_number, data)`:

```python
import queue

pq = queue.PriorityQueue()
pq.put((2, "write report"))
pq.put((1, "fix outage"))
pq.put((3, "lunch"))
print(pq.qsize(), pq.empty())                # 3 False
print(pq.get(), pq.get())                    # (1, 'fix outage') (2, 'write report')
```

`get()` blocks (waits) when the queue is empty, which is exactly what a worker thread wants. Because every call takes a lock, `queue.PriorityQueue` is slower than raw `heapq` — so in single-threaded code
use `heapq` directly, and reserve `queue.PriorityQueue` for communication between threads.

## 🔧 Building a Better One: Stable Order and Priority Updates

Two gaps in a raw `heapq` priority queue show up quickly in real programs.

1. **Ties.** Equal priorities should come out in the order they were added (first in, first out) — and the items must never be compared (see the tie trap in
   [min-heap-and-max-heap.md](min-heap-and-max-heap.md)). The fix is an increasing **counter** stored between the priority and the item.
2. **Changing or cancelling.** A heap cannot find an arbitrary item quickly, so "raise this task's priority" or "cancel this task" looks impossible in O(log n). The standard workaround (also described in the
   `heapq` documentation) is **lazy deletion**: don't dig the old entry out; just mark it as removed and leave it in the heap. When it eventually reaches the top, `pop` discards it. Updating a priority
   is then "mark the old entry removed, push a new entry."

A dictionary from each item to its current entry makes the marking O(1):

```python
import heapq
import itertools

class StablePriorityQueue:
    _REMOVED = object()                              # a marker meaning "this entry was cancelled"

    def __init__(self):
        self._heap = []                              # entries: [priority, order, item]
        self._entries = {}                           # item -> its live entry (items must be hashable)
        self._counter = itertools.count()            # the tie-breaker: increases with every push

    def __len__(self):
        return len(self._entries)

    def __contains__(self, item):
        return item in self._entries

    def push(self, item, priority=0):                # also serves as "update priority" for an item already present
        if item in self._entries:
            self.remove(item)
        entry = [priority, next(self._counter), item]
        self._entries[item] = entry
        heapq.heappush(self._heap, entry)            # O(log n)

    def remove(self, item):                          # O(1): mark the entry; it is discarded when it reaches the top
        entry = self._entries.pop(item)
        entry[2] = self._REMOVED

    def _discard_removed(self):
        while self._heap and self._heap[0][2] is self._REMOVED:
            heapq.heappop(self._heap)

    def peek(self):
        self._discard_removed()
        if not self._heap:
            raise KeyError("peek at an empty priority queue")
        priority, _, item = self._heap[0]
        return item, priority

    def pop(self):                                   # O(log n) amortized
        self._discard_removed()
        if not self._heap:
            raise KeyError("pop from an empty priority queue")
        priority, _, item = heapq.heappop(self._heap)
        del self._entries[item]
        return item, priority

pq = StablePriorityQueue()
pq.push("write report", 2)
pq.push("fix outage", 1)
pq.push("answer email", 2)
pq.push("lunch", 3)
pq.push("write report", 0)                            # update: the report just became urgent
pq.remove("lunch")                                    # cancel
print(len(pq), "lunch" in pq)                         # 3 False
print(pq.pop(), pq.pop(), pq.pop())                   # ('write report', 0) ('fix outage', 1) ('answer email', 2)
```

Notice three things. The updated task jumped to the front. The cancelled task never appears. And the leftover stale entries cost nothing while they sit in the heap: each is removed at most once, when it surfaces, so
the **amortized** cost of every operation stays O(log n). (The only price is memory: a queue with many cancellations holds stale entries until they surface; a long-running system may rebuild the heap
when stale entries outnumber live ones.)

Equal priorities come out in insertion order — a **stable** priority queue:

```python
tie = StablePriorityQueue()
for name in ["first", "second", "third"]:
    tie.push(name, 5)
print([tie.pop()[0] for _ in range(3)])               # ['first', 'second', 'third']
```

### Verification Against a Brute-Force Model

The queue is tested against the simplest correct implementation — a dictionary scanned for the minimum on every pop — over 60,000 random operations that mix pushes, updates, removals, peeks, and pops
on a small set of items (so updates and stale entries occur constantly):

```python
import random

random.seed(9)
mine = StablePriorityQueue()
model = {}                                           # item -> (priority, order of its latest push)
clock = 0
for step in range(60000):
    action = random.choice(["push", "push", "remove", "pop", "peek"])
    item = random.randint(0, 12)
    if action == "push":
        priority = random.randint(0, 5)
        mine.push(item, priority)
        model[item] = (priority, clock)
        clock += 1
    elif action == "remove" and item in model:
        mine.remove(item)
        del model[item]
    elif action == "pop" and model:
        best = min(model, key=lambda k: model[k])    # the smallest (priority, order) pair
        assert mine.pop() == (best, model[best][0])
        del model[best]
    elif action == "peek" and model:
        best = min(model, key=lambda k: model[k])
        assert mine.peek() == (best, model[best][0])
    assert len(mine) == len(model) and all((k in mine) == (k in model) for k in range(13))
print("60,000 random operations agree with a brute-force model")
```

```text
60,000 random operations agree with a brute-force model
```

## 🏥 Application 1: Emergency-Room Triage

Patients arrive over time with a severity (1 is most urgent). The most urgent patient is treated next; among equally urgent patients, the one who arrived first is treated first — exactly the stable
priority queue:

```python
triage = StablePriorityQueue()
arrivals = [("Ana", 3), ("Ben", 1), ("Chen", 3), ("Dara", 2), ("Eli", 1)]
for name, severity in arrivals:
    triage.push(name, severity)
order = [triage.pop()[0] for _ in range(len(triage))]
print(order)                                         # ['Ben', 'Eli', 'Dara', 'Ana', 'Chen']
```

Ben and Eli (both severity 1) are treated in arrival order, then Dara (2), then Ana and Chen (both 3, in arrival order).

## ⏱️ Application 2: A Discrete-Event Simulation

Simulations keep a priority queue of **future events** keyed by time. The loop repeatedly takes the earliest event, "runs" it, and may schedule new events — which can land anywhere in the future, so a plain list
would need re-sorting. A heap handles it naturally. This tiny coffee-shop simulation schedules a customer's arrival, the start of their order, and the moment it is ready:

```python
events = StablePriorityQueue()
events.push("customer A arrives", 0)
events.push("customer B arrives", 2)

log = []
while len(events):
    what, time = events.pop()
    log.append(f"t={time}: {what}")
    if what.endswith("arrives"):
        who = what.split()[1]
        events.push(f"customer {who} order is ready", time + 4)    # making the coffee takes 4 time units
print("\n".join(log))
```

```text
t=0: customer A arrives
t=2: customer B arrives
t=4: customer A order is ready
t=6: customer B order is ready
```

Event times need not arrive in order: B's order is pushed *after* A's, but the queue still interleaves them by time. The same pattern drives game loops, network simulators, and timer wheels.

Another famous user is **Dijkstra's shortest-path algorithm** ([shortest-path-algorithms.md](../graphs/shortest-path-algorithms.md)), which repeatedly extracts the nearest unfinished vertex and
sometimes lowers a vertex's recorded distance — the priority-update operation this file built.

## ⚠️ Starvation

If high-priority items keep arriving, a low-priority item may wait forever — **starvation**. Schedulers counter it with **aging**: gradually improve the priority of items that have waited a long time. With
the queue above, that means periodically calling `push(item, better_priority)` for old items.

## ⚖️ Costs of the Priority Queue Above

| Operation | Cost |
|-----------|------|
| `push` (new item or priority update) | O(log n) |
| `remove` (cancel) | O(1) |
| `pop` / `peek` | O(log n) amortized (discarding stale entries) |
| `__contains__`, `len` | O(1) |
| Space | O(n + stale entries) |

## Common Mistakes

- **Using a list scan for `pop`** when the queue is large — O(n) per pop makes the whole loop O(n²).
- **Comparing items on ties**, which raises `TypeError` or orders items arbitrarily. Use a counter.
- **Trying to update a priority by editing the entry inside the heap list**, which breaks the heap invariant. Mark-and-reinsert instead.
- **Forgetting that "highest priority" is a convention**: with `heapq`, the *smallest* number comes out first.
- **Using `queue.PriorityQueue` in single-threaded code**, paying for locks.
- **Letting stale entries pile up forever** in a long-lived queue with many cancellations.
- **Ignoring starvation** when priorities are strict.

## ➡️ Next

Continue to [heap-problems.md](heap-problems.md) to put heaps to work on classic problems: the k-th largest element, the k most frequent items, merging sorted lists, and the running median.
