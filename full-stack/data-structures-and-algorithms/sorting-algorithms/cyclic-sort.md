# 🔄 Cyclic Sort

## When the Value Is Its Own Address

Every comparison sort in this module has to make at least `⌈log₂ n!⌉` comparisons (see [sorting-fundamentals.md](sorting-fundamentals.md)). Cyclic sort sidesteps that limit by never comparing two items with each other. It uses a different kind of information: **if the values are exactly the integers `1` to `n`, each value tells you where it belongs.** The number 7 goes at index 6; no comparison is needed to know that. So the algorithm is simply: look at the value in the current slot, send it to its home slot, and repeat.

The result sorts in **O(n) time with O(1) extra space**, and the same idea solves a whole family of "which number is missing or duplicated?" problems that appear again and again in coding interviews.

> **A note on names.** *Cycle sort* in Wikipedia is a different algorithm: a general comparison sort that takes Θ(n²) time but is optimal in the number of writes ([Wikipedia: Cycle sort](https://en.wikipedia.org/wiki/Cycle_sort)). The technique in this file is often called "cyclic sort" in interview-preparation material. It does not compare items; it needs the values to be small integers in a known range.

All outputs below were produced by running the code on CPython 3.9.

## 🧱 The Algorithm

Walk through the list with an index `i`. Let `v = nums[i]`; the home of `v` is index `v − 1`.

- If `v` is already at its home (`i == v − 1`), move on to the next index.
- Otherwise swap `nums[i]` with `nums[v − 1]`. Now `v` is at home, and a **new** value has arrived at index `i`. **Do not move on:** look at index `i` again.

```python
def cyclic_sort(nums):
    """Sort a permutation of 1..n in place: O(n) time, O(1) extra space. Returns nums."""
    i = 0
    while i < len(nums):
        home = nums[i] - 1                                   # the index where the value nums[i] belongs
        if home != i:
            nums[i], nums[home] = nums[home], nums[i]        # send the value home; a new value arrives at index i
        else:
            i += 1                                           # nums[i] is in place: move on
    return nums

def trace_cyclic_sort(values):
    nums = list(values)
    lines = [f"start            {nums}"]
    i = 0
    while i < len(nums):
        home = nums[i] - 1
        if home != i:
            nums[i], nums[home] = nums[home], nums[i]
            lines.append(f"swap {i} <-> {home}      {nums}")
        else:
            i += 1
    return "\n".join(lines)

print(trace_cyclic_sort([3, 1, 5, 4, 2]))
print(cyclic_sort([3, 1, 5, 4, 2]))
```

```text
start            [3, 1, 5, 4, 2]
swap 0 <-> 2      [5, 1, 3, 4, 2]
swap 0 <-> 4      [2, 1, 3, 4, 5]
swap 0 <-> 1      [1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
```

Follow the trace. Index 0 holds `3`, whose home is index 2, so the two are swapped; index 0 now holds `5`, whose home is index 4; then it holds `2`, whose home is index 1; then it holds `1`, which is already home, so `i` finally advances. Three swaps sorted five items — and no two items were ever compared.

## ⏱️ Why It Is O(n)

The loop has two kinds of steps: a swap, and an advance of `i`.

- **Every swap puts a value into its final position, permanently.** The value moved to `home` stays there: a later swap exchanges the value at index `i` with whatever sits in *that value's* home slot, and a value that is already home is never found there, because all the values are different. So there are at most `n − 1` swaps.
- **`i` advances at most `n` times.**

Together: at most `2n − 1` loop iterations, so the running time is O(n), and only a few variables are used, so the extra space is O(1).

### The Exact Swap Count: Permutation Cycles

Follow the path `index → value − 1 → …` for `[3, 1, 5, 4, 2]`: index 0 holds 3, which belongs at index 2; index 2 holds 5, which belongs at index 4; index 4 holds 2, which belongs at index 1; index 1 holds 1, which belongs at index 0 — back where we started. That loop through four slots is a **cycle**. Index 3 holds `4`, which is already home, so it is a cycle of length one. Every permutation breaks into such cycles, and putting a cycle of length `L` in order takes exactly `L − 1` swaps. So

> **swaps = n − (number of cycles)**

Each swap of two positions changes the number of cycles by exactly one, so no algorithm that sorts by swapping can use fewer swaps. The next block checks the formula and the `2n − 1` bound on every permutation of up to six items, using a breadth-first search over all possible swap sequences as the independent referee, and then measures random permutations:

```python
import itertools
import math
import random
from collections import deque

def count_cycles(perm):
    """Number of cycles of a permutation of 1..n (index i leads to index perm[i] - 1)."""
    seen = [False] * len(perm)
    cycles = 0
    for start in range(len(perm)):
        if not seen[start]:
            cycles += 1
            j = start
            while not seen[j]:
                seen[j] = True
                j = perm[j] - 1
    return cycles

def cyclic_sort_counted(values):
    """Return (swaps, loop iterations) used by cyclic_sort on a permutation of 1..n."""
    nums = list(values)
    swaps = iterations = i = 0
    while i < len(nums):
        iterations += 1
        home = nums[i] - 1
        if home != i:
            nums[i], nums[home] = nums[home], nums[i]
            swaps += 1
        else:
            i += 1
    return swaps, iterations

print(count_cycles([3, 1, 5, 4, 2]), cyclic_sort_counted([3, 1, 5, 4, 2]))     # 2 (3, 8)

def minimum_swaps(start):
    """Fewest swaps of any two positions that sort `start`, found by breadth-first search over all arrangements."""
    target = tuple(sorted(start))
    seen = {tuple(start)}
    queue = deque([(tuple(start), 0)])
    while queue:
        arrangement, distance = queue.popleft()
        if arrangement == target:
            return distance
        for a, b in itertools.combinations(range(len(arrangement)), 2):
            neighbour = list(arrangement)
            neighbour[a], neighbour[b] = neighbour[b], neighbour[a]
            neighbour = tuple(neighbour)
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append((neighbour, distance + 1))

for n in range(1, 7):
    worst = 0
    for perm in itertools.permutations(range(1, n + 1)):
        swaps, iterations = cyclic_sort_counted(perm)
        assert swaps == n - count_cycles(perm) == minimum_swaps(perm)
        assert iterations <= 2 * n - 1
        worst = max(worst, swaps)
    print(f"n = {n}: all {math.factorial(n):>3} permutations sorted with the minimum possible number of swaps; the worst case is {worst}")

random.seed(1)
for n in (10, 100, 1_000):
    runs = 2_000
    average = sum(cyclic_sort_counted(random.sample(range(1, n + 1), n))[0] for _ in range(runs)) / runs
    harmonic = sum(1 / k for k in range(1, n + 1))
    print(f"n = {n:>5}: average swaps on random permutations {average:7.2f}    n - H(n) = {n - harmonic:7.2f}")
```

```text
2 (3, 8)
n = 1: all   1 permutations sorted with the minimum possible number of swaps; the worst case is 0
n = 2: all   2 permutations sorted with the minimum possible number of swaps; the worst case is 1
n = 3: all   6 permutations sorted with the minimum possible number of swaps; the worst case is 2
n = 4: all  24 permutations sorted with the minimum possible number of swaps; the worst case is 3
n = 5: all 120 permutations sorted with the minimum possible number of swaps; the worst case is 4
n = 6: all 720 permutations sorted with the minimum possible number of swaps; the worst case is 5
n =    10: average swaps on random permutations    7.04    n - H(n) =    7.07
n =   100: average swaps on random permutations   94.78    n - H(n) =   94.81
n =  1000: average swaps on random permutations  992.48    n - H(n) =  992.51
```

For every permutation of up to six items, the swap count equals `n − cycles` and equals the true minimum found by exhaustive search; the worst case, a single cycle through all items, needs `n − 1` swaps. For random permutations, the average number of cycles is the harmonic number `Hₙ` (about `ln n + 0.58`; see [Wikipedia: Random permutation statistics](https://en.wikipedia.org/wiki/Random_permutation_statistics)), so the average number of swaps is `n − Hₙ` — the measurements match.

## 🔁 Other Ranges, Duplicates, and Out-of-Range Values

The same idea adapts to other inputs:

- **Values `0` to `n − 1`:** the value *is* the index, so `home = nums[i]`.
- **Values `lo` to `lo + n − 1`:** `home = nums[i] − lo`.
- **Lists that need not be a permutation** — duplicates, missing values, zero, negatives, huge numbers: send a value home **only if** its home slot exists and does not already hold that same value. Everything else simply stays in a leftover slot.

```python
def place_in_homes(nums):
    """Move each value v with 1 <= v <= len(nums) to index v - 1, in place, in O(n) time.

    Duplicates and out-of-range values end up in the leftover slots."""
    i = 0
    while i < len(nums):
        home = nums[i] - 1
        if 0 <= home < len(nums) and nums[home] != nums[i]:       # the home slot exists and does not already hold this value
            nums[i], nums[home] = nums[home], nums[i]
        else:
            i += 1

example = [4, 3, 2, 7, 8, 2, 3, 1]
place_in_homes(example)
print(example)
print("slots holding the wrong value:", [i for i, v in enumerate(example) if v != i + 1])
```

```text
[1, 2, 3, 4, 3, 2, 7, 8]
slots holding the wrong value: [4, 5]
```

This loop still ends quickly, for the same reason as before: each swap fixes a value in a slot that did not hold it, and a slot that holds its own value is never disturbed (the check `nums[home] != nums[i]` refuses to swap two equal values — without it, two copies of the same number would be swapped with each other forever). So there are at most `n` swaps.

After the pass, one fact drives every application below:

> **Slot `i` holds a value other than `i + 1` exactly when the number `i + 1` does not occur in the input.**

If `i + 1` occurred, it would have been sent to slot `i` and left there. Conversely, if slot `i` holds `i + 1`, then `i + 1` was present. In the example above, slots 4 and 5 are wrong, so the numbers `5` and `6` are missing; and the values sitting in the wrong slots (`3` and `2`) are the **extra copies** of duplicated numbers.

## 🔎 The Missing-and-Duplicate Family

All six functions below copy their input first (`nums = list(nums)`), so the caller's list is untouched; that copy costs O(n) space. Remove it if you may rearrange the caller's list, and the extra space becomes O(1).

### 1. Missing Number (values `0` to `n`, one absent)

A list of `n` distinct numbers is taken from `0..n`, so exactly one number of that range is absent. Use the 0-based version of the placement (`home = value`); the value `n` has no slot, so it stays wherever it lands. The first slot that does not hold its own index names the missing number — or it is `n` if every slot is right.

```python
def missing_number(nums):
    """nums holds n distinct values from 0..n, so exactly one value of that range is absent."""
    nums = list(nums)
    n = len(nums)
    i = 0
    while i < n:
        home = nums[i]                                    # 0-based: the value is its own index
        if home < n and nums[home] != nums[i]:            # the value n has no slot, so it is left where it is
            nums[i], nums[home] = nums[home], nums[i]
        else:
            i += 1
    for i in range(n):
        if nums[i] != i:                                  # the first slot that does not hold its own index
            return i
    return n

print(missing_number([3, 0, 1]))                          # 2
print(missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]))        # 8
print(missing_number([0, 1]))                             # 2
```

### 2. All Numbers Missing From `1..n`

A list of `n` values, each in `1..n`, may contain duplicates; report every number of `1..n` that is absent. By the key fact, those are the numbers `i + 1` for the wrong slots `i`.

```python
def find_disappeared(nums):
    nums = list(nums)
    place_in_homes(nums)
    return [i + 1 for i, v in enumerate(nums) if v != i + 1]

print(find_disappeared([4, 3, 2, 7, 8, 2, 3, 1]))         # [5, 6]
print(find_disappeared([1, 1]))                           # [2]
```

### 3. All Duplicates

In a list of `n` values from `1..n` where each value occurs once or twice, the values in the wrong slots are exactly the second copies:

```python
def find_duplicates(nums):
    """Return the values that occur twice (in slot order, not necessarily sorted)."""
    nums = list(nums)
    place_in_homes(nums)
    return [v for i, v in enumerate(nums) if v != i + 1]

print(sorted(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1])))  # [2, 3]
```

### 4. The One Repeated Number

A list of `n + 1` values from `1..n` must repeat at least one value (pigeonhole principle); in this version exactly one value repeats, possibly more than twice. Placing values until a swap would collide with an equal value reveals it:

```python
def find_duplicate(nums):
    nums = list(nums)
    i = 0
    while i < len(nums):
        if nums[i] != i + 1:
            home = nums[i] - 1
            if nums[home] == nums[i]:
                return nums[i]                            # the home slot already holds this value: it is the repeated number
            nums[i], nums[home] = nums[home], nums[i]
        else:
            i += 1

print(find_duplicate([1, 3, 4, 2, 2]))                    # 2
print(find_duplicate([3, 1, 3, 4, 2]))                    # 3
```

If the list must not be modified at all, treat `i → nums[i]` as a linked list: because two indexes point to the repeated value, it is where a **cycle begins**, and Floyd's tortoise-and-hare method finds a cycle's entrance with O(1) space and no writes (the technique is explained in [common-linked-list-problems.md](../linked-lists/common-linked-list-problems.md)):

```python
def find_duplicate_read_only(nums):
    slow = fast = 0
    while True:                                           # phase 1: the pointers meet somewhere inside the cycle
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0
    while slow != fast:                                   # phase 2: moving one step at a time, they meet at the cycle's entrance
        slow = nums[slow]
        fast = nums[fast]
    return slow

print(find_duplicate_read_only([1, 3, 4, 2, 2]))          # 2
print(find_duplicate_read_only([3, 1, 3, 4, 2]))          # 3
```

### 5. The Corrupted Pair

A list was a permutation of `1..n`, but one number was overwritten with a copy of another. Report `[the number that now appears twice, the number that vanished]`. After placement there is exactly one wrong slot: it holds the duplicate, and its index plus one is the missing number.

```python
def find_error_pair(nums):
    nums = list(nums)
    place_in_homes(nums)
    for i, v in enumerate(nums):
        if v != i + 1:
            return [v, i + 1]

print(find_error_pair([1, 2, 2, 4]))                      # [2, 3]
print(find_error_pair([1, 1]))                            # [1, 2]
```

### 6. The Smallest Missing Positive Integer

Given any integers — negative, zero, repeated, enormous — find the smallest positive integer that is absent, in O(n) time and O(1) extra space. The answer can never exceed `n + 1`, so only the values `1..n` matter; place those and ignore the rest. The first wrong slot gives the answer, and if there is none, the answer is `n + 1`. This is a famously hard question for anyone who has not seen the idea:

```python
def first_missing_positive(nums):
    nums = list(nums)
    place_in_homes(nums)
    for i, v in enumerate(nums):
        if v != i + 1:
            return i + 1
    return len(nums) + 1

print(first_missing_positive([3, 4, -1, 1]))              # 2
print(first_missing_positive([1, 2, 0]))                  # 3
print(first_missing_positive([7, 8, 9, 11, 12]))          # 1
```

### Verification

Each function was compared with a brute-force definition (sets and counters) on thousands of random inputs, covering every case the functions claim to handle:

```python
from collections import Counter

def random_once_or_twice(n):
    """n values from 1..n in which every value occurs once or twice."""
    d = random.randint(0, n // 2)
    chosen = random.sample(range(1, n + 1), 2 * d)
    copied, removed = chosen[:d], chosen[d:]
    replacement = dict(zip(removed, copied))                # each removed value is replaced by a copy of a kept one
    values = [replacement.get(v, v) for v in range(1, n + 1)]
    random.shuffle(values)
    return values

random.seed(3)
cases = 5_000
for _ in range(cases):
    n = random.randint(2, 12)

    absent = random.randint(0, n)
    values = [v for v in range(n + 1) if v != absent]
    random.shuffle(values)
    assert missing_number(values) == absent

    values = [random.randint(1, n) for _ in range(n)]
    assert find_disappeared(values) == sorted(set(range(1, n + 1)) - set(values))

    values = random_once_or_twice(n)
    assert sorted(find_duplicates(values)) == sorted(v for v, c in Counter(values).items() if c == 2)

    repeated = random.randint(1, n)
    copies = random.randint(2, n + 1)
    others = random.sample([v for v in range(1, n + 1) if v != repeated], n + 1 - copies)
    values = [repeated] * copies + others
    random.shuffle(values)
    snapshot = list(values)
    assert find_duplicate(values) == find_duplicate_read_only(values) == repeated
    assert values == snapshot                               # neither version changed the caller's list

    perm = random.sample(range(1, n + 1), n)
    p, q = random.sample(range(n), 2)
    lost = perm[p]
    perm[p] = perm[q]                                       # overwrite one number with a copy of another
    assert find_error_pair(perm) == [perm[q], lost]

    values = [random.randint(-5, n + 5) for _ in range(random.randint(0, 12))]
    present = set(values)
    assert first_missing_positive(values) == next(k for k in itertools.count(1) if k not in present)
print(f"all six functions agree with brute force on {cases:,} random cases")
```

```text
all six functions agree with brute force on 5,000 random cases
```

## 🪤 The Range Check Is Not Optional

`place_in_homes` tests `0 <= home < len(nums)` before touching the list. Leave it out and Python's indexing rules bite: an index that is too large raises `IndexError`, but a **negative** index silently counts from the end of the list instead of failing. The value `-1` has `home = -2`, which in a two-item list is slot 0 — the home of the value `1`. The two values then trade places forever:

```python
def first_missing_positive_without_range_check(nums, max_steps=1_000):
    """The same algorithm minus the range check; returns None if it has not finished after max_steps steps."""
    nums = list(nums)
    i = steps = 0
    while i < len(nums):
        steps += 1
        if steps > max_steps:
            return None
        home = nums[i] - 1
        if nums[home] != nums[i]:                           # BUG: home may be negative or past the end
            nums[i], nums[home] = nums[home], nums[i]
        else:
            i += 1
    for i, v in enumerate(nums):
        if v != i + 1:
            return i + 1
    return len(nums) + 1

for case in ([-1, 1], [2]):
    try:
        print(case, "->", first_missing_positive_without_range_check(case))
    except IndexError as error:
        print(case, "-> IndexError:", error)

outcomes = Counter()
for size in range(1, 5):
    for case in itertools.product(range(-2, size + 2), repeat=size):      # every list of 1 to 4 values from -2 to size + 1
        expected = next(k for k in itertools.count(1) if k not in case)
        assert first_missing_positive(case) == expected                    # the version with the range check is always right
        try:
            answer = first_missing_positive_without_range_check(case)
        except IndexError:
            outcomes["IndexError"] += 1
        else:
            outcomes["never finished" if answer is None else "right answer" if answer == expected else "wrong answer"] += 1
print(dict(outcomes))
```

```text
[-1, 1] -> None
[2] -> IndexError: list index out of range
{'IndexError': 1683, 'right answer': 1311, 'never finished': 1486}
```

(`None` means the loop was still running after a thousand steps; on lists this small that can only mean it would never stop.) Of the 4,480 lists tested, the version without the range check crashed on 1,683, hung on 1,486, and was right on only 1,311 — while the version with the check, asserted inside the loop, was right on every one.

## ⚖️ Choosing an Approach

For the single-missing-number problem there are many solutions. Each of these functions was run on a shuffled list of 100,000 numbers with one absent:

```python
import timeit
from functools import reduce
from operator import xor

def missing_by_sum(nums):                                   # n(n+1)/2 minus the actual sum
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)

def missing_by_xor(nums):                                   # x ^ x == 0, so every present value cancels
    result = len(nums)
    for i, v in enumerate(nums):
        result ^= i ^ v
    return result

def missing_by_set(nums):
    return (set(range(len(nums) + 1)) - set(nums)).pop()

def missing_by_sorting(nums):
    for i, v in enumerate(sorted(nums)):
        if v != i:
            return i
    return len(nums)

random.seed(4)
n = 100_000
absent = random.randint(0, n)
values = [v for v in range(n + 1) if v != absent]
random.shuffle(values)

approaches = [("sum formula", missing_by_sum), ("XOR loop", missing_by_xor), ("set difference", missing_by_set),
              ("sort and scan", missing_by_sorting), ("cyclic placement", missing_number)]
print(f"{'approach':>16} | {'time (ms)':>9} | correct")
for name, function in approaches:
    milliseconds = min(timeit.repeat(lambda: function(values), number=1, repeat=5)) * 1000
    print(f"{name:>16} | {milliseconds:9.2f} | {function(values) == absent}")
```

Output:

```
        approach | time (ms) | correct
     sum formula |      0.36 | True
        XOR loop |      4.83 | True
  set difference |      3.18 | True
   sort and scan |      9.99 | True
cyclic placement |     17.70 | True
```

| Approach | Time | Extra space | Changes the input | Handles several missing and duplicated values |
|----------|------|-------------|-------------------|-----------------------------------------------|
| Sum formula or XOR | O(n) | O(1) | No | **No** — one unknown only |
| Set or counter | O(n) | O(n) | No | Yes |
| Sort, then scan | O(n log n) | O(1) to O(n) | Yes, unless it sorts a copy | Yes |
| Cyclic placement | O(n) | O(1) if the input may be rearranged | Yes (or O(n) for a copy) | Yes |

In Python, the built-ins implemented in C (`sum`, `set`) beat a hand-written loop by a wide margin at this size, so cyclic placement is not a speed-up in practice. Its value is **generality with O(1) extra space**: the sum and XOR tricks answer only the one-missing-number question, while placement also finds duplicates, several missing values, and the first missing positive. It is also the answer interviewers usually have in mind when they say "in O(n) time and constant space".

The same trade-off appears for sorting itself: a hand-written cyclic sort on a permutation of 1 to `n` is O(n), yet Python's built-in `sorted` is still faster for the sizes you are likely to use:

```python
for n in (10_000, 100_000, 1_000_000):
    perm = random.sample(range(1, n + 1), n)
    cyclic_ms = min(timeit.repeat(lambda: cyclic_sort(list(perm)), number=1, repeat=3)) * 1000
    builtin_ms = min(timeit.repeat(lambda: sorted(perm), number=1, repeat=3)) * 1000
    print(f"n = {n:>9,}: cyclic sort {cyclic_ms:8.1f} ms    sorted() {builtin_ms:8.1f} ms")
```

Output:

```
n =    10,000: cyclic sort      1.9 ms    sorted()      0.6 ms
n =   100,000: cyclic sort     19.5 ms    sorted()      9.2 ms
n = 1,000,000: cyclic sort    287.6 ms    sorted()    166.8 ms
```

The gap narrows as `n` grows, which is what `n log n` against `n` growth predicts, but even at a million items the C-implemented Timsort is still ahead. Cyclic sort is an *algorithmic technique* for constrained problems, not a replacement for the built-in sort.

## Common Mistakes

- **Moving to the next index after a swap.** The value that just arrived at index `i` has not been examined; advance only when `nums[i]` is home.
- **Off-by-one in the home index.** Values `1..n` live at `value − 1`; values `0..n−1` live at `value`. Mixing the two silently misplaces everything.
- **Forgetting the equality check with duplicates.** Swapping `nums[i]` with an equal value in its home slot changes nothing, so the loop never ends.
- **Forgetting the range check.** Out-of-range values need to be skipped, and negative values are especially dangerous in Python because negative indexes wrap around.
- **Using it where the values are not a small known range.** Strings, floats, and large or sparse integers have no direct index; use a comparison sort, [counting sort or radix sort](choosing-a-sorting-algorithm.md), or a hash table instead.
- **Forgetting that it rearranges the input.** If the caller's list must survive, work on a copy (O(n) space) or use a read-only method such as Floyd's.

## ➡️ Next

Continue to [choosing-a-sorting-algorithm.md](choosing-a-sorting-algorithm.md), the last file in this module: it compares every algorithm so far, adds counting sort and radix sort (two more sorts that escape the `n log n` limit by using values as positions), and ends with a decision guide.
