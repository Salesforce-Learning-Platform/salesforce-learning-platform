# 🗃️ Graph Representation

## Three Ways to Store the Same Graph

Before an algorithm can explore a graph, the graph has to live somewhere in memory. The same graph can be stored in several ways, and the choice changes the cost of the questions you ask most:
*Is there an edge between A and B? Who are A's neighbours? Show me every edge.* This file builds the three standard representations — the **adjacency list**, the **adjacency matrix**, and the
**edge list** — compares their costs (including a measurement), and shows **implicit** graphs such as a grid, which are never stored at all. All outputs were produced by running the code on CPython 3.9.

The running example is this small weighted, undirected graph:

```
        4
   A ─────── B
   │       ╱ │
 1 │    2╱   │ 5
   │   ╱     │
   C ─────── D
        3
```

Its edges are `A–B (4)`, `A–C (1)`, `B–C (2)`, `B–D (5)`, and `C–D (3)`.

## 📋 1. The Adjacency List

For each vertex, store **the collection of its neighbours**. In Python the natural form is a dictionary mapping each vertex to its neighbours (and, for a weighted graph, to a nested dictionary of
`neighbour → weight`):

```python
graph = {
    "A": {"B": 4, "C": 1},
    "B": {"A": 4, "C": 2, "D": 5},
    "C": {"A": 1, "B": 2, "D": 3},
    "D": {"B": 5, "C": 3},
}
print(graph["B"])                    # {'A': 4, 'C': 2, 'D': 5}   — the neighbours of B and the edge weights
print("D" in graph["C"])             # True     — is there an edge C-D? O(1) with a dictionary
print(sum(len(n) for n in graph.values()) // 2)       # 5         — each undirected edge appears twice, once per endpoint
```

For an **unweighted** graph, a dictionary of lists (or sets) is enough: `{"A": ["B", "C"], ...}`. The list stores each edge once per direction, so its size is **O(V + E)** — proportional to what is actually
there. It is the default choice, and the one the rest of this module uses.

## 🔲 2. The Adjacency Matrix

Number the vertices `0 … V−1` and keep a `V × V` table in which cell `[i][j]` says whether an edge goes from `i` to `j` (and, if weighted, what it weighs):

```
          A  B  C  D
       A  .  4  1  .          '.' = no edge
       B  4  .  2  5
       C  1  2  .  3
       D  .  5  3  .
```

Checking an edge is a single array lookup, **O(1)** — but the table has `V²` cells no matter how few edges exist, and listing a vertex's neighbours means scanning a whole row, **O(V)**. For an undirected graph the
matrix is symmetric (`[i][j] == [j][i]`).

## 📝 3. The Edge List

The simplest of all: a plain list of `(u, v)` or `(u, v, weight)` entries.

```python
edge_list = [("A", "B", 4), ("A", "C", 1), ("B", "C", 2), ("B", "D", 5), ("C", "D", 3)]
```

It takes only **O(E)** space and is exactly the input format of many problems and files. It is also what algorithms that process *edges* in order — such as Kruskal's minimum spanning tree algorithm in
[graph-problems.md](graph-problems.md) — want. But finding a vertex's neighbours means scanning every edge: **O(E)**.

## ⚖️ Cost Comparison

| Operation | Adjacency list | Adjacency matrix | Edge list |
|-----------|----------------|------------------|-----------|
| Space | **O(V + E)** | O(V²) | **O(E)** |
| Is there an edge `u–v`? | O(1) (dict/set) or O(degree) (list) | **O(1)** | O(E) |
| List the neighbours of `u` | **O(degree of u)** | O(V) | O(E) |
| Add an edge | O(1) | O(1) | O(1) |
| Remove an edge | O(1) (dict/set) or O(degree) (list) | O(1) | O(E) |
| Add a vertex | O(1) | O(V²) to rebuild the table | O(1) |
| Visit every edge | O(V + E) | O(V²) | **O(E)** |

**Rule of thumb:** use an **adjacency list** for almost everything, especially sparse graphs. Use a **matrix** when the graph is dense, when `V` is small, or when you need constant-time edge lookups (and for
algorithms like Floyd-Warshall that consider all pairs). Use an **edge list** for input and for edge-sorted algorithms.

## 🔨 A Reusable `Graph` Class

A small class wraps the adjacency-list representation, supporting directed or undirected graphs and optional weights:

