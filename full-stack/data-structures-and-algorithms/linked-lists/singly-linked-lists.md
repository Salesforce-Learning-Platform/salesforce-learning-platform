# 🔗 Singly Linked Lists

## Data Connected by References Instead of Stored Side by Side

An [array](../arrays/array-fundamentals.md) keeps its elements in one contiguous block, which is why reading by index is O(1) but
inserting at the front is O(n): everything must shift. A **linked list** takes the opposite trade. Each element lives in its own small
object called a **node**, and each node holds a **reference** (a pointer) to the next one. Elements can be anywhere in memory; the
references are the order.

```
head
  │
  ▼
┌────┬───┐   ┌────┬───┐   ┌────┬───┐
│ 10 │ ●─┼──▶│ 20 │ ●─┼──▶│ 30 │ ╳ │        ╳ = None: the end of the list
└────┴───┘   └────┴───┘   └────┴───┘
 value next
```

A *singly* linked list has one reference per node (to the next node), so you can only walk forward. This file builds one, shows what
each operation costs and why, and measures the real trade-offs against Python's `list`. All outputs were produced by running the code on
CPython 3.9.

## 🧱 The Building Blocks

```python
class Node:
    __slots__ = ("value", "next")        # no per-node __dict__: a node is two fields and nothing else

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

# build 10 -> 20 -> 30 by hand
head = Node(10, Node(20, Node(30)))
print(head.value, head.next.value, head.next.next.value)     # 10 20 30
print(head.next.next.next)                                    # None
```

Three facts define the structure:

- A list is just a reference to its first node, the **head**. Lose the head and you lose the whole list.
- The last node's `next` is `None`; that is how every walk knows when to stop.
- There is no index. To reach the third element you must follow the references from the head, one at a time.

Walking the list is the basic loop, and almost every operation is a variation of it:

```python
def to_list(head):
    values = []
    node = head
    while node is not None:
        values.append(node.value)
        node = node.next
    return values

print(to_list(head))        # [10, 20, 30]
```

## 🛠️ A Complete Singly Linked List

Keeping a reference to the last node (the **tail**) as well as the head makes appending O(1). Here is a full class, with the cost of
each method in its comment:

```python
class SinglyLinkedList:
    def __init__(self, values=()):
        self.head = None
        self.tail = None
        self._size = 0
        for value in values:
            self.append(value)

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __repr__(self):
        return f"SinglyLinkedList({list(self)})"

    def prepend(self, value):                       # O(1)
        self.head = Node(value, self.head)
        if self.tail is None:                       # the list was empty
            self.tail = self.head
        self._size += 1

    def append(self, value):                        # O(1), thanks to the tail reference
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def insert(self, index, value):                 # O(n): must walk to the position
        if not 0 <= index <= self._size:
            raise IndexError("insert index out of range")
        if index == 0:
            return self.prepend(value)
        if index == self._size:
            return self.append(value)
        previous = self._node_at(index - 1)
        previous.next = Node(value, previous.next)  # splice in after `previous`: two reference updates
        self._size += 1

    def pop_front(self):                            # O(1)
        if self.head is None:
            raise IndexError("pop from empty list")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return node.value

    def pop_back(self):                             # O(n): a singly linked node cannot reach its predecessor
        if self.head is None:
            raise IndexError("pop from empty list")
        if self.head is self.tail:
            return self.pop_front()
        previous = self.head
        while previous.next is not self.tail:
            previous = previous.next
        value = self.tail.value
        previous.next = None
        self.tail = previous
        self._size -= 1
        return value

    def remove(self, value):                        # O(n): remove the first match, return True if found
        previous, node = None, self.head
        while node is not None:
            if node.value == value:
                if previous is None:
                    self.head = node.next
                else:
                    previous.next = node.next       # bypass the node
                if node is self.tail:
                    self.tail = previous
                self._size -= 1
                return True
            previous, node = node, node.next
        return False

    def find(self, value):                          # O(n): index of the first match, or -1
        for index, existing in enumerate(self):
            if existing == value:
                return index
        return -1

    def __contains__(self, value):
        return self.find(value) != -1

    def get(self, index):                           # O(n): there is no random access
        return self._node_at(index).value

    def _node_at(self, index):
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        node = self.head
        for _ in range(index):
            node = node.next
        return node

items = SinglyLinkedList([1, 2, 3])
items.prepend(0)
items.append(4)
items.insert(2, 99)
print(items, len(items))          # SinglyLinkedList([0, 1, 99, 2, 3, 4]) 6
print(items.get(2), items.find(3), 3 in items, 42 in items)    # 99 4 True False
print(items.remove(99), items.remove(99), items)               # True False SinglyLinkedList([0, 1, 2, 3, 4])
print(items.pop_front(), items.pop_back(), items)              # 0 4 SinglyLinkedList([1, 2, 3])
```

### Why Each Operation Costs What It Does

