# 🧩 Dynamic Programming

## 📚 Overview

Some problems look impossibly large until you notice that the same smaller problems keep recurring. The 30th Fibonacci number takes nearly three million recursive calls by the textbook method, yet only 31 distinct questions are ever asked. **Dynamic programming (DP)** answers each distinct question once, remembers the answer, and builds larger answers from smaller ones — turning exponential-time recursion into polynomial-time algorithms. It is behind spell checkers, file-comparison tools, route and schedule planning, resource allocation, and a large share of the most frequently asked interview problems.

This module covers the two ways to organize the remembering — top-down memoization and bottom-up tabulation — and a five-step recipe (state, transition, base cases, order, answer) that turns a vague problem into a table. It then applies the recipe to one-dimensional problems (climbing stairs, house robber, decoding strings, coin change, maximum subarray, longest increasing subsequence, word break), to knapsack patterns (0/1 and unbounded knapsack, subset sum with a bitset shortcut, partition, signed sums, combinations versus permutations, pseudo-polynomial time), and to string problems (longest common subsequence, edit distance, palindromes). Every code example was run on CPython 3.9. Each solution was checked against a brute-force definition — every path, every subset, every sign assignment, every subsequence, or a breadth-first search over strings — on thousands of small inputs, and the benchmarks are real measurements.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Recognize the two properties of a DP problem — optimal substructure and overlapping subproblems — and explain why caching turns an exponential recursion into a linear or polynomial one.
- Implement a solution both top-down (a dictionary or `functools.lru_cache`) and bottom-up (a table), and choose between them using recursion depth, the number of reachable states, and space optimization.
- Apply the five-step recipe — state, transition, base cases, order, answer — and state a solution's time as (number of states) × (work per state).
- Solve the classic one-dimensional problems and explain why choosing the right state ("ending at `i`") is the heart of the solution.
- Solve 0/1 and unbounded knapsack problems, subset sum, partition, and signed-sum counting; explain why the direction of the capacity loop and the nesting of the coin loops change the problem solved; and use a Python integer as a bitset to speed up subset sum.
- Solve the string problems — longest common subsequence, edit distance, longest palindromic subsequence and substring, minimum insertions for a palindrome — and reconstruct the actual subsequence or edit script, not just its length.
- Recognize when greedy is correct and when it silently fails, and verify any DP against a brute-force version on small inputs.

## 📋 Prerequisites

- [Recursion](../recursion/README.md) — DP starts from recursions with repeated subproblems; the recursion-tree file introduces memoization.
- [Time and Space Complexity](../time-and-space-complexity/README.md) — the cost of a DP is (states) × (work per state), and space optimization is judged in Big O.
- [Arrays](../arrays/README.md) — tables are lists and lists of lists.
- [Strings](../strings/README.md) — the string problems rely on subsequences, substrings, and palindromes.
- [Hashing](../hashing/README.md) — dictionaries as caches (optional).
- [Bit Manipulation](../bit-manipulation/README.md) — the bitset shortcut for subset sum (optional).
- [Searching Algorithms](../searching-algorithms/README.md) — the O(n log n) longest increasing subsequence uses binary search (optional).
- Basic Python reading ability — the examples use functions, lists, nested lists, and the standard library (`functools`, `itertools`, `bisect`, `timeit`).

## 📂 Module Contents

| File | Description |
|------|-------------|
| [dp-fundamentals.md](dp-fundamentals.md) | Overlapping subproblems, memoization versus tabulation, recursion limits and reachable states measured, the five-step recipe with a verified grid example, and where greedy fails |
| [one-dimensional-dp.md](one-dimensional-dp.md) | Climbing stairs, minimum-cost climbing, house robber (linear and circular), decode ways, coin change with reconstruction, Kadane's algorithm, longest increasing subsequence in O(n²) and O(n log n), and word break |
| [knapsack-patterns.md](knapsack-patterns.md) | 0/1 knapsack with traceback and the one-row optimization, subset sum with a bitset, partition, target sum, unbounded knapsack and rod cutting, coin combinations versus permutations, and pseudo-polynomial time |
| [string-dp.md](string-dp.md) | Longest common subsequence, edit distance with its script, longest palindromic subsequence and substring, fewest insertions to make a palindrome; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [dp-fundamentals.md](dp-fundamentals.md) first, whatever your level: the recipe and the state-design discussion are what let you solve problems you have not seen. Then work through [one-dimensional-dp.md](one-dimensional-dp.md) and [string-dp.md](string-dp.md) if you are preparing for coding interviews — coin change, house robber, longest increasing subsequence, longest common subsequence, and edit distance are among the most frequently asked questions in the whole domain, and explaining the state and transition clearly matters as much as the code.

