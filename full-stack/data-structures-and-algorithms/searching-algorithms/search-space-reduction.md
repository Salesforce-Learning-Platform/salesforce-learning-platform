# ✂️ Search Space Reduction

## The Real Idea Behind Binary Search

[Binary search](binary-search.md) works because one cheap comparison lets you **throw away half of the candidates for certain**. That is a much more general idea than "find a number in a sorted list". Whenever you can find a test that proves a large *region* of candidates cannot contain the answer, you can keep discarding regions until the answer is the only candidate left, and the work drops from "look at everything" to a handful of steps.

Three questions turn the idea into a method:

1. **What are the candidates?** (indexes, pairs of indexes, cells of a grid, numbers in a range)
2. **What can one cheap test tell me about a whole region of them?**
3. **Why is it safe to discard that region?** (If you cannot give a one-sentence proof, you do not have an algorithm yet.)

This file applies the method to six problems. Every algorithm is cross-checked against a brute-force definition on thousands of cases, because search-space reduction is exactly where off-by-one errors and unproven assumptions hide. All outputs were produced by running the code on CPython 3.9.

| Problem | Candidates | What one test eliminates | Time |
|---------|------------|--------------------------|------|
| Rotated sorted array | Indexes | The half that cannot hold the target | O(log n) |
| Peak finding | Indexes | The side that is falling away from the probe | O(log n) |
| Sorted matrix | Cells | A whole row or column per step | O(log mn) or O(m + n) |
| Pair with a given sum | Pairs of indexes | One endpoint, with all its pairs | O(n) instead of O(n²) |
| Unbounded sorted list | Indexes in an unknown range | Everything beyond the first big probe | O(log i) |
| Evenly spread keys | Indexes | Everything on the wrong side of an estimate | O(log log n) on average, O(n) worst |

## 🔄 Rotated Sorted Arrays

Take a sorted list and **rotate** it: cut it somewhere and move the front part to the back. `[3, 8, 14, 21, 27, 33, 40]` rotated by four positions becomes `[27, 33, 40, 3, 8, 14, 21]`. The list is no longer sorted, so ordinary binary search fails — but it is still *almost* sorted, and that is enough.

**Finding the minimum.** Compare the middle item with the **last** item. If `nums[mid] > nums[high]`, the "drop" (where the rotation happened) must be to the right of `mid`, so the minimum is in `mid + 1..high`. Otherwise the right part is in order, and the minimum is at `mid` or to its left.

**Searching for a target.** At least one half of `low..high` is always in sorted order, and a comparison tells you which one: if `nums[low] <= nums[mid]`, the left half is sorted. In the sorted half you can say for certain whether the target lies in it (by checking the endpoints), and discard one half or the other accordingly.

```python
def find_minimum_rotated(nums):
    """Index of the smallest item in a rotated sorted list of distinct values."""
    low, high = 0, len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if nums[mid] > nums[high]:
            low = mid + 1                                  # the drop is to the right of mid, so the minimum is too
        else:
            high = mid                                     # mid itself might be the minimum
    return low

def search_rotated(nums, target):
    """Index of target in a rotated sorted list of distinct values, or -1."""
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[low] <= nums[mid]:                         # the left half low..mid is sorted
            if nums[low] <= target < nums[mid]:
                high = mid - 1                             # the target is in the sorted left half
            else:
                low = mid + 1
        else:                                              # the right half mid..high is sorted
            if nums[mid] < target <= nums[high]:
                low = mid + 1                              # the target is in the sorted right half
            else:
                high = mid - 1
    return -1

rotated = [27, 33, 40, 3, 8, 14, 21]
print(find_minimum_rotated(rotated), search_rotated(rotated, 8), search_rotated(rotated, 33), search_rotated(rotated, 9))       # 3 4 1 -1
```

The two functions were checked on **every rotation** of sorted lists of 1 to 12 distinct values, with every target from below the smallest item to above the largest:

```python
checked = 0
for size in range(1, 13):
    base = [3 * i for i in range(size)]
    for shift in range(size):
        nums = base[shift:] + base[:shift]
        assert find_minimum_rotated(nums) == (size - shift) % size
        for target in range(-1, 3 * size + 1):
            assert search_rotated(nums, target) == (nums.index(target) if target in nums else -1)
            checked += 1
print(f"{checked:,} searches over every rotation of lists of 1 to 12 items: all correct")
```

