# 🛑 Base Cases

## The Part That Decides Whether a Recursion Ever Stops

A recursive function is only correct if two things are true for **every** valid input:

1. **Some call stops.** There is at least one *base case* that returns an answer without recursing.
2. **Every call gets closer to stopping.** Each recursive call works on a problem that is strictly "smaller" in a
   way that eventually reaches a base case.

Almost every recursion bug is a violation of one of these. This file shows the typical failures, how to choose base
cases, and how to argue that a recursion terminates. Every function below was run, and the numeric ones were checked
against Python's built-ins on thousands of random inputs.

## 💥 What Happens Without a Base Case

Forget the base case and the function calls itself until Python's stack limit (see
[recursion-fundamentals.md](recursion-fundamentals.md)) stops it:

```python
def broken_sum(n):
    return n + broken_sum(n - 1)      # no base case: n goes 3, 2, 1, 0, -1, -2, ... forever

try:
    broken_sum(3)
except RecursionError:
    print("no base case -> RecursionError")
```

```text
no base case -> RecursionError
```

In a language or situation without a depth limit, the same bug would exhaust memory or crash the program. The error
is easy to spot because it happens immediately — the subtler bugs are base cases that *exist* but are never reached.

## 🚧 A Base Case That Is Never Reached

The base case must be reachable from every valid input, in the direction the recursion actually moves:

```python
def count_down_by_two(n):
    if n == 0:                         # base case: only reachable if n is even and non-negative
        return "done"
    return count_down_by_two(n - 2)

print(count_down_by_two(4))            # done
try:
    count_down_by_two(5)               # 5, 3, 1, -1, -3 ... steps over 0
except RecursionError:
    print("stepped over the base case")
```

```text
done
stepped over the base case
```

Two ways to fix it: make the base case a *range* (`if n <= 0`) so stepping over zero still stops, or validate the
input. The same hazard applies whenever the step size is greater than one, or the problem can shrink in two different
ways. Using `<=` (or `>=`) for a boundary is the safer habit; `==` is correct only when you can prove the value
is hit exactly.

Another variation moves the wrong way:

```python
def count_down_wrong(n):
    if n == 0:
        return "done"
    return count_down_wrong(n + 1)     # grows away from 0 instead of toward it

try:
    count_down_wrong(3)
except RecursionError:
    print("moved away from the base case")
```

```text
moved away from the base case
```

## 🔢 Functions That Need More Than One Base Case

The Fibonacci numbers are defined by `F(n) = F(n−1) + F(n−2)`, with `F(0) = 0` and `F(1) = 1`. The recursive case calls
**two** smaller problems, `n−1` and `n−2`, so there must be two base cases — otherwise `n−2` can jump past the only
base case:

```python
def fib(n):
    if n == 0:                         # base case 1
        return 0
    if n == 1:                         # base case 2
        return 1
    return fib(n - 1) + fib(n - 2)

print([fib(n) for n in range(10)])     # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def fib_one_base(n):
    if n == 0:
        return 0
    return fib_one_base(n - 1) + fib_one_base(n - 2)    # fib_one_base(1) calls fib_one_base(-1)

try:
    fib_one_base(1)
except RecursionError:
    print("one base case is not enough")
```

```text
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
one base case is not enough
```

**Rule of thumb:** if the recursive case reaches back by `k` steps, expect to need about `k` base cases — enough that
every call lands on one of them.

## 🎯 Choosing the Right Base Value

A base case is more than "stop"; it must return the **correct answer for the smallest input**, because every larger
answer is built on top of it. The usual way to find the value is to ask what the answer is for the *empty* or
*smallest* case, so that the combining step still works:

| Function | Base case | Why that value |
|----------|-----------|----------------|
| `factorial(n)` | `factorial(0) = 1` | An empty product is 1 — anything multiplied by 1 is unchanged |
| Sum of a list | `sum([]) = 0` | Adding 0 changes nothing |
| `power(x, n)` | `power(x, 0) = 1` | The multiplicative identity |
| Length of a list | `length([]) = 0` | Nothing to count |
| Concatenating strings | `""` | The empty string is the identity for `+` |

Get this wrong and every answer is wrong. For example, a factorial that returns `0` for `n == 0` returns `0` for
**every** `n`, because every result is that value multiplied by something.

Some problems have no sensible answer for the empty input. The maximum of an empty list is undefined, so the smallest
legitimate input is *one* element — and the empty case must be rejected before recursing:

```python
def max_of(numbers):
    if not numbers:
        raise ValueError("max_of() needs at least one number")

    def helper(index):
        if index == len(numbers) - 1:              # base case: the last element is the max of itself
            return numbers[index]
        return max(numbers[index], helper(index + 1))

    return helper(0)

print(max_of([3, 9, 4]))        # 9
print(max_of([7]))              # 7
try:
    max_of([])
except ValueError as error:
    print(error)                # max_of() needs at least one number
```

The wrapper checks the input once; the inner helper does the recursion and has a base case that is always reachable.
This **wrapper + helper** shape is common: validate at the door, recurse inside.

## 🧪 Guarding Against Invalid Input

Some inputs make a correct-looking recursion run forever. `factorial(-1)` calls `factorial(-2)`, then
`factorial(-3)`, never reaching 0. Decide what should happen and handle it before recursing:

```python
def factorial(n):
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(6))     # 720
try:
    factorial(-1)
except ValueError as error:
    print(error)        # factorial is not defined for negative numbers
```

Raising a clear error is much better than letting the program wander off until the stack overflows. (This is
different from `n <= 0` as a base case: here a negative input is a *mistake*, not a valid input with answer 1.)

## 📐 Proving That a Recursion Terminates

To convince yourself (or an interviewer) that a recursion stops, name a **measure** — a whole number that gets
strictly smaller on every call and cannot go below a fixed lower bound — and show that the base case is reached when the
measure hits that bound.

| Function | Measure | Why it shrinks | Base case |
|----------|---------|----------------|-----------|
| `factorial(n)` | `n` | Each call uses `n − 1` | `n == 0` |
| `total(numbers, index)` | `len(numbers) − index` | `index` grows by 1 | `index == len(numbers)` |
| `is_palindrome_recursive(text, left, right)` | `right − left` | Each call moves both ends inward by 1 | `left >= right` |
| `gcd(a, b)` | `b` | `a % b` is always smaller than `b` | `b == 0` |
| Binary search on `[low, high]` | `high − low + 1` (size of the range) | The range halves | An empty range |

If you cannot name such a measure for a recursion, that is a warning sign.

### Example: Euclid's Algorithm

The greatest common divisor can be computed with `gcd(a, b) = gcd(b, a mod b)`, stopping when `b` is `0`:

```python
def gcd(a, b):
    if b == 0:                          # base case
        return a
    return gcd(b, a % b)                # b is replaced by a smaller value: a % b < b

print(gcd(48, 18))                      # 6
print(gcd(7, 5))                        # 1
print(gcd(9, 0))                        # 9
```

Tracing `gcd(48, 18)`:

```
gcd(48, 18)  ->  gcd(18, 12)  ->  gcd(12, 6)  ->  gcd(6, 0)  ->  6
```

The measure is the second argument: `18 → 12 → 6 → 0`. Because `a % b` is always in `0 … b−1`, it strictly decreases,
so it must reach `0` — and it does so quickly, in a number of steps proportional to the number of digits.

### Example: Binary Search on a Range

Searching a sorted list by repeatedly halving the range has an unusual base case: the range can become **empty**.

```python
def binary_search(sorted_numbers, target, low=0, high=None):
    if high is None:
        high = len(sorted_numbers) - 1
    if low > high:                                   # base case 1: the range is empty -> not found
        return -1
    mid = (low + high) // 2
    if sorted_numbers[mid] == target:                # base case 2: found it
        return mid
    if sorted_numbers[mid] < target:
        return binary_search(sorted_numbers, target, mid + 1, high)   # discard the left half, including mid
    return binary_search(sorted_numbers, target, low, mid - 1)        # discard the right half, including mid

data = [2, 5, 8, 12, 16, 23, 38]
print(binary_search(data, 23))      # 5
print(binary_search(data, 7))       # -1
print(binary_search([], 1))         # -1
```

Notice `mid + 1` and `mid − 1`: excluding `mid` is what guarantees the range strictly shrinks. Using `mid` instead would
let a one-element range call itself with the same range forever — a base case that is never reached. The measure is the range
size, which at least halves and eventually reaches `0` (the empty-range base case). The recursion is `O(log n)` deep.

## 🧭 Negative and Zero Cases in Practice

One more illustration of "make the input smaller" interacting with edge cases — raising a number to an integer power:

```python
def power(x, n):
    if n == 0:                          # base case
        return 1
    if n < 0:
        return 1 / power(x, -n)         # reduce to the positive case: -n is a positive number
    return x * power(x, n - 1)

print(power(2, 10))        # 1024
print(power(2, 0))         # 1
print(power(2, -3))        # 0.125
```

The negative branch does not recurse toward a base case directly — it flips the sign once, producing a problem the
positive branch handles. That is fine, as long as the flip happens **once** and then the measure (`n`) starts
decreasing.

## ✅ A Base-Case Checklist

1. **List the smallest valid inputs** (zero, empty, one element, an empty range) and decide the correct answer for each.
2. **Write the base cases before the recursive case**, and test them first.
3. **Prefer `<=`/`>=` for boundaries** unless the value is certain to be hit exactly.
4. **Name the measure** that strictly decreases, and check that every recursive call decreases it.
5. **Reject invalid inputs up front** — often with a wrapper function.
6. **Count the base cases** against how far back the recursive case reaches.

## Common Mistakes

- **Omitting the base case**, or putting it after the recursive call so it is never evaluated.
- **Testing `n == 0` when the value can skip over 0** (steps of 2, negative inputs).
- **Wrong base value** (`factorial(0)` returning 0, or a sum of nothing returning 1).
- **Too few base cases** for a recursion that looks back several steps, as in Fibonacci.
- **Not shrinking the problem** — passing `n` instead of `n − 1`, or including `mid` in a binary-search half.
- **Letting invalid input recurse** instead of raising an error.
- **Putting validation inside the recursion**, repeating the same check at every level, when a wrapper would do.

## ➡️ Next

Continue to [recursion-tree.md](recursion-tree.md) to picture a recursion as a tree of calls and use that picture to
count calls, find the stack depth, and see why some recursions explode.
