# ➕➖ Insertion and Deletion in a BST

## Changing the Tree Without Breaking the Rule

Searching leaves a BST unchanged. Inserting and deleting change it, and after every change the ordering rule must still hold for every node. Insertion is
easy: a new key always goes into an empty slot at the bottom. **Deletion is the interesting operation**, because removing a node from the middle of the tree
leaves a hole, and the hole must be filled without disturbing the order. This file writes both operations recursively, walks through the three deletion cases,
tests them against Python's `set` over tens of thousands of random operations, and explains the cost. All outputs were produced by running the code on CPython 3.9.

## 🧱 The Starting Point

```python
class BSTNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def inorder_keys(node):
    return [] if node is None else inorder_keys(node.left) + [node.key] + inorder_keys(node.right)

def shape(node):                                    # a nested tuple (key, left, right) that shows the exact structure
    return None if node is None else (node.key, shape(node.left), shape(node.right))
```

`shape` makes the tree structure visible in plain text so that before-and-after pictures can be compared exactly.

## ➕ Insertion

The recursive form says it most clearly: *to insert a key into a subtree, insert it into the correct child subtree, and put the result back as that child.* The base case
is an empty slot, where the new node is created. The function returns the **root of the updated subtree**, which lets a parent reattach it:

```python
def insert(node, key):
    if node is None:
        return BSTNode(key)                         # found the empty slot: create the node here
    if key < node.key:
        node.left = insert(node.left, key)          # insert into the left subtree and reattach
    elif key > node.key:
        node.right = insert(node.right, key)
    return node                                     # equal key: nothing to do (duplicates are ignored)

root = None
for key in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    root = insert(root, key)
print(inorder_keys(root))                           # [1, 3, 4, 6, 7, 8, 10, 13, 14]
print(shape(root))
# (8, (3, (1, None, None), (6, (4, None, None), (7, None, None))), (10, None, (14, (13, None, None), None)))
```

Insertion always creates a **leaf**: no existing node moves, so the rest of the tree is untouched and the rule is preserved. The cost is the length of the path from
the root, **O(h)**. (The recursion is `h` deep, so a very lopsided tree could exceed Python's recursion limit — the iterative insertion in
[bst-fundamentals.md](bst-fundamentals.md) does not have that problem.)

## ➖ Deletion: Three Cases

Deleting key `k`: first *find* the node (the same descent as search). Then, depending on how many children it has:

### Case 1: A Leaf

Just remove it: its parent's pointer becomes `None`. Nothing else is affected.

```
   Delete 4:      6              6
                 / \     →        \
                4   7              7
```

### Case 2: One Child

Replace the node with its only child: the parent now points directly at the grandchild. The grandchild's whole subtree comes along, and the ordering still holds
because everything in it was already on the correct side of the removed node's parent.

```
   Delete 10 (only a right child, 14):
        8                  8
         \                  \
          10       →         14
            \               /
             14           13
            /
          13
```

### Case 3: Two Children

You cannot simply remove the node, since both subtrees need a parent. The standard trick is to replace the node's **key** with a key that preserves the order, and then
delete *that* key's original node instead. The right key to use is the node's **in-order successor** — the smallest key in its right subtree (equivalently, the
**predecessor**, the largest key in its left subtree). The successor is larger than everything in the left subtree and smaller than everything else in the right subtree, so it
fits exactly where the deleted key was. And because it is the *leftmost* node of the right subtree, it has **no left child**, so removing it falls into Case 1 or Case 2.

```
   Delete 3 (children 1 and 6):  the successor is the smallest key in 3's right subtree, which is 4.

        8                         8
       / \                       / \
      3   10                    4   10
     / \     \       →         / \     \
    1   6    14               1   6    14
       / \                          \
      4   7                          7
```

Copy `4` into the node that held `3`, then delete the original `4` from the right subtree.

```python
def minimum_node(node):
    while node.left is not None:
        node = node.left
    return node

def delete(node, key):
    if node is None:
        return None                                 # the key is not in the tree: nothing to delete
    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:                                           # found the node to delete
        if node.left is None:
            return node.right                       # cases 1 and 2: no left child -> promote the right child (or None)
        if node.right is None:
            return node.left                        # case 2: no right child -> promote the left child
        successor = minimum_node(node.right)        # case 3: two children
        node.key = successor.key                    # replace the key with its successor...
        node.right = delete(node.right, successor.key)    # ...then remove the successor's original node
    return node

tree = None
for key in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    tree = insert(tree, key)

tree = delete(tree, 4)                              # a leaf
print(inorder_keys(tree))                           # [1, 3, 6, 7, 8, 10, 13, 14]
tree = delete(tree, 10)                             # one child (14)
print(shape(tree)[2])                               # (14, (13, None, None), None)
tree = delete(tree, 3)                              # two children (1 and 6): the successor 6 takes its place
print(shape(tree)[1])                               # (6, (1, None, None), (7, None, None))
tree = delete(tree, 99)                             # a key that is not present: no change
print(inorder_keys(tree))                           # [1, 6, 7, 8, 13, 14]
```

