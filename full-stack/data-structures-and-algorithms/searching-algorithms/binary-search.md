# 🎯 Binary Search

## Halve the Possibilities With Every Question

You do not find a name in a printed phone book by reading every entry. You open it near the middle, see whether the name you want comes before or after the page you are looking at, and keep only the half that can contain it — then repeat. **Binary search** is exactly that, applied to a sorted list: compare the target with the middle item, discard the half that cannot contain it, and continue with what is left. Each comparison halves the remaining items, so a list of a million needs at most 20 probes and a list of a billion needs at most 30 — compared with the half a million (or half a billion) comparisons of [linear search](linear-search.md).

Binary search needs two things from the data: it must be **sorted** (see the [Sorting Algorithms](../sorting-algorithms/README.md) module), and it must support **random access** — jumping straight to the middle. Arrays and Python lists qualify; a linked list does not. The idea is simple to state and notoriously easy to get wrong: Jon Bentley observed that the first binary search was published in 1946 but the first one that worked for every `n` did not appear until 1962 (quoted in [Joshua Bloch's 2006 post](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/)). This file builds the algorithm iteratively and recursively, proves it correct, counts its probes exactly, extends it to duplicates, shows Python's `bisect` module, and demonstrates the classic bugs on purpose. All outputs were produced by running the code on CPython 3.9.

## 🧱 The Iterative Algorithm

Keep two indexes, `low` and `high`, that bracket the part of the list where the target could still be. Probe the middle:

- If the middle item is the target, return its index.
- If the middle item is smaller than the target, the target can only be to the right: set `low = mid + 1`.
- If it is larger, the target can only be to the left: set `high = mid - 1`.
- When `low` passes `high`, nothing remains: the target is not in the list.

```python
def binary_search(items, target):
    """Return an index of target in the sorted list items, or -1. O(log n) time, O(1) space."""
    low, high = 0, len(items) - 1                    # the target, if present, is somewhere in items[low..high]
    while low <= high:
        mid = low + (high - low) // 2                # the middle (written to be safe in languages with fixed-size integers)
        if items[mid] == target:
            return mid
        if items[mid] < target:
            low = mid + 1                            # discard mid and everything to its left
        else:
            high = mid - 1                           # discard mid and everything to its right
    return -1

def trace_binary_search(items, target):
    low, high = 0, len(items) - 1
    lines = []
    while low <= high:
        mid = low + (high - low) // 2
        verdict = "found" if items[mid] == target else ("go right" if items[mid] < target else "go left")
        lines.append(f"low={low:>2} high={high:>2} mid={mid:>2}  items[mid]={items[mid]:>3}  {verdict}")
        if items[mid] == target:
            break
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    else:
        lines.append(f"low={low:>2} high={high:>2}  empty range: {target} is not in the list")
    return "\n".join(lines)

numbers = [3, 8, 14, 21, 27, 33, 40, 46, 52, 61, 67, 74, 80, 89, 95, 99]
print(trace_binary_search(numbers, 67))
print()
print(trace_binary_search(numbers, 50))
print(binary_search(numbers, 67), binary_search(numbers, 50))               # 10 -1
```

```text
low= 0 high=15 mid= 7  items[mid]= 46  go right
low= 8 high=15 mid=11  items[mid]= 74  go left
low= 8 high=10 mid= 9  items[mid]= 61  go right
low=10 high=10 mid=10  items[mid]= 67  found

low= 0 high=15 mid= 7  items[mid]= 46  go right
low= 8 high=15 mid=11  items[mid]= 74  go left
low= 8 high=10 mid= 9  items[mid]= 61  go left
low= 8 high= 8 mid= 8  items[mid]= 52  go left
low= 8 high= 7  empty range: 50 is not in the list
10 -1
```

Searching for 67 in 16 items took 4 probes; searching for the missing 50 took 4 probes before the range emptied. A linear search would have needed 11 comparisons for 67 and 16 to learn that 50 is absent.

## ✅ Why It Is Correct: A Loop Invariant

The most reliable way to write a binary search is to state what is true at the top of every iteration — the **loop invariant** — and make every line preserve it:

> **Invariant:** if the target is in the list at all, it is in `items[low..high]`.

- *Initially* `low..high` is the whole list, so the invariant holds.
- *Each step preserves it:* if `items[mid] < target`, then because the list is sorted everything at or before `mid` is smaller than the target, so the target can only be in `mid + 1..high`; the other branch is symmetric.
- *The loop ends:* every iteration shrinks the range by at least one item (`mid` is excluded), so `low > high` eventually, and then the invariant says the target was never in the list.

The next block turns the invariant into an executable check. A copy of the search asserts it at the top of every iteration, and it is run on **every** sorted list of up to eight values taken from `0..5` (so duplicates are common) against **every** target, present or absent, including targets below the smallest and above the largest item:

```python
import itertools

def binary_search_checked(items, target):
    low, high = 0, len(items) - 1
    checks = 0
    while low <= high:
        assert target not in items or target in items[low:high + 1], "invariant broken"
        checks += 1
        mid = low + (high - low) // 2
        if items[mid] == target:
            return mid, checks
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    assert target not in items
    return -1, checks

lists_tested = searches = total_checks = 0
for size in range(0, 9):
    for items in itertools.combinations_with_replacement(range(6), size):         # every sorted list; duplicates allowed
        lists_tested += 1
        for target in range(-1, 7):
            index, checks = binary_search_checked(list(items), target)
            assert (index == -1) == (target not in items) and (index == -1 or items[index] == target)
            searches += 1
            total_checks += checks
print(f"{lists_tested:,} sorted lists, {searches:,} searches, {total_checks:,} invariant checks: all passed")
```

```text
3,003 sorted lists, 24,024 searches, 62,516 invariant checks: all passed
```

## 📏 How Many Probes? Exactly `⌊log₂ n⌋ + 1`

After `k` probes, at most `n / 2ᵏ` items remain, so the search ends after at most `⌊log₂ n⌋ + 1` probes. That formula is exact for the worst case, not just an upper bound. The block below counts probes for every possible target — present or absent — in lists of many sizes, and compares the worst case with the formula and with linear search:

```python
import math
import random

def probes_used(items, target):
    low, high = 0, len(items) - 1
    probes = 0
    while low <= high:
        mid = low + (high - low) // 2
        probes += 1
        if items[mid] == target:
            return probes
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return probes

print(f"{'n':>9} | {'worst-case probes':>17} | {'floor(log2 n) + 1':>17} | {'linear worst case':>17}")
for n in (1, 2, 3, 4, 7, 8, 100, 1_000, 1_023, 1_024, 1_025):
    items = [2 * i for i in range(n)]                                                  # gaps, so that absent targets exist
    worst = max(probes_used(items, target) for target in range(-1, 2 * n + 1))        # every present and absent target
    assert worst == math.floor(math.log2(n)) + 1
    print(f"{n:>9,} | {worst:>17} | {math.floor(math.log2(n)) + 1:>17} | {n:>17,}")

random.seed(1)
n = 1_000_000
items = list(range(n))
worst = max(probes_used(items, target) for target in random.sample(range(n), 20_000))
print(f"{n:>9,} | {worst:>17} | {math.floor(math.log2(n)) + 1:>17} | {n:>17,}   (20,000 random targets)")
```

```text
        n | worst-case probes | floor(log2 n) + 1 | linear worst case
        1 |                 1 |                 1 |                 1
        2 |                 2 |                 2 |                 2
        3 |                 2 |                 2 |                 3
        4 |                 3 |                 3 |                 4
        7 |                 3 |                 3 |                 7
        8 |                 4 |                 4 |                 8
      100 |                 7 |                 7 |               100
    1,000 |                10 |                10 |             1,000
    1,023 |                10 |                10 |             1,023
    1,024 |                11 |                11 |             1,024
    1,025 |                11 |                11 |             1,025
1,000,000 |                20 |                20 |         1,000,000   (20,000 random targets)
```

Doubling the list size adds exactly one probe: that is what O(log n) means in practice. A thousand items need 10 probes, a million need 20, a billion need 30, and eight billion need 33.

## 🔁 The Recursive Version

Binary search is naturally recursive: searching a range means checking the middle and then searching a smaller range.

```python
def binary_search_recursive(items, target, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low > high:
        return -1                                                            # the base case: an empty range
    mid = low + (high - low) // 2
    if items[mid] == target:
        return mid
    if items[mid] < target:
        return binary_search_recursive(items, target, mid + 1, high)
    return binary_search_recursive(items, target, low, mid - 1)

print(binary_search_recursive(numbers, 67), binary_search_recursive(numbers, 50))        # 10 -1
```

It computes the same answers, but uses O(log n) stack space instead of O(1): one frame per probe. Because the depth is at most `⌊log₂ n⌋ + 1`, Python's recursion limit (about 1,000 frames) is never a problem — a 30-frame stack suffices for a billion items. Because the recursive call is the last thing the function does, it converts mechanically into the loop above; in Python, where there is no tail-call optimization, the loop is the better choice.

Binary search needs only `len()` and indexing — not a real list. Python's `range` supports both without storing anything, so you can search a sequence of a trillion numbers:

```python
trillion = range(0, 3 * 10**12, 3)                      # a million-million multiples of 3, never stored in memory
index = binary_search(trillion, 123_456_789_012)
print(index, trillion[index])                           # 41152263004 123456789012
print(probes_used(trillion, 123_456_789_012), "probes for a sequence of", f"{len(trillion):,}", "items")
```

```text
41152263004 123456789012
37 probes for a sequence of 1,000,000,000,000 items
```

## 🟰 Duplicates: Lower and Upper Bounds

With repeated values, the plain `binary_search` returns *some* matching index — whichever probe happens to land on a match — not necessarily the first or the last:

```python
repeated = [1, 2, 2, 2, 2, 3]
print(binary_search(repeated, 2))                       # 2   — a valid answer, but neither the first (1) nor the last (4)
```

The fix is to search not for "a match" but for a **boundary**. The standard tools are two questions with unambiguous answers:

- `lower_bound(x)`: the index of the **first** item that is `>= x` (or `len(items)` if every item is smaller).
- `upper_bound(x)`: the index of the **first** item that is `> x` (or `len(items)`).

Both are written with a half-open range `[low, high)`, in which `high` may equal `len(items)` because the answer can be "one past the end":

```python
def lower_bound(items, target):
    """Index of the first item >= target; len(items) if there is none."""
    low, high = 0, len(items)                    # the answer is somewhere in [low, high]
    while low < high:
        mid = low + (high - low) // 2
        if items[mid] < target:
            low = mid + 1                        # items[mid] is too small to be the answer
        else:
            high = mid                           # items[mid] could be the answer, so keep it
    return low

def upper_bound(items, target):
    """Index of the first item > target; len(items) if there is none."""
    low, high = 0, len(items)
    while low < high:
        mid = low + (high - low) // 2
        if items[mid] <= target:
            low = mid + 1
        else:
            high = mid
    return low

def first_occurrence(items, target):
    i = lower_bound(items, target)
    return i if i < len(items) and items[i] == target else -1

def last_occurrence(items, target):
    i = upper_bound(items, target) - 1
    return i if i >= 0 and items[i] == target else -1

def count_occurrences(items, target):
    return upper_bound(items, target) - lower_bound(items, target)

def floor_value(items, x):                       # the largest item <= x, or None
    i = upper_bound(items, x)
    return items[i - 1] if i > 0 else None

def ceiling_value(items, x):                     # the smallest item >= x, or None
    i = lower_bound(items, x)
    return items[i] if i < len(items) else None

data = [1, 2, 2, 2, 2, 3, 5, 8, 8, 13]
print(lower_bound(data, 2), upper_bound(data, 2))                   # 1 5
print(first_occurrence(data, 2), last_occurrence(data, 2))          # 1 4
print(count_occurrences(data, 2), count_occurrences(data, 4))       # 4 0
print(lower_bound(data, 4), lower_bound(data, 99))                  # 6 10
print(floor_value(data, 7), ceiling_value(data, 7))                 # 5 8
print(floor_value(data, 0), ceiling_value(data, 14))                # None None
```

These two functions are the workhorses of binary searching. A single call answers many questions: where an item *would be inserted* to keep the list sorted (`lower_bound`), how many items fall in a range (`upper_bound(b) − lower_bound(a)`), the nearest item below or above a value, and whether a value is present at all.

The half-open template has a different invariant from the first version — and it is worth learning, because [binary search on the answer](binary-search-on-the-answer.md) uses it again:

> **Invariant (lower_bound):** everything before `low` is `< target`; everything from `high` on is `>= target`. The loop ends when `low == high`, and that single remaining position is the boundary.

In the `else` branch the code sets `high = mid`, not `mid - 1`, because `mid` may itself be the answer; it still terminates because `mid < high` whenever `low < high`, so the range always shrinks.

## 🐍 Python's `bisect` Module

The standard library implements exactly these boundaries, in C:

| `bisect` function | Same as |
|-------------------|---------|
| `bisect.bisect_left(a, x)` | `lower_bound` |
| `bisect.bisect_right(a, x)` (alias `bisect.bisect`) | `upper_bound` |
| `bisect.insort_left(a, x)` / `insort_right(a, x)` | insert `x` at that position (the search is O(log n); the insertion shifts items, so O(n)) |

Both search functions accept optional `lo` and `hi` arguments to restrict the range. A membership test with `bisect` is one boundary lookup plus an equality check. The `key` parameter, which lets `bisect` search records by a field, was added in Python 3.10 ([Python docs: bisect](https://docs.python.org/3/library/bisect.html)); it is not available on the Python 3.9 used to run this module, where the usual workaround is a separate sorted list of keys.

```python
import bisect

def contains(sorted_items, x):
    i = bisect.bisect_left(sorted_items, x)
    return i < len(sorted_items) and sorted_items[i] == x

random.seed(2)
for _ in range(5_000):
    items = sorted(random.randint(0, 10) for _ in range(random.randint(0, 15)))
    for x in range(-1, 12):
        assert lower_bound(items, x) == bisect.bisect_left(items, x)
        assert upper_bound(items, x) == bisect.bisect_right(items, x)
        assert contains(items, x) == (x in items)
        assert count_occurrences(items, x) == items.count(x)
        assert first_occurrence(items, x) == (items.index(x) if x in items else -1)
        assert last_occurrence(items, x) == (len(items) - 1 - items[::-1].index(x) if x in items else -1)
        copy = list(items)
        bisect.insort_right(copy, x)
        assert copy == sorted(items + [x])
print("lower/upper bounds, counts, first/last occurrences and insertion agree with bisect and list methods on 5,000 random lists")
```

```text
lower/upper bounds, counts, first/last occurrences and insertion agree with bisect and list methods on 5,000 random lists
```

How do the options compare on a sorted list of a million numbers? Time per search, averaged over 1,000 present targets:

```python
import timeit

random.seed(3)
n = 1_000_000
data = sorted(random.sample(range(10 * n), n))
targets = random.sample(data, 1_000)
lookup = set(data)

def per_call_us(function, arguments, number=3):
    return min(timeit.repeat(lambda: [function(a) for a in arguments], number=number, repeat=3)) / number / len(arguments) * 1e6

print(f"{'method':>34} | {'time per search':>16}")
print(f"{'x in list (linear scan)':>34} | {per_call_us(lambda x: x in data, targets[:20], number=1):>13,.0f} us")
print(f"{'hand-written binary_search':>34} | {per_call_us(lambda x: binary_search(data, x), targets):>13.2f} us")
print(f"{'bisect_left + equality check':>34} | {per_call_us(lambda x: contains(data, x), targets):>13.2f} us")
print(f"{'x in set (hash table)':>34} | {per_call_us(lambda x: x in lookup, targets):>13.3f} us")
```

Output:

```
                            method |  time per search
           x in list (linear scan) |        17,026 us
        hand-written binary_search |          2.25 us
      bisect_left + equality check |          0.54 us
             x in set (hash table) |         0.049 us
```

The hand-written Python binary search is thousands of times faster than the scan, and the C implementation in `bisect` is several times faster than the Python one. The set is faster still — but it costs O(n) extra memory, cannot answer "what is the next larger item?", and has no order. Binary search is the tool when the data is sorted (or must stay sorted), when you need **boundaries and ranges**, or when memory is tight.

## 🪲 Classic Bugs, on Purpose

Binary search is the standard example of an algorithm that is short, "obvious", and wrong in many published versions. Four ways it fails:

**1. The midpoint overflow.** `mid = (low + high) // 2` is wrong in languages with fixed-size integers when `low + high` exceeds the largest integer: the sum wraps to a negative number. This was found in the binary search that Bloch wrote for the Java library (`java.util.Arrays`) and in the one Bentley proved correct in *Programming Pearls*; it appears only for arrays of about a billion elements ([Bloch, 2006](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/)). Python integers never overflow, but we can simulate a 32-bit integer to see the effect, and `low + (high - low) // 2` is safe everywhere:

```python
import ctypes

low, high = 1_500_000_000, 2_000_000_000
print("true midpoint:                  ", (low + high) // 2)
print("(low + high) // 2 in 32-bit ints:", ctypes.c_int32(low + high).value // 2)
print("low + (high - low) // 2:         ", low + (high - low) // 2)
```

```text
true midpoint:                   1750000000
(low + high) // 2 in 32-bit ints: -397483648
low + (high - low) // 2:          1750000000
```

**2. Updating with `low = mid` instead of `mid + 1`.** `mid` was just examined and rejected; keeping it can leave the range unchanged forever.

**3. Mixing the two conventions.** Starting with `high = len(items)` (half-open) but looping with `while low <= high` (closed) lets `mid` reach `len(items)` and read past the end.

**4. Searching data that is not sorted.** Nothing warns you: the search silently returns wrong answers.

The block below runs the correct version and the two broken variants on every sorted list of 0 to 8 items with every target (90 searches), and shows the unsorted case:

```python
from collections import Counter

def search_with_low_equals_mid(items, target, guard=1_000):
    low, high = 0, len(items) - 1
    steps = 0
    while low <= high:
        steps += 1
        if steps > guard:
            return "hang"
        mid = low + (high - low) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            low = mid                                    # BUG: should be mid + 1
        else:
            high = mid - 1
    return -1

def search_with_mixed_bounds(items, target):
    low, high = 0, len(items)                            # BUG: half-open upper bound...
    while low <= high:                                   # ...with a closed-range loop
        mid = low + (high - low) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def outcomes(search):
    tally = Counter()
    for size in range(0, 9):
        items = [2 * i for i in range(size)]
        for target in range(-1, 2 * size + 1):
            expected = items.index(target) if target in items else -1
            try:
                answer = search(items, target)
            except IndexError:
                tally["IndexError"] += 1
                continue
            tally["hang" if answer == "hang" else "correct" if answer == expected else "wrong answer"] += 1
    return dict(tally)

print("correct version:        ", outcomes(binary_search))
print("low = mid:              ", outcomes(search_with_low_equals_mid))
print("mixed bounds:           ", outcomes(search_with_mixed_bounds))
print("unsorted list [5, 1, 4, 2, 3]: looking for 1 gives", binary_search([5, 1, 4, 2, 3], 1), "and for 3 gives", binary_search([5, 1, 4, 2, 3], 3))
```

```text
correct version:         {'correct': 90}
low = mid:               {'correct': 34, 'hang': 56}
mixed bounds:            {'IndexError': 18, 'correct': 72}
unsorted list [5, 1, 4, 2, 3]: looking for 1 gives -1 and for 3 gives -1
```

Most of the broken `low = mid` searches never finish, and the mixed-bounds version crashes whenever the target is larger than every item, and on the empty list. On the unsorted list, `1` and `3` are both in the list, yet the search reports `-1` for each.

## Common Mistakes

- **Forgetting that the list must be sorted** (in the same order the comparison assumes). Checking sortedness costs O(n), which defeats the purpose, so the precondition has to come from how the data is built.
- **Off-by-one errors** in the bounds and updates. Pick one convention — closed `[low, high]` with `while low <= high`, or half-open `[low, high)` with `while low < high` — and keep to it.
- **Slicing instead of indexing.** `binary_search(items[mid + 1:], target)` copies half the list at every step: the copies add up to about `n` items, turning an O(log n) search into O(n).
- **Assuming the returned index is the first (or last) occurrence.** With duplicates it is arbitrary; use `lower_bound` / `upper_bound`.
- **Using `(low + high) // 2` when porting the code to a language with fixed-size integers.**
- **Using binary search on a linked list.** Reaching the middle takes O(n) pointer hops, so each probe is expensive.
- **Doing a binary search on data you will search once.** If the list is unsorted and used once, a linear scan is cheaper than sorting first.

## ➡️ Next

Continue to [search-space-reduction.md](search-space-reduction.md): binary search is one instance of a much more general idea — find a property that lets you throw away a large part of the candidates at every step. The file applies it to rotated arrays, peaks, matrices, sorted pairs, unbounded lists, and evenly spread values.
