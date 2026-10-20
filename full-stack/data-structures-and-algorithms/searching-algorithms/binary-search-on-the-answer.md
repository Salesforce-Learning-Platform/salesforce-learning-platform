# 🎚️ Binary Search on the Answer

## Searching a Range of Possible Answers

Some problems ask for a *number* that is not stored anywhere: the slowest speed that still finishes the job in time, the smallest capacity that fits all the packages, the largest minimum distance you can achieve. There is no sorted list to search — but there is a range of possible answers, and often a cheap way to test one guess: *"Would a speed of 5 be fast enough?"*

If that test is **monotone** — once a guess works, every larger guess works too — the guesses split into a block of "no" followed by a block of "yes":

```
 guess:    1    2    3    4    5    6    7    8   ...
 works?   no   no   no  YES  YES  YES  YES  YES  ...
                          ^ the answer is the first YES
```

Finding the boundary of such a block is exactly what [binary search](binary-search.md) does. Instead of trying every guess (R tests for a range of size R), you try about `log₂ R` of them. If a test costs O(n), the whole solution costs O(n log R) rather than O(n·R). The technique is called **binary search on the answer** (or on the *answer space*), and it turns a large family of optimization problems — "minimize the maximum", "maximize the minimum", "smallest value such that…" — into a short loop. All outputs below were produced by running the code on CPython 3.9, and every solver is checked against a brute-force search over all candidate answers.

## 🧱 The Template: `first_true` and `last_true`

Two small functions cover every case. They use the half-open template from [binary-search.md](binary-search.md) (`while low < high`), so the loop invariant is easy to state:

```python
def first_true(low, high, is_good):
    """Smallest x in [low, high] with is_good(x) true.

    Requires is_good to be false...false true...true over the range, and is_good(high) to be true."""
    while low < high:
        mid = low + (high - low) // 2
        if is_good(mid):
            high = mid                                   # mid works, but a smaller x might too: keep mid
        else:
            low = mid + 1                                # mid fails, so every smaller x fails as well
    return low

def last_true(low, high, is_good):
    """Largest x in [low, high] with is_good(x) true.

    Requires is_good to be true...true false...false over the range, and is_good(low) to be true."""
    while low < high:
        mid = low + (high - low + 1) // 2                # round UP so that `low = mid` always makes progress
        if is_good(mid):
            low = mid                                    # mid works, but a larger x might too: keep mid
        else:
            high = mid - 1                               # mid fails, so every larger x fails as well
    return low
```

- **Invariant for `first_true`:** every value below `low` fails; `high` works (or is the last candidate). When `low == high`, that value is the first that works.
- **Invariant for `last_true`:** every value above `high` fails; `low` works. The mirror image.
- **Why `last_true` rounds up.** With `low = mid` as the update, a midpoint that rounds *down* can equal `low`, so the range never shrinks. The smallest case shows it: with `low = 0`, `high = 1`, and `mid = 0`, a good `mid` sets `low = 0` again, forever.

```python
def last_true_rounding_down(low, high, is_good, guard=1_000):
    steps = 0
    while low < high:
        steps += 1
        if steps > guard:
            return "still looping after 1,000 steps"
        mid = low + (high - low) // 2                    # BUG: rounds down
        if is_good(mid):
            low = mid
        else:
            high = mid - 1
    return low

print(last_true_rounding_down(0, 1, lambda x: x == 0))
print(last_true(0, 1, lambda x: x == 0))                                                            # 0

import random

random.seed(1)
for _ in range(3_000):
    low = random.randint(-20, 20)
    high = low + random.randint(0, 40)
    threshold = random.randint(low, high)
    assert first_true(low, high, lambda x: x >= threshold) == threshold
    assert last_true(low, high, lambda x: x <= threshold) == threshold
print("first_true and last_true find the threshold in 3,000 random ranges")
```

```text
still looping after 1,000 steps
0
first_true and last_true find the threshold in 3,000 random ranges
```

