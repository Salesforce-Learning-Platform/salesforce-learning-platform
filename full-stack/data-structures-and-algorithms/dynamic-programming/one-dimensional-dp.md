# 📏 One-Dimensional Dynamic Programming

## When the State Is a Single Number

The simplest dynamic programs have a state described by **one number**: a position in an array, an amount of money, a number of steps. The table is a one-dimensional list, the recurrence usually looks back a fixed number of entries (or over all earlier entries), and the answer is a single cell or the best cell. Many of the best-known interview problems are of this kind, and they all follow the same five-step recipe from [dp-fundamentals.md](dp-fundamentals.md): **state, transition, base cases, order, answer**.

This file works through seven problem families — climbing stairs, house robber, decoding strings, coin change, maximum subarray, longest increasing subsequence, and word break — each with the recipe spelled out, a clean implementation, and a brute-force check that tries every possibility on thousands of small cases. All outputs were produced by running the code on CPython 3.9.

| Problem | State `dp[i]` means… | Transition | Time | Space |
|---------|----------------------|------------|------|-------|
| Climbing stairs | ways to reach step `i` | `dp[i] = sum of dp[i − s]` over allowed step sizes `s` | O(n·k) | O(n), or O(k) |
| Min-cost stairs | cheapest cost to reach step `i` | min of arriving from one or two steps back | O(n) | O(1) |
| House robber | best total using the first `i` houses | `max(skip house i, take house i + best up to i − 2)` | O(n) | O(1) |
| Decode ways | ways to decode the first `i` digits | add the 1-digit and 2-digit endings that are valid | O(n) | O(1) |
| Coin change | fewest coins for amount `a` | `1 + min(dp[a − c])` over coins `c` | O(amount·coins) | O(amount) |
| Maximum subarray | best sum of a subarray ending at `i` | `max(x, best ending at i − 1 + x)` | O(n) | O(1) |
| Longest increasing subsequence | longest one ending at `i` | `1 + max(dp[j])` over `j < i` with `nums[j] < nums[i]` | O(n²), or O(n log n) | O(n) |
| Word break | can the first `i` letters be segmented | some `j < i` with `dp[j]` true and `s[j:i]` a word | O(n²) | O(n) |

## 🪜 Climbing Stairs and Its Family

*You can climb 1 or 2 steps at a time. In how many distinct ways can you climb to the top of an `n`-step staircase?*

- **State:** `ways[i]` = the number of ways to reach step `i`.
- **Transition:** the last move was a 1-step or a 2-step, so `ways[i] = ways[i − 1] + ways[i − 2]` — the Fibonacci recurrence.
- **Base case:** `ways[0] = 1` (one way to stand at the bottom: do nothing).
- **Answer:** `ways[n]`.

Allowing other step sizes only changes which earlier entries are added:

```python
def climb_ways(n, steps=(1, 2)):
    ways = [1] + [0] * n
    for i in range(1, n + 1):
        ways[i] = sum(ways[i - s] for s in steps if i >= s)
    return ways[n]

print([climb_ways(n) for n in range(10)])                            # [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
print([climb_ways(n, (1, 2, 3)) for n in range(8)])                  # [1, 1, 2, 4, 7, 13, 24, 44]
print(climb_ways(100))                                               # 573147844013817084101
```

The answer for 100 steps is a 21-digit number that no brute-force enumeration could reach, and Python's integers hold it exactly — no overflow handling needed (in languages with fixed-width integers, problems like this ask for the answer "modulo 10⁹ + 7" for that reason).

### Minimum Cost Climbing

*Each step `i` has a cost to leave it. You may start on step 0 or step 1, and climb 1 or 2 steps at a time. What is the cheapest way to reach the top, just past the last step?*

The state becomes a cost instead of a count: `dp[i]` = the cheapest cost to stand on position `i`, and `dp[i] = min(dp[i − 1] + cost[i − 1], dp[i − 2] + cost[i − 2])` — arrive from the previous step and pay its cost, or from two steps back and pay that cost. The top is position `len(cost)`.

