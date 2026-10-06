# 🧱 Arrays

## 📚 Overview

This module covers the array — the first concrete data structure in this domain — and applies the
complexity vocabulary from [Time and Space Complexity](../time-and-space-complexity/) to it: why
reading by index is O(1), what dynamic arrays do when they grow, what traversal, insertion, and
deletion really cost, and two techniques — two pointers and the sliding window — that turn many
nested-loop problems into a single linear pass.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain why array indexing is O(1) using contiguous memory and address arithmetic, and why
  appending to a dynamic array is amortized O(1).
- Traverse arrays forward, backward, and in two dimensions, and avoid the bugs caused by changing a
  list while looping over it.
- Predict the cost of an insertion or deletion from *where* it happens, and name the standard
  alternatives (`deque`, swap-and-pop, bulk filtering).
- Recognize when the two-pointer technique or a sliding window applies, implement both, and justify
  their O(n) running time.

## 📋 Prerequisites

- [Time and Space Complexity](../time-and-space-complexity/) — every claim in this module is stated in Big-O terms.
- Basic Python reading ability — the examples use Python lists, loops, and functions.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [array-fundamentals.md](array-fundamentals.md) | Contiguous memory, O(1) indexing, dynamic arrays and amortized append, and what a Python `list` is |
| [traversal.md](traversal.md) | Forward, backward, and 2D traversal; early exit; the change-while-iterating bug |
| [insertion-and-deletion.md](insertion-and-deletion.md) | Why shifting makes front/middle changes O(n), measured, plus `deque`, swap-and-pop, filtering, and `bisect` |
| [two-pointer-technique.md](two-pointer-technique.md) | Opposite-ends and reader/writer pointers, with five worked problems |
| [sliding-window.md](sliding-window.md) | Fixed and variable windows, amortized O(n) analysis; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** the last two files if you are preparing for coding interviews — two pointers and
sliding windows are among the most frequently used array patterns, and the amortized-analysis
argument in the sliding-window file is a common follow-up question.

**Skim** the fundamentals and traversal files if you already work comfortably with arrays — but read
the cost discussion in the insertion-and-deletion file, since `insert(0, x)` and `pop(0)` in loops
are a very common hidden performance problem.

## 🧠 Knowledge Check

<details>
<summary>Why is reading <code>items[i]</code> O(1) even for a million-element array, while checking whether a value is <em>in</em> the array is O(n)?</summary>

An array's elements sit in one contiguous block, so the address of element `i` is simply
`base_address + i × element_size` — one calculation, regardless of the array's length. There is no
comparable formula for finding an arbitrary *value*: with no ordering to exploit, every element may
need to be examined, giving O(n). (If the array is sorted, binary search brings it down to
O(log n).)

</details>

<details>
<summary>A sliding-window solution has a <code>while</code> loop nested inside a <code>for</code> loop. Why is it still O(n) rather than O(n²)?</summary>

The inner loop does not restart for each outer iteration. The `left` pointer only ever moves
forward, so across the whole run `right` advances at most `n` times and `left` advances at most `n`
times — at most `2n` steps in total. Totalling the work across the entire run, instead of
multiplying per-iteration worst cases, is amortized analysis.

</details>

## 📚 References

- [Python Design and History FAQ: How are lists implemented in CPython?](https://docs.python.org/3/faq/design.html) — the official description of a list as a contiguous array of references.
- [Python Wiki: TimeComplexity](https://wiki.python.org/moin/TimeComplexity) — time complexities of list operations, including the amortized-worst-case caveat.
- [Python docs: `collections.deque`](https://docs.python.org/3/library/collections.html) — O(1) operations at both ends, and the cost of middle indexing.
- [Python docs: `bisect`](https://docs.python.org/3/library/bisect.html) — binary search helpers and the cost of `insort`.
- [Python docs: `array`](https://docs.python.org/3/library/array.html) — compact typed arrays, including `itemsize` and `buffer_info()`.
- [W3Schools: DSA Arrays](https://www.w3schools.com/dsa/dsa_data_arrays.php) — a beginner-friendly introduction to arrays as a data structure.
- [GeeksforGeeks: Array Data Structure](https://www.geeksforgeeks.org/dsa/array-data-structure-guide/) — an overview of arrays and common array problems.
- [GeeksforGeeks: Two Pointers Technique](https://www.geeksforgeeks.org/dsa/two-pointers-technique/) — additional examples of both pointer patterns.
- [GeeksforGeeks: Sliding Window Technique](https://www.geeksforgeeks.org/dsa/window-sliding-technique/) — additional fixed- and variable-window examples.

## ➡️ Continue Your Learning Path

Continue to the Strings module, the next module in this domain, where the traversal, two-pointer,
and sliding-window ideas from this module are applied to text.
