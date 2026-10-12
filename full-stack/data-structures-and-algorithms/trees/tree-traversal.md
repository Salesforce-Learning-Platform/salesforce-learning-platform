# 🚶‍♂️ Tree Traversal

## Visiting Every Node, in a Chosen Order

A list has one natural order: front to back. A tree has several, because at each node you must decide *when* to visit the node relative to its
subtrees, and whether to go deep first or wide first. **Traversal** means visiting every node exactly once in a systematic order. It is the basis of
copying, printing, searching, evaluating, and measuring trees, and it comes in two families:

- **Depth-first search (DFS)** goes as deep as possible down one branch before backing up. Three variants — **preorder**, **inorder**, and
  **postorder** — differ in when the node itself is visited. DFS uses a stack (implicitly, through recursion).
- **Breadth-first search (BFS)**, also called **level-order**, visits all nodes at depth 0, then depth 1, then depth 2, and so on. BFS uses a queue.

All outputs below were produced by running the code on CPython 3.9. The examples use this tree:

```
          1
        /   \
       2     3
      / \     \
     4   5     6
```

```python
from collections import deque

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

root = TreeNode(1,
                TreeNode(2, TreeNode(4), TreeNode(5)),
                TreeNode(3, None, TreeNode(6)))
```

## 🕳️ Depth-First: Three Orders

In all three, the algorithm is the same two recursive calls (left subtree, right subtree) plus one visit to the node. Only the **position of the visit**
changes:

| Order | Sequence | Mnemonic |
|-------|----------|----------|
| **Preorder** | node, left, right | visit *pre*-(before) the subtrees |
| **Inorder** | left, node, right | visit *in* between |
| **Postorder** | left, right, node | visit *post*-(after) the subtrees |

```python
def preorder(node):
    if node is not None:
        yield node.value                    # visit first...
        yield from preorder(node.left)
        yield from preorder(node.right)

def inorder(node):
    if node is not None:
        yield from inorder(node.left)
        yield node.value                    # ...or in the middle...
        yield from inorder(node.right)

def postorder(node):
    if node is not None:
        yield from postorder(node.left)
        yield from postorder(node.right)
        yield node.value                    # ...or last

print(list(preorder(root)))     # [1, 2, 4, 5, 3, 6]
print(list(inorder(root)))      # [4, 2, 5, 1, 3, 6]
print(list(postorder(root)))    # [4, 5, 2, 6, 3, 1]
```

Trace preorder by hand: visit `1`; go left to `2`: visit `2`, go left to `4`: visit `4`, its children are empty so return; go right to `5`:
visit `5`; back at `1`, go right to `3`: visit `3`; its left is empty; go right to `6`: visit `6`. Result: `1 2 4 5 3 6`. Each node is visited
once and each `None` child costs one cheap call, so every order is **O(n) time**; the recursion depth equals the tree's height, so the space is **O(h)**.

### What Each Order Is Good For

- **Preorder** processes a node *before* its descendants: copying a tree, serializing it, and printing a directory listing (folder first, then contents).
  It yields *prefix* (Polish) notation for an expression tree.
- **Inorder** gives the left-to-right reading order. On a **binary search tree** it produces the values in **sorted order** — the reason it matters
  ([bst-fundamentals.md](../binary-search-trees/bst-fundamentals.md)). On an expression tree it yields infix notation.
- **Postorder** processes a node *after* its descendants: computing sizes and heights, deleting a tree (children before parents), and evaluating an
  expression tree. It yields *postfix* notation — the form evaluated by the stack in [stack-fundamentals.md](../stacks-and-queues/stack-fundamentals.md).

The last point is worth seeing. Here is the expression `(3 + 4) * 2` as a tree, where leaves are numbers and internal nodes are operators:

```python
expression = TreeNode("*",
                      TreeNode("+", TreeNode(3), TreeNode(4)),
                      TreeNode(2))

def evaluate(node):                                   # postorder: evaluate both children, then apply the operator
    if node.left is None and node.right is None:
        return node.value                             # a number
    left, right = evaluate(node.left), evaluate(node.right)
    return {"+": left + right, "-": left - right, "*": left * right}[node.value]

print(list(postorder(expression)))                    # [3, 4, '+', 2, '*']     — postfix
print(list(preorder(expression)))                     # ['*', '+', 3, 4, 2]     — prefix
print(list(inorder(expression)))                      # [3, '+', 4, '*', 2]     — infix (parentheses are lost)
print(evaluate(expression))                           # 14
```

The postorder output `3 4 + 2 *` is exactly the postfix expression a stack-based evaluator would consume. The inorder output has lost its
parentheses — which is why a tree, not the flat infix text, is the right representation for expressions.

