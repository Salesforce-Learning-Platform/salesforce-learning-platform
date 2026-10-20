# 🔀 Sorting Algorithms

## 📚 Overview

Sorting puts items in order, and almost every serious program does it somewhere: ranking search results, merging records, preparing data for binary search, finding duplicates, scheduling events. It is also the best laboratory for learning to judge algorithms. A dozen methods solve the same problem with different trade-offs in speed, memory, stability, and behaviour on special inputs, and a hard mathematical limit says how fast any comparison-based method can ever be.

This module covers the vocabulary (stability, in-place, adaptive) and the proof, verified by exhaustive search for small inputs, that comparison sorts need about `n log₂ n` comparisons; the three quadratic sorts and where each still earns its place; merge sort, quick sort, and heap sort, the three `n log n` workhorses, with their counting arguments, pivot strategies, and worst-case guarantees; cyclic sort, a linear-time technique for the values `1..n` that doubles as the standard tool for "find the missing or duplicate number" problems; and a closing comparison that adds counting sort and radix sort and ends with a measured decision guide. Every code example was run on CPython 3.9. Each algorithm was cross-checked against Python's `sorted` on thousands of random lists, comparison and swap counts are real measurements, and the prose was rewritten wherever a measurement contradicted a first guess.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Use the vocabulary of sorting precisely — stable, in-place, adaptive, comparison sort — and explain why the information-theoretic bound of `⌈log₂ n!⌉` comparisons applies to every comparison sort, and what kinds of knowledge let an algorithm escape it.
- Implement bubble, selection, and insertion sort, state their exact comparison and write counts (including the link between insertion sort and the number of inversions), and say when a quadratic sort is the right tool.
- Implement top-down and bottom-up merge sort; derive its worst-case comparison count; use the merge step to count inversions, to sort data too large for memory, and to sort a linked list.
- Implement quick sort with Lomuto and Hoare partitioning; compare pivot strategies by measurement; avoid the O(n²) worst case and deep recursion; handle duplicates with a three-way partition; and use quickselect to find the k-th item in expected linear time.
- Implement in-place heap sort and explain its guarantees (worst-case O(n log n) with O(1) extra space), its cost in comparisons, and why it is rarely used alone.
- Use cyclic placement to sort the values `1..n` in O(n) and to solve the missing-number, duplicate, and first-missing-positive problems, including the range checks that keep it from looping forever.
- Choose among all of the above — and counting sort, radix sort, and Python's built-in Timsort — for a given situation, and use `sorted`, `list.sort`, stable multi-key sorting, and `heapq` correctly in Python.

## 📋 Prerequisites

- [Arrays](../arrays/README.md) — sorting rearranges array elements by index; swaps and shifting are array operations.
- [Time and Space Complexity](../time-and-space-complexity/README.md) — every algorithm is analysed with Big O, and best, average, and worst cases are compared.
- [Recursion](../recursion/README.md) — merge sort and quick sort are recursive divide-and-conquer algorithms.
- [Heaps and Priority Queues](../heaps-and-priority-queues/README.md) — heap sort is built on the heap's array layout and sift operations.
- [Linked Lists](../linked-lists/README.md) — merge sort on linked lists (optional, in one section of the merge sort file).
- Basic Python reading ability — the examples use functions, lists, tuples, and the standard library (`heapq`, `bisect`, `functools`, `operator`, `itertools`, `timeit`).

## 📂 Module Contents

| File | Description |
|------|-------------|
| [sorting-fundamentals.md](sorting-fundamentals.md) | Vocabulary, stability, what Python's `sorted` promises, the comparison-sort lower bound verified by exhaustive search, and the test harness used for every algorithm |
| [elementary-sorts.md](elementary-sorts.md) | Bubble, selection, and insertion sort: traces, exact comparison and write counts, the inversion identity, and measured running times |
| [merge-sort.md](merge-sort.md) | Top-down and bottom-up merge sort, the worst-case comparison formula, counting inversions, external sorting with `heapq.merge`, and merge sort on linked lists |
| [quick-sort.md](quick-sort.md) | Lomuto and Hoare partitioning, a measured comparison of pivot strategies, recursion depth, three-way partitioning, a stable variant, and quickselect |
| [heap-sort.md](heap-sort.md) | In-place heap sort: build and extract phases, measured comparison counts, behaviour on different inputs, and its place among the `n log n` sorts |
| [cyclic-sort.md](cyclic-sort.md) | Sorting `1..n` in O(n), the exact swap count from permutation cycles, and the missing-number, duplicate, and first-missing-positive problems |
| [choosing-a-sorting-algorithm.md](choosing-a-sorting-algorithm.md) | Side-by-side properties, counting sort and radix sort, a benchmark across input shapes and at scale, Python's sorting toolkit, a decision guide, and the module summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [merge-sort.md](merge-sort.md) and [quick-sort.md](quick-sort.md) if you are preparing for coding interviews: writing either sort, stating its complexity and stability, explaining why quick sort's worst case happens and how to avoid it, and using the same ideas for inversion counting and the k-th largest element are among the most common questions. Read [cyclic-sort.md](cyclic-sort.md) in full for the family of "missing or duplicate number" problems — the first-missing-positive solution is a well-known hard question that becomes routine once you know the placement idea.

