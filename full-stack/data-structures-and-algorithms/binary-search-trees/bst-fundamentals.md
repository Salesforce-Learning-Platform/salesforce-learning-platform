# 🔍 BST Fundamentals

## A Binary Tree With an Ordering Rule

A [binary tree](../trees/binary-trees.md) places no conditions on the values it stores, so finding one means visiting nodes until it turns up: O(n). A
**binary search tree (BST)** adds a single rule that makes searching fast:

> For **every** node, all keys in its **left** subtree are **smaller** than the node's key, and all keys in its **right** subtree are **larger**.

```
              8
            /   \
           3     10            Everything left of 8 is < 8; everything right is > 8.
          / \      \           The same rule holds at every node, e.g. below 3:
         1   6      14         1 < 3 < 6, and 4 and 7 (under 6) are 3 < 4 < 6 < 7 < 8.
            / \    /
           4   7  13
```

The rule works like a game of "higher or lower": at each node, compare the target with the node's key, and discard one whole side. If the tree is reasonably
**balanced**, each comparison removes about half of what remains, so a search takes **O(log n)** steps — the idea of binary search on a sorted array, but in a
structure that also supports fast insertion and deletion. This file builds a BST, shows that reading it in order gives sorted output, explains how to *validate*
one (a classic trap), and measures the thing that matters most: how much the **shape** of the tree depends on the order in which keys arrive. All outputs
were produced by running the code on CPython 3.9.

## 🧱 The Node and the Tree

```python
class BSTNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self, keys=()):
        self.root = None
        self._size = 0
        for key in keys:
            self.insert(key)

    def __len__(self):
        return self._size

    def insert(self, key):                          # O(h); returns False if the key is already present
        if self.root is None:
            self.root = BSTNode(key)
            self._size += 1
            return True
        node = self.root
        while True:
            if key < node.key:
                if node.left is None:
                    node.left = BSTNode(key)        # found the empty slot where the key belongs
                    break
                node = node.left
            elif key > node.key:
                if node.right is None:
                    node.right = BSTNode(key)
                    break
                node = node.right
            else:
                return False                        # duplicate: this tree stores each key once
        self._size += 1
        return True

    def __contains__(self, key):                    # O(h): follow "higher or lower" down one path
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return True
        return False

    def __iter__(self):                             # in-order traversal: yields keys in ascending order
        stack, node = [], self.root
        while node or stack:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key
            node = node.right

    def minimum(self):                              # the leftmost node
        node = self.root
        while node.left is not None:
            node = node.left
        return node.key

    def maximum(self):                              # the rightmost node
        node = self.root
        while node.right is not None:
            node = node.right
        return node.key

tree = BinarySearchTree([8, 3, 10, 1, 6, 14, 4, 7, 13])
print(list(tree))                         # [1, 3, 4, 6, 7, 8, 10, 13, 14]
print(len(tree), tree.minimum(), tree.maximum())      # 9 1 14
print(6 in tree, 5 in tree)               # True False
print(tree.insert(6), len(tree))          # False 9
```

A few things to notice:

- **Search and insertion follow a single path** from the root down, so their cost is the length of that path: **O(h)**, where `h` is the tree's height.
- **Insertion places a new key at a leaf.** The search for the key ends at an empty slot; that slot is where the key belongs. Nothing already in the tree moves.
- **The minimum is the leftmost node** and **the maximum is the rightmost** — no comparisons needed, just follow `left` (or `right`) until it runs out.
- The iterative loops avoid recursion, so even a very lopsided tree will not hit Python's recursion limit.
- **Duplicates.** A BST must decide what to do with equal keys. This one stores each key once (set behaviour). Alternatives are storing a count in the node, or always
  sending equal keys to the right; whichever you choose, state it and keep it consistent.

## 🪄 In-Order Traversal Gives Sorted Order

