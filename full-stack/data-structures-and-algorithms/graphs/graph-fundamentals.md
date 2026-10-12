# 🕸️ Graph Fundamentals

## Things and the Connections Between Them

A [tree](../trees/tree-fundamentals.md) models a strict hierarchy: one root, and every other item has exactly one parent. Much real-world data is not like that. Cities are linked by roads in loops; people
befriend each other in every direction; web pages link to one another and back; software modules depend on each other. A **graph** is the general structure for *things* and the *connections* between them,
and a tree is simply a graph with strict extra rules.

Formally, a graph `G = (V, E)` is a set of **vertices** `V` (also called nodes) and a set of **edges** `E`, where each edge connects two vertices. That is all — but with it you can model maps,
networks, schedules, dependencies, and puzzles, and a small set of algorithms (the rest of this module) answers a large range of questions about them: *Can I get from here to there? What is the
shortest route? What must happen first? Which pieces are connected?* All outputs below were produced by running the code on CPython 3.9.

```
   Undirected graph                   Directed graph (arrows have a direction)

      A ───── B                           A ───▶ B
      │ ╲     │                           ▲      │
      │   ╲   │                           │      ▼
      D ───── C                           D ◀─── C
```

## 📖 The Vocabulary

| Term | Meaning |
|------|---------|
| **Vertex / node** | One of the things (a city, a person, a web page) |
| **Edge** | A connection between two vertices |
| **Undirected edge** | Works both ways (a two-way road, a friendship) — written `{A, B}` |
| **Directed edge (arc)** | Has a direction from a tail to a head (a one-way street, a hyperlink, "A depends on B") — written `(A, B)` |
| **Weighted graph** | Each edge carries a number: distance, cost, time, capacity |
| **Adjacent / neighbours** | Two vertices joined by an edge |
| **Degree** | The number of edges at a vertex. In a directed graph: **in-degree** (edges arriving) and **out-degree** (edges leaving) |
| **Path** | A sequence of vertices in which each consecutive pair is joined by an edge |
| **Cycle** | A path that returns to its starting vertex |
| **Connected** (undirected) | Every vertex can reach every other along some path |
| **Connected component** | A maximal group of vertices that can all reach one another |
| **Strongly connected** (directed) | Every vertex can reach every other *following arrow directions* |
| **DAG** | A **d**irected **a**cyclic **g**raph: arrows, no cycle — the structure of prerequisites and build orders |
| **Self-loop / parallel edges** | An edge from a vertex to itself / two edges between the same pair of vertices |
| **Sparse / dense** | Few edges (close to `V`) / many edges (close to `V²`) |
| **Complete graph** | Every pair of vertices is joined by an edge |

A **tree** is the special case: an undirected graph that is **connected and has no cycles**. A forest is a graph whose components are all trees.

## 🌍 Modelling With Graphs

The skill that matters most is *recognising* a graph hidden in a problem:

