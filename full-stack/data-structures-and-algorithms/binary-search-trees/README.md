# 🔍 Binary Search Trees

## 📚 Overview

A **binary search tree (BST)** is a binary tree with one rule: for every node, keys in the left subtree are smaller and keys in the right subtree are larger. That rule turns the
"higher or lower" game of binary search into a *dynamic* structure — one that supports fast search, insertion, and deletion **and** ordered questions that hash tables cannot
answer: the minimum, the next larger key, the k-th smallest, or all keys in a range. The catch is that every operation costs time proportional to the tree's **height**, which depends on
the order keys arrive in. This module builds a BST step by step, shows how its shape can collapse into a linked list, and then fixes the problem with rotations in a self-balancing AVL tree.

Every code example was run on CPython 3.9. The trees were tested against Python's `set` and against sorted-list equivalents (built on `bisect`) with tens of thousands of random operations, the BST and
AVL invariants were checked after every one of them, and the height and timing tables are real measurements.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- State the BST rule precisely, build a BST in Python, and explain why in-order traversal produces sorted output.
- Validate a BST correctly (carrying the allowed key range down the tree) and explain why comparing a node only with its children is wrong.
- Implement search, floor, ceiling, successor, predecessor, k-th smallest, range queries, and lowest common ancestor in O(h).
- Insert keys and delete them in all three cases (leaf, one child, two children via the successor) while preserving the BST rule.
- Explain why a BST's height depends on insertion order, and measure the difference between random and sorted input.
- Describe AVL balancing — balance factors, left and right rotations, and the four imbalance cases — and know where red-black trees and B-trees fit.

## 📋 Prerequisites

- [Trees](../trees/README.md) — the vocabulary, binary-tree shapes, and especially in-order traversal.
- [Recursion](../recursion/README.md) — most BST operations are naturally recursive.
- [Arrays](../arrays/README.md) — binary search on a sorted array is the idea a BST generalizes.
- [Time and Space Complexity](../time-and-space-complexity/README.md) — costs are stated in terms of the height `h`.
- Basic Python reading ability — the examples use Python classes, loops, and recursion.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [bst-fundamentals.md](bst-fundamentals.md) | The rule, a BST class, in-order = sorted, correct validation, and a measured comparison of random versus sorted insertion |
| [search-in-bst.md](search-in-bst.md) | Search, floor and ceiling, successor and predecessor, k-th smallest, pruned range queries, and LCA — checked against `bisect` |
| [insertion-and-deletion.md](insertion-and-deletion.md) | Insertion at a leaf and the three deletion cases, tested against a `set` for 40,000 random operations |
| [balanced-bsts.md](balanced-bsts.md) | AVL trees: rotations, the four cases, full insertion and deletion, invariant checks, measured payoff, and a tour of other balanced trees; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [insertion-and-deletion.md](insertion-and-deletion.md) and the rotation sections of [balanced-bsts.md](balanced-bsts.md) if you are preparing for coding
interviews: deleting a node with two children, validating a BST, and explaining *why* balance matters are standard questions, and being able to draw an AVL rotation is a common
follow-up. The correct-validation trap in [bst-fundamentals.md](bst-fundamentals.md) is asked constantly.

**Skim** [search-in-bst.md](search-in-bst.md) on a first pass if you only need the main idea, but return for floor/ceiling and range queries — they are the operations that justify using a BST
instead of a hash table. Reading the full AVL implementation is optional for most roles; understanding the guarantee and the rotation picture is enough.

## 🧠 Knowledge Check

<details>
<summary>A tree has root 5, left child 3, right child 8, and 3 has a right child 7. Every node is larger than its left child and smaller than its right child. Is it a valid BST?</summary>

No. The BST rule applies to **entire subtrees**, not just to direct children. The key `7` is in the **left** subtree of the root `5`, so it must be smaller than `5` — but it is larger.
Checking each node only against its immediate children (as the naive validator does) misses this. The correct check passes an allowed range `(low, high)` down the tree: going left
tightens `high` to the node's key, going right tightens `low`. See [bst-fundamentals.md](bst-fundamentals.md).

</details>

<details>
<summary>Why do inserting the keys 1, 2, 3, …, n in order into a plain BST and into an AVL tree produce such different performance?</summary>

In a plain BST, each new key is larger than every key so far, so it becomes the right child of the previous key: the tree is a chain of height `n − 1`, and the `i`-th insertion walks `i` nodes —
O(n²) in total, and every later search is O(n). An AVL tree checks the balance factor on the way back up from each insertion and applies a rotation whenever a node becomes lopsided (balance
factor ±2), so the height never exceeds about 1.44 · log₂ n and each insertion costs O(log n). The measured table in [balanced-bsts.md](balanced-bsts.md) shows heights of 3,999 versus 11 and a build time
roughly twelve times longer for the plain tree at 4,000 keys.

</details>

## 📚 References

- [Wikipedia: Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree), [AVL tree](https://en.wikipedia.org/wiki/AVL_tree), [Red–black tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree), and [B-tree](https://en.wikipedia.org/wiki/B-tree) — definitions, height bounds, and variants.
- [Python docs: `bisect`](https://docs.python.org/3/library/bisect.html) — binary search on sorted lists, the standard-library alternative to a balanced tree.
- [`sortedcontainers` on PyPI](https://pypi.org/project/sortedcontainers/) — a popular third-party ordered collection.
- [Java docs: `TreeMap`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/TreeMap.html) — a red-black-tree-based sorted map in a mainstream standard library.
- [W3Schools: DSA Binary Search Trees](https://www.w3schools.com/dsa/dsa_data_binarysearchtrees.php) and [AVL Trees](https://www.w3schools.com/dsa/dsa_data_avltrees.php) — illustrated beginner introductions.
- [GeeksforGeeks: Binary Search Tree](https://www.geeksforgeeks.org/dsa/binary-search-tree-data-structure/) and [AVL Tree](https://www.geeksforgeeks.org/dsa/introduction-to-avl-tree/) — overviews and practice problems.

## ➡️ Continue Your Learning Path

Continue to the [Heaps and Priority Queues](../heaps-and-priority-queues/README.md) module, the next module in this domain, where a weaker ordering rule — a parent is never larger than its
children — gives O(1) access to the minimum and O(log n) updates.
