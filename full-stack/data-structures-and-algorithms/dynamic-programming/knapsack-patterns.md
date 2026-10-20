# 🎒 Knapsack Patterns

## Choosing Items Under a Budget

A hiker has a pack that holds at most 7 kilograms and a pile of items, each with a weight and a value. Which items should go in the pack to maximize the total value? That is the **knapsack problem**, and its shape — *choose among items, subject to a limit on a total* — appears all over computing: packing a shipment, picking projects under a budget, filling a time slot, splitting a bill, reaching an exact target sum, making change.

The state needs two pieces of information, so the table has two dimensions: **which items have been considered** and **how much capacity is left**. This file develops the variants one at a time:

| Variant | Each item can be used… | Question | Example |
|---------|------------------------|----------|---------|
| 0/1 knapsack | at most once | Maximum total value within the capacity | Packing a bag |
| Subset sum | at most once | Can some items sum to exactly the target? | Exact change from a pile of bills |
| Partition | at most once | Can the items be split into two equal-sum halves? | Splitting a bill fairly |
| Target sum | exactly once, with a `+` or `−` sign | In how many ways do the signed items sum to the target? | Counting sign assignments |
| Unbounded knapsack | any number of times | Maximum total value within the capacity | Cutting a rod, filling a truck |
| Coin change (counting) | any number of times | How many ways to make the amount? | Counting combinations of coins |

Every algorithm is cross-checked against brute force (all subsets, all sign assignments, all multiplicities) on thousands of small instances. All outputs were produced by running the code on CPython 3.9. The recipe — state, transition, base cases, order, answer — is the one from [dp-fundamentals.md](dp-fundamentals.md).

## 🎒 0/1 Knapsack

*Items have weights and values, the pack holds at most `capacity`, and each item may be taken once or not at all. Maximize the total value.*

- **State:** `best[i][w]` = the maximum value achievable using only the first `i` items with capacity `w`.
- **Transition:** consider item `i`. Either **skip** it, giving `best[i − 1][w]`, or **take** it (if its weight fits), giving `value[i] + best[i − 1][w − weight[i]]`. Take the larger.
- **Base cases:** `best[0][w] = 0` (no items, no value), and capacity 0 holds nothing.
- **Order:** items one by one, capacities in any order within a row.
- **Answer:** `best[n][capacity]`.

The table has `(n + 1) × (capacity + 1)` cells, each computed in O(1). To report *which* items were chosen, walk backward from the answer: if `best[i][w]` differs from `best[i − 1][w]`, item `i` was taken, so subtract its weight and continue.

```python
def knapsack_table(weights, values, capacity):
    """Return (best value, indexes of the chosen items, the full table)."""
    n = len(weights)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight, value = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            best[i][w] = best[i - 1][w]                                   # skip item i
            if weight <= w:
                best[i][w] = max(best[i][w], best[i - 1][w - weight] + value)    # take item i
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if best[i][w] != best[i - 1][w]:                                  # the value changed because of item i
            chosen.append(i - 1)
            w -= weights[i - 1]
    return best[n][capacity], sorted(chosen), best

weights, values = [1, 3, 4, 5], [1, 4, 5, 7]
answer, chosen, table = knapsack_table(weights, values, 7)
print(f"best value {answer} from items {chosen} with weights {[weights[i] for i in chosen]} and values {[values[i] for i in chosen]}")
print("capacity:", *range(8))
for i, row in enumerate(table):
    print(f"first {i} items:", *row)
```

```text
best value 9 from items [1, 2] with weights [3, 4] and values [4, 5]
capacity: 0 1 2 3 4 5 6 7
first 0 items: 0 0 0 0 0 0 0 0
first 1 items: 0 1 1 1 1 1 1 1
first 2 items: 0 1 1 4 5 5 5 5
first 3 items: 0 1 1 4 5 6 6 9
first 4 items: 0 1 1 4 5 7 8 9
```

