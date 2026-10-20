# 🧩 Heap Problems

## One Idea: Keep Only the Candidates That Might Still Matter

Heap problems share a recognisable shape: *you only ever need the best (smallest or largest) few items, and the data is large, streaming, or arrives in several sorted pieces.* Sorting everything is
wasteful, because it orders items you will never look at. A heap lets you maintain just the candidates that matter, in O(log k) per item for a heap of size `k`. This file solves eight classic problems with
that idea. Every function was tested against a brute-force or direct-sorting version on thousands of random inputs (the verification block is at the end). All outputs were produced by running the code on
CPython 3.9.

Python's `heapq` is a min-heap, so a *max*-heap is simulated by negating values (see [min-heap-and-max-heap.md](min-heap-and-max-heap.md)).

```python
import heapq
from collections import Counter
```

## 1️⃣ The k-th Largest Element

*Find the k-th largest number in a list.* Sorting is O(n log n). With a heap, keep the **k largest items seen so far** in a **min**-heap of size `k`. The root of that heap is the smallest of the k largest — which is exactly the
k-th largest overall. For each new number, if it beats the root, it replaces it:

```python
def kth_largest(numbers, k):
    if not 1 <= k <= len(numbers):
        raise ValueError("k must be between 1 and len(numbers)")
    heap = list(numbers[:k])
    heapq.heapify(heap)                         # the k largest so far; heap[0] is the smallest of them
    for x in numbers[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)          # evict the smallest of the kept items, admit x
    return heap[0]

print(kth_largest([3, 2, 1, 5, 6, 4], 2))       # 5
print(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))    # 4
```

**O(n log k) time, O(k) space** — and the list does not even have to fit in memory, because the loop only needs one number at a time. That makes the same idea work for a **stream** of numbers, reporting
the k-th largest after every arrival:

```python
class KthLargest:
    def __init__(self, k):
        self._k = k
        self._heap = []                         # a min-heap holding the k largest values seen so far

    def add(self, x):
        if len(self._heap) < self._k:
            heapq.heappush(self._heap, x)
        elif x > self._heap[0]:
            heapq.heapreplace(self._heap, x)
        return self._heap[0] if len(self._heap) == self._k else None     # None until k values have arrived

stream = KthLargest(3)
print([stream.add(x) for x in [4, 5, 8, 2, 3, 5, 10, 9, 4]])      # [None, None, 4, 4, 4, 5, 5, 8, 8]
```

Why a **min**-heap to find the *largest*? Because the item you may need to throw away is the smallest of the ones you are keeping, and a min-heap exposes it in O(1).

## 2️⃣ The k Most Frequent Items

*Return the `k` items that occur most often* (ties broken by the smaller item, to make the answer unique). Count with a dictionary ([hash-based-problem-solving.md](../hashing/hash-based-problem-solving.md)), then select the
top `k` of the `m` distinct items with a heap instead of sorting all `m`:

```python
def top_k_frequent(items, k):
    counts = Counter(items)                                                    # O(n)
    return heapq.nsmallest(k, counts, key=lambda item: (-counts[item], item))  # best = highest count, then smallest item

print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))             # [1, 2]
print(top_k_frequent(list("mississippi"), 2))            # ['i', 's']
```

The key `(-count, item)` makes "most frequent first" into "smallest key first", which is what `nsmallest` wants. Time: O(n) to count plus O(m log k) to select, with O(m) space for the counts. Compare this with
sorting all the distinct items, O(m log m): the heap wins when `k` is much smaller than `m`.

## 3️⃣ Merge k Sorted Lists

*Merge `k` already-sorted lists into one sorted list.* Concatenating and sorting costs O(N log N) for `N` total items and ignores the work already done. A heap keeps **one candidate per list** — the next unmerged
item of each — and repeatedly takes the smallest. After taking an item, push its successor from the same list:

```python
def merge_k_sorted(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]     # (value, which list, position in that list)
    heapq.heapify(heap)
    result = []
    while heap:
        value, i, position = heapq.heappop(heap)
        result.append(value)
        if position + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][position + 1], i, position + 1))     # the next item of the same list
    return result

print(merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]]))      # [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(merge_k_sorted([[], [1, 2], [0, 5]]))                   # [0, 1, 2, 5]
```

