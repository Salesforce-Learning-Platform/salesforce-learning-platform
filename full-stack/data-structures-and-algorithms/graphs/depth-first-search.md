# 🕳️ Depth-First Search (DFS)

## Go as Deep as You Can, Then Back Up

Where [breadth-first search](breadth-first-search.md) explores in expanding rings, **depth-first search** behaves like someone exploring a maze with a ball of string: follow one corridor as far as it goes; when
you hit a dead end (or a place you have already been), backtrack to the last junction and try the next corridor. It uses a **stack** — either explicitly or through recursion — where BFS uses a queue.

DFS does not find shortest paths, but it excels at questions about *structure*:

- Can I reach B from A? Which vertices are in the same **connected component**?
- Does the graph contain a **cycle**?
- In what order can things be done so that every **dependency** comes first (**topological sort**)?
- How many **islands** are on this grid?

It is the graph generalisation of the depth-first tree traversals in [tree-traversal.md](../trees/tree-traversal.md). All outputs below were produced by running the code on CPython 3.9. Graphs are dictionaries
from each vertex to a list of its neighbours (an undirected edge appears in both lists).

## 🧭 The Algorithm, Recursively

Visit a vertex; mark it; then recurse into each unvisited neighbour. The function call stack remembers where to backtrack to:

```python
def dfs_recursive(graph, start):
    visited = set()
    order = []

    def visit(node):
        visited.add(node)
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                visit(neighbour)                  # go deeper first; return here when that branch is finished

    visit(start)
    return order

graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}
print(dfs_recursive(graph, "A"))       # ['A', 'B', 'D', 'E', 'F', 'C']
```

Trace it: from `A` go to its first neighbour `B`; from `B` the first unvisited neighbour is `D` — a dead end, so back to `B` and on to `E`; from `E` the unvisited neighbour is `F`; from `F` the neighbour
`C` is unvisited, so go there; `C`'s neighbours (`A`, `F`) are both visited, so it finishes, and the recursion unwinds all the way back. Compare this with BFS's `A, B, C, D, E, F`: DFS plunges down a path (`A → B → E → F → C`) before
touching `C` from `A`.

## 🔁 The Algorithm, Iteratively

An explicit stack replaces the call stack. To visit neighbours in the same order as the recursive version, push them in **reverse**, so the first neighbour ends up on top:

```python
def dfs_iterative(graph, start):
    visited = set()
    order = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue                              # this vertex was reached by another route in the meantime
        visited.add(node)
        order.append(node)
        for neighbour in reversed(graph[node]):
            if neighbour not in visited:
                stack.append(neighbour)
    return order

print(dfs_iterative(graph, "A"))       # ['A', 'B', 'D', 'E', 'F', 'C']
```

Note a difference from BFS: here a vertex is marked visited when it is **popped**, not when it is pushed, and the same vertex may sit on the stack more than once (the `if node in visited: continue` skips
the repeats). The order is identical to the recursive version.

Why bother with the iterative form? **Python's recursion limit**. A graph that is one long chain forces the recursive version a thousand frames deep:

```python
chain = {i: [i + 1] for i in range(5000)}
chain[5000] = []

print(len(dfs_iterative(chain, 0)))                 # 5001
try:
    dfs_recursive(chain, 0)
except RecursionError:
    print("the recursive version overflowed")        # the recursive version overflowed
```

Both versions cost **O(V + E)** time: every vertex is visited once and every adjacency list is scanned once. The stack holds at most `V` entries, and in the recursive form the recursion depth can reach `V`.

## ⏱️ Discovery and Finish Times

Many DFS applications use two timestamps per vertex: when it is **discovered** (first reached) and when it is **finished** (all its descendants fully explored). A single counter ticks at both events:

```python
def dfs_times(graph):
    discovery, finish = {}, {}
    clock = [0]

    def visit(node):
        clock[0] += 1
        discovery[node] = clock[0]
        for neighbour in graph[node]:
            if neighbour not in discovery:
                visit(neighbour)
        clock[0] += 1
        finish[node] = clock[0]

    for node in graph:                              # start a new search from every unvisited vertex
        if node not in discovery:
            visit(node)
    return discovery, finish

discovery, finish = dfs_times(graph)
for node in graph:
    print(node, discovery[node], finish[node])
```

```text
A 1 12
B 2 11
C 7 8
D 3 4
E 5 10
F 6 9
```