Read the last row: with capacity 7, the best value is 9, from the items of weight 3 and 4. Watching a row evolve is a good way to understand the transition: the entry for capacity 7 jumps from 5 to 9 when the third item (weight 4, value 5) becomes available, because its value 5 plus the best value for the remaining capacity 3 using the first two items (4) beats the 5 available without it.

### Squeezing the Table Into One Row

Row `i` depends only on row `i − 1`, so one row of length `capacity + 1` is enough — **if** the update order does not overwrite values that are still needed. Updating capacities from **high to low** guarantees that `best[w − weight]` still holds the value from *before* this item, so each item is used at most once. Updating from **low to high** would let an item be used again and again — which silently solves the *unbounded* problem instead:

```python
def knapsack_one_row(weights, values, capacity, reuse_items=False):
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        capacities = range(weight, capacity + 1) if reuse_items else range(capacity, weight - 1, -1)
        for w in capacities:
            best[w] = max(best[w], best[w - weight] + value)
    return best[capacity]

print("0/1, capacity high to low:     ", knapsack_one_row([2, 3], [3, 5], 6))
print("capacity low to high (reuse):  ", knapsack_one_row([2, 3], [3, 5], 6, reuse_items=True))
```

```text
0/1, capacity high to low:      8
capacity low to high (reuse):   10
```

With a capacity of 6 and items `(weight 2, value 3)` and `(weight 3, value 5)`, the genuine 0/1 answer is 8 (one of each, weight 5). The low-to-high loop reports 10 by using the weight-3 item twice — a result that is only valid when items can repeat. **The direction of the capacity loop is the whole difference between the two problems.**

## 🎯 Subset Sum: Can We Hit the Target?

*Given a list of positive integers, can some of them add up to exactly `target`?* This is the 0/1 knapsack with every value equal to its weight, and the table holds booleans: `reachable[s]` = "some subset sums to `s`". Starting from `reachable[0] = True`, each number `x` makes `s` reachable whenever `s − x` was already reachable — again iterating `s` from high to low so each number is used once:

```python
def subset_sum(nums, target):
    reachable = [True] + [False] * target
    for x in nums:
        for s in range(target, x - 1, -1):
            if reachable[s - x]:
                reachable[s] = True
    return reachable[target]

print(subset_sum([3, 34, 4, 12, 5, 2], 9), subset_sum([3, 34, 4, 12, 5, 2], 30))      # True False
```

### The Bitset Shortcut

The whole row `reachable` is a set of small integers — exactly what a Python integer can hold as a [bitset](../bit-manipulation/bit-masking.md). Bit `s` is 1 when sum `s` is reachable. Adding a number `x` to every reachable sum is a **left shift by `x`**, and keeping the old sums as well is an OR:

`reachable |= reachable << x`

One big-integer operation updates the entire row, 64 sums at a time or better. Masking to `target + 1` bits just keeps the integer from growing past what we need:

```python
def subset_sum_bitset(nums, target):
    reachable = 1                                              # bit 0 set: the sum 0 is reachable
    keep = (1 << (target + 1)) - 1
    for x in nums:
        reachable |= (reachable << x) & keep                   # every reachable sum s makes s + x reachable
    return bool((reachable >> target) & 1)

print(subset_sum_bitset([3, 34, 4, 12, 5, 2], 9), subset_sum_bitset([3, 34, 4, 12, 5, 2], 30))      # True False
```

Both functions are compared below on 300 random numbers (each from 1 to 500) and a target of 40,000:

```python
import random
import timeit

random.seed(2)
numbers = [random.randint(1, 500) for _ in range(300)]
target = 40_000
assert subset_sum(numbers, target) == subset_sum_bitset(numbers, target)
list_ms = min(timeit.repeat(lambda: subset_sum(numbers, target), number=1, repeat=2)) * 1000
bitset_ms = min(timeit.repeat(lambda: subset_sum_bitset(numbers, target), number=1, repeat=3)) * 1000
print(f"boolean list: {list_ms:9.1f} ms")
print(f"bitset:       {bitset_ms:9.2f} ms   ({list_ms / bitset_ms:,.0f} times faster)")
```

