# ⚙️ Bit Manipulation

## 📚 Overview

Underneath every number a program stores is a row of bits, and **bit manipulation** is the practice of working on that row directly: reading one bit, switching a group of bits on or off, comparing two patterns position by position, or sliding a pattern left and right. The operations are among the cheapest a processor can perform, and a small vocabulary of them turns up everywhere — permission flags, network addresses and subnet masks, packed colors, compact sets, checksums, error correction, hashing, graphics, and a famous family of interview puzzles whose answers fit in two lines.

This module starts with the operators themselves and with the part that surprises Python programmers: integers have no fixed width, so negative numbers behave as if padded with infinitely many sign bits, right shifts floor, and the precedence rules differ from C. It then builds the masking techniques (single bits, multi-bit fields, flags, packed data, subsets, and bitsets), the algebra of XOR (the unpaired number, the missing number, range queries, parity and recovery, Gray codes), and the patterns around the lowest set bit (power-of-two tests, population counts, rounding). Every code example was run on CPython 3.9. Each helper was checked against an independent reference — a list of digits, the standard `ipaddress` module, a `Counter`, or `itertools` — on thousands of random inputs, and the benchmarks are real measurements, including the cases where the built-in operation beats the hand-written trick.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Read and write numbers in binary, octal, and hexadecimal in Python, and use the six bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`) on both positive and negative integers.
- Explain how Python's unbounded integers differ from fixed-width integers in other languages: infinite sign extension, flooring right shifts, `~x == -x - 1`, and masking to simulate a fixed width.
- Avoid the common traps: operator precedence, `^` versus `**`, `~` on booleans, negative shift counts, and reading `bin(-5)` as stored bits.
- Get, set, clear, toggle, and update single bits; extract and insert multi-bit fields; and use masks for flags and permissions, packed colors and IPv4 addresses, and network membership tests.
- Enumerate all subsets and submasks with integers, and use a Python integer as a bitset, knowing when it beats `set` and when it wastes memory.
- Use XOR's properties (identity, self-inverse, commutativity, associativity) to find unpaired and missing numbers, answer range queries, compute parity, rebuild lost data, and generate Gray codes, and recognize why the XOR swap and repeating-key XOR are not good practice.
- Apply `n & (n - 1)` and `n & -n` to test for powers of two, count set bits, find the lowest and highest set bits, and round up to a power of two; and choose between a hand-written bit trick and a built-in operation.

## 📋 Prerequisites

- [Time and Space Complexity](../time-and-space-complexity/README.md) — the tricks are justified by their O(1) time and space, and the subset enumeration by its exponential growth.
- [Arrays](../arrays/README.md) — the examples loop over lists and use indexing; the `Counter` and prefix-array references assume basic list skills.
- [Hashing](../hashing/README.md) — a hash table is the usual alternative to the XOR "find the unpaired number" trick, and sets are the alternative to bitsets.
- [Sorting Algorithms](../sorting-algorithms/README.md) — the missing-number problem appears there with other solutions, and radix sort works digit by digit in the same way the bit tricks work bit by bit (optional).
- Basic Python reading ability — the examples use functions, list comprehensions, and the standard library (`enum`, `ipaddress`, `stat`, `functools`, `itertools`, `timeit`).

## 📂 Module Contents

| File | Description |
|------|-------------|
| [bitwise-operators.md](bitwise-operators.md) | Binary, octal, and hex notation; the six operators and their truth tables; negative numbers without a fixed width; flooring shifts; precedence and other Python traps; algebraic identities verified on random integers |
| [bit-masking.md](bit-masking.md) | Get, set, clear, toggle, and update bits; extracting and inserting fields; `IntFlag` and Unix permissions; packed colors and IPv4 addresses with network masks; subsets and submasks; Python integers as bitsets, measured against `set` |
| [xor-tricks.md](xor-tricks.md) | XOR's properties; swapping and the aliasing bug; the unpaired, two unpaired, and missing numbers; prefix XOR range queries; parity and RAID-style recovery; a toy cipher and its limits; Gray codes; Hamming distance |
| [power-of-two-and-counting-bits.md](power-of-two-and-counting-bits.md) | Clearing and isolating the lowest set bit; the power-of-two test; modulo by mask; four ways to count set bits, benchmarked; counting bits for 0..n; trailing zeros and rounding; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [xor-tricks.md](xor-tricks.md) and [power-of-two-and-counting-bits.md](power-of-two-and-counting-bits.md) if you are preparing for coding interviews: the single-number family, the missing number, "is this a power of two?", and "count the set bits" are among the most frequently asked bit questions, and the follow-ups — two unpaired numbers, counting bits for every number up to `n`, doing it without extra space — are answered in these files. Read [bit-masking.md](bit-masking.md) in full if you work with flags, permissions, protocol fields, or any problem that picks "a subset of these items".

**Skim** [bitwise-operators.md](bitwise-operators.md) if you already use bitwise operators in another language — but do not skip the sections on negative numbers, shifts, and precedence: Python's unbounded integers change the answers you might expect from C or Java. Treat the cipher, Gray code, and bitset sections as reference material unless they match a problem you have.

## 🧠 Knowledge Check

<details>
<summary>Why does <code>n &amp; (n - 1) == 0</code> (for <code>n &gt; 0</code>) test whether <code>n</code> is a power of two, and what else does the expression <code>n &amp; (n - 1)</code> compute?</summary>

Subtracting 1 from `n` turns its lowest set bit into 0 and every zero below it into 1, leaving the higher bits unchanged, so `n & (n - 1)` is `n` with its **lowest set bit cleared**. A power of two has exactly one set bit; clearing it leaves 0. For any other positive number at least one set bit remains. The `n > 0` condition is needed because `0 & -1` is also 0, yet zero is not a power of two. Repeating the clearing step until the value reaches 0 counts the set bits — one iteration per bit (Wegner's method, often called Brian Kernighan's algorithm). See [power-of-two-and-counting-bits.md](power-of-two-and-counting-bits.md).

</details>

<details>
<summary>Every number in a list appears twice except one. How does XOR find it in O(n) time and O(1) space, and how would you adapt the idea if <em>two</em> numbers are unpaired?</summary>

XOR is commutative and associative, `a ^ a == 0`, and `a ^ 0 == a`. XORing the whole list therefore cancels every pair, in any order, and leaves the single unpaired value — one pass and one variable. With two unpaired values `a` and `b`, the total is `a ^ b`, which is non-zero; any 1 bit in it marks a position where `a` and `b` differ. Choosing the lowest such bit (`both & -both`) and splitting the list into numbers with and without that bit separates `a` from `b` while keeping every equal pair together, so XORing each group yields one unpaired value per group. See [xor-tricks.md](xor-tricks.md).

</details>

## 📚 References

- [Wikipedia: Bitwise operation](https://en.wikipedia.org/wiki/Bitwise_operation), [Mask (computing)](https://en.wikipedia.org/wiki/Mask_(computing)), and [Two's complement](https://en.wikipedia.org/wiki/Two%27s_complement) — the operators, masks, and signed representation.
- [Wikipedia: Hamming weight](https://en.wikipedia.org/wiki/Hamming_weight) and [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) — population count algorithms and their applications.
- [Wikipedia: XOR swap algorithm](https://en.wikipedia.org/wiki/XOR_swap_algorithm), [Exclusive or](https://en.wikipedia.org/wiki/Exclusive_or), [Parity bit](https://en.wikipedia.org/wiki/Parity_bit), [Gray code](https://en.wikipedia.org/wiki/Gray_code), and [One-time pad](https://en.wikipedia.org/wiki/One-time_pad) — XOR's uses and limits.
- [Wikipedia: Bit array](https://en.wikipedia.org/wiki/Bit_array) and [Find first set](https://en.wikipedia.org/wiki/Find_first_set) — bitsets, and the lowest and highest set bit.
- [Python docs: bitwise operations on integers](https://docs.python.org/3/library/stdtypes.html#bitwise-operations-on-integer-types), [`int.bit_length`](https://docs.python.org/3/library/stdtypes.html#int.bit_length), [`int.bit_count`](https://docs.python.org/3/library/stdtypes.html#int.bit_count), and [operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence) — the language's exact rules.
- [Python docs: `enum.IntFlag`](https://docs.python.org/3/library/enum.html#enum.IntFlag), [`ipaddress`](https://docs.python.org/3/library/ipaddress.html), and [`stat`](https://docs.python.org/3/library/stat.html) — flags, addresses, and file permissions built on bits.
- [W3Schools: Python Operators](https://www.w3schools.com/python/python_operators.asp) and [Python Bitwise Operators](https://www.w3schools.com/python/gloss_python_bitwise_operators.asp) — beginner-friendly operator tables.
- [GeeksforGeeks: Bitwise Algorithms](https://www.geeksforgeeks.org/dsa/bitwise-algorithms/), [Python Bitwise Operators](https://www.geeksforgeeks.org/python/python-bitwise-operators/), and [Count set bits in an integer](https://www.geeksforgeeks.org/dsa/count-set-bits-in-an-integer/) — overviews and practice problems.

## ➡️ Continue Your Learning Path

Continue to the [Dynamic Programming](../dynamic-programming/README.md) module, the next module in this domain, where the focus moves from manipulating single values to solving problems by building answers out of smaller answers.
