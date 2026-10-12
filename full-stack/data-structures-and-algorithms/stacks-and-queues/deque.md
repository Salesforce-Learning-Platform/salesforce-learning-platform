# ⇄ The Deque (Double-Ended Queue)

## Add and Remove at Both Ends

A **deque** (pronounced "deck", short for *double-ended queue*) is a sequence where you can add and remove items at **either end** in constant
time. It generalizes both structures from this module: use only one end and it is a [stack](stack-fundamentals.md); add at one end and
remove at the other and it is a [queue](queue-fundamentals.md). Python's `collections.deque` is the standard implementation, and the
Python documentation describes it as a generalization of stacks and queues with thread-safe, memory-efficient appends and pops from either
side, at approximately the same O(1) speed in both directions.

```
 appendleft ─▶ ┌─────┬─────┬─────┬─────┬─────┐ ◀─ append
 popleft   ◀── │  1  │  2  │  3  │  4  │  5  │ ──▶ pop
               └─────┴─────┴─────┴─────┴─────┘
                front                    back
```

This file tours the deque's API, explains how it is built and why indexing into the middle is slow, and uses it for the **sliding window
maximum** — a classic problem whose O(n) solution depends on a deque. All outputs were produced by running the code on CPython 3.9.

## 🧰 The API

```python
from collections import deque

d = deque([2, 3, 4])
d.append(5)                  # add at the right end
d.appendleft(1)              # add at the left end
print(d)                     # deque([1, 2, 3, 4, 5])
print(d.pop(), d.popleft(), d)     # 5 1 deque([2, 3, 4])

d.extend([5, 6])             # add several items at the right, in order
d.extendleft([1, 0])         # add several at the left — each is placed in turn, so the order is REVERSED
print(d)                     # deque([0, 1, 2, 3, 4, 5, 6])

d.rotate(2)                  # rotate right: the last 2 items move to the front
print(d)                     # deque([5, 6, 0, 1, 2, 3, 4])
d.rotate(-3)                 # a negative number rotates left
print(d)                     # deque([1, 2, 3, 4, 5, 6, 0])

print(d[0], d[-1], len(d))   # 1 0 7       — indexing and len work like a list
print(3 in d)                # True        — membership is a scan: O(n)
```

Two details trip people up. **`extendleft` reverses the order** of what you give it, because it adds the items one at a time to the left end
(`extendleft([1, 0])` places `1`, then `0` in front of it). And **`rotate`** moves items from one end to the other in place — the same operation as
`rotate` in a [circular linked list](../linked-lists/circular-linked-lists.md).

### Bounded Deques: `maxlen`

Give a deque a maximum length and it becomes a **sliding window over a stream**: once it is full, adding to one end silently discards an
item from the opposite end.

```python
recent = deque(maxlen=3)
for value in range(1, 6):
    recent.append(value)
    print(list(recent))
# [1]
# [1, 2]
# [1, 2, 3]
# [2, 3, 4]
# [3, 4, 5]

left = deque([1, 2, 3], maxlen=3)
left.appendleft(0)                  # appending on the left pushes the rightmost item out
print(left)                         # deque([0, 1, 2], maxlen=3)
```

The documentation compares bounded deques to the Unix `tail` filter: ideal for "the last N log lines", "the last 10 actions", or a
moving average:

```python
class MovingAverage:
    def __init__(self, size):
        self._window = deque(maxlen=size)
        self._total = 0

    def add(self, value):
        if len(self._window) == self._window.maxlen:
            self._total -= self._window[0]          # the oldest value is about to be discarded
        self._window.append(value)
        self._total += value
        return self._total / len(self._window)

average = MovingAverage(3)
print([round(average.add(v), 2) for v in (10, 20, 30, 40, 50)])    # [10.0, 15.0, 20.0, 30.0, 40.0]
```

Updating a running total instead of re-summing the window makes each `add` O(1).

## 🧱 How a Deque Is Built — and Why the Middle Is Slow