The intervals `[discovery, finish]` obey the **parenthesis property**: for any two vertices the intervals are either completely nested (one is a descendant of the other in the DFS) or completely disjoint — never
partially overlapping. Here `A` spans `[1, 12]` and contains everything else, and `D` spans `[3, 4]` entirely inside `B`'s `[2, 11]`. Finish times are the key to topological sorting, below.

## 🔄 Cycle Detection

### Undirected Graphs

In an undirected graph, a DFS that meets an already-visited vertex *other than the one it just came from* has found a **cycle** (the neighbour was reached by another route, so there are two routes between the same
pair). The parent must be excluded, because every undirected edge leads straight back to where you came from:

```python
def has_cycle_undirected(graph):
    visited = set()

    def visit(node, parent):
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour == parent:
                continue                              # the edge we just walked along
            if neighbour in visited or visit(neighbour, node):
                return True                           # a second route to a visited vertex: a cycle
        return False

    return any(visit(v, None) for v in graph if v not in visited)

triangle = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
path = {0: [1], 1: [0, 2], 2: [1]}
print(has_cycle_undirected(triangle), has_cycle_undirected(path))      # True False
```

### Directed Graphs: Three Colours

The undirected rule fails for directed graphs. Consider a "diamond": `A → B`, `A → C`, `B → D`, `C → D`. The vertex `D` is reached twice, but there is no cycle — you cannot get back to `A`. A directed cycle exists
only if DFS finds an edge pointing to a vertex that is **still on the current path** (an ancestor being explored). So each vertex gets one of three colours:

- **white** — not yet visited;
- **gray** — currently being explored (on the recursion path);
- **black** — completely finished.

An edge to a **gray** vertex closes a cycle. An edge to a black vertex is harmless (it was fully explored earlier and did not lead back).

```python
def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph}

    def visit(node):
        color[node] = GRAY                            # now on the current path
        for neighbour in graph[node]:
            if color[neighbour] == GRAY:
                return True                           # an edge back to a vertex on the current path: a cycle
            if color[neighbour] == WHITE and visit(neighbour):
                return True
        color[node] = BLACK                           # finished; no cycle through it
        return False

    return any(color[v] == WHITE and visit(v) for v in graph)

def naive_directed_cycle(graph):                      # WRONG: "I have seen this vertex before" is not enough
    visited = set()
    def visit(node):
        if node in visited:
            return True
        visited.add(node)
        return any(visit(n) for n in graph[node])
    return any(visit(v) for v in graph if v not in visited)

diamond = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
loop = {"A": ["B"], "B": ["C"], "C": ["A"]}
print(naive_directed_cycle(diamond), has_cycle_directed(diamond))      # True False
print(has_cycle_directed(loop))                                        # True
```

The naive version declares the diamond cyclic. The three-colour version, which is **O(V + E)**, gets it right.

## 📋 Topological Sort

A **topological order** lists the vertices of a directed graph so that for every edge `u → v`, `u` comes before `v`. It exists exactly when the graph has no directed cycle (a DAG), and it answers "in what order can
these tasks be done, given their dependencies?" — build systems, course prerequisites, spreadsheet cell recalculation. There are two classic methods.

### Method 1: Reverse DFS Finishing Order

A vertex finishes only after everything it points to has finished. So listing vertices in **decreasing finish time** puts every vertex before the things that depend on it:

```python
def topological_sort_dfs(graph):
    visited = set()
    finished = []

    def visit(node):
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                visit(neighbour)
        finished.append(node)                          # appended only after all of its successors are done

    for v in graph:
        if v not in visited:
            visit(v)
    return finished[::-1]                              # reverse: latest-finished first

getting_dressed = {
    "underwear": ["trousers", "shoes"],
    "trousers": ["belt", "shoes"],
    "socks": ["shoes"],
    "shirt": ["belt", "tie"],
    "tie": ["jacket"],
    "belt": ["jacket"],
    "shoes": [],
    "jacket": [],
}
print(topological_sort_dfs(getting_dressed))
```

```text
['shirt', 'tie', 'socks', 'underwear', 'trousers', 'shoes', 'belt', 'jacket']
```

Any listed order puts each item before everything that depends on it (`underwear` before `trousers` before `shoes`; `shirt` and `belt` and `tie` before `jacket`). There can be many valid orders; the algorithm
returns one of them. This method assumes the graph has no cycle — on a cyclic graph the result is meaningless, so check with `has_cycle_directed` first if the input is untrusted.

