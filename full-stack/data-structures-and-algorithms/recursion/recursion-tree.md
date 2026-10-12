# 🌳 The Recursion Tree

## Draw the Calls, Then Read the Cost Off the Picture

A recursive function that calls itself once per level (like `factorial`) creates a chain of calls. A function that
calls itself **more than once** creates a *tree* of calls — and the shape of that tree explains both how it works and
what it costs. This file introduces the recursion tree and uses it for three jobs: seeing the order in which calls
happen, counting calls (time), and measuring the height (stack space).

Every number below was produced by running the code on CPython 3.9.

## 🖼️ Drawing the Calls

Draw one node per call. The original call is the **root**; each recursive call is a **child** of the call that made
it; the calls that hit a base case are the **leaves**. The easiest way to get the picture right is to have the function
print it, indenting by depth:

```python
def fib_tree(n, depth=0):
    print("  " * depth + f"fib({n})")
    if n < 2:
        return n
    return fib_tree(n - 1, depth + 1) + fib_tree(n - 2, depth + 1)

fib_tree(4)
```

```text
fib(4)
  fib(3)
    fib(2)
      fib(1)
      fib(0)
    fib(1)
  fib(2)
    fib(1)
    fib(0)
```

Read it top to bottom as the order in which the calls *start*. Each node's children are indented under it, left child
first (`n−1`, then `n−2`). In picture form:

```
                    fib(4)
                  /        \
             fib(3)          fib(2)
            /      \        /      \
        fib(2)    fib(1) fib(1)   fib(0)
        /     \
    fib(1)  fib(0)
```

Two facts jump out:

- **`fib(2)` is computed twice, and `fib(1)` three times.** The function has no memory, so the same subproblem is
  solved again and again. That repeated work is the whole story of why naive Fibonacci is slow.
- **At any moment only one root-to-node path is on the call stack.** While `fib(0)` (bottom left) runs, the stack holds
  `fib(4) → fib(3) → fib(2) → fib(0)`. The tree can be enormous, but the stack only ever holds one path.

## ⏱️ Time = Number of Calls

Each call does a constant amount of work besides its recursive calls, so the running time is proportional to the
**total number of nodes** in the tree. A counter shows how fast that grows:

```python
calls = 0

def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(f"{'n':>3} | {'fib(n)':>9} | {'calls':>9} | {'calls / previous':>16}")
previous = None
for n in (5, 10, 15, 20, 25, 30):
    calls = 0
    value = fib(n)
    ratio = "" if previous is None else f"{calls / previous:.2f}"
    print(f"{n:>3} | {value:>9,} | {calls:>9,} | {ratio:>16}")
    previous = calls
```

```text
  n |    fib(n) |     calls | calls / previous
  5 |         5 |        15 |                 
 10 |        55 |       177 |            11.80
 15 |       610 |     1,973 |            11.15
 20 |     6,765 |    21,891 |            11.10
 25 |    75,025 |   242,785 |            11.09
 30 |   832,040 | 2,692,537 |            11.09
```

Going from `n = 25` to `n = 30` multiplies the number of calls by about 11. The tree is not growing by a fixed
amount per level; each extra level multiplies its size. Looking at consecutive values of `n` shows the exact factor:

```python
counts = []
for n in range(20, 27):
    calls = 0
    fib(n)
    counts.append(calls)

print([round(counts[i + 1] / counts[i], 4) for i in range(len(counts) - 1)])
print(round((1 + 5 ** 0.5) / 2, 4))
```

```text
[1.6181, 1.6181, 1.618, 1.618, 1.618, 1.618]
1.618
```

Every extra `n` multiplies the number of calls by roughly **1.618** — the golden ratio. So the tree has about
1.618ⁿ nodes: **exponential time**, written O(φⁿ), or loosely O(2ⁿ) as an upper bound. A tree that doubles with each
level would grow even faster; this one grows slightly less than doubling because the right child (`n−2`) is a
shallower subtree than the left one (`n−1`).

## 📏 Space = Height of the Tree

Because the stack holds one root-to-node path, the **stack space is the height of the tree**. For `fib(n)` the longest
path is the all-left path `fib(n) → fib(n−1) → … → fib(1)`, which is `n` levels deep: **O(n) space**, even though the
time is exponential.

| Recursion | Tree shape | Calls (time) | Height (stack space) |
|-----------|-----------|--------------|----------------------|
| `factorial(n)` | A single chain | n + 1 | n + 1 |
| Binary search | A single chain that halves the range | about log₂ n | about log₂ n |
| Naive `fib(n)` | Lopsided binary tree | about φⁿ | n |
| Subsets of `n` items (include or skip each) | Complete binary tree | 2ⁿ⁺¹ − 1 | n + 1 |
| Merge sort on `n` items | Balanced binary tree | about 2n | about log₂ n |

## 📊 The Level-by-Level Method

For recursions that split a problem into equal parts, add up the work **level by level** and multiply by the number
of levels. Merge sort is the standard example: split a list in half, sort each half recursively, then merge the two
sorted halves.