CPython's `deque` is a **doubly linked list of fixed-size blocks**: each block holds 64 items, and the blocks are linked to each other in both
directions (this is stated in the comments of `Modules/_collectionsmodule.c`). Adding at either end writes into the end block, allocating a new
block only when it is full — so both ends are O(1), and the per-item memory overhead is small because one block's links are shared by 64 items.

The price is random access. To reach index `i`, the deque must hop from block to block from the nearer end, so the cost grows with the distance
from the ends. The documentation says it plainly: indexed access is O(1) at both ends but slows to O(n) in the middle, and for fast random
access you should use a list. A measurement of reading the *middle* element of each:

```python
import timeit

print(f"{'n':>9} | {'list[n // 2]':>12} | {'deque[n // 2]':>13}   (microseconds per read)")
for n in (1_000, 10_000, 100_000, 1_000_000):
    as_list = list(range(n))
    as_deque = deque(range(n))
    middle = n // 2
    t_list = min(timeit.repeat(lambda: as_list[middle], number=200, repeat=3)) / 200 * 1e6
    t_deque = min(timeit.repeat(lambda: as_deque[middle], number=200, repeat=3)) / 200 * 1e6
    print(f"{n:>9,} | {t_list:12.3f} | {t_deque:13.3f}")
```

One run on the test machine printed:

```
        n | list[n // 2] | deque[n // 2]   (microseconds per read)
    1,000 |        0.050 |         0.054
   10,000 |        0.044 |         0.112
  100,000 |        0.043 |         4.156
1,000,000 |        0.039 |        48.542
```

The list time is flat; the deque time grows with `n` — at a million items it is about a thousand times slower than the list — because the walk
covers more blocks. So choose by access pattern:

| Need | Choose |
|------|--------|
| Add/remove at both ends; FIFO queue; sliding window | `deque` |
| Index into the middle frequently; sort; slice | `list` |
| Stack only (one end) | Either; `list` is simplest |

## 🪞 Deque as a Two-Sided Reader: Palindromes

A deque lets you consume a sequence from both ends at once, which is exactly what a palindrome check does:

```python
def is_palindrome(text):
    letters = deque(ch.lower() for ch in text if ch.isalnum())
    while len(letters) > 1:
        if letters.popleft() != letters.pop():      # compare the two ends, then discard both
            return False
    return True

print(is_palindrome("A man, a plan, a canal: Panama"))     # True
print(is_palindrome("deque"))                              # False
```

(The two-pointer version in [palindrome-problems.md](../strings/palindrome-problems.md) uses O(1) extra space; the deque version copies the text,
trading space for clarity.)

## 📈 The Showpiece: Sliding Window Maximum

*Given a list of numbers and a window size `k`, report the maximum of every window of `k` consecutive numbers as the window slides one position
at a time.* For `[1, 3, -1, -3, 5, 3, 6, 7]` and `k = 3` the windows are `[1,3,-1]`, `[3,-1,-3]`, `[-1,-3,5]`, … with maxima `3, 3, 5, 5, 6, 7`.

The brute force scans every window: O(n · k). The [sliding-window technique](../arrays/sliding-window.md) works well for sums, but a maximum
cannot be updated by "subtract the outgoing element" — when the current maximum leaves the window, you need the *next* largest. A deque supplies
it. The key idea: keep the **indexes** of candidates in a deque whose values are in **decreasing order** from front to back. The front is always the
current maximum. For each new number:

1. **Expire** the front index if it has slid out of the window.
2. **Discard from the back** every index whose value is `<=` the new value — those numbers are older *and* smaller, so they can never be a window maximum again.
3. **Add** the new index at the back.
4. Once the first window is complete, report the front's value.

