# ⚛️ Transactions and ACID

## What a Transaction Is

A **transaction** groups several operations so that the database treats them as one unit of work. The standard example is a transfer between two bank accounts: debiting one and crediting the other is a single transaction. **ACID** (atomicity, consistency, isolation, durability) names the four properties that are meant to keep data valid despite errors, power failures, and other mishaps. Andreas Reuter and Theo Härder coined the acronym in 1983, building on Jim Gray's earlier work on the transaction concept ([Wikipedia: ACID](https://en.wikipedia.org/wiki/ACID)).

This lesson tests each property on SQLite from Python, including the places where the details surprise people. Python's `sqlite3` module is used with `isolation_level=None`, so that nothing starts a transaction behind your back: the code says `BEGIN`, `COMMIT`, and `ROLLBACK` itself. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54; every result is deterministic.

```python
import os
import sqlite3
import tempfile

def open_bank(path, journal_mode="delete"):
    db = sqlite3.connect(path, isolation_level=None, timeout=0)      # timeout=0: a busy database raises at once
    db.execute(f"PRAGMA journal_mode = {journal_mode}")
    db.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER NOT NULL CHECK (balance >= 0))")
    db.execute("INSERT INTO accounts VALUES ('ada', 100), ('lin', 100)")
    return db

def balances(db):
    return dict(db.execute("SELECT name, balance FROM accounts ORDER BY name"))
```

## 🧨 Atomicity: All or Nothing

