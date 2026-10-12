# 🧩 Common Graph Problems

## Putting the Graph Toolkit to Work

The earlier files each taught one tool: [BFS](breadth-first-search.md) for fewest steps, [DFS](depth-first-search.md) for structure, and [Dijkstra, Bellman-Ford, and Floyd-Warshall](shortest-path-algorithms.md)
for cheapest routes. Real problems rarely announce which tool they need. They arrive dressed as *delays in a network*, *flights with limited stops*, *word puzzles*, or *connecting cities with the least cable* — and the skill is
to **see the graph hidden inside**, decide what the vertices and edges are, and pick the matching algorithm. This file adds one new data structure, **union-find**, and one new algorithm family, **minimum spanning trees**, and then works
through four applications. Every function was tested against a brute-force or independent version on thousands of random inputs (the verification block is near the end). All outputs were produced by running the code on CPython 3.9.

```python
import heapq
import random
from collections import deque
```

## 🧱 Union-Find (Disjoint Sets)

Many problems ask: *are these two things already connected?* and *connect them.* A **union-find** structure (also called a disjoint-set union) maintains a collection of non-overlapping groups and supports two operations
very quickly:

- **`find(x)`** — which group is `x` in? (Each group is identified by a *representative*, its root.)
- **`union(a, b)`** — merge the groups of `a` and `b`.

Each group is a small tree stored in a parent array: every element points to its parent, and the root points to itself. Two optimizations make the trees stay shallow:

- **Union by size:** when merging, attach the *smaller* tree under the *larger* one.
- **Path compression:** during `find`, repoint every element on the way up directly at the root, so later finds are shorter.

```python
class UnionFind:
    def __init__(self, n):
        self._parent = list(range(n))                    # every element starts as its own group
        self._size = [1] * n
        self.components = n
        self.steps = 0                                   # parent pointers followed so far (for measuring only)

    def find(self, x):
        root = x
        while self._parent[root] != root:                # walk up to the root
            root = self._parent[root]
            self.steps += 1
        while self._parent[x] != root:                   # path compression: point everything on the path at the root
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                 # already in the same group
        if self._size[ra] < self._size[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra                            # the smaller tree hangs under the larger one
        self._size[ra] += self._size[rb]
        self.components -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

uf = UnionFind(6)
print(uf.union(0, 1), uf.union(1, 2), uf.union(0, 2))     # True True False   — 0 and 2 were already connected
print(uf.connected(0, 2), uf.connected(0, 5), uf.components)     # True False 4
```

`union` returns `False` when the two elements were already in the same group — exactly the signal that adding an edge would create a **cycle**, which makes union-find the natural tool for cycle detection in undirected graphs and
for Kruskal's algorithm below.

### Do the Optimizations Matter? A Measurement

Without them, a chain of unions builds one long path and every `find` walks it. This comparison counts the parent pointers followed for `n` unions that join the elements in a chain `(0,1), (1,2), (2,3), …`, followed by a `find` on
every element, using a naive union-find (no size rule, no compression) and the class above:

```python
class NaiveUnionFind:
    def __init__(self, n):
        self._parent = list(range(n))
        self.steps = 0

    def find(self, x):
        while self._parent[x] != x:
            x = self._parent[x]
            self.steps += 1
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self._parent[ra] = rb                        # always hang the first root under the second

print(f"{'n':>6} | {'naive: parent pointers followed':>31} | {'optimized':>10}")
for n in (500, 1_000, 2_000, 4_000):
    naive, smart = NaiveUnionFind(n), UnionFind(n)
    for i in range(n - 1):
        naive.union(i, i + 1)
        smart.union(i, i + 1)
    for i in range(n):
        naive.find(i)
        smart.find(i)
    print(f"{n:>6,} | {naive.steps:>31,} | {smart.steps:>10,}")
```

```text
     n | naive: parent pointers followed |  optimized
   500 |                         124,750 |        997
 1,000 |                         499,500 |      1,997
 2,000 |                       1,999,000 |      3,997
 4,000 |                       7,998,000 |      7,997
```

The naive version's work **quadruples** when `n` doubles (it is quadratic, about `n²` pointer steps), while the optimized version stays linear. With both optimizations, the amortized cost per operation is
essentially constant — formally the *inverse Ackermann function*, which Wikipedia notes is 4 or less for any `n` that could actually be written down in the physical universe
([Disjoint-set data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)).