```python
import random

def merge_sort(items, stats):
    if len(items) <= 1:                       # base case: 0 or 1 elements is already sorted
        return items
    middle = len(items) // 2
    left = merge_sort(items[:middle], stats)
    right = merge_sort(items[middle:], stats)
    return merge(left, right, stats)

def merge(left, right, stats):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        stats["comparisons"] += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

random.seed(4)
print(f"{'n':>6} | {'comparisons':>11} | {'n * log2(n)':>11}")
for n in (8, 64, 512, 4096):
    data = [random.randint(0, 10**6) for _ in range(n)]
    stats = {"comparisons": 0}
    result = merge_sort(data, stats)
    assert result == sorted(data)
    print(f"{n:>6,} | {stats['comparisons']:>11,} | {n * (n.bit_length() - 1):>11,}")
```

```text
     n | comparisons | n * log2(n)
     8 |          16 |          24
    64 |         296 |         384
   512 |       3,959 |       4,608
 4,096 |      44,007 |      49,152
```

(For a power of two, `n.bit_length() - 1` is exactly log₂ n, so the last column is `n·log₂ n`.) Why does the count
track `n log n`? Look at the tree level by level for `n = 8`:

```
level 0:  [8 items]                              1 merge of size 8  -> about 8 units of work
level 1:  [4]            [4]                     2 merges of size 4 -> about 8 units
level 2:  [2]   [2]      [2]   [2]               4 merges of size 2 -> about 8 units
level 3:  [1][1][1][1]   [1][1][1][1]            leaves, no merge work
```

Every level does about `n` units of work in total (the sizes add up to `n`), and halving `n` repeatedly takes
`log₂ n` levels. Total work: `n × log₂ n`, or **O(n log n)**. The list is split into halves, so the tree is only
`log₂ n` deep — the stack space is small (though this version also builds new lists, so it uses O(n) extra memory
for them).

The same level-by-level reasoning gives the other common recurrences:

| Recurrence | Meaning | Total | Example |
|------------|---------|-------|---------|
| T(n) = T(n−1) + O(1) | One call, problem shrinks by 1 | O(n) | `factorial`, `total` |
| T(n) = T(n−1) + O(n) | One call, O(n) work each (for example copying a slice) | O(n²) | `total_by_slicing` |
| T(n) = T(n/2) + O(1) | One call, problem halves | O(log n) | Binary search |
| T(n) = 2T(n/2) + O(n) | Two half-size calls, linear merge work | O(n log n) | Merge sort |
| T(n) = 2T(n−1) + O(1) | Two calls on a problem one smaller | O(2ⁿ) | Subsets, Tower of Hanoi |
| T(n) = T(n−1) + T(n−2) + O(1) | Two overlapping calls | O(φⁿ) | Naive Fibonacci |

For divide-and-conquer recurrences of the form T(n) = aT(n/b) + f(n) there is a general shortcut, the **master
theorem** ([Wikipedia: Master theorem](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms))); the
level-by-level picture is what it formalizes.

## ✂️ Pruning the Tree: Memoization

Naive Fibonacci is slow because the same subtrees appear repeatedly. If the function **remembers** answers it has
already computed, each distinct subproblem is solved once and every repeated call becomes an instant lookup. Python's
`functools.lru_cache` does this with a decorator:

```python
import functools

body_runs = 0

@functools.lru_cache(maxsize=None)
def fib_memo(n):
    global body_runs
    body_runs += 1
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

print(fib_memo(30))              # 832040
print(body_runs)                 # 31
print(fib_memo.cache_info())     # CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
print(fib_memo(90))              # 2880067194370816120
```

The function body ran only **31 times** for `fib_memo(30)` — once for each value from `0` to `30` — compared with
2,692,537 calls without the cache. The exponential tree collapsed into a single chain, which is why `fib_memo(90)`
returns instantly although the naive version would need on the order of 10¹⁹ calls for the same answer. The cost is
**memory**: the cache holds one entry per distinct argument (O(n) here).

This idea — *spot repeated subproblems and store their answers* — is the core of the Dynamic Programming module later in
this domain. Seeing it in the recursion tree is the best way to recognize when it applies: if the same node appears
in several places, cache it.

## 🔍 Using the Tree on a New Problem

When you meet a recursive function, ask four questions about its tree:

1. **How many children does each node have?** One → a chain; two → a binary tree.
2. **How much does the problem shrink?** By a constant (depth ≈ n) or by a fraction (depth ≈ log n).
3. **How much work happens at each node, besides the calls?** That multiplies the node count.
4. **Do the same subproblems appear more than once?** If so, memoization may collapse the tree.

## Common Mistakes

- **Assuming time and space are the same thing.** Naive Fibonacci takes exponential *time* but only linear *stack space*.
- **Counting only the leaves, or only one level**, instead of every node.
- **Forgetting the work done at each node** (such as the merge in merge sort or a slice copy) when estimating cost.
- **Treating `O(2ⁿ)` and `O(φⁿ)` as interchangeable in an exact answer** — `2ⁿ` is a valid upper bound for naive Fibonacci,
  but `φⁿ` is tighter.
- **Memoizing functions that are not pure** (their result depends on something other than the arguments).
- **Missing that `lru_cache` needs hashable arguments** (lists cannot be passed as cached arguments).

## ➡️ Next

Continue to [recursive-problem-solving.md](recursive-problem-solving.md) to apply the checklist, the base-case
discipline, and the tree-reading skills to a set of classic problems: fast exponentiation, subsets, permutations,
Tower of Hanoi, and more.
