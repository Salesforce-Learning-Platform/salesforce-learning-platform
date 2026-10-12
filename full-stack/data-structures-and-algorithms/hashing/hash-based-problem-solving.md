# 🧰 Hash-Based Problem Solving

## Trading Memory for Time

Most hash-table problems are solved with one move: **replace a search with a lookup.** A nested loop that asks "is there another
element that…?" becomes a single pass that stores what it has seen in a dictionary or set and asks the table in O(1)
(on average — see [hash-tables.md](hash-tables.md)). You pay O(n) extra memory and save a factor of n in time.

This file collects the patterns that appear again and again — lookup by complement, counting, membership, grouping, prefix
sums, run detection, consistent mapping, and caching — each with a worked problem. Every function was tested against a brute-force
version on thousands of random inputs, and every printed output was produced by running the code on CPython 3.9.

## 🎯 Pattern 1: Look Up the Complement (Two Sum)

*Given a list of numbers and a target, find two positions whose values add up to the target.* The brute force tries every pair —
O(n²) — as in the `has_pair_brute` function in [two-pointer-technique.md](../arrays/two-pointer-technique.md), which then uses
sorting plus two pointers. A hash table needs no sorting. For each value, the number it needs is `target − value`. If that number
was seen earlier, you are done; otherwise remember this value:

```python
def two_sum(numbers, target):
    seen = {}                                # value -> index where it was seen
    for index, value in enumerate(numbers):
        complement = target - value
        if complement in seen:               # O(1) average lookup replaces an inner loop
            return seen[complement], index
        seen[value] = index
    return None

print(two_sum([2, 7, 11, 15], 9))       # (0, 1)
print(two_sum([3, 2, 4], 6))            # (1, 2)
print(two_sum([3, 3], 6))               # (0, 1)   — equal values at two different positions
print(two_sum([1, 2, 3], 100))          # None
```

One pass, **O(n) time, O(n) space**. Storing a value only *after* checking for its complement prevents a number from pairing with
itself (so `two_sum([3], 6)` is `None`). Compared with the sorted two-pointer solution (O(n log n) time, O(1) extra space), this
spends memory to avoid sorting and keeps the original indexes — a trade-off worth naming in an interview.

## 🔢 Pattern 2: Counting

Counting how many times each value appears is the most common hash-table job. `collections.Counter` is a dictionary specialised for
it:

```python
from collections import Counter

counts = Counter("mississippi")
print(counts)                            # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
print(counts["s"], counts["z"])          # 4 0   — a missing key counts as zero, with no KeyError
print(counts.most_common(2))             # [('i', 4), ('s', 4)]

words = "the cat and the hat and the bat".split()
print(Counter(words).most_common(1))     # [('the', 3)]
```

`Counter` is built in one O(n) pass. Counting is the first half of many solutions: *the first non-repeating character*, *is this an
anagram?*, *which element appears more than n/2 times?*, and the character counts in
[string-patterns.md](../strings/string-patterns.md) all follow the same two steps — count everything, then answer from the counts.

## ✅ Pattern 3: Membership and Duplicates

A **set** answers "have I seen this?" in O(1). Three problems solved with it:

```python
def has_duplicate(items):
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False

def first_recurring(items):
    seen = set()
    for item in items:
        if item in seen:
            return item                      # the first value whose second occurrence appears earliest
        seen.add(item)
    return None

def common_elements(a, b):
    return sorted(set(a) & set(b))           # set intersection: O(len(a) + len(b)) on average

print(has_duplicate([4, 1, 7, 1]))              # True
print(first_recurring(list("acbbac")))          # b
print(common_elements([1, 2, 2, 3], [2, 3, 4])) # [2, 3]
```

`has_duplicate` is the improvement on the nested-loop `has_duplicate` from
[big-o-notation.md](../time-and-space-complexity/big-o-notation.md): O(n) time and O(n) space instead of O(n²) time and
O(1) space. Notice how it differs from `len(set(items)) != len(items)`: that is shorter, but it always builds the whole set,
while the loop above stops at the first repeat.

## 🗂️ Pattern 4: Group by a Canonical Key

When items must be bucketed by some property, compute a **canonical key** for each item and use it as the dictionary key. The
anagram grouping in [string-patterns.md](../strings/string-patterns.md) is the model: the sorted letters (or a tuple of letter counts)
identify each group. The same shape groups numbers by remainder, words by length, or records by city:

```python
from collections import defaultdict

def group_by(items, key):
    groups = defaultdict(list)               # a missing key starts as an empty list
    for item in items:
        groups[key(item)].append(item)
    return dict(groups)

print(group_by(range(10), lambda n: n % 3))
# {0: [0, 3, 6, 9], 1: [1, 4, 7], 2: [2, 5, 8]}
print(group_by(["pear", "fig", "plum", "kiwi", "apple"], len))
# {4: ['pear', 'plum', 'kiwi'], 3: ['fig'], 5: ['apple']}
```

