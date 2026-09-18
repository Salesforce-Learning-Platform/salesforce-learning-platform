# ⚙️ What Are Algorithms?

## The Procedures That Operate on Data Structures

[what-are-data-structures.md](what-are-data-structures.md) covered *how data is organized*. An
**algorithm** is the other, equally essential half: a genuine, step-by-step procedure for
*accomplishing a specific task* — searching, sorting, transforming — using that data.

## The Core Definition

```
An ALGORITHM is a FINITE, well-defined sequence of steps that
takes an INPUT and produces a CORRECT OUTPUT, for every possible
valid input.
```

The phrase "for every possible valid input" matters genuinely — a procedure that happens to work
for a few test cases but fails on some genuinely valid input isn't a correct algorithm at all,
merely a coincidence.

## A Concrete Illustration: Searching for a Value

```python
def linear_search(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1
```

```python
def binary_search(sorted_items, target):
    low, high = 0, len(sorted_items) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_items[mid] == target:
            return mid
        elif sorted_items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

Both algorithms genuinely solve the same problem — "find this value's position" — but with
dramatically different real performance: `linear_search` checks elements one by one; `binary_search`
(which requires *sorted* input) eliminates half the remaining possibilities with every single step.
This exact performance difference is precisely what
[Big-O notation](../time-and-space-complexity/big-o-notation.md), the next module, gives a formal
way to describe and compare.

## Algorithms Already Used Throughout This Repository

```
SORTING     → every "ORDER BY" clause in the SQL queries already
             covered in this repository's Backend domain runs a
             genuine sorting algorithm underneath

SEARCHING    → a database INDEX lookup (per Database Design and
             Modeling, earlier in this repository) is, at its
             core, an efficient searching algorithm

TRAVERSAL    → recursively rendering NESTED React components (per
             this repository's Frontend domain) is a genuine tree-
             traversal algorithm, applied to the component tree
```

This is exactly the same realization already established for data structures — algorithms have
been running constantly, underneath code already written throughout this repository, simply without
being examined by name.

## Correctness Before Efficiency

```
The FIRST question for any algorithm: does it produce the
CORRECT result, for EVERY valid input, including genuine edge
cases (an EMPTY list, a list with ONE element, DUPLICATE values)?

ONLY after correctness is established does efficiency (per Time
and Space Complexity, next in this domain) become the genuinely
relevant next question.
```

This directly echoes [testing-your-design.md](../../system-design/low-level-design/lld-problem-solving-and-machine-coding/testing-your-design.md)'s
own discipline from the System Design domain, earlier in this repository — an elegant, efficient
algorithm that produces the *wrong* answer on some genuine edge case is worse than a slower one that
is always genuinely correct.

## Common Mistakes

- Optimizing an algorithm's speed before genuinely verifying it produces correct results across
  realistic edge cases (empty input, a single element, duplicates).
- Assuming a faster-sounding algorithm is always the right choice, without considering its actual
  preconditions (like `binary_search`'s genuine requirement for already-sorted input).
- Treating "it works on my test cases" as equivalent to "it's correct," rather than deliberately
  reasoning through the full range of valid inputs an algorithm might actually receive.

## ➡️ Next

Continue to
[choosing-the-right-data-structure.md](choosing-the-right-data-structure.md) to see how these two
concepts — structure and algorithm — come together in an actual, practical decision.
