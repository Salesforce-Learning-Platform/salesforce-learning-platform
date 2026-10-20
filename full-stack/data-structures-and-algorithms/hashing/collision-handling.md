# 💥 Collision Handling

## When Two Keys Want the Same Slot

A **collision** is when two different keys hash to the same bucket. No hash table can avoid them: there are far more possible
keys than buckets, so by the pigeonhole principle some keys must share. What distinguishes hash table designs is what they *do*
when it happens. This file explains why collisions come sooner than intuition suggests, then compares the two standard
strategies — **separate chaining** and **open addressing** — with measurements.

Every result below was produced by running the code on CPython 3.9.

## 🎂 Collisions Come Early

It feels as if collisions should only appear when a table is nearly full. They don't. This is the *birthday problem*: in a group
of just 23 people the chance that two share a birthday already exceeds 50%, even though there are 365 days. The same arithmetic
applies to keys and buckets. The probability that `k` random keys hash into `m` buckets **without** any collision is
`(1 − 1/m)(1 − 2/m)…(1 − (k−1)/m)`:

```python
def collision_probability(keys, buckets):
    no_collision = 1.0
    for i in range(keys):
        no_collision *= (buckets - i) / buckets
    return 1 - no_collision

print(f"{collision_probability(23, 365):.3f}")          # 0.507   — 23 people, 365 birthdays
print(f"{collision_probability(40, 1000):.3f}")         # 0.546   — 40 keys in only 1,000 buckets
print(f"{collision_probability(100, 1000):.3f}")        # 0.994   — 100 keys: a collision is all but certain
```

The second line is the surprise: with 1,000 buckets and only **40** keys (a 4% load), a collision is already more likely than
not. A rule of thumb: the first collision arrives after roughly `√m` insertions. A simulation with a million buckets confirms it:

```python
import random

random.seed(3)

def inserts_before_first_collision(buckets):
    seen = set()
    count = 0
    while True:
        slot = random.randrange(buckets)
        if slot in seen:
            return count + 1                  # this insertion collided
        seen.add(slot)
        count += 1

trials = [inserts_before_first_collision(1_000_000) for _ in range(300)]
print(f"average insertions until the first collision: {sum(trials) / len(trials):,.0f}")
print(f"theory, sqrt(pi * m / 2): {(3.141592653589793 * 1_000_000 / 2) ** 0.5:,.0f}")
```

```text
average insertions until the first collision: 1,203
theory, sqrt(pi * m / 2): 1,253
```

Out of a million buckets, a collision typically happens after **only about 1,200 insertions** (theory predicts roughly 1,250) — a 0.12% load. Collisions are normal,
not exceptional, so a table must handle them gracefully from the very first insertion.

## ⛓️ Strategy 1: Separate Chaining

Each bucket holds a small collection (usually a list) of every entry that hashed there — the approach of the `HashTable` in
[hash-tables.md](hash-tables.md). A lookup hashes to the bucket and scans its chain.

**Cost.** If the hash function spreads keys evenly, the average chain length equals the **load factor** α = n / m. A successful
search examines about `1 + α/2` entries on average. The measurement below fills 1,000 buckets with random keys at different
loads and counts the comparisons needed to find every key:

```python
import random

random.seed(5)

def average_comparisons(load_factor, buckets=1000):
    table = [[] for _ in range(buckets)]
    keys = random.sample(range(10**9), int(buckets * load_factor))
    for key in keys:
        table[hash(key) % buckets].append(key)
    total = sum(table[hash(key) % buckets].index(key) + 1 for key in keys)   # entries examined to find each key
    return total / len(keys)

print(f"{'load factor':>11} | {'measured':>8} | {'1 + alpha/2':>11}")
for load in (0.5, 1, 2, 4, 8):
    print(f"{load:>11} | {average_comparisons(load):8.2f} | {1 + load / 2:11.2f}")
```

```text
load factor | measured | 1 + alpha/2
        0.5 |     1.21 |        1.25
          1 |     1.50 |        1.50
          2 |     1.99 |        2.00
          4 |     3.01 |        3.00
          8 |     4.98 |        5.00
```

