# 🌿 Binary Trees

## Every Node Has at Most Two Children

A **binary tree** is a tree in which each node has at most two children, called the **left child** and the **right child**. The restriction looks
small, but it makes trees easy to implement, easy to reason about, and the foundation of binary search trees, heaps, expression trees, and many
interview problems. This file defines the vocabulary of shapes, builds trees in Python, checks the shape properties in code, and shows how a complete
binary tree can live in a plain array. All outputs were produced by running the code on CPython 3.9.

```
         1
       /   \
      2     3          Every node has a left and a right slot.
     / \     \         Either may be empty (None).
    4   5     6
```

## 🧱 The Node

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left          # the left child, or None
        self.right = right        # the right child, or None

root = TreeNode(1,
                TreeNode(2, TreeNode(4), TreeNode(5)),
                TreeNode(3, None, TreeNode(6)))
print(root.value, root.left.value, root.right.value)       # 1 2 3
print(root.left.left.value, root.right.left)               # 4 None
```

Compare with the general tree's `children` list: here the two slots have *meaning* (left versus right), and an empty slot is `None`. A
`None` child is also the natural **base case** of every recursive binary-tree function: the empty tree.

## 📏 Basic Measurements

Each function follows the recursive definition "a binary tree is empty, or a root with a left tree and a right tree":

```python
def count_nodes(node):
    if node is None:
        return 0                                    # the empty tree has no nodes
    return 1 + count_nodes(node.left) + count_nodes(node.right)

def height(node):                                   # edges on the longest root-to-leaf path
    if node is None:
        return -1                                   # so that a single node has height 0
    return 1 + max(height(node.left), height(node.right))

def count_leaves(node):
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return count_leaves(node.left) + count_leaves(node.right)

print(count_nodes(root), height(root), count_leaves(root))      # 6 2 3
```

The odd-looking `height(None) == -1` makes the arithmetic work: a leaf has height `1 + max(-1, -1) = 0`. If you prefer to count nodes
(a single node has height 1), return `0` for `None`. Either convention is fine as long as you apply it consistently.

## 🔷 The Shapes

Several names describe how "filled in" a binary tree is. The differences matter because they determine the tree's height — and therefore the
cost of everything you do with it.

```
FULL                  COMPLETE              PERFECT               DEGENERATE (skewed)
(0 or 2 children)     (all levels full      (all levels full,     (a chain)
                      except maybe the      every leaf at the
                      last, filled          same depth)
                      left to right)
      1                    1                    1                      1
     / \                  / \                  / \                      \
    2   3                2   3                2   3                      2
       / \              / \  /               / \ / \                      \
      4   5            4  5 6               4  5 6  7                      3
```

| Shape | Definition | Height for `n` nodes |
|-------|------------|----------------------|
| **Full** | Every node has 0 or 2 children (never exactly 1) | Varies |
| **Complete** | Every level is full except possibly the last, which is filled **left to right** | Always ⌊log₂ n⌋ |
| **Perfect** | Every internal node has 2 children, and all leaves are at the same depth | log₂(n + 1) − 1 |
| **Balanced** | For every node, the heights of its left and right subtrees differ by at most 1 | O(log n) |
| **Degenerate / skewed** | Every node has at most one child: a linked list in disguise | n − 1 |

Each definition translates directly into code:

```python
from collections import deque

def is_full(node):
    if node is None:
        return True
    if (node.left is None) != (node.right is None):          # exactly one child: not full
        return False
    return is_full(node.left) and is_full(node.right)

def is_perfect(node):
    h = height(node)
    return count_nodes(node) == 2 ** (h + 1) - 1             # a perfect tree of height h has exactly 2^(h+1) - 1 nodes

def is_balanced(node):
    def check(n):                                            # returns the height, or -2 if some subtree is unbalanced
        if n is None:
            return -1
        left, right = check(n.left), check(n.right)
        if left == -2 or right == -2 or abs(left - right) > 1:
            return -2
        return 1 + max(left, right)
    return check(node) != -2

def is_complete(node):
    queue = deque([node])
    seen_gap = False                                         # have we met an empty slot in level order?
    while queue:
        current = queue.popleft()
        if current is None:
            seen_gap = True
        else:
            if seen_gap:
                return False                                 # a real node after a gap: not complete
            queue.append(current.left)
            queue.append(current.right)
    return True

