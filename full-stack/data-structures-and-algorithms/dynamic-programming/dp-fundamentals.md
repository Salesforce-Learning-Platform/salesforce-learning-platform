# 🧩 Dynamic Programming Fundamentals

## Recursion That Remembers

Some problems can be solved by combining the answers to smaller versions of the same problem — and the smaller versions keep repeating. Computing the 30th Fibonacci number by the textbook recursion makes nearly three million calls, yet only 31 different questions are ever asked. **Dynamic programming (DP)** is the discipline of answering each distinct question **once**, remembering the answer, and reusing it. The result is often an exponential-time algorithm turned into a polynomial-time one by adding a table.

A problem is a candidate for DP when it has two properties:

1. **Optimal substructure.** The answer to the whole problem can be built from the answers to smaller subproblems.
2. **Overlapping subproblems.** The same subproblems come up again and again, so remembering them saves work. (When the subproblems do *not* overlap — as in [merge sort](../sorting-algorithms/merge-sort.md), where each half is sorted separately — plain divide and conquer is enough and a table adds nothing.)

There are two ways to organize the remembering. **Top-down** (memoization) keeps the natural recursion and adds a cache. **Bottom-up** (tabulation) fills a table from the smallest subproblems upward with plain loops. This file shows both on Fibonacci numbers, compares them with measurements, introduces a five-step recipe, applies it to a grid problem with a brute-force check, and contrasts DP with greedy algorithms. The later files apply the recipe to [one-dimensional problems](one-dimensional-dp.md), [knapsack patterns](knapsack-patterns.md), and [string problems](string-dp.md). All outputs were produced by running the code on CPython 3.9.

## 🔁 The Problem: Overlapping Subproblems

The Fibonacci numbers are defined by `F(0) = 0`, `F(1) = 1`, and `F(n) = F(n-1) + F(n-2)`. Translated directly into code:

```python
def fib_naive(n):
    """Return (F(n), the number of function calls made)."""
    calls = 0
    def fib(k):
        nonlocal calls
        calls += 1
        return k if k < 2 else fib(k - 1) + fib(k - 2)
    return fib(n), calls

def fib_value(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(f"{'n':>3} | {'F(n)':>8} | {'calls':>10} | {'2*F(n+1) - 1':>12}")
for n in (5, 10, 20, 25, 30):
    value, calls = fib_naive(n)
    print(f"{n:>3} | {value:>8,} | {calls:>10,} | {2 * fib_value(n + 1) - 1:>12,}")
```

```text
  n |     F(n) |      calls | 2*F(n+1) - 1
  5 |        5 |         15 |           15
 10 |       55 |        177 |          177
 20 |    6,765 |     21,891 |       21,891
 25 |   75,025 |    242,785 |      242,785
 30 |  832,040 |  2,692,537 |    2,692,537
```

The call count grows by a factor of about 1.6 for every step of `n` — it is *exponential*. It satisfies `calls(n) = 2·F(n+1) − 1`, as the last column confirms, so `fib(50)` would need about 40 billion calls. The reason is visible in the call tree: `fib(5)` calls `fib(4)` and `fib(3)`, and `fib(4)` calls `fib(3)` again, so `fib(3)` is computed twice, `fib(2)` three times, and so on. Only `n + 1` different questions exist (`F(0)` through `F(n)`); the tree asks the same ones over and over.

## 📝 Top-Down: Memoization

Keep the recursion, but before computing a subproblem, look it up in a cache; after computing it, store it. Each distinct subproblem is now computed once:

```python
def fib_memo(n):
    """Return (F(n), the number of function calls made), caching results in a dictionary."""
    cache = {}
    calls = 0
    def fib(k):
        nonlocal calls
        calls += 1
        if k < 2:
            return k
        if k not in cache:
            cache[k] = fib(k - 1) + fib(k - 2)
        return cache[k]
    return fib(n), calls

print([fib_memo(n)[1] for n in (5, 10, 20, 30)])                 # [9, 19, 39, 59]
```

The number of calls is now `2n − 1`: linear instead of exponential. Python's standard library does the caching for you with `functools.lru_cache` (`maxsize=None` means unlimited; `functools.cache` is a shorthand added in Python 3.9), and `cache_info()` reports how well it worked ([Python docs: functools](https://docs.python.org/3/library/functools.html#functools.lru_cache)):

```python
import functools

@functools.lru_cache(maxsize=None)
def fib_cached(n):
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)

print(fib_cached(30))
print(fib_cached.cache_info())
```

```text
832040
CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
```

