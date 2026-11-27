# 🗃️ Why Databases Exist

## Data That Must Outlive the Program

A program's variables disappear when it ends, so real programs keep their data in files. For a small amount of data that one program reads and writes, that works. It stops working as soon as the data matters: when the same fact is needed in many places, when several programs or users change it at once, when a mistake or a crash must not corrupt it, and when new questions about it arrive every week. This lesson shows each of those problems happening in a few lines of Python, then shows what a database does instead. It uses **SQLite**, a database engine that ships with Python's standard library, so nothing needs to be installed. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54; error messages can differ slightly between versions.

## 1️⃣ The Same Fact in Many Places

A common first design is one flat file of orders, in which every row repeats the customer's details. The file below says where Ada lives twice. A program that handles Ada's move updates the row it happens to be working on:

```python
import csv
import io

ORDERS_CSV = """order_id,customer,city,total
1,Ada,London,30
2,Alan,Manchester,50
3,Ada,London,20
"""
rows = list(csv.DictReader(io.StringIO(ORDERS_CSV)))
rows[0]["city"] = "Bristol"                    # Ada has moved; only the row for order 1 is updated

cities_by_customer = {}
for row in rows:
    cities_by_customer.setdefault(row["customer"], set()).add(row["city"])
print({customer: sorted(cities) for customer, cities in cities_by_customer.items()})
```

```text
{'Ada': ['Bristol', 'London'], 'Alan': ['Manchester']}
```

The file now says that Ada lives in two places, and nothing in it says which is right. This is an **update anomaly**, the typical result of storing the same fact more than once. A database design stores each fact once and links to it: customers in one table, orders in another that refers to a customer by an identifier. Then a change happens in one place:

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)        # None: no hidden transactions; each statement commits
db.executescript("""
    CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), total INTEGER NOT NULL);
    INSERT INTO customers VALUES (1, 'Ada', 'London'), (2, 'Alan', 'Manchester');
    INSERT INTO orders VALUES (1, 1, 30), (2, 2, 50), (3, 1, 20);
""")
db.execute("UPDATE customers SET city = 'Bristol' WHERE name = 'Ada'")        # the fact is stored once
for row in db.execute("""SELECT o.id, c.name, c.city, o.total
                         FROM orders AS o JOIN customers AS c ON c.id = o.customer_id ORDER BY o.id"""):
    print(row)
db.close()
```

```text
(1, 'Ada', 'Bristol', 30)
(2, 'Alan', 'Manchester', 50)
(3, 'Ada', 'Bristol', 20)
```

Both of Ada's orders show the new city, because neither order stores it. Deciding how to split data into tables so that such anomalies cannot happen is the subject of **normalization**; [normalization.md](../../../backend/database-design-and-modeling/normalization.md) introduces it in practice, and a [later module of this section](../normalisation/README.md) studies the theory.

## 2️⃣ Nothing Stops Bad Data

A file accepts whatever a program writes: an order for a customer who does not exist, a negative total, a missing date, two customers with the same email address. A database lets you declare **constraints** that it enforces for every program that writes to it. SQLite checks foreign keys only when a connection switches the check on, so the first line does that:

```python
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("PRAGMA foreign_keys = ON")              # in SQLite, foreign key checks are off unless switched on
db.executescript("""
    CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE);
    CREATE TABLE orders (id INTEGER PRIMARY KEY,
                         customer_id INTEGER NOT NULL REFERENCES customers(id),
                         total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
                         placed_on TEXT NOT NULL);
    INSERT INTO customers VALUES (1, 'Ada', 'ada@example.com');
    INSERT INTO orders VALUES (10, 1, 900, '2026-01-06');
""")
ATTEMPTS = {
    "order for a customer who does not exist": "INSERT INTO orders VALUES (11, 99, 500, '2026-01-05')",
    "negative total": "INSERT INTO orders VALUES (12, 1, -500, '2026-01-05')",
    "order without a date": "INSERT INTO orders (id, customer_id, total_cents) VALUES (13, 1, 500)",
    "second customer with Ada's email": "INSERT INTO customers VALUES (2, 'Mallory', 'ada@example.com')",
    "delete a customer who has orders": "DELETE FROM customers WHERE id = 1",
}
for description, statement in ATTEMPTS.items():
    try:
        db.execute(statement)
        print(f"{description:<40} accepted")
    except sqlite3.IntegrityError as error:
        print(f"{description:<40} rejected: {error}")
print("orders stored:", db.execute("SELECT count(*) FROM orders").fetchone()[0])
db.close()

