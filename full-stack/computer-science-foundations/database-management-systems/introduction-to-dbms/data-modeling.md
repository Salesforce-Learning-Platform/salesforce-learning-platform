# 🧩 Data Modeling

## What Is a Data Model?

Before a database can hold anything, someone must decide **what to store and how it is related**. **Data modeling** is the process of creating a data model for an information system with formal techniques: it defines and analyses the data that an organization needs to support its business, usually together with the people who will use the system ([Wikipedia: Data modeling](https://en.wikipedia.org/wiki/Data_modeling)). The same word is also used for the *kind* of structure a database offers (tables, documents, graphs), which this lesson treats further down. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54.

## 📐 Three Stages of Modeling

Data modeling usually moves through three stages (the same article):

| Stage | Question it answers | Typical contents | Depends on technology? |
|-------|--------------------|------------------|------------------------|
| **Conceptual** | What does the business need to remember? | the things of interest and how they relate | No: it can be discussed with the business |
| **Logical** | How is that organized as data structures? | tables and columns, or other structures a database can implement | Depends on the kind of database, not on a product's storage |
| **Physical** | How is it stored? | indexes, partitions, storage layout | Yes: the chosen database system and its hardware |

The next lesson, on the [entity-relationship model](entity-relationship-model.md), is a standard tool of the conceptual stage.

## 🏢 Three Levels of a Database

A different three-level idea describes a running database, and the two are easy to confuse. A DBMS provides three views of its data ([Wikipedia: Database](https://en.wikipedia.org/wiki/Database)):

- The **external level** is how each group of users sees the data. There can be many such views: a finance department needs payment details, others do not.
- The **conceptual** (logical) level unifies the external views into one overall description, which mainly interests developers and database administrators.
- The **internal** (physical) level is how the DBMS lays the data out, using structures such as indexes for performance.

There is usually only one conceptual and one internal view, but any number of external views (the same article). The **three-schema approach**, which originated in the 1970s, names the three descriptions the external, conceptual, and internal schemas ([Wikipedia: Three-schema approach](https://en.wikipedia.org/wiki/Three-schema_approach)). Its purpose is **data independence**: the immunity of applications to changes in how data is defined and organized ([Wikipedia: Data independence](https://en.wikipedia.org/wiki/Data_independence)). It comes in two kinds:

- **Logical data independence:** the conceptual schema can change without changing the external views that applications use.
- **Physical data independence:** the storage can change without changing the logical schema.

## 🛡️ Logical Data Independence

An application asks for customer totals through a **view**, which is a stored query that behaves like a table. Later the tables behind it are redesigned: the name is split into two columns, and cities move to their own table. The view is redefined to match, and the application's query is not touched:

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.executescript("""
    CREATE TABLE people (id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, city TEXT NOT NULL);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, total INTEGER NOT NULL);
    INSERT INTO people VALUES (1, 'Ada Lovelace', 'London'), (2, 'Alan Turing', 'Manchester');
    INSERT INTO orders VALUES (1, 1, 30), (2, 2, 50), (3, 1, 20);
    CREATE VIEW customer_totals AS
        SELECT p.full_name AS customer, p.city, sum(o.total) AS spent
        FROM people AS p JOIN orders AS o ON o.person_id = p.id
        GROUP BY p.id ORDER BY p.id;
""")
APPLICATION_QUERY = "SELECT customer, city, spent FROM customer_totals"
before = db.execute(APPLICATION_QUERY).fetchall()
print("before:", before)

db.executescript("""                      -- the redesign: split the name, give cities their own table
    DROP VIEW customer_totals;
    CREATE TABLE cities (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
    INSERT INTO cities (name) SELECT DISTINCT city FROM people;
    CREATE TABLE people_new (id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL,
                             city_id INTEGER NOT NULL REFERENCES cities(id));
    INSERT INTO people_new
        SELECT p.id, substr(p.full_name, 1, instr(p.full_name, ' ') - 1), substr(p.full_name, instr(p.full_name, ' ') + 1), c.id
        FROM people AS p JOIN cities AS c ON c.name = p.city;
    DROP TABLE people;
    ALTER TABLE people_new RENAME TO people;
    CREATE VIEW customer_totals AS
        SELECT p.first_name || ' ' || p.last_name AS customer, c.name AS city, sum(o.total) AS spent
        FROM people AS p JOIN cities AS c ON c.id = p.city_id JOIN orders AS o ON o.person_id = p.id
        GROUP BY p.id ORDER BY p.id;
""")
after = db.execute(APPLICATION_QUERY).fetchall()
print("after: ", after)
print("same answer:", before == after)
db.close()
```

```text
before: [('Ada Lovelace', 'London', 50), ('Alan Turing', 'Manchester', 50)]
after:  [('Ada Lovelace', 'London', 50), ('Alan Turing', 'Manchester', 50)]
same answer: True
```

The tables changed completely, and the application did not notice. The independence is only as good as the view: if the redesign had removed information that the view needs, no view could hide it, and independence for *writes* is harder than for reads, because not every view can be updated.

## ⚙️ Physical Data Independence

Adding an **index** changes how the data is stored and found, but not what any query means. The next block runs the same query on 50,000 orders before and after creating indexes, and asks SQLite to explain its plan with `EXPLAIN QUERY PLAN`, which reports how a query will be run, including which indexes it uses ([SQLite: EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)). The wording of plans can change between SQLite versions:

```python
import random

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT NOT NULL, total INTEGER NOT NULL)")
generator = random.Random(1)
db.executemany("INSERT INTO orders (customer, total) VALUES (?, ?)",
               [(f"c{generator.randrange(2000)}", generator.randrange(1000)) for _ in range(50_000)])
QUERY = "SELECT count(*), sum(total) FROM orders WHERE customer = 'c42'"

def plan():
    return "; ".join(row[-1] for row in db.execute("EXPLAIN QUERY PLAN " + QUERY))

results = []
for label, statement in (("no index", None),
                         ("index on customer", "CREATE INDEX orders_by_customer ON orders (customer)"),
                         ("index on (customer, total)", "DROP INDEX orders_by_customer; CREATE INDEX orders_covering ON orders (customer, total)")):
    if statement:
        db.executescript(statement)
    results.append(db.execute(QUERY).fetchone())
    print(f"{label:<27} result {results[-1]}   plan: {plan()}")
print("same result every time:", len(set(results)) == 1)
db.close()
```

```text
no index                    result (21, 12217)   plan: SCAN orders
index on customer           result (21, 12217)   plan: SEARCH orders USING INDEX orders_by_customer (customer=?)
index on (customer, total)  result (21, 12217)   plan: SEARCH orders USING COVERING INDEX orders_covering (customer=?)
same result every time: True
```

The result never changed, only the way SQLite found it: first it **scanned** every row, then it **searched** the index and fetched the matching rows, and with the index that also contains `total`, a **covering index**, it answered from the index alone. Indexing is studied further in [the last module of this section](../classification-and-optimisation/README.md); the practical side is in [indexes.md](../../../backend/sql-fundamentals/indexes.md).

## 🧬 Families of Data Models

The data model that a DBMS offers shapes everything built on it. The main families, in outline ([Wikipedia: Database model](https://en.wikipedia.org/wiki/Database_model)):

| Model | Shape of the data | Notes |
|-------|-------------------|-------|
| **Flat** | one table | columns with similar values, rows of related ones |
| **Hierarchical** | a tree; every record has one parent | early mainframe systems such as IBM's IMS; XML documents have this shape |
| **Network** | records with several parents, so many-to-many fits | the CODASYL specification; popular before the relational model replaced it |
| **Relational** | tables (relations) | introduced by E. F. Codd in 1970, based on predicate logic and set theory; products implement an approximation of it |
| **Dimensional** | a central table of facts described by dimensions | a specialization of the relational model for data warehouses |
| **Object-oriented** | objects | from the 1990s, to avoid converting between objects and rows |
| **Graph** | nodes connected to any other nodes | more general than the network model |

Non-relational databases, often grouped as **NoSQL** and popular since the 2000s, use other query languages ([Wikipedia: Database](https://en.wikipedia.org/wiki/Database)). The relational model is the subject of the [next module of this section](../the-relational-model/README.md).

## 🔄 How a Model Gets Made

A practical order of work is to collect the facts that must be remembered and the questions that must be answered; draw a **conceptual** model with the people who know the business ([entity-relationship-model.md](entity-relationship-model.md)); turn it into a **logical** design for the chosen kind of database, removing redundancy where it matters; and only then make **physical** decisions, such as indexes, for the queries that are actually slow. [database-design-principles.md](../../../backend/database-design-and-modeling/database-design-principles.md) and [schema-design.md](../../../backend/database-design-and-modeling/schema-design.md) give practical advice on the last two steps.

## ✅ Checking the Code

The view gave the same totals as a separate computation in plain Python, before and after the redesign, and adding indexes on `customer`, `(customer, total)`, and `total` did not change the result of any of 120 test queries.

## Common Misconceptions

- **"The conceptual, logical, and physical models are the same as the external, conceptual, and internal levels."** The first three are stages of designing a database; the second three describe views of a running one.
- **"A view is a copy of the data."** An ordinary view stores only the query; it reads the current tables each time.
- **"Adding an index changes my results."** It changes how results are found, and how fast, not what a correct query returns.
- **"Choosing a database product comes first."** The business facts and the questions come first; the model and then the product follow from them.

## ➡️ Next

Continue to [entity-relationship-model.md](entity-relationship-model.md): the standard way to draw what a business needs to remember, and how a diagram becomes tables whose constraints enforce it.
