# 🔄 Circular Linked Lists

## A List With No End

In a [singly linked list](singly-linked-lists.md) the last node points to `None`. In a **circular linked list** the last node points
**back to the first**, so following `next` pointers goes round and round forever:

```
         ┌───────────────────────────────────┐
         ▼                                   │
       ┌────┐      ┌────┐      ┌────┐      ┌────┐
head ─▶│ 10 │─────▶│ 20 │─────▶│ 30 │─────▶│ 40 │   ◀─ tail
       └────┘      └────┘      └────┘      └────┘
```

There is no `None` to mark the end, which changes two things: **traversal needs a different stopping rule**, and the list is perfect for
anything that is naturally cyclic — taking turns, rotating through items, or repeating a sequence. This file builds one, uses it to solve
the Josephus problem and to simulate round-robin scheduling, and points out the Python tools that cover the same ground. All outputs
were produced by running the code on CPython 3.9.

## 🔑 Keep the Tail, Not the Head

With a circular list, one reference is enough to reach *both* ends: keep a reference to the **tail**. Since `tail.next` is the head,
the head is one step away.

```
tail ─▶ the last node;   tail.next ─▶ the first node (the head)
```

That gives O(1) access to the front *and* the back, and a way to insert at either end without walking:

```python
class CNode:
    __slots__ = ("value", "next")

    def __init__(self, value):
        self.value = value
        self.next = self                         # a lone node points to itself: a circle of one

class CircularLinkedList:
    def __init__(self, values=()):
        self._tail = None                        # the only reference we keep; the head is self._tail.next
        self._size = 0
        for value in values:
            self.append(value)

    def __len__(self):
        return self._size

    def __iter__(self):                          # go round exactly once, front to back
        if self._tail is None:
            return
        node = self._tail.next
        for _ in range(self._size):              # count steps: there is no None to stop at
            yield node.value
            node = node.next

    def __repr__(self):
        return f"CircularLinkedList({list(self)})"

    def prepend(self, value):                    # O(1): insert after the tail; the tail does not move
        node = CNode(value)
        if self._tail is None:
            self._tail = node
        else:
            node.next = self._tail.next
            self._tail.next = node
        self._size += 1

    def append(self, value):                     # O(1): prepend, then move the tail onto the new node
        self.prepend(value)
        self._tail = self._tail.next

    def pop_front(self):                         # O(1)
        if self._tail is None:
            raise IndexError("pop from empty list")
        head = self._tail.next
        if head is self._tail:                   # the only node
            self._tail = None
        else:
            self._tail.next = head.next
        self._size -= 1
        return head.value

    def rotate(self, steps=1):                   # O(steps): move the front element to the back, `steps` times
        if self._size:
            for _ in range(steps % self._size):
                self._tail = self._tail.next     # the old head becomes the new tail: nothing is copied

ring = CircularLinkedList(["a", "b", "c", "d"])
print(ring)                       # CircularLinkedList(['a', 'b', 'c', 'd'])
ring.rotate()
print(ring)                       # CircularLinkedList(['b', 'c', 'd', 'a'])
ring.rotate(2)
print(ring)                       # CircularLinkedList(['d', 'a', 'b', 'c'])
ring.prepend("z")
ring.append("y")
print(ring, len(ring))            # CircularLinkedList(['z', 'd', 'a', 'b', 'c', 'y']) 6
print(ring.pop_front(), ring)     # z CircularLinkedList(['d', 'a', 'b', 'c', 'y'])
```

The standout operation is **`rotate`**: moving the front element to the back is a single assignment, `tail = tail.next`, because in a
circle "the front" and "the back" are just which node you currently call the tail. An array would have to shift every element (or copy
slices) to rotate; a circular list changes one reference.

### The Traversal Trap

Because nothing is `None`, the usual `while node is not None:` loop **never ends**. The class above avoids this by counting `_size`
steps. Another safe pattern is to remember the starting node and stop when you come back to it:

```python
def walk_once(tail):
    if tail is None:
        return []
    values = []
    node = tail.next                  # start at the head
    while True:
        values.append(node.value)
        node = node.next
        if node is tail.next:         # back at the head: one full circle
            break
    return values

print(walk_once(ring._tail))          # ['d', 'a', 'b', 'c', 'y']
```

Note the loop shape: it must visit the head *before* testing for "back at the start", so it is a do-while (test at the bottom), not a
`while` that tests first. A `while node is not head` loop would skip a one-element list entirely.

### Testing Against a Model

`collections.deque` has a `rotate` method with the same meaning, which makes it a convenient model. A negative `deque.rotate` rotates the
other way, so `rotate(-1)` moves the front to the back, matching ours:

```python
import random
from collections import deque

random.seed(4)
mine, model = CircularLinkedList(), deque()
for step in range(20000):
    action = random.choice(["append", "prepend", "pop_front", "rotate"])
    value = random.randint(0, 99)
    if action == "append":
        mine.append(value); model.append(value)
    elif action == "prepend":
        mine.prepend(value); model.appendleft(value)
    elif action == "pop_front" and model:
        assert mine.pop_front() == model.popleft()
    elif action == "rotate":
        steps = random.randint(0, 12)
        mine.rotate(steps); model.rotate(-steps)
    assert list(mine) == list(model) and len(mine) == len(model)
print("20,000 random operations agree with collections.deque")
```

```text
20,000 random operations agree with collections.deque
```

## 🪑 The Josephus Problem