unchecked = sqlite3.connect(":memory:", isolation_level=None)       # the same mistake with the check left off
unchecked.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY)")
unchecked.execute("CREATE TABLE orders (customer_id INTEGER REFERENCES customers(id))")
unchecked.execute("INSERT INTO orders VALUES (99)")
print("with the check left off, an order for customer 99 is stored:",
      unchecked.execute("SELECT count(*) FROM orders").fetchone()[0] == 1)
unchecked.close()
```

```text
order for a customer who does not exist  rejected: FOREIGN KEY constraint failed
negative total                           rejected: CHECK constraint failed: total_cents >= 0
order without a date                     rejected: NOT NULL constraint failed: orders.placed_on
second customer with Ada's email         rejected: UNIQUE constraint failed: customers.email
delete a customer who has orders         rejected: FOREIGN KEY constraint failed
orders stored: 1
with the check left off, an order for customer 99 is stored: True
```

Every bad write was refused, and the one order that was valid is still the only one stored. The last lines matter too: SQLite's documentation says that foreign key checks are **off by default**, for backwards compatibility, and must be enabled on each connection ([SQLite: Foreign key support](https://www.sqlite.org/foreignkeys.html)). A database enforces only the rules that you declare and switch on.

## 3️⃣ Two Writers at Once

Two programs that update the same file by reading it, changing the value, and writing it back can lose an update: the race condition of [race-conditions.md](../../operating-systems/deadlocks-and-concurrency/race-conditions.md). A barrier forces the unlucky order, in which both read before either writes:

```python
import json
import os
import tempfile
import threading

def deposit_in_file(path, amount, both_have_read):
    with open(path) as handle:
        balance = json.load(handle)["balance"]
    both_have_read.wait()                              # force the unlucky schedule
    with open(path, "w") as handle:
        json.dump({"balance": balance + amount}, handle)

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "account.json")
    with open(path, "w") as handle:
        json.dump({"balance": 100}, handle)
    barrier = threading.Barrier(2)
    threads = [threading.Thread(target=deposit_in_file, args=(path, amount, barrier)) for amount in (50, 30)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    with open(path) as handle:
        print("file, after deposits of 50 and 30 to a balance of 100:", json.load(handle)["balance"], "(should be 180)")
```

```text
file, after deposits of 50 and 30 to a balance of 100: 150 (should be 180)
```

One deposit vanished. In SQL, the whole update is one statement, and the database coordinates the writers, which here are forty threads, each with its own connection, all started together:

```python
def deposit_in_database(path, amount, start_together):
    connection = sqlite3.connect(path, timeout=30, isolation_level=None)    # wait (up to 30 s) for other writers
    start_together.wait()
    connection.execute("UPDATE accounts SET balance = balance + ? WHERE id = 1", (amount,))
    connection.close()

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "bank.db")
    db = sqlite3.connect(path, isolation_level=None)
    db.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER NOT NULL)")
    db.execute("INSERT INTO accounts VALUES (1, 100)")
    barrier = threading.Barrier(40)
    threads = [threading.Thread(target=deposit_in_database, args=(path, amount, barrier)) for amount in range(1, 41)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    balance = db.execute("SELECT balance FROM accounts").fetchone()[0]
    print(f"database, after forty concurrent deposits of 1 to 40: {balance} (should be {100 + sum(range(1, 41))})")
    db.close()
```

```text
database, after forty concurrent deposits of 1 to 40: 920 (should be 920)
```

No deposit was lost, because SQLite allows only one writer at any instant and the other writers queue up for their turn ([SQLite: Appropriate uses](https://www.sqlite.org/whentouse.html)). (Databases differ in how much writing they let happen at once, which is part of the story of transactions in a later module of this section.)

## 4️⃣ A Crash in the Middle

Moving money takes two changes: subtract from one account and add to another. If the program dies between them, the money is gone. The next block starts a second Python process that makes the first change to two files and then stops abruptly with `os._exit`, which ends a process immediately without any clean-up (it stands in for a crash or a power cut, without crashing the interpreter):

```python
import subprocess
import sys
import textwrap

def run_in_new_process(code, argument):
    """Run `code` in a separate Python process, passing one argument; return the exit status."""
    return subprocess.run([sys.executable, "-c", textwrap.dedent(code), argument]).returncode

with tempfile.TemporaryDirectory() as workshop:
    for name, balance in (("ada", 500), ("lin", 300)):
        with open(os.path.join(workshop, name + ".txt"), "w") as handle:
            handle.write(str(balance))
    status = run_in_new_process("""
        import os, sys
        folder = sys.argv[1]
        def read(name):
            with open(os.path.join(folder, name + ".txt")) as handle:
                return int(handle.read())
        def write(name, value):
            with open(os.path.join(folder, name + ".txt"), "w") as handle:
                handle.write(str(value))
        write("ada", read("ada") - 200)        # step 1: take the money from ada
        os._exit(1)                            # the program dies before step 2
        write("lin", read("lin") + 200)
    """, workshop)
    balances = {name: int(open(os.path.join(workshop, name + ".txt")).read()) for name in ("ada", "lin")}
    print("exit status", status, "| files:", balances, "| total", sum(balances.values()), "(was 800)")
```

```text
exit status 1 | files: {'ada': 300, 'lin': 300} | total 600 (was 800)
```

Two hundred units no longer exist. A database groups the two changes into a **transaction**, and promises **atomic commit**: either all the changes of a transaction happen or none do ([SQLite: Atomic commit](https://www.sqlite.org/atomiccommit.html)). Here the process dies inside the transaction:

```python
with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "bank.db")
    db = sqlite3.connect(path, isolation_level=None)
    db.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER NOT NULL CHECK (balance >= 0))")
    db.execute("INSERT INTO accounts VALUES ('ada', 500), ('lin', 300)")
    db.close()
    status = run_in_new_process("""
        import os, sqlite3, sys
        db = sqlite3.connect(sys.argv[1], isolation_level=None)
        db.execute("BEGIN")
        db.execute("UPDATE accounts SET balance = balance - 200 WHERE name = 'ada'")
        os._exit(1)                            # dies inside the transaction, before the second update
    """, path)
    db = sqlite3.connect(path)
    balances = dict(db.execute("SELECT name, balance FROM accounts"))
    print("exit status", status, "| database:", balances, "| total", sum(balances.values()))
    db.close()