The key must be hashable and must produce *equal keys for items that belong together* — the equality contract from
[hash-functions.md](hash-functions.md). (`itertools.groupby` only groups *consecutive* items, and its documentation notes
the input generally needs to be sorted by the same key first — so for unsorted data this dictionary pattern is the usual tool.)

## ➕ Pattern 5: Prefix Sums With a Hash Map

*Count the contiguous subarrays whose elements add up to `k`* — in an array that may contain **negative numbers**, which breaks the
sliding-window approach in [sliding-window.md](../arrays/sliding-window.md). The key observation: let `prefix[i]` be the sum of the
first `i` elements. The subarray between positions `i` and `j` sums to `prefix[j] − prefix[i]`. So a subarray ending at `j` sums to
`k` exactly when some earlier prefix equals `prefix[j] − k`. Store how many times each prefix sum has occurred:

```python
def count_subarrays_with_sum(numbers, k):
    count = 0
    prefix = 0
    seen = {0: 1}                            # prefix sum -> how many times it has occurred (empty prefix: 0)
    for value in numbers:
        prefix += value
        count += seen.get(prefix - k, 0)     # earlier prefixes that leave exactly k in between
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

print(count_subarrays_with_sum([1, 1, 1], 2))            # 2     — [1,1] twice
print(count_subarrays_with_sum([1, 2, 3], 3))            # 2     — [1,2] and [3]
print(count_subarrays_with_sum([2, -1, 2, 3, -2, 5], 5)) # 2     — [2, 3] and [5], found despite the negative numbers
```

The initial entry `{0: 1}` represents the empty prefix and handles subarrays that start at the very beginning. One pass: **O(n) time,
O(n) space**, versus O(n²) for checking every start and end. This "prefix sum + hash map" pairing reappears whenever a
question asks for subarrays with a given sum, equal counts, or a given remainder.

## 🔗 Pattern 6: The Longest Run of Consecutive Numbers

*Given an unsorted list, find the length of the longest run of consecutive integers (such as 100, 101, 102…) in O(n) time.* Sorting
would cost O(n log n). With a set, a number can ask directly whether its neighbours exist. The trick for staying linear is to start
counting only at the **beginning** of a run:

```python
def longest_consecutive(numbers):
    present = set(numbers)
    best = 0
    for value in present:
        if value - 1 not in present:         # value is the start of a run
            length = 1
            while value + length in present:
                length += 1
            best = max(best, length)
    return best

print(longest_consecutive([100, 4, 200, 1, 3, 2]))        # 4    — the run 1, 2, 3, 4
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))# 9    — 0 through 8
print(longest_consecutive([]))                             # 0
```

Why is the nested loop still O(n)? The inner `while` only runs for the first number of each run, and it walks that run once. Every element
is therefore visited a constant number of times across the whole function — the same kind of amortized argument used for
sliding windows. Remove the `value - 1 not in present` guard and each element of a long run would walk the rest of the run,
making it O(n²).

## 🔁 Pattern 7: Consistent Mapping

*Do two strings have the same shape — can the characters of one be replaced one-for-one to produce the other?* (`"egg"` and `"add"`
do; `"foo"` and `"bar"` do not; `"badc"` and `"baba"` do not, because two different letters would map to the same one.) The mapping
must be consistent in both directions, so keep two dictionaries:

```python
def is_isomorphic(a, b):
    if len(a) != len(b):
        return False
    forward, backward = {}, {}
    for x, y in zip(a, b):
        if forward.setdefault(x, y) != y or backward.setdefault(y, x) != x:
            return False                     # x was already mapped elsewhere, or y was already claimed
    return True

print(is_isomorphic("egg", "add"))       # True
print(is_isomorphic("foo", "bar"))       # False
print(is_isomorphic("badc", "baba"))     # False
print(is_isomorphic("paper", "title"))   # True
```

`dict.setdefault(key, default)` returns the existing value if the key is present and otherwise stores and returns the default, so
the first time a character is seen it is recorded, and every later occurrence is checked against that record. One pass, O(n)
time.

## 💾 Pattern 8: Caching (and the LRU Cache)

A dictionary is also a **cache**: store the result of an expensive computation under its inputs and reuse it. This is what
`functools.lru_cache` did to the Fibonacci recursion in [recursion-tree.md](../recursion/recursion-tree.md). A cache cannot grow forever, so a
common design question is the **Least Recently Used (LRU) cache**: a fixed capacity, where adding an item beyond capacity evicts the one
that was used least recently. Both `get` and `put` must be O(1).