## 🔢 Example 1: Integer Square Root

The integer square root of `n` is the largest `x` with `x·x <= n`. The test `x·x <= n` is true for small `x` and false for large `x`, so `last_true` finds the boundary in O(log n) steps:

```python
import math

def integer_sqrt(n):
    return last_true(0, n, lambda x: x * x <= n)

print(integer_sqrt(0), integer_sqrt(1), integer_sqrt(99), integer_sqrt(100), integer_sqrt(10**30))      # 0 1 9 10 1000000000000000

for n in range(10_000):
    assert integer_sqrt(n) == math.isqrt(n)
for _ in range(2_000):
    n = random.randint(0, 10 ** random.randint(1, 40))
    assert integer_sqrt(n) == math.isqrt(n)
print("integer_sqrt agrees with math.isqrt on 0..9,999 and 2,000 random integers up to 40 digits")
```

```text
0 1 9 10 1000000000000000
integer_sqrt agrees with math.isqrt on 0..9,999 and 2,000 random integers up to 40 digits
```

(Python's `math.isqrt` is the production answer; the point is that the same few lines solve the harder problems below.)

## 🍌 Example 2: The Slowest Eating Speed

*There are piles of bananas and `h` hours. Each hour you choose one pile and eat up to `k` bananas from it; if the pile has fewer than `k`, you finish it and waste the rest of that hour. What is the smallest `k` that finishes everything within `h` hours?*

- **Candidates:** speeds `1..max(piles)`. At `max(piles)` every pile takes one hour, so any `h >= len(piles)` is achievable.
- **Test:** at speed `k`, a pile of `p` bananas takes `ceil(p / k)` hours; the speed is good if the total is at most `h`.
- **Monotone:** a faster speed never takes more hours, so the pattern is `no … no yes … yes`: use `first_true`.

```python
def min_eating_speed(piles, hours):
    if hours < len(piles):
        raise ValueError("each pile needs at least one hour")
    def finishes_in_time(speed):
        return sum(-(-pile // speed) for pile in piles) <= hours            # -(-a // b) is ceil(a / b)
    return first_true(1, max(piles), finishes_in_time)

print(min_eating_speed([3, 6, 7, 11], 8))                       # 4
print(min_eating_speed([30, 11, 23, 4, 20], 5))                 # 30
print(min_eating_speed([30, 11, 23, 4, 20], 6))                 # 23

def brute_speed(piles, hours):
    return next(k for k in range(1, max(piles) + 1) if sum(-(-p // k) for p in piles) <= hours)

for _ in range(3_000):
    piles = [random.randint(1, 30) for _ in range(random.randint(1, 6))]
    hours = random.randint(len(piles), len(piles) + 40)
    assert min_eating_speed(piles, hours) == brute_speed(piles, hours)
print("min_eating_speed agrees with a linear scan of all speeds on 3,000 random cases")
```

```text
4
30
23
min_eating_speed agrees with a linear scan of all speeds on 3,000 random cases
```

Each test is O(n) (one pass over the piles), and there are about `log₂(max pile)` tests: for a thousand piles of up to a billion bananas that is roughly 30 passes instead of up to a billion.

## 🚚 Example 3: The Smallest Ship Capacity

*Packages with given weights must be shipped in order, and each day's load is a contiguous run of packages whose total weight cannot exceed the ship's capacity. What is the smallest capacity that ships everything within `days` days?*

- **Candidates:** capacities from `max(weights)` (the heaviest package must fit) to `sum(weights)` (everything in one day).
- **Test:** simulate greedily — load packages until the next one would overflow, then start a new day — and count the days. A larger ship never needs more days.
- **Monotone:** yes, so `first_true`.

```python
def days_needed(weights, capacity):
    days, load = 1, 0
    for w in weights:
        if load + w > capacity:                         # the next package does not fit: start a new day
            days += 1
            load = 0
        load += w
    return days

def ship_capacity(weights, days):
    return first_true(max(weights), sum(weights), lambda capacity: days_needed(weights, capacity) <= days)

print(ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))        # 15
print(ship_capacity([3, 2, 2, 4, 1, 4], 3))                     # 6

def brute_capacity(weights, days):
    return next(c for c in range(max(weights), sum(weights) + 1) if days_needed(weights, c) <= days)

for _ in range(3_000):
    weights = [random.randint(1, 15) for _ in range(random.randint(1, 8))]
    days = random.randint(1, len(weights))
    assert ship_capacity(weights, days) == brute_capacity(weights, days)
print("ship_capacity agrees with a linear scan of all capacities on 3,000 random cases")
```

```text
15
6
ship_capacity agrees with a linear scan of all capacities on 3,000 random cases
```

### The Same Problem in Disguise: Splitting an Array

*Split a list of non-negative numbers into `m` contiguous parts so that the largest part sum is as small as possible.* The "ship" is the part, the "capacity" is the largest allowed part sum, and the "days" are the `m` parts — it is the same problem, solved by `ship_capacity`. The exhaustive check below tries every way of cutting the list:

```python
import itertools

def split_array_largest_sum(nums, parts):
    return ship_capacity(nums, parts)

def brute_split(nums, parts):
    best = math.inf
    for cuts in itertools.combinations(range(1, len(nums)), parts - 1):
        bounds = (0,) + cuts + (len(nums),)
        best = min(best, max(sum(nums[bounds[i]:bounds[i + 1]]) for i in range(parts)))
    return best

print(split_array_largest_sum([7, 2, 5, 10, 8], 2))             # 18
for _ in range(2_000):
    nums = [random.randint(0, 20) for _ in range(random.randint(1, 8))]
    parts = random.randint(1, len(nums))
    assert split_array_largest_sum(nums, parts) == brute_split(nums, parts)
print("split_array_largest_sum agrees with trying every way to cut the list on 2,000 random cases")
```

```text
18
split_array_largest_sum agrees with trying every way to cut the list on 2,000 random cases
```

Recognizing that two problems share a feasibility test is most of the skill: "painter's partition", "allocate books to students", and "minimize the maximum" scheduling problems all reduce to the same loop.

## 🐄 Example 4: Maximize the Minimum

*Stalls stand at given positions on a line, and `c` cows must be placed in distinct stalls so that the smallest distance between any two cows is as large as possible.*

The direction flips: a *small* required distance is easy to satisfy and a large one is hard, so the pattern is `yes … yes no … no`, and we want the **last** yes — `last_true`. The test for a distance `d` is a greedy placement: put the first cow in the first stall and each next cow in the first stall at least `d` away from the previous cow; the distance is feasible if all `c` cows fit.

```python
def largest_minimum_distance(stalls, cows):
    stalls = sorted(stalls)
    def can_place(distance):
        placed, last = 1, stalls[0]
        for stall in stalls[1:]:
            if stall - last >= distance:
                placed += 1
                last = stall
        return placed >= cows
    return last_true(1, stalls[-1] - stalls[0], can_place)

print(largest_minimum_distance([1, 2, 4, 8, 9], 3))             # 3

def brute_distance(stalls, cows):
    return max(min(b - a for a, b in zip(chosen, chosen[1:])) for chosen in itertools.combinations(sorted(stalls), cows))

for _ in range(3_000):
    stalls = random.sample(range(1, 40), random.randint(2, 8))
    cows = random.randint(2, len(stalls))
    assert largest_minimum_distance(stalls, cows) == brute_distance(stalls, cows)
print("largest_minimum_distance agrees with trying every placement on 3,000 random cases")
```

```text
3
largest_minimum_distance agrees with trying every placement on 3,000 random cases
```

With stalls at 1, 2, 4, 8, 9 and three cows, placing them at 1, 4, and 8 or 9 keeps every pair at least 3 apart, and no placement does better.

## 🔬 Real-Valued Answers

When the answer is a real number — a cube root, the time two trains meet, the smallest radius that covers a region — there is no "next integer", and the loop ends when the interval is small enough. The obvious test, `while high - low > epsilon`, has a trap: floating-point numbers have **limited resolution**, and for large values the gap between neighbouring floats can be larger than your `epsilon`, so the interval can never shrink below it:

```python
def sqrt_with_epsilon(x, epsilon, guard=2_000):
    low, high = 0.0, max(1.0, x)
    steps = 0
    while high - low > epsilon:
        steps += 1
        if steps > guard:
            return f"still looping after {guard:,} steps"
        mid = (low + high) / 2
        if mid * mid <= x:
            low = mid
        else:
            high = mid
    return low, steps

print(sqrt_with_epsilon(2.0, 1e-9))                  # (sqrt(2) to nine decimals)
print(sqrt_with_epsilon(1e20, 1e-9))                 # (the gap between floats near 10^10 is about 2e-6: never below 1e-9)
print(sqrt_with_epsilon(1e20, 1e-3))                 # (a tolerance that floats can actually reach)
```

```text
(1.4142135614529252, 31)
still looping after 2,000 steps
(9999999999.999424, 77)
```

The robust pattern is a **fixed number of iterations**. Each iteration halves the interval, so 100 iterations shrink it by a factor of `2¹⁰⁰ ≈ 10³⁰` — long before that, the endpoints become neighbouring floats and further iterations change nothing:

```python
def cube_root(x, iterations=100):
    low, high = 0.0, max(1.0, x)
    for _ in range(iterations):
        mid = (low + high) / 2
        if mid ** 3 <= x:
            low = mid
        else:
            high = mid
    return low

print(f"{'x':>14} | {'binary search':>22} | {'x ** (1/3)':>22}")
for x in (0.0, 1.0, 2.0, 27.0, 1e-6, 123456.789, 1e9):
    print(f"{x:>14} | {cube_root(x):>22.15g} | {x ** (1 / 3):>22.15g}")
```

```text
             x |          binary search |             x ** (1/3)
           0.0 |                      0 |                      0
           1.0 |                      1 |                      1
           2.0 |       1.25992104989487 |       1.25992104989487
          27.0 |                      3 |                      3
         1e-06 |                   0.01 |                   0.01
    123456.789 |       49.7933859218174 |       49.7933859218174
  1000000000.0 |                   1000 |                   1000
```

For real-valued answers, compare results with `math.isclose` rather than `==`, and decide the precision you need first.

## ⚠️ The Monotonicity Requirement

Everything above relies on the test being monotone. If it is not, binary search does not fail loudly: it returns *an* answer, and that answer is wrong. Asking for the first multiple of 7 in `1..98` with a test that is true at the multiples of 7 (and, to satisfy the "true at the top" precondition, at 98) gives nonsense:

```python
print(first_true(1, 98, lambda x: x % 7 == 0 or x == 98))       # 49   — not 7: the test is not monotone
```

When you are unsure, prove monotonicity in a sentence ("a faster speed never takes more hours"), or test it on small ranges with a brute-force checker that looks for a "no" after a "yes":

```python
def is_monotone_nondecreasing(is_good, low, high):
    seen_true = False
    for x in range(low, high + 1):
        if is_good(x):
            seen_true = True
        elif seen_true:
            return False
    return True

print(is_monotone_nondecreasing(lambda x: x * x >= 50, 0, 100), is_monotone_nondecreasing(lambda x: x % 7 == 0, 1, 98))     # True False

piles = [30, 11, 23, 4, 20]
print("eating-speed test is monotone on 1..30:", is_monotone_nondecreasing(lambda k: sum(-(-pile // k) for pile in piles) <= 6, 1, 30))
```

```text
True False
eating-speed test is monotone on 1..30: True
```

## 🧭 Recognizing the Pattern

| Problem | Answer range | Test for a guess | Direction |
|---------|--------------|------------------|-----------|
| Integer square root | `0..n` | `x·x <= n` | largest true |
| Slowest eating speed | `1..max pile` | total hours `<= h` | smallest true |
| Ship capacity | `max weight..total weight` | days needed `<= D` | smallest true |
| Split array, minimize the largest sum | `max item..total` | parts needed `<= m` | smallest true |
| Cows in stalls, maximize the smallest gap | `1..span` | all cows fit | largest true |
| Real-valued roots, rates, and radii | an interval of reals | a monotone inequality | fixed iterations |

Look for these signs: the question asks for a *minimum* or *maximum* number; "the largest of the smallest" or "the smallest of the largest" appears in the statement; there is an easy way to *check* a proposed value (usually one greedy pass); and the check is monotone. Then:

1. Decide the **range** of candidate answers (low and high bounds that are certain to bracket the answer).
2. Write the **check**, and justify its monotonicity.
3. Pick `first_true` (minimize) or `last_true` (maximize).
4. Cost: `(cost of one check) × log₂(size of the range)`.

## Common Mistakes

- **A check that is not monotone.** The search returns a confident, wrong answer. Prove the direction before coding.
- **Wrong bounds.** If `low` is above the true answer, or `high` is not feasible, the loop quietly returns the wrong value. The bounds must *bracket* the answer: for example, a ship capacity below the heaviest package is never feasible, so starting there would be wasted — but starting above the answer would miss it.
- **Forgetting to round up in a "maximize" search**, which hangs on the smallest ranges.
- **Using `while high - low > epsilon` with floats**, which can loop forever for large values. Use a fixed iteration count.
- **A greedy check that is itself wrong.** The outer binary search is only as correct as the feasibility test; compare the whole solver with a brute-force one on small inputs, as this file does.
- **Overflow in languages with fixed-size integers**: sums of weights and products like `x * x` can exceed 32-bit or even 64-bit ranges. Python integers do not overflow, which is why the code here does not need to guard against it.

## Module Summary

This module followed one idea — *use structure to avoid looking at everything* — from its simplest form to its most general. [Linear Search](linear-search.md) set the baseline: no assumptions, O(n), and the built-in operations that do it fastest in Python, plus the traps where a hidden linear search turns a program quadratic. [Binary Search](binary-search.md) halved the possibilities with each probe on sorted data, proved the loop correct with an invariant, counted probes exactly (`⌊log₂ n⌋ + 1`), handled duplicates with lower and upper bounds, introduced Python's `bisect` module, and demonstrated the classic bugs. [Search Space Reduction](search-space-reduction.md) generalized halving to rotated arrays, peaks in unsorted data, sorted matrices, two pointers, unbounded sequences, and interpolation, each justified by an elimination argument. This file used the same boundary-finding loop on *answers* instead of positions, which solves optimization problems with a single greedy check.

Carry these ideas forward:

- Binary search needs **order or monotonicity**, not necessarily a sorted array; it halves any space in which a single test rules out a whole half.
- State the **invariant** first, then make every line preserve it; most binary search bugs are broken invariants.
- Use `first_true` / `last_true` over a range of candidate answers for "minimize the maximum" and "maximize the minimum" problems; the cost is one feasibility check times `log₂` of the range.
- In Python, use `bisect` for sorted lists and `sorted`, `set`, or `dict` when they fit; hand-written searches are for learning, interviews, and problems with no library equivalent.
- Duplicates, boundaries, and empty ranges are where search code fails: test them exhaustively on small inputs against a brute-force version.

## ➡️ Next

Continue to the [Bit Manipulation](../bit-manipulation/README.md) module, the next module in this domain, where the focus moves from searching through values to working with the individual bits inside them — a toolkit that makes some searches, counts, and checks astonishingly short.
