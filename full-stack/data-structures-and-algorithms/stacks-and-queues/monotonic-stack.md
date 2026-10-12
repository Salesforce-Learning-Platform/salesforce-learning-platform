# 📉 The Monotonic Stack

## A Stack That Keeps Itself Sorted

A **monotonic stack** is an ordinary [stack](stack-fundamentals.md) with one rule: the values inside it are always in sorted order
(all increasing, or all decreasing, from bottom to top). Before pushing a new value, you **pop everything that would break the order**. Those
pops are not wasted — each popped item has just met the first element that is "bigger" (or "smaller") than it, which is often exactly the
answer the problem asks for.

That makes the monotonic stack the tool for a family of questions that sound quadratic but are solved in a single pass:

- *For each element, what is the next element to its right that is greater?*
- *How many days until it is warmer?*
- *How far back does the current price stay the highest?*
- *What is the largest rectangle in a bar chart?*

The brute force for each is two nested loops (O(n²)). A monotonic stack is **O(n)**. This file explains the pattern with one example, then
applies it to six problems. Every function was checked against a brute-force version on thousands of random inputs. All outputs were produced by
running the code on CPython 3.9.

## 🧭 The Pattern in One Example: Next Greater Element

*For each number, find the first number to its right that is larger; use `-1` if there is none.* For `[2, 1, 2, 4, 3]` the answer is `[4, 2, 4, -1, -1]`.

Scan left to right, keeping a stack of **indexes still waiting for their answer**. Because every waiting element is still waiting, none of them has
met a larger value yet — so the waiting values must be in **non-increasing order** from bottom to top (a larger value would have already
resolved the smaller ones below it). When a new value arrives, it is the "next greater" for every waiting element smaller than it; pop and answer
those, then push the new index to wait for its own answer.

```python
def next_greater(numbers):
    result = [-1] * len(numbers)
    waiting = []                                   # indexes whose answer is still unknown; values never increase upward
    for i, value in enumerate(numbers):
        while waiting and numbers[waiting[-1]] < value:
            result[waiting.pop()] = value          # `value` is the first larger number to the right of that index
        waiting.append(i)
    return result                                  # indexes left on the stack have no greater element: they stay -1

print(next_greater([2, 1, 2, 4, 3]))               # [4, 2, 4, -1, -1]
print(next_greater([5, 4, 3, 2, 1]))               # [-1, -1, -1, -1, -1]
print(next_greater([1, 2, 3, 4, 5]))               # [2, 3, 4, 5, -1]
```

Trace on `[2, 1, 2, 4, 3]` (stack shows `index:value`):

```
i=0  value 2   stack []                    → push          stack [0:2]
i=1  value 1   2 < 1? no                   → push          stack [0:2, 1:1]
i=2  value 2   1 < 2: pop 1:1 → result[1]=2
               2 < 2? no                   → push          stack [0:2, 2:2]
i=3  value 4   2 < 4: pop 2:2 → result[2]=4
               2 < 4: pop 0:2 → result[0]=4
                                           → push          stack [3:4]
i=4  value 3   4 < 3? no                   → push          stack [3:4, 4:3]
end: 3:4 and 4:3 never met a larger value → stay -1
```

**Why is it O(n)?** The `while` loop sits inside the `for` loop, so it looks quadratic. But every index is pushed exactly once and popped at most
once, so across the whole run there are at most `n` pushes and `n` pops. The total work of the inner loop, summed over all iterations, is at most `n` —
the same amortized argument used for sliding windows in [sliding-window.md](../arrays/sliding-window.md) and for the monotonic *deque* in
[deque.md](deque.md). **O(n) time, O(n) space.**

## 🧰 The Template

```
for each element x at position i:
    while the stack is not empty and the element on top BREAKS the order relative to x:
        pop it — x is its answer
    (optionally) read the answer for x from what is now on top of the stack
    push x (or its index)
```

