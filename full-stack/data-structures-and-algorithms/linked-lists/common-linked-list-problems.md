# 🧩 Common Linked List Problems

## Five Techniques Behind Almost Every Question

Linked-list interview problems look varied — reverse it, find the middle, detect a loop, merge two lists — but they are solved with a
small toolkit of pointer techniques:

| Technique | Idea | Used for |
|-----------|------|----------|
| **Dummy head** | A fake node before the head removes the "is this the head?" special case | Merging, deleting |
| **Slow and fast pointers** | One pointer moves 1 step, another moves 2 | Middle, cycles |
| **In-place reversal** | Flip each `next` link while walking | Reversing, palindromes |
| **Gap pointers** | Advance one pointer `n` steps ahead, then move both together | The *n*-th node from the end |
| **Pointer switching** | When a pointer reaches the end, restart it on the other list | Finding where two lists meet |

This file works through eight problems using those techniques, each solved in **O(n) time**, mostly in **O(1) extra space**. Every function
was run and checked against a list-based reference on thousands of random inputs. The input and output are linked lists of the `Node`
class from [singly-linked-lists.md](singly-linked-lists.md); the helpers below build and print them.

```python
class Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def build(values):
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head

def to_list(head):
    values = []
    while head is not None:
        values.append(head.value)
        head = head.next
    return values

print(to_list(build([1, 2, 3])))        # [1, 2, 3]
```

## 1️⃣ Reverse a List

Reversing means making every node point to its *predecessor* instead of its successor. Walk down the list keeping three references:
the node you are on, the one before it, and — saved *before* you change anything — the one after it.

```python
def reverse_list(head):
    previous = None
    node = head
    while node is not None:
        following = node.next        # 1. save the rest of the list before we break the link
        node.next = previous         # 2. flip this node's link to point backward
        previous = node              # 3. advance: this node becomes the "previous" one
        node = following
    return previous                  # `previous` ends on the old last node: the new head

print(to_list(reverse_list(build([1, 2, 3, 4]))))     # [4, 3, 2, 1]
print(to_list(reverse_list(build([]))))               # []
```

Trace on `1 → 2 → 3`:

```
start:        previous=None   node=1
after step 1: 1 → None        node=2     (1 now points backward at None)
after step 2: 2 → 1 → None    node=3
after step 3: 3 → 2 → 1 → None  node=None → return 3
```

**O(n) time, O(1) space.** If step 1 is skipped, flipping `node.next` loses the rest of the list — the most common bug. The same job can be
done recursively: reverse everything after the head, then make the old second node point back at the head.

```python
def reverse_recursive(head):
    if head is None or head.next is None:         # base case: empty or one node
        return head
    new_head = reverse_recursive(head.next)       # reverse the rest; new_head is the old last node
    head.next.next = head                         # the node after head now points back at head
    head.next = None                              # head becomes the tail
    return new_head

print(to_list(reverse_recursive(build([1, 2, 3, 4]))))   # [4, 3, 2, 1]
```

This is elegant but uses O(n) stack space and hits Python's recursion limit (about 1,000) on long lists — see
[recursion-fundamentals.md](../recursion/recursion-fundamentals.md). Prefer the loop.

## 2️⃣ Find the Middle (Slow and Fast Pointers)

Counting the nodes and then walking half-way takes two passes. With two pointers it takes one: `fast` moves two steps for every one step of
`slow`, so when `fast` reaches the end, `slow` is at the middle.

```python
def middle_node(head):                # for an even count, returns the second of the two middle nodes
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow

print(middle_node(build([1, 2, 3, 4, 5])).value)       # 3
print(middle_node(build([1, 2, 3, 4])).value)          # 3     — the second middle of 2 and 3
print(middle_node(build([7])).value)                   # 7
```

The loop condition checks `fast` *and* `fast.next` because `fast` jumps two nodes: for an even count it lands on `None`, for an odd
count on the last node. Checking only one of them risks an `AttributeError` on `None`.

## 3️⃣ Detect a Cycle (Floyd's Tortoise and Hare)

A list that contains a cycle never reaches `None`, so a plain walk loops forever. The slow/fast idea detects it: if there is a loop, `fast`
will eventually lap `slow` and they will land on the *same node*; if there is no loop, `fast` reaches the end.

```python
def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                 # compare identity (the node itself), not values
            return True
    return False

def build_with_cycle(values, cycle_to):       # make the last node point back at the node at index cycle_to
    head = build(values)
    if cycle_to is not None:
        nodes = []
        node = head
        while node is not None:
            nodes.append(node)
            node = node.next
        nodes[-1].next = nodes[cycle_to]
    return head

print(has_cycle(build_with_cycle([3, 2, 0, -4], 1)))       # True
print(has_cycle(build_with_cycle([1, 2, 3], None)))        # False
print(has_cycle(build_with_cycle([1], 0)))                 # True     — a single node pointing at itself
```

