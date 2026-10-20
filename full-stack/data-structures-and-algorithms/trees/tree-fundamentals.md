# 🌳 Tree Fundamentals

## Data With a Hierarchy

Arrays, linked lists, stacks, and queues all arrange items in a **line**: every item has at most one item before it and one after. Much
real data is not a line but a **hierarchy**: a folder contains files and more folders; a company has a CEO, managers, and employees; an HTML page
is an element containing elements. A **tree** is the data structure for exactly that: a set of **nodes** connected so that there is one
starting node, and every other node hangs below exactly one parent.

```
                CEO                       ← root
              /      \
           CTO        CFO                 ← CEO's children (siblings of each other)
          /    \         \
   Dev Lead     QA Lead   Accountant      ← leaves have no children
    /     \
 Dev 1   Dev 2
```

Trees are everywhere in computing: file systems, the DOM of a web page, programming-language syntax trees, database indexes, decision
trees, and the recursion trees you drew in [recursion-tree.md](../recursion/recursion-tree.md). This file introduces the vocabulary, builds a
general tree in Python, computes its basic measurements, and shows an alternative representation. All outputs were produced by running the code on
CPython 3.9.

## 📖 The Vocabulary

| Term | Meaning | In the diagram above |
|------|---------|----------------------|
| **Node** | One element of the tree, holding a value | Every box |
| **Edge** | A link between a parent and a child | Every line |
| **Root** | The single top node, with no parent | CEO |
| **Parent / child** | A node directly above / below another | CEO is the parent of CTO; CTO is a child of CEO |
| **Siblings** | Nodes with the same parent | CTO and CFO |
| **Leaf** | A node with no children | Dev 1, Dev 2, QA Lead, Accountant |
| **Internal node** | A node with at least one child | CEO, CTO, CFO, Dev Lead |
| **Ancestor / descendant** | Anywhere above / below along a path | CEO is an ancestor of Dev 1 |
| **Subtree** | A node together with all its descendants | The CTO's subtree has 5 nodes |
| **Depth of a node** | Number of edges from the root to the node | Dev 1 has depth 3 |
| **Level** | All nodes at the same depth (the root is level 0) | Level 1 = CTO, CFO |
| **Height of a node** | Number of edges on the longest path down to a leaf | CTO has height 2 |
| **Height of the tree** | The height of the root | 3 |
| **Degree** | The number of children a node has | CEO has degree 2 |

Careful with **height**: some books count *edges* (a single node has height 0), others count *nodes* (a single node has height 1). This module
counts **edges**, and always says so when it matters. A tree is also defined recursively: *a tree is a root together with zero or more
subtrees* — which is why almost every tree algorithm is naturally recursive.

### What Makes It a Tree

A tree is a **connected** structure with **no cycles**: from the root there is exactly one path to every node. A direct consequence is this:

> A tree with `n` nodes has exactly `n − 1` edges.

Every node except the root has exactly one parent edge, so there are `n − 1` edges. If a structure had more edges, it would have a cycle and
would no longer be a tree (it would be a [graph](../graphs/graph-fundamentals.md)). The claim is verified on random trees below.

## 🧱 A General Tree in Python

A node holds a value and a list of its children. A tree *is* its root node — everything below is reachable from it:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []                     # any number of children, in order

    def add_child(self, value):
        child = Node(value)
        self.children.append(child)
        return child                           # return it so the caller can keep building downward

ceo = Node("CEO")
cto = ceo.add_child("CTO")
cfo = ceo.add_child("CFO")
lead = cto.add_child("Dev Lead")
cto.add_child("QA Lead")
lead.add_child("Dev 1")
lead.add_child("Dev 2")
cfo.add_child("Accountant")

print(ceo.value, [child.value for child in ceo.children])      # CEO ['CTO', 'CFO']
```

## 📏 Measuring a Tree

Because a tree is a root plus smaller trees, each measurement is a short recursive function whose base case is a leaf. They use the
recursion habits from [recursive-problem-solving.md](../recursion/recursive-problem-solving.md): define what the function returns, trust it on the
children, and combine.

```python
def size(node):                                # number of nodes in the subtree rooted at `node`
    return 1 + sum(size(child) for child in node.children)

def height(node):                              # edges on the longest downward path
    if not node.children:
        return 0                               # base case: a leaf
    return 1 + max(height(child) for child in node.children)

def count_leaves(node):
    if not node.children:
        return 1
    return sum(count_leaves(child) for child in node.children)

def depth_of(node, target, depth=0):           # edges from `node` down to the node holding `target`; -1 if absent
    if node.value == target:
        return depth
    for child in node.children:
        found = depth_of(child, target, depth + 1)
        if found != -1:
            return found
    return -1

def path_to(node, target):                     # the values from `node` down to `target`, or None
    if node.value == target:
        return [node.value]
    for child in node.children:
        path = path_to(child, target)
        if path is not None:
            return [node.value] + path
    return None

print(size(ceo), height(ceo), count_leaves(ceo))      # 8 3 4
print(depth_of(ceo, "Dev 1"), depth_of(ceo, "CFO"), depth_of(ceo, "Nobody"))     # 3 1 -1
print(path_to(ceo, "Dev 2"))                          # ['CEO', 'CTO', 'Dev Lead', 'Dev 2']
print(size(cto), height(cto))                         # 5 2
```

Each function visits every node once, so each is **O(n) time**; the recursion depth equals the tree's height, so the space is **O(h)**.
`path_to` shows the pattern for search in an *unordered* tree: ask each child in turn, and stop at the first that finds the target. Without any
ordering (compare [binary search trees](../binary-search-trees/bst-fundamentals.md), where values are arranged to allow faster search), finding a value
means visiting nodes until it turns up: O(n) in the worst case.

### Printing a Tree

Indenting by depth reproduces the shape — the same technique as the call traces in
[recursion-fundamentals.md](../recursion/recursion-fundamentals.md), and the way a file explorer lists folders:

```python
def print_tree(node, depth=0):
    print("    " * depth + node.value)
    for child in node.children:
        print_tree(child, depth + 1)

