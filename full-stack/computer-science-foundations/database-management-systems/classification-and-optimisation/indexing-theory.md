# 🌲 How Indexes Work

## An Index Saves Pages

A database reads and writes its files in fixed-size **pages**; in SQLite they are 4,096 bytes by default on this machine, and a disk itself offers numbered blocks ([File System Basics](../../operating-systems/file-systems/file-system-basics.md)). Without a useful index, a query that filters a table usually has to read **every page** of it. An index is an extra structure that lets the database find the rows it needs by reading only a few pages. [indexes.md](../../../backend/sql-fundamentals/indexes.md) covers when to create one; this lesson is about how indexes are built inside. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54.

## 🪜 From Binary Search to a Wide Tree

A sorted list can be searched by halving it again and again: about log₂ N steps. In a large file, though, most of those steps land on a different page. A search tree whose nodes **are** pages does much better, because one page can hold hundreds of keys and point to hundreds of children. The usual structure is the **B+ tree**: internal nodes hold keys that guide the search, all data sits in the leaves, every leaf is at the same depth, and the leaves are usually linked in key order. Its number of children per node, the **fanout**, is typically 100 or more ([Wikipedia: B+ tree](https://en.wikipedia.org/wiki/B%2B_tree)). It is a variant of the **B-tree**, which Rudolf Bayer and Edward McCreight introduced around 1970 ([Wikipedia: B-tree](https://en.wikipedia.org/wiki/B-tree)).

```python
def levels(items, fanout):
    """Levels a tree needs when every node holds up to `fanout` entries or children."""
    height, reach = 1, fanout
    while reach < items:
        height, reach = height + 1, reach * fanout
    return height

print(f"{'items':>15}{'binary search steps':>22}{'fanout 100':>12}{'fanout 500':>12}")
for items in (1_000, 1_000_000, 1_000_000_000):
    print(f"{items:>15,}{items.bit_length():>22}{levels(items, 100):>12}{levels(items, 500):>12}")
```

```text
          items   binary search steps  fanout 100  fanout 500
          1,000                    10           2           2
      1,000,000                    20           3           3
  1,000,000,000                    30           5           4
```

A billion items are four or five pages deep, and the top levels are small enough to stay cached in memory, so a lookup often costs very few reads from storage.

## 🔨 Building a B+ Tree

The tree below keeps at most `max_keys` keys in a node. An insert walks down to the right leaf. When a node overflows, it **splits** in two: a leaf copies the first key of its new right half up to its parent, while an internal node moves its middle key up. If the root splits, a new root is created above it. That is the only way the tree grows taller, which is why all leaves stay at the same depth.

```python
from bisect import bisect_left, bisect_right

class Node:
    def __init__(self, leaf):
        self.leaf, self.keys, self.next = leaf, [], None     # next: the leaf to the right
        self.values, self.children = [], []                  # values in leaves, children elsewhere

class BPlusTree:
    def __init__(self, max_keys):
        self.max_keys, self.root, self.nodes_read = max_keys, Node(leaf=True), 0

    def _leaf_for(self, key):
        node = self.root
        self.nodes_read += 1
        while not node.leaf:
            node = node.children[bisect_right(node.keys, key)]
            self.nodes_read += 1
        return node

    def get(self, key):
        leaf = self._leaf_for(key)
        i = bisect_left(leaf.keys, key)
        return leaf.values[i] if i < len(leaf.keys) and leaf.keys[i] == key else None

    def scan(self, low, high):
        """Every (key, value) with low <= key <= high, in key order, following the leaf links."""
        leaf = self._leaf_for(low)
        i = bisect_left(leaf.keys, low)
        while leaf is not None:
            while i < len(leaf.keys):
                if leaf.keys[i] > high:
                    return
                yield leaf.keys[i], leaf.values[i]
                i += 1
            leaf, i = leaf.next, 0
            if leaf is not None:
                self.nodes_read += 1

    def put(self, key, value):
        split = self._insert(self.root, key, value)
        if split:                                            # the root split: the tree grows a level
            separator, right = split
            new_root = Node(leaf=False)
            new_root.keys, new_root.children = [separator], [self.root, right]
            self.root = new_root

    def _insert(self, node, key, value):
        """Insert below `node`; if it had to split, return (separator key, new right node)."""
        if node.leaf:
            i = bisect_left(node.keys, key)
            if i < len(node.keys) and node.keys[i] == key:
                node.values[i] = value                       # the key exists: replace its value
                return None
            node.keys.insert(i, key)
            node.values.insert(i, value)
        else:
            i = bisect_right(node.keys, key)
            split = self._insert(node.children[i], key, value)
            if split is None:
                return None
            node.keys.insert(i, split[0])
            node.children.insert(i + 1, split[1])
        if len(node.keys) <= self.max_keys:
            return None
        middle, right = len(node.keys) // 2, Node(node.leaf)
        if node.leaf:
            node.keys, right.keys = node.keys[:middle], node.keys[middle:]
            node.values, right.values = node.values[:middle], node.values[middle:]
            node.next, right.next = right, node.next
            return right.keys[0], right                      # copied up: it also stays in the leaf
        separator = node.keys[middle]                        # moved up: it leaves this level
        node.keys, right.keys = node.keys[:middle], node.keys[middle + 1:]
        node.children, right.children = node.children[:middle + 1], node.children[middle + 1:]
        return separator, right

def shape(tree):
    """(levels, leaves, how full the leaves are on average)."""
    height, node = 1, tree.root
    while not node.leaf:
        height, node = height + 1, node.children[0]
    leaves = keys = 0
    while node is not None:                                  # walk the chain of leaves
        leaves, keys, node = leaves + 1, keys + len(node.keys), node.next
    return height, leaves, keys / (leaves * tree.max_keys)
```

The next block inserts 100,000 keys in two arrival orders, with small and large nodes, and counts the nodes read by one lookup and by a range of 1,000 neighbouring keys:

```python
import random

KEYS = 100_000
ARRIVALS = {"random": random.Random(1).sample(range(KEYS), KEYS), "ascending": range(KEYS)}
print(f"{'max keys':>8}  {'arrival':<10}{'levels':>7}{'leaves':>8}{'leaf fill':>11}{'lookup reads':>14}{'range reads':>13}")
for max_keys in (4, 100):
    for label, keys in ARRIVALS.items():
        tree = BPlusTree(max_keys)
        for key in keys:
            tree.put(key, f"row {key}")
        height, leaves, fill = shape(tree)
        tree.nodes_read = 0
        assert tree.get(54_321) == "row 54321"
        lookup = tree.nodes_read
        tree.nodes_read = 0
        assert [key for key, _ in tree.scan(40_000, 40_999)] == list(range(40_000, 41_000))
        print(f"{max_keys:>8}  {label:<10}{height:>7}{leaves:>8,}{fill:>11.0%}{lookup:>14}{tree.nodes_read:>13}")
```

```text
max keys  arrival    levels  leaves  leaf fill  lookup reads  range reads
       4  random          9  34,344        73%             9          345
       4  ascending      11  49,999        50%            11          511
     100  random          3   1,442        69%             3           18
     100  ascending       3   1,999        50%             3           23
```

With room for only 4 keys per node, 100,000 keys need 9 to 11 levels; with room for 100 keys, only 3. A lookup reads one node per level. Keys that arrive in random order leave the leaves about 70% full, while ascending keys leave them only half full, because after each split no later key ever goes into the left half. With 100-key nodes, a range of 1,000 neighbouring keys reads only 18 to 23 nodes: one path down, then a walk along the chain of leaves. This is why B+ trees suit range queries and ordering.

Deleting keys is left out here: in the textbook algorithm, a node that becomes too empty borrows keys from a neighbour or merges with it ([Wikipedia: B-tree](https://en.wikipedia.org/wiki/B-tree)).

## 🔎 A Real One: SQLite's B-Trees

SQLite stores every table and index as a B-tree, in two variants: **table b-trees**, used for ordinary tables, are keyed by a 64-bit integer **rowid** and keep all row data in their leaves, while **index b-trees** use arbitrary keys and no separate data ([SQLite: Database File Format](https://www.sqlite.org/fileformat2.html)). The `dbstat` virtual table, which is enabled in this build, reports every page of a database ([SQLite: DBSTAT](https://www.sqlite.org/dbstat.html)), so the real trees can be measured:

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE people (id INTEGER PRIMARY KEY, email TEXT NOT NULL, joined INTEGER NOT NULL)")
generator = random.Random(3)
db.executemany("INSERT INTO people (email, joined) VALUES (?, ?)",
               ((f"user{generator.randrange(10**9):09d}@example.com", generator.randrange(10_000))
                for _ in range(100_000)))
db.execute("CREATE INDEX people_by_joined ON people (joined)")
db.execute("CREATE INDEX people_by_email ON people (email)")
print("page size:", db.execute("PRAGMA page_size").fetchone()[0], "bytes")

PAGES_OF = """SELECT pagetype, count(*), sum(ncell), sum(unused), sum(pgsize),
                     max(length(path) - length(replace(path, '/', '')))
              FROM dbstat WHERE name = ? GROUP BY pagetype"""
print(f"{'b-tree':<17}{'levels':>7}{'leaf pages':>11}{'inner pages':>12}{'leaf fill':>10}"
      f"{'entries per leaf':>17}{'entries above leaves':>21}")
for name in ("people", "people_by_joined", "people_by_email"):
    found = {kind: rest for kind, *rest in db.execute(PAGES_OF, (name,))}
    leaf_pages, in_leaves, unused, size, height = found["leaf"]
    inner_pages = found["internal"][0]
    print(f"{name:<17}{height:>7}{leaf_pages:>11,}{inner_pages:>12}{1 - unused / size:>10.0%}"
          f"{in_leaves / leaf_pages:>17.0f}{100_000 - in_leaves:>21,}")
```

```text
page size: 4096 bytes
b-tree            levels leaf pages inner pages leaf fill entries per leaf entries above leaves
people                 3        906           3       99%              110                    0
people_by_joined       2        261           1      100%              382                  260
people_by_email        3        820           9      100%              121                  819
```

What the numbers show:

- In the table b-tree, all 100,000 rows are in the leaves, as in a B+ tree. In the two index b-trees, a few hundred of the 100,000 entries sit in inner pages, as in a classic B-tree.
- **Key size matters.** A leaf holds about 382 entries of the index on the small integer `joined`, but only 121 entries of the index on the long `email` strings. Fewer entries per page means more pages, and sooner another level: the email index is already 3 levels deep, while the `joined` index has 2.
- The leaves are 99% to 100% full, far better than the simple halving above: the rowids arrived in ascending order, and both indexes were built after the rows were loaded. PostgreSQL also packs pages: it fills B-tree leaf pages to its fillfactor, 90% by default, when it builds an index and when new largest keys arrive ([PostgreSQL: CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)).

With a few hundred entries or children per page, even a billion rows are only about four or five levels deep, as the first table suggested.

## 📍 Where the Rows Live

If a table's rows are **stored in the order of an index key**, that index is **clustered**. Since rows can be physically ordered only one way, a table has at most one clustered index, while it can have many **secondary** (non-clustered) indexes that point at rows stored elsewhere ([Wikipedia: Database index](https://en.wikipedia.org/wiki/Database_index)).

- A normal SQLite table is a table b-tree keyed by its rowid, so the rows are clustered by rowid. A [`WITHOUT ROWID`](https://www.sqlite.org/withoutrowid.html) table is instead clustered on its primary key.
- Each entry of a SQLite index holds the indexed columns followed by the **row's key** (the rowid, or the primary key of a `WITHOUT ROWID` table). Unless the index already contains every column that the query needs, finding a row through it takes a **second search**, in the table ([SQLite: WITHOUT ROWID](https://www.sqlite.org/withoutrowid.html), [File Format](https://www.sqlite.org/fileformat2.html)).
- PostgreSQL stores every index separately from the table's rows (the **heap**), so an ordinary index scan reads both ([PostgreSQL: Index-Only Scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)).

An index that contains every column a query uses is a **covering index**, and it can answer without visiting the table; [data-modeling.md](../introduction-to-dbms/data-modeling.md) showed SQLite reporting `USING COVERING INDEX`. PostgreSQL calls the technique an index-only scan; it also depends on a **visibility map** that records which table pages need no further checking ([PostgreSQL: Index-Only Scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)).

## 🧰 Other Index Structures

| Structure | Good at | Notes |
|-----------|---------|-------|
| **B-tree / B+ tree** | equality, ranges, and returning rows in order | the usual default |
| **Hash** | equality only | PostgreSQL's hash index handles only the `=` comparison ([PostgreSQL: Index Types](https://www.postgresql.org/docs/current/indexes-types.html)) |
| **Inverted** (GIN) | values with many parts, such as arrays, JSON documents, and words in text | one entry per part, pointing at every row that contains it ([PostgreSQL: Index Types](https://www.postgresql.org/docs/current/indexes-types.html)) |
| **GiST** | a framework for other searches, such as nearest neighbours among points | the same page |
| **BRIN** | very large tables whose values follow the physical row order, such as timestamps | stores only a summary per range of pages (the same page) |
| **Bitmap** | columns with very few distinct values, mostly in analytics | answers conditions with bit operations ([Wikipedia: Database index](https://en.wikipedia.org/wiki/Database_index)) |
| **LSM tree** | heavy streams of writes | described below |

## 📝 Log-Structured Merge-Trees

A B-tree changes its pages where they are. A **log-structured merge-tree** (LSM tree) instead collects writes in memory and writes them out in large sorted batches, which turns many small random writes into sequential ones ([Wikipedia: LSM tree](https://en.wikipedia.org/wiki/Log-structured_merge-tree)). LevelDB and Cassandra work this way ([LevelDB: implementation notes](https://github.com/google/leveldb/blob/main/doc/impl.md), [Cassandra: Storage Engine](https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html)):

1. A write is appended to a **log** (for recovery) and put in an in-memory **memtable**.
2. A full memtable is written to disk as a **sorted run** that never changes afterwards.
3. A **delete** writes a **tombstone**, a marker that hides older values.
4. A read checks the memtable and then the runs from newest to oldest. Stores such as Cassandra use **Bloom filters** to skip runs that cannot hold the key.
5. **Compaction** merges runs, keeping the newest value for each key and dropping what is hidden.

The miniature below has no log or Bloom filters, and its compaction merges all runs at once when there are too many. It counts the entries written to "disk" and the runs searched by lookups:

```python
TOMBSTONE = object()

class MiniLSM:
    def __init__(self, memtable_limit, max_runs):
        self.memtable, self.runs = {}, []                     # runs: oldest first, each sorted by key
        self.memtable_limit, self.max_runs = memtable_limit, max_runs
        self.written = self.searched = 0
    def put(self, key, value):
        self.memtable[key] = value                            # a real store appends to a log first
        if len(self.memtable) >= self.memtable_limit:
            self.flush()
    def delete(self, key):
        self.put(key, TOMBSTONE)
    def flush(self):
        self.runs.append(sorted(self.memtable.items()))
        self.written += len(self.memtable)
        self.memtable = {}
        if len(self.runs) > self.max_runs:
            self.compact()
    def compact(self):
        newest = {}
        for run in self.runs:                                 # oldest first, so newer entries win
            newest.update(run)
        merged = sorted((key, value) for key, value in newest.items() if value is not TOMBSTONE)
        self.written += len(merged)                           # dropping tombstones is safe: all runs merged
        self.runs = [merged]
    def get(self, key):
        if key in self.memtable:
            value = self.memtable[key]
        else:
            value = None
            for run in reversed(self.runs):                   # newest first: the first match wins
                self.searched += 1
                i = bisect_left(run, (key,))
                if i < len(run) and run[i][0] == key:
                    value = run[i][1]
                    break
        return None if value is TOMBSTONE else value

print(f"{'compact when runs exceed':<26}{'entries written per write':>28}{'runs searched per lookup':>26}{'runs now':>10}")
for max_runs in (1, 4, 16):
    store, expected, generator = MiniLSM(memtable_limit=100, max_runs=max_runs), {}, random.Random(6)
    for step in range(30_000):                                # 30,000 writes to 5,000 keys, 15% deletes
        key = generator.randrange(5_000)
        if generator.random() < 0.15:
            store.delete(key)
            expected.pop(key, None)
        else:
            store.put(key, step)
            expected[key] = step
    lookups = [generator.randrange(6_000) for _ in range(2_000)]       # some keys were never written
    assert all(store.get(key) == expected.get(key) for key in lookups)
    print(f"{max_runs:<26}{store.written / 30_000:>28.1f}{store.searched / len(lookups):>26.1f}{len(store.runs):>10}")
print("every lookup matched a plain dictionary")
```

```text
compact when runs exceed     entries written per write  runs searched per lookup  runs now
1                                                 36.2                       1.0         1
4                                                  9.7                       3.8         4
16                                                 3.2                       7.4         8
every lookup matched a plain dictionary
```

Allowing only one run made compaction rewrite the same data again and again: about 36 entries went to disk for every write (**write amplification**), but a lookup searched only one run. Allowing up to 16 runs cut that to about 3, but a lookup then searched about 7 runs on average.

This is the basic trade-off of storage engines: work done while writing, against work done while reading, and the disk space held by old versions.

## 💸 What an Index Costs

Every index is a second structure that must be stored and kept up to date: inserting or deleting a row adds or removes an entry in every ordinary index on the table, and an update must change at least the indexes whose columns it changes. The measurements above show the space: the two indexes together take 1,091 pages, more than the 909 pages of the table itself. That is why you add an index for the queries that need it, not for every column ([indexes.md](../../../backend/sql-fundamentals/indexes.md), [MongoDB indexing](../../../backend/mongodb-fundamentals/indexing.md)). One rule of thumb from the SQLite documentation: do not keep two indexes where one is a **prefix** of the other, since the longer one can do the work of both ([SQLite: Query Planning](https://www.sqlite.org/queryplanner.html)).

## ✅ Checking the Code

A separate checker compared the B+ tree with a sorted dictionary on 600 random trees with 2 to 11 keys per node (about 116,000 inserts, 36,000 lookups, and 36,000 range scans). It confirmed that keys stayed sorted, that every leaf was at the same depth, that every node except the root stayed at least half full, and that the chain of leaves matched the tree; every lookup read one node per level. In SQLite's trees, every row had exactly one entry and the page counts were consistent. The miniature LSM store matched a dictionary on 400 random workloads with deletes, before and after compaction.

## Common Misconceptions

- **"A B+ tree is a kind of binary tree."** Its nodes have many children, often hundreds, which is the whole point.
- **"A hash index is always faster than a B-tree."** It supports only equality, with no ranges or ordering.
- **"A secondary index holds the whole row."** It usually holds the indexed columns and a way to find the row, such as its key, so other columns need a second lookup.
- **"More indexes make a database faster."** Each one speeds up some reads and slows down writes.
- **"LSM trees are simply better than B-trees."** They trade cheaper writes for extra work on reads and during compaction.

## ➡️ Next

An index helps only when the database decides to use it. Continue to [query-optimisation.md](query-optimisation.md).