**O(n) time, O(1) space.** The alternative — remember every visited node in a `set` — is also O(n) time but uses O(n) memory (it is the
[hash-based "seen before?" pattern](../hashing/hash-based-problem-solving.md)). Floyd's method needs no extra storage.

### Finding Where the Cycle Starts

Once the pointers meet, a second phase finds the *start* of the loop. Let `a` be the distance from the head to the cycle's start, `b` the
distance from the start to the meeting point, and `c` the cycle's length. When they meet, `slow` has moved `a + b` steps and `fast` has moved
`2(a + b)`; the difference, `a + b`, must be a whole number of laps: `a + b = m·c`. So `a = m·c − b` — walking `a` steps from the
meeting point lands exactly on the cycle's start. That means: put one pointer back at the head, and move both one step at a time. They
meet at the start of the cycle.

```python
def cycle_start(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                 # phase 1: they met inside the cycle
            slow = head                  # phase 2: restart one pointer at the head...
            while slow is not fast:
                slow = slow.next         # ...and move both one step at a time
                fast = fast.next
            return slow                  # they meet where the cycle begins
    return None

loop = build_with_cycle([3, 2, 0, -4, 9], 1)
print(cycle_start(loop).value)                             # 2     — the node at index 1
print(cycle_start(build([1, 2, 3])))                       # None
```

## 4️⃣ Merge Two Sorted Lists

Repeatedly take the smaller of the two front nodes and append it to the result. A **dummy head** means there is no special case for the first
node appended:

```python
def merge_sorted(a, b):
    dummy = tail = Node(None)
    while a is not None and b is not None:
        if a.value <= b.value:           # `<=` keeps the merge stable: ties come from list `a` first
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b       # attach whichever list still has nodes
    return dummy.next

print(to_list(merge_sorted(build([1, 3, 5]), build([2, 4, 6, 8]))))    # [1, 2, 3, 4, 5, 6, 8]
print(to_list(merge_sorted(build([]), build([1, 2]))))                 # [1, 2]
```

**O(n + m) time, O(1) extra space** — it relinks the existing nodes rather than creating new ones. This is the *merge* step of merge sort, which
works particularly well on linked lists (the Sorting module returns to it).

## 5️⃣ Remove the *n*-th Node From the End

Counting from the end seems to need the length first (two passes). **Gap pointers** do it in one: advance `lead` exactly `n` nodes ahead,
then move `lead` and `trail` together. When `lead` reaches the last node, `trail` is just before the node to delete.

```python
def remove_nth_from_end(head, n):
    if n < 1:
        raise ValueError("n must be at least 1")
    dummy = Node(None, head)
    lead = trail = dummy
    for _ in range(n):
        lead = lead.next
        if lead is None:
            raise ValueError("n is larger than the list")
    while lead.next is not None:         # move both until `lead` is on the last node
        lead = lead.next
        trail = trail.next
    trail.next = trail.next.next         # unlink the node after `trail`
    return dummy.next

print(to_list(remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)))    # [1, 2, 3, 5]
print(to_list(remove_nth_from_end(build([1, 2]), 2)))             # [2]       — removing the head works too
print(to_list(remove_nth_from_end(build([1]), 1)))                # []
```

The dummy head is what makes removing the *first* node (`n` equal to the length) work with no special case. **O(n) time, one pass,
O(1) space.**

## 6️⃣ Is the List a Palindrome?

Combine two earlier tools: find the middle, **reverse the second half in place**, compare the halves node by node, and (politely) reverse it
back so the caller's list is unchanged:

```python
def is_palindrome_list(head):
    if head is None or head.next is None:
        return True
    second_half = reverse_list(middle_node(head))     # reverse from the middle to the end
    first, other = head, second_half
    result = True
    while other is not None:                          # the second half is never longer than the first
        if first.value != other.value:
            result = False
            break
        first, other = first.next, other.next
    reverse_list(second_half)                         # restore the original list
    return result

print(is_palindrome_list(build([1, 2, 3, 2, 1])))     # True
print(is_palindrome_list(build([1, 2, 2, 1])))        # True
print(is_palindrome_list(build([1, 2, 3])))           # False

original = build([1, 2, 2, 1])
is_palindrome_list(original)
print(to_list(original))                              # [1, 2, 2, 1]   — restored
```

**O(n) time, O(1) space.** The obvious alternative copies the values into a Python list and compares it with its reverse — simpler, but it
spends O(n) memory.

## 7️⃣ Where Do Two Lists Meet?