That needs two things at once: a hash table for O(1) lookup, and a way to track *recency order* with O(1) updates.
Python's `collections.OrderedDict` is exactly that combination — its source describes a dictionary mapping keys to links in a
doubly linked list, with the same Big-O as a regular dictionary — and it offers `move_to_end` and `popitem(last=False)`:

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self._capacity = capacity
        self._items = OrderedDict()           # order = least recently used first, most recently used last

    def get(self, key):
        if key not in self._items:
            return None
        self._items.move_to_end(key)          # mark as most recently used
        return self._items[key]

    def put(self, key, value):
        if key in self._items:
            self._items.move_to_end(key)
        self._items[key] = value
        if len(self._items) > self._capacity:
            self._items.popitem(last=False)   # evict the least recently used entry

cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
print(cache.get("a"))        # 1     — "a" is now the most recently used
cache.put("c", 3)            # capacity exceeded: evicts "b", the least recently used
print(cache.get("b"))        # None
print(cache.get("a"), cache.get("c"))   # 1 3
```

Without `OrderedDict`, the standard from-scratch answer pairs a dictionary with your own doubly linked list (covered in the Linked Lists module later
in this domain). The principle is general: **a hash table gives fast access by key; pair it with another structure when you also
need order.**

## 📋 Choosing the Pattern

| The problem says… | Reach for… | Typical result |
|-------------------|------------|----------------|
| "find two items that…", "is there another item such that…" | Dictionary of seen values; look up the complement | O(n) time, O(n) space |
| "how many of each", "most frequent", "anagram" | `Counter` / dictionary of counts | O(n) |
| "any duplicates?", "have I seen this?", "in both lists" | `set` | O(n) |
| "group by…" | `defaultdict(list)` keyed by a canonical form | O(n) |
| "subarrays with sum / count / remainder…" (negatives allowed) | Prefix sums + dictionary of counts | O(n) |
| "longest consecutive…" in unsorted data | Set + start only at run beginnings | O(n) |
| "same pattern / one-to-one mapping" | Two dictionaries, one per direction | O(n) |
| "cache", "evict the least recently…" | `OrderedDict` (or dict + linked list) | O(1) per operation |

## ⚖️ Trade-Offs to Mention

- **Space for time.** Every pattern uses O(n) extra memory. If memory is the constraint, sorting plus two pointers may be the better answer.
- **Average vs. worst case.** "O(1)" means average; a poor hash or adversarial keys degrade it, as shown in
  [hash-tables.md](hash-tables.md).
- **Hashable keys only.** Convert lists to tuples (or strings) before using them as keys.
- **Order.** If the answer must be sorted or in sorted order, a hash table does not provide it; sort at the end if needed.
- **Small inputs.** For tiny lists, a plain scan is as fast and simpler.

## Common Mistakes

- **Inserting before checking** in "seen" problems, letting an element match itself (the two-sum bug).
- **Forgetting the empty-prefix entry** `{0: 1}` in prefix-sum counting.
- **Starting a run at every number** in the consecutive-sequence problem, turning O(n) into O(n²).
- **Using a one-directional map** for isomorphic strings, so two letters can map to one.
- **Using lists or other mutable values as keys** (`TypeError: unhashable type`).
- **Using `dict[key]` for counting** without handling the missing key — use `get`, `defaultdict`, or `Counter`.
- **Mutating a dictionary while iterating over it.**
- **Assuming a hash-based solution is always faster**, ignoring the memory it uses.

## Module Summary

The Hashing module turned "search" into "compute where it lives." [Hash Functions](hash-functions.md) covered what a good hash does,
how Python's `hash()` behaves (randomized strings, hashable-means-immutable), the equality contract, and how poorly designed functions
cluster. [Hash Tables](hash-tables.md) built a chained table from scratch, explained load factor and amortized resizing, and
compared it with CPython's `dict`. [Collision Handling](collision-handling.md) showed why collisions arrive early, and compared chaining with
open addressing (linear probing, tombstones, clustering, CPython's probe recurrence). This file applied the structure to eight
patterns.

Carry these ideas forward:

- A hash table gives O(1) average lookup, insert, and delete — given a good hash function and a bounded load factor.
- Equal keys must have equal hashes; keys must be hashable (effectively immutable).
- Collisions are inevitable and early; the strategy (chaining or probing) and the load factor determine how well a table copes.
- Most hash-based solutions are "single pass, remember what you have seen" — O(n) time bought with O(n) space.
- Later modules lean on this: graph algorithms track visited nodes in sets, dynamic programming caches in dictionaries, and tries build on
  dictionary-like children.

## ➡️ Next

Continue to the Linked Lists module, the next module in this domain, where data is connected by references instead of stored side by
side — and where the LRU cache's linked-list half is built by hand.
