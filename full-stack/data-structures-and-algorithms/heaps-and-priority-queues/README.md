# 🏔️ Heaps and Priority Queues

## 📚 Overview

A **priority queue** serves items in order of importance rather than arrival, and a **heap** is the structure that implements it efficiently. A heap keeps only a *partial* order — every parent is no larger than
its children — which is enough to find the minimum in O(1) and to insert or remove items in O(log n), and cheap enough to live in a plain array with no pointers. Heaps power operating-system schedulers,
event simulations, "top k" queries, and the shortest-path algorithms that come next in this domain.

This module builds a heap from scratch (sift up, sift down, and the linear-time `heapify`), explains Python's `heapq` and how to get max-heap behaviour and sensible tie-breaking from it, compares priority-queue
implementations with measurements, builds a stable priority queue that supports priority updates, and solves eight classic problems — the k-th largest element, the k most frequent items, merging sorted lists, the
running median, and more. Every code example was run on CPython 3.9; the heap was tested against `heapq` and every problem against a brute-force version on thousands of random inputs, and the comparison counts and
timings are real measurements.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- State the heap property, store a complete binary tree in an array, and implement `push`, `pop`, and `heapify` with sift-up and sift-down.
- Explain why `heapify` is O(n), why building by repeated pushes can cost n log n, and why a heap's internal list is not sorted.
- Use `heapq` effectively — `heappush`, `heappop`, `heapify`, `heapreplace`, `heappushpop`, `nsmallest`, `nlargest`, `merge` — and know when `nsmallest` beats `sorted` and when it does not.
- Build a max-heap from a min-heap (negation or a reversed comparison), prioritize tuples safely with a tie-breaking counter, and avoid the dictionary-comparison `TypeError`.
- Compare priority-queue implementations by Big-O and by measurement, and implement a stable queue with priority updates and cancellation using lazy deletion.
- Recognize heap problems — top k, k-th largest, merge k sorted, running median, greedy "take the two smallest" — and give their O(n log k) or O(log n) costs.

## 📋 Prerequisites

- [Trees](../trees/README.md) — especially [binary trees](../trees/binary-trees.md) and their array representation.
- [Arrays](../arrays/README.md) — the list operations a heap is built from.
- [Binary Search Trees](../binary-search-trees/README.md) — the contrast between a full ordering (BST) and a partial ordering (heap).
- [Time and Space Complexity](../time-and-space-complexity/README.md) — amortized and average-case reasoning.
- Basic Python reading ability — the examples use Python classes, generators, and the `heapq` module.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [heap-fundamentals.md](heap-fundamentals.md) | The heap property, array storage, sift up and down, a `MinHeap` class, comparison counts for `heapify` versus pushes, and heap sort |
| [min-heap-and-max-heap.md](min-heap-and-max-heap.md) | The `heapq` API, `nsmallest` versus `sorted` (measured), max-heaps by negation or reversal, the tuple tie trap, and a tie-breaking counter |
| [priority-queues.md](priority-queues.md) | The abstract data type, four implementations compared, `queue.PriorityQueue`, a stable queue with priority updates, and two applications |
| [heap-problems.md](heap-problems.md) | Eight classic problems with brute-force verification; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [heap-problems.md](heap-problems.md) if you are preparing for coding interviews: "k-th largest", "top k frequent", "merge k sorted lists", and "median of a stream" are among the most common heap questions, and explaining why the
k *largest* use a min-heap is a frequent follow-up. Also read the lazy-deletion section of [priority-queues.md](priority-queues.md), which answers "how do you update a priority in a heap?".

**Skim** [heap-fundamentals.md](heap-fundamentals.md) if you already know how a binary heap works, but do read the `heapify` section — "why is building a heap O(n)?" is a classic question. The `heapq` tour in
[min-heap-and-max-heap.md](min-heap-and-max-heap.md) is the one to keep open as a reference when you write real code.

## 🧠 Knowledge Check

<details>
<summary>To find the 10 <em>largest</em> items in a huge stream, why do you use a <em>min</em>-heap of size 10?</summary>

The heap holds the 10 largest items seen so far. When a new item arrives, the only item that might need to leave is the **smallest** of those 10 — and a min-heap gives you its smallest element at the root in O(1). If the
new item is bigger than the root, replace the root (`heapreplace`, O(log 10)); otherwise ignore the new item. A max-heap would put the *largest* kept item at the root, which tells you nothing about who to evict. The whole stream is
processed in O(n log k) time with only O(k) memory. See [heap-problems.md](heap-problems.md).

</details>

<details>
<summary>Building a heap by inserting <em>n</em> items one at a time looks like O(n log n), but <code>heapify</code> does it in O(n). What makes <code>heapify</code> cheaper?</summary>

`heapify` works bottom-up: it sifts down every internal node, starting from the last one. About half the nodes are leaves and need no work; a quarter of the nodes can sink at most one level; an eighth at most two; and so on. The total
work is roughly `n/4·1 + n/8·2 + n/16·3 + … ≤ n`, because nodes near the bottom — where most of them are — travel only a short distance. Inserting one at a time sifts each new item *up*, and in the worst case (items arriving in
descending order for a min-heap) every item travels all the way to the root, costing about log n each. The measurements in [heap-fundamentals.md](heap-fundamentals.md) show `heapify` staying under 2n comparisons while descending
pushes needed about 7 times more at 100,000 items.

</details>

## 📚 References

- [Python docs: `heapq`](https://docs.python.org/3/library/heapq.html) — the heap queue algorithm, its functions, and the priority-queue implementation notes (tie-breaking counter and lazy removal).
- [Python docs: `queue.PriorityQueue`](https://docs.python.org/3/library/queue.html#queue.PriorityQueue) — the thread-safe priority queue.
- [Wikipedia: Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)), [Binary heap](https://en.wikipedia.org/wiki/Binary_heap), [Priority queue](https://en.wikipedia.org/wiki/Priority_queue), and [Heapsort](https://en.wikipedia.org/wiki/Heapsort) — definitions, array layout, and analysis.
- [Wikipedia: Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding) — the "combine the two smallest" greedy idea used in the ropes problem.
- [W3Schools: Python `heapq` Module](https://www.w3schools.com/python/ref_module_heapq.asp) — a short beginner reference for the standard-library functions.
- [GeeksforGeeks: Heap Data Structure](https://www.geeksforgeeks.org/dsa/heap-data-structure/) and [Priority Queue](https://www.geeksforgeeks.org/dsa/priority-queue-set-1-introduction/) — overviews and practice problems.

## ➡️ Continue Your Learning Path

Continue to the [Graphs](../graphs/README.md) module, the next module in this domain, where items are connected by arbitrary relationships rather than a strict hierarchy — and where priority queues reappear in the
shortest-path algorithms.