Two lists may **merge** into one shared tail (the nodes are literally the same objects, not just equal values). Find the first shared node
without extra memory using **pointer switching**: walk one pointer along `a` and then continue along `b`; walk the other along `b` and then
along `a`. Both pointers travel `len(a) + len(b)` nodes in total, so after the lengths even out they arrive at the shared node *at the same
time* — or, if there is none, both reach `None` together.

```python
def intersection_node(a, b):
    p, q = a, b
    while p is not q:
        p = p.next if p is not None else b      # at the end of a, jump to the start of b
        q = q.next if q is not None else a      # at the end of b, jump to the start of a
    return p                                    # the shared node, or None

shared = build([8, 4, 5])
list_a = Node(4, Node(1, shared))
list_b = Node(5, Node(6, Node(1, shared)))
print(intersection_node(list_a, list_b).value)                  # 8
print(intersection_node(build([1, 2]), build([3, 4, 5])))       # None
```

**O(n + m) time, O(1) space.** The hash-set alternative (store every node of `a`, then look for one of `b`) uses O(n) space.

## 8️⃣ Remove Duplicates From a Sorted List

In a sorted list equal values are adjacent, so one pass comparing each node with its successor is enough:

```python
def remove_duplicates_sorted(head):
    node = head
    while node is not None and node.next is not None:
        if node.next.value == node.value:
            node.next = node.next.next          # skip the duplicate; stay on this node (there may be more)
        else:
            node = node.next
    return head

print(to_list(remove_duplicates_sorted(build([1, 1, 2, 3, 3, 3, 4]))))    # [1, 2, 3, 4]
```

Staying on the current node after deleting a duplicate is deliberate: a run of three equal values needs two deletions.

## 🧭 Choosing the Technique

| The problem says… | Reach for… |
|-------------------|-----------|
| "reverse", "in place", "second half" | In-place reversal (save `next` first) |
| "middle", "halfway" | Slow and fast pointers |
| "cycle", "loop", "repeats" | Fast and slow pointers; compare node identity |
| "merge", "delete", "might remove the head" | Dummy head |
| "*n*-th from the end" | Gap pointers (one pass) |
| "where two lists meet" | Pointer switching |

## ⏱️ Summary of Costs

| Problem | Time | Extra space |
|---------|------|-------------|
| Reverse (iterative / recursive) | O(n) | O(1) / O(n) stack |
| Middle node | O(n) | O(1) |
| Detect a cycle / find its start | O(n) | O(1) |
| Merge two sorted lists | O(n + m) | O(1) |
| Remove *n*-th from the end | O(n) | O(1) |
| Palindrome check | O(n) | O(1) |
| Intersection | O(n + m) | O(1) |
| Remove duplicates (sorted) | O(n) | O(1) |

## Common Mistakes

- **Overwriting `next` before saving the rest of the list** when reversing or splicing — the remainder becomes unreachable.
- **Not handling the empty list, one node, or removing the head** — use a dummy head and test these three cases first.
- **Dereferencing `None`** (`fast.next.next` when `fast.next` is `None`). Guard with `fast is not None and fast.next is not None`.
- **Comparing values instead of identity** when looking for a cycle or an intersection — equal values at different nodes are not the same node.
- **Forgetting that reversal changes the head**, then using the old head (now the tail) afterwards.
- **Creating a cycle by accident** when relinking, which turns later traversals into infinite loops.
- **Returning the wrong thing** — most of these functions must return the *new head* because the head can change.

## Module Summary

The Linked Lists module introduced data connected by references. [Singly Linked Lists](singly-linked-lists.md) built the node-and-pointer
structure, showed that insertion at the front is O(1) while indexing is O(n), introduced the dummy head, and measured the real trade-offs
against Python's `list`. [Doubly Linked Lists](doubly-linked-lists.md) added a backward link, giving O(1) removal of any known node and
a from-scratch LRU cache. [Circular Linked Lists](circular-linked-lists.md) closed the loop for rotation, the Josephus problem, and round-robin scheduling.
This file collected the techniques that solve most linked-list problems.

Carry these ideas forward:

- A linked list trades random access for cheap rearrangement: no shifting, but no indexing and poor cache behaviour.
- Pointer discipline is the skill: save references before you overwrite them, and test the empty, single-node, and head cases.
- Dummy heads, slow/fast pointers, in-place reversal, gap pointers, and pointer switching cover most interview problems.
- Trees (later in this domain) are linked structures with more than one `next`; the same reference thinking applies.
- In everyday Python, prefer `list` and `collections.deque`; implement linked lists to understand — and to build structures such as queues
  and LRU caches.

## ➡️ Next

Continue to the [Stacks and Queues](../stacks-and-queues/README.md) module, the next module in this domain, where two restricted ways of
adding and removing items — last-in-first-out and first-in-first-out — turn out to power function calls, undo, scheduling, and graph search.