## 🧮 Problem 1: Counting Components, Valid Trees, and the Redundant Edge

Union-find answers a family of connectivity questions with almost no code:

```python
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components

def is_valid_tree(n, edges):                              # a tree: connected, with no cycle <=> exactly n - 1 edges and every union succeeds
    if len(edges) != n - 1:
        return False
    uf = UnionFind(n)
    return all(uf.union(u, v) for u, v in edges)

def redundant_connection(n, edges):                        # given a tree plus ONE extra edge, find the edge that closes the cycle
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return (u, v)                                  # the first edge whose endpoints were already connected
    return None

print(count_components(5, [(0, 1), (1, 2), (3, 4)]))                    # 2
print(is_valid_tree(5, [(0, 1), (0, 2), (0, 3), (1, 4)]))               # True
print(is_valid_tree(5, [(0, 1), (1, 2), (2, 3), (1, 3)]))               # False   — a cycle, and vertex 4 is cut off
print(redundant_connection(4, [(0, 1), (1, 2), (2, 3), (3, 1)]))        # (3, 1)
```

Each runs in about **O(E)** (times the near-constant union-find cost). The same code answers "number of provinces" and "friend circles" puzzles.

## 🌲 Problem 2: Minimum Spanning Tree

Suppose you must connect a set of towns with cable so that every town is reachable from every other, using the **least total cable**. The answer is a **minimum spanning tree (MST)**: a subset of edges that connects all vertices, contains no
cycle (so exactly `V − 1` edges), and has the smallest possible total weight. Two classic greedy algorithms find one; both rest on the same fact — the cheapest edge that crosses between any chosen set of vertices and the rest can always
be part of an MST.

### Kruskal's Algorithm: Sort the Edges

Consider edges from **cheapest to most expensive**; take an edge if it connects two vertices that are not yet connected (otherwise it would form a cycle). Union-find answers "not yet connected?" instantly:

```python
def kruskal(n, edges):
    """edges: list of (u, v, weight), undirected. Returns (total weight, chosen edges)."""
    uf = UnionFind(n)
    total, chosen = 0, []
    for u, v, w in sorted(edges, key=lambda edge: edge[2]):
        if uf.union(u, v):                                 # joins two separate groups: safe to keep
            total += w
            chosen.append((u, v, w))
    return total, chosen

towns = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 3)]
print(kruskal(4, towns))                                   # (6, [(0, 2, 1), (1, 2, 2), (2, 3, 3)])
```

On the running example (the graph from [graph-representation.md](graph-representation.md): A=0, B=1, C=2, D=3) the cheapest connection uses the edges of weight 1, 2, and 3 for a total of 6; the weight-4 edge
`A–B` would form a cycle (A and B are already connected through C), and the weight-5 edge `B–D` is also skipped. Sorting dominates: **O(E log E)**.

### Prim's Algorithm: Grow One Tree

Start from any vertex and repeatedly add the **cheapest edge leaving the tree built so far**, using a [priority queue](../heaps-and-priority-queues/priority-queues.md) to find it. It resembles Dijkstra, except that the key is the edge
weight, not the distance from the source:

```python
def prim(n, edges, start=0):
    adjacency = {u: [] for u in range(n)}
    for u, v, w in edges:
        adjacency[u].append((w, v))
        adjacency[v].append((w, u))
    in_tree = {start}
    heap = list(adjacency[start])                           # candidate edges leaving the tree: (weight, far endpoint)
    heapq.heapify(heap)
    total = 0
    while heap and len(in_tree) < n:
        w, v = heapq.heappop(heap)                          # the cheapest edge out of the tree
        if v in in_tree:
            continue                                        # stale: both ends are already in the tree
        in_tree.add(v)
        total += w
        for item in adjacency[v]:
            if item[1] not in in_tree:
                heapq.heappush(heap, item)
    return total if len(in_tree) == n else None             # None: the graph is not connected

print(prim(4, towns))                                       # 6
```

**O((V + E) log V)** with a binary heap. Prim tends to be preferable on dense graphs and Kruskal on sparse ones; both give the same total weight (the MST itself is unique only if all edge weights are distinct). A
test below compares both against an exhaustive search.