The function returns the subtree root after the deletion, so that when the deleted node *was* the root of the subtree, the parent receives the replacement (`node.right`,
`node.left`, or the same node with its key replaced). Note the structure of the three cases in the code: the two single-child branches also handle the leaf, because a
leaf has `left is None`, and promoting its (empty) right child produces `None`.

The cost is the descent to the node (O(h)) plus, for Case 3, the walk to the successor and its deletion (also at most `h`): **O(h) overall**.

## ✅ Testing Against a `set`

A BST should behave like a set of keys that can also be read in order. The test below performs 40,000 random insertions and deletions and, after every operation, checks that:
(1) the in-order sequence equals the sorted contents of a real `set`, (2) the tree is still a valid BST, and (3) the node count matches.

```python
import random

random.seed(7)

def is_valid_bst(node, low=None, high=None):
    if node is None:
        return True
    if (low is not None and node.key <= low) or (high is not None and node.key >= high):
        return False
    return is_valid_bst(node.left, low, node.key) and is_valid_bst(node.right, node.key, high)

def count(node):
    return 0 if node is None else 1 + count(node.left) + count(node.right)

root, model = None, set()
cases = {"leaf": 0, "one child": 0, "two children": 0}
for step in range(40000):
    key = random.randint(0, 60)
    if random.random() < 0.55:
        root = insert(root, key)
        model.add(key)
    else:
        node = root                                  # classify the deletion, for the statistics below
        while node is not None and node.key != key:
            node = node.left if key < node.key else node.right
        if node is not None:
            kids = (node.left is not None) + (node.right is not None)
            cases[["leaf", "one child", "two children"][kids]] += 1
        root = delete(root, key)
        model.discard(key)
    assert inorder_keys(root) == sorted(model)
    assert is_valid_bst(root) and count(root) == len(model)
print("40,000 random operations agree with set; the BST rule held after every one")
print(cases)
```

```text
40,000 random operations agree with set; the BST rule held after every one
{'leaf': 3580, 'one child': 3133, 'two children': 3169}
```

All three deletion cases were exercised many times (the dictionary shows how often), and the tree remained a valid BST after every single operation — which is exactly what the
rule-checking `is_valid_bst` from [bst-fundamentals.md](bst-fundamentals.md) is for.

## ⚠️ Deletion Can Unbalance the Tree

Nothing in these algorithms keeps the tree balanced: ordered input still produces a chain, and deletions can leave a tree lopsided. This is the problem the final file addresses:
[balanced-bsts.md](balanced-bsts.md) adds rotations that restore balance after every change, so that *every* operation stays O(log n).

## 🧠 Variations Worth Knowing

- **Predecessor instead of successor.** Replacing with the largest key of the left subtree is symmetric and equally correct.
- **Lazy deletion.** Mark the node as deleted instead of removing it; searches skip deleted nodes. Deletion is O(h) with no restructuring, at the cost of wasted space until
  the tree is rebuilt.
- **Duplicates.** If equal keys are allowed, a count in each node (decrement on delete, remove at zero) is the simplest approach.
- **Deleting a whole subtree** is trivial (set the pointer to `None`); deleting by *rank* or by *range* needs the order-statistic and range techniques from
  [search-in-bst.md](search-in-bst.md).

## ⏱️ Costs

| Operation | Balanced tree | Worst case (degenerate) |
|-----------|---------------|-------------------------|
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Space for `n` keys | O(n) | O(n) |
| Recursion depth | O(log n) | O(n) — risks `RecursionError` in Python |

## Common Mistakes

- **Forgetting to reattach the returned subtree** (`node.left = delete(node.left, key)`), so the deletion has no effect.
- **Deleting a two-child node by simply removing it**, orphaning a subtree. Replace its key with the successor (or predecessor) first.
- **Choosing the wrong replacement**: any key from the right subtree *other than the minimum* would break the rule for the remaining right-subtree keys.
- **Forgetting to delete the successor's original node** after copying its key, leaving a duplicate.
- **Not handling an absent key**, or an empty tree, in `delete`.
- **Inserting duplicates inconsistently** so that a search can look on the wrong side.

## ➡️ Next

Continue to [balanced-bsts.md](balanced-bsts.md) to see how rotations keep a BST's height logarithmic no matter what order keys arrive in — the AVL tree, built and tested here.
