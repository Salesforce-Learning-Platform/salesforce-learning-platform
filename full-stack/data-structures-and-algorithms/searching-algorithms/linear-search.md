# 🔎 Linear Search

## Look at Every Item Until You Find It

**Linear search** (also called sequential search) is the simplest way to find something: start at the first item, compare it with the target, and move along until you find a match or run out of items. It needs no preparation, makes no assumptions about the order of the data, and works on anything you can walk through one item at a time — lists, strings, files, linked lists, database rows, a stream of events.

That generality is its strength, and its cost is time: in the worst case every item is examined, so the work grows in direct proportion to `n`. Every faster search in this module — starting with [binary search](binary-search.md) — buys speed by requiring something extra from the data (usually that it is sorted). This file shows what linear search costs, how Python's built-in tools do it faster than hand-written loops, when it is genuinely the right choice, and the two situations where it silently turns a program quadratic. All outputs were produced by running the code on CPython 3.9.

## 🧱 The Algorithm

```python
def linear_search(items, target):
    """Return the index of the first item equal to target, or -1."""
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1

def find_first(items, predicate):
    """Return the index of the first item for which predicate(item) is true, or -1."""
    for index, item in enumerate(items):
        if predicate(item):
            return index
    return -1

def find_last(items, target):
    for index in range(len(items) - 1, -1, -1):
        if items[index] == target:
            return index
    return -1

def find_all(items, target):
    return [index for index, item in enumerate(items) if item == target]

colors = ["red", "green", "blue", "green", "yellow"]
print(linear_search(colors, "green"))                           # 1
print(find_last(colors, "green"))                               # 3
print(find_all(colors, "green"))                                # [1, 3]
print(linear_search(colors, "purple"))                          # -1
print(find_first([3, 8, 12, 5, 20], lambda x: x > 10))          # 2
```

Notice the pattern: loop, test, return early on a match, and return a sentinel value (`-1`) only after the loop has looked at everything. `find_first` shows that "search" does not have to mean "equal to a value": any yes/no question about an item (greater than 10, starts with "A", is overdue) can drive the same loop. Finding the largest or smallest item is the same scan with a running best instead of an early exit.

## 📊 What It Costs

To count work precisely, wrap the values in a class that counts how many times `==` is evaluated:

```python
class Counted:
    count = 0
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        Counted.count += 1
        return self.value == other.value

n = 1_000
items = [Counted(v) for v in range(n)]

def comparisons_to_find(target):
    Counted.count = 0
    linear_search(items, Counted(target))
    return Counted.count

per_target = [comparisons_to_find(t) for t in range(n)]
print(f"target is the first item : {per_target[0]:>5} comparison")
print(f"target is the last item  : {per_target[-1]:>5} comparisons")
print(f"average over all {n:,} present targets: {sum(per_target) / n:.1f}   ((n + 1) / 2 = {(n + 1) / 2})")
print(f"target is absent         : {comparisons_to_find(-1):>5} comparisons")
```

```text
target is the first item :     1 comparison
target is the last item  :  1000 comparisons
average over all 1,000 present targets: 500.5   ((n + 1) / 2 = 500.5)
target is absent         :  1000 comparisons
```

| Case | Comparisons | Time |
|------|-------------|------|
| Best: target is the first item | 1 | O(1) |
| Average: target equally likely at any position | (n + 1) / 2 | O(n) |
| Worst: target is last, or absent | n | O(n) |

Two details matter in practice. First, an **unsuccessful** search is always the worst case: the only way to be sure that something is not there is to look at everything. Second, the average case is still *linear*: halving the work is a constant factor, not a better growth rate. A million-item list needs about half a million comparisons on average.

Space is O(1): only an index is kept.

## 🐍 Python's Built-In Linear Searches

Python already provides linear search as built-in operations, all implemented in C:

```python
numbers = [4, 8, 15, 16, 23, 42, 8]
print(15 in numbers, 99 in numbers)                             # True False
print(numbers.index(8))                                         # 1
try:
    numbers.index(99)
except ValueError as error:
    print(error)                                                # 99 is not in list
print(numbers.index(8, 2))                                      # 6
print(numbers.count(8))                                         # 2
print(any(n > 40 for n in numbers))                             # True
print(next((i for i, n in enumerate(numbers) if n > 20), -1))   # 4
```

- `x in seq` answers yes/no; `seq.index(x)` returns the position of the first match (and raises `ValueError` when there is none; the optional second argument starts the search later, which is how you find the next occurrence).
- `seq.count(x)` always scans the whole list.
- `any(...)` / `all(...)` stop at the first item that settles the answer.
- `next(generator, default)` is the idiomatic "first item satisfying a condition", with a default instead of an exception.

How much faster are the built-ins than a hand-written loop? Two more hand-written variants are needed for the comparison. A `while` loop with an explicit index is how the algorithm is written in many languages. The **sentinel** version avoids testing the index on every step by temporarily writing the target into the last slot, so the loop is guaranteed to stop:

```python
import random

def linear_search_while(items, target):
    i = 0
    while i < len(items):
        if items[i] == target:
            return i
        i += 1
    return -1

def sentinel_search(items, target):
    last = items[-1]
    items[-1] = target                      # the sentinel guarantees the loop below stops
    i = 0
    while items[i] != target:
        i += 1
    items[-1] = last                        # restore the original last item
    if i < len(items) - 1 or last == target:
        return i
    return -1

print(sentinel_search([4, 8, 15, 16], 15), sentinel_search([4, 8, 15, 16], 99), sentinel_search([4, 8, 15, 16], 16))       # 2 -1 3
```

Now the worst case, a target in the last position of a 100,000-item list, searched with three hand-written loops and the two built-ins (best of three runs, in milliseconds):

```python
import timeit

random.seed(1)
n = 100_000
data = random.sample(range(10 * n), n)
target = data[-1]                           # the worst case: the last position
copy_for_sentinel = list(data)

def best_ms(function, number=5):
    return min(timeit.repeat(function, number=number, repeat=3)) / number * 1000

assert linear_search(data, target) == linear_search_while(data, target) == sentinel_search(copy_for_sentinel, target) == data.index(target) == n - 1
for label, function in [("for loop with enumerate", lambda: linear_search(data, target)),
                        ("while loop with an index", lambda: linear_search_while(data, target)),
                        ("sentinel version", lambda: sentinel_search(copy_for_sentinel, target)),
                        ("list.index", lambda: data.index(target)),
                        ("x in list", lambda: target in data)]:
    print(f"{label:>26}: {best_ms(function):7.3f} ms")
```

Output:

```
   for loop with enumerate:   4.127 ms
  while loop with an index:  11.365 ms
          sentinel version:   5.310 ms
                list.index:   0.932 ms
                 x in list:   0.848 ms
```

Three lessons. The `enumerate` loop is two to three times faster than the index-and-compare `while` loop, because the interpreter does less work per item. The sentinel trick, which saves a comparison per step in languages like C, brings no gain in Python (here it was even a little slower than the `enumerate` loop), where each step costs far more than one comparison. And the built-ins are four to five times faster than the best loop written in Python: the same O(n) algorithm, but the loop runs in compiled code. The exact numbers depend on the machine and the run; the ordering does not. **When Python already has a built-in for the search you need, use it.**

## ⚖️ When Linear Search Is the Right Tool — and When It Is a Trap

Linear search is the right choice when:

- **The data is unsorted and you search it once or twice.** Sorting first costs O(n log n), more than the search itself.
- **The list is small.** Under a few dozen items, the overhead of anything cleverer does not pay off.
- **There is no random access.** A [linked list](../linked-lists/README.md) or a generator can only be walked from the front; binary search needs to jump to the middle.
- **The question is a predicate**, not equality with a key ("first order over $500"), and no index on that predicate exists.

It becomes a trap when the same data is searched **many times**. The next block measures, for a list of 100,000 numbers, what one linear search costs on average and what the alternatives cost to set up and to use:

```python
import bisect

random.seed(7)
n = 100_000
data = random.sample(range(10 * n), n)
queries = random.sample(data, 100)                     # targets at random positions: about half the list is scanned

t_linear = sum(timeit.timeit(lambda q=q: q in data, number=3) / 3 for q in queries) / len(queries) * 1000
t_sort = min(timeit.repeat(lambda: sorted(data), number=1, repeat=5)) * 1000
ordered = sorted(data)
def found_by_bisect(q):
    i = bisect.bisect_left(ordered, q)
    return i < len(ordered) and ordered[i] == q
t_bisect = sum(timeit.timeit(lambda q=q: found_by_bisect(q), number=50) / 50 for q in queries) / len(queries) * 1000
t_set_build = min(timeit.repeat(lambda: set(data), number=1, repeat=5)) * 1000
lookup_set = set(data)
t_set = sum(timeit.timeit(lambda q=q: q in lookup_set, number=200) / 200 for q in queries) / len(queries) * 1000

print(f"one linear search (list, `in`):        {t_linear:8.4f} ms each")
print(f"sort once: {t_sort:6.2f} ms   then one bisect search:  {t_bisect * 1000:8.3f} us each")
print(f"build a set once: {t_set_build:6.2f} ms   then one lookup: {t_set * 1000:8.3f} us each")
print(f"sorting pays for itself after about {t_sort / (t_linear - t_bisect):.0f} searches; building a set, after about {t_set_build / (t_linear - t_set):.0f}")
```

Output:

```
one linear search (list, `in`):          0.4704 ms each
sort once:  11.79 ms   then one bisect search:     0.329 us each
build a set once:   2.86 ms   then one lookup:    0.052 us each
sorting pays for itself after about 25 searches; building a set, after about 6
```

For a list that will be searched more than a couple of dozen times, preparing the data wins quickly: a sorted list with [binary search](binary-search.md) is more than a thousand times faster per query (0.47 ms versus 0.33 µs here), and a set (a [hash table](../hashing/README.md)) faster still, when only membership matters.

The most common trap is the **accidental quadratic**: a membership test on a *list* inside a loop. Each `x in big_list` is a hidden linear search, so the loop is O(n × m):

```python
random.seed(2)
allowed = random.sample(range(1_000_000), 5_000)
requests = random.sample(range(1_000_000), 5_000) + allowed[:2_000]

t_list = min(timeit.repeat(lambda: [x for x in requests if x in allowed], number=1, repeat=3)) * 1000
allowed_set = set(allowed)
t_set_loop = min(timeit.repeat(lambda: [x for x in requests if x in allowed_set], number=1, repeat=3)) * 1000
same = [x for x in requests if x in allowed] == [x for x in requests if x in allowed_set]
print(f"7,000 membership tests against a list of 5,000: {t_list:8.2f} ms")
print(f"the same tests against a set:                   {t_set_loop:8.3f} ms   (same answers: {same})")
```

Output:

```
7,000 membership tests against a list of 5,000:   147.81 ms
the same tests against a set:                      0.146 ms   (same answers: True)
```

The fix costs one line (`allowed_set = set(allowed)`) and removes a factor of about a thousand.

## 🔀 Making Linear Search Smarter: Move to Front