There were 31 *misses* — each of `F(0)` … `F(30)` computed once — and 28 *hits*, the repeated questions answered from the cache. (Arguments must be hashable, since they are used as dictionary keys: use tuples rather than lists for multi-part states.)

## 🏗️ Bottom-Up: Tabulation

Instead of starting from the big problem and recursing down, start from the base cases and build upward. The table of answers is filled in an order that guarantees every value needed is already there. For Fibonacci, the order is simply `0, 1, 2, …, n`:

```python
def fib_table(n):
    table = [0, 1] + [0] * max(0, n - 1)
    for k in range(2, n + 1):
        table[k] = table[k - 1] + table[k - 2]
    return table[n]

def fib_rolling(n):
    """The same recurrence keeping only the last two values: O(1) space."""
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous

print(fib_table(10), fib_rolling(10), fib_table(90) == fib_rolling(90) == fib_cached(90))        # 55 55 True
```

Look at what the recurrence needs: `table[k]` depends only on the previous two entries, so the whole table is unnecessary and two variables suffice. This **space optimization** — keeping only as many rows or values as the recurrence reaches back — recurs throughout dynamic programming.

## ⚖️ Top-Down or Bottom-Up?

Both do the same amount of arithmetic, but they differ in practice. First, **recursion depth**: top-down memoization still recurses `n` levels deep before it can start filling the cache, and Python's default limit is about 1,000 frames. A function wrapped by `lru_cache` uses more of that limit per level than a plain function (in CPython 3.9 the wrapper itself counts, as the measurement below shows). The block below finds the largest `n` that each style handles before hitting `RecursionError`:

```python
def fib_manual_memo(n, cache):
    if n < 2:
        return n
    if n not in cache:
        cache[n] = fib_manual_memo(n - 1, cache) + fib_manual_memo(n - 2, cache)
    return cache[n]

def largest_n_that_works(solve, upper=5_000):
    low, high = 1, upper
    while low < high:
        mid = (low + high + 1) // 2
        try:
            solve(mid)
            low = mid
        except RecursionError:
            high = mid - 1
        fib_cached.cache_clear()
    return low

print("dictionary memo, recursive:  ", largest_n_that_works(lambda n: fib_manual_memo(n, {})))
print("lru_cache memo, recursive:   ", largest_n_that_works(fib_cached))
print("table, bottom-up (capped at 5,000):", largest_n_that_works(fib_table))
```

```text
dictionary memo, recursive:   994
lru_cache memo, recursive:    497
table, bottom-up (capped at 5,000): 5000
```

The recursive versions stop at roughly 1,000 and 500 levels (the exact numbers vary slightly with where the call starts); the loop has no such limit. Raising the limit with `sys.setrecursionlimit` is possible but risks crashing the interpreter on very deep recursion, so for problems whose natural recursion is thousands of levels deep, **write the bottom-up version**.

Second, **how many subproblems are actually needed.** Top-down computes only the subproblems that the recursion reaches; bottom-up fills the whole table. When most states are unreachable, top-down wins. As an example, take *the fewest coins needed to make an amount*, with coin values 25, 50, and 100:

```python
def coin_change_top_down(coins, amount):
    """Return (fewest coins or None, number of distinct subproblems solved)."""
    @functools.lru_cache(maxsize=None)
    def fewest(rest):
        if rest == 0:
            return 0
        options = [fewest(rest - c) for c in coins if rest - c >= 0]
        options = [o for o in options if o is not None]
        return min(options) + 1 if options else None
    result = fewest(amount)
    return result, fewest.cache_info().currsize

def coin_change_bottom_up(coins, amount):
    """Return (fewest coins or None, number of table entries computed)."""
    infinity = float("inf")
    table = [0] + [infinity] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if a >= c and table[a - c] + 1 < table[a]:
                table[a] = table[a - c] + 1
    return (table[amount] if table[amount] != infinity else None), amount + 1

print("amount 5000:", coin_change_top_down((25, 50, 100), 5_000), coin_change_bottom_up((25, 50, 100), 5_000))
print("amount 4999:", coin_change_top_down((25, 50, 100), 4_999), coin_change_bottom_up((25, 50, 100), 4_999))
```

```text
amount 5000: (50, 201) (50, 5001)
amount 4999: (None, 200) (None, 5000)
```

Each pair is `(answer, states solved)`. Since every amount reachable from 5,000 by subtracting 25, 50, or 100 is a multiple of 25, the top-down version solves only 201 states, while the bottom-up table computes all 5,001. For the impossible amount 4,999 the difference is as large. When almost every state is needed, as in most textbook problems, the two are equally fast and the bottom-up loop is usually a little quicker because it avoids function-call overhead:

```python
import timeit

naive_ms = min(timeit.repeat(lambda: fib_naive(30), number=1, repeat=2)) * 1000
memo_us = min(timeit.repeat(lambda: fib_memo(30), number=200, repeat=3)) / 200 * 1e6
table_us = min(timeit.repeat(lambda: fib_table(30), number=2_000, repeat=3)) / 2_000 * 1e6
rolling_us = min(timeit.repeat(lambda: fib_rolling(30), number=2_000, repeat=3)) / 2_000 * 1e6
print(f"naive recursion  F(30): {naive_ms:10.2f} ms")
print(f"memoized         F(30): {memo_us:10.2f} us")
print(f"table            F(30): {table_us:10.2f} us")
print(f"two variables    F(30): {rolling_us:10.2f} us")
```

Output:

```
naive recursion  F(30):     199.22 ms
memoized         F(30):       6.30 us
table            F(30):       1.96 us
two variables    F(30):       0.77 us
```

Going from naive recursion to any of the DP versions removes four to five orders of magnitude of work at `n = 30` (a factor of roughly 30,000 to 250,000 in this run) — and the gap widens exponentially as `n` grows.

| | Top-down (memoization) | Bottom-up (tabulation) |
|--|------------------------|------------------------|
| Code shape | The natural recursion plus a cache | Loops that fill a table |
| Subproblems computed | Only those reached | All of them |
| Recursion limit | A risk for deep problems | None |
| Space optimization | Harder | Easy: keep only the rows or values needed |
| Best when | Many states are unreachable; the recurrence is easier to write recursively | The state space is dense or deep; you need speed or low memory |

## 🧭 A Five-Step Recipe

Every DP solution answers the same five questions. Write them down before writing code:

1. **State.** What does a subproblem look like? (Which numbers uniquely identify it? `n`, or `(row, column)`, or `(i, remaining_capacity)`.) State it in words: *"`best[r][c]` is the cheapest cost of a path from the top-left cell to cell `(r, c)`."*
2. **Transition.** How is a state's answer computed from the answers of smaller states? This is the recurrence.
3. **Base cases.** Which states are answered directly?
4. **Order.** In which order must states be computed so the transition's inputs already exist? (Bottom-up only; top-down gets this from the recursion.)
5. **Answer.** Which state holds the answer to the original problem?

The running time is then **(number of states) × (work per transition)**, and the space is the number of states you must keep.

### Worked Example: The Cheapest Path Through a Grid

*A grid of non-negative costs; you start at the top-left cell and may only move right or down. What is the cheapest total cost of a path to the bottom-right cell?*

1. **State:** `best(r, c)` = the cheapest cost of a path from the start to cell `(r, c)`.
2. **Transition:** the last move came from above or from the left, so `best(r, c) = cost[r][c] + min(best(r-1, c), best(r, c-1))`.
3. **Base cases:** `best(0, 0) = cost[0][0]`; in the first row only the left neighbour exists, in the first column only the one above.
4. **Order:** row by row, left to right.
5. **Answer:** `best(rows-1, cols-1)`.

There are `rows × cols` states, each computed in O(1): O(rows × cols) in total. The recursion without a cache would explore every path, and the number of paths is a binomial coefficient that explodes — 48,620 paths already in a 10×10 grid.

