# ↔️ The Two-Pointer Technique

## Two Indexes Instead of Two Nested Loops

Many array problems look like they require comparing every pair of elements — the nested-loop
O(n²) shape from `has_duplicate` in
[big-o-notation.md](../time-and-space-complexity/big-o-notation.md). When the array has some
*structure* (it is sorted, it is symmetric, or you only need to compact it), a pair of indexes
moving in a controlled way can settle the question in a **single pass: O(n) time and O(1) extra
space**.

## 🧭 The Two Common Patterns

```
OPPOSITE ENDS    left starts at index 0, right starts at index n-1,
                 and they move TOWARD each other.
                 → pair sums in sorted data, palindromes, reversing,
                   "best pair" problems

SAME DIRECTION   a READER scans every element; a WRITER trails behind,
                 marking where the next kept element belongs.
                 → removing items or compacting an array IN PLACE
```

(A third pattern — a "fast" and a "slow" pointer moving at different speeds — shows up mainly with
linked lists, later in this domain.)

## 🎯 Worked Example 1: A Pair That Adds Up to a Target (Sorted Array)

The brute-force version tries every pair:

```python
def has_pair_brute(nums, target):          # O(n²)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return True
    return False
```

With the array **sorted**, two pointers do it in one pass:

```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return left, right
        if total < target:
            left += 1          # need a bigger sum: the smallest value can't help
        else:
            right -= 1         # need a smaller sum: the largest value can't help
    return None
```

Tracing `two_sum_sorted([1, 3, 4, 6, 8, 11], 10)`:

```
left=0 (1), right=5 (11): 12 > 10  → move right inward
left=0 (1), right=4 (8):   9 < 10  → move left inward
left=1 (3), right=4 (8):  11 > 10  → move right inward
left=1 (3), right=3 (6):   9 < 10  → move left inward
left=2 (4), right=3 (6):  10 = 10  → found: indexes 2 and 3
```

**Why discarding is safe.** Because the array is sorted, if `nums[left] + nums[right]` is too small,
then `nums[left]` paired with *any* element at or before `right` is smaller still — so `nums[left]`
cannot be part of any solution among the remaining candidates, and can be discarded. The mirror
argument discards `nums[right]` when the sum is too large. Every iteration discards one element, so
the loop runs at most `n - 1` times: **O(n) time, O(1) space**. Remove the sortedness and this
argument — and the algorithm — no longer holds.

## 🪞 Worked Example 2: Reversing and Palindromes

Both walk inward from the two ends:

```python
def reverse_in_place(items):
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1

def is_palindrome(text):
    left, right = 0, len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True

is_palindrome("racecar")   # True
is_palindrome("python")    # False
```

`reverse_in_place` needs no second list — O(1) extra space — in contrast to `items[::-1]`, which
builds a full copy. (Text is just an array of characters here; the Strings module treats it in
depth.)

## 💧 Worked Example 3: Container With the Most Water

Given a list of vertical line heights, pick two lines that, together with the x-axis, hold the most
water. The area for lines at positions `i < j` is `(j - i) × min(height[i], height[j])`.

```python
def max_area(heights):
    left, right = 0, len(heights) - 1
    best = 0
    while left < right:
        width = right - left
        best = max(best, width * min(heights[left], heights[right]))
        if heights[left] < heights[right]:
            left += 1          # the shorter line limits the area — try replacing it
        else:
            right -= 1
    return best

max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])   # 49  (lines at index 1 and 8: width 7 × height 7)
```

The key decision is *which* pointer to move. The area is capped by the **shorter** line. Moving the
taller line inward shrinks the width and cannot raise the cap, so it can never beat the current
best — only replacing the shorter line has any chance of improving the result.

## 🧹 Worked Example 4: Remove Duplicates From a Sorted Array, In Place

Here the pointers move in the **same direction**. `read` scans every element; `write` marks the
next slot for a value not yet kept:

```python
def remove_duplicates_sorted(nums):
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:   # a value we haven't kept yet
            nums[write] = nums[read]
            write += 1
    return write                             # the new length

data = [1, 1, 2, 2, 2, 3, 5, 5]
k = remove_duplicates_sorted(data)
print(k, data[:k])   # 4 [1, 2, 3, 5]
print(data)          # [1, 2, 3, 5, 2, 3, 5, 5]
```

The invariant is: *`nums[:write]` always holds the distinct values seen so far, in order.* Only the
first `k` elements are meaningful afterward — the tail still holds leftovers, as the last line of
output shows. One pass, O(n) time, O(1) space — no repeated shifting.

## 0️⃣ Worked Example 5: Move Zeroes to the End, Keeping Order

```python
def move_zeroes(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1

data = [0, 1, 0, 3, 12]
move_zeroes(data)
print(data)          # [1, 3, 12, 0, 0]
```

When `write == read` the swap is a harmless self-swap. This is the safe, single-pass,
constant-space answer to the "remove while iterating" bug shown in [traversal.md](traversal.md), and
it avoids the repeated O(n) shifting that
[insertion-and-deletion.md](insertion-and-deletion.md) warns about.

## 🔍 Why It Is O(n)

Each pointer only ever moves in **one direction**. In the opposite-ends pattern the two pointers
close a gap of length `n`, so together they take at most `n - 1` steps. In the reader/writer pattern
the reader makes exactly one pass and the writer never passes it. There is no inner loop restarting
from the beginning — which is what separates this from the nested-loop O(n²) shape.

## ✅ When to Reach for It

| Situation | Pattern | Needs |
|-----------|---------|-------|
| Pair or triple with a target sum | Opposite ends | Sorted data |
| Palindrome check, in-place reversal | Opposite ends | Symmetric access from both ends |
| Best pair by a formula (most water) | Opposite ends | A rule for which side to discard |
| Remove or reorder in place | Reader / writer | One-pass decision per element |

If the data is **not** sorted and you need a pair sum, two pointers alone are the wrong tool:
sorting first costs O(n log n) and loses the original positions, and a hash-based lookup (covered in
the Hashing module, later in this domain) solves it in O(n) without sorting.

## Common Mistakes

- **Applying the opposite-ends pair search to unsorted data** — it returns wrong answers without
  raising any error, because the "safe to discard" argument no longer holds.
- **Writing `left <= right` in a pair problem**, which allows `left == right` and pairs an element
  with itself.
- **Forgetting to move a pointer in one branch** — the loop never ends.
- **Reading past the returned length after in-place compaction** — the tail holds leftovers (see the
  second `print` in Worked Example 4).
- **Moving the taller line in the "most water" problem** — only moving the shorter line can help.

## ➡️ Next

Continue to [sliding-window.md](sliding-window.md) to see a close relative of this technique that
moves both pointers forward and keeps a running summary of everything between them.
