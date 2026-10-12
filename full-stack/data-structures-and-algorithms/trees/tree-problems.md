# 🧩 Common Tree Problems

## One Way of Thinking, Many Problems

Almost every tree problem is solved by the same recursive thought process from [recursive-problem-solving.md](../recursion/recursive-problem-solving.md):

1. **Define what the function returns for a subtree**, in one sentence.
2. **Base case:** the empty tree (`None`), and often a leaf.
3. **Trust** the function on the left and right subtrees.
4. **Combine** their answers with the current node.

The only real design choice is *what to return*: sometimes a number (depth), sometimes a boolean (symmetric?), sometimes a node (lowest common ancestor), and
sometimes two things at once (a height *and* a running best). This file solves ten classic problems with that recipe. Every function was checked against a
brute-force or independent version on thousands of random trees (the verification block is at the end). All outputs were produced by running the code on
CPython 3.9. Heights and depths here count **nodes** on a path (a single node has depth 1), as most interview problems do.

The helpers build a tree from a level-order list (`None` marks a missing child, as in [binary-trees.md](binary-trees.md)):

```python
from collections import deque

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
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

tree = build_tree([3, 9, 20, None, None, 15, 7])
#        3
#       / \
#      9   20
#         /  \
#        15   7
print(tree.value, tree.left.value, tree.right.left.value)       # 3 9 15
```

## 1️⃣ Maximum Depth

*How many nodes lie on the longest path from the root down to a leaf?* The deepest path goes through the root and then through whichever subtree is deeper:

```python
def max_depth(node):
    if node is None:
        return 0                                   # the empty tree has depth 0
    return 1 + max(max_depth(node.left), max_depth(node.right))

print(max_depth(tree))                             # 3
print(max_depth(None), max_depth(TreeNode(1)))     # 0 1
```

**O(n) time, O(h) space.** This is the `height` function from [binary-trees.md](binary-trees.md) in the nodes convention.

## 2️⃣ Minimum Depth (a Classic Trap)

*How many nodes lie on the **shortest** path from the root to a **leaf**?* The tempting copy of the previous function — replace `max` with `min` — is wrong,
because a node with only one child is not a leaf: a missing child (`None`) is not a valid place for the path to end.

```python
def min_depth(node):
    if node is None:
        return 0
    if node.left is None:                          # only a right subtree: the path must continue there
        return 1 + min_depth(node.right)
    if node.right is None:                         # only a left subtree
        return 1 + min_depth(node.left)
    return 1 + min(min_depth(node.left), min_depth(node.right))

print(min_depth(tree))                             # 2     — the path 3 → 9
chain = build_tree([1, None, 2, None, 3])
print(min_depth(chain))                            # 3     — a naive min() would wrongly give 1
```

For the chain `1 → 2 → 3` the only leaf is `3`, so the answer is 3. The naive `1 + min(min_depth(None), min_depth(right))` would pick the empty left side (0) and
return 1. A level-order search also works and can stop at the first leaf it meets.

## 3️⃣ Same Tree and Symmetric Tree

*Are two trees identical — same shape and same values?* Compare the roots, then both pairs of subtrees. Both empty means equal; exactly one empty means different:

```python
def is_same_tree(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.value == b.value and is_same_tree(a.left, b.left) and is_same_tree(a.right, b.right)

print(is_same_tree(build_tree([1, 2, 3]), build_tree([1, 2, 3])))      # True
print(is_same_tree(build_tree([1, 2]), build_tree([1, None, 2])))      # False   — same values, different shape
```

*Is a tree a mirror image of itself?* Compare the tree with itself, crossing over: the left subtree's left must match the right subtree's right, and the left's right
must match the right's left:

```python
def is_symmetric(root):
    def mirror_equal(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return a.value == b.value and mirror_equal(a.left, b.right) and mirror_equal(a.right, b.left)
    return root is None or mirror_equal(root.left, root.right)

print(is_symmetric(build_tree([1, 2, 2, 3, 4, 4, 3])))      # True
print(is_symmetric(build_tree([1, 2, 2, None, 3, None, 3])))   # False
```

Both are O(n) time, visiting each pair of nodes once.

## 4️⃣ Path Sum and All Root-to-Leaf Paths

*Is there a root-to-leaf path whose values add up to a target?* Subtract each node's value from the target as you descend; at a leaf the remaining target must be zero.
Remember a path must end at a **leaf**:

```python
def has_path_sum(node, target):
    if node is None:
        return False
    if node.left is None and node.right is None:
        return node.value == target                # a leaf: does the remaining target equal its value?
    remaining = target - node.value
    return has_path_sum(node.left, remaining) or has_path_sum(node.right, remaining)

sums_tree = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
print(has_path_sum(sums_tree, 22))                 # True    — 5 → 4 → 11 → 2
print(has_path_sum(sums_tree, 5))                  # False   — 5 alone is not a leaf
```