*`n` people stand in a circle, numbered 1 to `n`. Starting from person 1, count off `k` people and eliminate the `k`-th, then keep
counting from the next person. Who is the last survivor?* The circular list expresses the story directly: rotate the ring so the
`k`-th person is at the front, then pop them.

```python
def josephus(n, k):
    ring = CircularLinkedList(range(1, n + 1))
    eliminated = []
    while len(ring) > 1:
        ring.rotate(k - 1)                       # skip k-1 people: they move to the back
        eliminated.append(ring.pop_front())      # the k-th person leaves the circle
    return eliminated, ring.pop_front()

order, survivor = josephus(7, 3)
print(order, survivor)              # [3, 6, 2, 7, 5, 1] 4
print(josephus(5, 2))               # ([2, 4, 1, 5], 3)
```

For `n = 7` and `k = 3` the people leave in the order 3, 6, 2, 7, 5, 1, and person **4** survives. The simulation costs O(n·k) —
each of the `n − 1` eliminations rotates up to `k − 1` steps. A known recurrence solves it in O(n) with no list at all: if `J(n)` is the
survivor's position (counting from 0) among `n` people, then `J(1) = 0` and `J(n) = (J(n − 1) + k) mod n`. The new circle of `n − 1`
people starts counting right after the eliminated person, so positions shift by `k`.

```python
def josephus_survivor(n, k):
    survivor = 0                                  # with one person, the survivor is position 0
    for size in range(2, n + 1):
        survivor = (survivor + k) % size
    return survivor + 1                           # convert to 1-based numbering

print(josephus_survivor(7, 3), josephus_survivor(5, 2), josephus_survivor(41, 3))    # 4 3 31
```

Both approaches are tested against each other for every `n` up to 60 and every `k` up to 12 (below). The `41, 3` case is the classic
version of the puzzle: with 41 people and every third eliminated, the last survivor stands at position 31.

```python
for n in range(1, 61):
    for k in range(1, 13):
        assert josephus(n, k)[1] == josephus_survivor(n, k), (n, k)
print("simulation and recurrence agree for all n <= 60, k <= 12")
```

```text
simulation and recurrence agree for all n <= 60, k <= 12
```

## 🕐 Round-Robin Scheduling

Operating systems commonly share a processor among tasks using **round-robin scheduling**: each task runs for at most a fixed *time
quantum*, then goes to the back of the line if it still has work to do. A circular list models "back of the line" exactly:

```python
def round_robin(jobs, quantum):
    ring = CircularLinkedList(jobs)               # jobs: (name, time_needed) pairs
    finished, clock = [], 0
    while len(ring):
        name, remaining = ring.pop_front()
        run = min(quantum, remaining)
        clock += run
        if remaining > run:
            ring.append((name, remaining - run))  # not done: back of the line
        else:
            finished.append((name, clock))        # done: record when it finished
    return finished

print(round_robin([("A", 5), ("B", 3), ("C", 1)], quantum=2))
# [('C', 5), ('B', 8), ('A', 9)]
```

Trace it: A runs 0–2 (3 left), B runs 2–4 (1 left), C runs 4–5 and finishes at time 5; A runs 5–7 (1 left), B runs 7–8 and finishes at 8;
A runs 8–9 and finishes at 9. (CPU scheduling is treated in depth in the Operating Systems modules later in this curriculum.)

## 🐍 The Python Equivalents

You rarely hand-roll a circular list in Python, because two tools cover the common needs:

```python
import itertools

print(list(itertools.islice(itertools.cycle("abc"), 7)))      # ['a', 'b', 'c', 'a', 'b', 'c', 'a']
```

`itertools.cycle` repeats a sequence forever — but it works by saving a copy of the elements and replaying it, so it is a *generator*, not
a structure you can insert into or remove from. For a structure you can modify, `collections.deque` supports `rotate` and O(1) work at
both ends (see [deque.md](../stacks-and-queues/deque.md)). A related idea is the **ring buffer** — a fixed-size array whose indexes
wrap around with `index % capacity`, used for streaming data and covered with queues in
[queue-fundamentals.md](../stacks-and-queues/queue-fundamentals.md).

## ⚙️ Costs and Uses

| Operation | Cost |
|-----------|------|
| Access the front or back | O(1) (via the tail reference) |
| Insert at the front or back | O(1) |
| Remove the front | O(1) |
| Remove the back | O(n) — as in any singly linked list, the predecessor must be found |
| Rotate by one | O(1) |
| Find a value | O(n) (stop after one full circle) |

Typical uses: round-robin schedulers, turn-taking in multiplayer games, circular buffers and playlists that loop, and repeated
animations or carousels.

## Common Mistakes

- **Writing `while node is not None:`**, which loops forever on a circular list. Count steps, or stop on returning to the start.
- **Testing "back at the start" before processing the head** — the loop then skips a one-element list.
- **Forgetting the single-node case**: a lone node's `next` is itself, and removing it must set the tail to `None`.
- **Breaking the circle** by leaving `tail.next` pointing at `None` or at a removed node after a deletion.
- **Printing a node's `repr` with its `next` links**, which recurses forever around the circle.
- **Using it where a `deque` would do** — `deque.rotate` already provides an efficient rotation.

## ➡️ Next

Continue to [common-linked-list-problems.md](common-linked-list-problems.md) for the classic interview problems: reversing, finding the
middle, detecting cycles, merging, and more — the techniques that complete this module.