| You want… | Keep the stack… | Pop while… |
|-----------|-----------------|-----------|
| Next **greater** element to the right | Decreasing (non-increasing) | top **<** new value |
| Next **smaller** element to the right | Increasing (non-decreasing) | top **>** new value |
| Previous **greater** to the left | Decreasing | top **<=** new value, then the remaining top is the answer |
| Previous **smaller** to the left | Increasing | top **>=** new value, then the remaining top is the answer |

Store **indexes** rather than values when the answer needs a position or distance — you can always look the value up from the index.

## 🌡️ Problem 1: Days Until a Warmer Temperature

*Given daily temperatures, report for each day how many days until a warmer one (0 if never).* It is the next-greater problem answering with a distance
(`i − j`) instead of the value:

```python
def days_until_warmer(temperatures):
    answer = [0] * len(temperatures)
    waiting = []                                    # indexes of days still waiting for a warmer day
    for i, temperature in enumerate(temperatures):
        while waiting and temperatures[waiting[-1]] < temperature:
            j = waiting.pop()
            answer[j] = i - j                       # day i is the first warmer day after day j
        waiting.append(i)
    return answer

print(days_until_warmer([73, 74, 75, 71, 69, 72, 76, 73]))    # [1, 1, 4, 2, 1, 1, 0, 0]
```

## 📈 Problem 2: Stock Span

*For each day, count the consecutive days ending today (including today) whose price was less than or equal to today's.* Keep a stack of
`(price, span)` pairs with strictly decreasing prices. A new price absorbs the spans of every smaller-or-equal price it pops:

```python
def stock_spans(prices):
    spans = []
    stack = []                                      # (price, span) pairs; prices strictly decrease upward
    for price in prices:
        span = 1                                    # today itself
        while stack and stack[-1][0] <= price:
            span += stack.pop()[1]                  # absorb all the days that the popped entry covered
        stack.append((price, span))
        spans.append(span)
    return spans

print(stock_spans([100, 80, 60, 70, 60, 75, 85]))   # [1, 1, 1, 2, 1, 4, 6]
```

The trick is that a popped entry's span already summarizes *all* the days beneath it that it covered, so they never need to be revisited.

## ⬅️ Problem 3: The Previous Smaller Element

Scanning left to right with an **increasing** stack, the element left on top after popping is the nearest value to the left that is smaller than the new
one:

```python
def previous_smaller(numbers):
    result = []
    stack = []                                      # values; non-decreasing upward
    for value in numbers:
        while stack and stack[-1] >= value:
            stack.pop()                             # these can never be the nearest smaller for anything to the right
        result.append(stack[-1] if stack else -1)   # whatever remains on top is smaller than `value`
        stack.append(value)
    return result

print(previous_smaller([4, 5, 2, 10, 8]))           # [-1, 4, -1, 2, 2]
```

## 🔁 Problem 4: A Circular Array

If the array is *circular* (after the last element comes the first), the next greater element may be found by wrapping around. Treat the array as
if it were written twice, and go through two laps, using the index `i % n`. Only first-lap indexes need answers, so only those are pushed:

```python
def next_greater_circular(numbers):
    n = len(numbers)
    result = [-1] * n
    waiting = []
    for i in range(2 * n):                          # two laps
        value = numbers[i % n]
        while waiting and numbers[waiting[-1]] < value:
            result[waiting.pop()] = value
        if i < n:
            waiting.append(i)                       # second-lap elements only resolve others
    return result

print(next_greater_circular([1, 2, 1]))             # [2, -1, 2]
print(next_greater_circular([5, 4, 3, 2, 1]))       # [-1, 5, 5, 5, 5]
```

For `[1, 2, 1]` the last `1` wraps around to find `2`, and the `2` finds nothing larger even after a full lap, so it stays `-1`.

## 🏙️ Problem 5: The Largest Rectangle in a Histogram