Visit the left subtree, then the node, then the right subtree
([inorder in tree-traversal.md](../trees/tree-traversal.md)). The BST rule guarantees that everything on the left is smaller and everything on the right is larger, so the output
is automatically in ascending order — as the first `print` above shows. This is also the idea behind **tree sort**: insert all the values into a BST, then read them
out in order. It is correct, but its speed depends entirely on the tree's shape, as the measurement later in this file shows.

## ✅ Validating a BST (The Common Trap)

*Given a binary tree, is it a valid BST?* The tempting check — compare every node only with its **immediate children** — is wrong. The rule is about *whole subtrees*,
so a node deep in the right subtree must still be larger than the root. This tree looks fine locally but is **not** a BST, because `7` sits in the left subtree of `5`:

```
        5
       / \
      3   8             3's right child is 7, and 3 < 7: correct locally.
       \                But 7 is in 5's LEFT subtree and 7 > 5: the BST rule is broken.
        7
```

```python
def naive_is_bst(node):                             # WRONG: only checks each node against its direct children
    if node is None:
        return True
    if node.left is not None and node.left.key >= node.key:
        return False
    if node.right is not None and node.right.key <= node.key:
        return False
    return naive_is_bst(node.left) and naive_is_bst(node.right)

def is_valid_bst(node, low=None, high=None):        # RIGHT: carry the allowed range down the tree
    if node is None:
        return True
    if (low is not None and node.key <= low) or (high is not None and node.key >= high):
        return False
    return is_valid_bst(node.left, low, node.key) and is_valid_bst(node.right, node.key, high)

broken = BSTNode(5)
broken.left, broken.right = BSTNode(3), BSTNode(8)
broken.left.right = BSTNode(7)

print(naive_is_bst(broken))        # True      — fooled
print(is_valid_bst(broken))        # False     — correct
print(is_valid_bst(tree.root))     # True
```

The correct version passes down the **open interval** `(low, high)` in which every key of the current subtree must lie: going left tightens `high` to the node's
key, going right tightens `low`. Every node is visited once: **O(n) time, O(h) space**. An equivalent test is that the in-order sequence is *strictly increasing*.

```python
import random

random.seed(4)

def random_binary_tree(n):                          # an arbitrary binary tree: values are NOT arranged in any order
    if n == 0:
        return None
    nodes = [BSTNode(random.randint(0, 6))]
    free = [(nodes[0], "left"), (nodes[0], "right")]
    for _ in range(n - 1):
        parent, side = free.pop(random.randrange(len(free)))
        node = BSTNode(random.randint(0, 6))
        setattr(parent, side, node)
        nodes.append(node)
        free += [(node, "left"), (node, "right")]
    return nodes[0]

def inorder_keys(node):
    return [] if node is None else inorder_keys(node.left) + [node.key] + inorder_keys(node.right)

valid_seen = 0
for _ in range(20000):
    t = random_binary_tree(random.randint(0, 9))
    keys = inorder_keys(t)
    expected = all(a < b for a, b in zip(keys, keys[1:]))        # strictly increasing in-order sequence
    assert is_valid_bst(t) == expected
    valid_seen += expected
print(f"is_valid_bst agrees with the in-order definition on 20,000 random trees ({valid_seen} of them were valid BSTs)")
```

```text
is_valid_bst agrees with the in-order definition on 20,000 random trees (5170 of them were valid BSTs)
```

## 📐 The Shape Depends on the Insertion Order

The BST rule fixes *where each key may go*, but not the tree's shape — that depends on the order of arrival. Insert `1, 2, 3, 4, 5` in order and every new key becomes the
right child of the previous one:

```
sorted input 1, 2, 3, 4, 5            a "good" order for the same keys: 3, 1, 4, 2, 5

   1                                          3
    \                                        / \
     2                                      1   4
      \                                      \   \
       3                                      2   5
        \
         4
          \
           5       height 4 = n - 1               height 2
```