print(is_full(root), is_complete(root), is_perfect(root), is_balanced(root))    # False False False True
perfect = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, TreeNode(6), TreeNode(7)))
print(is_full(perfect), is_complete(perfect), is_perfect(perfect), is_balanced(perfect))      # True True True True
chain = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
print(is_full(chain), is_complete(chain), is_perfect(chain), is_balanced(chain))      # False False False False
```

Several points are worth noting:

- `is_balanced` uses a classic trick: one traversal returns the height *and* signals failure with a sentinel (`-2`), so it runs in **O(n)** rather than
  recomputing heights at every node (which would be O(n²) on a skewed tree).
- `is_complete` scans in **level order** (it uses a queue — see [queue-fundamentals.md](../stacks-and-queues/queue-fundamentals.md)). In a complete tree
  the real nodes come first and the empty slots only afterwards; a real node appearing *after* an empty slot proves the tree is not complete.
- The three-node `chain` fails every test: it is the worst case, and the reason balanced trees matter.

## 🔢 Properties You Can Count On

Binary trees obey exact counting rules, which explain why a balanced tree is so efficient:

- **Level `i` holds at most `2ⁱ` nodes** (the root's level is 0).
- **A perfect tree of height `h` has exactly `2^(h+1) − 1` nodes** — the sum `1 + 2 + 4 + … + 2ʰ`.
- **Conversely, a tree with `n` nodes has height at least `⌊log₂ n⌋`.** Halving at each level means a million nodes fit in about 20 levels.
- **In a full binary tree, the number of leaves is one more than the number of internal nodes.**

These are checked below on randomly generated trees (the generator `random_binary_tree` is reused in later files):

```python
import random

random.seed(3)

def random_binary_tree(n):
    """Build a random binary tree with n nodes labelled 0..n-1 by hanging each new node on a free slot."""
    if n == 0:
        return None
    nodes = [TreeNode(0)]
    free = [(nodes[0], "left"), (nodes[0], "right")]
    for label in range(1, n):
        parent, side = free.pop(random.randrange(len(free)))
        node = TreeNode(label)
        setattr(parent, side, node)
        nodes.append(node)
        free += [(node, "left"), (node, "right")]
    return nodes[0]

def level_sizes(node):
    sizes, level = [], [node] if node else []
    while level:
        sizes.append(len(level))
        level = [child for n in level for child in (n.left, n.right) if child]
    return sizes

import math
for _ in range(3000):
    tree = random_binary_tree(random.randint(1, 60))
    n, h = count_nodes(tree), height(tree)
    assert all(size <= 2 ** i for i, size in enumerate(level_sizes(tree)))        # level i has at most 2^i nodes
    assert h >= math.floor(math.log2(n))                                           # height is at least floor(log2 n)
    assert h <= n - 1                                                              # ...and at most n - 1
    if is_full(tree):
        assert count_leaves(tree) == (n - count_leaves(tree)) + 1                  # leaves = internal nodes + 1
    if is_perfect(tree):
        assert n == 2 ** (h + 1) - 1

for h in range(0, 8):                                                              # build perfect trees explicitly
    def perfect_tree(depth):
        return None if depth < 0 else TreeNode(0, perfect_tree(depth - 1), perfect_tree(depth - 1))
    t = perfect_tree(h)
    assert is_perfect(t) and is_full(t) and is_complete(t) and is_balanced(t)
    assert count_nodes(t) == 2 ** (h + 1) - 1 and height(t) == h
print("shape and counting properties hold on 3,000 random trees and perfect trees up to height 7")
```

```text
shape and counting properties hold on 3,000 random trees and perfect trees up to height 7
```

## 🗄️ The Array Representation of a Complete Binary Tree

Because a *complete* binary tree has no gaps (every level is full, the last is filled left to right), it can be stored in a plain list **without any
pointers**. Number the nodes level by level starting at 0, and put the node numbered `i` at `array[i]`. The relationships become arithmetic:

```
                  0
               /     \
             1         2             index:    0   1   2   3   4   5
            / \       /                 value: A   B   C   D   E   F
           3   4     5
```

| Relationship | Index formula (0-based) |
|--------------|-------------------------|
| Left child of `i` | `2i + 1` |
| Right child of `i` | `2i + 2` |
| Parent of `i` | `(i − 1) // 2` |