Listing **every** root-to-leaf path is the same traversal while carrying the path so far. It is a first taste of
backtracking: add the node, recurse, then remove it again:

```python
def all_paths(root):
    paths, current = [], []

    def walk(node):
        if node is None:
            return
        current.append(node.value)                 # choose
        if node.left is None and node.right is None:
            paths.append(current[:])               # a leaf: record a COPY of the path so far
        else:
            walk(node.left)                        # explore
            walk(node.right)
        current.pop()                              # undo (backtrack)

    walk(root)
    return paths

print(all_paths(build_tree([1, 2, 3, None, 5])))   # [[1, 2, 5], [1, 3]]
```

Both run in O(n) time. Recording copies of paths costs O(n) per leaf in the worst case, so `all_paths` is O(n · h) overall.

## 5️⃣ Diameter of a Tree

*The diameter is the number of edges on the longest path between **any two nodes** (it need not pass through the root).* The longest path that has a node as its
highest point goes down its left subtree and down its right subtree: its length is `left_height + right_height`. So during **one** post-order pass, compute each node's
height and update a running best — the function returns one thing (height) while recording another (the best diameter):

```python
def diameter(root):
    best = 0

    def height(node):                              # height in nodes: 0 for the empty tree
        nonlocal best
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)             # the longest path through this node
        return 1 + max(left, right)

    height(root)
    return best

print(diameter(build_tree([1, 2, 3, 4, 5])))       # 3     — the path 4 → 2 → 1 → 3 (or 5 → 2 → 1 → 3)
print(diameter(build_tree([1, 2])))                # 1
```

The obvious method — computing the height afresh at every node — is O(n²) on a skewed tree. Combining the two jobs in one pass is **O(n)** and a pattern you will
use repeatedly.

## 6️⃣ Lowest Common Ancestor

*Given two nodes, find the lowest (deepest) node that has both as descendants (a node counts as its own descendant).* The recursion returns, for each subtree,
"the first target node I found in here, or the answer if I found both". At a node: if it is one of the targets, return it; otherwise ask both subtrees. If *each*
side found one target, the current node is the split point — the answer. If only one side found something, pass that result up.

```python
def lowest_common_ancestor(node, p, q):
    if node is None or node.value == p or node.value == q:
        return node
    left = lowest_common_ancestor(node.left, p, q)
    right = lowest_common_ancestor(node.right, p, q)
    if left is not None and right is not None:
        return node                                # p was found on one side and q on the other
    return left if left is not None else right

lca_tree = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(lowest_common_ancestor(lca_tree, 5, 1).value)      # 3
print(lowest_common_ancestor(lca_tree, 5, 4).value)      # 5     — a node is its own ancestor
print(lowest_common_ancestor(lca_tree, 6, 4).value)      # 5
```

O(n) time. This version assumes both values exist and are distinct. (In a **binary search tree** the ordering lets you find the LCA without visiting every node — see
[search-in-bst.md](../binary-search-trees/search-in-bst.md).)

## 7️⃣ Serialize and Deserialize

*Turn a tree into a string and back, losslessly.* A preorder traversal that also records the **empty children** with a marker (`#`) is enough, because the markers make
the structure unambiguous: when you read the string back, each `#` tells you a branch ended.

```python
def serialize(root):
    parts = []

    def walk(node):
        if node is None:
            parts.append("#")                      # an explicit marker for a missing child
            return
        parts.append(str(node.value))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(parts)

def deserialize(text):
    tokens = iter(text.split(","))

    def build():
        token = next(tokens)
        if token == "#":
            return None
        node = TreeNode(int(token))
        node.left = build()                        # the same order as serialize: node, left, right
        node.right = build()
        return node

    return build()

text = serialize(build_tree([1, 2, 3, None, None, 4, 5]))
print(text)                                        # 1,2,#,#,3,4,#,#,5,#,#
print(serialize(deserialize(text)) == text)        # True
```

Without the `#` markers, `1,2,3` could describe many different trees. This is the principle behind storing trees in files and sending them over a network, and it
needs O(n) time and space.

## 8️⃣ Rebuild a Tree From Its Traversals

*Given a tree's preorder and inorder sequences (all values distinct), reconstruct it.* The first preorder value is the root. Finding that value in the inorder
sequence splits it into the left subtree (everything before) and the right subtree (everything after); the remaining preorder values are then consumed left subtree
first. A dictionary from value to inorder position makes each split O(1):

