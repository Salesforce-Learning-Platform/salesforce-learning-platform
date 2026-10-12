# #️⃣ Hash Functions

## Turning Any Key Into a Number

Finding an item in an unsorted array takes O(n) steps, and even a sorted array needs O(log n). A **hash table**
(next file, [hash-tables.md](hash-tables.md)) aims for **O(1) on average** by *computing* where an item lives instead of
searching for it. The computation is done by a **hash function**: a function that turns a key — a string, a number, a tuple — into
an integer. That integer, reduced to the size of the table, picks a slot.

This file is about the function itself: what makes a good one, how Python's built-in `hash()` behaves, why some objects
cannot be hashed, and what goes wrong with a poorly designed function. All outputs were produced by running the code on
CPython 3.9.

## ✅ What a Good Hash Function Must Do

| Property | Meaning | Why a hash table needs it |
|----------|---------|---------------------------|
| **Deterministic** | The same key gives the same value (within one run of the program) | Otherwise the key can never be found again |
| **Consistent with equality** | If `a == b`, then `hash(a) == hash(b)` | Equal keys must land in the same slot |
| **Uniform** | Keys spread evenly across the possible values | Otherwise many keys pile into few slots |
| **Fast** | Cheap to compute, proportional to the key's size | The O(1) promise includes the cost of hashing |
| **Uses the whole key** | Every part of the key affects the result | Otherwise similar keys collide systematically |

The second row is a *one-way* rule: equal keys **must** have equal hashes, but different keys are *allowed* to share a hash
(a **collision**). Collisions are unavoidable — there are far more possible keys than hash values — and
[collision-handling.md](collision-handling.md) shows how tables cope with them.

## 🐍 Python's Built-In `hash()`

Python's `hash(obj)` returns an integer for any *hashable* object, and dictionaries and sets use it internally:

```python
print(hash(5))                       # 5        — small integers hash to themselves
print(hash(-1), hash(-2))            # -2 -2    — -1 is reserved internally, so it becomes -2 (a collision!)
print(hash(1.0) == hash(1) == hash(True))    # True   — they compare equal, so their hashes must match
print(hash((1, 2)) == hash((1, 2)))          # True   — equal tuples hash equally
print({1: "a", 1.0: "b", True: "c"})       # {1: 'c'}   — one key; the later values overwrite the earlier
```

Two things to notice. First, `hash(-1)` and `hash(-2)` are both `-2`: even Python's own function has collisions, which is
perfectly legal. Second, `1.0`, `1`, and `True` compare equal, so they *must* share a hash — which is why
`{1: "a", 1.0: "b", True: "c"}` is a dictionary with a single key.

### String Hashes Change Between Runs

For strings (and bytes), Python deliberately **randomizes** the hash value every time the interpreter starts. Two separate
runs hash the same text to different numbers:

```python
import os
import subprocess
import sys

def hash_of_hello(seed=None):
    env = dict(os.environ)
    env.pop("PYTHONHASHSEED", None)
    if seed is not None:
        env["PYTHONHASHSEED"] = str(seed)
    result = subprocess.run([sys.executable, "-c", "print(hash('hello'))"],
                            env=env, capture_output=True, text=True)
    return result.stdout.strip()

print(hash_of_hello() == hash_of_hello())           # False   — randomized per process
print(hash_of_hello(0) == hash_of_hello(0))         # True    — a fixed seed makes it repeatable
```

This is a security feature. If an attacker knew exactly how strings hash, they could craft many keys that all collide and
make a server's dictionary degrade to O(n) per operation — a *hash-flooding* denial of service. Randomizing the hash per
process closes that door (the behavior is documented under the
[`PYTHONHASHSEED`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED) setting). The consequence for
you: **never store `hash()` values in files or databases, and never rely on the iteration order of a `set` of strings
being the same between runs.** Within one run, equal strings always have equal hashes.

## 🔒 Hashable Means Immutable (in Practice)

A key's hash must not change while it sits in a table, so Python only lets you use objects whose hash is fixed by their
content:

```python
for obj in ([1, 2], {"a": 1}, {1, 2}, ([1], 2)):
    try:
        hash(obj)
    except TypeError as error:
        print(error)
```

```text
unhashable type: 'list'
unhashable type: 'dict'
unhashable type: 'set'
unhashable type: 'list'
```

Lists, dictionaries, and sets are mutable, so they are unhashable — and so is a tuple that *contains* one. Their
immutable counterparts work: tuples of hashable items, strings, numbers, `frozenset`, and `bytes`. This is why the
anagram-grouping example in [string-patterns.md](../strings/string-patterns.md) used a `tuple` of counts as the dictionary
key rather than a list.

## 🤝 The Equality Contract for Your Own Classes

When you define `__eq__` on a class, Python assumes instances might be mutable and **removes** the default hash:

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

try:
    hash(Point(1, 2))
except TypeError as error:
    print(error)           # unhashable type: 'Point'
