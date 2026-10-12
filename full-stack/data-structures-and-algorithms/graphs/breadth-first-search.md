# 🌊 Breadth-First Search (BFS)

## Explore in Rings: Nearest First

Breadth-first search explores a graph the way a ripple spreads on water: first the start vertex, then everything one edge away, then everything two edges away, and so on. Because it processes vertices in order of
distance, **the first time BFS reaches a vertex is along a path with the fewest possible edges**. That makes BFS the algorithm for:

- the **shortest path in an unweighted graph** (fewest edges, fewest moves, fewest clicks);
- everything **within `k` steps** of a vertex ("friends of friends");
- **connected components**;
- **2-colouring** (bipartite checks); and
- **grid and maze** problems, where each move costs one step.

BFS uses a [queue](../stacks-and-queues/queue-fundamentals.md) — first in, first out — which is exactly what makes the ripples go outward in order. It is the graph version of the level-order traversal in
[tree-traversal.md](../trees/tree-traversal.md). All outputs below were produced by running the code on CPython 3.9. Graphs here are dictionaries mapping each vertex to a list of its neighbours (see
[graph-representation.md](graph-representation.md)); an undirected edge appears in both vertices' lists.

## 🧭 The Algorithm

1. Put the start vertex in the queue and mark it visited.
2. Take the vertex at the front of the queue.
3. For each of its unvisited neighbours: mark it visited and add it to the back of the queue.
4. Repeat from step 2 until the queue is empty.

```python
from collections import deque

def bfs_order(graph, start):
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)             # mark when it is ENQUEUED, not when it is dequeued
                queue.append(neighbour)
    return order

graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}
print(bfs_order(graph, "A"))            # ['A', 'B', 'C', 'D', 'E', 'F']
```

```
        A            Ripple 0: A
       / \           Ripple 1: B, C        (one edge from A)
      B   C          Ripple 2: D, E, F     (two edges from A)
     / \   \
    D   E───F
```

### Why Mark Visited When You Enqueue

The `visited` set serves two purposes: it prevents infinite loops on cycles, and it prevents the same vertex from being queued repeatedly. The second purpose only works if the mark is made **when the vertex is
added to the queue**. If you wait until it is removed, a vertex reachable from several already-queued vertices gets queued several times. On a complete graph (every vertex joined to every other) the difference is dramatic:

```python
def complete_graph(n):
    return {v: [u for u in range(n) if u != v] for v in range(n)}

def pushes_marking_on_enqueue(graph, start):
    visited, queue, pushes = {start}, deque([start]), 1
    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                pushes += 1
    return pushes

def pushes_marking_on_dequeue(graph, start):
    visited, queue, pushes = set(), deque([start]), 1
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                queue.append(neighbour)
                pushes += 1
    return pushes

for n in (10, 50, 100):
    g = complete_graph(n)
    print(f"{n:>3} vertices: marked on enqueue -> {pushes_marking_on_enqueue(g, 0):>5} queue pushes; marked on dequeue -> {pushes_marking_on_dequeue(g, 0):>6}")
```

```text
 10 vertices: marked on enqueue ->    10 queue pushes; marked on dequeue ->     46
 50 vertices: marked on enqueue ->    50 queue pushes; marked on dequeue ->   1226
100 vertices: marked on enqueue ->   100 queue pushes; marked on dequeue ->   4951
```

Marking at enqueue gives exactly one push per vertex. Marking at dequeue lets the queue grow to roughly the number of *edges*, which for a dense graph is quadratic in the number of vertices. The visited order is
the same, but the work and memory are not.

## ⏱️ Cost

Each vertex is enqueued and dequeued at most once, and each vertex's neighbour list is scanned once, so the total work is proportional to the number of vertices plus the number of edges: **O(V + E)** time. The visited
set and the queue take **O(V)** space. (In an undirected graph each edge is looked at twice, once from each end — still O(E).)

## 📏 Shortest Paths and Distances

Record two facts as vertices are discovered: how far each is from the start, and **which vertex discovered it** (its *parent*). Distances come for free from the ripples, and following parents backward from any
vertex reconstructs a shortest path:

```python
def bfs(graph, start):
    distance = {start: 0}                          # also serves as the visited set
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if neighbour not in distance:
                distance[neighbour] = distance[node] + 1
                parent[neighbour] = node
                queue.append(neighbour)
    return distance, parent

def shortest_path(graph, start, goal):
    distance, parent = bfs(graph, start)
    if goal not in distance:
        return None                                # unreachable
    path = []
    node = goal
    while node is not None:                        # walk backward through the parents
        path.append(node)
        node = parent[node]
    return path[::-1]

distance, parent = bfs(graph, "A")
print(distance)                                    # {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2}
print(shortest_path(graph, "A", "F"))              # ['A', 'C', 'F']
print(shortest_path(graph, "D", "F"))              # ['D', 'B', 'E', 'F']
print(shortest_path({"X": [], "Y": []}, "X", "Y")) # None
```