| Real situation | Vertices | Edges | Kind of graph |
|----------------|----------|-------|---------------|
| Road map | Intersections | Roads (with lengths) | Weighted, undirected (or directed for one-way streets) |
| Social network | People | Friendships (or "follows") | Undirected (or directed) |
| The web | Pages | Hyperlinks | Directed |
| Course prerequisites | Courses | "A must come before B" | Directed acyclic (DAG) |
| A maze or game board | Cells or positions | Legal moves | Undirected or directed; often *implicit* (never stored) |
| Puzzle states (a Rubik's cube, "word ladder") | Configurations | One legal move apart | Implicit |
| Computer network | Machines | Links (with bandwidth) | Weighted, undirected |

Many graphs are **implicit**: you never build the whole thing. A chessboard has only 64 squares and a rule for the knight's moves; the graph exists in the rule. Exploring such a graph uses exactly the same
algorithms.

## 🔢 Counting Facts (Verified)

A few counting rules are worth knowing, because they explain algorithm costs:

- **Handshake lemma.** In an undirected graph, the degrees add up to **twice the number of edges** (each edge has two endpoints): `sum of degrees = 2 · |E|`.
- **Maximum edges.** A simple undirected graph on `n` vertices has at most `n(n − 1) / 2` edges; a simple directed graph at most `n(n − 1)`. So `|E|` ranges from 0 up to about `|V|²`.
- **Connectivity needs edges.** A connected graph on `n` vertices has at least `n − 1` edges.
- **Trees are the minimum.** A connected graph with *exactly* `n − 1` edges is a tree (connected, no cycles).

Rather than trust them, check them on thousands of random graphs. The checker below uses an independent method for connectivity and cycles (a union-find structure, which merges groups of vertices and notices when an
edge joins two vertices already in the same group):

```python
import random
from itertools import combinations

random.seed(1)

def random_simple_graph(n, m):
    """m distinct undirected edges (no self-loops, no parallel edges) on vertices 0..n-1."""
    return random.sample(list(combinations(range(n), 2)), m)

def degrees(n, edges):
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    return degree

def components_and_cycle(n, edges):
    """Return (number of connected components, whether the graph has a cycle) using union-find."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]            # path halving
            x = parent[x]
        return x

    cycle = False
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            cycle = True                             # u and v were already connected: this edge closes a cycle
        else:
            parent[ru] = rv
    return len({find(x) for x in range(n)}), cycle

trees_seen = 0
for _ in range(5000):
    n = random.randint(1, 8)
    max_edges = n * (n - 1) // 2
    m = random.randint(0, max_edges)
    edges = random_simple_graph(n, m)

    assert sum(degrees(n, edges)) == 2 * m                           # handshake lemma
    assert m <= max_edges                                            # edge bound

    components, has_cycle = components_and_cycle(n, edges)
    if components == 1:
        assert m >= n - 1                                            # a connected graph needs at least n - 1 edges
    is_tree = components == 1 and not has_cycle
    assert is_tree == (components == 1 and m == n - 1)               # connected + exactly n - 1 edges <=> tree
    trees_seen += is_tree
print(f"handshake lemma, edge bounds, and the tree test held on 5,000 random graphs ({trees_seen} of them were trees)")
```

```text
handshake lemma, edge bounds, and the tree test held on 5,000 random graphs (1212 of them were trees)
```

## 🧩 Connected Components, Concretely

A graph can fall into several separate pieces. Counting them, or asking whether two vertices lie in the same piece, is one of the most common graph questions:

```python
edges = [(0, 1), (1, 2), (3, 4), (5, 5)]          # vertices 0..6; a self-loop at 5; vertex 6 has no edges
components, has_cycle = components_and_cycle(7, edges)
print(components)                                 # 4   — {0, 1, 2}, {3, 4}, {5}, {6}
print(has_cycle)                                  # True — the self-loop (5, 5) closes a cycle of length 1
```

Four components, one of which (vertex 6) is isolated. The [BFS](breadth-first-search.md) and [DFS](depth-first-search.md) files show how to find the components with traversal, and
[graph-problems.md](graph-problems.md) builds the union-find structure properly.

## 📏 Density and Why It Matters

The ratio of the edges present to the edges possible is the graph's **density**. Most real networks are **sparse**: a person has hundreds of friends, not billions, so
`|E|` is on the order of `|V|`, not `|V|²`. That drives every design choice in this module: the choice of
[representation](graph-representation.md) (an adjacency list stores only the edges that exist; a matrix stores every possible pair), and the cost of algorithms, written in terms of **both** `V` and `E`
(for example, BFS costs **O(V + E)**, not O(V²)).

| Graph | Vertices `V` | Edges `E` | Density |
|-------|--------------|-----------|---------|
| A tree | `V` | `V − 1` | Extremely sparse |
| A grid of `r × c` cells (4 neighbours) | `r·c` | about `2·r·c` | Sparse |
| A social network | Millions | Hundreds per vertex | Sparse |
| A complete graph | `V` | `V(V − 1)/2` | Dense (density = 1) |

## 🗺️ A Map of the Module

| Question | Algorithm | File |
|----------|-----------|------|
| How do I store a graph? | Adjacency list, matrix, edge list | [graph-representation.md](graph-representation.md) |
| Fewest edges from A to B? Which vertices are within `k` steps? | Breadth-first search | [breadth-first-search.md](breadth-first-search.md) |
| Is there a path? A cycle? What order respects the dependencies? | Depth-first search, topological sort | [depth-first-search.md](depth-first-search.md) |
| Cheapest route when edges have costs? | Dijkstra, Bellman-Ford, Floyd-Warshall | [shortest-path-algorithms.md](shortest-path-algorithms.md) |
| Connect everything as cheaply as possible? Count groups? | Minimum spanning tree, union-find | [graph-problems.md](graph-problems.md) |

## Common Mistakes

- **Confusing directed and undirected edges.** An undirected edge is two-way; storing it once (A→B) and forgetting B→A breaks every search.
- **Assuming a graph is connected.** Algorithms that start from one vertex only reach that vertex's component; loop over all vertices to cover the rest.
- **Forgetting about cycles**, so that a traversal revisits vertices forever. Real graphs need a "visited" set.
- **Treating a graph like a tree** (looking for "the root" or a unique parent). Graphs have no root and vertices can have many incoming edges.
- **Using `V²` in cost estimates** for sparse graphs, or `E` for dense ones. State complexities in terms of both `V` and `E`.
- **Overlooking implicit graphs**: if the vertices are puzzle states or grid cells, build neighbours on demand instead of storing everything.

## ➡️ Next

Continue to [graph-representation.md](graph-representation.md) to see how graphs are stored in memory — adjacency lists, adjacency matrices, and edge lists — and how much each costs.