```

To make instances usable as keys, define `__hash__` consistently with `__eq__` — the Python documentation advises hashing
a tuple of the same components that `__eq__` compares:

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

visited = {Point(1, 2), Point(3, 4)}
print(Point(1, 2) in visited)      # True    — a different object, but equal and with an equal hash
print(len({Point(1, 2), Point(1, 2)}))   # 1
```

Equal objects have equal hashes, so the lookup finds the right slot, and `==` then confirms the match. The danger is
**mutating a key after it has been stored**: its hash changes, but the table still has it under the old slot.

```python
point = Point(1, 2)
seen = {point}
point.x = 99                       # the hash is now different from the one used to store it
print(point in seen)               # False   — looked in the wrong slot
print(len(seen))                   # 1       — yet it is still in the set
```

The object is stuck in the table where lookups can never reach it. Keep hashed fields immutable (a `frozen`
`dataclass` or a `tuple`/`namedtuple` does this for you).

## 🧪 Designing a Hash Function for Strings

How would you turn a string into a number? Three attempts show what separates a good function from a bad one. We test
each on two data sets: all 5,040 **anagrams** of `"abcdefg"` (the same letters in every order — a tough case), and 10,000
random six-letter words.

```python
import itertools
import random

def sum_of_ords(text):                    # attempt 1: add up the character codes
    return sum(ord(ch) for ch in text)

def polynomial(text):                     # attempt 2: h = h * 31 + code, like a number in base 31
    h = 0
    for ch in text:
        h = h * 31 + ord(ch)
    return h

def djb2(text):                           # attempt 3: Daniel Bernstein's well-known "djb2"
    h = 5381
    for ch in text:
        h = h * 33 + ord(ch)
    return h

def spread(hash_function, words, buckets=101):
    counts = [0] * buckets
    for word in words:
        counts[hash_function(word) % buckets] += 1
    used = sum(1 for count in counts if count)
    return f"distinct hash values {len({hash_function(w) for w in words}):>5} | buckets used {used:>3}/{buckets} | largest bucket {max(counts):>5}"

anagrams = ["".join(p) for p in itertools.permutations("abcdefg")]
random.seed(2)
words = ["".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(6)) for _ in range(10000)]

print("5,040 anagrams of 'abcdefg'")
for function in (sum_of_ords, polynomial, djb2):
    print(f"  {function.__name__:12} {spread(function, anagrams)}")

print("10,000 random 6-letter words (ideal: about 99 per bucket)")
for function in (sum_of_ords, polynomial, djb2):
    print(f"  {function.__name__:12} {spread(function, words)}")
```

```text
5,040 anagrams of 'abcdefg'
  sum_of_ords  distinct hash values     1 | buckets used   1/101 | largest bucket  5040
  polynomial   distinct hash values  5040 | buckets used 101/101 | largest bucket    67
  djb2         distinct hash values  5040 | buckets used 101/101 | largest bucket    66
10,000 random 6-letter words (ideal: about 99 per bucket)
  sum_of_ords  distinct hash values   117 | buckets used 101/101 | largest bucket   239
  polynomial   distinct hash values 10000 | buckets used 101/101 | largest bucket   131
  djb2         distinct hash values 10000 | buckets used 101/101 | largest bucket   129
```

Reading the results:

- **`sum_of_ords` is a disaster on anagrams.** Addition ignores order, so *every* permutation of the same letters has the
  same sum: 5,040 keys, **one** hash value, one bucket holding all of them. A hash table built on it would behave like
  a single linked list — O(n) lookups. On random words it fills every bucket but produces only 117 distinct values for 10,000 words, and the largest bucket
  holds more than twice the ideal share.
- **`polynomial` and `djb2` are both good.** Multiplying by a constant before adding each character makes *position*
  matter: `"ab"` and `"ba"` hash differently. Anagrams spread across all 101 buckets with the largest holding about
  1.3 times the average; random words are close to the ideal.

The lesson: **a hash function must depend on every part of the key, including order.** (Python's real string hash is more
sophisticated — it is keyed with the random per-process secret mentioned above — but it follows the same principle.)

### The Table Size Matters Too

Turning a big hash into a slot number uses a remainder: `slot = hash % table_size`. A badly chosen size can waste slots when
the keys have a pattern. Keys that are all multiples of 10, in a table of 16 versus 17 slots:

```python
keys = range(0, 1000, 10)
for size in (16, 17):
    print(f"{size} slots: {len({key % size for key in keys})} used")
```

```text
16 slots: 8 used
17 slots: 17 used
```

With 16 slots only 8 are ever used, because `10 × k mod 16` can only be even — half the table is wasted, and the keys crowd
into the other half. With 17 (a prime) every slot is reachable. This is why textbooks recommend **prime table sizes** for
simple hash functions. Python's dictionaries instead use powers of two (cheap to compute) and compensate by *mixing the
higher bits of the hash into the probe sequence*, as described in [collision-handling.md](collision-handling.md).

## 🔐 Cryptographic Hashes Are a Different Tool

The same word "hash" also names functions like SHA-256, used for integrity checks and digital signatures. They have
different goals: infeasible to reverse, infeasible to find two inputs with the same output, and a tiny change in the input
should scramble the whole output (the **avalanche effect**):