```python
def build_from_traversals(preorder, inorder):
    position = {value: i for i, value in enumerate(inorder)}     # a hash map: O(1) lookups (see the Hashing module)
    next_value = iter(preorder)

    def build(low, high):                          # build the subtree whose inorder values are inorder[low..high]
        if low > high:
            return None
        value = next(next_value)                   # the next preorder value is this subtree's root
        node = TreeNode(value)
        middle = position[value]
        node.left = build(low, middle - 1)         # left first: preorder lists the whole left subtree before the right
        node.right = build(middle + 1, high)
        return node

    return build(0, len(inorder) - 1)

rebuilt = build_from_traversals([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
print(serialize(rebuilt))                          # 3,9,#,#,20,15,#,#,7,#,#
print(serialize(rebuilt) == serialize(tree))       # True    — it is the tree from the start of this file
```

O(n) time and space using the dictionary (see [hash-tables.md](../hashing/hash-tables.md)); scanning for the root each time would make it O(n²). Preorder + inorder
determine a tree uniquely, and so do postorder + inorder. **Preorder + postorder do not**, because they cannot tell a lone left child from a lone right child:

```python
left_only = TreeNode(1, TreeNode(2))
right_only = TreeNode(1, None, TreeNode(2))
print(list(map(str, [serialize(left_only), serialize(right_only)])))      # ['1,2,#,#,#', '1,#,2,#,#']

def preorder(node):
    return [] if node is None else [node.value] + preorder(node.left) + preorder(node.right)

def postorder(node):
    return [] if node is None else postorder(node.left) + postorder(node.right) + [node.value]

print(preorder(left_only), postorder(left_only))       # [1, 2] [2, 1]
print(preorder(right_only), postorder(right_only))     # [1, 2] [2, 1]
```

Two different trees, identical preorder and postorder. (Their inorder sequences differ — `[2, 1]` versus `[1, 2]` — which is why inorder is the missing ingredient.)

## ✅ Verification Against Independent Methods

Each function was tested on thousands of random trees against a different method: a level-order search for the depths, an explicit enumeration of root-to-leaf paths for the sums,
a shortest-path search over the tree seen as an undirected graph for the diameter, and root-to-node paths for the lowest common ancestor.

```python
import random

random.seed(12)

def random_binary_tree(n):
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

def all_nodes(root):
    return [] if root is None else [root] + all_nodes(root.left) + all_nodes(root.right)

def is_leaf(node):
    return node.left is None and node.right is None

def levels(root):                                   # independent: level-order by level
    out, current = [], [root] if root else []
    while current:
        out.append(current)
        current = [c for n in current for c in (n.left, n.right) if c]
    return out

def root_to_leaf_values(root):
    if root is None:
        return []
    if is_leaf(root):
        return [[root.value]]
    return [[root.value] + rest for child in (root.left, root.right) for rest in root_to_leaf_values(child)]

def graph_diameter(root):                           # the longest shortest-path between any two nodes, as an undirected graph
    adjacency = {n.value: [] for n in all_nodes(root)}
    for n in all_nodes(root):
        for child in (n.left, n.right):
            if child:
                adjacency[n.value].append(child.value)
                adjacency[child.value].append(n.value)
    best = 0
    for start in adjacency:
        seen, frontier, distance = {start}, [start], 0
        while frontier:
            frontier = [m for v in frontier for m in adjacency[v] if m not in seen and not seen.add(m)]
            if frontier:
                distance += 1
        best = max(best, distance)
    return best

def paths_from_root(root, target):
    if root is None:
        return None
    if root.value == target:
        return [root.value]
    for child in (root.left, root.right):
        rest = paths_from_root(child, target)
        if rest is not None:
            return [root.value] + rest
    return None

def preorder_list(node):
    return [] if node is None else [node.value] + preorder_list(node.left) + preorder_list(node.right)

def inorder_list(node):
    return [] if node is None else inorder_list(node.left) + [node.value] + inorder_list(node.right)

for _ in range(4000):
    t = random_binary_tree(random.randint(0, 25))
    nodes = all_nodes(t)

    assert max_depth(t) == len(levels(t))
    leaf_levels = [i + 1 for i, level in enumerate(levels(t)) if any(is_leaf(n) for n in level)]
    assert min_depth(t) == (leaf_levels[0] if leaf_levels else 0)

    assert is_same_tree(t, deserialize(serialize(t)))                       # round trip
    assert is_same_tree(t, build_from_traversals(preorder_list(t), inorder_list(t)))

    sums = [sum(path) for path in root_to_leaf_values(t)]
    assert sorted(len(p) for p in all_paths(t)) == sorted(len(p) for p in root_to_leaf_values(t))
    assert all_paths(t) == root_to_leaf_values(t)
    for target in set(sums) | {-1, 10**6}:
        assert has_path_sum(t, target) == (target in sums)

    if t is not None:
        assert diameter(t) == graph_diameter(t)
        p, q = random.choice(nodes).value, random.choice(nodes).value
        path_p, path_q = paths_from_root(t, p), paths_from_root(t, q)
        common = [a for a, b in zip(path_p, path_q) if a == b][-1]           # the last shared node on the two root paths
        assert lowest_common_ancestor(t, p, q).value == common

for _ in range(1500):                                                        # symmetric trees: build one by mirroring
    half = random_binary_tree(random.randint(0, 10))
    def mirror_copy(node):
        return None if node is None else TreeNode(node.value, mirror_copy(node.right), mirror_copy(node.left))
    sym = TreeNode(0, half, mirror_copy(half)) if half is not None else TreeNode(0)
    assert is_symmetric(sym)
    if half is not None:
        sym.left.value = 99                                                  # break the symmetry
        assert not is_symmetric(sym)
print("all ten tree functions agree with their independent checks on thousands of random trees")
```