```text
2,106 searches over every rotation of lists of 1 to 12 items: all correct
```

### When Duplicates Appear

The proof above quietly relied on distinct values. With duplicates, `nums[low] <= nums[mid]` no longer proves that the left half is sorted: in `[1, 0, 1, 1, 1]` the items at `low`, `mid`, and `high` are all `1`, and the minimum could be on either side. The distinct-values algorithm then discards the wrong half. The repair is to **shrink the range by one at each end** when the three items are equal, which keeps the search correct at the cost of an O(n) worst case:

```python
import itertools

def search_rotated_with_duplicates(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[low] == nums[mid] == nums[high]:           # cannot tell which half is sorted: shrink both ends
            low += 1
            high -= 1
        elif nums[low] <= nums[mid]:
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1

def count_failures(search):
    """Try every rotation of every sorted list of up to 7 values drawn from {0, 1, 2}, and every target."""
    failures, total = 0, 0
    for size in range(1, 8):
        for base in itertools.combinations_with_replacement(range(3), size):
            for shift in range(size):
                nums = list(base[shift:] + base[:shift])
                for target in range(3):
                    answer = search(nums, target)
                    found = answer != -1 and nums[answer] == target
                    failures += found != (target in nums)
                    total += 1
    return failures, total

print(search_rotated([1, 0, 1, 1, 1], 0), search_rotated_with_duplicates([1, 0, 1, 1, 1], 0))      # -1 1
print("distinct-values version on lists with duplicates:", count_failures(search_rotated))
print("version that shrinks both ends:                  ", count_failures(search_rotated_with_duplicates))
```

```text
-1 1
distinct-values version on lists with duplicates: (36, 1890)
version that shrinks both ends:                   (0, 1890)
```

The first version gets the 0 in `[1, 0, 1, 1, 1]` wrong — it reports `-1` although the 0 is at index 1 — and fails on 36 of the 1,890 small cases tried; the second version gets none wrong. The price is the O(n) worst case: while the three probed items are equal, only the two ends can be discarded, so a long run of equal values makes the range shrink by two per step instead of halving. Whenever you design a halving rule, ask "what input makes my test inconclusive?"

## ⛰️ Finding a Peak in Unsorted Data

Binary search does **not** require sorted data; it requires a test that tells you which side to keep. Here is an example with no ordering at all. In a list where neighbouring items differ, a **peak** is an item greater than both its neighbours (the ends count as having a neighbour of minus infinity, so a list always has at least one peak). Find any peak in O(log n).

Probe the middle and compare it with its right neighbour. If `nums[mid] < nums[mid + 1]`, the list is **rising** at `mid`: either it keeps rising to the end (and the last item is a peak) or it turns downward somewhere to the right (and the turning point is a peak) — so a peak exists in `mid + 1..high`. Otherwise the list is falling at `mid`, and by the mirror argument a peak exists in `low..mid`.

```python
import random

def find_peak(nums):
    """Index of a peak (an item greater than its neighbours). Adjacent items must be different."""
    low, high = 0, len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if nums[mid] < nums[mid + 1]:
            low = mid + 1                                  # rising: a peak lies to the right
        else:
            high = mid                                     # falling: a peak lies at mid or to the left
    return low

profile = [2, 6, 5, 9, 3, 4, 1]
print(find_peak(profile), profile[find_peak(profile)])     # 1 6

random.seed(1)
for _ in range(5_000):
    nums = [random.randint(0, 20) for _ in range(random.randint(1, 15))]
    nums = [v for i, v in enumerate(nums) if i == 0 or v != nums[i - 1]]                 # no equal neighbours
    p = find_peak(nums)
    assert (p == 0 or nums[p - 1] < nums[p]) and (p == len(nums) - 1 or nums[p + 1] < nums[p])
print("find_peak returned a genuine peak on 5,000 random lists")
```

```text
1 6
find_peak returned a genuine peak on 5,000 random lists
```

(This list has peaks at indexes 1, 3, and 5; the search found the one at index 1. It guarantees only that it finds *a* peak, not the highest one.)

## 🧮 Searching a Sorted Matrix

Two common ways a matrix can be sorted give two different reductions.

**Rows sorted, and each row starts after the previous one ends.** Then reading the matrix row by row gives one long sorted list. Binary-search the *flattened* index `0..rows·cols − 1`, and convert each index back with `row = index // cols`, `col = index % cols`: O(log(rows·cols)).