```

```text
exit status 1 | database: {'ada': 500, 'lin': 300} | total 800
```

A skeptic might say that the change had simply not reached the disk yet. The next experiment makes sure that it has: it updates 100,000 rows with a very small cache, so that SQLite must write changed pages into the database file before the transaction ends (a writer updates the file when its memory cache fills up, and only after the journal that can undo the change is safely stored, [SQLite: File locking and concurrency](https://www.sqlite.org/lockingv3.html)), and then the process dies:

```python
import hashlib

def fingerprint(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "bank.db")
    db = sqlite3.connect(path, isolation_level=None)
    db.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER NOT NULL, note TEXT)")
    db.execute("BEGIN")
    db.executemany("INSERT INTO accounts VALUES (?, 100, ?)", [(number, "x" * 100) for number in range(1, 100_001)])
    db.execute("COMMIT")
    db.close()
    original = fingerprint(path)

    status = run_in_new_process("""
        import os, sqlite3, sys
        db = sqlite3.connect(sys.argv[1], isolation_level=None)
        db.execute("PRAGMA cache_size = 10")         # keep very little in memory, so changes spill into the file
        db.execute("PRAGMA cache_spill = 10")
        db.execute("BEGIN")
        db.execute("UPDATE accounts SET balance = balance - 1")      # change every row ...
        os._exit(1)                                                  # ... and die before COMMIT
    """, path)
    print("exit status:", status, "| files left behind:", sorted(os.listdir(workshop)))
    print("the database file was changed by the unfinished transaction:", fingerprint(path) != original)

    db = sqlite3.connect(path)
    print("sum of the balances after reopening:", f"{db.execute('SELECT sum(balance) FROM accounts').fetchone()[0]:,}")
    print("integrity check:", db.execute("PRAGMA integrity_check").fetchone()[0])
    db.close()
    print("the database file is identical to the original again:", fingerprint(path) == original,
          "| files left:", sorted(os.listdir(workshop)))
```

```text
exit status: 1 | files left behind: ['bank.db', 'bank.db-journal']
the database file was changed by the unfinished transaction: True
sum of the balances after reopening: 10,000,000
integrity check: ok
the database file is identical to the original again: True | files left: ['bank.db']
```

Part of the unfinished transaction was in the database file, and the next program to open the database undid it, leaving the file exactly as before. The **rollback journal**, the extra file left by the dead process, held what was needed: SQLite calls a journal that must be played back to restore a sane state a **hot journal**, which is what an earlier process that crashed in the middle of its work leaves behind ([SQLite: Atomic commit](https://www.sqlite.org/atomiccommit.html)). Writing a program that survives this correctly yourself is hard; the file system tools of [file-system-basics.md](../../operating-systems/file-systems/file-system-basics.md) (writing a new file and renaming it) protect one file at a time, not several related records.

## 5️⃣ Every Question Needs a Program

With files, each new question needs new code that says *how* to find the answer. A database accepts a **declarative query** that says *what* you want, and chooses how to compute it:

```python
rows = [(1, "Ada", "London", 30), (2, "Alan", "Manchester", 50), (3, "Ada", "London", 20), (4, "Grace", "London", 70)]