## 📡 Problem 3: Network Delay Time

*A signal starts at one node of a directed network; each link has a travel time. How long until every node has received it? Return -1 if some node is never reached.* The signal reaches each node by the fastest route, so the time to
reach everyone is the **largest shortest-path distance** from the source — a direct use of Dijkstra:

```python
def dijkstra_distances(graph, source):
    dist = {source: 0}
    heap = [(0, source)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in graph[u]:
            if v not in done and d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist

def network_delay_time(times, n, source):                    # nodes are numbered 1..n; times: (u, v, travel time)
    graph = {node: [] for node in range(1, n + 1)}
    for u, v, w in times:
        graph[u].append((v, w))
    dist = dijkstra_distances(graph, source)
    return max(dist.values()) if len(dist) == n else -1       # everyone reached? then the slowest arrival; otherwise -1

print(network_delay_time([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2))      # 2
print(network_delay_time([(1, 2, 1)], 2, 2))                            # -1   — node 1 can never be reached
```

## ✈️ Problem 4: Cheapest Flight With at Most `k` Stops

*Given flights `(from, to, price)`, find the cheapest trip from `src` to `dst` using at most `k` intermediate stops.* Plain Dijkstra does not respect a limit on the number of edges, but **Bellman-Ford's rounds** do: after round `r`, the
distance array holds the best cost using **at most `r` edges**. A trip with `k` stops has at most `k + 1` flights, so run exactly `k + 1` rounds — each computed from a *copy* of the previous round, so a single round cannot chain two flights:

```python
def cheapest_flight(n, flights, src, dst, k):
    inf = float("inf")
    cost = [inf] * n
    cost[src] = 0
    for _ in range(k + 1):                                    # at most k + 1 flights
        next_cost = cost[:]                                    # build this round from the previous round only
        for u, v, price in flights:
            if cost[u] != inf and cost[u] + price < next_cost[v]:
                next_cost[v] = cost[u] + price
        cost = next_cost
    return -1 if cost[dst] == inf else cost[dst]

flights = [(0, 1, 100), (1, 2, 100), (0, 2, 500)]
print(cheapest_flight(3, flights, 0, 2, 1))                    # 200   — via city 1 (one stop)
print(cheapest_flight(3, flights, 0, 2, 0))                    # 500   — direct only
```

Updating `cost` in place during a round would let the algorithm use several flights in one round and ignore the stop limit — the reason for the `next_cost` copy. Time **O(k · E)**.

## 🔤 Problem 5: Word Ladder (An Implicit Graph)

*Transform a start word into an end word, changing one letter at a time, with every intermediate word in a given list. What is the length of the shortest transformation sequence (counting both words)?* The words are vertices; two words are joined if they differ
in one letter. Fewest steps in an unweighted graph is **BFS**. To find neighbours quickly, bucket each word under every wildcard pattern (`hot` → `*ot`, `h*t`, `ho*`): two words are neighbours exactly when they share a pattern.

```python
def ladder_length(begin, end, words):
    word_set = set(words)
    if end not in word_set:
        return 0
    buckets = {}                                              # wildcard pattern -> words that match it
    for word in word_set | {begin}:
        for i in range(len(word)):
            buckets.setdefault(word[:i] + "*" + word[i + 1:], []).append(word)
    queue = deque([(begin, 1)])
    seen = {begin}
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            for neighbour in buckets.get(word[:i] + "*" + word[i + 1:], []):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append((neighbour, steps + 1))
    return 0

print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))     # 5   — hit → hot → dot → dog → cog
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]))            # 0   — "cog" is not allowed
```