```text
all ten tree functions agree with their independent checks on thousands of random trees
```

## 🧭 Choosing the Approach

| The problem asks… | Return value to design | Pattern |
|-------------------|------------------------|---------|
| Depth, height, count, sum | A number from each subtree | Postorder: combine the children's numbers |
| Is it the same / symmetric / balanced / valid? | A boolean (sometimes plus a number) | Compare two subtrees at once, or return a sentinel for "invalid" |
| Paths from the root | The path so far, passed *down* | Preorder with backtracking |
| A property spanning two subtrees (diameter, maximum path) | Height up, answer in a variable | One pass, return one thing, record another |
| A target node's relationship (ancestor, depth) | The node or `None` | Search both sides; combine |
| Store or transmit a tree | A string with explicit `None` markers | Preorder |
| Reconstruct a tree | Traversal sequences plus a lookup table | Recursion over index ranges |

## ⏱️ Costs

| Problem | Time | Extra space |
|---------|------|-------------|
| Maximum / minimum depth | O(n) | O(h) |
| Same tree / symmetric tree | O(n) | O(h) |
| Path sum | O(n) | O(h) |
| All root-to-leaf paths | O(n · h) | O(h) plus the output |
| Diameter | O(n) | O(h) |
| Lowest common ancestor | O(n) | O(h) |
| Serialize / deserialize | O(n) | O(n) |
| Rebuild from preorder and inorder | O(n) | O(n) |

Here `h` is the height: O(log n) for a balanced tree and O(n) for a skewed one, where recursion can also hit Python's recursion limit.

## Common Mistakes

- **Treating a node with one child as a leaf**, as in the naive minimum-depth function. A leaf has *no* children.
- **Recomputing the height at every node**, turning an O(n) diameter or balance check into O(n²).
- **Forgetting that a path must end at a leaf** in path-sum problems.
- **Appending the working list instead of a copy** when recording paths.
- **Forgetting the empty-tree case** (`None`) in every function.
- **Serializing without markers for missing children**, which makes the string ambiguous.
- **Assuming preorder + postorder identify a tree** — they do not; inorder is needed.
- **Assuming the values are unique** in LCA or reconstruction code without saying so.

## Module Summary

The Trees module introduced hierarchical data. [Tree Fundamentals](tree-fundamentals.md) defined the vocabulary (root, leaf, depth, height), built a general tree, showed
that a tree of `n` nodes has `n − 1` edges, and introduced the parent-array representation. [Binary Trees](binary-trees.md) restricted nodes to two children, defined full,
complete, perfect, and balanced shapes, counted their properties, and stored complete trees in arrays. [Tree Traversal](tree-traversal.md) visited every node in
preorder, inorder, postorder, and level order — recursively and with explicit stacks and queues — and compared DFS and BFS memory use. This file applied the recursive
recipe to ten classic problems.

Carry these ideas forward:

- A tree is a root plus smaller trees; define the answer for a subtree, handle `None`, trust the recursion, and combine.
- Shape controls cost: operations take time proportional to the height, which ranges from log n to n.
- DFS uses a stack and O(height) memory; BFS uses a queue and O(width) memory; know the traversal that fits the problem.
- Returning one value while recording another in a variable lets one pass answer questions that look like they need two.
- Binary search trees (next) add an ordering rule that makes searching fast; heaps, tries, and the graph algorithms later in this domain reuse everything here.

## ➡️ Next

Continue to the [Binary Search Trees](../binary-search-trees/README.md) module, the next module in this domain, where an ordering rule on the values turns a binary tree
into a structure that can search, insert, and delete in O(log n) — when it stays balanced.
