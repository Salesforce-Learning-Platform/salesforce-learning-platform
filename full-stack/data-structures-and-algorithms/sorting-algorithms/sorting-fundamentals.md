# 🔀 Sorting Fundamentals

## Putting Things in Order — and Why It Is Worth Studying

Sorting is one of the most common things programs do, and one of the most useful: a sorted list can be searched in O(log n) by binary search, merged
with another sorted list in a single pass, scanned for duplicates by comparing neighbours, and presented to a person in a readable order. Many problems that look unrelated — finding the median, grouping
equal items, scheduling intervals, matching two lists — become easy *after* a sort.

It is also the best place to learn how to compare algorithms. Dozens of sorting methods exist, each with a different mix of speed, memory use, and behaviour on special inputs, and the differences between
them illustrate almost every idea from the [complexity module](../time-and-space-complexity/big-o-notation.md). This module studies the algorithms interviews and real libraries depend on: the simple quadratic
sorts, merge sort, quick sort, heap sort, and cyclic sort, and it closes with counting sort, radix sort, and a measured guide to choosing between them. This first file builds the vocabulary, explains **stability**, shows what Python's built-in sort promises, proves (and measures) the limit on how fast any
comparison-based sort can be, and provides the test harness used for every algorithm in the module. All outputs were produced by running the code on CPython 3.9.

## 📖 The Vocabulary

| Term | Meaning | Why it matters |
|------|---------|----------------|
| **Comparison sort** | Decides order only by asking "is `a` before `b`?" | The most general kind; has a hard speed limit (see below) |
| **Stable** | Items with equal keys keep their original relative order | Essential when sorting by several keys in turn |
| **In-place** | Uses O(1) (or O(log n)) extra memory beyond the input | Matters for large data |
| **Adaptive** | Runs faster when the input is already (nearly) sorted | Real data is often partly ordered |
| **Internal / external** | Data fits in memory / must be sorted on disk in pieces | Different algorithms suit each |
| **Key** | The value a record is sorted by (a name, a date, a score) | Python's `key=` parameter |

## ⚖️ Stability

Suppose a class list is sorted alphabetically, and you then sort it by score. Students with the same score should stay in alphabetical order — that is what a **stable** sort guarantees: *if two items compare equal,
their relative order in the output is the same as in the input.*

```python
records = [("Ana", 90), ("Ben", 85), ("Cara", 90), ("Dev", 85), ("Eli", 90)]        # already in alphabetical order

by_score = sorted(records, key=lambda r: r[1], reverse=True)
print(by_score)
# [('Ana', 90), ('Cara', 90), ('Eli', 90), ('Ben', 85), ('Dev', 85)]
```

Within each score, the names are still alphabetical. Python's `sorted` and `list.sort` are guaranteed stable (the Sorting HOWTO in the Python documentation says so explicitly), and `reverse=True` keeps that guarantee —
equal items still come out in their *original* order, not reversed. Reversing a sorted list afterwards does *not*:

```python
from operator import itemgetter

ties = [("a", 1), ("b", 1), ("c", 2)]
print(sorted(ties, key=itemgetter(1), reverse=True))        # [('c', 2), ('a', 1), ('b', 1)]   — a still before b
print(sorted(ties, key=itemgetter(1))[::-1])                # [('c', 2), ('b', 1), ('a', 1)]   — the tie was reversed too
```

### An Unstable Algorithm

Not every sort is stable. **Selection sort** (next file) repeatedly swaps the smallest remaining item into position, and those swaps can leap over equal items:

```python
def selection_sort_by(items, key):
    items = list(items)
    for i in range(len(items) - 1):
        smallest = min(range(i, len(items)), key=lambda j: key(items[j]))
        items[i], items[smallest] = items[smallest], items[i]        # a long-distance swap: this is what breaks stability
    return items

pairs = [("a", 2), ("b", 2), ("c", 1)]
print(selection_sort_by(pairs, key=lambda p: p[1]))        # [('c', 1), ('b', 2), ('a', 2)]   — a and b swapped places
print(sorted(pairs, key=lambda p: p[1]))                    # [('c', 1), ('a', 2), ('b', 2)]
```

Moving `c` to the front swapped it with `a`, which carried `a` behind `b`. Both outputs are correctly sorted by score; only the second respects the original order of the ties.

### Why Stability Matters: Sorting by Several Keys

Stability lets you sort by multiple criteria with **successive sorts**: sort by the *least* important key first, then by the most important. Each later sort leaves earlier ordering intact among ties.

```python
people = [("Lee", "Ben"), ("Kim", "Cara"), ("Lee", "Ana"), ("Kim", "Dev")]           # (last name, first name)
by_first = sorted(people, key=lambda p: p[1])                                         # least important key first
by_last_then_first = sorted(by_first, key=lambda p: p[0])                             # then the most important key
print(by_last_then_first)       # [('Kim', 'Cara'), ('Kim', 'Dev'), ('Lee', 'Ana'), ('Lee', 'Ben')]
print(by_last_then_first == sorted(people))                                           # True   — comparing tuples does both at once
```