**Why is the first discovery shortest?** The queue always holds vertices in non-decreasing order of distance — at most two distinct values, `d` and `d + 1`. A vertex at distance `d + 1` can only be discovered
by a vertex at distance `d`, and every vertex at distance `d` is processed before any at distance `d + 1`. So a vertex is first reached through the shortest possible route. This argument **breaks when edges have
different costs**: then the fewest-*edges* path is not necessarily the cheapest, and
[Dijkstra's algorithm](shortest-path-algorithms.md) is needed.

### Everything Within `k` Steps

Stop expanding when the distance reaches `k` — "friends of friends" is `k = 2`:

```python
def within_steps(graph, start, k):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if distance[node] == k:
            continue                                # do not expand beyond k steps
        for neighbour in graph[node]:
            if neighbour not in distance:
                distance[neighbour] = distance[node] + 1
                queue.append(neighbour)
    return set(distance)

print(sorted(within_steps(graph, "A", 1)))          # ['A', 'B', 'C']
print(sorted(within_steps(graph, "A", 2)))          # ['A', 'B', 'C', 'D', 'E', 'F']
```

## 🧩 Connected Components

Starting a BFS from every vertex not yet seen discovers the graph piece by piece (for an undirected graph):

```python
def connected_components(graph):
    seen = set()
    components = []
    for start in graph:
        if start not in seen:
            component = bfs_order(graph, start)    # everything reachable from `start`
            seen.update(component)
            components.append(component)
    return components

islands = {0: [1], 1: [0, 2], 2: [1], 3: [4], 4: [3], 5: []}
print(connected_components(islands))                # [[0, 1, 2], [3, 4], [5]]
```

Each vertex and edge is processed once overall: still **O(V + E)**.

## 🎨 Bipartite Graphs (Two-Colouring)

A graph is **bipartite** if its vertices can be split into two groups with every edge going *between* the groups — like students and the clubs they join, or any "two teams, no conflicts inside a team" problem. BFS colours
the start vertex 0, its neighbours 1, their neighbours 0, and so on. If an edge ever joins two vertices of the *same* colour, the graph is not bipartite (it contains an odd-length cycle):

```python
def is_bipartite(graph):
    color = {}
    for start in graph:                            # cover every component
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbour in graph[node]:
                if neighbour not in color:
                    color[neighbour] = 1 - color[node]       # the opposite colour
                    queue.append(neighbour)
                elif color[neighbour] == color[node]:
                    return False                              # an edge inside one group
    return True

square = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [2, 0]}        # a 4-cycle: even, so bipartite
triangle = {0: [1, 2], 1: [0, 2], 2: [0, 1]}                 # a 3-cycle: odd, so not
print(is_bipartite(square), is_bipartite(triangle))           # True False
```

## 🗺️ BFS on a Grid: Shortest Path Through a Maze

A grid is an implicit graph ([graph-representation.md](graph-representation.md)): each open cell is a vertex, and its up/down/left/right neighbours are its edges. BFS gives the minimum number of steps:

```python
def maze_steps(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    distance = {start: 0}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            return distance[(r, c)]
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" and (nr, nc) not in distance:
                distance[(nr, nc)] = distance[(r, c)] + 1
                queue.append((nr, nc))
    return -1                                      # the goal cannot be reached

maze = [
    "S.#....",
    ".##.##.",
    "....#..",
    ".##...#",
    "...#..G",
]
print(maze_steps(maze, (0, 0), (4, 6)))           # 10
walled_off = ["S#G"]
print(maze_steps(walled_off, (0, 0), (0, 2)))      # -1
```

Cells are tuples `(row, column)`, which are hashable and so can be dictionary keys. The cost is **O(rows × cols)**, since each cell is queued at most once.

### Multi-Source BFS

Start the BFS from **several vertices at once** by queueing all of them at distance 0. The ripples then spread from every source simultaneously, so each cell's distance is to its *nearest* source. For example,
the distance from every cell of a grid to the nearest cell containing `0`:

```python
def distance_to_nearest_zero(grid):
    rows, cols = len(grid), len(grid[0])
    distance = [[None] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                distance[r][c] = 0
                queue.append((r, c))                # every zero is a source
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and distance[nr][nc] is None:
                distance[nr][nc] = distance[r][c] + 1
                queue.append((nr, nc))
    return distance

for row in distance_to_nearest_zero([[0, 1, 1], [1, 1, 1], [1, 1, 0]]):
    print(row)
```

```text
[0, 1, 2]
[1, 2, 1]
[2, 1, 0]
```

Running one BFS per source would cost O(sources × cells); the multi-source version is a single O(cells) pass. The same idea spreads fire, rot, or a signal through a grid.

## ✅ Verification

BFS was checked on thousands of random graphs against independent methods: **Floyd-Warshall** (a different shortest-path algorithm, see [shortest-path-algorithms.md](shortest-path-algorithms.md)) for distances,
**union-find** for components, **trying every possible 2-colouring** for bipartiteness, and a **relaxation** algorithm (repeatedly improving distances until nothing changes) for the maze:

```python
import itertools
import random

random.seed(2)

def random_graph(n, directed):
    graph = {v: [] for v in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < 0.25 and (directed or u < v):
                graph[u].append(v)
                if not directed:
                    graph[v].append(u)
    return graph

def floyd_warshall_hops(graph):
    inf = float("inf")
    n = len(graph)
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for u in graph:
        for v in graph[u]:
            d[u][v] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d

def union_find_components(graph):
    parent = list(graph)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u in graph:
        for v in graph[u]:
            parent[find(u)] = find(v)
    groups = {}
    for v in graph:
        groups.setdefault(find(v), set()).add(v)
    return {frozenset(g) for g in groups.values()}

def brute_force_bipartite(graph):
    for colouring in itertools.product((0, 1), repeat=len(graph)):
        if all(colouring[u] != colouring[v] for u in graph for v in graph[u]):
            return True
    return False

for _ in range(1500):
    directed = random.random() < 0.5
    g = random_graph(random.randint(1, 7), directed)
    d = floyd_warshall_hops(g)
    for start in g:
        distance, parent = bfs(g, start)
        assert distance == {v: d[start][v] for v in g if d[start][v] != float("inf")}
        assert set(bfs_order(g, start)) == set(distance)
        for goal in g:
            path = shortest_path(g, start, goal)
            if goal in distance:
                assert path[0] == start and path[-1] == goal and len(path) == distance[goal] + 1
                assert all(b in g[a] for a, b in zip(path, path[1:]))        # every step is a real edge
            else:
                assert path is None
        for k in range(4):
            assert within_steps(g, start, k) == {v for v in g if d[start][v] <= k}
    if not directed:
        assert {frozenset(c) for c in connected_components(g)} == union_find_components(g)
        assert is_bipartite(g) == brute_force_bipartite(g)

def relaxation_distances(maze, start):
    rows, cols = len(maze), len(maze[0])
    best = {start: 0}
    changed = True
    while changed:
        changed = False
        for (r, c), steps in list(best.items()):
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" and best.get((nr, nc), 10**9) > steps + 1:
                    best[(nr, nc)] = steps + 1
                    changed = True
    return best

for _ in range(1500):
    rows, cols = random.randint(1, 6), random.randint(1, 6)
    maze = ["".join("#" if random.random() < 0.3 else "." for _ in range(cols)) for _ in range(rows)]
    maze[0] = "." + maze[0][1:]
    reference = relaxation_distances(maze, (0, 0))
    goal = (random.randrange(rows), random.randrange(cols))
    assert maze_steps(maze, (0, 0), goal) == reference.get(goal, -1) if maze[goal[0]][goal[1]] != "#" else True

    grid = [[random.choice([0, 1, 1]) for _ in range(cols)] for _ in range(rows)]
    zeros = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    if zeros:
        expected = [[min(abs(r - zr) + abs(c - zc) for zr, zc in zeros) for c in range(cols)] for r in range(rows)]
        assert distance_to_nearest_zero(grid) == expected
print("BFS agrees with Floyd-Warshall, union-find, brute-force colouring, and relaxation on 3,000 random inputs")
```

```text
BFS agrees with Floyd-Warshall, union-find, brute-force colouring, and relaxation on 3,000 random inputs
```

## 🧠 When to Use BFS

| Situation | BFS? |
|-----------|------|
| Fewest edges / moves / hops between two vertices | **Yes** |
| All vertices within `k` steps | **Yes** (stop at depth `k`) |
| Edges have different costs | No — use [Dijkstra](shortest-path-algorithms.md) |
| Does *any* path exist, or what is the structure (cycles, order)? | BFS works, but [DFS](depth-first-search.md) is usually simpler |
| Memory is tight and the graph is wide | Careful: the queue can hold a whole level (see [tree-traversal.md](../trees/tree-traversal.md)) |

## Common Mistakes

- **Marking visited on dequeue instead of on enqueue**, which queues vertices many times and can turn O(V + E) into O(V²) work.
- **Using a list as the queue** with `pop(0)` (O(n) per pop). Use `collections.deque`.
- **Using BFS distances on a weighted graph** as if they were costs.
- **Starting from one vertex and assuming the graph is connected**; loop over all vertices for components.
- **Forgetting the reverse edge** when building an undirected graph.
- **Reconstructing the path without parent links**, or building the path forward instead of backward from the goal.
- **Letting a grid BFS walk off the edge** or through walls — check bounds and obstacles before enqueueing.

## ➡️ Next

Continue to [depth-first-search.md](depth-first-search.md) to explore the other way — as deep as possible before backing up — and to learn cycle detection and topological sorting.
