# 🧭 Searching a BST (and Everything the Ordering Makes Possible)

## More Than "Is It There?"

The ordering rule from [bst-fundamentals.md](bst-fundamentals.md) — left smaller, right larger — does more than speed up equality search. Because the keys are
arranged in sorted order along every path, a BST can answer *ordered* questions in O(h) time (`h` = height), which a hash table cannot:

- Is the key present? (and return its node)
- What is the **largest key ≤ x** (the *floor*), or the **smallest key ≥ x** (the *ceiling*)?
- What comes **just after** or **just before** a key (the *successor* and *predecessor*)?
- What is the **k-th smallest** key?
- Which keys lie in a **range** `[low, high]`?
- What is the **lowest common ancestor** of two keys?

Every function below walks down a single path (or a bounded part of the tree) rather than the whole structure. All outputs were produced by running the code
on CPython 3.9, and every function was checked against the sorted-list equivalent (built on `bisect`) on thousands of random trees.

The examples use this tree, built by inserting the keys in the order shown:

```python
class BSTNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):                              # iterative insert; returns the (possibly new) root
    if root is None:
        return BSTNode(key)
    node = root
    while True:
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
                return root
            node = node.left
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key)
                return root
            node = node.right
        else:
            return root                             # duplicate: ignore

def build_bst(keys):
    root = None
    for key in keys:
        root = insert(root, key)
    return root

root = build_bst([8, 3, 10, 1, 6, 14, 4, 7, 13])
#               8
#             /   \
#            3     10
#           / \      \
#          1   6      14
#             / \    /
#            4   7  13
```

## 🔎 Search

```python
def search(root, key):                              # returns the node holding `key`, or None; O(h)
    node = root
    while node is not None:
        if key < node.key:
            node = node.left                        # the key can only be in the left subtree
        elif key > node.key:
            node = node.right                       # ...or only in the right subtree
        else:
            return node
    return None

def search_recursive(node, key):                    # the same idea, written the recursive way
    if node is None or node.key == key:
        return node
    return search_recursive(node.left if key < node.key else node.right, key)

print(search(root, 6).key, search(root, 5))                          # 6 None
print(search_recursive(root, 13).key, search_recursive(root, 99))    # 13 None
```

Each comparison discards an entire subtree. The cost is the length of the path taken, so **O(h)**: about `log₂ n` in a balanced tree, and `n` in a degenerate one.

## ⬇️ Floor and Ceiling

The **floor** of `x` is the largest key that is `≤ x`; the **ceiling** is the smallest key that is `≥ x`. Search for `x` as usual, but remember the best candidate seen so
far: whenever you move *right*, the node you left behind is a smaller-or-equal candidate (for floor); whenever you move *left*, it is a larger-or-equal candidate (for ceiling).

```python
def floor_key(root, x):                             # largest key <= x, or None
    best, node = None, root
    while node is not None:
        if node.key == x:
            return x
        if node.key < x:
            best = node.key                         # a candidate; there might be a closer one on the right
            node = node.right
        else:
            node = node.left                        # too big: look left
    return best

def ceiling_key(root, x):                           # smallest key >= x, or None
    best, node = None, root
    while node is not None:
        if node.key == x:
            return x
        if node.key > x:
            best = node.key
            node = node.left
        else:
            node = node.right
    return best

print(floor_key(root, 5), floor_key(root, 8), floor_key(root, 0))        # 4 8 None
print(ceiling_key(root, 5), ceiling_key(root, 11), ceiling_key(root, 15))    # 6 13 None
```

These answer "what is the nearest key at or below / above this value?" — the building block for scheduling ("the next free slot at or after 3 pm") and for finding the
closest value to a target (compare the floor and the ceiling).

## ↔️ Successor and Predecessor

The **successor** of a key is the next larger key in sorted order; the **predecessor** is the next smaller. They are the floor and ceiling of "just above" and "just below" the key:

```python
def successor(root, key):                           # smallest key strictly greater than `key`, or None
    best, node = None, root
    while node is not None:
        if node.key > key:
            best = node.key
            node = node.left
        else:
            node = node.right
    return best

def predecessor(root, key):                         # largest key strictly smaller than `key`, or None
    best, node = None, root
    while node is not None:
        if node.key < key:
            best = node.key
            node = node.right
        else:
            node = node.left
    return best

print(successor(root, 8), successor(root, 7), successor(root, 14))          # 10 8 None
print(predecessor(root, 8), predecessor(root, 10), predecessor(root, 1))    # 7 8 None
```

Why does `successor(root, 7)` return 8? The key `7` is a leaf with no right subtree, so the next larger key is the nearest ancestor of which `7` lies in the *left* subtree —
that is `8`. The loop finds it automatically by remembering each node it turns left at. (The same successor is needed to delete a node with two children, in
[insertion-and-deletion.md](insertion-and-deletion.md).)

## 🔢 The k-th Smallest Key

Because an in-order traversal produces keys in ascending order, the k-th smallest is the k-th key visited. An iterative in-order walk can **stop early**, doing only
O(h + k) work rather than visiting every node:

```python
def kth_smallest(root, k):                          # 1-based; raises IndexError if k is out of range
    stack, node = [], root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.key                         # stop as soon as we reach the k-th key
        node = node.right
    raise IndexError("k is larger than the number of keys")

print([kth_smallest(root, k) for k in range(1, 10)])    # [1, 3, 4, 6, 7, 8, 10, 13, 14]
```

If you need many such queries, store in each node the **size of its subtree**; then the k-th smallest is found in O(h) by comparing `k` with the left subtree's size at each step
(an "order-statistic tree"). That requires keeping the sizes up to date on every insertion and deletion.

## 📏 Range Queries

*Return all keys between `low` and `high`.* A full traversal is O(n). The ordering lets you **prune**: if the current key is less than `low`, nothing in its left subtree can qualify; if
it is greater than `high`, nothing in its right subtree can.

```python
def keys_in_range(root, low, high):
    result = []

    def walk(node):
        if node is None:
            return
        if low < node.key:
            walk(node.left)                         # the left subtree may contain keys >= low
        if low <= node.key <= high:
            result.append(node.key)
        if node.key < high:
            walk(node.right)                        # the right subtree may contain keys <= high

    walk(root)
    return result                                   # already in ascending order

print(keys_in_range(root, 4, 10))                   # [4, 6, 7, 8, 10]
print(keys_in_range(root, 11, 12))                  # []
```

The cost is **O(h + m)**, where `m` is the number of keys returned: the walk follows two paths down to the boundaries, plus the matching nodes between them. The saving is easy
to see by counting visited nodes on a large tree:

```python
import random

random.seed(5)
big = build_bst(random.sample(range(1_000_000), 100_000))        # 100,000 random keys

def count_visits(root, low, high):
    visits = 0

    def walk(node):
        nonlocal visits
        if node is None:
            return
        visits += 1
        if low < node.key:
            walk(node.left)
        if node.key < high:
            walk(node.right)

    walk(root)
    return visits

found = len(keys_in_range(big, 500_000, 500_050))
print(f"keys in the range: {found}; nodes visited: {count_visits(big, 500_000, 500_050):,} of 100,000")
```

```text
keys in the range: 8; nodes visited: 29 of 100,000
```

Answering a narrow range query on a tree of 100,000 keys touches only a few dozen nodes, instead of all 100,000 — a hash table has no equivalent.

## 🌳 Lowest Common Ancestor in a BST

In a general binary tree, finding the lowest common ancestor of two nodes requires searching both subtrees ([tree-problems.md](../trees/tree-problems.md)). The BST ordering turns it into a
single descent: the LCA is the first node on the way down whose key lies **between** the two targets (or equals one of them), because that is where their paths split.

