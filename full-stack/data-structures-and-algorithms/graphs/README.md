# 🕸️ Graphs

## 📚 Overview

A **graph** is a set of things (vertices) and the connections between them (edges): road maps, social networks, the web, course prerequisites, computer networks, and the hidden state spaces of puzzles and games. It is the most general data structure in
this domain — a tree is a graph with strict extra rules — and a small set of algorithms answers an astonishing range of questions about it: Can I get from here to there? What is the fewest-step or cheapest route? Is there a cycle? What order respects the
dependencies? How do I connect everything as cheaply as possible?

This module covers graph vocabulary and the counting facts behind algorithm costs; how to store a graph (and when not to store it at all); breadth-first and depth-first search; the shortest-path family — Dijkstra, Bellman-Ford, Floyd-Warshall, and the DAG special case; and
union-find with minimum spanning trees and four applied problems. Every code example was run on CPython 3.9. The algorithms were cross-checked against each other and against independent definitions on thousands of random graphs — distances against Floyd-Warshall,
cycle detection against reachability closures, minimum spanning trees against exhaustive search — and the benchmarks are real measurements.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Use graph vocabulary precisely (directed, weighted, degree, path, cycle, component, DAG) and recognize a graph hidden inside a problem, including implicit graphs such as grids and word puzzles.
- Choose between an adjacency list, adjacency matrix, and edge list, and justify the choice with space and time costs for sparse and dense graphs.
- Implement BFS and use it for shortest paths in unweighted graphs, connected components, bipartite checks, grid mazes, and multi-source searches; explain why vertices are marked when enqueued.
- Implement DFS recursively and iteratively, detect cycles in undirected and directed graphs (the three-colour method), produce topological orders two ways, and count islands.
- Choose and implement the right shortest-path algorithm — BFS, Dijkstra, Bellman-Ford, Floyd-Warshall, or DAG relaxation — and explain exactly why Dijkstra fails with negative weights.
- Use union-find with union by size and path compression, build minimum spanning trees with Kruskal's and Prim's algorithms, and solve network-delay, limited-stops, and word-ladder problems.

## 📋 Prerequisites

- [Trees](../trees/README.md) — graphs generalize trees; BFS and DFS generalize level-order and depth-first traversal.
- [Stacks and Queues](../stacks-and-queues/README.md) — DFS uses a stack, BFS uses a queue.
- [Heaps and Priority Queues](../heaps-and-priority-queues/README.md) — Dijkstra's and Prim's algorithms use a priority queue.
- [Hashing](../hashing/README.md) — dictionaries and sets underpin visited sets and adjacency lists.
- [Recursion](../recursion/README.md) — recursive DFS and backtracking.
- [Time and Space Complexity](../time-and-space-complexity/README.md) — costs are stated in terms of both V and E.
- Basic Python reading ability — the examples use Python classes, dictionaries, and `heapq`.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [graph-fundamentals.md](graph-fundamentals.md) | Vocabulary, modelling real problems as graphs, and the handshake lemma, edge bounds, and tree test verified on random graphs |
| [graph-representation.md](graph-representation.md) | Adjacency lists, matrices, and edge lists; a reusable `Graph` class; implicit grid graphs; measured memory and scan costs |
| [breadth-first-search.md](breadth-first-search.md) | Level-by-level search: shortest paths, components, bipartite colouring, maze solving, multi-source BFS; why to mark visited on enqueue |
| [depth-first-search.md](depth-first-search.md) | Recursive and iterative DFS, discovery/finish times, cycle detection, two topological sorts, islands, and backtracking |
| [shortest-path-algorithms.md](shortest-path-algorithms.md) | Dijkstra (with a scaling measurement), why negative weights break it, Bellman-Ford, Floyd-Warshall, and DAG shortest paths, cross-validated |
| [graph-problems.md](graph-problems.md) | Union-find, minimum spanning trees (Kruskal and Prim), network delay, cheapest flights with limited stops, and word ladder; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [breadth-first-search.md](breadth-first-search.md), [depth-first-search.md](depth-first-search.md), and [shortest-path-algorithms.md](shortest-path-algorithms.md) if you are preparing for coding interviews: BFS/DFS traversal, cycle detection, topological sort, grid
problems ("number of islands", mazes), and Dijkstra are among the most frequently asked topics, and explaining *why* Dijkstra needs non-negative weights, or why BFS marks vertices on enqueue, is a common follow-up.