A BST built from sorted data is just a linked list: height `n − 1`, with every search, insertion, and deletion taking O(n). Measuring it makes the difference concrete.
This inserts `n` keys in **random order** and in **sorted order**, and compares the heights with the best possible height for `n` nodes, `⌊log₂ n⌋`:

```python
import math

def tree_height(root):                              # height in edges, iteratively (a sorted tree is far too deep to recurse)
    if root is None:
        return -1
    height, level = -1, [root]
    while level:
        height += 1
        level = [child for node in level for child in (node.left, node.right) if child]
    return height

print(f"{'n':>8} | {'best possible':>13} | {'random order':>12} | {'sorted order':>12}")
for n in (100, 1_000, 3_000, 100_000):
    keys = list(range(n))
    shuffled = keys[:]
    random.shuffle(shuffled)
    random_height = tree_height(BinarySearchTree(shuffled).root)
    sorted_height = tree_height(BinarySearchTree(keys).root) if n <= 3_000 else "skipped"
    print(f"{n:>8,} | {math.floor(math.log2(n)):>13} | {random_height:>12} | {sorted_height:>12}")
```

Output:

```
       n | best possible | random order | sorted order
     100 |             6 |           14 |           99
   1,000 |             9 |           21 |          999
   3,000 |            11 |           26 |         2999
 100,000 |            16 |           39 |      skipped
```

(The 100,000 sorted case was skipped: it would take roughly five billion steps.) Sorted input gives a height of `n − 1`, as predicted. Random input gives a height
about two to three times the ideal — larger than the minimum, but still **logarithmic**: from 1,000 keys to 100,000 keys (100 times as many), the height grows only from
about 20 to about 40. It is a well-known result that the expected height of a BST built by inserting keys in random order is O(log n) (see
[Wikipedia: Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree)).

The lesson is the reason the final file in this module exists: **a plain BST has no defence against ordered input**, and real data is often partly sorted
(timestamps, IDs, alphabetized names). [Balanced BSTs](balanced-bsts.md) keep the height near log n regardless of arrival order.

## ⚖️ BST, Sorted Array, or Hash Table?

| Operation | BST (balanced) | BST (worst case) | Sorted array | Hash table |
|-----------|----------------|------------------|--------------|------------|
| Search | O(log n) | O(n) | O(log n) (binary search) | **O(1)** average |
| Insert | O(log n) | O(n) | O(n) (shifting) | O(1) average |
| Delete | O(log n) | O(n) | O(n) | O(1) average |
| Minimum / maximum | O(log n) | O(n) | **O(1)** | O(n) |
| Next larger / smaller key | O(log n) | O(n) | O(log n) | O(n) |
| All keys in sorted order | O(n) (in-order) | O(n) | O(n) | O(n log n) (sort first) |
| Keys in a range | O(log n + k) | O(n) | O(log n + k) | O(n) |

A BST earns its place when you need **both** fast updates **and** ordered operations — minimum, maximum, neighbours, range queries, sorted iteration — which hash tables
cannot give and sorted arrays give only with slow updates.

## Common Mistakes

- **Validating a BST by comparing only parent and child**, missing violations deeper in the tree. Carry the allowed range down.
- **Ignoring the duplicate policy**, so equal keys end up on both sides and searches become inconsistent.
- **Assuming a BST is balanced.** Its height depends on insertion order; sorted input gives a linked list.
- **Recursing on a possibly deep tree** and hitting Python's recursion limit — use loops, or balance the tree.
- **Using `<=` and `>=` inconsistently** in comparisons, so a key equal to a node can be sent in different directions.
- **Expecting a BST to be faster than a hash table for plain lookups** — its advantage is ordering, not raw lookup speed.

## ➡️ Next

Continue to [search-in-bst.md](search-in-bst.md) for the operations that exploit the ordering: search, floor and ceiling, successor and predecessor, the k-th smallest key,
and range queries.