- **`prepend`** creates one node and points it at the old head — two steps regardless of the list's length: **O(1)**.
- **`append`** is also O(1) *because we kept `tail`*. Without a tail reference it must walk the whole list to find the end: O(n).
- **`insert(index, …)`** has two parts: walking to the node before the position (O(n)) and the splice itself (O(1)). The splice is
  the part linked lists are good at — it changes two references and moves nothing. The walk is the part they are bad at.
- **`pop_back`** is **O(n)** even with a tail reference: to make the *second-to-last* node the new tail, you must find it, and a
  node only knows its successor. This is the main motivation for the [doubly linked list](doubly-linked-lists.md).
- **`remove(value)`** must find the value first (O(n)) while remembering the node *before* it, because that node's `next` is the
  reference to change.

Always check the **edge cases** around the ends: removing the head, removing the tail (the `tail` reference must move), removing the
only element (both `head` and `tail` become `None`), and operating on an empty list. Most linked-list bugs live there.

### A Testing Habit

A new data structure should be tested against one that is known to be right. This runs 30,000 random operations on the list and on a
Python `list` side by side and compares the results:

```python
import random

random.seed(7)
mine, model = SinglyLinkedList(), []
for step in range(30000):
    action = random.choice(["prepend", "append", "insert", "remove", "pop_front", "pop_back", "get", "find"])
    value = random.randint(0, 20)
    if action == "prepend":
        mine.prepend(value); model.insert(0, value)
    elif action == "append":
        mine.append(value); model.append(value)
    elif action == "insert":
        index = random.randint(0, len(model))
        mine.insert(index, value); model.insert(index, value)
    elif action == "remove":
        expected = value in model
        if expected:
            model.remove(value)
        assert mine.remove(value) == expected
    elif action == "pop_front" and model:
        assert mine.pop_front() == model.pop(0)
    elif action == "pop_back" and model:
        assert mine.pop_back() == model.pop()
    elif action == "get" and model:
        index = random.randrange(len(model))
        assert mine.get(index) == model[index]
    elif action == "find":
        assert mine.find(value) == (model.index(value) if value in model else -1)
    assert list(mine) == model and len(mine) == len(model)
    assert (mine.tail.value if mine.tail else None) == (model[-1] if model else None)
print("30,000 random operations agree with a Python list")
```

```text
30,000 random operations agree with a Python list
```

The last assertion checks the `tail` reference too — the easiest thing to forget to update.

## 🛡️ The Dummy-Head Technique

Deleting a node requires changing the `next` of the node *before* it — but the head has no node before it, so it needs a special case. A
**dummy** (or sentinel) node placed in front of the real head removes the special case: every real node now has a predecessor.

```python
def build(values):
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head

def remove_all(head, target):
    dummy = Node(None, head)               # a fake node before the head
    previous = dummy
    while previous.next is not None:
        if previous.next.value == target:
            previous.next = previous.next.next      # unlink: no special case for the head
        else:
            previous = previous.next
    return dummy.next                      # the (possibly new) head

print(to_list(remove_all(build([7, 1, 7, 7, 2, 7]), 7)))    # [1, 2]
print(to_list(remove_all(build([5, 5, 5]), 5)))             # []
print(to_list(remove_all(build([]), 5)))                    # []
```

The first list shows the payoff: the head itself is removed, and so are consecutive nodes, with no `if previous is None` branch. The
function returns `dummy.next` because the head may have changed. This pattern appears throughout
[common-linked-list-problems.md](common-linked-list-problems.md).

## 📏 Measured Trade-Offs Against `list`

Linked lists are taught as the structure with O(1) insertion — but whether that matters depends on what the competition costs. Two
measurements on CPython 3.9.

**Memory.** Every node is a separate object:

```python
import sys
import tracemalloc

class NodeWithDict:                      # an ordinary class: every instance also carries a __dict__
    def __init__(self, value, next=None):
        self.value, self.next = value, next

print(sys.getsizeof(Node(1)), "bytes per Node with __slots__")
print(sys.getsizeof(NodeWithDict(1)) + sys.getsizeof(NodeWithDict(1).__dict__), "bytes per node without __slots__")
print((sys.getsizeof(list(range(1000))) - sys.getsizeof(list(range(100)))) // 900, "bytes per Python list slot (one pointer)")

n = 200_000
tracemalloc.start()
start = tracemalloc.get_traced_memory()[0]
linked = build(list(range(n)))
after_linked = tracemalloc.get_traced_memory()[0]
array = list(range(n))
after_array = tracemalloc.get_traced_memory()[0]
tracemalloc.stop()
print(f"{(after_linked - start) / n:.0f} bytes per element (linked list, includes the int object)")
print(f"{(after_array - after_linked) / n:.0f} bytes per element (Python list, includes the int object)")
```

One run on the test machine printed:

```
48 bytes per Node with __slots__
152 bytes per node without __slots__
8 bytes per Python list slot (one pointer)
76 bytes per element (linked list, includes the int object)
36 bytes per element (Python list, includes the int object)
```

A node costs about **48 bytes** of overhead for two references, against **8 bytes** for a slot in a Python list (one pointer). Without
`__slots__` the node would cost 152 bytes. Per element, the linked list used roughly twice the memory of the list here, once the shared
cost of the integer objects is included.