Output:

```
boolean list:     450.0 ms
bitset:            0.24 ms   (1,848 times faster)
```

The recurrence is identical; only the data structure changed — the same trade that [bit-masking.md](../bit-manipulation/bit-masking.md) measured for set operations. The bitset version tells you *whether* a sum is reachable but not *which* numbers make it; to recover the numbers, use the boolean table with parent information as in the 0/1 knapsack above.

## ✂️ Partition Into Two Equal Halves

*Can a list of positive integers be split into two groups with equal sums?* If the total is odd, no. Otherwise one group must sum to exactly `total / 2`, and the other group is then forced to match — so the question is a subset-sum question:

```python
def can_partition(nums):
    total = sum(nums)
    return total % 2 == 0 and subset_sum_bitset(nums, total // 2)

print(can_partition([1, 5, 11, 5]), can_partition([1, 2, 3, 5]))                      # True False
```

The first list (total 22) splits as `{11}` and `{1, 5, 5}`; the second (total 11) has an odd total, so no split can exist.

## ➕➖ Counting: Subsets With a Sum, and Signed Sums

Replacing "reachable (yes/no)" by "number of ways" turns subset sum into a counting problem: `ways[s] += ways[s − x]` instead of OR. That one change counts the subsets of a list that sum to a target.

A famous disguise is **target sum**: *put a `+` or a `−` in front of every number so that the total equals `target`; in how many ways can this be done?* Let `P` be the numbers given a plus sign and `N` those given a minus sign. Then `sum(P) − sum(N) = target` and `sum(P) + sum(N) = total`, so `sum(P) = (total + target) / 2`. The signed-sum question is therefore the question "how many subsets have sum `(total + target) / 2`?" — which must be a whole number, or the answer is 0.

```python
def count_subsets_with_sum(nums, target):
    ways = [1] + [0] * target
    for x in nums:
        for s in range(target, x - 1, -1):
            ways[s] += ways[s - x]
    return ways[target]

def count_signed_sums(nums, target):
    total = sum(nums)
    if abs(target) > total or (total + target) % 2 != 0:
        return 0
    return count_subsets_with_sum(nums, (total + target) // 2)

print(count_subsets_with_sum([1, 2, 3, 4, 5], 5))                  # 3   — {5}, {1, 4}, {2, 3}
print(count_signed_sums([1, 1, 1, 1, 1], 3))                       # 5   — one minus sign among five ones
```

Reducing one problem to another before writing any DP is a skill in itself; here a sign puzzle becomes a table of counts.

## ♾️ Unbounded Knapsack: Items Can Repeat

When items may be used any number of times, the choice at each capacity is "which item do I add **last**?", and the one-row table iterates capacities from **low to high** so that earlier entries may already include the item:

- **State:** `best[w]` = the maximum value with capacity exactly `w` to spend.
- **Transition:** `best[w] = max(best[w − weight] + value)` over all items that fit.

*Rod cutting* is the standard example: a rod of length `n` can be cut into integer pieces, and a piece of length `k` sells for `price[k]`; maximize the revenue.

```python
def unbounded_knapsack(weights, values, capacity):
    best = [0] * (capacity + 1)
    for w in range(1, capacity + 1):
        for weight, value in zip(weights, values):
            if weight <= w:
                best[w] = max(best[w], best[w - weight] + value)
    return best[capacity]

def rod_cutting(prices, length):
    """prices[k - 1] is the price of a piece of length k."""
    return unbounded_knapsack(list(range(1, len(prices) + 1)), prices, length)

prices = [1, 5, 8, 9, 10, 17, 17, 20]
print([rod_cutting(prices, n) for n in range(1, 9)])               # [1, 5, 8, 10, 13, 17, 18, 22]
```

