# #️⃣ Hashing

## 📚 Overview

Hashing is the idea of *computing* where data lives instead of searching for it. A **hash function** turns a key into a number; a
**hash table** uses that number to pick a slot in an array, so reading, inserting, and deleting take **O(1) on average**. Hash tables
power Python's `dict` and `set`, database indexes, caches, and countless interview solutions, and they are the most common way to
trade a little memory for a large speedup. This module explains the hash function, builds a hash table from scratch, examines the
unavoidable problem of collisions, and then applies the structure to the patterns that recur in problem solving.

Every code example was run on CPython 3.9. The hash tables built in the module were tested against Python's own `dict` with
tens of thousands of random operations, every problem solution was checked against a brute-force version, and the benchmarks and
simulations are real measurements.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain what a good hash function must do, why equal keys must have equal hashes, and why keys must be hashable (effectively immutable).
- Describe how Python's `hash()` behaves, including per-process randomization of string hashes, and implement `__eq__` and `__hash__`
  together correctly.
- Build a hash table with separate chaining, explain load factor and amortized resizing, and say when the O(1) bound fails.
- Compare chaining with open addressing (linear probing, tombstones, clustering), and explain why collisions arrive much sooner than
  intuition suggests.
- Describe how CPython's `dict` differs from a textbook table (open addressing, power-of-two sizes, a two-thirds load limit, insertion order).
- Recognize and apply the standard hash-based patterns: complement lookup, counting, membership, grouping, prefix sums, run detection,
  consistent mapping, and caching.

## 📋 Prerequisites

- [Time and Space Complexity](../time-and-space-complexity/README.md) — O(1) average, amortized, and worst-case reasoning.
- [Arrays](../arrays/README.md) — a hash table is built on an array; dynamic resizing mirrors the dynamic array.
- [Strings](../strings/README.md) — strings are the most common keys, and several examples reuse string problems.
- [Recursion](../recursion/README.md) — optional, for the memoization discussion.
- Basic Python reading ability — the examples use Python classes, dictionaries, and sets.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [hash-functions.md](hash-functions.md) | What makes a good hash, Python's `hash()`, hashable vs. unhashable, the equality contract, designing string hashes, cryptographic hashes, and Rabin–Karp |
| [hash-tables.md](hash-tables.md) | A chained hash table built from scratch and tested against `dict`, load factor, amortized resizing, the O(n) worst case, and how CPython's `dict` differs |
| [collision-handling.md](collision-handling.md) | The birthday effect, separate chaining, linear probing with tombstones, clustering measured against theory, and CPython's probe sequence |
| [hash-based-problem-solving.md](hash-based-problem-solving.md) | Eight patterns — two-sum, counting, sets, grouping, prefix sums, consecutive runs, mapping, LRU caching; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [hash-based-problem-solving.md](hash-based-problem-solving.md) if you are preparing for coding interviews: replacing a
nested loop with a dictionary lookup is the single most frequent optimization, and the prefix-sum and consecutive-sequence patterns
are common follow-ups. Also read [hash-tables.md](hash-tables.md) closely — "how does a hash table work, and when is it slow?" is a
standard question.

**Skim** [collision-handling.md](collision-handling.md) on a first pass if you only need to *use* dictionaries — but come back for
the tombstone and clustering sections if you want to understand why open-addressing tables resize early, or you may be asked to
implement one. Read the equality-contract sections of [hash-functions.md](hash-functions.md) before defining your own hashable classes.

## 🧠 Knowledge Check

<details>
<summary>Why is a dictionary lookup "O(1) on average" but "O(n) in the worst case"? What would cause the worst case?</summary>

A lookup hashes the key to pick a bucket (or the start of a probe sequence) and then examines only the few entries there. If the hash
function spreads keys evenly and the load factor is kept bounded by resizing, those few entries are a constant number on average.
The worst case occurs when many keys land in the same bucket — because of a poor hash function, or keys deliberately crafted to
collide — so a lookup must scan a chain or probe sequence containing a large fraction of all the keys: O(n). The measurement in
[hash-tables.md](hash-tables.md) shows a constant hash making operations quadratic overall.

</details>

<details>
<summary>You define a class with <code>__eq__</code> comparing two fields. You add instances to a set, then change one of those fields on an instance already in the set. What goes wrong?</summary>

If `__hash__` is built from the same fields as `__eq__`, changing a field changes the object's hash, but the set still stores the
object in the slot chosen by the *old* hash. A later lookup computes the new hash, looks in the wrong slot, and fails to find the
object — even though it is still in the set (its `len` is unchanged). The object is effectively lost inside the table. Keys must
not change while they are stored, which is why hashable types are normally immutable. See
[hash-functions.md](hash-functions.md).

</details>

## 📚 References

- [Python docs: `object.__hash__` (data model)](https://docs.python.org/3/reference/datamodel.html) — the hash/equality contract and mutable-key warning.
- [Python docs: `PYTHONHASHSEED`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED) and [PEP 456](https://peps.python.org/pep-0456/) — hash randomization and the string hash algorithm.
- [Python docs: `collections`](https://docs.python.org/3/library/collections.html) — `Counter`, `defaultdict`, and `OrderedDict`.
- [Python wiki: TimeComplexity](https://wiki.python.org/moin/TimeComplexity) — average and worst-case costs of `dict` and `set` operations.
- [CPython source: `Objects/dictobject.c`](https://github.com/python/cpython/blob/3.9/Objects/dictobject.c) — the implementation notes on open addressing, probing, and the two-thirds load limit.
- [Wikipedia: Linear probing](https://en.wikipedia.org/wiki/Linear_probing) — expected probe counts, clustering, and deletion strategies.
- [OWASP: Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) — why a plain fast hash is the wrong tool for passwords.
- [W3Schools: DSA Hash Tables](https://www.w3schools.com/dsa/dsa_theory_hashtables.php) and [Python Dictionaries](https://www.w3schools.com/python/python_dictionaries.asp) — beginner-friendly introductions.
- [GeeksforGeeks: Hashing Data Structure](https://www.geeksforgeeks.org/dsa/hashing-data-structure/) — an overview of hashing, collision handling, and common problems.

## ➡️ Continue Your Learning Path

Continue to the Linked Lists module, the next module in this domain, where data is connected by references instead of stored side by
side.