**Skim** [graph-fundamentals.md](graph-fundamentals.md) and [graph-representation.md](graph-representation.md) if you already know the vocabulary and adjacency lists — but note the density discussion and the memory measurement, which justify why sparse graphs use lists.
Treat [graph-problems.md](graph-problems.md) as a reference for union-find and minimum spanning trees, and read it fully if you want to see how the earlier tools combine on applied problems.

## 🧠 Knowledge Check

<details>
<summary>Why does a directed graph need a three-colour (white/gray/black) cycle test, when an undirected graph only needs "have I seen this vertex before (other than my parent)?"</summary>

In a directed graph, reaching an already-visited vertex does not imply a cycle: in the "diamond" `A → B → D` and `A → C → D`, the vertex `D` is reached twice, but you can never get back to `A`. A directed cycle exists only when an edge
points to a vertex that is **still on the current DFS path** (an ancestor that has not finished). Colouring vertices gray while they are on the path, and black once fully explored, distinguishes the two cases: an edge to a gray vertex is a cycle; an edge to a black vertex
is harmless. In an undirected graph every edge can be walked both ways, so any second route to a visited vertex (excluding the edge you arrived by) must close a cycle. See [depth-first-search.md](depth-first-search.md).

</details>

<details>
<summary>In Dijkstra's algorithm, why does a negative edge weight make the answer wrong, and which algorithm do you use instead?</summary>

Dijkstra finalizes the closest unfinished vertex and never revisits it, trusting that any other route to it would have to pass through a vertex at least as far away and then add a non-negative amount. With a negative edge, a longer-looking route can still end up cheaper:
in `S → A (2)`, `S → B (3)`, `B → A (−2)`, Dijkstra finalizes `A` at 2 before examining `B`, and every vertex reached through `A` keeps a stale distance (the cheaper route through `B` gives `A = 1`). Use **Bellman-Ford**, which relaxes every edge `V − 1` times
and can also detect negative cycles, or Floyd-Warshall for all pairs. See [shortest-path-algorithms.md](shortest-path-algorithms.md).

</details>

## 📚 References

- [Wikipedia: Graph (discrete mathematics)](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)), [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search), [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search), and [Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting) — definitions and analysis.
- [Wikipedia: Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm), [Bellman–Ford algorithm](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm), and [Floyd–Warshall algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm) — the shortest-path family, including applications such as routing protocols.
- [Wikipedia: Minimum spanning tree](https://en.wikipedia.org/wiki/Minimum_spanning_tree) and [Disjoint-set data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) — Kruskal's and Prim's algorithms; union by size, path compression, and the inverse-Ackermann bound.
- [W3Schools: DSA Graphs](https://www.w3schools.com/dsa/dsa_theory_graphs.php), [Graph Implementation](https://www.w3schools.com/dsa/dsa_data_graphs_implementation.php), [Traversal](https://www.w3schools.com/dsa/dsa_algo_graphs_traversal.php), [Cycle Detection](https://www.w3schools.com/dsa/dsa_algo_graphs_cycledetection.php), [Dijkstra](https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php), [Bellman-Ford](https://www.w3schools.com/dsa/dsa_algo_graphs_bellmanford.php), [Kruskal](https://www.w3schools.com/dsa/dsa_algo_mst_kruskal.php), and [Prim](https://www.w3schools.com/dsa/dsa_algo_mst_prim.php) — illustrated beginner introductions.
- [GeeksforGeeks: Graph Data Structure](https://www.geeksforgeeks.org/dsa/graph-data-structure-and-algorithms/), [BFS](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/), [DFS](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/), and [Dijkstra's Algorithm](https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/) — overviews and practice problems.
- [Python docs: `heapq`](https://docs.python.org/3/library/heapq.html) and [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) — the priority queue and queue used throughout.

## ➡️ Continue Your Learning Path

Continue to the Sorting Algorithms module, the next module in this domain, where the focus moves from connecting data to ordering it — and where the heap, divide-and-conquer recursion, and comparison-counting ideas from earlier modules reappear.
