# 🚦 Concurrency Control

## What Must Be Guaranteed?

A database runs many transactions at once and must make the result as if they had run in some one-at-a-time order. To reason about that, we look at a **schedule**: the order in which the reads and writes of several transactions actually happen. A schedule is **serial** when each transaction finishes before the next starts, and **serializable** when it is equivalent in its outcome to some serial schedule ([Wikipedia: Database transaction schedule](https://en.wikipedia.org/wiki/Database_transaction_schedule)). All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); every result is deterministic.

## ⚔️ Conflicts and the Precedence Graph

Two actions **conflict** if they belong to different transactions, touch the same item, and at least one of them writes it: read–write, write–read, and write–write. Swapping two actions that do not conflict changes nothing, so a schedule that orders every conflicting pair as some serial schedule does is **conflict-serializable**. There is a simple test: draw a **precedence graph** with an arrow from Ti to Tj whenever an action of Ti comes before a conflicting action of Tj; the schedule is conflict-serializable exactly when this graph, built from the committed transactions, has **no cycle** (the same article):

```python
def conflicting_pairs(schedule):
    """(Ti, Tj) for every action of Ti that comes before a conflicting action of Tj. Actions are (txn, "r"/"w", item)."""
    for position, (first, kind1, item1) in enumerate(schedule):
        for second, kind2, item2 in schedule[position + 1:]:
            if first != second and item1 == item2 and "w" in (kind1, kind2):
                yield first, second

def conflict_serializable(schedule):
    graph = {transaction: set() for transaction, _, _ in schedule}
    for first, second in conflicting_pairs(schedule):
        graph[first].add(second)
    state = {}
    def on_a_cycle(node):
        state[node] = "visiting"
        for following in graph[node]:
            if state.get(following) == "visiting" or (following not in state and on_a_cycle(following)):
                return True
        state[node] = "done"
        return False
    return not any(node not in state and on_a_cycle(node) for node in graph)

lost_update = [("T1", "r", "x"), ("T2", "r", "x"), ("T1", "w", "x"), ("T2", "w", "x")]
interleaved = [("T1", "r", "x"), ("T1", "w", "x"), ("T2", "r", "x"), ("T1", "r", "y"), ("T2", "w", "x"), ("T1", "w", "y")]
for label, schedule in (("lost update", lost_update), ("another interleaving", interleaved)):
    edges = sorted(set(conflicting_pairs(schedule)))
    print(f"{label:<21} arrows {edges}  conflict-serializable: {conflict_serializable(schedule)}")
```

```text
lost update           arrows [('T1', 'T2'), ('T2', 'T1')]  conflict-serializable: False
another interleaving  arrows [('T1', 'T2')]  conflict-serializable: True
```

In the lost update, T1 read before T2 wrote, and T2 read before T1 wrote: the arrows point both ways, so no serial order can explain the schedule. In the second schedule every conflict points from T1 to T2, so it is equivalent to running T1 first.

## 🔐 Two-Phase Locking

Checking schedules after the fact is too late; a database needs a rule that only ever **produces** serializable ones. **Two-phase locking (2PL)** is such a rule: a pessimistic method that guarantees conflict-serializability. A transaction locks data before using it, with shared locks for reading and exclusive locks for writing, and does it in two phases: an **expanding** phase in which it only acquires locks, and a **shrinking** phase in which it only releases them ([Wikipedia: Two-phase locking](https://en.wikipedia.org/wiki/Two-phase_locking)). **Strict** 2PL keeps write locks until the transaction ends, and **strong strict** 2PL keeps every lock until the end, which also gives strictness and prevents dirty reads (the same article).

The next block runs strong strict 2PL on every possible interleaving of two small programs. A step whose lock is held by someone else has to wait; if every remaining transaction is waiting, that is a **deadlock**, the same circular wait as in [deadlocks.md](../../operating-systems/deadlocks-and-concurrency/deadlocks.md). PostgreSQL, for example, detects deadlocks automatically and resolves them by aborting one of the transactions involved ([PostgreSQL documentation: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)):

```python
def strict_2pl_runs(programs):
    """Every way the programs can run under strong strict 2PL (all locks held until commit).
    A program is a list of ("r", item) / ("w", item); it commits after its last action.
    Returns (the completed schedules, the number of ways of ending in a deadlock)."""
    completed, deadlocks = [], 0

    def explore(next_step, locks, schedule):
        nonlocal deadlocks
        if all(step > len(programs[t]) for t, step in enumerate(next_step)):
            completed.append(schedule)
            return
        progressed = False
        for t, step in enumerate(next_step):
            if step > len(programs[t]):
                continue
            advanced = next_step[:t] + (step + 1,) + next_step[t + 1:]
            if step == len(programs[t]):                      # commit: release all of t's locks
                released = {item: {o: m for o, m in held.items() if o != t} for item, held in locks.items()}
                explore(advanced, released, schedule)
                progressed = True
                continue
            kind, item = programs[t][step]
            held = locks.get(item, {})
            blocked = any(owner != t and (kind == "w" or mode == "w") for owner, mode in held.items())
            if not blocked:
                mode = "w" if kind == "w" or held.get(t) == "w" else "r"
                explore(advanced, {**locks, item: {**held, t: mode}}, schedule + [(f"T{t + 1}", kind, item)])
                progressed = True
        if not progressed:
            deadlocks += 1

    explore(tuple(0 for _ in programs), {}, [])
    return completed, deadlocks

increment = [("r", "x"), ("w", "x")]
transfer_ab = [("w", "a"), ("w", "b")]
transfer_ba = [("w", "b"), ("w", "a")]
for label, programs in (("two increments of x", [increment, increment]),
                        ("transfers locking a, b and b, a", [transfer_ab, transfer_ba]),
                        ("transfers both locking a, then b", [transfer_ab, transfer_ab])):
    completed, deadlocks = strict_2pl_runs(programs)
    print(f"{label:<34} completed runs: {len(completed)}, all conflict-serializable: "
          f"{all(conflict_serializable(s) for s in completed)}, runs ending in deadlock: {deadlocks}")
```

```text
two increments of x                completed runs: 2, all conflict-serializable: True, runs ending in deadlock: 2
transfers locking a, b and b, a    completed runs: 2, all conflict-serializable: True, runs ending in deadlock: 2
transfers both locking a, then b   completed runs: 2, all conflict-serializable: True, runs ending in deadlock: 0
```

Every run that completes is serializable; the price is blocking and deadlock. The two increments deadlock in a way that is easy to miss: both take a **shared** lock to read, and then each needs an **exclusive** lock that the other's shared lock prevents. (Where it is supported, `SELECT ... FOR UPDATE` locks the selected rows as if for an update at the moment they are read, which the same PostgreSQL page describes.) The transfers that lock their accounts in opposite orders can deadlock too, and ordering the locks the same way in every transaction removes the deadlock, the lock-ordering rule of [deadlock-prevention.md](../../operating-systems/deadlocks-and-concurrency/deadlock-prevention.md).

## 🌗 Optimistic Control and Multiple Versions

Locking is not the only way:

- **Optimistic concurrency control** lets transactions run without locks and checks, before committing, that no other transaction has modified the data it read; if one has, the committing transaction rolls back and may be restarted. It was proposed by Kung and Robinson in 1979 and suits workloads where conflicts are rare ([Wikipedia: Optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)). The serializable level of the previous lesson's simulator works this way.
- **Multiversion concurrency control (MVCC)** keeps several versions of a data item, so that each user sees a snapshot of the database at an instant, and a writer's changes are not visible to others until it commits; this avoids the contention of making readers wait for writers ([Wikipedia: Multiversion concurrency control](https://en.wikipedia.org/wiki/Multiversion_concurrency_control)). Snapshot isolation is usually built on it.

## 🗝️ How SQLite Does It

SQLite locks the whole database file and moves through five states ([SQLite: File locking and concurrency](https://www.sqlite.org/lockingv3.html)):

| State | Meaning |
|-------|---------|
| **UNLOCKED** | no lock held |
| **SHARED** | reading; many connections can hold it at once, and nobody can write the file |
| **RESERVED** | planning to write; only one connection at a time, and new readers are still admitted |
| **PENDING** | waiting to write; existing readers may finish, but no new shared locks are granted |
| **EXCLUSIVE** | writing the file; no other lock of any kind |

This explains the rollback-journal behaviour of [transactions-and-acid.md](transactions-and-acid.md): the writer held a RESERVED lock while the reader read, could not get the EXCLUSIVE lock for its commit while the reader's SHARED lock remained, and succeeded once the reader finished. WAL mode changes this: writes go to a separate log, so readers do not block the writer and the writer does not block readers ([SQLite: Write-ahead logging](https://www.sqlite.org/wal.html)).

## ✅ Checking the Code

The precedence-graph test agreed with the definition (some serial order keeps every conflicting pair in the same order) on 20,000 random schedules. All 213,048 schedules that strict two-phase locking completed for 3,000 random sets of programs were conflict-serializable, and 343 of the sets could end in a deadlock.

## Common Misconceptions

- **"Serializable means transactions run one at a time."** It means the result is as if they had; they may well run concurrently.
- **"Two-phase locking is the same as two-phase commit."** 2PL is a concurrency control method; two-phase commit is a protocol for committing across several systems.
- **"Locks guarantee no deadlocks."** 2PL guarantees serializability, and it can deadlock.
- **"MVCC means no locks at all."** It removes much of the waiting between readers and writers; writers can still conflict with each other.

## ➡️ Next

This completes the Transactions and ACID module: what a transaction promises, the anomalies that isolation levels allow or forbid, and the mechanisms that enforce them. The next module of this section, [Database Classification and Optimisation](../classification-and-optimisation/README.md), looks at the kinds of database there are and how queries are made fast.
