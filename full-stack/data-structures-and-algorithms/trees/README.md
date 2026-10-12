# 🌳 Trees

## 📚 Overview

Every structure so far has arranged items in a line. A **tree** arranges them in a **hierarchy**: one root, and every other node hanging below exactly one parent.
Trees describe file systems, web pages, organization charts, parsed code, and decision processes, and they are the foundation of binary search trees, heaps, tries,
and the graph algorithms that follow in this domain. This module teaches the vocabulary, the binary tree and its shapes, the four ways of visiting every node
(preorder, inorder, postorder, and level order), and the recursive way of thinking that solves most tree problems.

Every code example was run on CPython 3.9. Data structures and algorithms were checked against independent references — property counts on thousands of random trees,
iterative traversals against recursive ones, depths against level-order searches, diameters against graph searches, and lowest common ancestors against root paths —
and the memory comparison between depth-first and breadth-first search is a real measurement.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Use tree vocabulary precisely: root, leaf, parent, child, sibling, subtree, depth, height, level — and explain why a tree with `n` nodes has `n − 1` edges.
- Implement general and binary trees, and compute size, height, leaf count, and paths with short recursive functions.
- Distinguish full, complete, perfect, balanced, and degenerate binary trees; state how each affects height; and store a complete tree in an array.
- Implement preorder, inorder, postorder, and level-order traversal both recursively and iteratively, and choose the right one for a task.
- Compare depth-first and breadth-first space use by tree shape, and explain why deep trees need iterative traversal in Python.
- Solve classic tree problems — depth, symmetry, path sums, diameter, lowest common ancestor, serialization, and reconstruction from traversals — with the
  "define, base case, trust, combine" recipe.

## 📋 Prerequisites

- [Recursion](../recursion/README.md) — tree algorithms are recursion made visible; the call tree is itself a tree.
- [Stacks and Queues](../stacks-and-queues/README.md) — depth-first traversal uses a stack, breadth-first uses a queue.
- [Linked Lists](../linked-lists/README.md) — a tree node is a linked-list node with more than one `next`.
- [Hashing](../hashing/README.md) — used to rebuild a tree from traversals in O(n).
- [Time and Space Complexity](../time-and-space-complexity/README.md) — costs are stated in terms of `n`, the height `h`, and the width `w`.
- Basic Python reading ability — the examples use Python classes, generators, and recursion.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [tree-fundamentals.md](tree-fundamentals.md) | Vocabulary, a general tree, recursive measurements, properties verified on random trees, and the parent-array representation |
| [binary-trees.md](binary-trees.md) | The binary node, full/complete/perfect/balanced shapes with code to test them, counting properties, array storage, and building from a level-order list |
| [tree-traversal.md](tree-traversal.md) | Preorder, inorder, postorder, and level order — recursive and iterative; expression trees; DFS-versus-BFS memory measured |
| [tree-problems.md](tree-problems.md) | Ten classic problems with brute-force verification; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [tree-traversal.md](tree-traversal.md) and [tree-problems.md](tree-problems.md) if you are preparing for coding interviews: traversal orders, minimum depth, diameter,
and lowest common ancestor are among the most frequently asked questions, and explaining *why* the diameter needs one pass (return a height, record a best) is a common
follow-up.

**Skim** [tree-fundamentals.md](tree-fundamentals.md) if you already know the vocabulary — but read the sections on height conventions and the shape of trees,
which explain why the same algorithm can cost O(log n) on one tree and O(n) on another. Read [binary-trees.md](binary-trees.md) closely before the next module: the array
representation and the shape definitions return in binary search trees and heaps.

## 🧠 Knowledge Check

<details>
<summary>Why does <code>min_depth</code> need special handling for a node with only one child, when <code>max_depth</code> does not?</summary>

Minimum depth measures the shortest path from the root to a **leaf** — a node with no children. A node with a single child is not a leaf, so the path must continue into
that child; the empty (`None`) side is not a place where a path can end. If you naively take `min` of both subtree depths, the empty side contributes 0 and wrongly ends the
path at a node that still has a child. For maximum depth, an empty side contributes 0 to a `max`, which can never beat a real subtree, so no special case is needed. See
[tree-problems.md](tree-problems.md).

</details>

<details>
<summary>Preorder and postorder traversals of two different binary trees can be identical, but preorder and inorder cannot. Why?</summary>

Preorder says which node is the root of each subtree, and inorder says which nodes lie to its left and which to its right — together they pin down every split. Preorder and
postorder both only tell you *which values belong to a subtree*, not whether a lone child is a left child or a right child. For example, a root `1` with only a left child `2`, and
a root `1` with only a right child `2`, both have preorder `[1, 2]` and postorder `[2, 1]`, while their inorder sequences differ (`[2, 1]` and `[1, 2]`). See the demonstration in
[tree-problems.md](tree-problems.md).

</details>

## 📚 References

- [Wikipedia: Tree (data structure)](https://en.wikipedia.org/wiki/Tree_(data_structure)), [Binary tree](https://en.wikipedia.org/wiki/Binary_tree), and [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal) — definitions, variants, and traversal orders (including Morris traversal).
- [Wikipedia: Lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) — the problem and its applications.
- [W3Schools: DSA Trees](https://www.w3schools.com/dsa/dsa_theory_trees.php), [Binary Trees](https://www.w3schools.com/dsa/dsa_data_binarytrees.php), and [Pre-order Traversal](https://www.w3schools.com/dsa/dsa_algo_binarytrees_preorder.php) — illustrated beginner introductions.
- [GeeksforGeeks: Tree Data Structure](https://www.geeksforgeeks.org/dsa/introduction-to-tree-data-structure-and-algorithm-tutorials/), [Binary Tree](https://www.geeksforgeeks.org/dsa/binary-tree-data-structure/), and [Tree Traversals](https://www.geeksforgeeks.org/dsa/tree-traversals-inorder-preorder-and-postorder/) — overviews and practice problems.
- [Python docs: `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) — the queue used for level-order traversal.

## ➡️ Continue Your Learning Path

Continue to the Binary Search Trees module, the next module in this domain, where an ordering rule on the values turns a binary tree into a structure that can search,
insert, and delete in O(log n) — when it stays balanced.
