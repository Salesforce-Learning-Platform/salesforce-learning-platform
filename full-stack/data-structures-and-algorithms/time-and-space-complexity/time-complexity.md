# ⏱️ Time Complexity

## The Growth Rate of an Algorithm's Running Time

[analyzing-algorithms.md](analyzing-algorithms.md) covered the *rules* for classifying code.
**Time complexity** is specifically the application of those rules to an algorithm's *running
time* — how the number of operations grows as input size grows. This file consolidates that view
into a single, complete reference.

## A Reference Table of Common Operations

```
OPERATION                              TIME COMPLEXITY
Array access by index                  O(1)
Array search (unsorted)                O(n)
Array search (sorted, binary search)   O(log n)
Array insertion/deletion at END        O(1)  (amortized)
Array insertion/deletion at START      O(n)  (every element shifts)
Hash map get/set (average case)        O(1)
Hash map get/set (worst case)          O(n)  (all keys collide)
Sorting (comparison-based, optimal)    O(n log n)
Nested loop over same input            O(n²)
```

This table directly previews the specific data structures this domain covers next — Arrays,
Linked Lists, Hashing, and beyond each build on exactly this same time-complexity vocabulary,
applied to their own specific operations.

## Why Array Insertion at the Start Is O(n)

```python
items = [1, 2, 3, 4, 5]
items.insert(0, 0)   # inserting AT THE START
# RESULT: [0, 1, 2, 3, 4, 5]
```

```
Inserting at INDEX 0 requires shifting EVERY existing element one
position to the right, to make room - for n existing elements,
that's n shift operations → O(n).

Inserting at the END (items.append(6)) requires NO shifting at
all → O(1).
```

This distinction is genuinely important and will recur directly in
[Arrays](../arrays/insertion-and-deletion.md), later in this domain — *where* in a structure an
operation happens can change its complexity dramatically, even for the same structure.

## Average Case vs. Worst Case, Concretely: Hash Maps

```
A well-implemented hash map's GET/SET is O(1) on AVERAGE - the
hash function distributes keys evenly across available "buckets,"
so any single lookup touches very few elements.

The WORST case - every key hashing to the SAME bucket (a
"collision") - degrades to O(n), since all colliding keys must
then be searched linearly within that one bucket.
```

This is exactly the same reason [caching-strategies.md](../../system-design/high-level-design/core-infrastructure/caching-strategies.md),
covered earlier in the System Design domain, treats a well-tuned hash-based cache lookup as
effectively constant-time in practice — genuine hash collisions are rare with a well-designed hash
function, even though the theoretical worst case remains O(n).

## Comparing Two Algorithms for the Same Problem, Concretely

```python
def contains_duplicate_slow(items):     # O(n²)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False

def contains_duplicate_fast(items):     # O(n)
    seen = set()
    for item in items:
        if item in seen:      # O(1) average-case hash set lookup
            return True
        seen.add(item)
    return False
```

Both functions solve the *exact* same problem, correctly — but `contains_duplicate_fast` trades a
small amount of extra memory (the `seen` set) for a dramatically better time complexity, going from
O(n²) to O(n). This exact trade-off — memory for speed — is precisely what
[space-complexity.md](space-complexity.md), the next file, examines formally.

## Common Mistakes

- Assuming all data structure operations of the "same kind" (like insertion) have identical time
  complexity, regardless of *where* in the structure the operation happens.
- Treating a hash map's average-case O(1) as a guaranteed worst-case bound, rather than a
  genuinely different, weaker worst-case guarantee.
- Comparing two algorithms only by their time complexity, without considering the space complexity
  trade-off often required to achieve a faster running time.

## ➡️ Next

Continue to [space-complexity.md](space-complexity.md) to examine the other half of this trade-off:
how much memory an algorithm actually requires.