## 🔁 Depth-First Without Recursion

Recursion uses the call stack; you can use an explicit [stack](../stacks-and-queues/stack-fundamentals.md) instead. This avoids Python's recursion
limit on very deep trees (see [recursion-fundamentals.md](../recursion/recursion-fundamentals.md)).

**Preorder** is the easiest. Pop a node, visit it, and push its children — **right first**, so that the left child is popped (and processed) first:

```python
def preorder_iterative(root):
    result = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        result.append(node.value)
        if node.right:
            stack.append(node.right)                # pushed first, so it is processed last
        if node.left:
            stack.append(node.left)
    return result
```

**Inorder** is trickier, because a node is visited only *after* its whole left subtree. Walk left as far as possible, remembering the path on the stack;
then pop, visit, and move to the right subtree:

```python
def inorder_iterative(root):
    result = []
    stack = []
    node = root
    while node or stack:
        while node:                                 # descend left, remembering the path
            stack.append(node)
            node = node.left
        node = stack.pop()                          # the leftmost unvisited node
        result.append(node.value)                   # visit it
        node = node.right                           # then handle its right subtree
    return result
```

**Postorder** has a neat trick: a preorder that visits *node, right, left* produces the **reverse** of postorder (*left, right, node*):

```python
def postorder_iterative(root):
    result = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        result.append(node.value)                   # node, then right, then left, in this order
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return result[::-1]                             # reverse: left, right, node

print(preorder_iterative(root))      # [1, 2, 4, 5, 3, 6]
print(inorder_iterative(root))       # [4, 2, 5, 1, 3, 6]
print(postorder_iterative(root))     # [4, 5, 2, 6, 3, 1]
```

All three give the same results as the recursive versions, in O(n) time, with the stack holding at most one root-to-node path plus pending siblings: O(h)
space.

## 🌊 Breadth-First: Level Order

Level-order traversal visits nodes by distance from the root. A [queue](../stacks-and-queues/queue-fundamentals.md) enforces this: dequeue a node, visit it,
and enqueue its children at the back — so all of a level is processed before any of the next:

```python
def level_order(root):
    result = []
    queue = deque([root] if root else [])
    while queue:
        node = queue.popleft()
        result.append(node.value)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result

print(level_order(root))             # [1, 2, 3, 4, 5, 6]
```

Often the problem wants nodes **grouped by level** (`[[1], [2, 3], [4, 5, 6]]`). The simplest way is to process one whole level per loop iteration:

```python
def level_order_by_level(root):
    levels = []
    current = [root] if root else []
    while current:
        levels.append([node.value for node in current])
        current = [child for node in current for child in (node.left, node.right) if child]
    return levels

print(level_order_by_level(root))    # [[1], [2, 3], [4, 5, 6]]
```

Variations come from reshaping this loop: reverse the list for each odd level to get a **zigzag** traversal, or keep only the last node of each level for the
**right-side view** of the tree:

```python
def zigzag(root):
    return [level if i % 2 == 0 else level[::-1] for i, level in enumerate(level_order_by_level(root))]

def right_side_view(root):
    return [level[-1] for level in level_order_by_level(root)]

print(zigzag(root))                  # [[1], [3, 2], [4, 5, 6]]
print(right_side_view(root))         # [1, 3, 6]
```

BFS is O(n) time. Its extra space is the **widest level** of the tree, O(w).

## 🧮 DFS Memory or BFS Memory? It Depends on the Shape

DFS needs space proportional to the tree's **height**; BFS needs space proportional to its **width**. For a bushy, balanced tree the height is small and the
width is huge; for a long chain it is the other way around. This experiment records the peak size of the DFS stack and the BFS queue on perfect trees (as bushy as
possible) and on chains (as thin as possible) of the same number of nodes:

```python
def perfect_tree(height):
    return None if height < 0 else TreeNode(0, perfect_tree(height - 1), perfect_tree(height - 1))

def chain(n):
    node = None
    for _ in range(n):
        node = TreeNode(0, None, node)
    return node

def peak_dfs_stack(root):
    peak, stack = 0, [root]
    while stack:
        peak = max(peak, len(stack))
        node = stack.pop()
        for child in (node.right, node.left):
            if child:
                stack.append(child)
    return peak

def peak_bfs_queue(root):
    peak, queue = 0, deque([root])
    while queue:
        peak = max(peak, len(queue))
        node = queue.popleft()
        for child in (node.left, node.right):
            if child:
                queue.append(child)
    return peak

print(f"{'shape':>16} | {'nodes':>7} | {'DFS peak stack':>14} | {'BFS peak queue':>14}")
for h in (4, 8, 12, 16):
    t = perfect_tree(h)
    n = 2 ** (h + 1) - 1
    print(f"{'perfect, h=' + str(h):>16} | {n:>7,} | {peak_dfs_stack(t):>14,} | {peak_bfs_queue(t):>14,}")
for n in (31, 511, 8191):
    t = chain(n)
    print(f"{'chain':>16} | {n:>7,} | {peak_dfs_stack(t):>14,} | {peak_bfs_queue(t):>14,}")
```