```python
import hashlib

a = hashlib.sha256(b"hello").hexdigest()
b = hashlib.sha256(b"hellp").hexdigest()          # one letter changed
print(a)
print(b)
different_bits = bin(int(a, 16) ^ int(b, 16)).count("1")
print(different_bits, "of 256 bits differ")
```

```text
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
fdd7585e08c4e2afd71dcabdb4636c89d557a3f42db9e2040c8bbd1708aa4ce7
131 of 256 bits differ
```

Changing one letter flipped 131 of the 256 output bits — about half, as expected for a well-mixed function. Always the same
output for the same input (SHA-256 is deterministic and, unlike `hash()`, is **not** randomized per run), which makes it
suitable for checksums. But cryptographic hashes are slower than the functions hash tables use, so dictionaries do not use
them. And a plain fast hash is the wrong tool for storing passwords: use a dedicated, deliberately slow password-hashing
scheme ([OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)).

## 🔁 A Hash Function at Work: Rolling Hashes and Rabin–Karp

[string-patterns.md](../strings/string-patterns.md) searched for a pattern in a text with the naive method (re-compare
every window) and with KMP. **Rabin–Karp** takes a hashing approach: compute a hash of the pattern, then slide a window
across the text comparing *hashes*, which are single numbers and therefore cheap to compare. The trick that makes this
fast is a **rolling hash**: when the window moves one character, the new hash is computed from the old one in O(1) by
removing the leaving character's contribution and adding the arriving one.

Treat the characters as digits of a number in base 256 and take everything modulo a large prime:

```python
def rabin_karp(text, pattern, base=256, modulus=1_000_000_007, stats=None):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    high = pow(base, m - 1, modulus)               # the weight of the window's leading character
    target = window = 0
    for i in range(m):
        target = (target * base + ord(pattern[i])) % modulus
        window = (window * base + ord(text[i])) % modulus

    matches = []
    for start in range(n - m + 1):
        if window == target:                         # hashes agree: it MIGHT be a match
            if text[start:start + m] == pattern:     # so verify the characters
                matches.append(start)
            elif stats is not None:
                stats["false_alarms"] += 1           # a collision: same hash, different text
        if start + m < n:                            # roll: drop text[start], add text[start + m]
            window = ((window - ord(text[start]) * high) * base + ord(text[start + m])) % modulus
    return matches

print(rabin_karp("ababcabababc", "abab"))          # [0, 5, 7]
print(rabin_karp("hello world", "xyz"))            # []


text = "the quick brown fox jumps over the lazy dog " * 3
for modulus in (7, 101, 1_000_000_007):
    stats = {"false_alarms": 0}
    matches = rabin_karp(text, "fox", modulus=modulus, stats=stats)
    print(f"modulus {modulus:>13,}: matches {matches}, false alarms {stats['false_alarms']}")
```

```text
[0, 5, 7]
[]
modulus             7: matches [16, 60, 104], false alarms 24
modulus           101: matches [16, 60, 104], false alarms 6
modulus 1,000,000,007: matches [16, 60, 104], false alarms 0
```

Two lessons. The **verification step is essential**: because different strings can share a hash, a hash match is only
a *candidate*. With a tiny modulus (7) the search hit 24 false alarms — windows whose hash equalled the pattern's
without the text being equal — and the character comparison discarded every one, so the answer is the same at every
modulus. With a large prime modulus false alarms are rare (none here), so the expected time is **O(n + m)**, but a
worst case with many collisions degrades to O(n · m). And the **O(1) roll** is what a hash function that "uses the whole key" can
sometimes offer: one that is *incrementally updatable*. Rabin–Karp's real strength is searching for *many* patterns at
once, where one rolling hash can be compared against a whole set of pattern hashes (using the hash tables of the next file).

## 🧭 Summary

- A hash function maps a key to an integer; a table turns it into a slot with `% size`.
- Required: deterministic within a run, equal keys → equal hashes, uniform, fast, sensitive to the whole key.
- Python's `hash()` is randomized for strings per process; keys must be hashable (effectively immutable).
- Define `__eq__` and `__hash__` together, from the same fields, and never mutate a hashed key.
- Bad functions (sum of characters) create clusters; good ones (polynomial/djb2 style) spread keys.
- Cryptographic hashes serve different goals and are not used inside hash tables.

## Common Mistakes

- **Using a hash that ignores order** (sum of characters), making anagrams collide.
- **Storing `hash()` results** across runs or machines and expecting the same values.
- **Mutating an object after using it as a key**, losing it inside the table.
- **Defining `__eq__` without `__hash__`**, or `__hash__` from different fields than `__eq__` compares.
- **Trusting a hash match as proof of equality** — always confirm candidates (as Rabin–Karp does).
- **Assuming the hash alone decides the slot** — the table size and collision strategy matter just as much.
- **Using fast non-cryptographic hashes for security**, or cryptographic hashes where a hash table needs speed.

## ➡️ Next

Continue to [hash-tables.md](hash-tables.md) to see how a hash function and an array combine into the data structure behind
Python's `dict` and `set` — built from scratch, tested, and measured.