```python
class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self._adj = {}                                   # vertex -> {neighbour: weight}

    def add_vertex(self, v):
        self._adj.setdefault(v, {})

    def add_edge(self, u, v, weight=1):
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u][v] = weight
        if not self.directed:
            self._adj[v][u] = weight                     # an undirected edge is stored in both directions

    def remove_edge(self, u, v):
        del self._adj[u][v]
        if not self.directed:
            del self._adj[v][u]

    def has_edge(self, u, v):
        return v in self._adj.get(u, {})

    def weight(self, u, v):
        return self._adj[u][v]

    def neighbors(self, u):
        return list(self._adj[u])

    def degree(self, u):                                 # out-degree, for a directed graph
        return len(self._adj[u])

    def vertices(self):
        return list(self._adj)

    def edges(self):                                     # each edge once: (u, v, weight)
        seen = set()
        for u, nbrs in self._adj.items():
            for v, w in nbrs.items():
                if self.directed or (v, u) not in seen:
                    seen.add((u, v))
                    yield (u, v, w)

    def __len__(self):
        return len(self._adj)

g = Graph()
for u, v, w in edge_list:
    g.add_edge(u, v, w)
print(len(g), g.degree("B"), sorted(g.neighbors("C")))        # 4 3 ['A', 'B', 'D']
print(g.has_edge("A", "D"), g.has_edge("D", "C"), g.weight("B", "D"))      # False True 5
print(sorted(g.edges()))      # [('A', 'B', 4), ('A', 'C', 1), ('B', 'C', 2), ('B', 'D', 5), ('C', 'D', 3)]

road = Graph(directed=True)                                   # a one-way street from X to Y
road.add_edge("X", "Y", 7)
print(road.has_edge("X", "Y"), road.has_edge("Y", "X"))       # True False
```

### Converting Between Representations

Switching representation is mechanical, and a round trip is a good test that nothing was lost. The matrix uses `None` for "no edge" so that a weight of `0` remains distinguishable:

```python
def to_matrix(graph, order):
    index = {v: i for i, v in enumerate(order)}
    matrix = [[None] * len(order) for _ in order]
    for u, v, w in graph.edges():
        matrix[index[u]][index[v]] = w
        if not graph.directed:
            matrix[index[v]][index[u]] = w
    return matrix

def from_matrix(matrix, order, directed=False):
    graph = Graph(directed)
    for v in order:
        graph.add_vertex(v)
    for i, row in enumerate(matrix):
        for j, w in enumerate(row):
            if w is not None and (directed or i <= j):
                graph.add_edge(order[i], order[j], w)
    return graph

def reverse(graph):                                           # a directed graph with every edge flipped
    flipped = Graph(directed=True)
    for v in graph.vertices():
        flipped.add_vertex(v)
    for u, v, w in graph.edges():
        flipped.add_edge(v, u, w)
    return flipped

order = ["A", "B", "C", "D"]
matrix = to_matrix(g, order)
for row in matrix:
    print(row)
print(sorted(from_matrix(matrix, order).edges()) == sorted(g.edges()))      # True
print(sorted(reverse(road).edges()))                                         # [('Y', 'X', 7)]
```

```text
[None, 4, 1, None]
[4, None, 2, 5]
[1, 2, None, 3]
[None, 5, 3, None]
True
[('Y', 'X', 7)]
```

## 🔲 Implicit Graphs: The Grid

Many problems give you a grid — a maze, a map of islands, a game board — rather than a graph. Each cell is a vertex, and its neighbours are the adjacent cells. You do **not** build an adjacency list; you
compute the neighbours on demand:

```python
def grid_neighbors(row, col, rows, cols):
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):         # up, down, left, right
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            yield (r, c)

print(list(grid_neighbors(0, 0, 3, 4)))        # [(1, 0), (0, 1)]                    — a corner has 2 neighbours
print(list(grid_neighbors(1, 1, 3, 4)))        # [(0, 1), (2, 1), (1, 0), (1, 2)]    — an interior cell has 4
```

A `rows × cols` grid has `V = rows·cols` vertices and about `2V` edges. Storing them explicitly would waste memory; generating neighbours on demand costs nothing. The same trick works for
puzzles, where the "neighbours" of a state are the states reachable by one legal move. Add diagonals (eight directions), or wrap around the edges (a torus), by changing the list of offsets.

## 📖 Reading a Graph From Text

Programs and puzzles often supply a graph as text: a line with `V` and `E`, followed by `E` lines of edges. Parsing it into an adjacency list is a short loop:

```python
def read_graph(text, directed=False):
    lines = text.strip().splitlines()
    vertex_count, edge_count = map(int, lines[0].split())
    graph = Graph(directed)
    for v in range(vertex_count):
        graph.add_vertex(v)                                   # so that isolated vertices are included
    for line in lines[1:1 + edge_count]:
        u, v, *rest = line.split()
        graph.add_edge(int(u), int(v), int(rest[0]) if rest else 1)
    return graph

parsed = read_graph("""
5 4
0 1 10
1 2 20
0 2 5
3 4 1
""")
print(len(parsed), sorted(parsed.edges()))    # 5 [(0, 1, 10), (0, 2, 5), (1, 2, 20), (3, 4, 1)]
```

Adding every vertex first matters: otherwise a vertex with no edges (an isolated vertex) would silently vanish from the graph.

## 📊 What the Representations Cost in Memory and Time

On a sparse graph — `V` vertices and about `3V` edges, typical of real networks — compare the memory for a matrix and an adjacency list, and the time to visit every neighbour of every vertex:

```python
import random
import time
import tracemalloc

def random_edges(n, m):
    seen = set()
    while len(seen) < m:
        u, v = random.randrange(n), random.randrange(n)
        if u != v and (u, v) not in seen and (v, u) not in seen:
            seen.add((u, v))
    return list(seen)

def build_matrix(n, edges):
    matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = matrix[v][u] = 1
    return matrix

def build_lists(n, edges):
    adjacency = {v: [] for v in range(n)}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    return adjacency

def megabytes(build):
    tracemalloc.start()
    start = tracemalloc.get_traced_memory()[0]
    structure = build()
    used = tracemalloc.get_traced_memory()[0] - start
    tracemalloc.stop()
    return used / 1e6, structure

random.seed(3)
print(f"{'V':>6} | {'E':>7} | {'matrix MB':>9} | {'lists MB':>8} | {'scan matrix (ms)':>16} | {'scan lists (ms)':>15}")
for n in (500, 1_000, 2_000):
    edges = random_edges(n, 3 * n)
    m_mb, matrix = megabytes(lambda: build_matrix(n, edges))
    l_mb, lists = megabytes(lambda: build_lists(n, edges))

    start = time.perf_counter()
    count = sum(1 for u in range(n) for v in range(n) if matrix[u][v])        # visit every neighbour via the matrix
    t_matrix = (time.perf_counter() - start) * 1000
    start = time.perf_counter()
    count2 = sum(1 for u in lists for v in lists[u])                          # visit every neighbour via the lists
    t_lists = (time.perf_counter() - start) * 1000
    assert count == count2 == 2 * len(edges)
    print(f"{n:>6,} | {len(edges):>7,} | {m_mb:>9.1f} | {l_mb:>8.2f} | {t_matrix:>16.1f} | {t_lists:>15.2f}")
```

Output:

```
     V |       E | matrix MB | lists MB | scan matrix (ms) | scan lists (ms)
   500 |   1,500 |       2.0 |     0.09 |              7.9 |            0.08
 1,000 |   3,000 |       8.1 |     0.17 |             26.8 |            0.16
 2,000 |   6,000 |      32.1 |     0.36 |            106.8 |            0.32
```

Doubling `V` **quadruples** the matrix's memory and scan time (it is O(V²)), while the adjacency list grows only about twofold (O(V + E)). At 2,000 vertices and 6,000 edges the matrix already needs about ninety times
more memory, and scanning it is more than three hundred times slower — and at a million vertices the matrix (a trillion cells) would be impossible, while the list is still modest. That is why sparse graphs use adjacency lists.

## ✅ Verification

The `Graph` class and the conversions were checked on random graphs: the matrix round trip must reproduce the edge set, the degree sum must equal twice the number of edges (undirected) or the number of edges
(directed), reversing twice must give back the original, and a graph written as text and parsed again must be unchanged:

```python
random.seed(5)
for _ in range(2000):
    n = random.randint(1, 8)
    directed = random.random() < 0.5
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v and (directed or u < v)]
    chosen = random.sample(pairs, random.randint(0, len(pairs)))
    graph = Graph(directed)
    for v in range(n):
        graph.add_vertex(v)
    for u, v in chosen:
        graph.add_edge(u, v, random.randint(0, 9))                # weights include 0, which a matrix must still represent

    order = list(range(n))
    rebuilt = from_matrix(to_matrix(graph, order), order, directed)
    assert sorted(rebuilt.edges()) == sorted(graph.edges())
    assert sum(graph.degree(v) for v in graph.vertices()) == (len(chosen) if directed else 2 * len(chosen))
    if directed:
        assert sorted(reverse(reverse(graph)).edges()) == sorted(graph.edges())

    text = f"{n} {len(chosen)}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in graph.edges())
    again = read_graph(text, directed)
    assert sorted(again.edges()) == sorted(graph.edges()) and len(again) == n
print("matrix round trips, degree sums, double reversal, and text parsing all agree on 2,000 random graphs")
```

```text
matrix round trips, degree sums, double reversal, and text parsing all agree on 2,000 random graphs
```

## 🧭 Choosing a Representation

| Situation | Choose |
|-----------|--------|
| Most graph algorithms (BFS, DFS, Dijkstra) on sparse graphs | **Adjacency list** |
| Dense graph, small `V`, or constant-time "is there an edge?" queries | Adjacency matrix |
| All-pairs algorithms (Floyd-Warshall) | Adjacency matrix |
| Sorting or scanning edges (Kruskal's minimum spanning tree) | Edge list |
| The graph is a grid, a board, or a puzzle | Implicit graph (compute neighbours on demand) |

## Common Mistakes

- **Storing an undirected edge once**, so only one direction can be traversed.
- **Forgetting isolated vertices** — add every vertex explicitly, not only those that appear in edges.
- **Using an adjacency matrix for a large sparse graph**, running out of memory (`V²` cells).
- **Using `0` to mean "no edge" in a weighted matrix**, which cannot distinguish a real zero-weight edge.
- **Using a list for neighbours and calling `in` on it** for edge checks inside a loop (O(degree) each time); use a `set` or `dict`.
- **Mutating the neighbour collection while iterating over it.**
- **Building the whole graph when it is implicit** — generate neighbours instead.

## ➡️ Next

Continue to [breadth-first-search.md](breadth-first-search.md) to explore a graph level by level and find shortest paths in unweighted graphs.
