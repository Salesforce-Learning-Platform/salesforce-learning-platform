# 🧠 Recursive Problem Solving

## A Method, Then Eight Problems

Knowing what recursion *is* does not yet make it easy to *write*. The skill is in a small habit of thought: describe the
answer to a problem **in terms of the answer to a smaller version of the same problem**, then check the edges. This
file gives that habit a method and practises it on classic problems of increasing difficulty — from summing digits to
generating all subsets, permutations, and balanced parentheses.

Every function was run, and each was checked against a built-in or brute-force version on thousands of random
inputs or every possible input in a range.

## 🧭 The Method

1. **Define the function precisely.** Write one sentence: "`f(x)` returns ___." Everything else depends on this
   meaning staying fixed.
2. **Identify the smallest inputs** and answer them directly — the base cases ([base-cases.md](base-cases.md)).
3. **Make the leap of faith.** Assume `f` already works correctly for every *smaller* input. Do not trace the inner
   calls in your head.
4. **Express the answer for the current input** using the answers to the smaller inputs — and a little extra work.
5. **Check progress.** Each recursive call must move strictly toward a base case.
6. **Estimate the cost** by drawing the tree ([recursion-tree.md](recursion-tree.md)).

The "leap of faith" in step 3 is the same reasoning as mathematical induction: if the base case is right, and the
step from `n−1` to `n` is right, then every `n` is right.

## 1️⃣ Summing the Digits of a Number

*Define it:* `sum_of_digits(n)` returns the sum of the decimal digits of a non-negative integer `n`.

*Smallest input:* a single digit is its own sum. *The leap of faith:* assume we can already sum the digits of `n // 10`
(all digits but the last). *Combine:* add the last digit, `n % 10`.

```python
def sum_of_digits(n):
    if n < 10:                               # base case: one digit
        return n
    return n % 10 + sum_of_digits(n // 10)   # last digit + the digits of the rest

print(sum_of_digits(4))        # 4
print(sum_of_digits(1729))     # 19   — 1 + 7 + 2 + 9
print(sum_of_digits(0))        # 0
```

The input loses one digit per call, so the depth equals the number of digits: O(log₁₀ n) time and stack space.

## 2️⃣ Reversing a String

*Define it:* `reverse_text(text)` returns `text` backwards. *Base case:* a string of length 0 or 1 is its own reverse.
*Leap of faith:* assume we can reverse everything except the first character. *Combine:* put that first character at the
end.

```python
def reverse_text(text):
    if len(text) <= 1:                       # base case
        return text
    return reverse_text(text[1:]) + text[0]  # reverse the rest, then append the first character

print(reverse_text("recursion"))   # noisrucer
print(reverse_text(""))            # (empty line)
print(reverse_text("a"))           # a
```

This is correct, and a clear illustration of the method — but it is a poor way to reverse a string in practice. Each call
copies the rest of the string (`text[1:]`) and builds a new string with `+`, so the total cost is **O(n²)**, and the
depth is `n`, which hits Python's recursion limit near 1000 characters. Use `text[::-1]`, or the two-pointer approach in
[string-manipulation.md](../strings/string-manipulation.md), for real work.

## 3️⃣ Fast Exponentiation

*Define it:* `fast_power(base, exponent)` returns `base ** exponent` for an integer `exponent >= 0`. The obvious
approach multiplies `base` by itself `exponent` times — `exponent` multiplications. But `base¹⁰ = (base⁵)²`:
**halving the exponent** and squaring needs far fewer multiplications.

```python
def fast_power(base, exponent):
    if exponent == 0:                              # base case
        return 1
    half = fast_power(base, exponent // 2)         # ONE recursive call, stored in a variable
    if exponent % 2 == 0:
        return half * half                          # base^(2k) = (base^k)^2
    return half * half * base                       # base^(2k+1) = (base^k)^2 * base

print(fast_power(2, 10))      # 1024
print(fast_power(3, 0))       # 1
print(fast_power(7, 13))      # 96889010407
```

The exponent halves on each call, so the recursion is only about log₂(exponent) deep: **O(log n) multiplications**
instead of O(n). The detail that matters most is storing the result in `half`. Writing the call twice, as in
`fast_power(base, e // 2) * fast_power(base, e // 2)`, makes two calls per level and turns the chain into a complete binary tree
whose size is proportional to the exponent itself — all the savings vanish. Counting the calls proves it:

```python
def calls_single(exponent):               # fast_power's shape: one recursive call per level
    return 1 if exponent == 0 else 1 + calls_single(exponent // 2)

def calls_double(exponent):               # the "call it twice" mistake
    return 1 if exponent == 0 else 1 + 2 * calls_double(exponent // 2)

print(f"{'exponent':>9} | {'one call per level':>18} | {'two calls per level':>19}")
for exponent in (16, 256, 1024, 65536):
    print(f"{exponent:>9,} | {calls_single(exponent):>18,} | {calls_double(exponent):>19,}")
```

