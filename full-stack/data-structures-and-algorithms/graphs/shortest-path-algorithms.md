# 🛣️ Shortest-Path Algorithms

## The Cheapest Route, Not Just the Fewest Hops

[Breadth-first search](breadth-first-search.md) finds the path with the fewest *edges*. Real networks attach a **cost** to each edge — distance, travel time, price, latency — and the cheapest path is often not the one with
the fewest edges: a two-stop flight can cost less than a direct one. Finding it is the **shortest-path problem**, and the algorithm to use depends on two questions:

1. *From one source to everywhere (single-source), or between every pair (all-pairs)?*
2. *Can edges have negative weights?* (A negative weight might be a discount, a refund, or an energy gain.)

| Algorithm | Solves | Negative weights? | Time |
|-----------|--------|-------------------|------|
| BFS ([breadth-first-search.md](breadth-first-search.md)) | Single-source, all edges cost 1 | — | O(V + E) |
| **Dijkstra** | Single-source | **No** | O((V + E) log V) with a heap |
| **Bellman-Ford** | Single-source | **Yes**; detects negative cycles | O(V · E) |
| **Floyd-Warshall** | All-pairs | **Yes**; detects negative cycles | O(V³) |
| Shortest paths on a DAG | Single-source, acyclic graphs | Yes | O(V + E) |

This file builds each of them, shows precisely how Dijkstra fails when a weight is negative, and verifies all of them against each other on thousands of random graphs. All outputs were produced by running the code
on CPython 3.9.

Weighted graphs are dictionaries mapping each vertex to a list of `(neighbour, weight)` pairs. The running example is the graph from [graph-representation.md](graph-representation.md):

```
        4
   A ─────── B
   │       ╱ │
 1 │    2╱   │ 5
   │   ╱     │
   C ─────── D
        3
```

```python
import heapq

graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("A", 4), ("C", 2), ("D", 5)],
    "C": [("A", 1), ("B", 2), ("D", 3)],
    "D": [("B", 5), ("C", 3)],
}
```

The direct road `A–B` costs 4, but going `A → C → B` costs only `1 + 2 = 3`: the cheapest route is not the one with the fewest edges.

## 🥇 Dijkstra's Algorithm (Non-Negative Weights)

Dijkstra's algorithm grows a set of vertices whose shortest distance is **final**, always finalizing the closest not-yet-finalized vertex next. It keeps a **tentative distance** for every vertex and a
[priority queue](../heaps-and-priority-queues/priority-queues.md) ordered by tentative distance:

1. Start with `dist[source] = 0` and everything else unknown (infinite).
2. Repeatedly take the vertex `u` with the **smallest tentative distance** that is not yet finalized. Its distance is now final.
3. **Relax** each edge `u → v` with weight `w`: if `dist[u] + w` is smaller than the current `dist[v]`, update `dist[v]` (and remember `u` as `v`'s parent).
4. Stop when no candidates remain.

```python
def dijkstra(graph, source):
    dist = {source: 0}
    parent = {source: None}
    done = set()                                       # vertices whose distance is final
    heap = [(0, source)]                               # (tentative distance, vertex)
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue                                   # a stale entry: u was already finalized with a smaller distance
        done.add(u)
        for v, w in graph[u]:
            if v in done:
                continue                               # a finalized distance never changes
            candidate = d + w
            if candidate < dist.get(v, float("inf")):
                dist[v] = candidate                    # found a cheaper route to v through u
                parent[v] = u
                heapq.heappush(heap, (candidate, v))   # push a new entry; the old one becomes stale
    return dist, parent

def path_to(parent, target):
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]

dist, parent = dijkstra(graph, "A")
print(dist)                                            # {'A': 0, 'B': 3, 'C': 1, 'D': 4}   — in the order vertices were first reached
print(path_to(parent, "B"), path_to(parent, "D"))      # ['A', 'C', 'B'] ['A', 'C', 'D']
```

The heap does not support "lower this entry's priority" efficiently, so, as in [priority-queues.md](../heaps-and-priority-queues/priority-queues.md), the code uses **lazy deletion**: it pushes a new `(smaller distance, vertex)` entry
and discards older entries for the same vertex when they surface (the `if u in done` check).

**Why is it correct?** When `u` is popped with distance `d`, any other route to `u` must leave the finalized region through some other vertex still in the heap — whose tentative distance is at least `d` — and
then add a non-negative amount. So no route can beat `d`. This argument needs **every weight to be non-negative**.

**Cost.** Each vertex is finalized once; each edge causes at most one push. With a binary heap each push and pop costs O(log), so the total is **O((V + E) log V)**. (Python's `heapq` needs the vertices to be comparable
when two heap entries have equal distances; for arbitrary vertex objects, put a counter between the distance and the vertex, as in [min-heap-and-max-heap.md](../heaps-and-priority-queues/min-heap-and-max-heap.md).)

### How Fast Is It? Dijkstra on Grids

A grid of `n × n` cells with random step costs from 1 to 9 has `V = n²` vertices and about `4V` directed edges. Timing Dijkstra from the top-left corner as the grid grows:

```python
import random
import time

def grid_graph(n, seed):
    rng = random.Random(seed)
    g = {}
    for r in range(n):
        for c in range(n):
            g[r * n + c] = [(rr * n + cc, rng.randint(1, 9))
                            for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
                            if 0 <= rr < n and 0 <= cc < n]
    return g

print(f"{'grid':>9} | {'vertices':>9} | {'edges':>9} | {'Dijkstra (ms)':>13} | {'ms per 1000 vertices':>20}")
for n in (50, 100, 200, 400):
    g = grid_graph(n, 1)
    edges = sum(len(v) for v in g.values())
    start = time.perf_counter()
    dist, _ = dijkstra(g, 0)
    elapsed = (time.perf_counter() - start) * 1000
    assert len(dist) == n * n
    print(f"{n:>4} x {n:<3}| {n * n:>9,} | {edges:>9,} | {elapsed:>13.1f} | {elapsed / (n * n / 1000):>20.2f}")
```

Output:

```
     grid |  vertices |     edges | Dijkstra (ms) | ms per 1000 vertices
  50 x 50 |     2,500 |     9,800 |           2.2 |                 0.87
 100 x 100|    10,000 |    39,600 |          10.4 |                 1.04
 200 x 200|    40,000 |   159,200 |          42.0 |                 1.05
 400 x 400|   160,000 |   638,400 |         183.7 |                 1.15
```

Quadrupling the number of vertices roughly quadruples the time (the cost per thousand vertices grows only slowly), as the near-linear `(V + E) log V` bound predicts. This is quick enough for graphs with hundreds of
thousands of vertices, even in pure Python.

### Where Dijkstra Fails: Negative Weights

Dijkstra finalizes a vertex the moment it is popped, trusting that nothing can improve it later. A negative edge breaks that trust. In this graph the route `S → B → A` costs `3 + (−2) = 1`, cheaper than
the direct `S → A` at cost 2 — but Dijkstra finalizes `A` at distance 2 *before* it ever looks at `B`, and then `T` (reached through `A`) is stuck with the wrong distance:

```python
negative = {
    "S": [("A", 2), ("B", 3)],
    "A": [("T", 2)],
    "B": [("A", -2)],
    "T": [],
}
dist, _ = dijkstra(negative, "S")
print(dist["A"], dist["T"])                 # 2 4        — Dijkstra's (wrong) answer
```

The true shortest distances are `A = 1` (via `B`) and `T = 3`. The next algorithm gets them right.

## 🔁 Bellman-Ford (Negative Weights Allowed)

Bellman-Ford drops the cleverness for a brute-force guarantee. **A shortest path never needs more than `V − 1` edges** (a path with more edges would repeat a vertex, forming a cycle that cannot help unless it is negative). So
relax *every* edge, `V − 1` times: after round `k`, every vertex whose shortest path uses at most `k` edges has its correct distance.

```python
def bellman_ford(vertices, edges, source):
    """edges: list of (u, v, w), directed. Returns (dist, parent), or (None, None) if a negative cycle is reachable."""
    inf = float("inf")
    dist = {v: inf for v in vertices}
    parent = {v: None for v in vertices}
    dist[source] = 0
    for _ in range(len(vertices) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break                                       # nothing improved: the distances are final
    for u, v, w in edges:                               # one more round: an improvement now means a negative cycle
        if dist[u] != inf and dist[u] + w < dist[v]:
            return None, None
    return dist, parent

vertices = ["S", "A", "B", "T"]
edge_list = [(u, v, w) for u, nbrs in negative.items() for v, w in nbrs]
dist, parent = bellman_ford(vertices, edge_list, "S")
print(dist)                                             # {'S': 0, 'A': 1, 'B': 3, 'T': 3}
print(path_to(parent, "T"))                             # ['S', 'B', 'A', 'T']

cycle_edges = [("X", "Y", 1), ("Y", "Z", -3), ("Z", "X", 1)]     # the cycle costs 1 - 3 + 1 = -1 each lap
print(bellman_ford(["X", "Y", "Z"], cycle_edges, "X"))          # (None, None)
```

If the extra `V`-th round still finds an improvement, the graph has a **negative cycle** reachable from the source: going around it again and again lowers the total without limit, so "shortest" has no meaning. Bellman-Ford
reports it (`None`) instead of returning nonsense. Total cost: `V − 1` rounds over `E` edges, **O(V · E)** — slower than Dijkstra, but correct for negative weights and able to detect negative cycles. (An *undirected* edge
with negative weight is itself a negative cycle — walk back and forth along it — so negative weights make sense only on directed edges.)

## 🌐 Floyd-Warshall (All Pairs)

To get the shortest distance between *every* pair of vertices, one could run Dijkstra from every source. Floyd-Warshall instead uses dynamic programming over the *intermediate vertices allowed*. Let `d[i][j]` be the best
distance found from `i` to `j`. For each vertex `k` in turn, ask: *does going through `k` improve any pair?* — that is, is `d[i][k] + d[k][j] < d[i][j]`? After considering all `k`, every pair holds its true shortest distance.

```python
def floyd_warshall(n, edges):
    """Vertices 0..n-1; edges: list of (u, v, w). Returns the n x n matrix of shortest distances."""
    inf = float("inf")
    d = [[inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)                        # keep the cheapest of any parallel edges
    for k in range(n):                                   # allow vertex k as an intermediate stop
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d

edges_a = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 3), (1, 0, 4), (2, 0, 1), (2, 1, 2), (3, 1, 5), (3, 2, 3)]
for row in floyd_warshall(4, edges_a):
    print(row)
```

```text
[0, 3, 1, 4]
[3, 0, 2, 5]
[1, 2, 0, 3]
[4, 5, 3, 0]
```

Three nested loops over `V` give **O(V³) time** and O(V²) space — practical for a few hundred vertices, hopeless for millions. It is the right tool when you need many or all pairs, when `V` is small, or when you
want something very short to code. A negative value on the diagonal (`d[i][i] < 0`) signals a negative cycle through vertex `i`. The loop order matters: the **intermediate vertex `k` must be the outermost loop**.

## 🧱 A Special Case: Shortest Paths in a DAG

If the graph has no directed cycles, there is a linear-time method that even accepts negative weights: process the vertices in [topological order](depth-first-search.md), relaxing each vertex's outgoing edges once. By the time
a vertex is processed, everything that can lead to it has already been processed, so its distance is final.

```python
from collections import deque

def dag_shortest_paths(graph, source):
    indegree = {v: 0 for v in graph}
    for u in graph:
        for v, _ in graph[u]:
            indegree[v] += 1
    ready = deque(v for v in graph if indegree[v] == 0)
    order = []
    while ready:                                         # Kahn's algorithm: a topological order
        u = ready.popleft()
        order.append(u)
        for v, _ in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
    dist = {v: float("inf") for v in graph}
    dist[source] = 0
    for u in order:
        if dist[u] != float("inf"):
            for v, w in graph[u]:
                dist[v] = min(dist[v], dist[u] + w)      # relax each edge exactly once
    return dist

tasks = {"start": [("a", 5), ("b", 3)], "a": [("c", 6), ("d", 2)], "b": [("c", 2), ("d", 7)], "c": [("end", 4)], "d": [("end", 1)], "end": []}
print(dag_shortest_paths(tasks, "start")["end"])         # 8
```

**O(V + E)**. The same code with `max` in place of `min` finds the *longest* path in a DAG — the length of the critical path in a project schedule (impossible in general graphs, but easy in a DAG).

## ✅ Verification: Cross-Checking the Algorithms

The three general algorithms solve overlapping problems, which allows them to check each other. On thousands of random graphs: Dijkstra, Bellman-Ford, and Floyd-Warshall must agree whenever weights are non-negative;
Bellman-Ford and Floyd-Warshall must agree when weights include negatives but no negative cycle exists (such graphs are produced by adding *potentials*, a standard trick that cannot create a negative cycle); every
reconstructed path must be real and have exactly the reported cost; negative-cycle detection must match Floyd-Warshall's diagonal; and the DAG method must match Bellman-Ford.

```python
random.seed(3)
INF = float("inf")

def random_weighted_digraph(n, p, low, high):
    edges = [(u, v, random.randint(low, high)) for u in range(n) for v in range(n) if u != v and random.random() < p]
    graph = {u: [] for u in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
    return graph, edges

def path_cost(graph, path):
    return sum(min(w for x, w in graph[a] if x == b) for a, b in zip(path, path[1:]))

def reachable_from(graph, source):
    seen, stack = {source}, [source]
    while stack:
        u = stack.pop()
        for v, _ in graph[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen

dijkstra_wrong = 0
for _ in range(2500):
    n = random.randint(1, 7)

    # 1. non-negative weights: all three algorithms agree
    graph, edges = random_weighted_digraph(n, random.choice([0.2, 0.4, 0.7]), 0, 9)
    fw = floyd_warshall(n, edges)
    for s in range(n):
        dj, parent = dijkstra(graph, s)
        bf, _ = bellman_ford(list(range(n)), edges, s)
        assert dj == {v: bf[v] for v in range(n) if bf[v] != INF} == {v: fw[s][v] for v in range(n) if fw[s][v] != INF}
        for target in dj:
            p = path_to(parent, target)
            assert p[0] == s and p[-1] == target and path_cost(graph, p) == dj[target]

    # 2. negative edges but no negative cycle (built with potentials): Bellman-Ford = Floyd-Warshall; Dijkstra may be wrong
    base, _ = random_weighted_digraph(n, 0.5, 0, 9)
    potential = [random.randint(-6, 6) for _ in range(n)]
    graph = {u: [(v, w + potential[u] - potential[v]) for v, w in nbrs] for u, nbrs in base.items()}
    edges = [(u, v, w) for u, nbrs in graph.items() for v, w in nbrs]
    fw = floyd_warshall(n, edges)
    assert all(fw[i][i] == 0 for i in range(n))                          # no negative cycle by construction
    for s in range(n):
        bf, parent = bellman_ford(list(range(n)), edges, s)
        assert bf is not None and {v: bf[v] for v in range(n)} == {v: fw[s][v] for v in range(n)}
        for target in range(n):
            if bf[target] != INF:
                p = path_to(parent, target)
                assert path_cost(graph, p) == bf[target]
        dj, _ = dijkstra(graph, s)
        if dj != {v: bf[v] for v in range(n) if bf[v] != INF}:
            dijkstra_wrong += 1

    # 3. arbitrary weights: negative-cycle detection agrees with Floyd-Warshall's diagonal
    graph, edges = random_weighted_digraph(n, 0.5, -3, 6)
    fw = floyd_warshall(n, edges)
    for s in range(n):
        reachable = reachable_from(graph, s)
        negative_cycle_reachable = any(fw[v][v] < 0 for v in reachable)
        bf, _ = bellman_ford(list(range(n)), edges, s)
        assert (bf is None) == negative_cycle_reachable

    # 4. DAGs with negative weights: the topological-order method matches Bellman-Ford
    dag = {u: [(v, random.randint(-4, 9)) for v in range(u + 1, n) if random.random() < 0.5] for u in range(n)}
    dag_edges = [(u, v, w) for u, nbrs in dag.items() for v, w in nbrs]
    bf, _ = bellman_ford(list(range(n)), dag_edges, 0)
    assert dag_shortest_paths(dag, 0) == bf
print(f"Dijkstra, Bellman-Ford, Floyd-Warshall and the DAG method agree on 2,500 random graphs of each kind")
print(f"Dijkstra returned a wrong answer for {dijkstra_wrong} (graph, source) combinations that had negative edges, as predicted")
```

```text
Dijkstra, Bellman-Ford, Floyd-Warshall and the DAG method agree on 2,500 random graphs of each kind
Dijkstra returned a wrong answer for 1489 (graph, source) combinations that had negative edges, as predicted
```

## 🧭 Choosing an Algorithm

| Situation | Use |
|-----------|-----|
| Unweighted graph (or all weights equal) | **BFS** |
| Non-negative weights, one source | **Dijkstra** |
| Negative weights possible, one source; or detect a negative cycle | **Bellman-Ford** |
| Distances between all pairs; small `V` | **Floyd-Warshall** |
| The graph is a DAG | Topological-order relaxation (linear time) |
| Weights are only 0 and 1 | A double-ended queue (0-1 BFS) — faster than Dijkstra |
| One source and one target, with a good estimate of the remaining distance | A* (Dijkstra guided by a heuristic) |

Real systems add refinements — bidirectional search, precomputed hubs, and heuristics — but they are built on exactly these ideas. Network routing protocols such as OSPF and IS-IS are a classic application of shortest-path algorithms ([Wikipedia: Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)).

## Common Mistakes

- **Using Dijkstra with negative weights.** It silently returns wrong answers; use Bellman-Ford.
- **Using BFS for a weighted graph.** BFS minimises edges, not cost.
- **Forgetting that Dijkstra's heap holds stale entries**; skip an entry whose vertex is already finalized.
- **Treating "no path" as a number** — keep unreachable vertices out of the result or use infinity, and never add to infinity unguarded in languages where it overflows.
- **Putting the Floyd-Warshall intermediate vertex `k` in the inner loop**, which gives wrong results.
- **Ignoring negative cycles**: Bellman-Ford's extra round exists to detect them; skipping it can return distances that mean nothing.
- **Treating an undirected negative edge as acceptable**; it is a negative cycle.
- **Rebuilding the path from `dist` alone** — store a parent for each vertex.

## ➡️ Next

Continue to [graph-problems.md](graph-problems.md) to apply these algorithms and the traversals to classic problems — network delay, cheapest flights, minimum spanning trees, and union-find — and finish the module.
