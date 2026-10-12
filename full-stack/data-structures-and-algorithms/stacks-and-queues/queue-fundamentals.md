# 🚶 Queue Fundamentals

## First In, First Out

A **queue** is the structure of a line at a shop: items join at the **back** and leave from the **front**, so the item that has waited
longest is served first — **First In, First Out (FIFO)**. It is the mirror image of the [stack](stack-fundamentals.md), which serves the
*newest* item first.

```
 enqueue(40)                                        dequeue() → 10
     │                                                    ▲
     ▼                                                    │
   back ─▶ [ 40 ] [ 30 ] [ 20 ] [ 10 ] ─▶ front
```

Queues model fairness and ordering — print jobs, requests waiting for a server, messages between programs, tasks waiting for a
processor — and they drive **breadth-first search**, which explores a graph or tree level by level. This file shows how to implement
queues correctly (naïve versions are surprisingly slow), builds three of them, and applies the structure. All outputs were produced by
running the code on CPython 3.9.

## ⚙️ The Operations

| Operation | Meaning | Target cost |
|-----------|---------|-------------|
| `enqueue(x)` | Add `x` at the back | O(1) |
| `dequeue()` | Remove and return the front item | O(1) |
| `peek()` | Look at the front item without removing it | O(1) |
| `is_empty()` / `len()` | Is anything waiting? | O(1) |

## 🐌 The Trap: A Python `list` Is a Poor Queue

A list makes `append` (enqueue) cheap, so `pop(0)` (dequeue) looks natural — but removing the first element makes every other element shift
one place left. That is O(n) per dequeue, O(n²) to drain a queue (the shifting cost explained in
[insertion-and-deletion.md](../arrays/insertion-and-deletion.md)). The standard-library answer is `collections.deque`; there is also
`queue.Queue`, a thread-safe queue designed for communication between threads. This benchmark enqueues `n` items and then dequeues them all:

```python
import timeit
from collections import deque
from queue import Queue

def with_list(n):
    items = []
    for i in range(n):
        items.append(i)
    while items:
        items.pop(0)

def with_deque(n):
    items = deque()
    for i in range(n):
        items.append(i)
    while items:
        items.popleft()

def with_queue_class(n):
    items = Queue()
    for i in range(n):
        items.put(i)
    while not items.empty():
        items.get()

print(f"{'n':>7} | {'list.pop(0)':>11} | {'deque.popleft':>13} | {'queue.Queue':>11}   (ms)")
for n in (10_000, 20_000, 40_000, 80_000):
    times = [min(timeit.repeat(lambda: fn(n), number=1, repeat=3)) * 1000
             for fn in (with_list, with_deque, with_queue_class)]
    print(f"{n:>7,} | {times[0]:11.2f} | {times[1]:13.2f} | {times[2]:11.2f}")
```

One run on the test machine printed:

```
      n | list.pop(0) | deque.popleft | queue.Queue   (ms)
 10,000 |        5.28 |          0.57 |       17.51
 20,000 |       22.26 |          1.13 |       35.15
 40,000 |      103.28 |          2.31 |       70.71
 80,000 |      423.94 |          4.63 |      140.41
```

Reading the table: the `list.pop(0)` column roughly **quadruples** each time `n` doubles (quadratic), while `deque` doubles (linear, O(1) per
operation). `queue.Queue` is also linear but roughly 30 times slower than `deque` here (140 ms against 4.6 ms at 80,000 items), because every call acquires
a lock to be safe across threads. The Python documentation describes `queue.Queue` as implementing the multi-producer, multi-consumer queue for exchanging
information safely between threads; in single-threaded code, use `deque`.

```python
from collections import deque

line = deque()
line.append("alice")           # enqueue at the back
line.append("bob")
line.append("carol")
print(line.popleft())          # alice   — dequeue from the front
print(line[0], len(line))      # bob 2   — peek at the front
```

## 🔨 Building Queues From Scratch

Three classic constructions show different ways of reaching O(1). All three are tested against `collections.deque` at the end of the section.

### 1. A Linked-List Queue

Keep references to both ends of a [singly linked list](../linked-lists/singly-linked-lists.md): enqueue at the **tail**, dequeue at the **head**.
Both are O(1) because neither needs to walk the list:

```python
class Node:
    __slots__ = ("value", "next")

    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedQueue:
    def __init__(self):
        self._head = None                    # front of the queue
        self._tail = None                    # back of the queue
        self._size = 0

    def enqueue(self, item):
        node = Node(item)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def dequeue(self):
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        node = self._head
        self._head = node.next
        if self._head is None:               # the queue became empty
            self._tail = None
        self._size -= 1
        return node.value

    def peek(self):
        if self._head is None:
            raise IndexError("peek at empty queue")
        return self._head.value

    def __len__(self):
        return self._size
```