```text
 exponent | one call per level | two calls per level
       16 |                  6 |                  63
      256 |                 10 |               1,023
    1,024 |                 12 |               4,095
   65,536 |                 18 |             262,143
```

## 4️⃣ The Tower of Hanoi

Three pegs; `n` disks of different sizes start stacked on the source peg, smallest on top. Move them all to the target
peg, one disk at a time, never placing a larger disk on a smaller one. This looks hard until you trust recursion:

- To move `n` disks from source to target: first move the top `n−1` disks out of the way onto the spare peg
  (the leap of faith), then move the biggest disk, then move the `n−1` disks from the spare onto the target.
- *Base case:* moving zero disks takes no moves.

```python
def hanoi(n, source, target, spare, moves):
    if n == 0:                                     # base case: nothing to move
        return
    hanoi(n - 1, source, spare, target, moves)     # clear the top n-1 disks onto the spare peg
    moves.append((source, target))                 # move the largest disk
    hanoi(n - 1, spare, target, source, moves)     # bring the n-1 disks back on top of it

moves = []
hanoi(3, "A", "C", "B", moves)
print(moves)
print(len(moves))        # 7
```

```text
[('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]
7
```

Each call makes two calls on `n−1`, so the tree is a complete binary tree and the number of moves satisfies
`T(n) = 2·T(n−1) + 1`, which solves to **2ⁿ − 1**. This is not a weakness of the algorithm: the smallest possible
number of moves really is 2ⁿ − 1 ([Tower of Hanoi](https://en.wikipedia.org/wiki/Tower_of_Hanoi)), so no cleverer
algorithm exists. The solution is simple to write and exponentially long to execute — 20 disks already need over a
million moves.

## 5️⃣ All Subsets (Include or Skip)

*Define it:* `subsets(items)` returns every subset of a list. For each item there are exactly two choices —
**include it or skip it** — and the choices for the remaining items are the same problem again.

```python
def subsets(items):
    result = []

    def choose(index, current):
        if index == len(items):                   # base case: every item has been decided
            result.append(current[:])             # store a COPY of the current choice
            return
        choose(index + 1, current)                # choice 1: skip items[index]
        current.append(items[index])              # choice 2: include it...
        choose(index + 1, current)
        current.pop()                             # ...then undo, so the caller sees current unchanged

    choose(0, [])
    return result

print(subsets([1, 2, 3]))
print(len(subsets(list(range(10)))))     # 1024
```

```text
[[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]
1024
```

The decision tree has depth `n` and `2ⁿ` leaves (one per subset), so the function takes O(2ⁿ · n) time
(copying each result) and, besides the output, O(n) stack space.

Two details deserve attention. The `current.pop()` after the second call is **backtracking**: it undoes the choice so that
the same list can be reused when the recursion returns to the caller — a technique used heavily in the later modules.
And `current[:]` copies the list. Without the copy, every entry of `result` would point at the same list, which ends up
empty:

```python
def subsets_without_copy(items):
    result = []

    def choose(index, current):
        if index == len(items):
            result.append(current)               # BUG: stores the working list itself
            return
        choose(index + 1, current)
        current.append(items[index])
        choose(index + 1, current)
        current.pop()

    choose(0, [])
    return result

print(subsets_without_copy([1, 2]))     # [[], [], [], []]
```

## 6️⃣ All Permutations

*Define it:* `permutations(items)` returns every ordering of the items. Choose which item goes first (any of the
remaining ones), then permute what is left — the same problem, smaller.

```python
def permutations(items):
    result = []

    def build(current, remaining):
        if not remaining:                          # base case: nothing left to place
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])           # place remaining[i] next
            build(current, remaining[:i] + remaining[i + 1:])    # permute everything else
            current.pop()                          # backtrack

    build([], list(items))
    return result

print(permutations([1, 2, 3]))
print(len(permutations(range(5))))    # 120
```

```text
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
120
```

There are `n!` permutations, so the tree has `n!` leaves and the function is **O(n · n!)**. That growth is fast: 10
items already give 3,628,800 permutations. Problems that ask for *all* arrangements are inherently expensive — the cost is
the size of the answer.

## 7️⃣ Balanced Parentheses (Backtracking With Rules)

*Define it:* `generate_parentheses(n)` returns every string of `n` pairs of parentheses that is correctly balanced. Rather
than generate all `2²ⁿ` strings and filter, **prune as you build**: add `(` while fewer than `n` have been used, and add
`)` only while it would not close more than has been opened.

```python
def generate_parentheses(n):
    result = []

    def build(current, opened, closed):
        if len(current) == 2 * n:                  # base case: a complete string
            result.append("".join(current))
            return
        if opened < n:                             # we may still open one
            current.append("(")
            build(current, opened + 1, closed)
            current.pop()
        if closed < opened:                        # we may close only what is open
            current.append(")")
            build(current, opened, closed + 1)
            current.pop()

    build([], 0, 0)
    return result

print(generate_parentheses(3))
print([len(generate_parentheses(n)) for n in range(1, 8)])
```

```text
['((()))', '(()())', '(())()', '()(())', '()()()']
[1, 2, 5, 14, 42, 132, 429]
```

The counts `1, 2, 5, 14, 42, 132, 429` are the **Catalan numbers**
([OEIS A000108](https://oeis.org/A000108)). The two `if` conditions are what make this efficient: invalid strings are
never started, so no work is wasted on dead ends. This "choose, explore, undo — and skip choices that break the rules" is
the pattern of **backtracking**.

## 8️⃣ Flattening Nested Lists (Structure Is Recursive)

When the *data* is nested to an unknown depth, recursion is the natural fit. *Define it:* `flatten(nested)` returns all
the non-list values in order. A list is processed item by item; an item that is itself a list is flattened by the same
function.

```python
def flatten(nested):
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten(item))             # a nested list is the same problem, smaller
        else:
            flat.append(item)                      # a plain value
    return flat

print(flatten([1, [2, [3, [4]], 5], [], [[6]]]))   # [1, 2, 3, 4, 5, 6]
print(flatten([]))                                  # []
```

This works until the nesting is deeper than Python's recursion limit. For deep or untrusted input, replace the call
stack with an **explicit stack** — a list you manage yourself — which has no depth limit:

```python
def flatten_iterative(nested):
    flat = []
    stack = list(reversed(nested))                 # the top of the stack is the next item to process
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))           # unpack: its first element ends up on top
        else:
            flat.append(item)
    return flat

print(flatten_iterative([1, [2, [3, [4]], 5], [], [[6]]]))   # [1, 2, 3, 4, 5, 6]

deep = 1
for _ in range(5000):                              # nest the value 5000 levels deep
    deep = [deep]

print(flatten_iterative(deep))                      # [1]
try:
    flatten(deep)
except RecursionError:
    print("the recursive version overflowed")       # the recursive version overflowed
```

Converting a recursion to an explicit stack is always possible: the call stack *is* a stack of "what to do next". It trades
elegance for safety, and it is the standard remedy when recursion depth is a concern.

## ⚖️ Recursion or Iteration?

| Situation | Prefer |
|-----------|--------|
| The data or the problem is naturally nested or self-similar (trees, nested lists, directories) | Recursion |
| You must explore choices and undo them (subsets, permutations, puzzles) | Recursion with backtracking |
| The problem splits into independent halves (merge sort, binary search) | Recursion |
| A simple counted repetition or running total | A loop |
| The depth could be in the thousands | A loop, or an explicit stack |
| The same subproblem recurs many times | Recursion **plus** caching — see [recursion-tree.md](recursion-tree.md) |

## Common Mistakes

- **Starting to code before stating what the function returns.**
- **Tracing the inner calls by hand** instead of trusting the function on smaller input.
- **Calling the recursive function twice** where once (stored in a variable) would do, as in fast exponentiation.
- **Forgetting to copy the working list** when saving a result in a backtracking function.
- **Forgetting to undo a choice** (`pop`), so state leaks between branches.
- **Generating everything and filtering** when the rules allow pruning early.
- **Using recursion on data that can be very deep** without an iterative fallback.
- **Mutating an argument that the caller still needs.**

## Module Summary

[Recursion Fundamentals](recursion-fundamentals.md) introduced the base case and recursive case, showed the call stack
winding down and unwinding, and measured Python's recursion limit and its lack of tail-call optimization.
[Base Cases](base-cases.md) showed how recursions fail — missing, unreachable, or wrong base cases — and how to prove
termination by naming a measure that shrinks. [The Recursion Tree](recursion-tree.md) turned recursion into a picture, read
time off the number of calls and stack space off the height, and showed how memoization prunes repeated work. This file
supplied a method and eight worked problems.

Carry these ideas forward:

- Define the function, write the base cases, trust the smaller calls, combine, and check progress.
- Time is the number of calls; stack space is the depth.
- Python's recursion limit is about 1000 — use loops or an explicit stack for deep inputs.
- Repeated subproblems call for caching; "choose, explore, undo" is backtracking.
- Recursion is the engine of the trees, graphs, sorting, and dynamic-programming modules to come.

## ➡️ Next

Continue to the [Hashing](../hashing/README.md) module, the next module in this domain, where a different idea — using
a key to compute where data lives — turns many O(n) searches into O(1) lookups.