*Given bar heights (each of width 1), find the area of the largest rectangle that fits inside the bars.* For `[2, 1, 5, 6, 2, 3]` the answer is `10`
(the two bars of heights 5 and 6, forming a 2 × 5 rectangle).

A rectangle's height is limited by its shortest bar. So for each bar, ask: *how far left and right can a rectangle of this bar's full height extend?*
The limit on each side is the nearest **smaller** bar — exactly what an increasing stack finds. Keep indexes of bars with increasing heights; when
a shorter bar arrives, each taller bar on the stack has found its right boundary. Its left boundary is the bar just beneath it on the stack:

```python
def largest_rectangle(heights):
    best = 0
    stack = []                                      # indexes of bars with increasing heights
    for i, h in enumerate(heights + [0]):           # the extra 0 height flushes the whole stack at the end
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]           # this bar's right boundary is i
            left = stack[-1] if stack else -1       # its left boundary is the bar now on top (or the edge)
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best

print(largest_rectangle([2, 1, 5, 6, 2, 3]))        # 10
print(largest_rectangle([2, 4]))                    # 4
print(largest_rectangle([]))                        # 0
```

Walk through the key moment. When the bar of height 2 (index 4) arrives, the stack holds `[1 (h=1), 2 (h=5), 3 (h=6)]`. Bar 3 (height 6) is taller, so
it is popped: its right boundary is index 4 and its left boundary is index 2 (still on the stack), giving width `4 − 2 − 1 = 1` and area `6`. Then bar 2
(height 5) pops: left boundary is index 1, width `4 − 1 − 1 = 2`, area `10` — the answer. This is O(n) instead of the brute force's O(n²).

## 🔢 Problem 6: Remove K Digits to Make the Smallest Number

*Given a number as a string and an integer `k`, remove exactly `k` digits so that the remaining number is as small as possible.* The greedy insight: a
digit that is **larger than the digit after it** should go first, since removing it makes the more significant position smaller. A stack of kept digits
makes that comparison with the most recent digit, popping while removals remain:

```python
def remove_k_digits(number, k):
    stack = []
    for digit in number:
        while k and stack and stack[-1] > digit:
            stack.pop()                             # a bigger digit before a smaller one: remove it
            k -= 1
        stack.append(digit)
    if k:
        stack = stack[:-k]                          # still removals left: the tail holds the largest digits
    return "".join(stack).lstrip("0") or "0"        # drop leading zeros; an empty result means 0

print(remove_k_digits("1432219", 3))                # 1219
print(remove_k_digits("10200", 1))                  # 200
print(remove_k_digits("10", 2))                     # 0
print(remove_k_digits("112", 1))                    # 11
```

For `"1432219"` with `k = 3`: the `4` is removed before the `3`, then the `3` before the `2`, then the `2` before the `1`, leaving `1219`. For `"112"`
nothing is out of order, so the removal comes from the end. Again each digit is pushed and popped at most once: O(n).

## ✅ Verification

Each function above was tested against a plain brute-force definition on thousands of random inputs:

```python
import itertools
import random

random.seed(13)

for _ in range(5000):
    numbers = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
    n = len(numbers)

    expected_next = [next((numbers[j] for j in range(i + 1, n) if numbers[j] > numbers[i]), -1) for i in range(n)]
    assert next_greater(numbers) == expected_next

    expected_days = [next((j - i for j in range(i + 1, n) if numbers[j] > numbers[i]), 0) for i in range(n)]
    assert days_until_warmer(numbers) == expected_days

    expected_spans = []
    for i in range(n):
        span = 1
        while i - span >= 0 and numbers[i - span] <= numbers[i]:
            span += 1
        expected_spans.append(span)
    assert stock_spans(numbers) == expected_spans

    expected_prev = [next((numbers[j] for j in range(i - 1, -1, -1) if numbers[j] < numbers[i]), -1) for i in range(n)]
    assert previous_smaller(numbers) == expected_prev

    expected_circular = [next((numbers[(i + step) % n] for step in range(1, n) if numbers[(i + step) % n] > numbers[i]), -1)
                         for i in range(n)]
    assert next_greater_circular(numbers) == expected_circular

    expected_area = max([min(numbers[i:j]) * (j - i) for i in range(n) for j in range(i + 1, n + 1)], default=0)
    assert largest_rectangle(numbers) == expected_area

for _ in range(3000):
    digits = "".join(random.choice("0123456789") for _ in range(random.randint(1, 7)))
    k = random.randint(0, len(digits))
    candidates = ["".join(digits[i] for i in range(len(digits)) if i not in removed) or "0"
                  for removed in map(set, itertools.combinations(range(len(digits)), k))]
    expected = str(min(int(c) for c in candidates))
    assert remove_k_digits(digits, k) == expected, (digits, k)
print("all six monotonic-stack functions agree with brute force")
```