**Skim** [knapsack-patterns.md](knapsack-patterns.md) if you only need the 0/1 pattern, but keep the sections on loop direction and on combinations versus permutations: they explain a large class of off-by-a-factor wrong answers. Treat the bitset subset-sum shortcut and the pseudo-polynomial discussion as reference material unless you work with large capacities.

## 🧠 Knowledge Check

<details>
<summary>Why does memoizing the recursive Fibonacci function change its running time from exponential to linear?</summary>

The recursion `F(n) = F(n − 1) + F(n − 2)` asks only `n + 1` different questions (`F(0)` through `F(n)`), but without a cache it asks the same ones over and over — the number of calls is `2·F(n + 1) − 1`, which grows by a factor of about 1.6 per step (2,692,537 calls for `n = 30`). With a cache, each distinct question is computed once and every repeat is answered by a lookup, so the number of calls drops to `2n − 1` (59 for `n = 30`). The general rule is that the running time of a DP is the number of distinct states times the work per state. See [dp-fundamentals.md](dp-fundamentals.md).

</details>

<details>
<summary>In the 0/1 knapsack's one-row version, why must the capacity loop run from high to low, and what does running it low to high compute instead?</summary>

Row `i` of the table depends on row `i − 1` at smaller capacities. Updating capacities from high to low means `best[w − weight]` has not yet been changed by the current item when `best[w]` is computed, so each item is used at most once. Updating from low to high means `best[w − weight]` may already include the current item, so the item can be used repeatedly — which is the *unbounded* knapsack. With items `(weight 2, value 3)` and `(weight 3, value 5)` and capacity 6, the first order gives 8 and the second gives 10. See [knapsack-patterns.md](knapsack-patterns.md).

</details>

## 📚 References

- [Wikipedia: Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming), [Overlapping subproblems](https://en.wikipedia.org/wiki/Overlapping_subproblems), [Optimal substructure](https://en.wikipedia.org/wiki/Optimal_substructure), and [Memoization](https://en.wikipedia.org/wiki/Memoization) — the method, its two defining properties, and caching.
- [Wikipedia: Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem), [Subset sum problem](https://en.wikipedia.org/wiki/Subset_sum_problem), and [Pseudo-polynomial time](https://en.wikipedia.org/wiki/Pseudo-polynomial_time) — the variants, their complexity, and what pseudo-polynomial means.
- [Wikipedia: Longest common subsequence](https://en.wikipedia.org/wiki/Longest_common_subsequence), [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance), [Longest increasing subsequence](https://en.wikipedia.org/wiki/Longest_increasing_subsequence), and [Maximum subarray problem](https://en.wikipedia.org/wiki/Maximum_subarray_problem) — the classic string and sequence problems.
- [Wikipedia: Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) — when local choices are safe, and when they are not.
- [Python docs: `functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache) and [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) — caching function results.
- [W3Schools: Dynamic Programming](https://www.w3schools.com/dsa/dsa_ref_dynamic_programming.php), [Memoization](https://www.w3schools.com/dsa/dsa_ref_memoization.php), [Tabulation](https://www.w3schools.com/dsa/dsa_ref_tabulation.php), and [The Knapsack Problem](https://www.w3schools.com/dsa/dsa_ref_knapsack.php) — short illustrated introductions.
- [GeeksforGeeks: Introduction to Dynamic Programming](https://www.geeksforgeeks.org/dsa/introduction-to-dynamic-programming-data-structures-and-algorithm-tutorials/), [0/1 Knapsack](https://www.geeksforgeeks.org/dsa/0-1-knapsack-problem-dp-10/), [Longest Common Subsequence](https://www.geeksforgeeks.org/dsa/longest-common-subsequence-dp-4/), [Edit Distance](https://www.geeksforgeeks.org/dsa/edit-distance-dp-5/), [Longest Increasing Subsequence](https://www.geeksforgeeks.org/dsa/longest-increasing-subsequence-dp-3/), and [Coin Change](https://www.geeksforgeeks.org/dsa/coin-change-dp-7/) — overviews and practice problems.

## ➡️ Continue Your Learning Path

Continue to the [Tries](../tries/README.md) module, the next module in this domain, where the focus moves to a tree built for strings — one that answers prefix questions in time proportional to the length of the query, and that combines naturally with bit manipulation and with dynamic programming.