print_tree(ceo)
```

```text
CEO
    CTO
        Dev Lead
            Dev 1
            Dev 2
        QA Lead
    CFO
        Accountant
```

## 🔬 Checking the Properties on Random Trees

Rather than take `edges = n − 1` on trust, build thousands of random trees and measure. This generator attaches each new node to a randomly chosen
existing node, which always produces a valid tree:

```python
import random

random.seed(2)

def random_tree(n):
    nodes = [Node(0)]
    for label in range(1, n):
        parent = random.choice(nodes)
        nodes.append(parent.add_child(label))
    return nodes[0], nodes

def count_edges(node):
    return sum(1 + count_edges(child) for child in node.children)

for _ in range(3000):
    n = random.randint(1, 40)
    root, nodes = random_tree(n)
    assert size(root) == n
    assert count_edges(root) == n - 1                       # edges = nodes - 1
    assert 0 <= height(root) <= n - 1                       # a chain is the tallest possible tree
    assert 1 <= count_leaves(root) <= max(1, n - 1) or n == 1
    # every node's depth equals the length of its path from the root, minus one
    for node in nodes:
        assert len(path_to(root, node.value)) - 1 == depth_of(root, node.value)
print("3,000 random trees: edges = nodes - 1, depth = path length - 1, height <= nodes - 1")
```

```text
3,000 random trees: edges = nodes - 1, depth = path length - 1, height <= nodes - 1
```

The extreme shapes are worth remembering. A **chain** (every node has one child) has height `n − 1` — it is really a linked list. A **star** (one root
with `n − 1` leaf children) has height 1. Algorithms whose cost depends on the height behave very differently on the two, which is why the *shape* of
a tree matters as much as its size.

## 🗂️ A Different Representation: The Parent Array

A tree does not have to be stored as linked objects. When the nodes are numbered `0 … n−1`, you can store just **each node's parent**:

```python
#            index:   0   1   2   3   4   5
parents = [-1, 0, 0, 1, 1, 2]        # node 0 is the root (parent -1); nodes 1 and 2 are its children; 3 and 4 hang under 1; 5 under 2
```

```
        0
       / \
      1   2
     / \   \
    3   4   5
```

From this one list you can recover everything — children lists and depths, for example:

```python
def children_from_parents(parents):
    children = {i: [] for i in range(len(parents))}
    for node, parent in enumerate(parents):
        if parent != -1:
            children[parent].append(node)
    return children

def depths_from_parents(parents):
    depths = [None] * len(parents)
    def depth(node):
        if depths[node] is None:
            depths[node] = 0 if parents[node] == -1 else depth(parents[node]) + 1
        return depths[node]
    return [depth(i) for i in range(len(parents))]

print(children_from_parents(parents))      # {0: [1, 2], 1: [3, 4], 2: [5], 3: [], 4: [], 5: []}
print(depths_from_parents(parents))        # [0, 1, 1, 2, 2, 2]
```

This compact form needs only one integer per node and finds a node's *parent* in O(1) — something the linked representation (which only points
downward) cannot do without extra work. The trade-off is that finding a node's children takes a scan (or the derived dictionary above). It
reappears in disjoint-set (union-find) structures, and the same index idea is used to store *complete binary trees* in arrays, as you will see in
[binary-trees.md](binary-trees.md) and in the [Heaps and Priority Queues](../heaps-and-priority-queues/README.md) module.

## 🧭 Kinds of Trees You Will Meet

The general tree above puts no restriction on the number of children or the arrangement of values. The rest of this domain studies special cases:

| Kind | Restriction | Purpose |
|------|-------------|---------|
| **Binary tree** | At most 2 children per node (left, right) | The next file; the basis of most of the others |
| **Binary search tree** | Left subtree < node < right subtree | Fast search, insertion, deletion |
| **Heap** | A parent is ≥ (or ≤) its children | Priority queues |
| **[Trie](../tries/README.md)** | Children indexed by characters | Prefix search |
| **Balanced trees** (AVL, red-black, B-tree) | Height kept near log n | Guaranteed fast operations; database indexes |

## ⚖️ What a Tree Costs

| Operation (general tree) | Cost |
|--------------------------|------|
| Add a child to a node you already hold | O(1) |
| Find a node by value (unordered) | O(n) |
| Find a node's parent (linked representation) | O(n) — O(1) with a parent pointer or parent array |
| Compute size, height, leaf count | O(n) |
| Memory | O(n): one node object per element plus the children lists |

## Common Mistakes

- **Mixing up height and depth.** Depth counts down from the root; height counts down to the deepest leaf. State whether you count edges or nodes.
- **Off-by-one in height**: a lone node has height 0 (edges) or 1 (nodes) — pick one convention.
- **Assuming a tree is balanced.** A tree of `n` nodes can have height anywhere from about `log n` to `n − 1`.
- **Forgetting the base case for leaves** in recursive functions — `max()` of an empty list of children raises `ValueError`.
- **Creating a cycle by attaching an existing node as a child of its own descendant**; the result is a graph, and recursive functions will not terminate.
- **Treating "search in a tree" as fast** without an ordering rule; that speed comes from structures such as binary search trees.

## ➡️ Next

Continue to [binary-trees.md](binary-trees.md) to restrict each node to two children — the structure behind searching, sorting, and heaps — and to learn
its shapes, properties, and array representation.
