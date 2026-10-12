# 🔤 Strings

## 📚 Overview

This module treats text as the second concrete data structure after the [array](../arrays/README.md). A
string is an ordered sequence of characters, so the traversal, two-pointer, and sliding-window techniques
carry over directly — but strings add three twists that cause most string bugs: they are **immutable**,
their "characters" are Unicode **code points** rather than bytes, and operations that look cheap (slicing,
`+=`) can copy the whole string. The module covers those foundations, the everyday transformations, the
palindrome family of problems, and the handful of reusable patterns — frequency counting, windows, prefix
scanning, pattern matching, and stacks — behind most string questions.

Every code example was run, and each algorithm was checked against a brute-force or built-in version on
thousands of random inputs. The benchmarks in the module are real measurements from CPython 3.9, and they show
the shapes of the cost curves (linear vs. quadratic), which are what matter.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain string immutability, the difference between code points and bytes, and why `len`, indexing, and
  comparison behave the way they do.
- Build strings efficiently with `join`, and recognize when `+=`, prepending, or repeated slicing turn
  linear work into quadratic work.
- Reverse text and words, count characters, check anagrams, run-length encode, and shift letters, stating the
  time and space cost of each.
- Solve the palindrome family — basic, ignoring case and punctuation, one removal allowed, longest palindromic
  substring, counting, and rearrangement — and justify the O(n) or O(n²) bounds.
- Recognize the five core string patterns from a problem's wording and apply counting, two pointers, sliding
  windows, prefix scans, and KMP substring search.

## 📋 Prerequisites

- [Arrays](../arrays/README.md) — strings reuse indexing, traversal, the two-pointer technique, and sliding windows.
- [Time and Space Complexity](../time-and-space-complexity/README.md) — every claim is stated in Big-O terms.
- Basic Python reading ability — the examples use Python strings, lists, dictionaries, and functions.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [string-fundamentals.md](string-fundamentals.md) | Immutability, code points vs. bytes, memory per character, comparison, operation costs, and measured string-building strategies |
| [string-manipulation.md](string-manipulation.md) | Reversing, splitting, counting, anagrams, run-length encoding, letter shifting, rotation, and removing characters |
| [palindrome-problems.md](palindrome-problems.md) | Six palindrome problems from two-pointer checks to expand-around-center, with a measured worst case |
| [string-patterns.md](string-patterns.md) | Counting, two pointers, windows, prefixes, naive vs. KMP search, and stack-based parsing; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [palindrome-problems.md](palindrome-problems.md) and [string-patterns.md](string-patterns.md) if you
are preparing for coding interviews — palindromes, anagrams, minimum-window substrings, and substring search are
among the most frequently asked string questions, and explaining *why* each approach is O(n) or O(n²) is a common
follow-up.

**Skim** [string-manipulation.md](string-manipulation.md) if you already write string-processing code comfortably,
but do read the Unicode and string-building sections of [string-fundamentals.md](string-fundamentals.md): they
explain failures that tests with plain English text will never reveal.

## 🧠 Knowledge Check

<details>
<summary>Why should you build a long string by appending pieces to a list and calling <code>"".join()</code> instead of using <code>+=</code> in a loop — even though <code>+=</code> sometimes benchmarks fine in CPython?</summary>

Strings are immutable, so each `+=` conceptually creates a new string and copies the old one, which makes the
total cost quadratic in the final length. CPython can sometimes extend a string in place when nothing else refers
to it, which hides the problem — but that is an implementation detail: the measurements in
[string-fundamentals.md](string-fundamentals.md) show the cost becoming quadratic as soon as a second reference
exists or when prepending, and PEP 8 advises against relying on it. `join` copies every piece exactly once on every
implementation, so it is linear everywhere.

</details>

<details>
<summary>When checking whether a string can become a palindrome by removing at most one character, why is it enough to try only two options at the first mismatch?</summary>

Moving inward from both ends, everything outside the first mismatched pair already matches. At the mismatch, a
palindrome can only be formed if one of the two mismatched characters is removed — any other deletion would leave
that mismatch in place. So you test the remainder with the left character skipped, and with the right character
skipped; if either remainder is a palindrome, the answer is yes. Each test is one linear scan, so the whole check
is O(n). See [palindrome-problems.md](palindrome-problems.md).

</details>

## 📚 References

- [Python docs: Text Sequence Type — `str`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) — the methods used throughout the module.
- [Python docs: Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) and [`unicodedata`](https://docs.python.org/3/library/unicodedata.html) — code points, encodings, and normalization.
- [PEP 393 — Flexible String Representation](https://peps.python.org/pep-0393/) — how CPython stores one, two, or four bytes per character.
- [PEP 8 — Programming Recommendations](https://peps.python.org/pep-0008/) — why not to rely on CPython's in-place string concatenation.
- [Python FAQ: What is the most efficient way to concatenate many strings together?](https://docs.python.org/3/faq/programming.html) — the `str.join()` idiom.
- [W3Schools: Python Strings](https://www.w3schools.com/python/python_strings.asp) — a beginner-friendly tour of string operations.
- [GeeksforGeeks: Introduction to Strings](https://www.geeksforgeeks.org/dsa/introduction-to-strings-data-structure-and-algorithm-tutorials/) — an overview of strings in data structures and algorithms.
- [GeeksforGeeks: KMP Algorithm for Pattern Searching](https://www.geeksforgeeks.org/dsa/kmp-algorithm-for-pattern-searching/) and [Manacher's Algorithm](https://www.geeksforgeeks.org/dsa/manachers-algorithm-linear-time-longest-palindromic-substring-part-1/) — the linear-time algorithms mentioned but not derived here.

## ➡️ Continue Your Learning Path

Continue to the [Recursion](../recursion/README.md) module, the next module in this domain, which introduces
solutions defined in terms of smaller versions of themselves — the foundation for trees, graphs, and dynamic programming.