The heap never holds more than `k` entries, so each push and pop costs O(log k): **O(N log k) time, O(k) extra space** (not counting the output). This is exactly what `heapq.merge` does lazily, and it is the core of
**external sorting** — sorting data too large for memory by sorting chunks and merging them. The tuple `(value, i, position)` includes the list index so that ties on `value` never compare the lists themselves.

## 4️⃣ The Running Median

*After each number arrives from a stream, report the median of all numbers so far.* Re-sorting each time is O(n log n) per query. Split the numbers into a **lower half** and an **upper half**: the median is
at the boundary. The lower half needs fast access to its **largest** element (a max-heap); the upper half needs fast access to its **smallest** (a min-heap). Keep them balanced so their sizes differ by at most one.

```python
class RunningMedian:
    def __init__(self):
        self._low = []                           # max-heap (negated values): the smaller half
        self._high = []                          # min-heap: the larger half

    def add(self, x):
        heapq.heappush(self._low, -x)                              # put x in the lower half...
        heapq.heappush(self._high, -heapq.heappop(self._low))      # ...then move that half's largest up to the upper half
        if len(self._high) > len(self._low):                       # keep the lower half the same size or one bigger
            heapq.heappush(self._low, -heapq.heappop(self._high))

    def median(self):
        if not self._low:
            raise ValueError("no numbers yet")
        if len(self._low) > len(self._high):
            return float(-self._low[0])                            # odd count: the lower half's largest
        return (-self._low[0] + self._high[0]) / 2                 # even count: the average of the two middle values

rm = RunningMedian()
medians = []
for x in [5, 15, 1, 3, 8, 7, 9, 10, 20, 2]:
    rm.add(x)
    medians.append(rm.median())
print(medians)           # [5.0, 10.0, 5.0, 4.0, 5.0, 6.0, 7.0, 7.5, 8.0, 7.5]
```

Each `add` is O(log n) (a few heap operations) and each `median` is O(1) (look at the two roots). The key invariants are: every number in the lower half is ≤ every number in the upper half, and the
lower half has the same number of items as the upper half or one more.

## 5️⃣ Connect Ropes at Minimum Cost

*You have ropes of various lengths. Joining two ropes costs the sum of their lengths. Join all of them into one rope with the least total cost.* The greedy insight: always join the two **shortest** ropes, because a
long rope that is joined early gets paid for again in every later join. After joining, the new rope goes back into the pool — a job for a min-heap (this is the same greedy idea as **Huffman coding**):

```python
def min_cost_to_connect(ropes):
    heap = list(ropes)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        first, second = heapq.heappop(heap), heapq.heappop(heap)     # the two shortest ropes
        total += first + second                                       # the cost of joining them
        heapq.heappush(heap, first + second)                          # the joined rope goes back into the pool
    return total

print(min_cost_to_connect([4, 3, 2, 6]))        # 29
print(min_cost_to_connect([1, 2, 3, 4, 5]))     # 33
print(min_cost_to_connect([7]))                 # 0
```

For `[4, 3, 2, 6]`: join 2+3=5 (cost 5), then 4+5=9 (cost 9), then 6+9=15 (cost 15): total 29. O(n log n). The answer is checked against an exhaustive search of every possible joining order in the
verification block.

## 6️⃣ The k Closest Points to the Origin

*Given points on a plane, return the `k` closest to the origin.* Keep the `k` closest seen so far in a **max**-heap keyed by distance, so the farthest of the kept points is at the root and can be evicted when a closer
one arrives. Comparing squared distances avoids square roots:

```python
def k_closest(points, k):
    heap = []                                              # a max-heap (negated squared distance) of the k closest so far
    for x, y in points:
        d = -(x * x + y * y)
        if len(heap) < k:
            heapq.heappush(heap, (d, x, y))
        elif d > heap[0][0]:                               # closer than the farthest kept point
            heapq.heapreplace(heap, (d, x, y))
    return sorted((x, y) for _, x, y in heap)

print(k_closest([(1, 3), (-2, 2), (5, 8), (0, 1)], 2))     # [(-2, 2), (0, 1)]
```

