# 🔁 Transactions and ACID

## 📚 Overview

A database is shared, and things fail in the middle. **Transactions** are how a database keeps data correct anyway: a group of operations that happens completely or not at all, leaves the data in a valid state, does not trip over other transactions, and is not lost once it is committed. These four promises are called **ACID**. This module tests them instead of just stating them, and shows where the details matter: a failed statement that does not undo its transaction, a commit that can be refused, readers that see snapshots, and isolation levels that quietly allow anomalies.

The module starts with ACID in SQLite from Python, with experiments for atomicity, consistency, isolation, and durability, including a constraint error followed by a careless commit that creates money, two journal modes that make readers and writers behave differently, and the limits of durability when the power fails. It then studies **isolation levels and anomalies** (dirty reads, non-repeatable reads, phantoms, lost updates, and write skew) with a small simulator that tries every interleaving of two transactions at four levels. It ends with **concurrency control**: schedules and conflict-serializability, two-phase locking and its deadlocks, optimistic and multiversion methods, and SQLite's lock states. The code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54, and the simulator and the locking model were checked against independent references on thousands of random programs.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Define a transaction and each ACID property, and say which parts the database guarantees and which parts the transaction's code must get right.
- Use `BEGIN`, `COMMIT`, and `ROLLBACK` correctly, including after a failing statement and a refused commit.
- Explain what another connection can see while a transaction runs, and how SQLite's rollback-journal and WAL modes differ.
- Explain durability against a program crash and against a power failure, and the role of settings and logs.
- Name the concurrency anomalies, say which isolation levels allow which, and explain write skew and snapshot isolation.
- Decide whether a schedule is conflict-serializable, and explain two-phase locking, its deadlocks, optimistic control, and multiversion control.

## 📋 Prerequisites

- [Introduction to DBMS](../introduction-to-dbms/README.md): why transactions exist, and recovery after a crash.
- [The Relational Model](../the-relational-model/README.md): tables, keys, and constraints.
- Helpful: the race conditions, locks, and deadlocks of the [Deadlocks and Concurrency](../../operating-systems/deadlocks-and-concurrency/README.md) module.
- Basic Python reading ability: functions, classes, context managers, and the `sqlite3` module at an introductory level.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [transactions-and-acid.md](transactions-and-acid.md) | Atomicity (including the failed-statement trap), consistency, isolation with two connections and two journal modes, write skew refused by SQLite, and durability against crashes and power failures |
| [isolation-levels.md](isolation-levels.md) | The anomalies, the SQL standard's levels as PostgreSQL implements them, a simulator that tries every interleaving at four levels, and the cost of aborted transactions |
| [concurrency-control.md](concurrency-control.md) | Schedules, conflicts and the precedence graph, two-phase locking and deadlocks, optimistic and multiversion control, and SQLite's lock states |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [transactions-and-acid.md](transactions-and-acid.md) if you write code that uses a database: the failed-statement trap and the refused commit cause real bugs. For interviews and exams, practise [isolation-levels.md](isolation-levels.md) (which level allows which anomaly) and the precedence graph in [concurrency-control.md](concurrency-control.md).

**Skim** the simulator's classes in [isolation-levels.md](isolation-levels.md) if you only need the table, but change a scenario and rerun it once: it is the quickest way to see why write skew slips past snapshot isolation.

## 🧠 Knowledge Check

<details>
<summary>In a money transfer, the second UPDATE fails with a constraint violation. The program catches the exception and then calls COMMIT. What happens in SQLite, and what should the code do?</summary>

SQLite undoes only the **failing statement** (its default conflict handling, which matches the SQL standard) and leaves the transaction open with the earlier changes in place, so committing keeps the first update: in the experiment, the credit was kept without the matching debit and the total money grew. Atomicity protects the transaction as a whole only if the program **rolls back** when anything fails. A context manager that commits on success and rolls back on any error (including a refused `COMMIT`) does this every time; [transactions-and-acid.md](transactions-and-acid.md) shows both versions.

</details>

<details>
<summary>Two doctors are on call, and at least one must stay. Under snapshot isolation, two transactions each check that two doctors are on call and then take a different doctor off call. What happens, why does "first committer wins" not stop it, and what would?</summary>

Both transactions read the same snapshot (two on call), each updates a **different** row, and both commit, leaving nobody on call. This is **write skew**. First committer wins only rejects a transaction that writes something another has changed, and these two write sets do not overlap. Stopping it needs a level that also checks what was **read** (serializable), or a way to turn the hidden conflict into a visible one: lock the rows you base a decision on (for example `SELECT ... FOR UPDATE` where supported), or **materialize the conflict** by having both transactions update a shared row. A transaction rejected this way must be retried. [isolation-levels.md](isolation-levels.md) counts how often each level lets it happen.

</details>

## 📚 References

- [Wikipedia: ACID](https://en.wikipedia.org/wiki/ACID), [Database transaction](https://en.wikipedia.org/wiki/Database_transaction), [Isolation](https://en.wikipedia.org/wiki/Isolation_(database_systems)), [Snapshot isolation](https://en.wikipedia.org/wiki/Snapshot_isolation), and [Database transaction schedule](https://en.wikipedia.org/wiki/Database_transaction_schedule).
- [Wikipedia: Two-phase locking](https://en.wikipedia.org/wiki/Two-phase_locking), [Optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control), [Multiversion concurrency control](https://en.wikipedia.org/wiki/Multiversion_concurrency_control), and [Write-ahead logging](https://en.wikipedia.org/wiki/Write-ahead_logging).
- Hal Berenson, Phil Bernstein, Jim Gray, and others, [A Critique of ANSI SQL Isolation Levels](https://arxiv.org/abs/cs/0701157): why the standard's definitions leave anomalies such as write skew uncovered.
- PostgreSQL documentation: [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) and [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html).
- SQLite documentation: [Transactions](https://www.sqlite.org/lang_transaction.html), [Isolation](https://www.sqlite.org/isolation.html), [Conflict resolution](https://www.sqlite.org/lang_conflict.html), [File locking and concurrency](https://www.sqlite.org/lockingv3.html), [Write-ahead logging](https://www.sqlite.org/wal.html), [Atomic commit](https://www.sqlite.org/atomiccommit.html), and [`PRAGMA synchronous`](https://www.sqlite.org/pragma.html#pragma_synchronous).
- [Python docs: `sqlite3`](https://docs.python.org/3/library/sqlite3.html).
- [GeeksforGeeks: ACID Properties](https://www.geeksforgeeks.org/dbms/acid-properties-in-dbms/), [Transaction Isolation Levels](https://www.geeksforgeeks.org/dbms/transaction-isolation-levels-dbms/), [Two-Phase Locking](https://www.geeksforgeeks.org/dbms/two-phase-locking-protocol/), and [Conflict Serializability](https://www.geeksforgeeks.org/dbms/conflict-serializability-in-dbms/): overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to Database Classification and Optimisation, the last module of this section: with correct data and correct transactions, it compares the kinds of database that exist and studies how indexes and query plans make queries fast.