The measurements track the formula. Two properties make chaining attractive:

- **It degrades gracefully.** At α = 4 the average search still examines only about 3 entries. The load factor can even exceed 1.
- **Deletion is trivial.** Remove the entry from its list.

The costs: a separate list object per non-empty bucket (extra memory and pointer chasing), and poor cache behavior because the
entries are scattered in memory.

## 🕳️ Strategy 2: Open Addressing

Open addressing stores every entry **directly in the bucket array**, with no chains. When the target slot is taken, the table
**probes** — examines other slots in a fixed, reproducible order — until it finds an empty one. A lookup follows the same probe
sequence and stops at the key (found) or an empty slot (absent).

The simplest probe sequence is **linear probing**: try `i`, then `i+1`, `i+2`, … wrapping around. Here is a complete table with
linear probing, including the one tricky operation, deletion:

```python
EMPTY = object()
TOMBSTONE = object()

class LinearProbingTable:
    def __init__(self, capacity=8, max_load=0.7, use_tombstones=True):
        self._slots = [EMPTY] * capacity           # each slot: EMPTY, TOMBSTONE, or a (key, value) pair
        self._live = 0                              # live entries
        self._filled = 0                            # live entries + tombstones (both lengthen probes)
        self._max_load = max_load
        self._use_tombstones = use_tombstones

    def __len__(self):
        return self._live

    def _probe(self, key):
        capacity = len(self._slots)
        start = hash(key) % capacity
        for step in range(capacity):
            yield (start + step) % capacity         # linear probing: i, i+1, i+2, ...

    def put(self, key, value):
        first_tombstone = None
        for i in self._probe(key):
            slot = self._slots[i]
            if slot is EMPTY:                       # the key is not in the table: insert here (or in a freed slot)
                target = first_tombstone if first_tombstone is not None else i
                if self._slots[target] is EMPTY:
                    self._filled += 1               # a fresh slot is consumed; reusing a tombstone adds nothing
                self._slots[target] = (key, value)
                self._live += 1
                if self._filled / len(self._slots) > self._max_load:
                    self._resize(len(self._slots) * 2)
                return
            if slot is TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = i             # remember the first reusable slot, but keep looking for the key
            elif slot[0] == key:
                self._slots[i] = (key, value)       # existing key: update
                return
        raise RuntimeError("no empty slot found")   # cannot happen while the load limit keeps empty slots available

    def get(self, key, default=None):
        for i in self._probe(key):
            slot = self._slots[i]
            if slot is EMPTY:
                return default                      # an empty slot ends the probe sequence: the key is absent
            if slot is not TOMBSTONE and slot[0] == key:
                return slot[1]
        return default

    def remove(self, key):
        for i in self._probe(key):
            slot = self._slots[i]
            if slot is EMPTY:
                return False
            if slot is not TOMBSTONE and slot[0] == key:
                self._slots[i] = TOMBSTONE if self._use_tombstones else EMPTY
                self._live -= 1
                return True
        return False

    def _resize(self, new_capacity):
        old_slots = self._slots
        self._slots = [EMPTY] * new_capacity
        self._live = self._filled = 0
        for slot in old_slots:
            if slot is not EMPTY and slot is not TOMBSTONE:
                self.put(*slot)                     # re-insert live entries; tombstones disappear

table = LinearProbingTable()
for key in (3, 11, 19):                             # all three hash to slot 3 in an 8-slot table
    table.put(key, f"value-{key}")
print(table.get(11), table.get(19), table.get(5, "absent"))     # value-11 value-19 absent
```

Keys `3`, `11`, and `19` all want slot 3 (`k % 8 == 3`). The first takes slot 3, the second is pushed to slot 4, and the third to slot 5. A
lookup for `19` starts at slot 3 and *walks* — past `3`, past `11` — until it finds `19`.

### Why Deletion Needs a Tombstone

Suppose we delete `11` by simply emptying its slot. Now the probe sequence for `19` hits that empty slot at index 4 and
concludes "an empty slot means the key was never here" — and `19` becomes unreachable:

```python
naive = LinearProbingTable(use_tombstones=False)
safe = LinearProbingTable(use_tombstones=True)
for t in (naive, safe):
    for key in (3, 11, 19):
        t.put(key, f"value-{key}")
    t.remove(11)

print("empty the slot  :", naive.get(19))    # empty the slot : None — 19 is lost!
print("leave tombstone :", safe.get(19))     # leave tombstone : value-19
```

A **tombstone** is a special marker meaning "an entry was here; keep probing." Lookups skip over tombstones, insertions may
reuse them, and a resize discards them. The cost is that tombstones occupy slots and lengthen probe sequences until the next
resize, so the table counts them toward its load. (There is an alternative, *eager* deletion, that moves later entries back to close the gap —
more complex, and not needed here.)

### Testing Against `dict`

As with the chained table, a randomized comparison with Python's `dict`, with lots of deletions, builds confidence:

```python
import random

random.seed(2)
mine, reference = LinearProbingTable(), {}
for step in range(30000):
    key = random.randint(0, 120)
    action = random.choice(["put", "get", "remove"])
    if action == "put":
        mine.put(key, step)
        reference[key] = step
    elif action == "get":
        assert mine.get(key) == reference.get(key)
    else:
        assert mine.remove(key) == (reference.pop(key, None) is not None)
    assert len(mine) == len(reference)
print("30,000 random operations agree with dict")
```

```text
30,000 random operations agree with dict
```

## 📉 Why Load Factor Matters Even More Here: Clustering