O(n log k) time, O(k) space. When `k` is small compared with `n`, this is much cheaper than sorting all `n` distances, and it works on a stream of points.

## 7️⃣ Last Stone Weight

*Stones with given weights are smashed together: take the two heaviest; if they are equal both vanish, otherwise the lighter is destroyed and the heavier loses that weight. Repeat. What is left?* The repeated
need for "the two largest" is a max-heap:

```python
def last_stone_weight(stones):
    heap = [-s for s in stones]                            # a max-heap, via negation
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = -heapq.heappop(heap), -heapq.heappop(heap)  # the two heaviest stones, a >= b
        if a != b:
            heapq.heappush(heap, -(a - b))                 # the remainder goes back
    return -heap[0] if heap else 0

print(last_stone_weight([2, 7, 4, 1, 8, 1]))               # 1
print(last_stone_weight([5, 5]))                           # 0
```

## 8️⃣ Sorting a Nearly Sorted List

*Each element of a list is at most `k` positions away from where it would be in sorted order. Sort it faster than O(n log n).* The smallest remaining element must be among the next `k + 1` unprocessed
elements. A min-heap of that window finds it, then slides forward:

```python
def sort_nearly_sorted(numbers, k):
    heap = list(numbers[:k + 1])
    heapq.heapify(heap)                                    # the window of the next k + 1 elements
    result = []
    for x in numbers[k + 1:]:
        result.append(heapq.heappushpop(heap, x))          # add the next element, take out the smallest
    while heap:
        result.append(heapq.heappop(heap))                 # drain the window
    return result

print(sort_nearly_sorted([2, 1, 4, 3, 6, 5, 8, 7], 1))     # [1, 2, 3, 4, 5, 6, 7, 8]
```

**O(n log k)** — when `k` is small this approaches linear time, whereas a general sort is O(n log n).

## ✅ Verification

Each function was compared with a direct definition on thousands of random inputs: `sorted` for the selection problems, `statistics.median` for the running median, an exhaustive search over joining orders for the
ropes, plain sorting by distance for the points, and a re-sorting simulation for the stones.

```python
import random
import statistics

random.seed(14)

def brute_min_cost(ropes):                                   # try every pair to join first (exponential: only for tiny inputs)
    if len(ropes) <= 1:
        return 0
    best = None
    for i in range(len(ropes)):
        for j in range(i + 1, len(ropes)):
            rest = [r for idx, r in enumerate(ropes) if idx not in (i, j)] + [ropes[i] + ropes[j]]
            cost = ropes[i] + ropes[j] + brute_min_cost(rest)
            best = cost if best is None else min(best, cost)
    return best

def brute_stones(stones):
    stones = sorted(stones)
    while len(stones) > 1:
        a, b = stones.pop(), stones.pop()
        if a != b:
            stones.append(a - b)
            stones.sort()
    return stones[0] if stones else 0

for _ in range(4000):
    numbers = [random.randint(-30, 30) for _ in range(random.randint(1, 25))]
    k = random.randint(1, len(numbers))
    assert kth_largest(numbers, k) == sorted(numbers, reverse=True)[k - 1]

    stream, tracker = KthLargest(k), []
    for i, x in enumerate(numbers):
        tracker.append(stream.add(x))
        expected = sorted(numbers[:i + 1], reverse=True)[k - 1] if i + 1 >= k else None
        assert tracker[-1] == expected

    items = [random.randint(0, 6) for _ in range(random.randint(0, 30))]
    counts = Counter(items)
    kk = random.randint(0, 8)
    assert top_k_frequent(items, kk) == sorted(counts, key=lambda it: (-counts[it], it))[:kk]

    lists = [sorted(random.randint(0, 20) for _ in range(random.randint(0, 6))) for _ in range(random.randint(0, 5))]
    assert merge_k_sorted(lists) == sorted(x for lst in lists for x in lst) == list(heapq.merge(*lists))

    rm = RunningMedian()
    for i, x in enumerate(numbers):
        rm.add(x)
        assert rm.median() == statistics.median(numbers[:i + 1])

    ropes = [random.randint(1, 15) for _ in range(random.randint(0, 6))]
    assert min_cost_to_connect(ropes) == brute_min_cost(ropes)

    points = [(random.randint(-8, 8), random.randint(-8, 8)) for _ in range(random.randint(1, 15))]
    kc = random.randint(1, len(points))
    got = sorted(x * x + y * y for x, y in k_closest(points, kc))
    assert got == sorted(x * x + y * y for x, y in points)[:kc] and len(set(k_closest(points, kc))) <= kc

    stones = [random.randint(1, 20) for _ in range(random.randint(0, 10))]
    assert last_stone_weight(stones) == brute_stones(stones)

    window = random.randint(0, 5)
    base = sorted(random.randint(0, 50) for _ in range(random.randint(0, 30)))
    nearly = []
    for start in range(0, len(base), window + 1):             # shuffle inside blocks of window + 1: nothing moves more than `window` places
        block = base[start:start + window + 1]
        random.shuffle(block)
        nearly += block
    assert sort_nearly_sorted(nearly, window) == sorted(nearly)
print("all eight heap problems agree with their direct definitions on 4,000 random inputs")
```