```text
           shape |   nodes | DFS peak stack | BFS peak queue
    perfect, h=4 |      31 |              5 |             16
    perfect, h=8 |     511 |              9 |            256
   perfect, h=12 |   8,191 |             13 |          4,096
   perfect, h=16 | 131,071 |             17 |         65,536
           chain |      31 |              1 |              1
           chain |     511 |              1 |              1
           chain |   8,191 |              1 |              1
```

On the perfect trees the DFS stack stays tiny (about `h + 1`), while the BFS queue ends up holding an entire level, about half of all the nodes. On the chain,
both stay at a single entry. So neither is "more memory-efficient" in general: **choose by the shape you expect and by what you need**. (A third technique,
Morris traversal, does DFS in O(1) extra space by temporarily rewiring the tree, at the cost of complexity; see
[Wikipedia: Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal).)

## ✅ Verification

The iterative and recursive versions must agree on every tree, and level order must be consistent with node depths. The check uses random trees, including
skewed ones:

```python
import random

random.seed(8)

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

def depths(node, depth=0, out=None):
    out = {} if out is None else out
    if node:
        out[node.value] = depth
        depths(node.left, depth + 1, out)
        depths(node.right, depth + 1, out)
    return out

for _ in range(5000):
    tree = random_binary_tree(random.randint(0, 40))
    assert preorder_iterative(tree) == list(preorder(tree))
    assert inorder_iterative(tree) == list(inorder(tree))
    assert postorder_iterative(tree) == list(postorder(tree))
    d = depths(tree)
    order = level_order(tree)
    assert [d[v] for v in order] == sorted(d[v] for v in order)                 # depths never decrease in level order
    assert sorted(order) == sorted(d) == sorted(list(preorder(tree)))           # every node visited exactly once
    assert [v for level in level_order_by_level(tree) for v in level] == order
    # a chain of left children would exceed recursion limits; the iterative versions must still work
deep = None
for label in range(5000):
    deep = TreeNode(label, deep)
assert len(inorder_iterative(deep)) == 5000 and len(level_order(deep)) == 5000
try:
    list(inorder(deep))
    raise AssertionError("expected RecursionError")
except RecursionError:
    pass
print("iterative = recursive on 5,000 random trees; level order respects depth; a 5,000-deep tree needs the iterative version")
```

```text
iterative = recursive on 5,000 random trees; level order respects depth; a 5,000-deep tree needs the iterative version
```

The last test is the practical reason to know the iterative versions: the recursive `inorder` fails with `RecursionError` on a 5,000-node skewed tree,
while the explicit stack handles it.

## 🧭 Choosing a Traversal

| You need… | Use |
|-----------|-----|
| Copy or serialize a tree; print a hierarchy parent-first | Preorder |
| Sorted order from a binary search tree | Inorder |
| Compute a result from the children first (size, height, sums); delete a tree; evaluate an expression | Postorder |
| Shortest path in an unweighted tree; process level by level; the nearest matching node | Level order (BFS) |
| A very deep tree | An iterative version with an explicit stack |

## ⚖️ Costs

| Traversal | Time | Extra space |
|-----------|------|-------------|
| Preorder / inorder / postorder (recursive or iterative) | O(n) | O(h) |
| Level order (BFS) | O(n) | O(w), the widest level |
| Level order grouped by level | O(n) | O(w) for the current level plus the output |

## Common Mistakes

- **Mixing up the three orders**: remember where the node sits relative to *left* and *right* — before, between, or after.
- **Pushing children in the wrong order** in iterative preorder (push right first so left is popped first).
- **Forgetting the `None` base case**, producing an `AttributeError` or infinite recursion.
- **Marking a node visited too late or too early** in iterative inorder: it is visited when popped, not when pushed.
- **Using a list with `pop(0)` as the BFS queue**, making BFS quadratic (use `deque`; see [queue-fundamentals.md](../stacks-and-queues/queue-fundamentals.md)).
- **Assuming BFS or DFS is always cheaper in memory** — it depends on whether the tree is wide or tall.
- **Recursing on a skewed tree** with thousands of nodes and hitting the recursion limit.

## ➡️ Next

Continue to [tree-problems.md](tree-problems.md) to apply traversal and the recursive way of thinking to the classic tree problems: depth, symmetry,
path sums, diameter, lowest common ancestor, and tree serialization.