```python
def lca_bst(root, p, q):
    low, high = min(p, q), max(p, q)
    node = root
    while node is not None:
        if node.key > high:
            node = node.left                        # both targets are in the left subtree
        elif node.key < low:
            node = node.right                       # both are in the right subtree
        else:
            return node.key                         # the paths split here (or this is one of the targets)
    return None

print(lca_bst(root, 1, 7), lca_bst(root, 4, 7), lca_bst(root, 13, 14), lca_bst(root, 3, 3))    # 3 6 14 3
```

O(h) time and O(1) space — better than the O(n) of the general-tree version.

## ✅ Verification

Every function above was compared with the equivalent operation on a sorted list, using `bisect`, over thousands of random trees:

```python
import bisect

random.seed(6)
for _ in range(5000):
    keys = random.sample(range(60), random.randint(1, 25))
    tree = build_bst(keys)
    ordered = sorted(keys)
    for x in range(-2, 62, 3):
        i = bisect.bisect_right(ordered, x)
        assert floor_key(tree, x) == (ordered[i - 1] if i else None)
        j = bisect.bisect_left(ordered, x)
        assert ceiling_key(tree, x) == (ordered[j] if j < len(ordered) else None)
        assert successor(tree, x) == (ordered[i] if i < len(ordered) else None)
        assert predecessor(tree, x) == (ordered[j - 1] if j else None)
        assert (search(tree, x) is not None) == (x in ordered) == (search_recursive(tree, x) is not None)
    for k in range(1, len(ordered) + 1):
        assert kth_smallest(tree, k) == ordered[k - 1]
    low, high = sorted(random.sample(range(-2, 62), 2))
    assert keys_in_range(tree, low, high) == [v for v in ordered if low <= v <= high]
    p, q = random.choice(ordered), random.choice(ordered)
    # check the LCA against the two root-to-node paths: it is the last node they share
    def path(target):
        node, out = tree, []
        while node.key != target:
            out.append(node.key)
            node = node.left if target < node.key else node.right
        return out + [target]
    common = [a for a, b in zip(path(p), path(q)) if a == b][-1]
    assert lca_bst(tree, p, q) == common
try:
    kth_smallest(build_bst([1, 2, 3]), 4)
    raise AssertionError("expected IndexError")
except IndexError:
    pass
print("search, floor, ceiling, successor, predecessor, k-th smallest, range, and LCA agree with bisect and root-path checks")
```

```text
search, floor, ceiling, successor, predecessor, k-th smallest, range, and LCA agree with bisect and root-path checks
```

## ⏱️ Costs

| Operation | Time | Space |
|-----------|------|-------|
| Search / floor / ceiling / successor / predecessor | O(h) | O(1) iterative |
| k-th smallest (plain BST) | O(h + k) | O(h) |
| k-th smallest (with subtree sizes) | O(h) | O(1) extra per node |
| Range query returning `m` keys | O(h + m) | O(h) |
| Lowest common ancestor | O(h) | O(1) |

With a balanced tree `h` is O(log n); in a degenerate tree it is O(n), which is why [balanced-bsts.md](balanced-bsts.md) matters.

## Common Mistakes

- **Searching both subtrees** — the ordering means only one side can contain the key.
- **Returning the first greater key you meet as the successor**, rather than remembering each node where you turned left and continuing to the closest one.
- **Forgetting the empty case** (`None` root, `k` out of range, no floor or ceiling).
- **Treating successor as "go right once"** — if the node has no right subtree, the successor is an ancestor.
- **Not pruning in a range query**, accidentally turning O(h + m) into O(n).
- **Using the general-tree LCA** on a BST and missing the O(h) shortcut.

## ➡️ Next

Continue to [insertion-and-deletion.md](insertion-and-deletion.md) to see how the tree changes: inserting is easy, but deleting a node with two children needs the
successor you just learned to find.
