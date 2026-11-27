# 🪟 Isolation Levels and Anomalies

## Why Not Always Isolate Completely?

Isolation determines how much of one transaction others can see. A lower isolation level lets more users work with the same data at the same time but exposes them to more concurrency effects; a higher level prevents more of them, but needs more resources and makes it likelier that one transaction blocks another ([Wikipedia: Isolation](https://en.wikipedia.org/wiki/Isolation_(database_systems))). Databases therefore offer levels, and the default is often not the strongest one. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); every result is deterministic.

## 👻 The Anomalies

| Anomaly | What goes wrong |
|---------|-----------------|
| **Dirty read** | a transaction reads data written by another transaction that has not committed |
| **Non-repeatable read** | a transaction reads a value again and finds that another committed transaction has changed it |
| **Phantom read** | a transaction repeats a query and finds that a committed transaction has changed which rows match |
| **Lost update** | two transactions read a value and both write a new one based on it; one change disappears |
| **Write skew** | two transactions read the same data, then update *different* items, each unaware of the other, and together break a rule |
| **Serialization anomaly** | the committed result matches no order of running the transactions one at a time |

The definitions of dirty, non-repeatable, phantom, and serialization anomaly follow the [PostgreSQL documentation](https://www.postgresql.org/docs/current/transaction-iso.html), and write skew is described in [Wikipedia: Snapshot isolation](https://en.wikipedia.org/wiki/Snapshot_isolation). The SQL standard defines four isolation levels. **Serializable** is defined by its effect: any concurrent execution of serializable transactions must give the same result as running them one at a time in some order. The other three are defined by anomalies that must not occur. PostgreSQL's table, which also lists serialization anomalies, reads ([PostgreSQL documentation: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)):

| Level | Dirty read | Non-repeatable read | Phantom read | Serialization anomaly |
|-------|------------|---------------------|--------------|-----------------------|
| Read uncommitted | allowed, but not in PostgreSQL | possible | possible | possible |
| Read committed | not possible | possible | possible | possible |
| Repeatable read | not possible | not possible | allowed, but not in PostgreSQL | possible |
| Serializable | not possible | not possible | not possible | not possible |

The standard says which anomalies must **not** happen, so a database may prevent more. In PostgreSQL, *read uncommitted* behaves like *read committed*, and its *repeatable read* does not allow phantoms; read committed is its default (same page). Names are not guarantees across products: check what your database's level actually promises.

## 🧪 A Simulator That Tries Every Interleaving

The best way to see why a level allows an anomaly is to try **every** order in which the steps of two transactions can happen. The classes below are a small model of a database with four levels:

- **read uncommitted:** a write is visible to everyone at once (and undone if the transaction aborts);
- **read committed:** writes stay private until commit; each read sees the latest committed data;
- **snapshot:** a transaction reads from a snapshot taken at its first operation, and commits only if nobody else has since committed a change to anything it writes (the *first committer wins*);
- **serializable:** like snapshot, but the commit also fails if anything the transaction **read** has been changed by a later commit, including rows that would match its search conditions.

Real databases implement levels with locks or versions in different ways ([concurrency-control.md](concurrency-control.md)); this model captures what each level lets a transaction see.

```python
LEVELS = ("read uncommitted", "read committed", "snapshot", "serializable")

class Database:
    def __init__(self, rows, level):
        self.rows, self.level = dict(rows), level
        self.commits = []                                   # one list of (key, old, new) per committed transaction

class Transaction:
    def __init__(self, db):
        self.db, self.start = db, None
        self.writes, self.undo = {}, []                     # private writes; undo records for "read uncommitted"
        self.read_keys, self.conditions = set(), []
        self.status = "active"

    def begin(self):
        if self.start is None:                              # like a deferred BEGIN: starts at the first operation
            self.start = len(self.db.commits)
            self.snapshot = dict(self.db.rows)

    def view(self):
        snapshotted = self.db.level in ("snapshot", "serializable")
        rows = dict(self.snapshot if snapshotted else self.db.rows)
        rows.update(self.writes)
        return rows

    def read(self, key):
        self.begin()
        self.read_keys.add(key)
        return self.view().get(key)

    def count(self, condition):
        self.begin()
        self.conditions.append(condition)
        return sum(1 for value in self.view().values() if condition(value))

    def write(self, key, value):
        self.begin()
        if self.db.level == "read uncommitted":
            self.undo.append((key, self.db.rows.get(key)))
            self.db.rows[key] = value                       # visible to everybody at once
        self.writes[key] = value

    def conflicts(self):
        later = [change for commit in self.db.commits[self.start:] for change in commit]
        if self.db.level == "snapshot":
            return any(key in self.writes for key, _, _ in later)
        if self.db.level == "serializable":
            return any(key in self.writes or key in self.read_keys
                       or any((old is not None and c(old)) or (new is not None and c(new)) for c in self.conditions)
                       for key, old, new in later)
        return False

    def commit(self):
        self.begin()
        if self.conflicts():
            self.status = "aborted"
            return
        changes = [(key, self.db.rows.get(key), value) for key, value in self.writes.items()]
        if self.db.level != "read uncommitted":
            self.db.rows.update(self.writes)
        self.db.commits.append(changes)
        self.status = "committed"

    def abort(self):
        self.begin()
        for key, old in reversed(self.undo):
            if old is None:
                del self.db.rows[key]
            else:
                self.db.rows[key] = old
        self.status = "aborted"

def interleavings(lengths):
    """Every order in which the steps of several transactions can happen."""
    if not any(lengths):
        yield ()
        return
    for i, remaining in enumerate(lengths):
        if remaining:
            rest = lengths[:i] + (remaining - 1,) + lengths[i + 1:]
            for order in interleavings(rest):
                yield (i,) + order

def run(rows, programs, order, level):
    db = Database(rows, level)
    transactions = [Transaction(db) for _ in programs]
    memory = [{} for _ in programs]
    next_step = [0] * len(programs)
    for i in order:
        programs[i][next_step[i]](transactions[i], memory[i])
        next_step[i] += 1
    return db, transactions, memory
```

Each anomaly is written as two small programs, one step per database operation, plus a test that decides whether the anomaly happened in a particular run:

```python
def keep(name, operation):
    def step(t, m):
        m[name] = operation(t, m)
    return step

def act(operation):
    return lambda t, m: operation(t, m)

COMMIT = act(lambda t, m: t.commit())
ABORT = act(lambda t, m: t.abort())
is_big = lambda salary: salary > 100
increment = [keep("x", lambda t, m: t.read("x")), act(lambda t, m: t.write("x", m["x"] + 1)), COMMIT]

def go_off_call(name):
    return [keep("on_call", lambda t, m: t.count(lambda status: status == "on call")),
            act(lambda t, m: m["on_call"] >= 2 and t.write(name, "off")), COMMIT]

SCENARIOS = {
    "dirty read": ({"x": 50},
        [[act(lambda t, m: t.write("x", 100)), ABORT], [keep("seen", lambda t, m: t.read("x")), COMMIT]],
        lambda db, ts, m: m[1]["seen"] == 100),
    "non-repeatable read": ({"x": 50},
        [[keep("first", lambda t, m: t.read("x")), keep("second", lambda t, m: t.read("x")), COMMIT],
         [act(lambda t, m: t.write("x", 70)), COMMIT]],
        lambda db, ts, m: ts[0].status == "committed" and m[0]["first"] != m[0]["second"]),
    "phantom read": ({"ada": 120, "lin": 90},
        [[keep("first", lambda t, m: t.count(is_big)), keep("second", lambda t, m: t.count(is_big)), COMMIT],
         [act(lambda t, m: t.write("sam", 150)), COMMIT]],
        lambda db, ts, m: ts[0].status == "committed" and m[0]["first"] != m[0]["second"]),
    "lost update": ({"x": 10}, [increment, increment],
        lambda db, ts, m: all(t.status == "committed" for t in ts) and db.rows["x"] != 12),
    "write skew": ({"ada": "on call", "lin": "on call"}, [go_off_call("ada"), go_off_call("lin")],
        lambda db, ts, m: all(t.status == "committed" for t in ts) and "on call" not in db.rows.values()),
}

print(f"{'anomaly':<21}" + "".join(f"{level:>18}" for level in LEVELS))
for name, (rows, programs, happened) in SCENARIOS.items():
    orders = list(interleavings(tuple(len(p) for p in programs)))
    cells = [f"{sum(happened(*run(rows, programs, order, level)) for order in orders)} of {len(orders)}" for level in LEVELS]
    print(f"{name:<21}" + "".join(f"{cell:>18}" for cell in cells))
```

```text
anomaly                read uncommitted    read committed          snapshot      serializable
dirty read                       2 of 6            0 of 6            0 of 6            0 of 6
non-repeatable read             3 of 10           2 of 10           0 of 10           0 of 10
phantom read                    3 of 10           2 of 10           0 of 10           0 of 10
lost update                    12 of 20          18 of 20           0 of 20           0 of 20
write skew                     12 of 20          18 of 20          18 of 20           0 of 20
```

Each cell counts the interleavings in which the anomaly occurred. The pattern matches the theory:

- **Dirty reads** happen only at *read uncommitted*.
- **Non-repeatable reads** and **phantom reads** disappear once a transaction reads from a snapshot.
- **Lost updates** survive *read committed*, because each transaction saw committed data and still overwrote the other. Under *snapshot*, the second committer is aborted.
- **Write skew** survives even *snapshot* isolation: the two transactions write **different** rows, so no write conflicts, yet together they leave nobody on call. Only the serializable check, which also looks at what was read, stops it. Snapshot isolation is popular because it performs well and avoids most of the anomalies that serializability avoids, but not all ([Wikipedia: Snapshot isolation](https://en.wikipedia.org/wiki/Snapshot_isolation)).

No cell reaches the total number of interleavings: in the serial ones, where one transaction finishes before the other starts, no anomaly can happen at any level.

## 🔁 The Price: Aborted Transactions

Stopping an anomaly by refusing a commit means that someone must **try again**. Counting the interleavings in which a transaction was aborted shows the cost:

```python
for name in ("lost update", "write skew"):
    rows, programs, _ = SCENARIOS[name]
    orders = list(interleavings(tuple(len(p) for p in programs)))
    for level in ("read committed", "snapshot", "serializable"):
        aborted = sum(any(t.status == "aborted" for t in run(rows, programs, order, level)[1]) for order in orders)
        print(f"{name:<12} {level:<16} a transaction had to be aborted in {aborted:>2} of {len(orders)} interleavings")
```

```text
lost update  read committed   a transaction had to be aborted in  0 of 20 interleavings
lost update  snapshot         a transaction had to be aborted in 18 of 20 interleavings
lost update  serializable     a transaction had to be aborted in 18 of 20 interleavings
write skew   read committed   a transaction had to be aborted in  0 of 20 interleavings
write skew   snapshot         a transaction had to be aborted in  0 of 20 interleavings
write skew   serializable     a transaction had to be aborted in 18 of 20 interleavings
```

An application that uses strong isolation must therefore be written to **retry** a transaction that fails, from the beginning, including its reads. That is a small price for never having to reason about anomalies. The alternatives at weaker levels are to lock explicitly what you read, for example with `SELECT ... FOR UPDATE` where the database supports it ([PostgreSQL documentation: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)), or to make a single statement do the whole update, as `UPDATE accounts SET balance = balance + 1` does.

## ✅ Checking the Code

The simulator was checked with 1,500 random sets of transaction programs (reads, writes, and decisions based on counting rows) in 268,803 interleavings. At the serializable level, every run gave the same final data and the same values read as some one-at-a-time run of its committed transactions. The same programs did produce results that no serial order explains at read committed and at snapshot; no transaction at read committed or above ever read uncommitted data; and under snapshot and serializable, repeated reads of an unchanged item gave the same value.

## Common Misconceptions

- **"Isolation levels with the same name behave the same everywhere."** The standard sets minimum guarantees; products differ, and some levels are stronger than their names require.
- **"Read committed prevents lost updates."** It only prevents reading uncommitted data.
- **"Snapshot isolation is serializable."** It allows write skew.
- **"The default level is the safest one."** It often is not; PostgreSQL's default is read committed.
- **"A failed commit means something is broken."** At strong levels it is how conflicts are reported; retry the transaction.

## ➡️ Next

Continue to [concurrency-control.md](concurrency-control.md): how a database actually enforces isolation, what "serializable" means precisely, and how locks and versions achieve it.
