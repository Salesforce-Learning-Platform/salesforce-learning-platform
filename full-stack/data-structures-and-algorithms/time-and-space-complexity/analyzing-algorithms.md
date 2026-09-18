# 🔍 Analyzing Algorithms

## Turning Code Into a Big-O Classification

[big-o-notation.md](big-o-notation.md) defined the complexity classes themselves. This file covers
the genuinely practical skill: reading actual code and determining *which* complexity class it
belongs to, using a small set of repeatable rules rather than guesswork.

## Rule 1: Sequential Statements Add

```python
def process(items):
    print(items[0])        # O(1)
    total = sum(items)     # O(n)
    print(total)            # O(1)
```

```
Sequential steps' complexities are ADDED, then the DOMINANT term
is kept: O(1) + O(n) + O(1) = O(n) overall - the constant-time
steps become genuinely insignificant next to the O(n) step.
```

## Rule 2: Loops Multiply by Their Iteration Count

```python
def print_all(items):        # a SINGLE loop over n items
    for item in items:         # → O(n)
        print(item)

def print_pairs(items):      # a NESTED loop, each running n times
    for a in items:            # → O(n) * O(n) = O(n²)
        for b in items:
            print(a, b)
```

A single loop over `n` items is O(n); a loop nested inside another loop, both running over the same
input, multiplies to O(n²) — directly the same nested-loop pattern already shown in
`has_duplicate` in [big-o-notation.md](big-o-notation.md).

## Rule 3: Halving the Input Each Step Means O(log n)

```python
def binary_search(sorted_items, target):   # per what-are-
    low, high = 0, len(sorted_items) - 1     # algorithms.md,
    while low <= high:                        # previous module
        mid = (low + high) // 2
        if sorted_items[mid] == target:
            return mid
        elif sorted_items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

```
Each iteration ELIMINATES HALF the remaining search space - so
the number of iterations needed is the number of times n can be
HALVED before reaching 1, which is PRECISELY log₂(n).
```

Any algorithm that repeatedly *halves* the problem it's working on — not just binary search —
follows this same O(log n) pattern.

## Rule 4: Sequential Loops Add, Nested Loops Multiply

```python
def summarize(items):
    for item in items:          # LOOP 1: O(n)
        print(item)
    for item in items:          # LOOP 2: O(n), SEPARATE from Loop 1
        print(item * 2)
    # total: O(n) + O(n) = O(2n) → simplifies to O(n)
```

This is a genuinely common point of confusion worth being precise about: two *sequential*,
back-to-back loops over the same input **add** (O(n) + O(n) = O(n)); two *nested* loops
**multiply** (O(n) * O(n) = O(n²)) — the difference is whether one loop runs *inside* the other, or
merely *after* it.

## Rule 5: Focus on the Worst Case Unless Stated Otherwise

```
Big-O analysis, unless explicitly stated otherwise, describes the
WORST CASE - the scenario requiring the MOST work.

linear_search's worst case: the target is the LAST element
checked, or ISN'T present at all → O(n)

linear_search's BEST case: the target is the FIRST element
checked → O(1) - but this is NOT what "linear_search is O(n)"
actually refers to.
```

Worst-case analysis is the genuinely conservative, safe default — it guarantees an algorithm won't
perform *worse* than its stated complexity, regardless of the specific input it happens to receive.

## A Complete Worked Example

```python
def find_common_elements(list_a, list_b):
    common = []
    for a in list_a:              # O(n) outer loop
        for b in list_b:            # O(m) inner loop
            if a == b:
                common.append(a)
                break
    return common
# Overall: O(n * m) - a NESTED loop over two DIFFERENT-sized
# inputs, so the two input sizes are kept SEPARATE rather than
# both being called "n"
```

This worked example is worth studying closely — when two loops iterate over *different* collections
of potentially different sizes, using separate variables (`n` and `m`) instead of assuming both are
the same size produces a genuinely more accurate, honest complexity analysis.

## Common Mistakes

- Assuming every loop is automatically O(n), without checking whether it's nested inside another
  loop (making it O(n²)) or merely sequential with another loop (keeping it O(n)).
- Analyzing an algorithm's best case and reporting it as the algorithm's overall complexity, rather
  than the conventionally-used worst case.
- Treating two different input collections as both being size "n," obscuring a more precise and
  honest O(n * m) analysis.

## ➡️ Next

Continue to [time-complexity.md](time-complexity.md) to see time complexity examined in full depth,
across a complete, worked reference table of common operations.
