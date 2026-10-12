# 🪆 Recursion

## 📚 Overview

Recursion is a way of structuring a solution so that a function solves a problem by solving smaller copies of the
same problem. It is the natural tool for anything that contains smaller versions of itself — nested folders, trees,
puzzles that split into sub-puzzles — and it underlies divide and conquer, backtracking, and dynamic programming later in
this domain. This module teaches recursion as a discipline rather than a trick: how the call stack really behaves, how to
choose and prove base cases, how to draw a recursion as a tree and read its cost from the picture, and a method for
writing recursive solutions to classic problems.

Every code example was run on CPython 3.9, every printed output is real, and each algorithm was checked against a
built-in or brute-force version on thousands of random inputs or exhaustively on small sizes.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain how a recursive call uses the call stack, and describe the winding-down and unwinding phases of a
  recursion.
- Write a recursive function from a clear definition, with correct base cases and a recursive case that makes
  strict progress.
- Diagnose the common failures — missing, unreachable, or wrong base cases, and the Python recursion limit — and
  explain why Python does not optimize tail calls.
- Draw a recursion tree, count its calls to find the running time, and use its height to find the stack space.
- Recognize when repeated subproblems call for caching, and apply `functools.lru_cache`.
- Apply a recursive method to classic problems: fast exponentiation, Tower of Hanoi, subsets, permutations,
  balanced parentheses, and flattening nested lists — and convert a recursion to an explicit stack.

## 📋 Prerequisites

- [Time and Space Complexity](../time-and-space-complexity/README.md) — recursion costs are expressed in Big-O terms.
- [Arrays](../arrays/README.md) — indexing, slicing, and why slices copy.
- Basic Python reading ability — the examples use Python functions, lists, and dictionaries.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [recursion-fundamentals.md](recursion-fundamentals.md) | Base case and recursive case, the call stack in action, time and space, Python's recursion limit, tail recursion, recursion vs. iteration |
| [base-cases.md](base-cases.md) | What goes wrong without a reachable base case, multiple base cases, choosing base values, termination proofs, Euclid and binary search |
| [recursion-tree.md](recursion-tree.md) | Drawing calls as a tree, counting calls and height, the level-by-level method, recurrence table, memoization |
| [recursive-problem-solving.md](recursive-problem-solving.md) | A six-step method and eight problems from digit sums to backtracking; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [base-cases.md](base-cases.md) and [recursion-tree.md](recursion-tree.md) even if you have written
recursive functions before: correct base cases and the ability to read cost off a recursion tree are the two skills
interviewers test most, and they are what makes the trees, graphs, and dynamic-programming modules approachable.

**Skim** [recursion-fundamentals.md](recursion-fundamentals.md) if you are already comfortable with call stacks — but
read the sections on Python's recursion limit and tail recursion, which are specific to Python and often asked about.
Work through the problems in [recursive-problem-solving.md](recursive-problem-solving.md) by predicting each answer
yourself before reading it.

## 🧠 Knowledge Check

<details>
<summary>The naive recursive Fibonacci function takes exponential time but uses only linear stack space. How can both be true?</summary>

Time is proportional to the **number of calls** (the nodes of the recursion tree), and the naive Fibonacci tree has about
1.618ⁿ nodes because the same subproblems are recomputed in many places. Stack space is proportional to the **height** of
the tree, because only one root-to-node path of calls is on the stack at any moment. The longest path (`fib(n) → fib(n−1)
→ … → fib(1)`) has `n` levels, so the space is O(n) even though the tree is exponentially large. See
[recursion-tree.md](recursion-tree.md).

</details>

<details>
<summary>A recursive function works for small inputs but raises <code>RecursionError</code> for an input of 5,000. Writing it in a tail-recursive style does not help. Why not, and what are the real options?</summary>

Python's default limit is about 1,000 frames, and CPython does not eliminate tail calls (its creator declined to, partly
because eliminated frames would disappear from tracebacks), so a tail-recursive function still uses one frame per call.
The real options are to rewrite the function as a loop, to manage an **explicit stack** yourself (as in
`flatten_iterative`), or — only when the depth is bounded and you understand the platform risk — to raise the limit with
`sys.setrecursionlimit`, which the Python documentation warns can crash the interpreter if set too high. See
[recursion-fundamentals.md](recursion-fundamentals.md).

</details>

## 📚 References

- [Python docs: `sys.getrecursionlimit` and `sys.setrecursionlimit`](https://docs.python.org/3/library/sys.html) — the recursion limit and the warning about raising it.
- [Python docs: `functools.lru_cache`](https://docs.python.org/3/library/functools.html) — caching results of pure functions.
- [Guido van Rossum: Tail Recursion Elimination](http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html) — why Python does not eliminate tail calls.
- [Wikipedia: Master theorem](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)) — the shortcut for divide-and-conquer recurrences.
- [Wikipedia: Tower of Hanoi](https://en.wikipedia.org/wiki/Tower_of_Hanoi) — the puzzle and the proof that 2ⁿ − 1 moves are optimal.
- [OEIS A000108: Catalan numbers](https://oeis.org/A000108) — the sequence counting balanced parentheses.
- [W3Schools: Python Function Recursion](https://www.w3schools.com/python/gloss_python_function_recursion.asp) — a short beginner introduction.
- [GeeksforGeeks: Introduction to Recursion](https://www.geeksforgeeks.org/dsa/introduction-to-recursion-data-structure-and-algorithm-tutorials/) — an overview of recursion and its common problems.

## ➡️ Continue Your Learning Path

Continue to the [Hashing](../hashing/README.md) module, the next module in this domain, where a different idea — using a key
to compute where data lives — turns many O(n) searches into O(1) lookups.
