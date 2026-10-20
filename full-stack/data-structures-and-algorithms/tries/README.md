# 🌲 Tries

## 📚 Overview

A **trie** (pronounced "try" or "tree", from *retrieval*) stores a set of strings in a tree whose edges are letters. Words that begin alike share a path, so a question about a *prefix* — does any word start with `pre`? how many? which, in alphabetical order? — is answered by walking down one path, in time proportional to the length of the query, however many words are stored. Tries power autocomplete and spell checking, and in a bitwise form they route Internet traffic by longest-prefix match and solve the "largest XOR" family of problems.

This module builds the structure from scratch and measures it honestly. It starts with the node, insertion, search, and prefix checks, then measures how much prefix sharing saves, what a trie costs in Python memory (about ten times a set), and where it does and does not beat a set and a sorted list searched with binary search. It adds per-node counters, deletion that prunes dead branches, alphabetical autocomplete with early termination, and the longest common prefix. It applies the trie to ranked autocomplete, shortest-root replacement, wildcard search, the longest word built one letter at a time, and finding dictionary words on a letter board. And it combines the trie with **bit manipulation** (a binary trie for the largest XOR pair and subarray, and IP longest-prefix routing) and with **dynamic programming** (word segmentation and counting distinct substrings). Every code example was run on CPython 3.9. Each structure and algorithm was checked against a plain `set`, a regular expression, or a brute-force definition on thousands of random inputs, with structural invariants verified after every step, and the benchmarks are real measurements — including the ones where the trie loses.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain the trie's structure (nodes, edges labelled by symbols, an end-of-word flag) and implement insert, search, and prefix check in O(L) for a word of length L, independent of the number of words stored.
- Measure how much prefix sharing saves and what a trie costs in memory in Python, and decide between a trie, a hash set, and a sorted list with `bisect` for a given workload.
- Add per-node counters to count words by prefix, delete words without leaving dead branches, produce completions in alphabetical order with early termination, and compute the longest common prefix.
- Solve prefix problems that need branching and pruning: ranked autocomplete, shortest-root replacement, wildcard search with `.`, the longest word buildable one letter at a time, and word search on a letter board.
- Build a binary trie over the bits of integers, use it for the largest XOR of two numbers and of a subarray, and for longest-prefix IP routing.
- Combine a trie with dynamic programming for word break and segmentation counts, and use a suffix trie to count distinct substrings.
- Verify a data structure with a model-based test: random operations compared with a trusted model, with invariants checked after every step.

## 📋 Prerequisites

- [Trees](../trees/README.md) — a trie is a tree; the traversal vocabulary (root, child, depth, pre-order) carries over.
- [Hashing](../hashing/README.md) — a hash set is the main alternative, and the node's children are dictionaries.
- [Strings](../strings/README.md) — prefixes, substrings, and palindromes.
- [Searching Algorithms](../searching-algorithms/README.md) — the sorted-list-plus-`bisect` baseline the trie is measured against.
- [Bit Manipulation](../bit-manipulation/README.md) — the binary trie, XOR, and prefix masks (needed for the last file).
- [Dynamic Programming](../dynamic-programming/README.md) — word break and counting (needed for the last file).
- Basic Python reading ability — the examples use classes, dictionaries, generators of words, and the standard library (`heapq`, `ipaddress`, `re`, `tracemalloc`, `timeit`).

## 📂 Module Contents

| File | Description |
|------|-------------|
| [trie-fundamentals.md](trie-fundamentals.md) | The structure, insert/search/prefix check, why the end flag is essential, prefix sharing and memory measured, and an honest comparison with a set and a sorted list, including the insertion crossover |
| [trie-operations.md](trie-operations.md) | Per-node counters, prefix counts, deletion with pruning, alphabetical autocomplete with early termination, longest common prefix, and a model-based test that checks for dead branches after every step |
| [prefix-problems.md](prefix-problems.md) | Ranked autocomplete, shortest-root replacement, wildcard search, the longest buildable word, and word search on a board, with the trie benchmarked against one search per word |
| [tries-with-bits-and-dp.md](tries-with-bits-and-dp.md) | Binary tries for the largest XOR pair and subarray, longest-prefix IP routing, trie-driven word break and segmentation counts, suffix tries; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [trie-fundamentals.md](trie-fundamentals.md) and [trie-operations.md](trie-operations.md) first: implementing insert, search, `starts_with`, and delete cleanly — and explaining the trade-off against a hash set — is the standard interview ask. Read [prefix-problems.md](prefix-problems.md) if you are preparing for coding interviews: autocomplete, replace words, add-and-search-with-wildcards, and word search II are among the most frequently asked trie questions. Read the binary-trie section of [tries-with-bits-and-dp.md](tries-with-bits-and-dp.md) for the maximum-XOR family.

