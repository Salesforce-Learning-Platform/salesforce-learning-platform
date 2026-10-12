# 🪆 Recursion Fundamentals

## Solving a Problem by Solving a Smaller Copy of It

A function is **recursive** when it calls itself. That sounds circular, and it would be — an endless loop —
except for one rule that every working recursive function follows:

> Each call must either **stop** (answer directly) or **hand a strictly smaller version of the problem to
> another call**, and eventually the smaller versions must reach one that stops.

Think of a set of nesting dolls. To count the dolls, open the largest one: if it is empty (the solid smallest
doll), the answer is 1; otherwise the answer is 1 plus the count of the dolls inside. You never count the whole
stack at once; you trust the inside count and add one.

Recursion is the natural way to describe anything that contains smaller copies of itself — folders inside
folders, a tree whose branches are smaller trees, a problem that splits into two half-size problems. It is the
foundation of trees, graphs, backtracking, divide and conquer, and dynamic programming later in this domain.

All code in this file was run on CPython 3.9, and the printed outputs are real.

## 🧱 The Two Parts

Every recursive function has the same skeleton:

```text
def solve(problem):
    if problem is small enough:        # 1. BASE CASE: answer directly, no recursion
        return the_direct_answer
    smaller = make_it_smaller(problem) # 2. RECURSIVE CASE: reduce the problem...
    partial = solve(smaller)           #    ...let a call solve it (trust that it works)...
    return combine(problem, partial)   #    ...and use that answer to build ours
```

- The **base case** is the part that does not recurse. Without it, the calls never stop.
- The **recursive case** must move toward the base case — the input must get strictly "smaller" in some
  sense (a smaller number, a shorter list, a smaller range of indexes).

The classic first example is the factorial: `n! = n × (n−1)!`, with `0! = 1`.

```python
def factorial(n):
    if n == 0:                         # base case
        return 1
    return n * factorial(n - 1)        # recursive case: a smaller problem, n-1

print(factorial(5))     # 120
print(factorial(0))     # 1
```

Two more small examples build the habit of identifying the parts:

```python
def countdown(n):
    if n == 0:                         # base case
        print("liftoff")
        return
    print(n)
    countdown(n - 1)                   # smaller problem: n-1

countdown(3)
```

```text
3
2
1
liftoff
```

```python
def total(numbers, index=0):
    if index == len(numbers):          # base case: nothing left to add
        return 0
    return numbers[index] + total(numbers, index + 1)    # this element + the sum of the rest

print(total([4, 8, 15, 16]))   # 43
print(total([]))               # 0
```

`total` shrinks the problem by moving an **index** forward rather than slicing the list; the reason is explained in
"What Recursion Costs" below.

## 📚 What Really Happens: The Call Stack

Each call gets its own **frame** on the call stack — a private copy of its parameters and local variables. A frame
stays there, waiting, until the call it made returns. The best way to see this is to make the function narrate
itself, indenting by depth:

```python
def factorial_traced(n, depth=0):
    indent = "  " * depth
    print(f"{indent}factorial({n}) called")
    if n == 0:
        print(f"{indent}-> base case, returns 1")
        return 1
    result = n * factorial_traced(n - 1, depth + 1)
    print(f"{indent}factorial({n}) returns {result}")
    return result

factorial_traced(3)
```

```text
factorial(3) called
  factorial(2) called
    factorial(1) called
      factorial(0) called
      -> base case, returns 1
    factorial(1) returns 1
  factorial(2) returns 2
factorial(3) returns 6
```

Read it as two phases:

1. **Winding down.** `factorial(3)` calls `factorial(2)`, which calls `factorial(1)`, which calls `factorial(0)`.
   Nothing is multiplied yet: each frame is paused, waiting for the answer to its smaller problem. At the deepest
   point there are **four frames on the stack**.
2. **Unwinding.** `factorial(0)` returns 1, so `factorial(1)` can finish its multiplication (`1 × 1`), which lets
   `factorial(2)` finish (`2 × 1`), and so on back to the top. Frames are removed in last-in, first-out order.

The work of combining answers happens on the way **back up**. That is why a recursive function needs memory
proportional to its depth — every waiting frame holds its local variables.

## 🧱 Recursion Is Not Free: Time and Space

Count two things: how many calls are made (time), and how deep the stack gets (space).

| Function | Calls made | Maximum depth | Time | Extra space (stack) |
|----------|-----------|---------------|------|---------------------|
| `factorial(n)` | n + 1 | n + 1 | O(n) | O(n) |
| `total(numbers)` | n + 1 | n + 1 | O(n) | O(n) |
| `countdown(n)` | n + 1 | n + 1 | O(n) | O(n) |

A loop doing the same job needs O(1) extra space. That is the first trade-off of recursion: **clarity for
problems that are naturally recursive, paid for with stack space.**

The way the problem is made smaller matters, too. Compare two versions of the same sum:

