# 📈 Big-O Notation

## A Precise Language for the Performance Difference Already Observed

[what-are-algorithms.md](../introduction-to-data-structures-and-algorithms/what-are-algorithms.md),
the previous module, showed `linear_search` and `binary_search` behaving very differently as input
size grows — but only described this difference informally. **Big-O notation** is the formal,
precise, universally-used language for describing exactly *how* an algorithm's performance scales
as its input grows.

## What Big-O Actually Measures

```
Big-O describes an algorithm's GROWTH RATE as input size (n)
GROWS TOWARD INFINITY - NOT the exact number of operations for
one specific input size, and NOT wall-clock time (which varies by
hardware, language, and implementation details).
```

This distinction matters genuinely — Big-O is about the *shape* of how performance degrades as `n`
grows, deliberately abstracting away hardware-specific, implementation-specific detail so
algorithms can be compared on genuinely equal terms.

## The Common Complexity Classes, From Best to Worst

```
O(1)        constant     → same performance REGARDLESS of input size
O(log n)    logarithmic  → performance grows SLOWLY as input grows
O(n)        linear       → performance grows PROPORTIONALLY to input
O(n log n)  linearithmic → common for GOOD sorting algorithms
O(n²)       quadratic    → performance grows with the SQUARE of input
O(2ⁿ)       exponential  → performance DOUBLES with each additional
                            input element - GENUINELY impractical
                            beyond small inputs
```

## Concrete Examples of Each, Grounded in Already-Covered Code

```python
def get_first(items):              # O(1) - ALWAYS one operation,
    return items[0]                  # regardless of list size

def binary_search(sorted_items, target):   # O(log n) - per
    ...                                      # what-are-algorithms.md

def linear_search(items, target):   # O(n) - per what-are-
    ...                               # algorithms.md, earlier

def has_duplicate(items):           # O(n²) - a NESTED loop,
    for i in range(len(items)):       # comparing every pair
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                return True
    return False
```

`has_duplicate` genuinely illustrates why nested loops over the same input commonly produce O(n²)
behavior — for every one of `n` outer iterations, there's another full pass of up to `n` inner
iterations, multiplying to roughly `n * n` total operations.

## Why Constants and Lower-Order Terms Are Dropped

```
An algorithm doing EXACTLY "2n + 10" operations is still O(n),
NOT O(2n) or O(2n + 10) - Big-O deliberately describes the
DOMINANT growth term, since AS n GROWS LARGE, the constant "10"
and the multiplier "2" become GENUINELY insignificant compared to
n's own growth.
```

This is a genuinely important, often-confusing rule worth understanding precisely — Big-O isn't
concerned with a small, fixed constant-factor difference; it's concerned with how an algorithm's
performance *scales* as input grows toward genuinely large values.

## Visualizing the Growth Rates

```
For n = 1,000:
  O(1)         → 1 operation
  O(log n)     → ~10 operations
  O(n)         → 1,000 operations
  O(n log n)   → ~10,000 operations
  O(n²)        → 1,000,000 operations
  O(2ⁿ)        → a number so large it's genuinely impractical to
                  even compute
```

This concrete comparison is worth internalizing — the *gap* between these complexity classes grows
dramatically as `n` increases, which is exactly why choosing an algorithm with a better complexity
class matters far more, at real scale, than any small, constant-factor optimization.

## Common Mistakes

- Confusing Big-O with exact operation counts or wall-clock time, rather than the abstracted growth
  rate it's actually designed to describe.
- Assuming a small, constant multiplier meaningfully changes an algorithm's Big-O classification,
  when Big-O deliberately drops constants to focus on dominant growth behavior.
- Writing nested loops over the same input without recognizing the resulting O(n²) (or worse)
  behavior, and its genuine impact at real scale.

## ➡️ Next

Continue to [analyzing-algorithms.md](analyzing-algorithms.md) to see how to actually determine an
algorithm's Big-O complexity by reading its code.
