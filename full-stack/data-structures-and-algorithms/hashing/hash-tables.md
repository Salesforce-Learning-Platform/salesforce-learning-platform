# 🗄️ Hash Tables

## An Array Plus a Hash Function

A **hash table** stores key–value pairs in an array of slots called **buckets**. To find where a key belongs, it runs the key
through a [hash function](hash-functions.md) and reduces the result to a valid index:

```
index = hash(key) % number_of_buckets
```

Reading, inserting, and deleting then go straight to one bucket instead of searching — **O(1) on average**. Python's `dict`
and `set` are hash tables; so are Java's `HashMap`, JavaScript's `Map` and `Set`, and C++'s `unordered_map`. Knowing how one
works explains why dictionary lookups are fast, why keys must be hashable, and when the O(1) promise breaks.

This file builds one from scratch, tests it against Python's `dict`, measures how it behaves, and then looks at the real thing.
All outputs were produced by running the code on CPython 3.9.

## 🧱 The Idea in One Picture

With 4 buckets and integer keys (an integer's hash is itself):

```
key 10 -> 10 % 4 = 2         bucket 0: []
key 7  ->  7 % 4 = 3         bucket 1: []
key 6  ->  6 % 4 = 2         bucket 2: [10, 6]    <- two keys, same bucket: a collision
key 12 -> 12 % 4 = 0         bucket 3: [7]
```

Keys `10` and `6` land in the same bucket. The simplest fix, **separate chaining**, lets each bucket hold a small list of
entries; a lookup hashes to the bucket and then scans that short list comparing keys with `==`. (The second strategy, open
addressing, is in [collision-handling.md](collision-handling.md).)

## 🔨 Building One: A Hash Table With Chaining

```python
class HashTable:
    def __init__(self, capacity=8, max_load=0.75):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0
        self._max_load = max_load

    @property
    def capacity(self):
        return len(self._buckets)

    def __len__(self):
        return self._size

    def _index(self, key):
        return hash(key) % len(self._buckets)

    def put(self, key, value):
        bucket = self._buckets[self._index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)           # key already present: replace its value
                return
        bucket.append((key, value))                # new key: add to the chain
        self._size += 1
        if self._size / len(self._buckets) > self._max_load:
            self._resize(len(self._buckets) * 2)   # too crowded: grow

    def get(self, key, default=None):
        for existing_key, value in self._buckets[self._index(key)]:
            if existing_key == key:
                return value
        return default

    def remove(self, key):
        bucket = self._buckets[self._index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        sentinel = object()
        return self.get(key, sentinel) is not sentinel

    def _resize(self, new_capacity):
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(new_capacity)]
        for bucket in old_buckets:
            for key, value in bucket:
                self._buckets[self._index(key)].append((key, value))   # re-hash every entry

table = HashTable()
table.put("apple", 3)
table.put("pear", 5)
table.put("apple", 4)               # same key: updates, does not add
print(len(table), table.get("apple"), table.get("kiwi", "missing"))     # 2 4 missing
print("pear" in table, "kiwi" in table)                                  # True False
print(table.remove("pear"), table.remove("pear"), len(table))            # True False 1
```

Walk through the three operations:

- **`put`** hashes the key, scans only that bucket's chain for an existing equal key (to update it), and otherwise appends.
- **`get`** and **`remove`** hash the key and scan only one chain.
- **`_resize`** is the one expensive step: it allocates a bigger bucket array and **re-inserts every entry**, because
  `hash(key) % new_size` generally gives a different index than `hash(key) % old_size`.

### Correctness Check Against `dict`

A new data structure should be tested against one that is known to be right. This runs 20,000 random operations on the table
and on a `dict` side by side and compares the answers after every step:

```python
import random

random.seed(1)
mine, reference = HashTable(), {}
for step in range(20000):
    key = random.randint(0, 300)
    action = random.choice(["put", "get", "remove", "contains"])
    if action == "put":
        mine.put(key, step)
        reference[key] = step
    elif action == "get":
        assert mine.get(key) == reference.get(key)
    elif action == "remove":
        assert mine.remove(key) == (reference.pop(key, None) is not None)
    else:
        assert (key in mine) == (key in reference)
    assert len(mine) == len(reference)
print("20,000 random operations agree with dict")
```

```text
20,000 random operations agree with dict
```

## 📈 Load Factor and Resizing

The **load factor** is `items / buckets`. If it grows too large, chains get long and the O(1) promise erodes: the average
chain length *is* the load factor. So the table watches it and, when it passes a threshold (0.75 here), **doubles** the
bucket array. Watching the capacity while inserting 13 integer keys into a table that starts with 4 buckets:

```python
table = HashTable(capacity=4)
last_capacity = table.capacity
for key in range(1, 14):
    table.put(key, key * key)
    if table.capacity != last_capacity:
        print(f"after inserting {len(table):>2} items: capacity {last_capacity} -> {table.capacity}")
        last_capacity = table.capacity
print(f"final: {len(table)} items, {table.capacity} buckets, load factor {len(table) / table.capacity:.2f}")
```

```text
after inserting  4 items: capacity 4 -> 8
after inserting  7 items: capacity 8 -> 16
after inserting 13 items: capacity 16 -> 32
final: 13 items, 32 buckets, load factor 0.41
```

A resize touches every entry, so a single `put` that triggers it costs O(n). But because the capacity **doubles**, resizes get
rarer as the table grows (at 4, 7, 13, 25, … items), and the total cost of all resizes while inserting `n` items is less than
`2n` re-insertions. Spread across the `n` inserts that is O(1) each — the same **amortized O(1)** argument that explains
`list.append` in [array-fundamentals.md](../arrays/array-fundamentals.md) and
[insertion-and-deletion.md](../arrays/insertion-and-deletion.md).

## ⚠️ When the O(1) Promise Breaks

Everything above assumes the hash function spreads keys out. If many keys share a hash, they all land in one chain and every
operation scans it: **O(n)**. A deliberately bad key class shows the effect (the key's hash is always `1`):

```python
import timeit

class GoodKey:
    def __init__(self, n): self.n = n
    def __eq__(self, other): return self.n == other.n
    def __hash__(self): return hash(self.n)          # spreads keys out

class BadKey(GoodKey):
    def __hash__(self): return 1                     # every key collides

def fill_and_read(key_class, n):
    table = HashTable()
    for i in range(n):
        table.put(key_class(i), i)
    for i in range(n):
        table.get(key_class(i))

print(f"{'n':>6} | {'good hash':>10} | {'constant hash':>13}   (ms)")
for n in (250, 500, 1000, 2000):
    good = min(timeit.repeat(lambda: fill_and_read(GoodKey, n), number=1, repeat=3)) * 1000
    bad = min(timeit.repeat(lambda: fill_and_read(BadKey, n), number=1, repeat=3)) * 1000
    print(f"{n:>6,} | {good:10.2f} | {bad:13.2f}")
```

One run on the test machine printed:

```
     n |  good hash | constant hash   (ms)
   250 |       0.38 |          4.85
   500 |       0.75 |         18.77
 1,000 |       1.52 |         75.40
 2,000 |       3.14 |        301.51
```

With a good hash, doubling `n` roughly doubles the time (n operations at O(1) each). With the constant hash, doubling `n` roughly
**quadruples** it: n operations at O(n) each is O(n²). This is why the hash-flooding attack mentioned in
[hash-functions.md](hash-functions.md) is a real security problem, and why the table's "O(1)" is written **O(1) average,
O(n) worst case**.

## 🐍 How Python's `dict` Differs

Our table is faithful to the idea but not to CPython's implementation. The real `dict` differs in four ways, which can be
confirmed from CPython's source (`Objects/dictobject.c`, 3.9) and the language documentation:

| Aspect | Our `HashTable` | CPython's `dict` |
|--------|-----------------|------------------|
| Collision strategy | Separate chaining (a list per bucket) | **Open addressing** with a probe sequence that mixes in higher bits of the hash |
| Bucket count | Doubles; any size | Always a **power of two** (minimum 8) |
| Maximum load | 0.75 | **Two-thirds** of the slots may be used before it grows |
| Order | Bucket order (looks random) | **Insertion order**, guaranteed since Python 3.7 |

A power-of-two size also lets CPython turn `hash mod size` into a single bit mask, `hash & (size - 1)` (see [power-of-two-and-counting-bits.md](../bit-manipulation/power-of-two-and-counting-bits.md)).
CPython keeps a compact array of entries in insertion order plus a separate sparse array of small indexes into it — that is how
it preserves order and saves memory. You can watch the two-thirds rule from the outside by measuring the dictionary's size in
memory as keys are added; each jump is a resize:

```python
import sys

d = {}
last = sys.getsizeof(d)
print(f"{len(d):>3} keys: {last:>5} bytes")
for i in range(1, 100):
    d[i] = None
    size = sys.getsizeof(d)
    if size != last:
        print(f"{len(d):>3} keys: {size:>5} bytes  (storage grew)")
        last = size
```

One run on the test machine printed:

```
  0 keys:    64 bytes
  1 keys:   232 bytes  (storage grew)
  6 keys:   360 bytes  (storage grew)
 11 keys:   640 bytes  (storage grew)
 22 keys:  1176 bytes  (storage grew)
 43 keys:  2272 bytes  (storage grew)
 86 keys:  4696 bytes  (storage grew)
```

(The byte counts are specific to CPython 3.9 on a 64-bit build; other versions differ. The *thresholds* tell the story.) A table of 8
slots has room for `8 × 2/3 = 5` entries, so the 6th key forces a resize to 16 slots (room for 10); the 11th key forces 32
(room for 21); the 22nd forces 64 (room for 42); and so on, each time roughly doubling. That matches the source comment that a
dictionary is resized when it is "USABLE_FRACTION (currently two-thirds) full".

## 🏁 What the O(1) Is Worth

The payoff of hashing is easiest to see on **membership tests**. Searching a list for a value that is not there must examine every
element; a set hashes straight to the answer:

```python
import timeit

print(f"{'n':>9} | {'x in list':>12} | {'x in set':>10}   (microseconds per lookup of a missing value)")
for n in (1_000, 10_000, 100_000, 1_000_000):
    as_list = list(range(n))
    as_set = set(as_list)
    t_list = min(timeit.repeat(lambda: -1 in as_list, number=20, repeat=3)) / 20 * 1e6
    t_set = min(timeit.repeat(lambda: -1 in as_set, number=20, repeat=3)) / 20 * 1e6
    print(f"{n:>9,} | {t_list:12.2f} | {t_set:10.3f}")
```

One run on the test machine printed:

```
        n |    x in list |   x in set   (microseconds per lookup of a missing value)
    1,000 |         4.70 |      0.048
   10,000 |        47.58 |      0.052
  100,000 |       482.57 |      0.050
1,000,000 |      4789.67 |      0.050
```

The list column grows tenfold each row — linear, O(n) — while the set column stays flat. This single idea ("replace a scan with a
lookup") is behind most of the techniques in [hash-based-problem-solving.md](hash-based-problem-solving.md).

## 📋 Cost Summary

| Operation | Average | Worst case | Notes |
|-----------|---------|-----------|-------|
| Insert / update | O(1) amortized | O(n) | Worst case: a resize, or all keys colliding |
| Lookup | O(1) | O(n) | Worst case: all keys in one chain or probe sequence |
| Delete | O(1) | O(n) | Same as lookup |
| Iterate over all entries | O(n) | O(n) | Visits every item (and, for tables, every bucket) |
| Memory | O(n) | O(n) | Larger constant than an array: spare buckets and stored hashes/pointers |

The Python wiki's [TimeComplexity](https://wiki.python.org/moin/TimeComplexity) page lists the same figures for `dict` and
`set`: get, set, and delete are O(1) on average and O(n) in the worst case.

## 🧰 Using Hash Tables in Python

| Tool | Use |
|------|-----|
| `dict` | Key → value mapping; `d[key]`, `d.get(key, default)`, `key in d`, `d.setdefault(key, [])` |
| `set` | Membership and uniqueness; `a & b`, `a \| b`, `a - b` |
| `collections.Counter` | Counting occurrences: `Counter("banana")` |
| `collections.defaultdict` | A `dict` that creates missing values: `defaultdict(list)` |
| `frozenset`, `tuple` | Immutable, hashable stand-ins for sets and lists when you need a composite key |

## ⚖️ Strengths and Limits

**Use a hash table when** you need fast lookup, insertion, deletion, counting, or "have I seen this?" by exact key.

**Consider something else when:**

- You need keys **in sorted order** or **range queries** ("all keys between 10 and 20") — a sorted array with binary search or
  a balanced tree supports these; a hash table scatters keys on purpose.
- Memory is tight — a hash table keeps spare capacity and stores more per entry than an array.
- The data is **tiny** — scanning a list of five items is as fast as hashing.
- Your keys are **mutable** or have no sensible hash.

## Common Mistakes

- **Treating O(1) as guaranteed** instead of "average, given a good hash function and a bounded load factor."
- **Using mutable objects as keys**, or changing a key's hashed fields after insertion (see
  [hash-functions.md](hash-functions.md)).
- **Relying on iteration order** of a `set`, or assuming a hand-built table preserves insertion order.
- **Forgetting to re-hash everything when resizing** — an entry left at its old index becomes unfindable.
- **Searching a list repeatedly inside a loop** when converting it to a `set` once would make each lookup O(1).
- **Deleting while iterating** over a dictionary (`RuntimeError: dictionary changed size during iteration`) — iterate over a
  copy of the keys instead.

## ➡️ Next

Continue to [collision-handling.md](collision-handling.md) to look closely at what happens when two keys want the same bucket:
why collisions come sooner than intuition suggests, and how chaining and open addressing (linear probing, tombstones) compare.