A rod of length 8 earns 22 by cutting it into pieces of 2 and 6 (prices 5 and 17); selling it whole earns only 20.

### Coin Change, Counting: Combinations or Permutations?

*In how many ways can an amount be made from coins (each usable many times)?* The answer depends on a question that the statement must settle: does **order** matter? `1 + 2` and `2 + 1` are the same *combination* of coins but two different *sequences*. The two interpretations differ only in the **order of the two loops**:

```python
def coin_combinations(coins, amount):
    ways = [1] + [0] * amount
    for coin in coins:                                    # coins outermost: each coin is "decided" once, so order cannot matter
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]
    return ways[amount]

def coin_sequences(coins, amount):
    ways = [1] + [0] * amount
    for a in range(1, amount + 1):                        # amounts outermost: any coin may come first, so order matters
        for coin in coins:
            if coin <= a:
                ways[a] += ways[a - coin]
    return ways[amount]

print(coin_combinations([1, 2, 5], 5), coin_sequences([1, 2, 5], 5))                  # 4 9
```

With coins 1, 2, and 5 and an amount of 5, there are 4 combinations (`5`; `2+2+1`; `2+1+1+1`; `1+1+1+1+1`) but 9 ordered sequences, since `2+2+1`, `2+1+2`, and `1+2+2` count separately, as do the four orderings of `2+1+1+1`. Recognizing which of the two a problem asks for, and choosing the loop nesting to match, is a common source of wrong answers.

## ⏱️ Pseudo-Polynomial Time

The 0/1 knapsack table has `n × capacity` cells, so its time is O(n · capacity). That looks polynomial, but `capacity` is a *number*, not the *size* of the input: writing down a capacity of a billion takes only about 30 bits, while the table needs a billion columns. Running time that is polynomial in the **value** of a number but exponential in its **bit length** is called **pseudo-polynomial**. In practice it means the algorithm is great for capacities up to millions and hopeless for astronomically large ones. The general knapsack problem is NP-complete in its decision form, and the pseudo-polynomial dynamic program is the standard way around it when the numbers are modest ([Wikipedia: Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem)). The time grows in direct proportion to the capacity:

```python
random.seed(3)
item_weights = [random.randint(50, 500) for _ in range(100)]
item_values = [random.randint(10, 100) for _ in range(100)]
print(f"{'capacity':>9} | {'time (ms)':>9} | {'best value':>10}")
for capacity in (5_000, 10_000, 20_000, 40_000):
    elapsed = min(timeit.repeat(lambda: knapsack_one_row(item_weights, item_values, capacity), number=1, repeat=2)) * 1000
    print(f"{capacity:>9,} | {elapsed:>9.1f} | {knapsack_one_row(item_weights, item_values, capacity):>10,}")
```

Output:

```
 capacity | time (ms) | best value
    5,000 |      60.1 |      2,142
   10,000 |     120.5 |      3,295
   20,000 |     244.7 |      4,955
   40,000 |     491.7 |      5,706
```

Doubling the capacity doubles the time, as the formula predicts, and a capacity of 10⁹ would take hours in pure Python and gigabytes of memory.

## ✅ Verification

Every function was compared with an exhaustive definition on thousands of small random instances — all subsets for the 0/1 problems, all sign assignments for target sum, all item multiplicities for the unbounded problem, and explicit enumeration for the coin counts:

```python
import itertools
import random

def knapsack_brute(weights, values, capacity):
    best = 0
    for mask in range(1 << len(weights)):
        items = [i for i in range(len(weights)) if mask >> i & 1]
        if sum(weights[i] for i in items) <= capacity:
            best = max(best, sum(values[i] for i in items))
    return best

def unbounded_brute(weights, values, capacity):
    best = 0
    for counts in itertools.product(*(range(capacity // w + 1) for w in weights)):
        if sum(c * w for c, w in zip(counts, weights)) <= capacity:
            best = max(best, sum(c * v for c, v in zip(counts, values)))
    return best

def subset_sum_brute(nums, target):
    return any(sum(c) == target for r in range(len(nums) + 1) for c in itertools.combinations(nums, r))

def signed_sums_brute(nums, target):
    return sum(1 for signs in itertools.product((1, -1), repeat=len(nums)) if sum(s * x for s, x in zip(signs, nums)) == target)

def combinations_brute(coins, amount):
    count = 0
    def choose(i, rest):
        nonlocal count
        if rest == 0:
            count += 1
        elif i < len(coins):
            for uses in range(rest // coins[i] + 1):
                choose(i + 1, rest - uses * coins[i])
    choose(0, amount)
    return count

def sequences_brute(coins, amount):
    return 1 if amount == 0 else sum(sequences_brute(coins, amount - c) for c in coins if c <= amount)

random.seed(1)
for _ in range(1_500):
    n = random.randint(0, 8)
    ws = [random.randint(1, 8) for _ in range(n)]
    vs = [random.randint(0, 20) for _ in range(n)]
    cap = random.randint(0, 20)
    expected = knapsack_brute(ws, vs, cap)
    value, items, _ = knapsack_table(ws, vs, cap)
    assert value == knapsack_one_row(ws, vs, cap) == expected
    assert sum(ws[i] for i in items) <= cap and sum(vs[i] for i in items) == value
    if 0 < n <= 4 and cap <= 12:
        assert unbounded_knapsack(ws, vs, cap) == unbounded_brute(ws, vs, cap)
    nums = [random.randint(0, 9) for _ in range(random.randint(0, 8))]
    goal = random.randint(0, 30)
    positive = [x for x in nums if x > 0]
    assert subset_sum(positive, goal) == subset_sum_bitset(positive, goal) == subset_sum_brute(positive, goal)
    if positive:
        assert can_partition(positive) == any(2 * sum(c) == sum(positive) for r in range(len(positive) + 1) for c in itertools.combinations(positive, r))
    small = [random.randint(0, 6) for _ in range(random.randint(1, 8))]
    signed_goal = random.randint(-15, 15)
    assert count_signed_sums(small, signed_goal) == signed_sums_brute(small, signed_goal)
    coins = sorted(random.sample(range(1, 7), random.randint(1, 3)))
    amount = random.randint(0, 14)
    assert coin_combinations(coins, amount) == combinations_brute(coins, amount)
    assert coin_sequences(coins, amount) == sequences_brute(coins, amount)
print("knapsack, subset sum, partition, signed sums, unbounded knapsack and both coin counts agree with exhaustive search on 1,500 rounds")
```

```text
knapsack, subset sum, partition, signed sums, unbounded knapsack and both coin counts agree with exhaustive search on 1,500 rounds
```

## Common Mistakes

- **Iterating capacities in the wrong direction** in the one-row 0/1 table. High to low is 0/1; low to high lets items repeat.
- **Confusing combinations with permutations** in counting problems; the loop nesting decides which one you compute.
- **Forgetting zeros in counting problems.** A zero can be included or left out without changing a sum, so each zero doubles the count. The loop `for s in range(target, x - 1, -1)` handles `x = 0` correctly (every entry is doubled); code that skips zeros would not.
- **Using a bitset to recover the chosen items.** It answers "reachable?" only; keep parent information in the boolean table when the actual numbers are needed.
- **Treating the pseudo-polynomial bound as polynomial.** Time proportional to the capacity's *value* becomes impractical for huge capacities.
- **Hand-rolling the reduction wrongly.** In the signed-sum problem, check that `(total + target)` is even and `|target| ≤ total` before indexing the table.

## ➡️ Next

Continue to [string-dp.md](string-dp.md): the two dimensions of the table become *positions in two strings*, and the same recipe finds the longest common subsequence, the edit distance, and the longest palindromic subsequence and substring.