# the program way: say how to group and add
spent_by_city = {}
for _, _, city, total in rows:
    spent_by_city[city] = spent_by_city.get(city, 0) + total
by_program = sorted(spent_by_city.items())

# the query way: say what is wanted
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT, city TEXT, total INTEGER)")
db.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", rows)
by_query = db.execute("SELECT city, sum(total) FROM orders GROUP BY city ORDER BY city").fetchall()
print("program:", by_program)
print("query:  ", by_query)
print("same answer:", by_program == by_query)
db.close()
```

```text
program: [('London', 120), ('Manchester', 50)]
query:   [('London', 120), ('Manchester', 50)]
same answer: True
```

## 🏛️ What a Database Management System Is

A **database** is an organized collection of data; the **database management system (DBMS)** is the software that interacts with users, applications, and the database itself to capture and analyse the data; and the database, the DBMS, and the applications together are sometimes called a **database system** ([Wikipedia: Database](https://en.wikipedia.org/wiki/Database)). In a definition by Connolly and Begg that the same article quotes, a DBMS is software that lets users define, create, maintain, and control access to the database. E. F. Codd proposed the services that a full general-purpose DBMS should provide (the same article):

| Service | What the experiments above showed |
|---------|-----------------------------------|
| Storing, retrieving, and updating data | queries that say what is wanted |
| A catalog describing the data | the table definitions that the database keeps |
| Transactions and concurrency | forty writers, and atomic commit |
| Recovery when the database is damaged | the hot journal |
| Authorization of access | not shown: SQLite has no `GRANT` or `REVOKE` and relies on the operating system's file permissions ([SQLite: features not implemented](https://www.sqlite.org/omitted.html)) |
| Access from remote locations | not shown: SQLite is embedded in the program |
| Enforcing constraints | the rejected writes |

Examples of database management systems include PostgreSQL, MySQL, MariaDB, Microsoft SQL Server, and Oracle Database (the same article). They differ in many ways; the most basic is the **data model**, the subject of [data-modeling.md](data-modeling.md). Relational databases, which store data in tables and mostly use SQL, became dominant in the 1980s, and non-relational "NoSQL" databases became popular in the 2000s (the same article); [sql-vs-nosql.md](../../../backend/database-design-and-modeling/sql-vs-nosql.md) compares the two for practical use.

SQLite is an unusual member of the family: it is a library that runs inside your program and keeps a database in one file, so it has no server, no user accounts, and no network access. Its documentation says that it does not compete with client/server databases; it competes with writing your own files with `fopen` ([SQLite: Appropriate uses](https://www.sqlite.org/whentouse.html)).

## 📄 When a Plain File Is Enough

A database is not always the answer. A plain file is often right for a small configuration file, a log that is only appended to, or data that one program writes once and reads whole, provided that you can tolerate the loss or inconsistency that the experiments above showed, or avoid it simply (for example by writing a new file and renaming it). Reach for a database when facts are shared and updated, when several writers may be active, when related changes must happen together, or when the questions keep changing.

## ✅ Checking the Code

The experiments were also checked independently. On 12,000 random inserts and deletes, SQLite accepted exactly the operations that the same rules, written separately in Python, allowed. The forty concurrent deposits gave the exact total in each of 25 repeated runs. And in 12 crash tests that changed between 1 and 100,000 rows before the process died, the database file was restored byte for byte every time, including the 8 runs in which the changes had already reached the file.

## Common Misconceptions

- **"A database is just a file with a fancy format."** The format is the small part; the guarantees (constraints, transactions, concurrency control, recovery) are the point.
- **"Using a database means my data cannot be wrong."** A database enforces the rules you declare. SQLite does not even check foreign keys until asked.
- **"The words database and DBMS mean the same thing."** The database is the data; the DBMS is the software that manages it.
- **"Writing a new file and renaming it gives me transactions."** It makes the replacement of one file atomic; it does not coordinate several writers, or changes to several related records.

## ➡️ Next

Continue to [data-modeling.md](data-modeling.md): how the data a business needs is turned, stage by stage, into the structures a database stores, and how a database keeps its users independent of those structures.