The graph is never built explicitly beyond the buckets. For `N` words of length `L` this costs about O(N · L²) (building each word's `L` patterns takes O(L) apiece).

## ✅ Verification

Every function was compared with an independent or exhaustive method on thousands of random inputs: union-find components against a breadth-first search; the tree test against its definition; the redundant edge by trying to remove edges from
the end; Kruskal and Prim against an **exhaustive search over every set of `V − 1` edges** for the true minimum; network delay against Floyd-Warshall; flights against exploring every route of up to `k + 1` flights; and word ladders against a
brute-force pairwise-adjacency BFS.

```python
from itertools import combinations

random.seed(21)
INF = float("inf")

def bfs_components(n, edges):
    adjacency = {v: [] for v in range(n)}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen, count = set(), 0
    for s in range(n):
        if s not in seen:
            count += 1
            stack = [s]
            seen.add(s)
            while stack:
                x = stack.pop()
                for y in adjacency[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
    return count

def is_spanning_tree(n, chosen):
    uf = UnionFind(n)
    return len(chosen) == n - 1 and all(uf.union(u, v) for u, v, _ in chosen)

def brute_force_mst(n, edges):
    return min(sum(w for _, _, w in subset) for subset in combinations(edges, n - 1) if is_spanning_tree(n, subset))

for _ in range(3000):
    n = random.randint(1, 7)
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    edges = random.sample(pairs, random.randint(0, len(pairs)))
    assert count_components(n, edges) == bfs_components(n, edges)

    tree_edges = [(random.randrange(i), i) for i in range(1, n)]              # a random tree on n vertices
    assert is_valid_tree(n, tree_edges)
    extra = random.choice([e for e in pairs if e not in tree_edges and (e[1], e[0]) not in tree_edges] or [None])
    if n >= 3 and extra is not None:
        with_extra = tree_edges + [extra]
        random.shuffle(with_extra)
        expected = next(e for e in reversed(with_extra) if is_valid_tree(n, [x for x in with_extra if x != e]))
        assert redundant_connection(n, with_extra) == expected
        assert not is_valid_tree(n, with_extra)

    # minimum spanning tree: a connected random weighted graph
    if n >= 2:
        pool = [e for e in pairs if e not in tree_edges]
        connected = tree_edges + random.sample(pool, min(random.randint(0, 3), len(pool)))
        weighted = [(u, v, random.randint(1, 9)) for u, v in connected]
        if len(weighted) <= 10:
            best = brute_force_mst(n, weighted)
            k_total, k_edges = kruskal(n, weighted)
            assert k_total == best == prim(n, weighted) and is_spanning_tree(n, k_edges)

    # network delay vs Floyd-Warshall (nodes 1..n)
    times = [(u + 1, v + 1, random.randint(1, 9)) for u in range(n) for v in range(n) if u != v and random.random() < 0.35]
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in times:
        d[u - 1][v - 1] = min(d[u - 1][v - 1], w)
    for k_ in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k_] + d[k_][j])
    source = random.randrange(n)
    slowest = max(d[source])
    assert network_delay_time(times, n, source + 1) == (-1 if slowest == INF else slowest)

    # cheapest flight with at most k stops vs exploring every route of up to k + 1 flights
    flights = [(u, v, random.randint(1, 9)) for u in range(n) for v in range(n) if u != v and random.random() < 0.4]
    src, dst, stops = random.randrange(n), random.randrange(n), random.randint(0, 3)

    def best_route(city, remaining):                       # cheapest cost from `city` to dst using at most `remaining` flights
        options = [0] if city == dst else []
        if remaining > 0:
            options += [price + best_route(v, remaining - 1) for u, v, price in flights if u == city]
        return min(options) if options else INF

    expected = best_route(src, stops + 1)
    assert cheapest_flight(n, flights, src, dst, stops) == (-1 if expected == INF else expected)

alphabet = "abc"
for _ in range(1500):
    length = random.randint(1, 3)
    words = list({"".join(random.choice(alphabet) for _ in range(length)) for _ in range(random.randint(1, 9))})
    begin = "".join(random.choice(alphabet) for _ in range(length))
    end = random.choice(words)
    neighbours = lambda a: [b for b in set(words) | {begin} if sum(x != y for x, y in zip(a, b)) == 1]
    expected, seen_, frontier, steps = 0, {begin}, [begin], 1
    while frontier:
        if end in frontier:
            expected = steps
            break
        frontier = list({nb for w in frontier for nb in neighbours(w) if nb not in seen_})
        seen_ |= set(frontier)
        steps += 1
    assert ladder_length(begin, end, words) == expected
print("union-find problems, MSTs, network delay, cheapest flights and word ladders agree with independent checks")
```

```text
union-find problems, MSTs, network delay, cheapest flights and word ladders agree with independent checks
```

## 🧭 Recognizing the Graph

| The problem says… | Model it as… | Use |
|-------------------|--------------|-----|
| "fewest moves / steps / transformations" | Unweighted graph (often implicit) | BFS |
| "can these be connected?" / "how many groups?" / "does adding this edge form a cycle?" | Undirected graph, connectivity | Union-find (or DFS/BFS) |
| "connect everything as cheaply as possible" | Weighted undirected graph | Minimum spanning tree (Kruskal or Prim) |
| "fastest/cheapest route", "how long until everyone receives it" | Weighted directed graph | Dijkstra (non-negative) or Bellman-Ford |
| "...with at most `k` stops/edges" | Bellman-Ford with `k + 1` rounds | Layered relaxation |
| "valid ordering given prerequisites"; "is there a cyclic dependency?" | DAG | Topological sort ([depth-first-search.md](depth-first-search.md)) |
| "split into two groups with no conflicts inside" | Bipartite check | BFS two-colouring |

## ⏱️ Costs

| Problem | Algorithm | Time |
|---------|-----------|------|
| Components, valid tree, redundant edge | Union-find | about O(E) |
| Minimum spanning tree | Kruskal / Prim | O(E log E) / O((V + E) log V) |
| Network delay time | Dijkstra | O((V + E) log V) |
| Cheapest flight, at most `k` stops | Layered Bellman-Ford | O(k · E) |
| Word ladder | BFS over wildcard buckets | about O(N · L²) |

## Common Mistakes

- **Not seeing the graph.** Ask: what are the vertices, what are the edges, are they weighted or directed, and is the graph given or implicit?
- **Using Dijkstra when an edge limit applies** ("at most `k` stops"); Dijkstra ignores edge counts.
- **Updating a Bellman-Ford round in place**, which lets one round chain several edges.
- **Forgetting that an MST needs a connected graph**; on a disconnected graph Kruskal returns a spanning *forest*.
- **Forgetting both optimizations in union-find**, turning near-constant operations into linear ones.
- **Checking a graph is a tree by edges only** (`n − 1` edges is necessary but not sufficient — it could be disconnected with a cycle).
- **Building an explicit graph for an implicit problem** (word ladders, puzzles), which can be enormous.
- **Returning the maximum shortest distance without checking that every node was reached** (network delay).

## Module Summary

The Graphs module generalized trees to arbitrary connections. [Graph Fundamentals](graph-fundamentals.md) defined the vocabulary — directed and weighted graphs, degree, paths, cycles, components, DAGs — and verified the counting facts that govern
algorithm costs. [Graph Representation](graph-representation.md) compared adjacency lists, matrices, and edge lists, measured their memory, and introduced implicit graphs such as grids. [Breadth-First Search](breadth-first-search.md) found
fewest-step paths, components, bipartite colourings, and maze routes with a queue. [Depth-First Search](depth-first-search.md) used a stack for cycle detection, topological sorting, and flood fill.
[Shortest-Path Algorithms](shortest-path-algorithms.md) added edge costs with Dijkstra, Bellman-Ford, and Floyd-Warshall, and showed exactly where Dijkstra fails. This file added union-find and minimum spanning trees and solved four
applied problems.

Carry these ideas forward:

- Choose the representation by density: adjacency lists for sparse graphs (almost always), matrices for dense ones or all-pairs work.
- Costs are stated in both `V` and `E`: BFS and DFS are O(V + E); Dijkstra is O((V + E) log V); Bellman-Ford is O(VE); Floyd-Warshall is O(V³).
- BFS for fewest edges, Dijkstra for non-negative costs, Bellman-Ford for negative costs or edge limits, DFS for structure (cycles, order, components).
- Union-find answers "connected yet?" in near-constant time, and powers Kruskal's algorithm.
- Many problems hide an implicit graph (grids, words, puzzle states): model first, then pick the algorithm.
- Dynamic programming, backtracking, and many scheduling problems later in this domain are graph problems in disguise.

## ➡️ Next

Continue to the Sorting Algorithms module, the next module in this domain, where the focus moves from connecting data to ordering it — and where the heap, the divide-and-conquer recursion, and the comparison-counting ideas from earlier modules
reappear.