### 2. A Ring Buffer (Circular Array)

For a queue with a **fixed capacity**, use an array whose ends are glued together with modular arithmetic. Keep the index of the front item and
the count of items; the back is `(front + size) % capacity`. Nothing ever shifts — a dequeue just advances `front` — and the array is reused
as the queue "moves around" it:

```python
class RingBufferQueue:
    def __init__(self, capacity):
        self._slots = [None] * capacity
        self._front = 0                      # index of the oldest item
        self._size = 0

    def enqueue(self, item):
        if self._size == len(self._slots):
            raise OverflowError("queue is full")
        back = (self._front + self._size) % len(self._slots)    # wraps around the end of the array
        self._slots[back] = item
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            raise IndexError("dequeue from empty queue")
        item = self._slots[self._front]
        self._slots[self._front] = None      # let the object be garbage-collected
        self._front = (self._front + 1) % len(self._slots)
        self._size -= 1
        return item

    def peek(self):
        if self._size == 0:
            raise IndexError("peek at empty queue")
        return self._slots[self._front]

    def __len__(self):
        return self._size

rb = RingBufferQueue(3)
for letter in "abc":
    rb.enqueue(letter)
print(rb.dequeue(), rb.dequeue())     # a b
rb.enqueue("d")                       # reuses the slot at index 0: the queue wrapped around
rb.enqueue("e")                       # ...and index 1
print(rb._slots, rb._front)           # ['d', 'e', 'c'] 2
try:
    rb.enqueue("f")
except OverflowError as error:
    print(error)                      # queue is full
```

Tracking `size` separately is what distinguishes "empty" from "full" — in both cases `front` and `back` would otherwise coincide. Ring buffers
are used for streaming data, keyboard buffers, and audio, where memory must stay bounded and allocation costs must stay predictable.

### 3. A Queue Made From Two Stacks

A [stack](stack-fundamentals.md) reverses order; two reversals restore it. Keep an **inbox** stack for arrivals and an **outbox** stack for
departures. When the outbox is empty, pour the whole inbox into it — which reverses it, leaving the *oldest* item on top:

```python
class TwoStackQueue:
    def __init__(self):
        self._inbox = []                     # new items are pushed here
        self._outbox = []                    # items leave from here, oldest on top

    def enqueue(self, item):
        self._inbox.append(item)

    def _refill(self):
        if not self._outbox:
            while self._inbox:
                self._outbox.append(self._inbox.pop())    # reverses the order
        if not self._outbox:
            raise IndexError("dequeue from empty queue")

    def dequeue(self):
        self._refill()
        return self._outbox.pop()

    def peek(self):
        self._refill()
        return self._outbox[-1]

    def __len__(self):
        return len(self._inbox) + len(self._outbox)
```

A single `dequeue` can cost O(n) when it triggers a pour. But each item moves from inbox to outbox **at most once** and is pushed and popped
once in each — about three constant-time operations per item over its whole life. Spread across all operations, the cost per operation is
**O(1) amortized** — the same style of argument as the dynamic array's doubling in
[array-fundamentals.md](../arrays/array-fundamentals.md).

### Testing All Three Against `deque`

```python
import random

random.seed(6)
for make in (LinkedQueue, lambda: RingBufferQueue(50), TwoStackQueue):
    mine, model = make(), deque()
    for step in range(30000):
        if random.random() < 0.55 and len(model) < 50:           # stay within the ring buffer's capacity
            mine.enqueue(step)
            model.append(step)
        elif model:
            assert mine.peek() == model[0]
            assert mine.dequeue() == model.popleft()
        assert len(mine) == len(model)
    for operation in (mine.dequeue, mine.peek):
        if not model:
            try:
                operation()
                raise AssertionError("expected IndexError")
            except IndexError:
                pass
print("linked, ring-buffer and two-stack queues agree with collections.deque")
```

```text
linked, ring-buffer and two-stack queues agree with collections.deque
```

## 🔧 Applications

### Counting Recent Requests (a Sliding Window)

*How many requests arrived in the last 300 seconds?* Requests arrive in time order, so the oldest are at the front of a queue. To count, drop
everything older than the window from the front, then report the length. Each timestamp is added once and removed at most once, so the work is
amortized O(1) per request:

```python
class HitCounter:
    def __init__(self, window=300):
        self._window = window
        self._hits = deque()                          # timestamps, oldest first

    def hit(self, timestamp):
        self._hits.append(timestamp)

    def count(self, timestamp):                       # timestamps must not go backward
        while self._hits and self._hits[0] <= timestamp - self._window:
            self._hits.popleft()                      # too old: outside the window
        return len(self._hits)

counter = HitCounter(window=300)
for t in (1, 2, 3, 300):
    counter.hit(t)
print(counter.count(300))      # 4   — all four hits are within the last 300 seconds
print(counter.count(301))      # 3   — the hit at time 1 has just aged out
print(counter.count(600))      # 0   — everything has expired
```

This is the queue version of the sliding window in [sliding-window.md](../arrays/sliding-window.md), and the idea behind rate limiters.

### Breadth-First Search

A queue explores things in the order they were discovered: visit a node, enqueue its unvisited neighbours, and repeat. Everything at distance 1
is processed before anything at distance 2, which makes the first time you reach a node the *shortest path* (in number of edges). Here it computes
the distance from a start node to every reachable node in a graph stored as a dictionary of neighbour lists:

```python
def bfs_distances(graph, start):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if neighbour not in distance:              # first time we see it: this is the shortest route
                distance[neighbour] = distance[node] + 1
                queue.append(neighbour)
    return distance

graph = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C", "E"], "E": ["D"], "F": []}
print(bfs_distances(graph, "A"))       # {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 3}
```

`F` is unreachable, so it does not appear. BFS is developed fully for trees in [tree-traversal.md](../trees/tree-traversal.md) (level-order
traversal) and for graphs in the [Graphs](../graphs/README.md) module (see [breadth-first-search.md](../graphs/breadth-first-search.md)).

### Tests for the Applications

```python
def brute_force_hits(hits, now, window):
    return sum(1 for h in hits if now - window < h <= now)

for _ in range(3000):
    counter, hits, now = HitCounter(window=10), [], 0
    for _ in range(random.randint(0, 25)):
        now += random.randint(0, 6)
        if random.random() < 0.6:
            counter.hit(now)
            hits.append(now)
        assert counter.count(now) == brute_force_hits(hits, now, 10)

def all_distances(graph, start):                           # brute force: relax every edge until nothing improves
    distance = {start: 0}
    changed = True
    while changed:
        changed = False
        for node, neighbours in graph.items():
            for neighbour in neighbours:
                if node in distance and distance[node] + 1 < distance.get(neighbour, float("inf")):
                    distance[neighbour] = distance[node] + 1
                    changed = True
    return distance

for _ in range(1500):
    nodes = list(range(random.randint(1, 8)))
    graph = {n: [] for n in nodes}
    for _ in range(random.randint(0, 12)):
        a, b = random.choice(nodes), random.choice(nodes)
        graph[a].append(b)
        graph[b].append(a)
    start = random.choice(nodes)
    assert bfs_distances(graph, start) == all_distances(graph, start)
print("hit counter and BFS agree with brute-force versions")
```

```text
hit counter and BFS agree with brute-force versions
```

## 🚌 A Related Structure: The Priority Queue

In an ordinary queue, order of arrival decides who is served first. A **priority queue** serves the item with the highest priority first,
whatever its arrival time (hospital triage, task schedulers). It is usually built on a heap, which is the subject of the
[Heaps and Priority Queues](../heaps-and-priority-queues/README.md) module; `queue.PriorityQueue` and `heapq` provide it in Python.

## ⚖️ Queue Cost Summary

| Implementation | enqueue | dequeue | Notes |
|----------------|---------|---------|-------|
| `list` with `pop(0)` | O(1) | **O(n)** | Avoid |
| `collections.deque` | O(1) | O(1) | The default choice in Python |
| `queue.Queue` | O(1) | O(1) | Thread-safe and blocking; slower; for inter-thread communication |
| Linked list (head and tail) | O(1) | O(1) | Extra memory per node |
| Ring buffer | O(1) | O(1) | Fixed capacity, no allocation after creation |
| Two stacks | O(1) | O(1) amortized | A classic design question |

## Common Mistakes

- **Using `list.pop(0)` for a queue** and getting O(n²) behaviour on large inputs.
- **Using `queue.Queue` in single-threaded code**, paying for locks you do not need.
- **Forgetting the tail pointer** (or clearing it) when the last element is dequeued from a linked-list queue.
- **Confusing empty with full** in a ring buffer — track the size separately, or leave one slot unused.
- **Forgetting to wrap with `% capacity`**, which makes indexes run off the end of the array.
- **Marking nodes visited when dequeuing rather than when enqueuing** in BFS, which adds the same node many times.
- **Assuming a priority queue is a FIFO queue** — it is not; arrival order does not decide the order of service.

## ➡️ Next

Continue to [deque.md](deque.md) for the double-ended queue, which does the job of both a stack and a queue, and powers the sliding-window
maximum.