```python
copied = 0

def total_by_slicing(numbers):
    global copied
    if not numbers:
        return 0
    rest = numbers[1:]                  # builds a NEW list of n-1 elements
    copied += len(rest)
    return numbers[0] + total_by_slicing(rest)

print(total_by_slicing(list(range(100))))   # 4950
print(copied)                                # 4950   — 99 + 98 + ... + 1 + 0 elements copied
```

Slicing a list copies it (see [array traversal](../arrays/traversal.md) and
[string-fundamentals.md](../strings/string-fundamentals.md) for the same point about strings). Over `n` levels that
adds up to `n(n−1)/2` copied elements — **O(n²) time** for what should be an O(n) task. The index-based `total`
above copies nothing. Whenever a recursive function passes a slice, ask whether passing `start`/`end` indexes would
be cheaper.

## 🛑 Python's Recursion Limit

Because the stack uses memory, Python caps its depth to protect the interpreter. The default limit is 1000 frames:

```python
import sys

print(sys.getrecursionlimit())

def dive():
    dive()

try:
    dive()
except RecursionError as error:
    print(type(error).__name__)
    print(str(error).startswith("maximum recursion depth exceeded"))
```

```text
1000
RecursionError
True
```

In practice a call chain gets slightly under 1000 deep (on CPython 3.9, a trivial function managed 998 frames from
inside another function; the exact number depends on the version and on what is already on the stack). This limit
is a real constraint for recursive solutions on large inputs:

```python
try:
    factorial(2000)
except RecursionError:
    print("factorial(2000) overflowed the stack")   # factorial(2000) overflowed the stack
```

`sys.setrecursionlimit()` can raise the limit, but the Python documentation warns that the highest possible value is
platform-dependent and that "a too-high limit can lead to a crash", because deep recursion can exhaust the real C
stack. For depth in the thousands or more, rewrite the function as a loop — or with an explicit stack, as shown in
[recursive-problem-solving.md](recursive-problem-solving.md).

### Tail Recursion Does Not Help in Python

A function is **tail recursive** when the recursive call is the very last thing it does, so nothing is left to do after
it returns. Some languages (Scheme, and optimizing compilers for several others) reuse the current frame for such
calls, so the stack never grows. **Python does not do this.** A tail-recursive sum still fails:

```python
def sum_to(n, accumulator=0):
    if n == 0:
        return accumulator
    return sum_to(n - 1, accumulator + n)     # the last action: a tail call

print(sum_to(100))        # 5050
try:
    sum_to(5000)
except RecursionError:
    print("tail recursion still overflows")   # tail recursion still overflows
```

This is a deliberate decision. Guido van Rossum explained that eliminating tail calls would remove stack frames
that tracebacks rely on, making bugs harder to debug
([Tail Recursion Elimination](http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html)). The practical
rule in Python: write a loop when the depth could be large.

## 🔁 Recursion vs. Iteration

Anything recursive can be written as a loop, and vice versa. The factorial, as a loop:

```python
def factorial_loop(n):
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result

print(factorial_loop(5))                    # 120
print(factorial_loop(5) == factorial(5))    # True
```

| | Recursion | Iteration |
|---|-----------|-----------|
| Natural for | Trees, nested data, divide and conquer, backtracking | Counting, scanning, accumulating |
| Extra space | One stack frame per level (O(depth)) | Usually O(1) |
| Depth limit in Python | About 1000 | None |
| Readability | Excellent when the problem is self-similar | Excellent when the problem is a simple sequence |

A good rule: use recursion when the **problem's structure** is recursive; use a loop when you are merely repeating.

## ✅ A Checklist for Writing a Recursive Function

1. **State in one sentence what the function returns** for any valid input (for example, "returns `n!`").
2. **Write the base case(s) first.** Which inputs can be answered with no recursion?
3. **Trust the function on smaller inputs**, and express the answer for the current input using it.
4. **Check that every recursive call moves strictly toward a base case.**
5. **Count the calls and the depth** to know the time and the stack space.

[base-cases.md](base-cases.md) examines step 2 and step 4 in detail, and
[recursive-problem-solving.md](recursive-problem-solving.md) applies the whole checklist to larger problems.

## Common Mistakes

- **No base case, or a base case the calls never reach** — the result is a `RecursionError`.
- **Not making the problem smaller** (`countdown(n)` calling `countdown(n)`), or making it larger by mistake.
- **Forgetting to `return` the recursive result** — the function silently returns `None`.
- **Passing slices of lists or strings** and unknowingly making the algorithm O(n²).
- **Assuming tail recursion is optimized in Python.**
- **Using recursion for plain loops** where a `for` loop is clearer and has no depth limit.
- **Raising `sys.setrecursionlimit` to hide a deep recursion** instead of restructuring the solution.

## ➡️ Next

Continue to [base-cases.md](base-cases.md) to look closely at the part of a recursive function that decides whether it
ever stops: choosing, testing, and reasoning about base cases.
