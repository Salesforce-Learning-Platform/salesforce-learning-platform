# ↔️ Doubly Linked Lists

## A Link Backward, and What It Buys

In a [singly linked list](singly-linked-lists.md), a node knows only its successor. That one-way link caused every awkward
cost in the last file: `pop_back` had to walk the whole list to find the second-to-last node, and `remove` needed the node *before*
the target, found by walking. A **doubly linked list** gives each node a second reference, `prev`, to its predecessor:

```
        ┌──────┐      ┌──────┐      ┌──────┐
None ◀──│  10  │◀────▶│  20  │◀────▶│  30  │──▶ None
        └──────┘      └──────┘      └──────┘
           ▲                            ▲
          head                         tail
```

Each link now exists in both directions. The payoff is that a node can **unlink itself**: knowing both neighbours, it can connect them
to each other in O(1) without any walking. This file builds a doubly linked list with sentinel nodes, uses it to get O(1) work at both
ends and O(1) removal of any node you hold, and finishes with a complete LRU cache built from a dictionary and a doubly linked list.
All outputs were produced by running the code on CPython 3.9.

## 🧱 Nodes With Two Links, and Sentinels at Both Ends

The singly linked list needed special cases for the head and tail. A doubly linked list avoids nearly all of them with two **sentinel**
nodes — permanent, empty nodes at each end that never hold data:

```
 _head  ⇄  node A  ⇄  node B  ⇄  node C  ⇄  _tail
(sentinel)                               (sentinel)
```

Every real node always has a real or sentinel neighbour on both sides, so inserting and removing never has to ask "is this the
first node?" or "is this the last?". An empty list is simply `_head ⇄ _tail`.

```python
class DNode:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self, values=()):
        self._head = DNode(None)                    # sentinel before the first element
        self._tail = DNode(None)                    # sentinel after the last element
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
        for value in values:
            self.push_back(value)

    def __len__(self):
        return self._size

    def __iter__(self):                             # front to back
        node = self._head.next
        while node is not self._tail:
            yield node.value
            node = node.next

    def reversed(self):                             # back to front: this is free with prev links
        node = self._tail.prev
        while node is not self._head:
            yield node.value
            node = node.prev

    def __repr__(self):
        return f"DoublyLinkedList({list(self)})"

    def _insert_between(self, value, before, after):
        node = DNode(value)
        node.prev, node.next = before, after
        before.next = node                          # four reference updates, no matter how long the list is
        after.prev = node
        self._size += 1
        return node

    def push_front(self, value):                    # O(1); returns the node as a "handle"
        return self._insert_between(value, self._head, self._head.next)

    def push_back(self, value):                     # O(1)
        return self._insert_between(value, self._tail.prev, self._tail)

    def insert_after(self, node, value):            # O(1) given the node
        return self._insert_between(value, node, node.next)

    def insert_before(self, node, value):           # O(1) given the node
        return self._insert_between(value, node.prev, node)

    def remove(self, node):                         # O(1) given the node: no walk to find a predecessor
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None
        self._size -= 1
        return node.value

    def pop_front(self):                            # O(1)
        if self._size == 0:
            raise IndexError("pop from empty list")
        return self.remove(self._head.next)

    def pop_back(self):                             # O(1): the singly linked version was O(n)
        if self._size == 0:
            raise IndexError("pop from empty list")
        return self.remove(self._tail.prev)

    def move_to_front(self, node):                  # O(1): unlink and relink the same node
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev, node.next = self._head, self._head.next
        self._head.next.prev = node
        self._head.next = node

items = DoublyLinkedList([1, 2, 3])
b = items.push_back(4)
items.push_front(0)
items.insert_after(b, 5)
print(items, len(items))                  # DoublyLinkedList([0, 1, 2, 3, 4, 5]) 6
print(list(items.reversed()))             # [5, 4, 3, 2, 1, 0]
print(items.remove(b), items)             # 4 DoublyLinkedList([0, 1, 2, 3, 5])
print(items.pop_back(), items.pop_front(), items)      # 5 0 DoublyLinkedList([1, 2, 3])
```

