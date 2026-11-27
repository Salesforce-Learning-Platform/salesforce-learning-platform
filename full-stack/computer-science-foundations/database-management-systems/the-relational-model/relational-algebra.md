# ➗ Relational Algebra

## Operators on Relations

**Relational algebra**, introduced by Codd as part of the relational model in 1970, defines operators that take relations and produce relations, so that the operators can be combined freely. It is the theoretical foundation of relational query languages, above all SQL ([Wikipedia: Relational algebra](https://en.wikipedia.org/wiki/Relational_algebra)). Learning it explains what SQL queries *mean* and how a database can rearrange them to run faster. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54; the results are deterministic.

## 🧱 The Basic Operators

| Operator | Symbol | Meaning |
|----------|--------|---------|
| **Selection** | σ | the tuples that satisfy a condition |
| **Projection** | π | only the named attributes (duplicates vanish, because the result is a set) |
| **Rename** | ρ | the same tuples with attribute names changed |
| **Union** | ∪ | tuples in either relation |
| **Difference** | − | tuples in the first but not the second |
| **Cartesian product** | × | every tuple of one combined with every tuple of the other |

Union and difference need the two relations to have the same attributes, and the product needs them to have no attribute names in common ([Wikipedia: Relational algebra](https://en.wikipedia.org/wiki/Relational_algebra)). In Python, a relation can be a tuple of attribute names and a set of rows:

```python
from collections import namedtuple

Relation = namedtuple("Relation", "attributes rows")

def relation(attributes, rows):
    return Relation(tuple(attributes), frozenset(tuple(row) for row in rows))

def select(r, condition):
    return Relation(r.attributes, frozenset(row for row in r.rows if condition(dict(zip(r.attributes, row)))))

def project(r, attributes):
    positions = [r.attributes.index(a) for a in attributes]
    return Relation(tuple(attributes), frozenset(tuple(row[p] for p in positions) for row in r.rows))

def rename(r, names):
    return Relation(tuple(names.get(a, a) for a in r.attributes), r.rows)

def union(r, s):
    assert set(r.attributes) == set(s.attributes), "union needs the same attributes"
    return Relation(r.attributes, r.rows | project(s, r.attributes).rows)

def difference(r, s):
    assert set(r.attributes) == set(s.attributes), "difference needs the same attributes"
    return Relation(r.attributes, r.rows - project(s, r.attributes).rows)

def product(r, s):
    assert not set(r.attributes) & set(s.attributes), "rename shared attributes first"
    return Relation(r.attributes + s.attributes, frozenset(a + b for a in r.rows for b in s.rows))
```

## 🔗 Operators Built From the Basic Ones

Several useful operators add no new power: each can be written with the six above. **Intersection** is R − (R − S). A **theta join** is a selection applied to a product. The **natural join** keeps the combinations of tuples that agree on all attributes with the same name, showing each such attribute once; the **semijoin** keeps the tuples of the first relation that have at least one partner in the second, and the **antijoin** the tuples that have none ([Wikipedia: Join (relational algebra)](https://en.wikipedia.org/wiki/Join_(relational_algebra))). **Division**, R ÷ S, answers "for all" questions: it gives the values of the attributes of R that are not in S which appear with **every** tuple of S; SQL has no operator for it (the same article):

```python
def intersection(r, s):
    return difference(r, difference(r, s))

def theta_join(r, s, condition):
    return select(product(r, s), condition)

def natural_join(r, s):
    shared = [a for a in r.attributes if a in s.attributes]
    renamed = rename(s, {a: "_" + a for a in shared})
    matched = select(product(r, renamed), lambda t: all(t[a] == t["_" + a] for a in shared))
    return project(matched, r.attributes + tuple(a for a in s.attributes if a not in shared))

def semijoin(r, s):
    return project(natural_join(r, s), r.attributes)

def antijoin(r, s):
    return difference(r, semijoin(r, s))

def divide(r, s):
    keep = tuple(a for a in r.attributes if a not in s.attributes)
    candidates = project(r, keep)
    missing = difference(product(candidates, s), project(r, keep + s.attributes))   # pairs that should be there but are not
    return difference(candidates, project(missing, keep))

completed = relation(("student", "task"), [("ada", "design"), ("ada", "queries"), ("ada", "report"),
                                           ("lin", "design"), ("lin", "queries"), ("sam", "queries")])
database_tasks = relation(("task",), [("design",), ("queries",)])
print("did every database task:", sorted(divide(completed, database_tasks).rows))
print("did at least one:       ", sorted(project(semijoin(completed, database_tasks), ("student",)).rows))
```

```text
did every database task: [('ada',), ('lin',)]
did at least one:        [('ada',), ('lin',), ('sam',)]
```

Ada and Lin completed both tasks; Sam completed only one. A semijoin asks "is there at least one partner?"; division asks "is there a partner for *every* tuple?".

## 🧩 From Algebra to SQL

Every operator has a SQL form. The block below builds many random databases and compares each operator implemented in Python with the SQL query that expresses it, using `DISTINCT` where SQL would otherwise keep duplicates:

```python
import random
import sqlite3

SQL_FORMS = {
    "selection": "SELECT DISTINCT * FROM r WHERE a < b",
    "projection": "SELECT DISTINCT b FROM r",
    "union": "SELECT b FROM r UNION SELECT b FROM t",
    "difference": "SELECT b FROM r EXCEPT SELECT b FROM t",
    "intersection": "SELECT b FROM r INTERSECT SELECT b FROM t",
    "product": "SELECT DISTINCT r.a, r.b, u.x FROM r CROSS JOIN u",
    "natural join": "SELECT DISTINCT * FROM r NATURAL JOIN s",
    "semijoin": "SELECT DISTINCT * FROM r WHERE EXISTS (SELECT 1 FROM s WHERE s.b = r.b)",
    "antijoin": "SELECT DISTINCT * FROM r WHERE NOT EXISTS (SELECT 1 FROM s WHERE s.b = r.b)",
    "division": """SELECT DISTINCT a FROM r AS outer_r WHERE NOT EXISTS (
                       SELECT 1 FROM t WHERE NOT EXISTS (SELECT 1 FROM r WHERE r.a = outer_r.a AND r.b = t.b))""",
}
ALGEBRA_FORMS = {
    "selection": lambda r, s, t, u: select(r, lambda row: row["a"] < row["b"]),
    "projection": lambda r, s, t, u: project(r, ("b",)),
    "union": lambda r, s, t, u: union(project(r, ("b",)), t),
    "difference": lambda r, s, t, u: difference(project(r, ("b",)), t),
    "intersection": lambda r, s, t, u: intersection(project(r, ("b",)), t),
    "product": lambda r, s, t, u: product(r, u),
    "natural join": lambda r, s, t, u: natural_join(r, s),
    "semijoin": lambda r, s, t, u: semijoin(r, s),
    "antijoin": lambda r, s, t, u: antijoin(r, s),
    "division": lambda r, s, t, u: divide(r, t),
}

def random_relation(attributes, generator, size):
    return relation(attributes, [[generator.randrange(4) for _ in attributes] for _ in range(generator.randrange(size))])

def load(connection, name, rel):
    connection.execute(f"CREATE TABLE {name} ({', '.join(rel.attributes)})")
    connection.executemany(f"INSERT INTO {name} VALUES ({', '.join('?' * len(rel.attributes))})", list(rel.rows))

generator = random.Random(7)
agreements = {name: 0 for name in SQL_FORMS}
for _ in range(500):
    tables = {"r": random_relation(("a", "b"), generator, 9), "s": random_relation(("b", "c"), generator, 9),
              "t": random_relation(("b",), generator, 5), "u": random_relation(("x",), generator, 4)}
    connection = sqlite3.connect(":memory:")
    for name, rel in tables.items():
        load(connection, name, rel)
    for operator, query in SQL_FORMS.items():
        from_sql = frozenset(tuple(row) for row in connection.execute(query))
        from_algebra = ALGEBRA_FORMS[operator](tables["r"], tables["s"], tables["t"], tables["u"]).rows
        agreements[operator] += from_sql == from_algebra
    connection.close()
for operator, count in agreements.items():
    print(f"{operator:<13} Python and SQL agree on {count} of 500 random databases")
```

```text
selection     Python and SQL agree on 500 of 500 random databases
projection    Python and SQL agree on 500 of 500 random databases
union         Python and SQL agree on 500 of 500 random databases
difference    Python and SQL agree on 500 of 500 random databases
intersection  Python and SQL agree on 500 of 500 random databases
product       Python and SQL agree on 500 of 500 random databases
natural join  Python and SQL agree on 500 of 500 random databases
semijoin      Python and SQL agree on 500 of 500 random databases
antijoin      Python and SQL agree on 500 of 500 random databases
division      Python and SQL agree on 500 of 500 random databases
```

All ten operators agreed on all 500 databases, including those where a table is empty, where division by an empty relation keeps every candidate.

## ⚡ Why a Database Rearranges Queries

Because the operators obey algebraic laws, an expression can be rewritten into another that gives the same result with much less work. Moving selections as early as possible is the most important such rule, because selection reduces the size of intermediate results ([Wikipedia: Relational algebra](https://en.wikipedia.org/wiki/Relational_algebra)). For example, a condition that uses only one side of a product can be applied to that side first:

```python
generator = random.Random(3)
customers = relation(("customer", "city"), [(f"c{i}", generator.choice(["London", "Paris", "Rome", "Oslo", "Lima",
                                                                     "Cairo", "Delhi", "Quito", "Hanoi", "Accra"]))
                                          for i in range(300)])
orders = relation(("order_id", "buyer"), [(i, f"c{generator.randrange(300)}") for i in range(1000)])

def in_london(row):
    return row["city"] == "London"

def matches(row):
    return row["buyer"] == row["customer"]

late = select(product(customers, orders), lambda row: in_london(row) and matches(row))
early_input = select(customers, in_london)
early = select(product(early_input, orders), matches)
print("filter after combining: ", f"{len(customers.rows) * len(orders.rows):>9,}", "combined tuples examined")
print("filter before combining:", f"{len(early_input.rows) * len(orders.rows):>9,}", "combined tuples examined")
print("same result:", late.rows == early.rows, f"({len(early.rows)} tuples)")
```

```text
filter after combining:    300,000 combined tuples examined
filter before combining:    33,000 combined tuples examined
same result: True (110 tuples)
```

The answer is the same, and the second form built about a tenth as many combinations, because only about one customer in ten lives in London. A database's **query optimizer** applies rules like this, and chooses join algorithms (nested loop, sort-merge, and hash joins are the three fundamental ones, [Wikipedia: Join (SQL)](https://en.wikipedia.org/wiki/Join_(SQL))) and indexes, which is why a declarative query can run quickly without saying how. [query-optimisation.md](../classification-and-optimisation/query-optimisation.md) studies these join algorithms and the optimizer's choices.

## ✅ Checking the Code

Besides the comparison with SQL above, the derived operators were checked against direct set definitions (for example, the antijoin against "the tuples of R with no matching tuple in S") on 3,000 random relations, and the two forms of the query in the last block were compared on 500 random customer and order tables, always giving the same result.

## Common Misconceptions

- **"Relational algebra is only theory."** It is what query optimizers manipulate when they rewrite a query into a faster one.
- **"A natural join is the same as an inner join."** A natural join matches *all* attributes that share a name, which can silently match more columns than intended; an inner join states its condition.
- **"Division is unimportant because SQL lacks it."** "Customers who bought every product" is a division, written in SQL with nested `NOT EXISTS` or with grouping.
- **"Projection never changes the number of rows."** In the algebra, projection removes duplicates, so it can shrink the result.

## ➡️ Next

Continue to [sql-and-the-relational-model.md](sql-and-the-relational-model.md): the places where SQL departs from the model, most importantly `NULL` and its three-valued logic.
