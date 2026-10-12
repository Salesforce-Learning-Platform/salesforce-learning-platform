# ⚖️ Balanced BSTs

## Keeping the Height Logarithmic, Whatever the Input

Everything a [binary search tree](bst-fundamentals.md) does — search, insert, delete, floor, range — costs time proportional to its **height**. In a balanced tree
that is about log₂ n; in a degenerate one it is n. The unbalanced BST has no protection against sorted or partly sorted input, which is common in practice (timestamps,
sequential IDs, alphabetized lists). A **self-balancing BST** repairs its own shape after every insertion and deletion so that the height *always* stays O(log n).

This file builds the oldest and simplest self-balancing tree, the **AVL tree** (named for its inventors, Adelson-Velsky and Landis), from the ground up: the
balance rule, the **rotation** that fixes it, the four cases, and full insertion and deletion. It then measures the payoff and surveys the other balanced trees. All outputs were
produced by running the code on CPython 3.9, and the AVL tree was tested against a Python `set` with its invariants checked after every operation.

## 📐 The AVL Rule

An AVL tree is a BST with one extra rule:

> For **every** node, the heights of its left and right subtrees differ by **at most 1**.

The difference (left height minus right height) is the node's **balance factor**, and it must always be −1, 0, or +1. It is a surprisingly strong guarantee: the
smallest AVL tree of height `h` has about 1.618ʰ nodes (a Fibonacci-like growth), so an AVL tree with `n` nodes can be no taller than about `1.44 · log₂ n`
([Wikipedia: AVL tree](https://en.wikipedia.org/wiki/AVL_tree) gives the exact bound). Each node stores its own height so the balance factor can be read in O(1):

```python
class AVLNode:
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1                              # height counted in nodes: a leaf has height 1

def height(node):
    return node.height if node else 0

def update(node):
    node.height = 1 + max(height(node.left), height(node.right))

def balance_factor(node):                            # positive: left-heavy; negative: right-heavy
    return height(node.left) - height(node.right)
```

## 🔄 Rotations: The Repair Operation

A **rotation** is a local rearrangement of three nodes that changes the shape **without breaking the BST ordering**. A right rotation lifts a left child above its parent; a left
rotation lifts a right child. The picture shows a right rotation around `y` (subtrees `A`, `B`, `C` hang below and keep their order):

```
        y                          x
       / \       rotate right     / \
      x   C      ─────────▶      A   y
     / \                            / \
    A   B                          B   C
```

The ordering is preserved because `A < x < B < y < C` before and after. Subtree `B` — which was between `x` and `y` — moves from `x`'s right to `y`'s left, and that is the only
subtree that changes parent. A rotation changes **three pointers** and is O(1).

```python
def rotate_right(y):
    x = y.left
    y.left = x.right                                 # B moves from x's right to y's left
    x.right = y                                      # y becomes x's right child
    update(y)                                        # y is lower now: update its height first
    update(x)
    return x                                         # x is the new root of this subtree

def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    update(x)
    update(y)
    return y
```

## 🧩 The Four Imbalance Cases

After inserting or deleting, a node on the path back to the root may have a balance factor of +2 or −2. There are exactly four shapes, and each has a fix:

| Case | Where the extra height is | Fix |
|------|---------------------------|-----|
| **Left-Left** | The left child's *left* subtree | One right rotation at the node |
| **Right-Right** | The right child's *right* subtree | One left rotation at the node |
| **Left-Right** | The left child's *right* subtree | Left-rotate the left child, then right-rotate the node |
| **Right-Left** | The right child's *left* subtree | Right-rotate the right child, then left-rotate the node |

The "zig-zag" cases (Left-Right, Right-Left) need two rotations because a single rotation would just move the problem to the other side. In code, one `rebalance` function covers all
four:

```python
def rebalance(node):
    update(node)
    balance = balance_factor(node)
    if balance > 1:                                  # left-heavy
        if balance_factor(node.left) < 0:            # Left-Right: first turn it into Left-Left
            node.left = rotate_left(node.left)
        return rotate_right(node)
    if balance < -1:                                 # right-heavy
        if balance_factor(node.right) > 0:           # Right-Left: first turn it into Right-Right
            node.right = rotate_right(node.right)
        return rotate_left(node)
    return node                                      # already balanced
```

## ➕ AVL Insertion

Insert exactly as in an ordinary BST, then **rebalance every node on the path back up** to the root. The recursive structure does this naturally: each call, after inserting below
itself, rebalances itself on the way out.

```python
def avl_insert(node, key):
    if node is None:
        return AVLNode(key)
    if key < node.key:
        node.left = avl_insert(node.left, key)
    elif key > node.key:
        node.right = avl_insert(node.right, key)
    else:
        return node                                  # duplicate: ignore
    return rebalance(node)                           # fix this node on the way back up

def shape(node):                                     # nested tuples (key, left, right) to see the structure
    return None if node is None else (node.key, shape(node.left), shape(node.right))

for name, keys in [("Left-Left (3, 2, 1)", [3, 2, 1]), ("Right-Right (1, 2, 3)", [1, 2, 3]),
                   ("Left-Right (3, 1, 2)", [3, 1, 2]), ("Right-Left (1, 3, 2)", [1, 3, 2])]:
    root = None
    for key in keys:
        root = avl_insert(root, key)
    print(f"{name:24} -> {shape(root)}")
```

```text
Left-Left (3, 2, 1)      -> (2, (1, None, None), (3, None, None))
Right-Right (1, 2, 3)    -> (2, (1, None, None), (3, None, None))
Left-Right (3, 1, 2)     -> (2, (1, None, None), (3, None, None))
Right-Left (1, 3, 2)     -> (2, (1, None, None), (3, None, None))
```

In all four cases, three keys that would have formed a lopsided chain end up as a perfectly balanced triangle with `2` at the root. An ordinary BST fed `1, 2, 3` would
have produced the chain from [bst-fundamentals.md](bst-fundamentals.md).

At most **one** rotation (single or double) is needed per insertion to restore the rule for the whole tree, and the rebalancing work along the path is O(h) = O(log n), so
insertion is **O(log n)** in the worst case.

## ➖ AVL Deletion

Delete exactly as in an ordinary BST (see [insertion-and-deletion.md](insertion-and-deletion.md): leaf, one child, or two children via the successor), then rebalance every node on
the path back up. Deletion may need a rotation at several levels, but each is O(1) and there are at most O(log n) levels:

```python
def avl_delete(node, key):
    if node is None:
        return None
    if key < node.key:
        node.left = avl_delete(node.left, key)
    elif key > node.key:
        node.right = avl_delete(node.right, key)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        successor = node.right                       # two children: replace with the in-order successor
        while successor.left is not None:
            successor = successor.left
        node.key = successor.key
        node.right = avl_delete(node.right, successor.key)
    return rebalance(node)                           # fix this node on the way back up
```

## ✅ Verification: A Set Model and the AVL Invariants

A balanced tree has two kinds of correctness: it must behave like a set, and it must **remain balanced**. The test performs 60,000 random insertions and deletions and, after
every one, checks: the in-order keys equal the sorted contents of a real `set`; the BST ordering holds; every stored height is correct; every balance factor is −1, 0, or +1;
and the height respects the theoretical AVL bound.

```python
import math
import random

random.seed(11)

def check_avl(node, low=None, high=None):
    """Return the true height of the subtree, asserting every AVL and BST invariant on the way."""
    if node is None:
        return 0
    assert (low is None or node.key > low) and (high is None or node.key < high)       # BST order
    left = check_avl(node.left, low, node.key)
    right = check_avl(node.right, node.key, high)
    assert abs(left - right) <= 1                                                       # AVL balance rule
    assert node.height == 1 + max(left, right)                                          # stored height is right
    return 1 + max(left, right)

def inorder_keys(node):
    return [] if node is None else inorder_keys(node.left) + [node.key] + inorder_keys(node.right)

root, model, rotations_checked = None, set(), 0
for step in range(60000):
    key = random.randint(0, 200)
    if random.random() < 0.55:
        root = avl_insert(root, key)
        model.add(key)
    else:
        root = avl_delete(root, key)
        model.discard(key)
    h = check_avl(root)
    assert inorder_keys(root) == sorted(model)
    assert h <= 1.4405 * math.log2(len(model) + 2) or h <= 2          # the AVL height bound (in nodes)

for n in range(1, 400):                                                # sorted insertions: the worst case for a plain BST
    root = None
    for key in range(n):
        root = avl_insert(root, key)
    assert check_avl(root) <= 1.4405 * math.log2(n + 2) + 1
print("60,000 random operations agree with set; every AVL invariant held after every operation")
print("sorted insertions of 1..399 keys all produced valid, balanced AVL trees")
```

```text
60,000 random operations agree with set; every AVL invariant held after every operation
sorted insertions of 1..399 keys all produced valid, balanced AVL trees
```

## 📊 The Payoff: Sorted Input

Insert the keys `0, 1, 2, …, n−1` in sorted order — the worst case for a plain BST — into both trees and compare height and build time:

```python
import time

def plain_insert(root, key):                          # an ordinary (unbalanced) BST insert, iterative
    new = AVLNode(key)
    if root is None:
        return new
    node = root
    while True:
        if key < node.key:
            if node.left is None:
                node.left = new
                return root
            node = node.left
        else:
            if node.right is None:
                node.right = new
                return root
            node = node.right

def edge_height(root):                                # height in edges, computed level by level (works for deep trees)
    height_, level = -1, [root] if root else []
    while level:
        height_ += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return height_

print(f"{'n':>6} | {'plain BST height':>16} | {'AVL height':>10} | {'plain BST build':>15} | {'AVL build':>10}")
for n in (500, 1_000, 2_000, 4_000):
    start = time.perf_counter()
    plain = None
    for key in range(n):
        plain = plain_insert(plain, key)
    plain_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    avl = None
    for key in range(n):
        avl = avl_insert(avl, key)
    avl_time = (time.perf_counter() - start) * 1000
    print(f"{n:>6,} | {edge_height(plain):>16,} | {edge_height(avl):>10} | {plain_time:>12.1f} ms | {avl_time:>7.1f} ms")
```

Output:

```
     n | plain BST height | AVL height | plain BST build |  AVL build
   500 |              499 |          8 |          5.7 ms |     2.4 ms
 1,000 |              999 |          9 |         22.3 ms |     5.8 ms
 2,000 |            1,999 |         10 |         86.6 ms |    12.3 ms
 4,000 |            3,999 |         11 |        343.5 ms |    27.4 ms
```

The plain BST's height is `n − 1` and its build time grows **quadratically** (each insertion walks the whole chain), while the AVL tree's height stays near log₂ n and its build time grows
almost linearly. At 4,000 sorted keys the AVL tree is both far shorter and far faster to build, even though each insertion does extra work for rebalancing. (The AVL build is also
recursive, which is safe because its depth is only O(log n); the plain tree's depth would break a recursive version.)

## 🌲 Other Balanced Trees

| Tree | Idea | Where it is used |
|------|------|------------------|
| **AVL tree** | Strict balance: subtree heights differ by at most 1 | Lookup-heavy workloads; teaching |
| **Red-black tree** | Nodes coloured red or black with rules that keep the longest path at most twice the shortest; fewer rotations per update than AVL | Language libraries and kernels (for example, C++ `std::map` and Java's `TreeMap` are commonly implemented with red-black trees) |
| **B-tree / B+ tree** | Many keys per node and many children; a very shallow, wide tree built for disk and block access | Database indexes and file systems |
| **2-3 trees, AA trees, treaps, splay trees, skip lists** | Alternative ways of keeping operations fast on average or amortized | Teaching, specialized libraries |

Python's standard library does not include a balanced BST. The usual substitutes are a **sorted list with `bisect`** (O(log n) search, O(n) insertion — acceptable
when updates are rare), a **heap** when you only need the minimum ([heap-fundamentals.md](../heaps-and-priority-queues/heap-fundamentals.md)), or a third-party package such as
[`sortedcontainers`](https://pypi.org/project/sortedcontainers/) when you need an ordered collection with fast updates. In interviews, the expected knowledge is *why* balancing is needed,
what a rotation does, and the O(log n) guarantee — not typing out a red-black tree.

## ⚖️ Costs

| Operation | Plain BST (worst) | AVL tree |
|-----------|-------------------|----------|
| Search | O(n) | **O(log n)** |
| Insert | O(n) | **O(log n)** worst case; at most 1 rotation |
| Delete | O(n) | **O(log n)** worst case; up to O(log n) rotations |
| Space | O(n) | O(n) plus one height per node |
| In-order traversal | O(n) | O(n) |
| Height | up to n − 1 | at most about 1.44 log₂ n |

## Common Mistakes

- **Updating heights in the wrong order** during a rotation — update the node that moved *down* first, then the one that moved up.
- **Forgetting to rebalance on the way back up after deletion**, which (unlike insertion) can need fixes at several levels.
- **Using a single rotation for the zig-zag cases** (Left-Right and Right-Left), which leaves the tree unbalanced.
- **Checking only the root's balance** — the rule must hold at every node.
- **Not reattaching the rotated subtree** to the parent (`node.left = rotate_left(node.left)`).
- **Believing a balanced tree is always the right choice** — for read-mostly data, a sorted array with binary search is simpler and faster.

## Module Summary

The Binary Search Trees module added an ordering rule to the binary tree. [BST Fundamentals](bst-fundamentals.md) defined the rule, built a tree, showed that in-order traversal yields
sorted keys, explained how to validate a BST correctly, and measured how insertion order controls height. [Searching a BST](search-in-bst.md) used the ordering for search, floor and
ceiling, successor and predecessor, k-th smallest, range queries, and lowest common ancestor in O(h). [Insertion and Deletion](insertion-and-deletion.md) covered adding leaves and the
three deletion cases, verified against a `set`. This file kept the height logarithmic with AVL rotations.

Carry these ideas forward:

- A BST's operations cost O(h); the height is between log₂ n and n − 1, depending on arrival order.
- The ordering supports questions a hash table cannot: minimum, neighbours, ranges, sorted iteration.
- Deletion with two children uses the in-order successor (or predecessor).
- Self-balancing trees (AVL, red-black, B-trees) guarantee O(log n) by rotating locally after each change.
- Heaps (next) relax the ordering rule to "parent before children" in order to support a different task: fast access to the smallest or largest item.

## ➡️ Next

Continue to the [Heaps and Priority Queues](../heaps-and-priority-queues/README.md) module, the next module in this domain, where a weaker ordering rule — a parent is never larger than its
children — gives O(1) access to the minimum and O(log n) updates, the basis of priority queues.