**Skim** [elementary-sorts.md](elementary-sorts.md) if you already know the three quadratic sorts, but keep the insertion-sort and inversion discussion, which explains why library sorts use insertion sort for short runs. Treat [heap-sort.md](heap-sort.md) as reference material unless you need an in-place sort with a worst-case guarantee, and read [choosing-a-sorting-algorithm.md](choosing-a-sorting-algorithm.md) for its decision guide and the Python toolkit even if you skip the rest: in practice, the right answer is usually `sorted()`.

## 🧠 Knowledge Check

<details>
<summary>Why can no comparison-based sorting algorithm beat O(n log n) in the worst case, and how can counting sort run in O(n + k)?</summary>

A comparison sort learns about the input only through yes/no questions ("is `a` before `b`?"), so it can be drawn as a binary decision tree whose leaves are the possible output orders. Every one of the `n!` orderings of `n` distinct items needs its own leaf, and a binary tree with `n!` leaves has height at least `⌈log₂ n!⌉` — about `n log₂ n − 1.44 n` — so some input forces that many comparisons. Counting sort is not a comparison sort: it uses each key *as an index* into an array of counters, which tells it more than any comparison could. That works only when the keys are integers from a known, small range `k`, and it costs O(n + k) time and space. See [sorting-fundamentals.md](sorting-fundamentals.md) and [choosing-a-sorting-algorithm.md](choosing-a-sorting-algorithm.md).

</details>

<details>
<summary>Quick sort has an O(n²) worst case yet is widely used. What causes the bad case, and how do you avoid it?</summary>

The cost depends on how evenly each partition splits the list. If the pivot is repeatedly the smallest or largest item — for example, the first or last item of an already sorted list — each partition removes just one item and the total work is `(n − 1) + (n − 2) + … = n(n − 1)/2` comparisons. Duplicates cause the same collapse when every item equals the pivot. The standard defences are a **random pivot** (no input is bad for it, so the expected cost is about `1.39 n log₂ n` comparisons), **median of three** pivots, a **three-way partition** so equal items are never revisited, recursing into the **smaller** part first so the stack stays O(log n), and **introsort**, which switches to heap sort if the recursion gets too deep. See [quick-sort.md](quick-sort.md).

</details>

## 📚 References

- [Wikipedia: Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm) and [Comparison sort](https://en.wikipedia.org/wiki/Comparison_sort) — the catalogue of algorithms and the lower-bound argument.
- [Wikipedia: Insertion sort](https://en.wikipedia.org/wiki/Insertion_sort), [Merge sort](https://en.wikipedia.org/wiki/Merge_sort), [Quicksort](https://en.wikipedia.org/wiki/Quicksort), and [Heapsort](https://en.wikipedia.org/wiki/Heapsort) — definitions, analysis, and variants.
- [Wikipedia: Timsort](https://en.wikipedia.org/wiki/Timsort) and [Introsort](https://en.wikipedia.org/wiki/Introsort) — the hybrid algorithms used by Python and by some C++ standard libraries.
- [Wikipedia: Counting sort](https://en.wikipedia.org/wiki/Counting_sort), [Radix sort](https://en.wikipedia.org/wiki/Radix_sort), and [Cycle sort](https://en.wikipedia.org/wiki/Cycle_sort) — the non-comparison sorts, and the differently named comparison sort that is often confused with cyclic sort.
- [Python docs: Sorting Techniques](https://docs.python.org/3/howto/sorting.html), [`list.sort`](https://docs.python.org/3/library/stdtypes.html#list.sort), [`sorted`](https://docs.python.org/3/library/functions.html#sorted), and [`heapq`](https://docs.python.org/3/library/heapq.html) — key functions, stability, and the top-k tools.
- [CPython `listsort.txt`](https://github.com/python/cpython/blob/main/Objects/listsort.txt) — the author's own description of Timsort.
- [W3Schools: Bubble Sort](https://www.w3schools.com/dsa/dsa_algo_bubblesort.php), [Selection Sort](https://www.w3schools.com/dsa/dsa_algo_selectionsort.php), [Insertion Sort](https://www.w3schools.com/dsa/dsa_algo_insertionsort.php), [Quicksort](https://www.w3schools.com/dsa/dsa_algo_quicksort.php), [Merge Sort](https://www.w3schools.com/dsa/dsa_algo_mergesort.php), [Counting Sort](https://www.w3schools.com/dsa/dsa_algo_countingsort.php), and [Radix Sort](https://www.w3schools.com/dsa/dsa_algo_radixsort.php) — illustrated beginner introductions.
- [GeeksforGeeks: Sorting Algorithms](https://www.geeksforgeeks.org/dsa/sorting-algorithms/), [Insertion Sort](https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/), [Merge Sort](https://www.geeksforgeeks.org/dsa/merge-sort/), [QuickSort](https://www.geeksforgeeks.org/dsa/quick-sort-algorithm/), [Heap Sort](https://www.geeksforgeeks.org/dsa/heap-sort/), [Counting Sort](https://www.geeksforgeeks.org/dsa/counting-sort/), and [Radix Sort](https://www.geeksforgeeks.org/dsa/radix-sort/) — overviews and practice problems.

## ➡️ Continue Your Learning Path

Continue to the Searching Algorithms module, where sorted data pays off: binary search finds an item among a million in about twenty steps, and the same idea of halving the possibilities solves a surprising range of problems — including some that have no list in them at all.