```python
def min_cost_climbing(cost):
    n = len(cost)
    dp = [0] * (n + 1)                                               # dp[0] = dp[1] = 0: starting on either step is free
    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
    return dp[n]

print(min_cost_climbing([10, 15, 20]), min_cost_climbing([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]))      # 15 6
```

## 🏠 House Robber

*A row of houses holds money `nums[i]`. Adjacent houses have linked alarms: robbing two neighbours triggers the police. What is the most you can take?*

- **State:** `best[i]` = the most you can take from the first `i` houses.
- **Transition:** for house `i` there are two choices. **Skip it:** `best[i − 1]`. **Rob it:** `nums[i − 1] + best[i − 2]` (you could not have robbed house `i − 1`). Take the larger.
- **Base cases:** `best[0] = 0`, `best[1] = nums[0]`.

Since each entry depends on only the previous two, two variables replace the table:

```python
def rob(nums):
    skip, take = 0, 0                    # best total if the latest house is not robbed / is robbed
    for money in nums:
        skip, take = max(skip, take), skip + money
    return max(skip, take)

def rob_in_a_circle(nums):
    """The first and last houses are also neighbours: rob one of the two ranges that exclude one end."""
    if len(nums) == 1:
        return nums[0]
    return max(rob(nums[:-1]), rob(nums[1:]))

print(rob([2, 7, 9, 3, 1]), rob_in_a_circle([2, 3, 2]), rob_in_a_circle([1, 2, 3, 1]))          # 12 3 4
```

The circular variant reduces to the linear problem twice: in a valid plan, either the first house or the last house is not robbed (they are neighbours), so the best plan is the better of "linear problem without the last house" and "linear problem without the first house".

## 🔢 Decode Ways

*A message of digits encodes letters with `1 → A, 2 → B, …, 26 → Z`. In how many ways can a digit string be decoded? (`"12"` can be read as `1,2` = "AB" or as `12` = "L".)*

- **State:** `ways[i]` = the number of ways to decode the first `i` digits.
- **Transition:** the last letter used either the last digit alone (valid if it is not `'0'`) or the last two digits (valid if they form a number from 10 to 26): `ways[i] = (ways[i − 1] if s[i−1] != '0') + (ways[i − 2] if 10 ≤ int(s[i−2:i]) ≤ 26)`.
- **Base case:** `ways[0] = 1` (the empty prefix has one decoding: nothing).

```python
def decode_ways(s):
    if not s:
        return 0
    ways = [1] + [0] * len(s)
    for i in range(1, len(s) + 1):
        if s[i - 1] != "0":
            ways[i] += ways[i - 1]                                   # the last digit stands alone
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            ways[i] += ways[i - 2]                                   # the last two digits form one letter
    return ways[-1]

print([decode_ways(s) for s in ("12", "226", "06", "10", "2101", "11106")])                   # [2, 3, 0, 1, 1, 2]
```

The zeros are the subtle part: a `'0'` can never be decoded alone, and it is only usable as the second digit of `10` or `20`. `"06"` has no decoding at all — a leading zero cannot start a letter — and `"10"` has exactly one.

## 🪙 Coin Change: The Fewest Coins

*Given coin values and a target amount, what is the fewest coins that sum exactly to the amount (any coin may be used any number of times)? Report that no combination works if none does.*

- **State:** `fewest[a]` = the fewest coins that make amount `a`.
- **Transition:** the last coin used was some `c`, so `fewest[a] = 1 + min(fewest[a − c])` over coins `c ≤ a`.
- **Base case:** `fewest[0] = 0`; unreachable amounts hold infinity.

[dp-fundamentals.md](dp-fundamentals.md) showed why greedy fails here (coins 1, 3, 4 and amount 6). Remembering which coin achieved each minimum lets you reconstruct the coins used by walking back from the amount:

```python
def coin_change_min(coins, amount):
    infinity = float("inf")
    fewest = [0] + [infinity] * amount
    last_coin = [None] * (amount + 1)
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and fewest[a - coin] + 1 < fewest[a]:
                fewest[a] = fewest[a - coin] + 1
                last_coin[a] = coin
    if fewest[amount] == infinity:
        return None, []
    used, a = [], amount
    while a:
        used.append(last_coin[a])                                    # walk back through the choices that were made
        a -= last_coin[a]
    return fewest[amount], sorted(used, reverse=True)

print(coin_change_min([1, 2, 5], 11), coin_change_min([2], 3), coin_change_min([1, 3, 4], 6))      # (3, [5, 5, 1]) (None, []) (2, [3, 3])
```

Storing a "parent" pointer next to each table entry — the choice that produced the optimum — is the standard way to turn the *value* of an optimal solution into the *solution itself*. The counting version of this problem (how many combinations?) belongs with the [knapsack patterns](knapsack-patterns.md).

## ➕ Maximum Subarray (Kadane's Algorithm)

*Find the contiguous run of a list of numbers (positive and negative) with the largest sum.*

- **State:** `ending_here[i]` = the best sum of a subarray that **ends exactly at** index `i`.
- **Transition:** that subarray either extends the best one ending at `i − 1`, or starts fresh at `i`: `ending_here[i] = max(nums[i], ending_here[i − 1] + nums[i])`.
- **Answer:** the maximum over all `i` (the best subarray must end somewhere).

Defining the state as "ends exactly at `i`" rather than "best so far" is what makes the transition work, and the one-variable form below is known as Kadane's algorithm:

```python
def max_subarray(nums):
    """Return (best sum, (start, end)) of a non-empty contiguous subarray."""
    best = ending_here = nums[0]
    start = best_start = best_end = 0
    for i in range(1, len(nums)):
        if nums[i] > ending_here + nums[i]:                          # a fresh start beats extending a poor prefix
            ending_here, start = nums[i], i
        else:
            ending_here += nums[i]
        if ending_here > best:
            best, best_start, best_end = ending_here, start, i
    return best, (best_start, best_end)

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))                 # (6, (3, 6))
```

The winning run is `[4, -1, 2, 1]` at indexes 3 to 6. A brute-force scan of every start and end would cost O(n²) (or O(n³) when summing each range afresh); the DP does it in one pass.

## 📈 Longest Increasing Subsequence

*Find the length of the longest strictly increasing subsequence (not necessarily contiguous) of a list.*

- **State:** `best[i]` = the length of the longest increasing subsequence that **ends at** index `i`.
- **Transition:** it extends the best subsequence ending at any earlier smaller element: `best[i] = 1 + max(best[j])` over `j < i` with `nums[j] < nums[i]` (or `1` if none).
- **Answer:** `max(best)`.

That is O(n²). A famous refinement runs in **O(n log n)** by keeping, for each length `L`, the *smallest possible last element* of an increasing subsequence of length `L`. The list `tails` is always sorted, so a new element either extends the longest subsequence (if it is larger than every tail) or **replaces** the first tail that is at least as large — a binary search, using [`bisect`](../searching-algorithms/binary-search.md). The list `tails` is not itself a subsequence; only its *length* is the answer:

```python
import bisect

def lis_quadratic(nums):
    if not nums:
        return 0
    best = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best)

def lis_fast(nums):
    tails = []                                                       # tails[L-1] = smallest last element of an increasing run of length L
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)                                          # x extends the longest run found so far
        else:
            tails[i] = x                                             # x is a smaller ending for runs of length i + 1
    return len(tails)

print(lis_quadratic([10, 9, 2, 5, 3, 7, 101, 18]), lis_fast([10, 9, 2, 5, 3, 7, 101, 18]))      # 4 4
```

Using `bisect_left` finds the first tail `>= x`, which keeps the subsequence *strictly* increasing; `bisect_right` would allow equal elements. How much difference does the better algorithm make?

```python
import random
import timeit

random.seed(7)
print(f"{'n':>6} | {'LIS length':>10} | {'O(n^2) DP':>11} | {'O(n log n)':>11}")
for n in (500, 1_000, 2_000, 4_000):
    data = [random.randint(0, 10**6) for _ in range(n)]
    assert lis_quadratic(data) == lis_fast(data)
    quadratic_ms = min(timeit.repeat(lambda: lis_quadratic(data), number=1, repeat=2)) * 1000
    fast_ms = min(timeit.repeat(lambda: lis_fast(data), number=1, repeat=3)) * 1000
    print(f"{n:>6,} | {lis_fast(data):>10} | {quadratic_ms:>8.1f} ms | {fast_ms:>8.2f} ms")
```