**Speed.** Walking a linked list versus looping over a list, and building by inserting at the front:

```python
import timeit
from collections import deque

def walk(head):
    total = 0
    while head is not None:
        total += head.value
        head = head.next
    return total

print(f"{'n':>9} | {'walk linked list':>16} | {'for loop over list':>18}   (ms)")
for n in (10_000, 100_000, 1_000_000):
    linked = build(list(range(n)))
    array = list(range(n))

    def loop_over_list():
        total = 0
        for value in array:
            total += value
        return total

    t_linked = min(timeit.repeat(lambda: walk(linked), number=3, repeat=3)) / 3 * 1000
    t_array = min(timeit.repeat(loop_over_list, number=3, repeat=3)) / 3 * 1000
    print(f"{n:>9,} | {t_linked:16.2f} | {t_array:18.2f}")

print()
print(f"{'n':>9} | {'linked prepend':>14} | {'list.insert(0)':>14} | {'deque.appendleft':>16}   (ms to insert n items at the front)")
for n in (10_000, 20_000, 40_000):
    def with_linked():
        head = None
        for value in range(n):
            head = Node(value, head)

    def with_list():
        items = []
        for value in range(n):
            items.insert(0, value)

    def with_deque():
        items = deque()
        for value in range(n):
            items.appendleft(value)

    times = [min(timeit.repeat(fn, number=1, repeat=3)) * 1000 for fn in (with_linked, with_list, with_deque)]
    print(f"{n:>9,} | {times[0]:14.2f} | {times[1]:14.2f} | {times[2]:16.2f}")
```

One run on the test machine printed:

```
        n | walk linked list | for loop over list   (ms)
   10,000 |             0.40 |               0.21
  100,000 |             4.19 |               1.98
1,000,000 |            41.41 |              20.22

        n | linked prepend | list.insert(0) | deque.appendleft   (ms to insert n items at the front)
   10,000 |           1.22 |          13.72 |             0.32
   20,000 |           2.50 |          54.17 |             0.65
   40,000 |           5.09 |         214.65 |             1.27
```

Read the two tables separately:

- **Walking** a linked list is slower than looping over a list (about twice as slow here, even though both are plain Python loops).
  Each step follows a reference to an object that may be anywhere in memory, whereas a list's elements are laid out together, which
  CPU caches reward. In compiled languages this *cache locality* effect is often much larger.
- **Inserting at the front** shows the linked list's strength: its time doubles when `n` doubles (O(1) each), while `list.insert(0, …)`
  roughly **quadruples** (O(n) each — the shifting from
  [insertion-and-deletion.md](../arrays/insertion-and-deletion.md)). But `collections.deque.appendleft`, also O(1), beats the hand-built
  linked list: a deque is itself a doubly linked list, stored in blocks of 64 elements to reduce the per-node overhead (CPython's
  `Modules/_collectionsmodule.c` describes it as "a doubly-linked list of fixed-length blocks").

## ⚖️ Arrays or Linked Lists?

| | Array / Python `list` | Singly linked list |
|--|-----------------------|--------------------|
| Read the *i*-th element | **O(1)** | O(n) |
| Insert/delete at the front | O(n) | **O(1)** |
| Insert/delete at the back | O(1) amortized (append/pop) | append O(1) with a tail; removal O(n) |
| Insert/delete in the middle *given the position* | O(n): shifting | **O(1)** if you already hold the previous node |
| Find a value | O(n) | O(n) |
| Memory per element | One pointer (8 bytes) | One node object (48 bytes + the value) |
| Cache behavior | Excellent: contiguous | Poor: scattered nodes |
| Size must be known or resized | Resizes by doubling (amortized O(1)) | Grows one node at a time |

The honest summary: **in everyday Python, a `list` (or a `deque`) is almost always the better choice.** Linked lists matter because they
(1) teach pointer manipulation, which every later structure — trees, graphs, hash-table chains — depends on; (2) are the building block
of structures such as queues, LRU caches, and `deque`; (3) give O(1) insertion and removal *wherever you already hold a reference*, which
arrays cannot match; and (4) are an interview staple.

## Common Mistakes

- **Losing the rest of the list** by overwriting `node.next` before saving it. When splicing, link the *new* node first.
- **Forgetting to update `tail`** when removing the last node or inserting at the end.
- **Not handling the empty list**, a single node, or the head separately — use a dummy head to avoid special cases.
- **Walking off the end** (`node.next.next` when `node.next` is `None`) and getting `AttributeError: 'NoneType' object has no attribute…`.
- **Believing linked-list indexing is O(1)**, or that "insert is O(1)" without counting the walk needed to *find* the position.
- **Creating cycles accidentally** — pointing a later node back at an earlier one makes every traversal loop forever.
- **Returning the old head** from a function that may have changed it.

## ➡️ Next

Continue to [doubly-linked-lists.md](doubly-linked-lists.md) to add a second reference per node — a link backward — and see what that
makes possible: O(1) removal of any known node, O(1) work at both ends, and a from-scratch LRU cache.
