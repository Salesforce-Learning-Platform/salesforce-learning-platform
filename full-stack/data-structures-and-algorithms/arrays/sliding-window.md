# 🪟 The Sliding Window Technique

## Reuse the Work From the Previous Step

Many array problems ask about a **contiguous run** of elements: the best sum of `k` consecutive
values, the shortest stretch that reaches a target, the longest stretch with no repeats. The obvious
approach examines every possible run and recomputes each one from scratch. The **sliding window**
instead keeps a *summary* of the current run and updates it as the run moves one step — adding the
element that enters and removing the one that leaves — turning O(n·k) or O(n²) work into **O(n)**.

It is a close relative of [two-pointer-technique.md](two-pointer-technique.md): two indexes,
`left` and `right`, mark the window's edges, but here **both only move forward**, and what matters is
the summary of everything between them.

## 📏 Fixed-Size Window: Maximum Sum of `k` Consecutive Elements

The brute-force version re-adds `k` numbers for every position — O(n · k):

```python
def max_sum_of_k_brute(nums, k):
    return max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1))
```

Consecutive windows share `k - 1` elements, so there is no need to re-add them:

```python
def max_sum_of_k(nums, k):
    if k <= 0 or k > len(nums):
        raise ValueError("k must be between 1 and len(nums)")
    window = sum(nums[:k])                       # the first window, computed once
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]   # add the newcomer, drop the oldest
        best = max(best, window)
    return best

max_sum_of_k([2, 1, 5, 1, 3, 2], 3)   # 9
```

Tracing `[2, 1, 5, 1, 3, 2]` with `k = 3`:

```
first window [2, 1, 5]            sum = 8
slide: add 1, drop 2  → [1, 5, 1]  sum = 8 + 1 - 2 = 7
slide: add 3, drop 1  → [5, 1, 3]  sum = 7 + 3 - 1 = 9   ← best
slide: add 2, drop 5  → [1, 3, 2]  sum = 9 + 2 - 5 = 6
```

Each slide is O(1), so the whole scan is **O(n)** time. (`nums[:k]` makes a temporary copy of `k`
elements; summing the first `k` values with a plain loop keeps the extra space strictly O(1).)

## 🔄 Variable-Size Window: Shortest Run That Reaches a Target

Find the length of the shortest contiguous subarray whose sum is **at least** `target`. The window
grows on the right until it qualifies, then shrinks from the left for as long as it *still*
qualifies:

```python
def min_subarray_len(nums, target):
    left = 0
    window = 0
    best = float("inf")
    for right in range(len(nums)):
        window += nums[right]                   # expand: take in nums[right]
        while window >= target:                 # still qualifies: try to shrink
            best = min(best, right - left + 1)
            window -= nums[left]
            left += 1
    return 0 if best == float("inf") else best

min_subarray_len([2, 3, 1, 2, 4, 3], 7)   # 2   (the subarray [4, 3])
```

Notice *where* the answer is recorded: for a **shortest** valid window, every shrink step that still
qualifies is a candidate, so the update sits **inside** the `while` loop.

**This version assumes non-negative numbers and `target >= 1`.** It relies on the window sum only
growing as the window grows and only shrinking as it shrinks. With negative values that breaks:

```python
min_subarray_len([2, -1, 2, 3, -2, 5], 5)   # returns 3 — but the true answer is 1 (the lone 5)
```

Shrinking stopped as soon as the sum dipped below 5, so the window never got to try "drop the `-2`",
which would have *raised* the sum. When values can be negative, a sliding window is the wrong tool.

## 🔤 Variable-Size Window With a Set: Longest Run With No Repeats

Find the length of the longest substring in which no character repeats. A `set` tracks which
characters are currently inside the window; when the incoming character is already there, shrink
from the left until it is not:

```python
def longest_unique_substring(text):
    seen = set()
    left = 0
    best = 0
    for right, char in enumerate(text):
        while char in seen:                 # a repeat: shrink until it's gone
            seen.remove(text[left])
            left += 1
        seen.add(char)
        best = max(best, right - left + 1)  # the window [left, right] is now valid
    return best

longest_unique_substring("abcabcbb")   # 3   ("abc")
```

Here the update goes **after** the `while` loop: for a **longest** valid window, only the window
that has just been made valid again is a candidate. (Membership checks on a set are O(1) on average;
the Hashing module, later in this domain, explains why. A string is treated as an array of
characters here.)

## 🧩 The Template

```
left = 0
for right in range(len(items)):
    add items[right] to the window's summary
    while the window breaks (or, for 'shortest', still meets) the rule:
        [shortest: record the answer here]
        remove items[left] from the summary
        left += 1
    [longest: record the answer here]
```

The two flavours differ only in where the answer is recorded, as the previous two examples showed.

## 🧠 Why It Is O(n) Even With a Nested `while`

[analyzing-algorithms.md](../time-and-space-complexity/analyzing-algorithms.md) said nested loops
multiply. That rule assumes the inner loop **restarts from the beginning** on every outer iteration.
Here it does not: `left` only ever moves forward. Across the *entire* run, `right` advances at most
`n` times and `left` advances at most `n` times — at most `2n` steps in total. Counting the total
work across the whole run, rather than per iteration, is called **amortized analysis**, the same
idea that makes `append` amortized O(1) in [array-fundamentals.md](array-fundamentals.md).

Space is O(1) for numeric windows. When the window's summary is a set, as in the last example, it is
bounded by the window's size — and, for characters, by the size of the alphabet.

## 👀 Recognizing the Pattern

Reach for a sliding window when the problem says:

- "contiguous subarray" or "substring"
- "longest" or "shortest" run satisfying a rule
- "maximum (or minimum) over every window of size `k`"
- the rule can be updated cheaply when one element enters and one leaves

If the elements you want are *not* contiguous, or negatives break the "grow means bigger" logic,
look elsewhere.

## Common Mistakes

- **Recomputing the window from scratch** at every step — that quietly returns the solution to
  O(n · k).
- **Forgetting to remove the outgoing element's contribution** when `left` advances, leaving the
  summary out of sync with the window.
- **Recording the answer in the wrong place** — inside the `while` for "shortest", after it for
  "longest".
- **Using a sum-based window on data with negative numbers**, where growing the window can lower the
  sum.
- **Miscounting the window length** — it is `right - left + 1`, not `right - left`.
- **Not guarding `k > len(nums)`** in the fixed-size version.

## Module Summary

Across this module: an **array** stores its elements in contiguous memory, so reading or writing by
index is a single address calculation — O(1) — and dynamic arrays such as Python's `list` stay
usable as they grow because `append` is amortized O(1) (see
[array-fundamentals.md](array-fundamentals.md)); **traversal** visits every element in O(n) time and
O(1) extra space, with the classic trap of changing a list while looping over it (see
[traversal.md](traversal.md)); **insertion and deletion** are cheap at the end but cost O(n)
elsewhere because later elements must shift, with `deque`, swap-and-pop, bulk filtering, and
`bisect` as the standard ways to work around or understand that cost (see
[insertion-and-deletion.md](insertion-and-deletion.md)); the **two-pointer technique** replaces
nested loops with a single O(n), O(1)-space pass when the data has structure — sorted order,
symmetry, or a reader/writer split (see [two-pointer-technique.md](two-pointer-technique.md)); and
the **sliding window** maintains a running summary of a contiguous region, amortizing its inner loop
into O(n) total work (see this file). Every complexity claim here uses the vocabulary built in
[Time and Space Complexity](../time-and-space-complexity/).

## ➡️ Next

Continue to the Strings module, the next module in this domain, where the two-pointer and
sliding-window ideas reappear on text.