Linear probing has a weakness called **primary clustering**: occupied slots tend to merge into long runs, and any key hashing
into a run must walk to its end — which makes the run longer still. The effect is mild at low load and dramatic near full. For
an ideal hash function the expected number of probes are classic results from Knuth: `½(1 + 1/(1−α))` for a successful search and
`½(1 + 1/(1−α)²)` for an unsuccessful one (the same growth the [Wikipedia article on linear
probing](https://en.wikipedia.org/wiki/Linear_probing) gives as O(1 + 1/(1−α)) and O(1 + 1/(1−α)²)). A simulation with 20,011 slots, using an ideal random hash value for each key, agrees with the formulas:

```python
import random

def linear_probing_probes(load, capacity=20011, trials=30):
    found_total = absent_total = 0.0
    for _ in range(trials):
        slots = [None] * capacity
        count = int(load * capacity)
        starts = [random.randrange(capacity) for _ in range(count)]    # an ideal random hash for each key
        for key, start in enumerate(starts):
            i = start
            while slots[i] is not None:
                i = (i + 1) % capacity                                 # linear probing
            slots[i] = key
        found = 0
        for key, start in enumerate(starts):                           # probes needed to find each stored key
            i, probes = start, 1
            while slots[i] != key:
                i = (i + 1) % capacity
                probes += 1
            found += probes
        absent = 0
        for _ in range(4000):                                          # probes needed to learn a random key is absent
            i, probes = random.randrange(capacity), 1
            while slots[i] is not None:
                i = (i + 1) % capacity
                probes += 1
            absent += probes
        found_total += found / count
        absent_total += absent / 4000
    return found_total / trials, absent_total / trials

random.seed(8)
print(f"{'load':>5} | {'find (measured)':>15} {'formula':>8} | {'absent (measured)':>17} {'formula':>8}")
for load in (0.25, 0.5, 0.7, 0.9):
    found, absent = linear_probing_probes(load)
    print(f"{load:>5} | {found:15.2f} {0.5 * (1 + 1 / (1 - load)):8.2f} | {absent:17.2f} {0.5 * (1 + 1 / (1 - load) ** 2):8.2f}")
```

```text
 load | find (measured)  formula | absent (measured)  formula
 0.25 |            1.16     1.17 |              1.39     1.39
  0.5 |            1.50     1.50 |              2.50     2.50
  0.7 |            2.16     2.17 |              6.12     6.06
  0.9 |            5.46     5.50 |             49.47    50.50
```

Look at the last row: at 90% full a failed lookup takes **roughly fifty probes**. That is why open-addressing tables resize long
before they are full (ours at 70%, CPython's `dict` at two-thirds) — the performance cliff is steep.

## 🔀 Better Probe Sequences

Linear probing's fixed step means keys that collide follow *identical* paths, which causes clustering. Other probe sequences
spread them out:

- **Quadratic probing** steps `1, 4, 9, …` from the start slot, which breaks up long runs.
- **Double hashing** uses a *second* hash of the key as the step size, so different keys get different paths.
- **CPython's `dict`** uses a recurrence that mixes in the higher bits of the hash. Its source (`Objects/dictobject.c`) documents the
  scheme: start at `j = hash mod 2ⁱ`, then repeatedly set `perturb >>= 5` and `j = (5·j + 1 + perturb) mod 2ⁱ`. Because the table size is
  a power of two, "mod 2ⁱ" is just a bit mask (see [power-of-two-and-counting-bits.md](../bit-manipulation/power-of-two-and-counting-bits.md)). This
  reproduces that recurrence:

```python
def cpython_style_probe(hash_value, table_size, count):
    mask = table_size - 1                       # table_size is a power of two
    perturb = hash_value & (2**64 - 1)
    slot = hash_value & mask
    order = [slot]
    for _ in range(count - 1):
        perturb >>= 5
        slot = (5 * slot + 1 + perturb) & mask
        order.append(slot)
    return order

print(cpython_style_probe(0, 8, 8))           # [0, 1, 6, 7, 4, 5, 2, 3]
print(cpython_style_probe(5, 8, 4))           # [5, 2, 3, 0]
print(cpython_style_probe(5 + 64, 8, 4))      # [5, 4, 5, 2]
```

The first line matches the example in the CPython source comment for a table of 8 slots (`0 → 1 → 6 → 7 → 4 → 5 → 2 → 3`):
with a hash of 0, `perturb` is 0 and the recurrence cycles through every slot exactly once. The last two lines show
the point of `perturb`: hashes `5` and `69` start at the same slot (they agree in their low three bits) but follow *different*
paths, because their higher bits differ — so keys that collide on the first slot do not keep colliding.

## ⚖️ Chaining vs. Open Addressing

| | Separate chaining | Open addressing |
|--|-------------------|-----------------|
| Where entries live | In per-bucket lists | In the bucket array itself |
| Load factor | Can exceed 1 | Must stay below 1 (resize early) |
| Deletion | Remove from the list | Needs tombstones (or back-shifting) |
| Memory | Extra object per chain; pointer overhead | Compact; no per-entry objects |
| Cache behavior | Scattered in memory | Contiguous probes are cache-friendly |
| Sensitivity to clustering | Low | Higher — depends on probe sequence |
| Used by | Java's `HashMap` (with tree buckets for long chains), many textbooks | CPython's `dict` and `set`, many modern high-performance tables |

Neither is "better"; they trade memory layout and simplicity against load tolerance. Other schemes exist — **cuckoo hashing**
(each key has two possible slots, giving worst-case O(1) lookups) and **Robin Hood hashing** (an open-addressing variant that
evens out probe lengths) — but they are refinements of the same two ideas.

## Common Mistakes

- **Assuming collisions only happen in nearly-full tables** — the birthday effect means they begin almost immediately.
- **Deleting from an open-addressing table by emptying the slot**, which breaks later keys' probe sequences.
- **Letting an open-addressing table fill up** — probe lengths explode as α approaches 1, and a completely full table makes unsuccessful
  searches loop forever unless the probe loop is bounded.
- **Forgetting that tombstones count toward the load**, so a table with many deletions can need a resize even though few entries are live.
- **Using a weak hash function and blaming the strategy** — clustering from a poor hash defeats both chaining and probing.
- **Comparing only hashes** and skipping the `==` check on the key — equal hashes do not mean equal keys.

## ➡️ Next

Continue to [hash-based-problem-solving.md](hash-based-problem-solving.md) to put hash tables to work: two-sum, counting,
grouping, prefix sums, longest consecutive sequences, and an LRU cache.