Study `_insert_between` and `remove` — together they are the whole technique. Insertion creates a node and rewires **four**
references (the new node's two, and one on each neighbour). Removal rewires **two** (the neighbours point at each other) and clears the
removed node's own links. Neither cares how long the list is.

**Handles.** Notice that `push_back` and `insert_after` *return the node*. A caller who keeps that node can later call
`items.remove(node)` or `items.move_to_front(node)` in O(1), with no search. Arrays cannot offer that: removing an arbitrary element
costs O(n) because of shifting, even if you know its position. This ability is what makes a doubly linked list the right partner for a
hash table, as the LRU cache below shows.

### Testing Against a Model

The test keeps a Python list of the same nodes, so it can pick a random node to remove, move, or insert next to:

```python
import random

random.seed(5)
mine = DoublyLinkedList()
nodes = []                                          # the same nodes, in the same order, held in a Python list
for step in range(20000):
    action = random.choice(["push_front", "push_back", "insert_after", "insert_before", "remove", "move_to_front", "pop_front", "pop_back"])
    value = random.randint(0, 99)
    if action == "push_front":
        nodes.insert(0, mine.push_front(value))
    elif action == "push_back":
        nodes.append(mine.push_back(value))
    elif action == "insert_after" and nodes:
        i = random.randrange(len(nodes))
        nodes.insert(i + 1, mine.insert_after(nodes[i], value))
    elif action == "insert_before" and nodes:
        i = random.randrange(len(nodes))
        nodes.insert(i, mine.insert_before(nodes[i], value))
    elif action == "remove" and nodes:
        node = nodes.pop(random.randrange(len(nodes)))
        expected = node.value
        assert mine.remove(node) == expected
    elif action == "move_to_front" and nodes:
        node = nodes.pop(random.randrange(len(nodes)))
        mine.move_to_front(node)
        nodes.insert(0, node)
    elif action == "pop_front" and nodes:
        assert mine.pop_front() == nodes.pop(0).value
    elif action == "pop_back" and nodes:
        assert mine.pop_back() == nodes.pop().value
    assert list(mine) == [n.value for n in nodes] and len(mine) == len(nodes)
    assert list(mine.reversed()) == [n.value for n in reversed(nodes)]
print("20,000 random operations agree with the model, in both directions")
```

```text
20,000 random operations agree with the model, in both directions
```

Checking the reversed traversal on every step is what catches a forgotten `prev` update — the typical doubly-linked-list bug, because a
list with a broken `prev` link still *looks* correct when read forward.

## ⚙️ What Changed in the Costs

| Operation | Singly (with tail) | Doubly (with sentinels) |
|-----------|--------------------|-------------------------|
| Insert/remove at the front | O(1) | O(1) |
| Insert at the back | O(1) | O(1) |
| **Remove the last element** | O(n) | **O(1)** |
| **Remove a given node** | O(n): find the predecessor | **O(1)** |
| Insert before a given node | O(n) | **O(1)** |
| Walk backward | Impossible | Easy |
| Find a value / read index *i* | O(n) | O(n) (can start from the nearer end) |
| Extra memory per node | one reference | **two references** |

The extra reference is not free:

```python
import sys

class SinglyNode:                                  # the node from the previous file, for comparison
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

print(sys.getsizeof(SinglyNode(1)), "bytes for a singly linked node")
print(sys.getsizeof(DNode(1)), "bytes for a doubly linked node")
```

One run on the test machine printed:

```
48 bytes for a singly linked node
56 bytes for a doubly linked node
```

(Both classes use `__slots__`.) Each node carries one more 8-byte pointer, about 17% more per node, and
every insertion and removal updates more references — which is why you reach for a doubly linked list only when you need what it adds.

## 🧠 A Practical Showpiece: An LRU Cache From Scratch

A **Least Recently Used (LRU) cache** keeps a bounded number of items; when it is full, adding a new item evicts the one that was
used least recently. Both `get` and `put` must be O(1). The requirements pull in two directions:

- *Look up by key in O(1)* → a hash table (see [hash-tables.md](../hashing/hash-tables.md)).
- *Track recency order and move an item to "most recent" in O(1)* → a doubly linked list, kept in recency order, where a hit is unlinked
  from wherever it is and relinked at the front.

The dictionary maps each key to its **list node**, and that handle is what makes the O(1) relinking possible:

```python
class LRUCache:
    def __init__(self, capacity):
        self._capacity = capacity
        self._order = DoublyLinkedList()            # front = most recently used, back = least recently used
        self._nodes = {}                            # key -> the node holding (key, value)

    def get(self, key):
        node = self._nodes.get(key)
        if node is None:
            return None
        self._order.move_to_front(node)             # a hit makes it the most recently used
        return node.value[1]

    def put(self, key, value):
        node = self._nodes.get(key)
        if node is not None:
            node.value = (key, value)               # update in place and mark as most recent
            self._order.move_to_front(node)
            return
        self._nodes[key] = self._order.push_front((key, value))
        if len(self._order) > self._capacity:
            evicted_key, _ = self._order.pop_back() # the least recently used entry
            del self._nodes[evicted_key]            # ...and forget its handle

cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
print(cache.get("a"))             # 1      — "a" becomes the most recently used
cache.put("c", 3)                 # over capacity: evicts "b"
print(cache.get("b"))             # None
print(cache.get("a"), cache.get("c"))    # 1 3
```

Each node stores `(key, value)` rather than only the value, because when the back node is evicted we need its *key* to delete it from the
dictionary. This is the same behaviour as the `OrderedDict`-based `LRUCache` in
[hash-based-problem-solving.md](../hashing/hash-based-problem-solving.md) — which is simply this design packaged in the standard library. A
test against a plain-list model confirms it:

```python
class ListLRU:                                      # a slow but obviously correct model
    def __init__(self, capacity):
        self.capacity, self.items = capacity, []     # least recently used first
    def get(self, key):
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.append(self.items.pop(i))
                return v
        return None
    def put(self, key, value):
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                break
        self.items.append((key, value))
        if len(self.items) > self.capacity:
            self.items.pop(0)

random.seed(3)
for capacity in (1, 2, 3, 5):
    fast, slow = LRUCache(capacity), ListLRU(capacity)
    for step in range(8000):
        key = random.randint(0, 9)
        if random.random() < 0.5:
            fast.put(key, step)
            slow.put(key, step)
        else:
            assert fast.get(key) == slow.get(key)
print("LRU cache agrees with the model for capacities 1, 2, 3 and 5")
```

```text
LRU cache agrees with the model for capacities 1, 2, 3 and 5
```

## 🌍 Where Doubly Linked Lists Appear

- **`collections.deque`** — Python's double-ended queue is a doubly linked list of 64-slot blocks (see
  [deque.md](../stacks-and-queues/deque.md)).
- **LRU caches** and other eviction policies, as above.
- **Browser history, undo/redo, and playlists** — anything with "previous" and "next" and a current position.
- **Text editors** that keep the lines or gaps of a document in a list so insertion at the cursor is cheap.
- **Operating systems** — kernels keep tasks and memory blocks in linked lists for O(1) insertion and removal.

## Common Mistakes

- **Updating only one direction of a link.** Every insert must set `prev` *and* `next` on the new node and update a neighbour in each
  direction (four assignments); every removal must update both neighbours. Test reversed traversal.
- **Wrong order of assignments**, overwriting a reference before reading it. Using local variables for `before` and `after` first, as
  `_insert_between` does, avoids this.
- **Forgetting the sentinels are not data** — iterate until you reach `_tail`, and never expose them.
- **Calling `remove` twice with the same node** or using a node after removing it (its links are cleared on purpose).
- **Storing only the value in LRU nodes**, then being unable to delete the evicted key from the dictionary.
- **Choosing a doubly linked list when a `deque` or `list` is enough** — in Python that is most of the time.

## ➡️ Next

Continue to [circular-linked-lists.md](circular-linked-lists.md) to connect the end of a list back to its beginning, which suits
round-robin scheduling and puzzles like the Josephus problem.