Output:

```
     n | LIS length |   O(n^2) DP |  O(n log n)
   500 |         45 |     10.2 ms |     0.06 ms
 1,000 |         58 |     39.9 ms |     0.13 ms
 2,000 |         86 |    161.8 ms |     0.24 ms
 4,000 |        119 |    660.7 ms |     0.51 ms
```

Each doubling of `n` roughly quadruples the quadratic version and barely more than doubles the fast one; at 4,000 items the refinement is more than a thousand times faster.

## 🔤 Word Break

*Given a string and a dictionary of words, can the string be split into a sequence of dictionary words?*

- **State:** `ok[i]` = true if the first `i` characters can be segmented.
- **Transition:** `ok[i]` is true if some split point `j < i` has `ok[j]` true and `s[j:i]` is a word.
- **Base case:** `ok[0] = True` (the empty prefix).
- **Answer:** `ok[len(s)]`.

```python
def word_break(s, words):
    dictionary = set(words)
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        ok[i] = any(ok[j] and s[j:i] in dictionary for j in range(i))
    return ok[len(s)]

print(word_break("leetcode", ["leet", "code"]), word_break("applepenapple", ["apple", "pen"]), word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))       # True True False
```

Without the table, the recursion re-solves the same suffixes many times: a string of 30 letters `a` with the words `a`, `aa`, and `aaa` can be segmented in 53,798,080 different ways (the stair-climbing count for steps of 1, 2, and 3), and a plain recursion would visit them all. With the table, each prefix is solved once. The cost is O(n²) prefix pairs times the cost of a substring-and-lookup. (A trie of the dictionary can speed up the inner test, which is a natural combination for the Tries module later in this domain.)

## ✅ Verification

Every function above was compared with a brute-force definition on thousands of small random inputs: all recursive paths for the stair problems, every subset of non-adjacent houses, every split of a digit string, every combination of coins, every contiguous range, every subset of a list for the increasing subsequence, and a plain recursive segmentation of the string:

```python
def climb_brute(n, steps):
    return 1 if n == 0 else sum(climb_brute(n - s, steps) for s in steps if n >= s)

def min_cost_brute(cost):
    def from_position(i):
        return 0 if i >= len(cost) else cost[i] + min(from_position(i + 1), from_position(i + 2))
    return min(from_position(0), from_position(1))

def rob_brute(nums, circle=False):
    best = 0
    for mask in range(1 << len(nums)):
        chosen = [i for i in range(len(nums)) if mask >> i & 1]
        if any(b - a == 1 for a, b in zip(chosen, chosen[1:])):
            continue
        if circle and len(nums) > 1 and 0 in chosen and len(nums) - 1 in chosen:
            continue
        best = max(best, sum(nums[i] for i in chosen))
    return best

def decode_brute(s):
    if s == "":
        return 1
    if s[0] == "0":
        return 0
    return decode_brute(s[1:]) + (decode_brute(s[2:]) if len(s) >= 2 and 10 <= int(s[:2]) <= 26 else 0)

def coin_brute(coins, amount):
    best = None
    def go(rest, count):
        nonlocal best
        if rest == 0:
            best = count if best is None else min(best, count)
            return
        for coin in coins:
            if coin <= rest:
                go(rest - coin, count + 1)
    go(amount, 0)
    return best

def lis_brute(nums):
    best = 0
    for mask in range(1 << len(nums)):
        subsequence = [nums[i] for i in range(len(nums)) if mask >> i & 1]
        if all(a < b for a, b in zip(subsequence, subsequence[1:])):
            best = max(best, len(subsequence))
    return best

def word_break_brute(s, words):
    return s == "" or any(s.startswith(w) and word_break_brute(s[len(w):], words) for w in words)

import random

random.seed(1)
for _ in range(1_500):
    for steps in ((1, 2), (1, 2, 3), (2, 5), (1, 3, 4)):
        n = random.randint(0, 14)
        assert climb_ways(n, steps) == climb_brute(n, steps)
    costs = [random.randint(0, 20) for _ in range(random.randint(2, 10))]
    assert min_cost_climbing(costs) == min_cost_brute(costs)
    houses = [random.randint(0, 15) for _ in range(random.randint(1, 10))]
    assert rob(houses) == rob_brute(houses) and rob_in_a_circle(houses) == rob_brute(houses, circle=True)
    digits = "".join(random.choice("0123456789") if random.random() < 0.3 else random.choice("12") for _ in range(random.randint(1, 10)))
    assert decode_ways(digits) == decode_brute(digits)
    coins = random.sample(range(1, 9), random.randint(1, 3))
    amount = random.randint(0, 14)
    fewest, used = coin_change_min(coins, amount)
    assert fewest == coin_brute(coins, amount) and (fewest is None or (sum(used) == amount and len(used) == fewest))
    numbers = [random.randint(-9, 9) for _ in range(random.randint(1, 12))]
    best, (i, j) = max_subarray(numbers)
    assert best == max(sum(numbers[a:b + 1]) for a in range(len(numbers)) for b in range(a, len(numbers))) and sum(numbers[i:j + 1]) == best
    sequence = [random.randint(0, 12) for _ in range(random.randint(0, 11))]
    assert lis_quadratic(sequence) == lis_fast(sequence) == lis_brute(sequence)
    vocabulary = {"".join(random.choice("ab") for _ in range(random.randint(1, 3))) for _ in range(random.randint(1, 4))}
    text = "".join(random.choice("ab") for _ in range(random.randint(0, 9)))
    assert word_break(text, vocabulary) == word_break_brute(text, vocabulary)
print("all seven solutions agree with their brute-force definitions on 1,500 rounds of random inputs")
```

```text
all seven solutions agree with their brute-force definitions on 1,500 rounds of random inputs
```

## 🧭 Choosing the State

All of these problems hinge on one design decision: **what exactly does `dp[i]` mean?** Notice how the right definition changed the difficulty:

- For maximum subarray, "the best sum **ending at** `i`" works and "the best sum within the first `i` items" does not — the second cannot be extended by one element without knowing how the best run ended.
- For longest increasing subsequence, "the longest one **ending at** `i`" gives a transition; "the longest within the first `i`" does not.
- For house robber, the state needs to remember only whether the latest house was taken, and so two variables suffice.

When a transition seems impossible to write, change the state. The usual fixes are to add the missing information ("ending at `i`", "using the first `i` items and capacity `w`", "having taken or skipped the last one"), which is exactly how the [knapsack](knapsack-patterns.md) and [string](string-dp.md) problems grow a second dimension.

## Common Mistakes

- **Off-by-one in the table size.** `ways` has `n + 1` entries because positions run from `0` to `n`; mixing indexes into the input with indexes into the table (`cost[i − 1]` versus `dp[i]`) is the usual culprit.
- **Forgetting the zero cases.** Decode ways with `'0'` characters, coin change with amount `0`, and the empty string for word break are the places where the recurrence needs care.
- **Initializing unreachable states with `0`.** In minimization problems use infinity (or `None`) so that "impossible" is not mistaken for "free".
- **Using "best so far" as the state** when the transition needs to know how the best solution ends (maximum subarray, increasing subsequence).
- **Returning the table's last entry when the answer is the best entry** (maximum subarray and increasing subsequence take the maximum over all `i`).
- **Rebuilding a solution without parent pointers.** The table gives the *value*; to report the coins or items chosen, record the choice that produced each optimum.

## ➡️ Next

Continue to [knapsack-patterns.md](knapsack-patterns.md): add a second dimension — a capacity — and the same recipe covers choosing items under a budget, deciding whether a target sum is reachable, splitting a collection into equal halves, counting signed sums, and the combinations-versus-permutations question that hides in coin change.