```python
values = ["A", "B", "C", "D", "E", "F"]

def left_child(i):  return 2 * i + 1
def right_child(i): return 2 * i + 2
def parent(i):      return (i - 1) // 2

print(values[left_child(1)], values[right_child(1)], values[parent(5)])     # D E C
print([values[i] for i in range(len(values)) if left_child(i) >= len(values)])      # ['D', 'E', 'F']  — the leaves
```

This is compact (no pointers) and gives O(1) access to a node's parent — the same idea as the parent array in
[tree-fundamentals.md](tree-fundamentals.md). It is exactly how a **heap** is stored (see the [Heaps and Priority Queues](../heaps-and-priority-queues/README.md) module). It works
only for complete trees: a sparse tree stored this way would waste most of the array on gaps — a skewed tree of height `h` needs an array of
about `2ʰ` slots.

## 🏗️ Building a Tree From a List (Level Order)

Interview problems usually describe a binary tree as a list in level order, with `None` marking a missing child (this is also how many testing
platforms print trees). A queue builds it: take nodes level by level, attach the next two list items as each node's left and right child:

```python
from collections import deque

def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root

def to_level_list(root):
    if root is None:
        return []
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
        else:
            result.append(node.value)
            queue.append(node.left)
            queue.append(node.right)
    while result and result[-1] is None:           # trim trailing None markers
        result.pop()
    return result

tree = build_tree([1, 2, 3, 4, 5, None, 6])
print(to_level_list(tree))                          # [1, 2, 3, 4, 5, None, 6]
print(count_nodes(tree), height(tree))              # 6 2
print(to_level_list(build_tree([1, None, 2, None, 3])))    # [1, None, 2, None, 3]   — the skewed chain
```

## 🔁 Mirroring a Tree

*Swap the left and right children of every node.* The recursive definition is two lines — the mirror of a tree is a root with its two subtrees
swapped, each of them mirrored:

```python
def mirror(node):
    if node is None:
        return None
    node.left, node.right = mirror(node.right), mirror(node.left)
    return node

mirrored = mirror(build_tree([1, 2, 3, 4, 5, None, 6]))
print(to_level_list(mirrored))                      # [1, 3, 2, 6, None, 5, 4]
```

## 🖥️ Drawing a Tree

A sideways drawing is easy and handy for debugging: print the right subtree first (above), then the node, then the left subtree (below), indenting by
depth. Turn the page 90° clockwise to read it.

```python
def draw(node, depth=0):
    if node is None:
        return
    draw(node.right, depth + 1)
    print("    " * depth + str(node.value))
    draw(node.left, depth + 1)

draw(build_tree([1, 2, 3, 4, 5, None, 6]))
```

```text
        6
    3
1
        5
    2
        4
```

## ⚖️ Why the Shape Decides the Cost

Nearly every binary-tree algorithm costs time proportional to the **height**, so shape is everything. A balanced tree of a million nodes has a height
of about 20; a skewed tree of a million nodes has a height of 999,999 — a linked list that also overflows Python's recursion limit (about 1,000 frames)
if you traverse it recursively. This is why [binary search trees](../binary-search-trees/balanced-bsts.md) come with *balancing* schemes.

| Property | Balanced | Skewed |
|----------|----------|--------|
| Height for `n` nodes | O(log n) | O(n) |
| Recursion depth (traversal) | O(log n) | O(n): risks `RecursionError` |
| Typical operation (search, insert) | O(log n) | O(n) |

## Common Mistakes

- **Not handling `None` children**: `node.left.value` raises `AttributeError` when `left` is `None`. Check first, or let the base case return for `None`.
- **Mixing up "full", "complete", and "perfect"** — three different definitions; state which one you mean.
- **Computing balance by calling `height` at every node**, making the check O(n²) on skewed trees.
- **Using the array formulas on a tree that is not complete**, producing wrong or sparse arrays.
- **Off-by-one on the height convention** (`-1` versus `0` for the empty tree).
- **Forgetting that mutating functions such as `mirror` change the tree in place** — copy first if you need the original.

## ➡️ Next

Continue to [tree-traversal.md](tree-traversal.md) to learn how to visit every node of a binary tree systematically: the three depth-first orders and
the breadth-first (level-order) walk, each recursively and iteratively.