### Method 2: Kahn's Algorithm (Peeling Off Sources)

Repeatedly remove a vertex that has **no incoming edges** (nothing it still waits for), output it, and delete its outgoing edges, which may free other vertices. Track each vertex's **in-degree**: when it reaches zero, the vertex is
ready.

```python
from collections import deque

def topological_sort_kahn(graph):
    indegree = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1
    ready = deque(v for v in graph if indegree[v] == 0)     # vertices that wait for nothing
    order = []
    while ready:
        node = ready.popleft()
        order.append(node)
        for neighbour in graph[node]:
            indegree[neighbour] -= 1
            if indegree[neighbour] == 0:
                ready.append(neighbour)                      # its last prerequisite just finished
    return order if len(order) == len(graph) else None       # None: a cycle kept some vertices from ever becoming ready

print(topological_sort_kahn(getting_dressed))
print(topological_sort_kahn(loop))                           # None — a cycle has no valid order
```

```text
['underwear', 'socks', 'shirt', 'trousers', 'tie', 'belt', 'shoes', 'jacket']
None
```

A bonus of Kahn's algorithm is built-in cycle detection: if the output is shorter than the vertex count, the leftover vertices form (or depend on) a cycle. Both methods run in **O(V + E)**. Kahn's is the natural choice when
you need to *detect* an impossible schedule, or to process tasks in "waves" (everything ready at the same time can run in parallel).

## 🏝️ Counting Islands in a Grid

A grid of `"1"` (land) and `"0"` (water) is an implicit graph in which land cells touching horizontally or vertically are connected. The number of **islands** is the number of connected components of land. Start a search from each
unvisited land cell; the search marks that whole island visited, so each island is counted exactly once. A stack-based DFS avoids recursion-depth problems on big grids:

```python
def count_islands(grid):
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    seen = set()
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                islands += 1                                   # a new, unvisited island
                seen.add((r, c))
                stack = [(r, c)]
                while stack:                                   # flood-fill the island
                    cr, cc = stack.pop()
                    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" and (nr, nc) not in seen:
                            seen.add((nr, nc))
                            stack.append((nr, nc))
    return islands

sea = [
    "11000",
    "11000",
    "00100",
    "00011",
]
print(count_islands(sea))                           # 3
print(count_islands(["000", "000"]), count_islands([]))        # 0 0
```

The same flood-fill idea is what a paint-bucket tool uses. Cost: **O(rows × cols)**. BFS would work equally well here; DFS is shorter to write.

## 🛤️ Backtracking: Listing All Paths

DFS plus *undoing* the last step — **backtracking** — enumerates all simple paths (paths with no repeated vertex) from one vertex to another:

```python
def all_paths(graph, start, goal):
    paths = []
    path = [start]

    def visit(node):
        if node == goal:
            paths.append(path[:])                     # record a COPY of the path so far
            return
        for neighbour in graph[node]:
            if neighbour not in path:                 # never revisit a vertex on the current path
                path.append(neighbour)
                visit(neighbour)
                path.pop()                            # backtrack: undo the step

    visit(start)
    return paths

for p in all_paths(graph, "A", "F"):
    print(p)
```

```text
['A', 'B', 'E', 'F']
['A', 'C', 'F']
```

The number of simple paths can grow exponentially with the size of the graph, so this is practical only for small graphs — for "does a path exist?" or "what is the shortest?" use plain DFS or BFS instead.

## ✅ Verification

Every function was checked on thousands of random graphs against an independent definition: the **recursive and iterative orders must agree**; the **parenthesis property** must hold for all interval pairs; cycle detection is compared with a
**Floyd-Warshall reachability closure** (a directed graph has a cycle exactly when some vertex can reach itself) and, for undirected graphs, with **union-find**; both topological sorts must respect every edge; and island counts are
compared with a union-find over land cells.