```python
def sliding_window_max(numbers, k):
    if k < 1:
        raise ValueError("k must be at least 1")
    window = deque()                         # indexes; their values decrease from front to back
    result = []
    for i, value in enumerate(numbers):
        if window and window[0] <= i - k:
            window.popleft()                 # 1. the front index fell out of the window
        while window and numbers[window[-1]] <= value:
            window.pop()                     # 2. smaller, older values can never be a maximum again
        window.append(i)                     # 3. add the new candidate
        if i >= k - 1:
            result.append(numbers[window[0]])    # 4. the front is the maximum of the current window
    return result

print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))       # [3, 3, 5, 5, 6, 7]
print(sliding_window_max([9, 8, 7, 6], 2))                     # [9, 8, 7]
print(sliding_window_max([1, 2, 3, 4], 4))                     # [4]
```

Trace on `[1, 3, -1, -3, 5, 3, 6, 7]` with `k = 3` (the deque shows *indexes*, with their values beside them):

```
i=0  value 1   deque: [0 (1)]
i=1  value 3   pop 0 (1 <= 3)      deque: [1 (3)]
i=2  value -1                      deque: [1 (3), 2 (-1)]            → window 0..2, max = 3
i=3  value -3                      deque: [1 (3), 2 (-1), 3 (-3)]    → max = 3
i=4  value 5   index 1 expired; pop 3, 2 (smaller)     deque: [4 (5)]   → max = 5
i=5  value 3                       deque: [4 (5), 5 (3)]             → max = 5
i=6  value 6   pop 5, 4            deque: [6 (6)]                    → max = 6
i=7  value 7   pop 6               deque: [7 (7)]                    → max = 7
```

**Why O(n)?** Each index is appended once and removed at most once — either from the back by a larger arrival or from the front when it
expires. The inner `while` loop looks quadratic, but its total work across the whole run is bounded by `n`, the same amortized argument as the
nested loop in [sliding-window.md](../arrays/sliding-window.md). Total: **O(n) time, O(k) space**. The invariant "values decrease from front to
back" is called a *monotonic* deque; the same idea with a stack is the subject of [monotonic-stack.md](monotonic-stack.md).

### Verification

```python
import random

random.seed(10)
for _ in range(10000):
    numbers = [random.randint(-10, 10) for _ in range(random.randint(1, 15))]
    k = random.randint(1, len(numbers))
    expected = [max(numbers[i:i + k]) for i in range(len(numbers) - k + 1)]
    assert sliding_window_max(numbers, k) == expected, (numbers, k)

moving, values = MovingAverage(4), []
for _ in range(5000):
    value = random.randint(0, 100)
    values.append(value)
    assert abs(moving.add(value) - sum(values[-4:]) / len(values[-4:])) < 1e-9
print("sliding_window_max and MovingAverage agree with brute force")
```

```text
sliding_window_max and MovingAverage agree with brute force
```

## ⚖️ Costs

| Operation | `deque` | `list` |
|-----------|---------|--------|
| Add/remove at the right end | O(1) | O(1) amortized |
| Add/remove at the **left** end | **O(1)** | O(n) |
| Index at the ends | O(1) | O(1) |
| Index in the middle | O(n) | **O(1)** |
| Insert/delete in the middle | O(n) | O(n) |
| `rotate(k)` | O(k) | O(n) (slicing) |
| Search with `in` | O(n) | O(n) |

## Common Mistakes

- **Indexing or slicing a deque in the middle** and expecting list speed (and slices are not supported — convert with `list()` first).
- **Forgetting that `extendleft` reverses** the order of its input.
- **Forgetting `maxlen` silently discards** items from the opposite end — a feature for sliding windows, a surprise if you expected an error.
- **Storing values instead of indexes** in the sliding-window deque, so you cannot tell when the front has expired.
- **Using `<` instead of `<=`** when discarding from the back, leaving equal values that are harmless for the maximum but break the invariant for other variants.
- **Using a deque as a `list` replacement** where random access or sorting is needed.

## ➡️ Next

Continue to [monotonic-stack.md](monotonic-stack.md) to see the same "keep a monotonic structure" idea applied with a stack, solving a family of
"next greater element" problems in a single pass.