**Atomicity** means that a transaction either happens completely or leaves the database unchanged ([Wikipedia: ACID](https://en.wikipedia.org/wiki/ACID)). [why-databases-exist.md](../introduction-to-dbms/why-databases-exist.md) showed that SQLite keeps this promise when a program dies in the middle of a transaction. A failing **statement** is different, and this catches many people out:

```python
with tempfile.TemporaryDirectory() as workshop:
    db = open_bank(os.path.join(workshop, "bank.db"))
    db.execute("BEGIN")
    db.execute("UPDATE accounts SET balance = balance + 150 WHERE name = 'lin'")        # the credit
    try:
        db.execute("UPDATE accounts SET balance = balance - 150 WHERE name = 'ada'")    # ada has only 100
    except sqlite3.IntegrityError as error:
        print("the debit was refused:", error)
    print("still inside the transaction:", db.in_transaction)
    db.execute("COMMIT")                                                                # the mistake
    print("after committing anyway:", balances(db), "| total:", sum(balances(db).values()))
    db.close()
```

```text
the debit was refused: CHECK constraint failed: balance >= 0
still inside the transaction: True
after committing anyway: {'ada': 100, 'lin': 250} | total: 350
```

150 units have appeared from nowhere. SQLite's default response to a constraint violation, which is also what the SQL standard specifies, is to abort **only the failing statement** and undo its changes; the earlier changes stay, and the transaction remains open ([SQLite: Conflict resolution](https://www.sqlite.org/lang_conflict.html)). Atomicity covers the whole transaction only if the program **rolls it back** when anything goes wrong. A small context manager makes that automatic, and it also handles a `COMMIT` that fails:

```python
from contextlib import contextmanager

@contextmanager
def transaction(db):
    """Commit if the block succeeds; roll back if anything fails, including the COMMIT itself."""
    db.execute("BEGIN IMMEDIATE")                       # take SQLite's write lock at the start
    try:
        yield db
        db.execute("COMMIT")
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise

with tempfile.TemporaryDirectory() as workshop:
    db = open_bank(os.path.join(workshop, "bank.db"))
    try:
        with transaction(db):
            db.execute("UPDATE accounts SET balance = balance + 150 WHERE name = 'lin'")
            db.execute("UPDATE accounts SET balance = balance - 150 WHERE name = 'ada'")
    except sqlite3.IntegrityError as error:
        print("the transfer failed:", error)
    print("balances:", balances(db), "| total:", sum(balances(db).values()))
    db.close()
```

```text
the transfer failed: CHECK constraint failed: balance >= 0
balances: {'ada': 100, 'lin': 100} | total: 200
```

`BEGIN IMMEDIATE` starts a write transaction at once; a plain `BEGIN` is **deferred**, so the transaction starts only when the database is first touched, and a later write must upgrade it, which can fail ([SQLite: Transactions](https://www.sqlite.org/lang_transaction.html)).

## ✅ Consistency: From One Valid State to Another

**Consistency** means that a transaction takes the database from one valid state to another, preserving its invariants: everything written must satisfy the declared rules, such as constraints, cascades, and triggers ([Wikipedia: ACID](https://en.wikipedia.org/wiki/ACID)). The database can only enforce rules it knows. "The total amount of money stays the same" is not a column constraint; the database would happily commit a transfer that credits more than it debits. Keeping such **application invariants** is the job of correct transaction code, which atomicity and isolation then protect.

## 🔒 Isolation: Concurrent Transactions

**Isolation** ensures that running transactions concurrently leaves the database as if they had run one after another; with weaker isolation levels, some effects of other transactions can become visible ([Wikipedia: ACID](https://en.wikipedia.org/wiki/ACID)). The next block puts a second connection, a reader, next to the transfer. First the transfer is written as two separate statements, each committed on its own, and then as one transaction:

```python
with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "bank.db")
    writer = open_bank(path)
    reader = sqlite3.connect(path, isolation_level=None, timeout=0)

    def total_seen_by_reader():
        return reader.execute("SELECT sum(balance) FROM accounts").fetchone()[0]

    writer.execute("UPDATE accounts SET balance = balance - 30 WHERE name = 'ada'")
    print("two separate statements, between them the reader sees a total of", total_seen_by_reader())
    writer.execute("UPDATE accounts SET balance = balance + 30 WHERE name = 'lin'")

    with transaction(writer):
        writer.execute("UPDATE accounts SET balance = balance - 30 WHERE name = 'ada'")
        own = writer.execute("SELECT sum(balance) FROM accounts").fetchone()[0]
        print(f"inside one transaction, the reader sees {total_seen_by_reader()} while the writer sees {own}")
        writer.execute("UPDATE accounts SET balance = balance + 30 WHERE name = 'lin'")
    print("after the commit:", total_seen_by_reader(), balances(reader))
    writer.close()
    reader.close()
```

```text
two separate statements, between them the reader sees a total of 170
inside one transaction, the reader sees 200 while the writer sees 170
after the commit: 200 {'ada': 40, 'lin': 160}
```

Without a transaction, the reader caught the money in transit. Inside one, it saw the old, consistent state until the commit, and then the new one.

SQLite's documentation says that all its transactions are **serializable**: it makes writers take turns, so that only one writes at a time ([SQLite: Isolation](https://www.sqlite.org/isolation.html)). How readers and a writer coexist depends on the **journal mode**. With the default rollback journal, a reader that is in the middle of a transaction holds a shared lock that a writer must wait out before it can commit. In **WAL** (write-ahead log) mode, a reader keeps seeing a **snapshot** of the database as it was when its transaction started, even after a writer commits (the same page):

```python
for mode in ("delete", "wal"):
    with tempfile.TemporaryDirectory() as workshop:
        path = os.path.join(workshop, "bank.db")
        writer = open_bank(path, mode)
        reader = sqlite3.connect(path, isolation_level=None, timeout=0)
        reader.execute("BEGIN")
        seen = [balances(reader)["ada"]]                 # the reader's transaction starts here
        writer.execute("BEGIN IMMEDIATE")
        writer.execute("UPDATE accounts SET balance = 0 WHERE name = 'ada'")
        try:
            writer.execute("COMMIT")
            story = "committed at once"
        except sqlite3.OperationalError as error:
            story = f"COMMIT refused ({error})"
        seen.append(balances(reader)["ada"])             # still inside the reader's transaction
        reader.execute("COMMIT")
        if writer.in_transaction:                        # a refused COMMIT leaves the transaction open
            writer.execute("COMMIT")
            story += ", then succeeded once the reader had finished"
        seen.append(balances(reader)["ada"])             # a new read
        print(f"{mode:<6} writer {story}")
        print(f"       reader saw ada's balance: {seen[0]}, then {seen[1]}, then {seen[2]}")
        writer.close()
        reader.close()
```

```text
delete writer COMMIT refused (database is locked), then succeeded once the reader had finished
       reader saw ada's balance: 100, then 100, then 0
wal    writer committed at once
       reader saw ada's balance: 100, then 100, then 0
```

(`delete` is SQLite's name for the default rollback-journal mode.) Either way, the reader never saw a value that changed in the middle of its own transaction. The difference is who waits: in rollback-journal mode the writer's commit had to wait for the reader, which is why a program must be ready for a `database is locked` error; in WAL mode the writer did not wait at all.

Isolation also covers decisions. Two doctors are on call, the rule is that at least one must stay, and each of two transactions checks that **two** are on call before taking one off. If both could commit, nobody would be left:

```python
def on_call(db):
    return db.execute("SELECT count(*) FROM doctors WHERE on_call = 1").fetchone()[0]

for mode in ("delete", "wal"):
    with tempfile.TemporaryDirectory() as workshop:
        path = os.path.join(workshop, "hospital.db")
        setup = sqlite3.connect(path, isolation_level=None)
        setup.execute(f"PRAGMA journal_mode = {mode}")
        setup.execute("CREATE TABLE doctors (name TEXT PRIMARY KEY, on_call INTEGER)")
        setup.execute("INSERT INTO doctors VALUES ('ada', 1), ('lin', 1)")
        setup.close()
        first = sqlite3.connect(path, isolation_level=None, timeout=0)
        second = sqlite3.connect(path, isolation_level=None, timeout=0)
        first.execute("BEGIN")
        second.execute("BEGIN")
        print(f"{mode:<6} both check: {on_call(first)} and {on_call(second)} doctors on call")
        for connection, name in ((first, "ada"), (second, "lin")):
            try:
                connection.execute("UPDATE doctors SET on_call = 0 WHERE name = ?", (name,))
                if mode == "wal":
                    connection.execute("COMMIT")
                print(f"       taking {name} off call: accepted")
            except sqlite3.OperationalError as error:
                print(f"       taking {name} off call: refused ({error})")
                connection.execute("ROLLBACK")
        if first.in_transaction:
            first.execute("COMMIT")
        print(f"       doctors still on call: {on_call(first)}")
        first.close()
        second.close()
```

```text
delete both check: 2 and 2 doctors on call
       taking ada off call: accepted
       taking lin off call: refused (database is locked)
       doctors still on call: 1
wal    both check: 2 and 2 doctors on call
       taking ada off call: accepted
       taking lin off call: refused (database is locked)
       doctors still on call: 1
```

In both modes the second transaction could not write. With the rollback journal, the first already held the single write lock; in WAL mode, the second's snapshot was out of date once the first had committed, and a transaction that has only read cannot start writing once another connection has modified the database, or while it is doing so ([SQLite: Transactions](https://www.sqlite.org/lang_transaction.html)). The second transaction has to roll back and try again, and on its second attempt it would see only one doctor on call and stop. [isolation-levels.md](isolation-levels.md) shows that weaker isolation levels allow exactly this mistake.

## 💾 Durability: Committed Means Kept

**Durability** guarantees that a committed transaction stays committed even if the system then fails, for example through a power cut or a crash ([Wikipedia: ACID](https://en.wikipedia.org/wiki/ACID)). The experiment commits one transaction, starts another, and then ends the process abruptly with `os._exit`:

```python
import subprocess
import sys
import textwrap

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "bank.db")
    open_bank(path).close()
    program = textwrap.dedent("""
        import os, sqlite3, sys
        db = sqlite3.connect(sys.argv[1], isolation_level=None)
        db.execute("BEGIN")
        db.execute("UPDATE accounts SET balance = balance + 25 WHERE name = 'ada'")
        db.execute("COMMIT")                                      # committed
        db.execute("BEGIN")
        db.execute("UPDATE accounts SET balance = balance + 999 WHERE name = 'lin'")
        os._exit(1)                                               # dies before committing the second change
    """)
    status = subprocess.run([sys.executable, "-c", program, path]).returncode
    db = sqlite3.connect(path)
    print("exit status", status, "| after reopening:", balances(db))
    print("journal mode:", db.execute("PRAGMA journal_mode").fetchone()[0],
          "| synchronous setting:", db.execute("PRAGMA synchronous").fetchone()[0], "(2 means FULL)")
    db.close()
```

```text
exit status 1 | after reopening: {'ada': 125, 'lin': 100}
journal mode: delete | synchronous setting: 2 (2 means FULL)
```

The committed change survived and the uncommitted one vanished. A crash of the **program** is the easy case: SQLite's documentation says transactions are durable across application crashes whatever the `synchronous` setting or journal mode. A **power cut** or operating system crash is harder, because data may still be in caches that never reached the disk, and the setting then matters ([SQLite: `PRAGMA synchronous`](https://www.sqlite.org/pragma.html#pragma_synchronous)):

- With `synchronous=FULL`, SQLite makes sure content is safely written to disk before continuing, so a power failure will not corrupt the database. With a **rollback journal**, though, the documentation says `FULL` is not necessarily durable across a power loss, and recommends `EXTRA` where durability matters.
- In **WAL mode**, `FULL` gives all four ACID properties. `NORMAL` keeps the database consistent but **loses durability**: a recently committed transaction may be rolled back after a power loss or system crash.

This experiment cannot cut the power, so these two points come from the documentation. Underneath, durability depends on the file system's promise that data forced to disk stays there ([file-system-basics.md](../../operating-systems/file-systems/file-system-basics.md)). Many databases keep a **write-ahead log**: changes are first recorded in a log on stable storage before they are applied to the database, which provides both atomicity and durability ([Wikipedia: Write-ahead logging](https://en.wikipedia.org/wiki/Write-ahead_logging)). SQLite's default rollback journal works the other way round: it saves the old pages first, so that an unfinished change can be undone ([SQLite: Atomic commit](https://www.sqlite.org/atomiccommit.html)).

## ✅ Checking the Code

The experiments of this file printed the same output in each of 25 repeated runs.

## Common Misconceptions

- **"If a statement fails, the transaction is rolled back."** In SQLite (and the SQL standard's default behaviour) only the statement is undone; the program must roll back the transaction.
- **"A transaction makes my business rules hold."** The database enforces only the rules it knows; the transaction must be written correctly, and then atomicity and isolation protect it.
- **"Isolation means other users are locked out."** Readers can often keep working; what isolation limits is what they can see.
- **"`COMMIT` cannot fail."** It can, for example when another connection holds a lock; handle the error and retry or roll back.
- **"Committed data can never be lost."** Durability depends on the settings and on the hardware keeping its promises; read your database's documentation.

## ➡️ Next

Continue to [isolation-levels.md](isolation-levels.md): the anomalies that concurrent transactions can cause, the isolation levels that prevent them, and a simulator that tries every possible interleaving.