**Skim** the memory and timing measurements in [trie-fundamentals.md](trie-fundamentals.md) if you only need the structure — but remember their conclusion, which interviewers like: a trie is not automatically faster than a set or a sorted list. Treat the routing and suffix-trie sections as reference material unless you work with networking or text indexing.

## 🧠 Knowledge Check

<details>
<summary>Why does a trie need an end-of-word flag, and what goes wrong without it?</summary>

A node represents a *prefix*, not necessarily a word: after inserting `inn`, the nodes for `i` and `in` exist, but `in` was never inserted. The flag records which nodes are the ends of stored words. Without it, every prefix of a stored word would be reported as a word (`search("in")` would be true), and deleting a word could not be distinguished from deleting only its tail. The flag also lets `starts_with` (does the path exist?) and `search` (does the path exist **and** end a word?) give different answers, which is the whole point of the structure. See [trie-fundamentals.md](trie-fundamentals.md).

</details>

<details>
<summary>In a binary trie over 31-bit integers, why does choosing the child with the opposite bit at each level find the number with the largest XOR?</summary>

The XOR of two numbers has a `1` at a bit position exactly when they differ there, and a `1` at a higher position outweighs every lower position put together (`2ᵏ` is larger than `2ᵏ⁻¹ + … + 1`). So the best partner for `x` is found greedily from the most significant bit: at each level, if a stored number has the opposite bit, follow it and the XOR gets a `1` at that position; otherwise follow the same bit. This takes 31 steps per query, so finding the largest XOR over all pairs costs O(n · 31) instead of the O(n²) of testing every pair. See [tries-with-bits-and-dp.md](tries-with-bits-and-dp.md).

</details>

## 📚 References

- [Wikipedia: Trie](https://en.wikipedia.org/wiki/Trie), [Radix tree](https://en.wikipedia.org/wiki/Radix_tree), and [Suffix tree](https://en.wikipedia.org/wiki/Suffix_tree) — the structure, its compressed form, and the suffix variant.
- [Wikipedia: Longest prefix match](https://en.wikipedia.org/wiki/Longest_prefix_match), [Autocomplete](https://en.wikipedia.org/wiki/Autocomplete), [Approximate string matching](https://en.wikipedia.org/wiki/Approximate_string_matching), and [Aho–Corasick algorithm](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm) — what tries are used for.
- [Python docs: `ipaddress`](https://docs.python.org/3/library/ipaddress.html) and [`heapq`](https://docs.python.org/3/library/heapq.html) — the standard-library tools used for routing checks and ranked suggestions.
- [W3Schools: Trees](https://www.w3schools.com/dsa/dsa_theory_trees.php) — the tree vocabulary a trie builds on.
- [GeeksforGeeks: Introduction to Trie](https://www.geeksforgeeks.org/dsa/introduction-to-trie-data-structure-and-algorithm-tutorials/), [Trie Insert and Search](https://www.geeksforgeeks.org/dsa/trie-insert-and-search/), [Trie Delete](https://www.geeksforgeeks.org/dsa/trie-delete/), and [Word Break Problem using Trie](https://www.geeksforgeeks.org/dsa/word-break-problem-trie-solution/) — overviews and practice problems.

## ➡️ Continue Your Learning Path

Continue to the Operating Systems module, the first in the Computer Science Foundations domain, where the focus moves from the data structures and algorithms programs are built from to the system that runs them: processes, memory, scheduling, and files.