```text
all eight heap problems agree with their direct definitions on 4,000 random inputs
```

## 🧭 Recognising the Pattern

| The problem says… | Heap structure | Cost |
|-------------------|----------------|------|
| "the k largest / k-th largest" | **Min**-heap of size `k` | O(n log k) |
| "the k smallest / nearest / cheapest" | **Max**-heap of size `k` | O(n log k) |
| "the k most frequent" | Count, then a heap of size `k` over the counts | O(n + m log k) |
| "merge k sorted sequences" | Min-heap with one entry per sequence | O(N log k) |
| "median of a stream" | Max-heap (lower half) + min-heap (upper half) | O(log n) per add |
| "repeatedly take the two smallest/largest" | One heap, pop twice, push once | O(n log n) |
| "each item is at most `k` places out of order" | Min-heap window of size `k + 1` | O(n log k) |

## Common Mistakes

- **Using a max-heap to find the k largest** — you need a *min*-heap of size `k`, so that the item to evict is at the root.
- **Pushing everything and popping `k` times** (O(n log n)) when a heap of size `k` (O(n log k)) suffices.
- **Pushing tuples whose later elements cannot be compared** (add an index or counter tie-breaker, as in the merge).
- **Forgetting to negate back** when reading from a simulated max-heap.
- **Letting the two median heaps drift out of balance**, or putting a number in the wrong half.
- **Greedy mistakes in the ropes problem**: joining the *largest* ropes first, or forgetting to push the combined rope back.
- **Sorting when the data is a stream** that cannot be held in memory.

## Module Summary

The Heaps and Priority Queues module introduced a structure that trades full sorting for fast access to the extreme item. [Heap Fundamentals](heap-fundamentals.md) defined the heap property, stored a complete tree in an array, built
`push`, `pop`, and linear-time `heapify`, and showed that building by pushes can cost n log n while heapify never exceeds 2n comparisons. [Min-Heaps and Max-Heaps](min-heap-and-max-heap.md) toured `heapq`, derived max-heap behaviour
by negation and reversal, and covered the tuple tie trap. [Priority Queues](priority-queues.md) defined the abstract data type, measured four implementations, and built a stable queue with lazy deletion for priority updates. This
file applied the heap to eight classic problems.

Carry these ideas forward:

- A heap keeps only a *partial* order — a parent never exceeds its children — which is why it is cheaper than a sorted structure: O(1) peek, O(log n) push and pop, O(n) build.
- To keep the `k` largest items, use a **min**-heap of size `k`; to keep the `k` smallest, use a **max**-heap.
- Use `heapq` in single-threaded Python; handle ties with a counter; change priorities with lazy deletion.
- Heaps are the engine of Dijkstra's shortest-path algorithm and of Prim's minimum spanning tree algorithm in the Graphs module that follows, and of [heap sort](../sorting-algorithms/heap-sort.md) in the Sorting module.

## ➡️ Next

Continue to the [Graphs](../graphs/README.md) module, the next module in this domain, where items are connected by arbitrary relationships rather than a strict hierarchy — and where priority queues reappear in the shortest-path algorithms.