```python
import random

random.seed(7)

def random_digraph(n, p):
    return {u: [v for v in range(n) if v != u and random.random() < p] for u in range(n)}

def reachability(graph):
    n = len(graph)
    reach = [[False] * n for _ in range(n)]
    for u in graph:
        for v in graph[u]:
            reach[u][v] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True
    return reach

def uf_has_cycle(graph):                                 # undirected, simple graph
    parent = list(graph)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u in graph:
        for v in graph[u]:
            if u < v:
                ru, rv = find(u), find(v)
                if ru == rv:
                    return True
                parent[ru] = rv
    return False

def respects_edges(graph, order):
    position = {v: i for i, v in enumerate(order)}
    return sorted(position) == sorted(graph) and all(position[u] < position[v] for u in graph for v in graph[u])

assert respects_edges(getting_dressed, topological_sort_dfs(getting_dressed))
assert respects_edges(getting_dressed, topological_sort_kahn(getting_dressed))

for _ in range(2500):
    g = random_digraph(random.randint(1, 7), random.choice([0.1, 0.2, 0.35]))
    reach = reachability(g)
    cyclic = any(reach[v][v] for v in g)
    assert has_cycle_directed(g) == cyclic
    for start in g:
        assert dfs_recursive(g, start) == dfs_iterative(g, start)
        assert set(dfs_recursive(g, start)) == {start} | {v for v in g if reach[start][v]}
    order = topological_sort_kahn(g)
    assert (order is None) == cyclic
    if not cyclic:
        assert respects_edges(g, order) and respects_edges(g, topological_sort_dfs(g))
    discovery, finish = dfs_times(g)
    nodes = list(g)
    for a in nodes:
        for b in nodes:
            if a != b:
                (da, fa), (db, fb) = (discovery[a], finish[a]), (discovery[b], finish[b])
                nested = (da < db and fb < fa) or (db < da and fa < fb)
                disjoint = fa < db or fb < da
                assert nested or disjoint                           # never partially overlapping

    # undirected version of the same random edges
    ug = {v: set() for v in g}
    for u in g:
        for v in g[u]:
            ug[u].add(v)
            ug[v].add(u)
    ug = {v: sorted(ns) for v, ns in ug.items()}
    assert has_cycle_undirected(ug) == uf_has_cycle(ug)

for _ in range(2000):
    rows, cols = random.randint(1, 6), random.randint(1, 6)
    grid = ["".join(random.choice("01") for _ in range(cols)) for _ in range(rows)]
    parent = {(r, c): (r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "1"}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (r, c) in list(parent):
        for nr, nc in ((r + 1, c), (r, c + 1)):
            if (nr, nc) in parent:
                parent[find((r, c))] = find((nr, nc))
    assert count_islands(grid) == len({find(x) for x in parent})

    graph_a = random_digraph(random.randint(2, 6), 0.3)
    s, t = random.sample(list(graph_a), 2)
    found = all_paths(graph_a, s, t)
    assert len(found) == len({tuple(p) for p in found})                          # no duplicates
    assert all(p[0] == s and p[-1] == t and len(set(p)) == len(p) and all(b in graph_a[a] for a, b in zip(p, p[1:])) for p in found)
print("DFS, cycle detection, topological sorts, times, islands and path listing all agree with independent checks")
```

```text
DFS, cycle detection, topological sorts, times, islands and path listing all agree with independent checks
```

## 🆚 DFS or BFS?

| Question | Prefer |
|----------|--------|
| Shortest path by number of edges | **BFS** |
| Does a path exist? What is reachable? | Either; DFS is shorter to write |
| Connected components, flood fill, counting islands | Either |
| Cycle detection | **DFS** (three colours, or parent tracking) |
| Topological order of a DAG | **DFS** (reverse finish) or Kahn's algorithm (queue) |
| Enumerate all paths or configurations (backtracking) | **DFS** |
| Very deep graphs in Python | Iterative DFS (avoid the recursion limit) |
| Very wide graphs, tight memory | DFS (stack holds one path) over BFS (queue holds a whole frontier) |

## Common Mistakes

- **Using recursive DFS on deep graphs** in Python and hitting the recursion limit.
- **Applying the undirected cycle rule to a directed graph** (it flags harmless diamonds) — use the three-colour method.
- **Forgetting to exclude the parent** in undirected cycle detection, so every edge looks like a cycle.
- **Forgetting to restart from every unvisited vertex** (disconnected graphs, topological sort).
- **Reversing the topological order incorrectly**: the DFS finish order must be reversed.
- **Running topological sort on a graph with a cycle** without checking — the output is meaningless.
- **Not undoing a step when backtracking**, or recording the working path instead of a copy.

## ➡️ Next

Continue to [shortest-path-algorithms.md](shortest-path-algorithms.md) to find cheapest routes when edges have costs: Dijkstra's algorithm, Bellman-Ford, and Floyd-Warshall.