**Rows sorted left to right and columns sorted top to bottom — but no relationship between rows.** Binary search over a single index does not apply, but a clever starting point does: begin in the **top-right corner**. If that value is larger than the target, the whole column below it (all at least as large) is eliminated, so move left. If it is smaller, the whole row to its left (all at most as small) is eliminated, so move down. Each step removes a full row or column, so at most `rows + cols − 1` cells are visited:

```python
def search_matrix_flattened(matrix, target):
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    low, high = 0, rows * cols - 1
    while low <= high:
        mid = (low + high) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return False

def search_matrix_staircase(matrix, target):
    if not matrix or not matrix[0]:
        return False
    row, col = 0, len(matrix[0]) - 1                       # start at the top-right corner
    while row < len(matrix) and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value > target:
            col -= 1                                       # everything below in this column is >= value: discard the column
        else:
            row += 1                                       # everything to the left in this row is <= value: discard the row
    return False

fully_sorted = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
partly_sorted = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
print(search_matrix_flattened(fully_sorted, 16), search_matrix_flattened(fully_sorted, 13))           # True False
print(search_matrix_staircase(partly_sorted, 5), search_matrix_staircase(partly_sorted, 15))          # True False

random.seed(2)
for _ in range(3_000):
    rows, cols = random.randint(1, 6), random.randint(1, 6)
    flat = sorted(random.sample(range(100), rows * cols))
    matrix = [flat[r * cols:(r + 1) * cols] for r in range(rows)]
    for target in range(-1, 101, 3):
        assert search_matrix_flattened(matrix, target) == (target in flat)
    row_part, col_part = sorted(random.sample(range(50), rows)), sorted(random.sample(range(50), cols))
    grid = [[3 * a + b for b in col_part] for a in row_part]                              # rows and columns both ascending
    present = {v for row in grid for v in row}
    for target in range(0, 200, 7):
        assert search_matrix_staircase(grid, target) == (target in present)
print("both matrix searches agree with a membership test on 3,000 random matrices")
```

```text
True False
True False
both matrix searches agree with a membership test on 3,000 random matrices
```

The weaker the sortedness, the weaker the speed-up: the fully sorted matrix needs about `log₂(m·n)` probes, the staircase needs up to `m + n`. For a 1,000 × 1,000 matrix that is roughly 20 versus up to 1,999 — still vastly better than the million cells of a scan.

## 👉👈 Two Pointers on a Sorted List

Find two items of a sorted list that add up to a target. The brute-force way tries every pair: O(n²). Binary-searching for each item's partner gives O(n log n). The reduction below does it in **O(n)** by eliminating a candidate — together with all of its pairs — at each step.

Put a pointer `i` at the smallest item and `j` at the largest. If `nums[i] + nums[j]` is too small, then `nums[i]` cannot pair with *any* item at `j` or to its left either (they are all at most `nums[j]`), so `nums[i]` is eliminated for good: `i += 1`. If the sum is too large, then `nums[j]` cannot pair with anything at `i` or to its right (they are all at least `nums[i]`): `j -= 1`. Each step removes one item, so there are at most `n − 1` steps.

```python
def pair_with_sum(nums, target):
    """Indexes (i, j), i < j, of two items of the sorted list nums that add up to target, or None."""
    i, j = 0, len(nums) - 1
    while i < j:
        total = nums[i] + nums[j]
        if total == target:
            return i, j
        if total < target:
            i += 1                                         # nums[i] is too small to pair with anything remaining
        else:
            j -= 1                                         # nums[j] is too large to pair with anything remaining
    return None

print(pair_with_sum([2, 7, 11, 15, 20], 26), pair_with_sum([2, 7, 11, 15, 20], 10))       # (2, 3) None

random.seed(3)
for _ in range(5_000):
    nums = sorted(random.randint(0, 30) for _ in range(random.randint(0, 12)))
    for target in range(0, 61, 3):
        answer = pair_with_sum(nums, target)
        brute = any(nums[a] + nums[b] == target for a in range(len(nums)) for b in range(a + 1, len(nums)))
        assert (answer is not None) == brute
        assert answer is None or (answer[0] < answer[1] and nums[answer[0]] + nums[answer[1]] == target)
print("pair_with_sum agrees with the brute-force pair search on 5,000 random lists")
```

