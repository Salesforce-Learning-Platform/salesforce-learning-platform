# 🔗 Linked Lists

## 📚 Overview

A linked list stores a sequence as separate **nodes**, each holding a value and a **reference** to the next node (and, in a doubly linked
list, to the previous one). Where an [array](../arrays/README.md) keeps elements side by side in memory and gives instant index access, a
linked list scatters them and follows references — trading random access for cheap rearrangement. It is the first structure in this domain
built from *references*, and the pointer-manipulation skills it teaches carry straight into trees, graphs, hash-table chains, queues, and caches.

This module builds singly, doubly, and circular linked lists from scratch, measures their real costs against Python's `list` and
`collections.deque`, builds an LRU cache and solves the Josephus problem with them, and collects the pointer techniques — dummy heads,
slow/fast pointers, in-place reversal, gap pointers, pointer switching — that solve most interview questions. Every class was tested against
a model with tens of thousands of random operations, every algorithm against a reference on thousands of random inputs, and every benchmark
is a real measurement on CPython 3.9.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Build singly, doubly, and circular linked lists, and state the cost of every operation and the reason for it.
- Use sentinel (dummy) nodes to eliminate head and tail special cases, and keep references (tail, handles) that turn O(n) operations into O(1).
- Explain when a linked list beats an array (front insertion, removal of a known node) and when it does not (indexing, memory, cache locality).
- Combine a hash table with a doubly linked list to build an LRU cache with O(1) `get` and `put`.
- Solve the classic problems: reverse, middle, cycle detection and cycle start, merge, *n*-th from the end, palindrome, intersection, and
  duplicate removal.
- Recognize the six places pointer bugs hide: saving `next`, the empty list, one node, the head, the tail, and cycles.

## 📋 Prerequisites

- [Arrays](../arrays/README.md) — the structure linked lists are compared with throughout.
- [Time and Space Complexity](../time-and-space-complexity/README.md) — every claim is stated in Big-O terms.
- [Recursion](../recursion/README.md) — used for the recursive reversal and to explain stack cost.
- [Hashing](../hashing/README.md) — the LRU cache pairs a dictionary with a linked list.
- Basic Python reading ability — the examples use Python classes, generators, and dictionaries.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [singly-linked-lists.md](singly-linked-lists.md) | Nodes and references, a complete singly linked list, the dummy head, and measured memory, traversal, and front-insertion costs |
| [doubly-linked-lists.md](doubly-linked-lists.md) | A second link, sentinels at both ends, O(1) removal by handle, and an LRU cache built from scratch |
| [circular-linked-lists.md](circular-linked-lists.md) | A list with no end: tail-only access, O(1) rotation, the Josephus problem, round-robin scheduling |
| [common-linked-list-problems.md](common-linked-list-problems.md) | Eight classic problems and the five pointer techniques behind them; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [common-linked-list-problems.md](common-linked-list-problems.md) if you are preparing for coding interviews — reversal, cycle
detection, merging, and the *n*-th node from the end are among the most frequently asked questions, and the reasoning (such as why Floyd's
method finds the cycle start) is a common follow-up. Read [doubly-linked-lists.md](doubly-linked-lists.md) for the LRU cache, a popular
design question.

**Skim** [singly-linked-lists.md](singly-linked-lists.md) if you already know the basic structure — but look at the dummy-head technique and
the measured comparison with `list`, which explain *why* linked lists are used less in everyday Python than the textbooks suggest.
[circular-linked-lists.md](circular-linked-lists.md) is the lightest file and can be skimmed unless you need rotation or scheduling.

## 🧠 Knowledge Check

<details>
<summary>"Inserting into a linked list is O(1), but inserting into an array is O(n)." Why is that statement incomplete, and what is the more accurate version?</summary>

The O(1) refers only to the *splice itself*: rewiring a couple of references once you are already holding the node before the
insertion point. To *get* to that position in a linked list you must walk from the head, which is O(n) — there is no index to jump
to. So inserting at the **front** (or anywhere you already hold a reference) is O(1), while inserting at a position given by index or value is
O(n) for both structures: shifting in the array, walking in the list. A linked list wins when the position is already known or is the front,
and an array usually wins otherwise, helped by its memory layout. See [singly-linked-lists.md](singly-linked-lists.md).

</details>

<details>
<summary>How does the slow/fast pointer technique detect a cycle, and why does it need only O(1) extra memory?</summary>

Two pointers walk the list, `slow` one step at a time and `fast` two. If the list ends, `fast` reaches `None` and there is no cycle. If there
is a cycle, both pointers eventually enter it, and since `fast` gains one node on `slow` per step, it must catch up and land on the same
node — so meeting proves a cycle. Only two references are stored, regardless of the list's length, so extra space is O(1). The
alternative of recording visited nodes in a set also takes O(n) time but needs O(n) memory. See
[common-linked-list-problems.md](common-linked-list-problems.md).

</details>

## 📚 References

- [Python docs: `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) — Python's double-ended queue, itself a doubly linked list of blocks.
- [CPython source: `Modules/_collectionsmodule.c`](https://github.com/python/cpython/blob/3.9/Modules/_collectionsmodule.c) — the implementation notes for `deque` blocks.
- [Python docs: `itertools.cycle`](https://docs.python.org/3/library/itertools.html#itertools.cycle) — repeating a sequence forever.
- [Wikipedia: Linked list](https://en.wikipedia.org/wiki/Linked_list) — variants, trade-offs, and history.
- [Wikipedia: Cycle detection](https://en.wikipedia.org/wiki/Cycle_detection) — Floyd's tortoise-and-hare algorithm and its analysis.
- [Wikipedia: Josephus problem](https://en.wikipedia.org/wiki/Josephus_problem) and [Round-robin scheduling](https://en.wikipedia.org/wiki/Round-robin_scheduling) — the two applications used in the circular-list file.
- [W3Schools: DSA Linked Lists](https://www.w3schools.com/dsa/dsa_theory_linkedlists.php) — a beginner-friendly illustrated introduction.
- [GeeksforGeeks: Linked List Data Structure](https://www.geeksforgeeks.org/dsa/linked-list-data-structure/) — an overview and a long list of practice problems.

## ➡️ Continue Your Learning Path

Continue to the [Stacks and Queues](../stacks-and-queues/README.md) module, the next module in this domain, where two restricted ways of
adding and removing items power function calls, undo, scheduling, and graph search.