```text
all six monotonic-stack functions agree with brute force
```

## ⏱️ Costs at a Glance

| Problem | Brute force | Monotonic stack |
|---------|-------------|-----------------|
| Next greater / smaller element | O(n²) | **O(n)** |
| Days until warmer | O(n²) | **O(n)** |
| Stock span | O(n²) | **O(n)** |
| Largest rectangle in a histogram | O(n²) | **O(n)** |
| Remove *k* digits | O(C(n, k)) combinations | **O(n)** |

Space is O(n) in every case (the stack, in the worst case, holds every index).

## 🧠 Recognizing the Pattern

Reach for a monotonic stack when a problem asks, *for each element*, about the **nearest** element on one side that is larger or smaller — or
about ranges bounded by such elements (spans, rectangles, "visible" buildings). The signal is the word *nearest* (or *next*, *previous*) combined
with a comparison. If instead the question is about a **window of fixed size** — "the maximum of every `k` consecutive values" — use the monotonic
*deque* in [deque.md](deque.md).

## Common Mistakes

- **Storing values when you need positions.** If the answer is a distance or a width, push indexes.
- **Using `<` where `<=` is needed (or the reverse)**, which mishandles equal values — decide what "greater" means for ties and test with duplicates.
- **Forgetting the leftovers** at the end: elements still on the stack have no answer (the default), or need to be flushed (a trailing sentinel such as
  the extra `0` in the histogram).
- **Thinking the nested loop is O(n²).** Count pushes and pops across the whole run instead.
- **Mixing up the direction** — scanning left to right finds *next* elements as items are popped, and *previous* elements as items are left on top.
- **Wrapping the array without bounding the second lap**, pushing second-lap indexes and corrupting the answers.

## Module Summary

The Stacks and Queues module covered two restricted ways of adding and removing items. [Stack Fundamentals](stack-fundamentals.md) introduced
last-in-first-out, with bracket matching, postfix evaluation, infix conversion, a min-stack, and undo.
[Queue Fundamentals](queue-fundamentals.md) introduced first-in-first-out, showed why `list.pop(0)` is a trap, built linked, ring-buffer, and
two-stack queues, and previewed breadth-first search. [The Deque](deque.md) combined both ends, explained why the middle is slow, and solved
the sliding-window maximum. This file used a stack that keeps itself ordered to solve "next greater" problems in a single pass.

Carry these ideas forward:

- A stack answers "most recent first"; a queue answers "oldest first"; a deque does both ends.
- In Python, use a `list` for stacks and `collections.deque` for queues — never `list.pop(0)`.
- Amortized analysis: a loop nested in a loop can still be O(n) if every element is added and removed once.
- Stacks power recursion and depth-first search; queues power breadth-first search — the two ways to explore trees and graphs next.
- Monotonic stacks and deques turn "nearest greater/smaller" and "window maximum" problems from O(n²) to O(n).

## ➡️ Next

Continue to the [Trees](../trees/README.md) module, the next module in this domain, where data is organized hierarchically — and where stacks and
queues become the two engines of traversal: depth-first and breadth-first.