```python
import itertools
import random

def grid_min_path_top_down(grid):
    @functools.lru_cache(maxsize=None)
    def best(r, c):
        if r == 0 and c == 0:
            return grid[0][0]
        options = []
        if r > 0:
            options.append(best(r - 1, c))                 # arrived from above...
        if c > 0:
            options.append(best(r, c - 1))                 # ...or from the left
        return grid[r][c] + min(options)
    return best(len(grid) - 1, len(grid[0]) - 1)

def grid_min_path_bottom_up(grid):
    rows, cols = len(grid), len(grid[0])
    best = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                best[r][c] = grid[0][0]
            elif r == 0:
                best[r][c] = best[r][c - 1] + grid[r][c]
            elif c == 0:
                best[r][c] = best[r - 1][c] + grid[r][c]
            else:
                best[r][c] = min(best[r - 1][c], best[r][c - 1]) + grid[r][c]
    return best[-1][-1]

def grid_min_path_one_row(grid):
    """Keep one row: row[c] holds the answer for the current row, updated in place."""
    cols = len(grid[0])
    row = [0] * cols
    for r, line in enumerate(grid):
        for c in range(cols):
            if r == 0 and c == 0:
                row[c] = line[c]
            elif r == 0:
                row[c] = row[c - 1] + line[c]
            elif c == 0:
                row[c] = row[c] + line[c]                  # row[c] still holds the value from the row above
            else:
                row[c] = min(row[c], row[c - 1]) + line[c]  # min(from above, from the left)
    return row[-1]

def grid_min_path_brute_force(grid):
    """Try every path: choose which of the (rows - 1 + cols - 1) steps go down."""
    rows, cols = len(grid), len(grid[0])
    best = float("inf")
    for down_steps in itertools.combinations(range(rows + cols - 2), rows - 1):
        r = c = 0
        total = grid[0][0]
        for step in range(rows + cols - 2):
            if step in down_steps:
                r += 1
            else:
                c += 1
            total += grid[r][c]
        best = min(best, total)
    return best

example = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
print(grid_min_path_top_down(tuple(map(tuple, example))), grid_min_path_bottom_up(example), grid_min_path_one_row(example))       # 7 7 7
print(len(list(itertools.combinations(range(18), 9))), "paths through a 10 x 10 grid")

random.seed(1)
for _ in range(2_000):
    rows, cols = random.randint(1, 5), random.randint(1, 5)
    grid = [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]
    frozen = tuple(tuple(line) for line in grid)
    expected = grid_min_path_brute_force(grid)
    assert grid_min_path_top_down(frozen) == grid_min_path_bottom_up(grid) == grid_min_path_one_row(grid) == expected
print("top-down, bottom-up, and one-row versions agree with trying every path on 2,000 random grids")
```

```text
7 7 7
48620 paths through a 10 x 10 grid
top-down, bottom-up, and one-row versions agree with trying every path on 2,000 random grids
```

The three DP versions use the same recurrence in different forms, and the brute-force check — which tries every path, impractical beyond tiny grids — confirms them. The single-row version shows space optimization again: each row depends only on the one above, so one row of storage replaces the whole table (`O(cols)` instead of `O(rows × cols)`).

## 🆚 DP, Greedy, and Divide and Conquer

DP is often confused with two neighbours:

- **Divide and conquer** splits a problem into *independent* subproblems (merge sort's two halves). Nothing repeats, so no table is needed.
- **A greedy algorithm** makes the locally best choice at each step and never reconsiders. When that is provably correct, it is faster than DP. When it is not, the answer is simply wrong, and DP — which weighs *all* the choices through the table — is the safe alternative.

The standard demonstration is making change. With coins of 1, 3, and 4, the amount 6 is best made as 3 + 3 (two coins), but greedy takes the biggest coin first — 4 + 1 + 1 — and uses three:

```python
def coin_change_greedy(coins, amount):
    count = 0
    for coin in sorted(coins, reverse=True):
        count += amount // coin
        amount %= coin
    return count if amount == 0 else None

print(coin_change_greedy((1, 3, 4), 6), coin_change_bottom_up((1, 3, 4), 6)[0])            # 3 2
print(coin_change_greedy((1, 5, 10, 25), 63), coin_change_bottom_up((1, 5, 10, 25), 63)[0])     # 6 6
```

For US coin values (1, 5, 10, 25) greedy happens to be optimal, which is why it works for cash registers; for coins (1, 3, 4) it is not, and no local rule fixes it. If you cannot *prove* that the greedy choice is safe, use DP.

## Common Mistakes

- **Starting with code instead of the state.** If you cannot say in one sentence what a table entry means, the recurrence will be wrong. Write the state down first.
- **Missing or wrong base cases.** Most DP bugs are in the first row, the first column, `n = 0`, or an empty input.
- **Using an unhashable argument with a cache.** `lru_cache` needs hashable arguments; pass tuples, not lists.
- **Filling the table in the wrong order.** Each entry's inputs must already be computed — row by row for the grid, increasing `k` for Fibonacci.
- **Deep recursion in Python.** A memoized recursion with thousands of levels raises `RecursionError`; switch to bottom-up.
- **Expecting DP to help when subproblems do not overlap.** A table costs memory; use it only when the same subproblems actually recur.
- **Treating greedy as DP.** If locally best choices are not provably safe, they can be wrong (coins 1, 3, 4).

## ➡️ Next

Continue to [one-dimensional-dp.md](one-dimensional-dp.md), where the state is a single number and the recipe is applied to a family of classic problems: climbing stairs, house robber, decoding strings, coin change, maximum subarray, longest increasing subsequence, and word break.