This only works because the second sort is stable. (Python's tuple comparison is the shortcut when all keys sort in the same direction; successive stable sorts handle *mixed* directions, such as "last name ascending,
score descending".)

## 🐍 Python's Built-In Sort

In practice you will almost always use Python's own sort:

```python
numbers = [3, 1, 2]
print(sorted(numbers), numbers)             # [1, 2, 3] [3, 1, 2]    — sorted() returns a NEW list
print(numbers.sort(), numbers)              # None [1, 2, 3]         — list.sort() sorts IN PLACE and returns None

words = ["banana", "kiwi", "Apple", "fig"]
print(sorted(words))                        # ['Apple', 'banana', 'fig', 'kiwi']    — uppercase letters sort before lowercase
print(sorted(words, key=str.lower))         # ['Apple', 'banana', 'fig', 'kiwi']    — compare case-insensitively
print(sorted(words, key=len))               # ['fig', 'kiwi', 'Apple', 'banana']    — by length; ties keep input order
```

The `key` argument is a function applied **once per item**; items are then compared by their keys. (If all you have is a two-argument comparison function, `functools.cmp_to_key` wraps it into a key function.) The algorithm is **Timsort**, which the CPython source describes as "an adaptive, stable, natural mergesort": it finds runs of already-ordered items in the input, extends short
runs with binary insertion sort, and merges runs. It does O(n log n) work in the worst case but needs far fewer comparisons on data that already has some order. In an interview you may be asked to implement a sort
yourself; in production code, use `sorted`.

## 🧱 How Fast Can a Comparison Sort Be? A Hard Limit

Merge sort and quick sort take O(n log n) time. Is there a faster comparison sort waiting to be discovered? **No** — and the argument is short enough to follow.

Think of the algorithm as a game of twenty questions. Each comparison is a yes/no question. Before any comparison, the input could be *any* of the `n!` possible orderings of `n` distinct items. The algorithm must end by knowing
which ordering it was given. Each yes/no answer can at best cut the remaining possibilities in half, so after `k` comparisons at most `2^k` orderings can be told apart. To distinguish `n!` orderings it needs
`2^k ≥ n!`, that is:

> **Every comparison sort needs at least ⌈log₂(n!)⌉ comparisons in the worst case.**

By Stirling's approximation, `log₂(n!) ≈ n log₂ n − 1.44 n`, which is Θ(n log n). So no comparison sort can beat O(n log n) in the worst case: merge sort and heap sort are optimal.

For tiny inputs the bound can be checked exhaustively. The search below plays out every possible strategy for sorting `n` items — at each step it considers every comparison, assuming the *worst* answer — and
reports the smallest number of comparisons that always suffices:

```python
import itertools
import math
from functools import lru_cache

def min_comparisons(n):
    """The fewest comparisons that ALWAYS suffice to sort n distinct items, found by exhaustive search of every strategy."""
    @lru_cache(maxsize=None)
    def solve(possible):                          # `possible`: the orderings still consistent with all answers so far
        if len(possible) == 1:
            return 0                              # only one ordering left: sorted
        best = None
        for i, j in itertools.combinations(range(n), 2):
            if_less = frozenset(p for p in possible if p[i] < p[j])           # orderings in which item i < item j
            if not if_less or len(if_less) == len(possible):
                continue                          # this comparison tells us nothing new
            cost = 1 + max(solve(if_less), solve(possible - if_less))         # the adversary picks the worse answer
            if best is None or cost < best:
                best = cost
        return best

    return solve(frozenset(itertools.permutations(range(n))))

print(f"{'n':>2} | {'orderings (n!)':>14} | {'best possible worst case':>24} | {'ceil(log2(n!))':>14}")
for n in range(1, 6):
    print(f"{n:>2} | {math.factorial(n):>14} | {min_comparisons(n):>24} | {math.ceil(math.log2(math.factorial(n))):>14}")
```

```text
 n | orderings (n!) | best possible worst case | ceil(log2(n!))
 1 |              1 |                        0 |              0
 2 |              2 |                        1 |              1
 3 |              6 |                        3 |              3
 4 |             24 |                        5 |              5
 5 |            120 |                        7 |              7
```

For `n` from 1 to 5, the true minimum equals the counting bound exactly: 0, 1, 3, 5, 7 comparisons. (For larger `n` the true minimum can be slightly above `⌈log₂ n!⌉`, and finding it is hard;
the bound is a floor that no algorithm can go under.)

### How Close Does Python's Sort Get?

The same idea can be measured on real sorts. Wrapping the items in a class that counts every `<` comparison shows how many comparisons Python's `sorted` actually uses:

```python
import random

class Counted:
    count = 0
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.count += 1
        return self.value < other.value

def comparisons_used(values):
    items = [Counted(v) for v in values]
    Counted.count = 0
    sorted(items)
    return Counted.count

def lower_bound(n):
    return math.ceil(sum(math.log2(k) for k in range(2, n + 1)))      # ceil(log2(n!))

def stirling(n):                                                      # n·log2(n) − n·log2(e) + ½·log2(2πn)
    return n * math.log2(n) - n * math.log2(math.e) + 0.5 * math.log2(2 * math.pi * n)

random.seed(1)
print(f"{'n':>8} | {'ceil(log2 n!)':>13} | {'Stirling':>9} | {'sorted(random)':>14} | {'sorted(ascending)':>17} | {'sorted(descending)':>18}")
for n in (10, 100, 1_000, 10_000, 100_000):
    trials = 20 if n <= 10_000 else 3
    average = sum(comparisons_used(random.sample(range(10 * n), n)) for _ in range(trials)) / trials
    print(f"{n:>8,} | {lower_bound(n):>13,} | {stirling(n):>9,.0f} | {average:>14,.0f} | "
          f"{comparisons_used(range(n)):>17,} | {comparisons_used(range(n, 0, -1)):>18,}")
```

```text
       n | ceil(log2 n!) |  Stirling | sorted(random) | sorted(ascending) | sorted(descending)
      10 |            22 |        22 |             23 |                 9 |                  9
     100 |           525 |       525 |            534 |                99 |                 99
   1,000 |         8,530 |     8,529 |          8,634 |               999 |                999
  10,000 |       118,459 |   118,458 |        119,918 |             9,999 |              9,999
 100,000 |     1,516,705 | 1,516,704 |      1,529,261 |            99,999 |             99,999
```

Three observations. Stirling's formula tracks the exact bound closely. On **random** input Python's sort uses only about 1–2% more comparisons than the theoretical minimum — it is nearly perfect. And on input that is already
ascending or descending it uses just `n − 1` comparisons: it notices the existing order in one pass (this is what *adaptive* means), so sorted data is the best case rather than a bad one.

## 🚀 Beyond Comparisons

The `n log n` limit applies only to algorithms that learn about the data *solely through comparisons*. If you know something more — for example, that the values are integers from 1 to `n` — you can do better.
**Cyclic sort** in [cyclic-sort.md](cyclic-sort.md), and **counting sort** and **radix sort** in [choosing-a-sorting-algorithm.md](choosing-a-sorting-algorithm.md), sort in O(n) time (or close to it) by using the values themselves as positions. The price is the extra knowledge about the data.

## ✅ A Test Harness for Every Sort in This Module

Sorting algorithms are easy to get subtly wrong: an off-by-one that only matters for a list of two equal items, or a swap that breaks stability. Every algorithm in this module is checked by the same function. It takes
a sort function `sort(items, key)` that must return a **new** sorted list without changing its input, runs it on hundreds of random lists (including many duplicates), and reports two things: whether the result is
correctly sorted, and whether it is *stable* (identical to Python's stable sort when the key is only part of each record):

```python
def check_sort(sort_function, trials=300):
    """Return (correct, stable) for sort_function(items, key) -> a new sorted list."""
    random.seed(0)
    correct = stable = True
    for _ in range(trials):
        keys = [random.randint(0, 5) for _ in range(random.randint(0, 20))]       # few distinct keys: many ties
        records = [(k, position) for position, k in enumerate(keys)]              # (key, original position)
        original = list(records)
        result = sort_function(records, key=lambda r: r[0])
        if records != original:                                                    # the input must not be modified
            correct = False
        if [r[0] for r in result] != sorted(keys):
            correct = False
        if result != sorted(original, key=lambda r: r[0]):                         # same order as Python's stable sort?
            stable = False
    return correct, stable

print("Python's sorted():", check_sort(lambda items, key: sorted(items, key=key)))      # (True, True)
print("selection sort    :", check_sort(selection_sort_by))                             # (True, False)
```

The harness classifies `sorted` as correct and stable and selection sort as correct but **not** stable — confirming what the example above showed, now on hundreds of random inputs. Later files reuse this function
(redefined at the top of each file so that every file runs on its own).

## ⏱️ What to Remember

| Fact | Detail |
|------|--------|
| Comparison-sort speed limit | At least ⌈log₂(n!)⌉ ≈ n log₂ n − 1.44 n comparisons in the worst case |
| Python's `sorted` / `list.sort` | Timsort: stable, adaptive, O(n log n) worst case, n − 1 comparisons on sorted input |
| `sorted` vs `.sort()` | New list vs in place (returns `None`) |
| Stability | Needed for multi-key sorting by successive passes (least important key first) |
| `reverse=True` | Preserves stability; `sorted(x)[::-1]` does not |

## Common Mistakes

- **Using the return value of `list.sort()`**: it returns `None`, so `ordered = items.sort()` loses the list.
- **Sorting mixed types**: `sorted([3, "a"])` raises `TypeError` in Python 3 because `int` and `str` cannot be compared.
- **Forgetting that uppercase sorts before lowercase** in plain string sorts; use `key=str.lower` or `str.casefold` for case-insensitive order.
- **Assuming any algorithm is stable** — selection sort and quick sort are not (unless specially built).
- **Sorting in the wrong order for multi-key sorts**: the most important key must be sorted **last**.
- **Claiming a comparison sort can run in O(n)** in the general case — the decision-tree argument rules it out.

## ➡️ Next

Continue to [elementary-sorts.md](elementary-sorts.md) for the three simple O(n²) sorts — bubble, selection, and insertion — what each one costs, and why insertion sort is still used inside real libraries.
