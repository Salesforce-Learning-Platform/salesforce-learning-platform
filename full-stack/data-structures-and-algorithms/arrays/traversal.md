# 🔁 Traversal

## Visiting Every Element Exactly Once

**Traversal** means walking through an array and doing something with each element. It is the
operation underneath summing, counting, finding a maximum, filtering, and — with an early exit —
searching. [array-fundamentals.md](array-fundamentals.md) showed that reaching *one* element by
index is O(1); traversal does that `n` times, so it costs **O(n) time**. Because it only needs a
loop counter and perhaps one running value, its extra space is **O(1)**
(see [space-complexity.md](../time-and-space-complexity/space-complexity.md)).

## ➡️ The Four Common Directions

```python
scores = [72, 95, 88, 61, 79]

# 1. Forward, by value — when the position doesn't matter
for score in scores:
    print(score)

# 2. Forward, by index and value — when the position matters
for i, score in enumerate(scores):
    print(i, score)

# 3. Backward — start at the last valid index (len - 1) and stop after 0
for i in range(len(scores) - 1, -1, -1):
    print(i, scores[i])          # visits 79, 61, 88, 95, 72

# 4. Every other element — step by 2
for i in range(0, len(scores), 2):
    print(scores[i])             # visits 72, 88, 79
```

Prefer the simplest form that works: reach for the index only when the position is genuinely part of
the answer. (Slicing such as `scores[::2]` also works, but it builds a new list first — O(n) extra
space — whereas the `range` form allocates nothing.)

## 🔎 Traversal in Practice: Finding a Maximum

```python
def find_max(items):
    best = items[0]
    for x in items[1:]:
        if x > best:
            best = x
    return best

find_max([72, 95, 88, 61, 79])   # 95
```

One pass, one extra variable: O(n) time, O(1) space. (`items[1:]` copies the list; for large input,
iterate by index from 1 to avoid that copy — or simply use the built-in `max`, which is also a
single O(n) traversal.) This is the same shape as `linear_search` in
[what-are-algorithms.md](../introduction-to-data-structures-and-algorithms/what-are-algorithms.md):
search is just a traversal that stops early.

## ⏹️ Stopping Early

```python
def contains_negative(items):
    for x in items:
        if x < 0:
            return True          # found one — no need to look further
    return False
```

The worst case is still O(n) (no negatives at all, so every element is checked), but the best case
is O(1). As [analyzing-algorithms.md](../time-and-space-complexity/analyzing-algorithms.md)
explains, Big-O conventionally reports the worst case.

## 🧮 Two-Dimensional Arrays

A grid is an array of arrays, traversed with two nested loops:

```python
grid = [
    [1,  2,  3,  4],
    [5,  6,  7,  8],
    [9, 10, 11, 12],
]

row_sums = [sum(row) for row in grid]
col_sums = [sum(grid[r][c] for r in range(len(grid))) for c in range(len(grid[0]))]

print(row_sums)   # [10, 26, 42]
print(col_sums)   # [15, 18, 21, 24]
```

The loops are nested, but that does **not** make this O(n²) in the sense of
[big-o-notation.md](../time-and-space-complexity/big-o-notation.md). The two loops range over
*different* dimensions, so the work is rows × columns — exactly the number of cells. If `n` counts
the cells, traversal is O(n); if you name the dimensions separately, it is O(rows × cols), the same
"keep the sizes separate" habit used for `n * m` in
[analyzing-algorithms.md](../time-and-space-complexity/analyzing-algorithms.md).

## ⚠️ Changing an Array While Traversing It

Removing elements from a list *during* a `for` loop over that same list is one of the most common
traversal bugs. Each removal shifts later elements one slot left, but the loop's internal position
still moves forward — so the element that slid into the current slot is skipped:

```python
numbers = [0, 0, 1, 0, 2]
for n in numbers:
    if n == 0:
        numbers.remove(n)

print(numbers)   # [1, 0, 2]  — a zero survived
```

Three safe alternatives:

```python
numbers = [0, 0, 1, 0, 2]

# 1. Build a new list (clearest; O(n) extra space)
cleaned = [n for n in numbers if n != 0]            # [1, 2]

# 2. Delete in place, walking BACKWARD so shifts never affect unvisited indexes
for i in range(len(numbers) - 1, -1, -1):
    if numbers[i] == 0:
        del numbers[i]                               # numbers is now [1, 2]
```

A third option — a reader/writer pair of indexes that compacts the array in a single pass with
O(1) extra space — is the subject of [two-pointer-technique.md](two-pointer-technique.md).

Also remember that the loop variable is a *name bound to each element*, not the slot itself:

```python
vals = [1, 2, 3]
for v in vals:
    v *= 2          # rebinds the local name `v`; the list is untouched
print(vals)         # [1, 2, 3]
```

To change elements in place, assign through the index: `vals[i] = vals[i] * 2`.

## 🌀 A Note on Recursion

Any traversal can also be written recursively. It still does O(n) work, but each call adds a frame
to the call stack, so it uses O(n) space instead of O(1) — the
[recursive call-stack cost](../time-and-space-complexity/space-complexity.md) described earlier.
The Recursion module, later in this domain, returns to this trade-off.

## Common Mistakes

- **Removing or inserting while looping over the same list**, which skips or repeats elements.
- **Using `range(len(items))` when the index isn't needed**, adding noise and a chance for
  off-by-one errors — iterate by value instead.
- **Off-by-one in backward loops** — the range `range(n - 1, -1, -1)` starts at the last valid
  index and stops *after* 0; writing `-0` or `0` as the stop value skips index 0.
- **Copying the array without noticing** — slices like `items[1:]` allocate a new list, changing a
  traversal's space cost from O(1) to O(n).
- **Assuming nested loops are always O(n²)** — they multiply the *sizes they range over*; a
  rows × columns grid is linear in its cell count.

## ➡️ Next

Continue to [insertion-and-deletion.md](insertion-and-deletion.md) to see why adding or removing an
element costs very different amounts depending on *where* in the array it happens.