If some items are searched far more often than others, you can keep a list in a better order. The **move-to-front** heuristic ([Wikipedia: Self-organizing list](https://en.wikipedia.org/wiki/Self-organizing_list)) reorders the list as it is used: each time an item is found, it moves to the front, so popular items drift toward the start where they are found quickly. The simulation compares three strategies for 100 items whose popularity follows a skewed (Zipf-like) pattern, 20,000 queries each, reporting the average number of items examined per search:

```python
def average_cost(order, queries, move_to_front):
    lst = list(order)
    total = 0
    for q in queries:
        position = lst.index(q)
        total += position + 1                           # items examined
        if move_to_front and position:
            lst.insert(0, lst.pop(position))
    return total / len(queries)

random.seed(3)
population = list(range(100))
weights = [1 / (rank + 1) for rank in population]       # item 0 is the most popular, item 99 the least
skewed = random.choices(population, weights=weights, k=20_000)
uniform = random.choices(population, k=20_000)
arbitrary_order = population[:]
random.shuffle(arbitrary_order)
by_popularity = sorted(population, key=lambda item: -weights[item])        # the best possible fixed order

print(f"{'':>26} | {'skewed queries':>14} | {'uniform queries':>15}")
print(f"{'fixed, arbitrary order':>26} | {average_cost(arbitrary_order, skewed, False):>14.1f} | {average_cost(arbitrary_order, uniform, False):>15.1f}")
print(f"{'fixed, sorted by popularity':>26} | {average_cost(by_popularity, skewed, False):>14.1f} | {'(no popularity)':>15}")
print(f"{'move to front':>26} | {average_cost(arbitrary_order, skewed, True):>14.1f} | {average_cost(arbitrary_order, uniform, True):>15.1f}")
```

```text
                           | skewed queries | uniform queries
    fixed, arbitrary order |           48.9 |            50.6
fixed, sorted by popularity |           19.3 | (no popularity)
             move to front |           26.3 |            50.7
```

With skewed queries, move-to-front cuts the work roughly in half compared with an arbitrary fixed order (48.9 down to 26.3 items examined), without knowing the popularity in advance, and lands within about a third of the best possible fixed order (19.3). With uniform queries it brings no benefit (and costs a little for the reshuffling). The principle — *adapt the data's layout to how it is used* — is the idea behind caches such as the LRU cache in [doubly-linked-lists.md](../linked-lists/doubly-linked-lists.md).

## ✅ Verification

All the hand-written searches were compared with the built-in operations (and with simple comprehensions) on thousands of random lists, including empty lists, single items, and many duplicates:

```python
random.seed(4)
for _ in range(5_000):
    values = [random.randint(0, 9) for _ in range(random.randint(0, 20))]
    for target in range(-1, 11):
        first = values.index(target) if target in values else -1
        assert linear_search(values, target) == linear_search_while(values, target) == first
        if values:
            assert sentinel_search(list(values), target) == first
        assert find_all(values, target) == [i for i, v in enumerate(values) if v == target]
        last = len(values) - 1 - values[::-1].index(target) if target in values else -1
        assert find_last(values, target) == last
        assert find_first(values, lambda v: v >= target) == next((i for i, v in enumerate(values) if v >= target), -1)
print("all linear searches agree with the built-in operations on 5,000 random lists")
```

```text
all linear searches agree with the built-in operations on 5,000 random lists
```

## Common Mistakes

- **Treating the index `0` as "not found".** `if linear_search(items, x):` is false when the item is first, because `0` is falsy. Compare with the sentinel explicitly: `if index != -1:`.
- **Using the `-1` result as an index.** In Python `items[-1]` is the last item, so `items[linear_search(items, x)]` silently returns the wrong element when the search fails instead of raising an error.
- **Calling `list.index` without handling `ValueError`.** It raises when the item is missing; test with `in` first (two scans) or catch the exception.
- **Hiding a linear search inside a loop** (`x in some_list` for every `x`): the result is O(n × m). Convert the list to a set first.
- **Sorting just to search once.** Sorting costs more than the linear search it replaces.
- **Comparing floats with `==`.** `0.1 + 0.2 == 0.3` is `False`; search with a tolerance (`math.isclose`) when the values are computed.

The two Python-specific traps look like this:

```python
items = ["a", "b", "c"]
index = linear_search(items, "a")
if index:                                              # BUG: index is 0, which is falsy
    print("found")
else:
    print("not found (but 'a' is there!)")
print(items[linear_search(items, "z")])                # (BUG: -1 silently selects the last item, 'c')
```

```text
not found (but 'a' is there!)
c
```

## ➡️ Next

Continue to [binary-search.md](binary-search.md): when the data is sorted, each comparison can discard half of the remaining items, which turns a million-item search from half a million comparisons into about twenty.
