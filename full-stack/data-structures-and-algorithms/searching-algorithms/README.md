# 🔍 Searching Algorithms

## 📚 Overview

Finding things is the other half of working with data. Programs look up users, check whether a word is in a dictionary, locate the first order over a threshold, decide whether a value was seen before, and answer questions like "what is the smallest capacity that works?". The cost of the search often decides whether a program feels instant or unusable, and the difference between the best and worst method can be a factor of a million.

This module starts with the simplest search, linear search, and with what it really costs, including the built-in Python operations and the hidden linear searches that make loops quadratic. It then covers binary search in depth: the iterative and recursive forms, a loop invariant that proves them correct, an exact probe count, lower and upper bounds for duplicates, Python's `bisect` module, and the classic bugs reproduced on purpose. Next comes the general idea behind it, search-space reduction, applied to rotated arrays, peaks in unsorted data, sorted matrices, two pointers, unbounded lists, and interpolation. The module closes with binary search on the answer, which solves "minimize the maximum" and "maximize the minimum" problems by searching a range of possible answers instead of a list. Every code example was run on CPython 3.9. Each algorithm was cross-checked against a brute-force definition on thousands of cases (often exhaustively on every small input), and the benchmarks are real measurements.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Implement linear search and its variants (first, last, all matches, by predicate), state its best, average, and worst costs, and name the Python built-ins that do it faster (`in`, `list.index`, `next`).
- Spot a hidden linear search inside a loop, and decide with measurements when sorting first or building a set pays off.
- Write binary search iteratively and recursively without off-by-one errors by stating the loop invariant, and explain why it needs exactly `⌊log₂ n⌋ + 1` probes in the worst case.
- Use lower and upper bounds (`bisect_left` and `bisect_right`) for first and last occurrences, counts, insertion points, floors, and ceilings, and use Python's `bisect` module.
- Recognize the classic binary search bugs — midpoint overflow, `low = mid`, mixed range conventions, unsorted input — and test search code exhaustively against a brute-force version.
- Apply search-space reduction to rotated arrays, peak finding, sorted matrices, pair sums, unbounded sequences (exponential search), and evenly spread keys (interpolation search), and explain when each one breaks.
- Solve optimization problems with binary search on the answer: define the range, write a monotone feasibility check, and choose `first_true` or `last_true`.

## 📋 Prerequisites

- [Arrays](../arrays/README.md) — searching works on indexed sequences; binary search needs random access.
- [Time and Space Complexity](../time-and-space-complexity/README.md) — O(n) versus O(log n) and the idea of best, average, and worst cases.
- [Sorting Algorithms](../sorting-algorithms/README.md) — binary search needs sorted data, and the break-even point for sorting first appears in the linear search file.
- [Recursion](../recursion/README.md) — the recursive form of binary search (optional).
- [Hashing](../hashing/README.md) — sets and dictionaries as the alternative to searching a list.
- Basic Python reading ability — the examples use functions, lists, tuples, and the standard library (`bisect`, `itertools`, `math`, `timeit`).

## 📂 Module Contents

| File | Description |
|------|-------------|
| [linear-search.md](linear-search.md) | Linear search and its variants, exact comparison counts, Python's built-in searches, a measured break-even against sorting and sets, the accidental-quadratic trap, and move-to-front |
| [binary-search.md](binary-search.md) | Iterative and recursive binary search, the loop invariant, the exact probe count, lower and upper bounds, the `bisect` module, and the classic bugs reproduced |
| [search-space-reduction.md](search-space-reduction.md) | Rotated arrays (with and without duplicates), peak finding, sorted matrices, two pointers, exponential search, and interpolation search, each cross-checked |
| [binary-search-on-the-answer.md](binary-search-on-the-answer.md) | `first_true` and `last_true`, integer square root, eating speed, ship capacity, array splitting, maximize-the-minimum, real-valued answers, and the module summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [binary-search.md](binary-search.md) and [binary-search-on-the-answer.md](binary-search-on-the-answer.md) if you are preparing for coding interviews: writing a correct binary search from memory, using lower and upper bounds for duplicates, and recognizing "minimize the maximum" problems as searches over the answer are among the most frequently asked topics, and the invariant-based explanation is the follow-up interviewers look for. Read the rotated-array and matrix sections of [search-space-reduction.md](search-space-reduction.md) as well; they are standard questions.

