# 💾 Space Complexity

## The Other Half of the Trade-Off

[time-complexity.md](time-complexity.md) closed by trading memory for speed in
`contains_duplicate_fast`. **Space complexity** is the formal measurement of exactly that memory
cost — using the identical Big-O notation already covered, now applied to memory instead of
operation count.

## The Core Definition

```
SPACE COMPLEXITY measures how much ADDITIONAL memory an algorithm
requires, as a function of input size n - NOT counting the input
itself, only the EXTRA memory the algorithm allocates while
running.
```

The phrase "not counting the input itself" matters — space complexity is about an algorithm's own
*additional* memory footprint, not the size of the data it was already given to work with.

## Concrete Examples, Grounded in Already-Covered Code

```python
def sum_all(items):            # O(1) space - only ONE extra
    total = 0                    # variable ("total"), REGARDLESS
    for item in items:           # of how large "items" is
        total += item
    return total

def contains_duplicate_fast(items):   # O(n) space - the "seen"
    seen = set()                        # set can grow to hold UP
    for item in items:                  # TO n elements
        if item in seen:
            return True
        seen.add(item)
    return False

def get_first_n(items, n):     # O(n) space - the NEW list
    return items[:n]             # holds up to n elements,
                                   # separate from the original
```

`sum_all` needs exactly one extra variable no matter how large `items` grows — genuinely O(1) space.
`contains_duplicate_fast`, from [time-complexity.md](time-complexity.md), needs a `seen` set that
can grow proportionally with the input — genuinely O(n) space. This is precisely the trade-off
already previewed: `contains_duplicate_fast` spent O(n) space to bring time complexity down from
O(n²) to O(n).

## Recursive Calls Consume Space Too

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

```
Each RECURSIVE call adds a new frame to the CALL STACK, which
consumes real memory until that call RETURNS. factorial(5) has, at
its deepest point, 5 stack frames alive SIMULTANEOUSLY → O(n)
space, even though the function itself allocates NO explicit data
structure.
```

This is a genuinely easy-to-miss source of space complexity, and it directly previews
[Recursion](../recursion/), later in this domain, where call-stack space becomes a central,
recurring concern — including the specific risk of a *stack overflow* when recursive depth grows
too large for the available call stack.

## The Time-Space Trade-Off, Stated Explicitly

```
It is EXTREMELY common for a faster algorithm (better time
complexity) to require MORE memory (worse space complexity), and
vice versa - a SLOWER algorithm can often run in LESS memory.

There is genuinely no universal "right" choice - the correct
trade-off depends on the ACTUAL constraints of the system: is
memory the scarce, limited resource (an embedded device), or is
response time the priority (a user-facing API)?
```

This mirrors, precisely, the reliability-vs-cost and consistency-vs-performance trade-offs already
covered in [consistency-vs-performance-tradeoffs.md](../../system-design/high-level-design/communication-and-data-layer/consistency-vs-performance-tradeoffs.md)
in the System Design domain — there is rarely a single correct answer in isolation; the right choice
depends on the actual, concrete constraints of the system being built.

## Common Mistakes

- Counting the input itself as part of an algorithm's space complexity, rather than only the
  *additional* memory the algorithm allocates.
- Overlooking recursive call-stack space as a genuine space cost, since no explicit data structure
  is visibly allocated in the code.
- Assuming a faster algorithm is unconditionally "better," without weighing its space complexity
  trade-off against the actual constraints of the system it will run in.

## Module Summary

Across this module: **Big-O notation** is the formal language for an algorithm's growth rate as
input size grows toward infinity, deliberately abstracting away constants and hardware-specific
detail (see [big-o-notation.md](big-o-notation.md)); **analyzing algorithms** means applying a
small set of repeatable rules — sequential steps add, nested loops multiply, halving input means
logarithmic growth, and worst case is the conventional default — to classify real code (see
[analyzing-algorithms.md](analyzing-algorithms.md)); **time complexity** is that same analysis
applied specifically to running time, with the concrete reference table of common data structure
operations every later module in this domain builds on (see [time-complexity.md](time-complexity.md));
and **space complexity** is the mirrored analysis applied to memory, revealing a frequent, genuine
trade-off — an algorithm can often trade more memory for less time, or vice versa, with the right
choice depending entirely on a system's actual, concrete constraints.

## ➡️ Next

Continue to [Arrays](../arrays/) to apply this complexity vocabulary to the first concrete data
structure in this domain.
