# 🔑 Relations and Keys

## A Model Built on Sets

The **relational model**, first described by Edgar F. Codd in 1969, represents all data as **tuples** grouped into **relations**. Its aim is a *declarative* way to describe data and ask for it: users say what the database holds and what they want from it, and the database management system decides how to store it and how to answer ([Wikipedia: Relational model](https://en.wikipedia.org/wiki/Relational_model)). Most relational databases use SQL, which the same article describes as an engineering *approximation* of the model. This lesson is about the model itself; the practical SQL lessons start at [SQL Fundamentals](../../../backend/sql-fundamentals/README.md). All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54; the results are deterministic.

## 📦 Relations, Tuples, and Attributes

An **attribute** is a name paired with a **domain** (a type). A **heading** is a set of attributes with different names, a **tuple** gives each attribute a value from its domain, and a **relation** is a heading together with a **body**, a set of tuples with that heading. The number of attributes is the relation's **degree** ([Wikipedia: Relation (database)](https://en.wikipedia.org/wiki/Relation_(database))). Because the body is a *set*, and the heading too, three things follow: there are **no duplicate tuples**, the tuples have **no order**, and the attributes have no order either.

| Relational model | SQL |
|------------------|-----|
| relation | table |
| tuple | row |
| attribute | column |
| domain | data type (plus constraints) |

SQL tables are not quite relations. A table can hold **duplicate rows** unless a constraint forbids it, and a query without `ORDER BY` may return rows in whatever order the system finds fastest ([PostgreSQL documentation: `SELECT`](https://www.postgresql.org/docs/current/sql-select.html)). Both are easy to see:

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE pets (name TEXT, species TEXT)")
db.executemany("INSERT INTO pets VALUES (?, ?)", [("rex", "dog"), ("tom", "cat"), ("bob", "fish"), ("amy", "dog")])
QUERY = "SELECT name FROM pets"                       # no ORDER BY
print("before adding an index:", [name for (name,) in db.execute(QUERY)])
db.execute("CREATE INDEX pets_by_name ON pets (name)")
print("after adding an index: ", [name for (name,) in db.execute(QUERY)],
      "| plan:", "; ".join(row[-1] for row in db.execute("EXPLAIN QUERY PLAN " + QUERY)))
db.execute("INSERT INTO pets VALUES ('rex', 'dog')")
print("identical rows ('rex', 'dog') stored:", db.execute("SELECT count(*) FROM pets WHERE name = 'rex'").fetchone()[0])
db.close()
```

```text
before adding an index: ['rex', 'tom', 'bob', 'amy']
after adding an index:  ['amy', 'bob', 'rex', 'tom'] | plan: SCAN pets USING COVERING INDEX pets_by_name
identical rows ('rex', 'dog') stored: 2
```

Adding an index changed nothing about the data, yet the order of the answer changed, because SQLite chose to read the index. If the order matters, say so with `ORDER BY`. And the second copy of `('rex', 'dog')` was accepted, which no relation would allow.

## 🗝️ Keys

A **superkey** is any set of attributes whose values identify each tuple of a relation uniquely; the set of *all* attributes is always one, because a relation has no duplicate tuples ([Wikipedia: Superkey](https://en.wikipedia.org/wiki/Superkey)). A **candidate key** is a *minimal* superkey: removing any attribute would allow duplicates. A relation can have several candidate keys of different sizes; one is chosen as the **primary key**, and the others are **alternate keys**. Attributes that belong to some candidate key are called **prime** ([Wikipedia: Candidate key](https://en.wikipedia.org/wiki/Candidate_key)). [schema-design.md](../../../backend/database-design-and-modeling/schema-design.md) discusses the practical choice of a primary key.

The next function finds the candidate keys that are consistent with a given set of rows, by trying every set of attributes from the smallest up:

```python
from itertools import combinations

def keys_of_these_rows(attributes, rows):
    """The minimal attribute sets whose values are all different in THESE rows."""
    found = []
    for size in range(1, len(attributes) + 1):
        for chosen in combinations(attributes, size):
            if any(set(smaller) <= set(chosen) for smaller in found):
                continue                                              # contains a key already: not minimal
            positions = [attributes.index(a) for a in chosen]
            if len({tuple(row[p] for p in positions) for row in rows}) == len(rows):
                found.append(chosen)
    return found

BOOKING = ("room", "day", "guest", "phone")
rows = [(101, "Mon", "Ada", "555-1"), (102, "Mon", "Lin", "555-2"), (101, "Tue", "Lin", "555-2")]
print("keys consistent with three bookings:", keys_of_these_rows(BOOKING, rows))
rows += [(103, "Tue", "Lin", "555-2"),                      # Lin books a second room on Tuesday ...
         (101, "Wed", "Ada", "555-1")]                      # ... and Ada books room 101 again
print("after two more bookings:            ", keys_of_these_rows(BOOKING, rows))
```

```text
keys consistent with three bookings: [('room', 'day'), ('room', 'guest'), ('room', 'phone'), ('day', 'guest'), ('day', 'phone')]
after two more bookings:             [('room', 'day')]
```

With only three rows, five different pairs of columns happen to be unique, including `guest` with `day`. After two more bookings, only `(room, day)` is left. **A key is a statement about every valid state of the data, not about the rows you happen to have.** Rows can only *refute* a key; which keys hold is decided by the rules of the business (here: a room can be booked once per day, so `(room, day)` is a key by rule).

## 🛡️ Integrity Constraints

- **Domain constraints:** each value belongs to its attribute's domain (types, `CHECK`).
- **Key constraints:** no two tuples agree on a candidate key (`PRIMARY KEY`, `UNIQUE`).
- **Entity integrity:** every row of a table has a unique, non-null primary key value, so that each row stands for one entity ([Wikipedia: Entity integrity](https://en.wikipedia.org/wiki/Entity_integrity)).
- **Referential integrity:** every reference is valid. A **foreign key** is a set of attributes that refers to a candidate key of another (or the same) relation, and each of its values must exist there, or be null ([Wikipedia: Foreign key](https://en.wikipedia.org/wiki/Foreign_key), [Referential integrity](https://en.wikipedia.org/wiki/Referential_integrity)).

SQLite has one surprise to know about entity integrity: although the SQL standard says that a primary key can never be null, SQLite allows `NULL` in a primary key column unless the column is an `INTEGER PRIMARY KEY`, the table is `WITHOUT ROWID` or `STRICT`, or the column is declared `NOT NULL`; the documentation calls this a bug in early versions that is kept for compatibility ([SQLite: `CREATE TABLE`](https://www.sqlite.org/lang_createtable.html)):

```python
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE loose (code TEXT PRIMARY KEY, note TEXT)")
db.execute("INSERT INTO loose VALUES (NULL, 'first'), (NULL, 'second')")
print("rows with a NULL primary key:", db.execute("SELECT count(*) FROM loose WHERE code IS NULL").fetchone()[0])
db.execute("CREATE TABLE careful (code TEXT NOT NULL PRIMARY KEY, note TEXT)")
try:
    db.execute("INSERT INTO careful VALUES (NULL, 'first')")
except sqlite3.IntegrityError as error:
    print("with NOT NULL:", error)
db.close()
```

```text
rows with a NULL primary key: 2
with NOT NULL: NOT NULL constraint failed: careful.code
```

### What Happens When a Referenced Row Is Deleted?

A foreign key says what must happen to the rows that refer to a deleted (or updated) row. SQL defines five **referential actions**: `CASCADE`, `RESTRICT`, `NO ACTION`, `SET NULL`, and `SET DEFAULT` ([Wikipedia: Foreign key](https://en.wikipedia.org/wiki/Foreign_key)); SQLite implements all five, and `NO ACTION` is the default ([SQLite: Foreign key support](https://www.sqlite.org/foreignkeys.html)). The block deletes a team that two players refer to, under each action:

```python
for action in ("NO ACTION", "RESTRICT", "CASCADE", "SET NULL", "SET DEFAULT"):
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("CREATE TABLE teams (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute(f"CREATE TABLE players (name TEXT, team_id INTEGER DEFAULT 0 REFERENCES teams(id) ON DELETE {action})")
    db.execute("INSERT INTO teams VALUES (0, 'free agents'), (1, 'red')")
    db.execute("INSERT INTO players VALUES ('ada', 1), ('lin', 1)")
    try:
        db.execute("DELETE FROM teams WHERE id = 1")
        outcome = "team deleted"
    except sqlite3.IntegrityError:
        outcome = "delete refused"
    print(f"{action:<12} {outcome:<15} players now: {db.execute('SELECT name, team_id FROM players ORDER BY name').fetchall()}")
    db.close()
```

```text
NO ACTION    delete refused  players now: [('ada', 1), ('lin', 1)]
RESTRICT     delete refused  players now: [('ada', 1), ('lin', 1)]
CASCADE      team deleted    players now: []
SET NULL     team deleted    players now: [('ada', None), ('lin', None)]
SET DEFAULT  team deleted    players now: [('ada', 0), ('lin', 0)]
```

`NO ACTION` and `RESTRICT` both refused the delete here. They differ in *when* the check happens: `RESTRICT` objects immediately, while `NO ACTION` is checked at the end of the statement, or of the transaction when the constraint is deferred ([SQLite: Foreign key support](https://www.sqlite.org/foreignkeys.html)). `CASCADE` deletes the referring rows too, so use it only when they have no meaning of their own; `SET NULL` and `SET DEFAULT` keep the rows and change the reference.

## ✅ Checking the Code

`keys_of_these_rows` agreed with a direct reading of the definition (a set of attributes is a candidate key if its values are all different and no proper subset has that property) on 2,000 random tables of up to five columns.

## Common Misconceptions

- **"A table is a relation."** A SQL table can contain duplicate rows, and SQL results can carry duplicates; a relation cannot.
- **"Rows come back in the order they were inserted."** Without `ORDER BY` there is no promised order, as the index experiment showed.
- **"A column that is unique today is a key."** Keys are rules about all valid data; current rows can only disprove them.
- **"A primary key is automatically `NOT NULL`."** In standard SQL it is; in SQLite you should declare `NOT NULL` yourself unless the key is an integer primary key.

## ➡️ Next

Continue to [relational-algebra.md](relational-algebra.md): the operators that take relations and give relations, which are the foundation of every query.