**Skim** [linear-search.md](linear-search.md) if you already know the algorithm — but keep the sections on built-ins, the break-even measurement, and the accidental-quadratic trap, which matter in everyday Python code. Treat the exponential and interpolation search sections of [search-space-reduction.md](search-space-reduction.md) as reference material unless you work with unbounded streams or very large, evenly spread data.

## 🧠 Knowledge Check

<details>
<summary>Why does binary search need at most ⌊log₂ n⌋ + 1 probes, and what two things must be true of the data for it to work?</summary>

Each probe examines the middle item and keeps only the half that can contain the target, so after `k` probes at most `n / 2ᵏ` items remain. The search must end once fewer than one item remains, which happens after at most `⌊log₂ n⌋ + 1` probes — about 20 for a million items and 30 for a billion. The data must be **sorted** (so that a comparison at the middle tells you which half to keep) and must allow **random access** (so that you can jump to the middle in O(1)); a sorted linked list does not qualify. See [binary-search.md](binary-search.md).

</details>

<details>
<summary>A problem asks for the smallest ship capacity that delivers all packages within D days. How can this be solved with binary search when there is no sorted array?</summary>

The candidate answers form a range (from the heaviest package to the total weight), and a proposed capacity can be tested with one greedy pass that counts the days needed. The test is **monotone**: if capacity `c` works, any larger capacity works too, so the capacities split into a block of "too small" followed by a block of "big enough". Binary search finds the boundary — the first capacity that works — in about `log₂(range)` tests, each costing O(n). The key is the proof that the test is monotone; without it the search silently returns a wrong answer. See [binary-search-on-the-answer.md](binary-search-on-the-answer.md).

</details>

## 📚 References

- [Wikipedia: Linear search](https://en.wikipedia.org/wiki/Linear_search), [Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm), [Interpolation search](https://en.wikipedia.org/wiki/Interpolation_search), and [Exponential search](https://en.wikipedia.org/wiki/Exponential_search) — definitions, analysis, and variants.
- [Wikipedia: Self-organizing list](https://en.wikipedia.org/wiki/Self-organizing_list) and [Bisection method](https://en.wikipedia.org/wiki/Bisection_method) — the move-to-front heuristic, and the numerical cousin of binary search on real-valued answers.
- [Joshua Bloch: "Nearly All Binary Searches and Mergesorts are Broken"](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/) — the midpoint overflow bug found in the JDK and in *Programming Pearls*.
- [Python docs: `bisect`](https://docs.python.org/3/library/bisect.html), [`math.isqrt`](https://docs.python.org/3/library/math.html#math.isqrt), and [common sequence operations](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range) — the standard library's searching tools.
- [W3Schools: Linear Search](https://www.w3schools.com/dsa/dsa_algo_linearsearch.php) and [Binary Search](https://www.w3schools.com/dsa/dsa_algo_binarysearch.php) — illustrated beginner introductions.
- [GeeksforGeeks: Linear Search](https://www.geeksforgeeks.org/dsa/linear-search/), [Binary Search](https://www.geeksforgeeks.org/dsa/binary-search/), [Interpolation Search](https://www.geeksforgeeks.org/dsa/interpolation-search/), [Exponential Search](https://www.geeksforgeeks.org/dsa/exponential-search/), and [Binary Search on Answer](https://www.geeksforgeeks.org/dsa/binary-search-on-answer-tutorial-with-problems/) — overviews and practice problems.

## ➡️ Continue Your Learning Path

Continue to the [Bit Manipulation](../bit-manipulation/README.md) module, where the focus moves from searching through values to working with the individual bits inside them — a toolkit that makes some counts, checks, and searches astonishingly short.