```text
(2, 3) None
pair_with_sum agrees with the brute-force pair search on 5,000 random lists
```

The two-pointer technique appears all over array problems (three-sum, removing duplicates, merging, palindrome checks); the proof of correctness is always an elimination argument like the one above. For an *unsorted* list, a hash set ([hashing](../hashing/README.md)) finds the pair in O(n) instead.

## 📏 Exponential Search: When the Length Is Unknown

Binary search needs to know where the end is. What if the sorted sequence is unbounded — an infinite series, a very large file read sequentially, a sorted stream behind an API that returns `None` past the end? **Exponential search** (due to Bentley and Yao, 1976) first finds a range that must contain the target by *doubling* the probe index — 1, 2, 4, 8, … — until it reaches an item at least as large as the target (or the end), and then runs an ordinary binary search inside the last doubling range ([Wikipedia: Exponential search](https://en.wikipedia.org/wiki/Exponential_search)). If the target sits at index `i`, both phases take O(log i) steps, no matter how long the list is.

```python
def exponential_search(get, target):
    """Search a sorted sequence of unknown length. get(i) returns the i-th item, or None past the end."""
    if get(0) is None:
        return -1
    bound = 1
    while True:                                            # phase 1: double until the target must be at or before `bound`
        value = get(bound)
        if value is None or value >= target:
            break
        bound *= 2
    low, high = bound // 2, bound                          # phase 2: binary search in the last doubling range
    while low <= high:
        mid = (low + high) // 2
        value = get(mid)
        if value is None or value > target:
            high = mid - 1
        elif value < target:
            low = mid + 1
        else:
            return mid
    return -1

calls = 0
def square(i):                                             # the infinite sorted sequence 0, 1, 4, 9, 16, ...
    global calls
    calls += 1
    return i * i

print(f"{'target':>22} | {'found at index':>14} | {'get() calls':>11}")
for index in (5, 1_000, 1_000_000, 100_000_000):
    calls = 0
    found = exponential_search(square, index * index)
    print(f"{index * index:>22,} | {found:>14,} | {calls:>11}")

random.seed(4)
for _ in range(3_000):
    data = sorted(random.sample(range(200), random.randint(0, 40)))
    get = lambda i, data=data: data[i] if 0 <= i < len(data) else None
    for target in range(-1, 201, 5):
        assert exponential_search(get, target) == (data.index(target) if target in data else -1)
print("exponential_search agrees with list.index on 3,000 random finite lists")
```

```text
                target | found at index | get() calls
                    25 |              5 |           8
             1,000,000 |          1,000 |          18
     1,000,000,000,000 |      1,000,000 |          35
10,000,000,000,000,000 |    100,000,000 |          55
exponential_search agrees with list.index on 3,000 random finite lists
```

Searching for the square of a hundred million among an infinite sequence took 55 `get()` calls, because the cost depends on the position `i`, not on a length that does not exist. Even for ordinary arrays, exponential search can beat binary search when the target is likely to be near the front.

## 🎯 Interpolation Search: Guessing Instead of Halving

Binary search always probes the exact middle. If you know the keys are spread evenly — like names in a phone book, or timestamps arriving steadily — you can do better by *estimating* where the target should be, the way you open a dictionary near the back when looking for "wolf". **Interpolation search** probes at

`pos = low + (target − items[low]) · (high − low) / (items[high] − items[low])`

and then discards the part of the list on the wrong side of `pos`. On uniformly distributed keys it needs about `log log n` probes on average, but in the worst case — for instance when the keys grow exponentially — it can degrade to O(n) ([Wikipedia: Interpolation search](https://en.wikipedia.org/wiki/Interpolation_search)).

```python
def interpolation_search(items, target):
    """Return (index or -1, number of probes). The list must be sorted; it works best when the values are spread evenly."""
    low, high = 0, len(items) - 1
    probes = 0
    while low <= high and items[low] <= target <= items[high]:
        probes += 1
        if items[high] == items[low]:
            return (low if items[low] == target else -1), probes
        pos = low + (target - items[low]) * (high - low) // (items[high] - items[low])
        if items[pos] == target:
            return pos, probes
        if items[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1, probes

def binary_probes(items, target):
    low, high = 0, len(items) - 1
    probes = 0
    while low <= high:
        mid = (low + high) // 2
        probes += 1
        if items[mid] == target:
            return probes
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return probes

random.seed(5)
print(f"{'sorted data':>34} | {'interpolation: average (max)':>28} | {'binary: average':>15}")
for n in (1_000, 100_000, 1_000_000):
    uniform = sorted(random.sample(range(100 * n), n))
    targets = random.sample(uniform, min(2_000, n))
    inter = [interpolation_search(uniform, t)[1] for t in targets]
    binary = [binary_probes(uniform, t) for t in targets]
    print(f"{'evenly spread, n = ' + format(n, ','):>34} | {sum(inter) / len(inter):>19.2f} ({max(inter):>4}) | {sum(binary) / len(binary):>15.2f}")

skewed = sorted({int(1.0006 ** i) + i for i in range(30_000)})                       # keys that grow exponentially
targets = random.sample(skewed, 1_000)
inter = [interpolation_search(skewed, t)[1] for t in targets]
binary = [binary_probes(skewed, t) for t in targets]
print(f"{'exponentially growing, n = ' + format(len(skewed), ','):>34} | {sum(inter) / len(inter):>19.2f} ({max(inter):>4}) | {sum(binary) / len(binary):>15.2f}")

for _ in range(3_000):
    data = sorted(random.sample(range(300), random.randint(0, 40)))
    for target in range(-1, 301, 7):
        position, _ = interpolation_search(data, target)
        assert (position == -1) == (target not in data) and (position == -1 or data[position] == target)
print("interpolation_search agrees with a membership test on 3,000 random lists")
```

```text
                       sorted data | interpolation: average (max) | binary: average
          evenly spread, n = 1,000 |                3.66 (   8) |            8.99
        evenly spread, n = 100,000 |                4.09 (   9) |           15.68
      evenly spread, n = 1,000,000 |                4.18 (   9) |           18.89
 exponentially growing, n = 30,000 |             2152.64 (5231) |           13.94
interpolation_search agrees with a membership test on 3,000 random lists
```

On evenly spread data, interpolation search needs about 4 probes whether the list holds a thousand items or a million — `log log n` grows that slowly — while binary search needs 9, 16, and 19. On exponentially growing keys the linear estimate is badly wrong at every step and interpolation search needs thousands of probes where binary search needs about 14. The lesson is general: **an estimate speeds up the common case but gives up the guarantee**. Binary search's strength is that it assumes nothing about the values, only their order.

## 🧭 Recognizing the Pattern

Search-space reduction is the right tool when a problem has these three features:

- **Structure in the candidates** — sorted, rotated, monotone, bitonic, or arranged in a grid — that makes some tests informative.
- **A test that is cheap compared with scanning** and whose answer rules out a *large* region, not a single candidate.
- **A proof that the region can safely be discarded**, ideally one sentence long, written down before the code.

If the structure is only *partly* there, look for the weakest argument that still works (the matrix staircase needs only sorted rows and columns). If the argument fails in some case (duplicates in a rotated list), plan for the fallback and its cost. And whenever a brute-force version is easy to write, write it and compare the two on thousands of small inputs: with halving algorithms, a handful of hand-picked examples will not find the bug.

## Common Mistakes

- **Discarding a region without a proof.** The elimination step is the algorithm; code that "seems to work" on a few examples often fails on a case such as duplicates, a single item, or an empty range.
- **Forgetting that duplicates can break order-based reasoning**, as in the rotated array.
- **Mixing range conventions** (`low <= high` with `high = mid`, or `low < high` with `high = mid - 1`) — the cause of most infinite loops and skipped candidates.
- **Using the wrong tie-breaking rule in a peak search**: comparing with the *left* neighbour at the wrong boundary, or reading `nums[mid + 1]` when `mid` is the last index. The loop condition `low < high` guarantees `mid + 1` is valid.
- **Assuming interpolation search is always faster.** It is only faster when the keys are spread evenly; on skewed data it can be far slower than binary search.
- **Using the matrix staircase from the wrong corner.** Starting at the top-left or bottom-right gives no way to decide between "go right" and "go down".

## ➡️ Next

Continue to [binary-search-on-the-answer.md](binary-search-on-the-answer.md): the candidates do not have to be positions in a list at all. When the *answer* to a problem is a number in a range, and you can test whether a guess is big enough, you can binary-search the answer itself.
