# 🧮 SQL and the Relational Model

## An Approximation of the Model

SQL is the language of relational databases, but it is only an engineering approximation of the relational model, and it departs from it in many details ([Wikipedia: Relational model](https://en.wikipedia.org/wiki/Relational_model)). Knowing where it departs prevents some of the most common database bugs. This lesson studies those places; the syntax of queries is taught in [sql-basics.md](../../../backend/sql-fundamentals/sql-basics.md), [joins.md](../../../backend/sql-fundamentals/joins.md), [aggregations.md](../../../backend/sql-fundamentals/aggregations.md), and [subqueries.md](../../../backend/sql-fundamentals/subqueries.md). All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54; the results are deterministic.

## 🪣 Bags, Not Sets

A relation is a set, but SQL results are **bags** (multisets): `SELECT` keeps duplicate rows unless you ask for `DISTINCT`, while `UNION`, `INTERSECT`, and `EXCEPT` remove duplicates unless you add `ALL` ([PostgreSQL documentation: `SELECT`](https://www.postgresql.org/docs/current/sql-select.html)). SQLite offers `UNION ALL` but not `INTERSECT ALL` or `EXCEPT ALL`: its `INTERSECT` and `EXCEPT` always remove duplicates ([SQLite: `SELECT`](https://www.sqlite.org/lang_select.html)):

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.executescript("""
    CREATE TABLE staff (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL, manager_id INTEGER);
    INSERT INTO staff VALUES (1, 'ada', 'London', NULL), (2, 'lin', 'London', 1), (3, 'sam', 'Paris', 1), (4, 'eve', 'Paris', 2);
""")
print("SELECT city          :", [c for (c,) in db.execute("SELECT city FROM staff ORDER BY city")])
print("SELECT DISTINCT city :", [c for (c,) in db.execute("SELECT DISTINCT city FROM staff ORDER BY city")])
print("UNION                :", [c for (c,) in db.execute("SELECT city FROM staff UNION SELECT city FROM staff ORDER BY city")])
print("UNION ALL (8 rows)   :", len(db.execute("SELECT city FROM staff UNION ALL SELECT city FROM staff").fetchall()))
```

```text
SELECT city          : ['London', 'London', 'Paris', 'Paris']
SELECT DISTINCT city : ['London', 'Paris']
UNION                : ['London', 'Paris']
UNION ALL (8 rows)   : 8
```

## ❓ NULL and Three-Valued Logic

`NULL` marks a missing value. It is not a value of any domain, so comparing anything with it gives neither true nor false but a third result, **unknown**; some expressions can still be decided, for example unknown `OR` true is true ([Wikipedia: Null (SQL)](https://en.wikipedia.org/wiki/Null_(SQL))). SQL's logic therefore has three values. The block asks SQLite for the whole truth table of `AND`, `OR`, and `NOT`, and compares it with Kleene's three-valued logic written in Python, in which false < unknown < true, `AND` takes the smaller and `OR` the larger:

```python
import itertools

SQL_LITERAL = {"true": "1", "unknown": "NULL", "false": "0"}
NAME = {1: "true", 0: "false", None: "unknown"}
RANK = {"false": 0, "unknown": 1, "true": 2}
BY_RANK = {rank: name for name, rank in RANK.items()}

def evaluate(expression):
    return NAME[db.execute(f"SELECT {expression}").fetchone()[0]]

print(f"{'a':<8}{'b':<9}{'a AND b':<9}{'a OR b':<8}")
agrees = True
for a, b in itertools.product(SQL_LITERAL, repeat=2):
    both = evaluate(f"{SQL_LITERAL[a]} AND {SQL_LITERAL[b]}")
    either = evaluate(f"{SQL_LITERAL[a]} OR {SQL_LITERAL[b]}")
    agrees &= both == BY_RANK[min(RANK[a], RANK[b])] and either == BY_RANK[max(RANK[a], RANK[b])]
    print(f"{a:<8}{b:<9}{both:<9}{either:<8}")
for a in SQL_LITERAL:
    negated = evaluate(f"NOT {SQL_LITERAL[a]}")
    agrees &= negated == BY_RANK[2 - RANK[a]]
    print(f"NOT {a}: {negated}")
print("SQLite matches Kleene's three-valued logic:", agrees)
```

```text
a       b        a AND b  a OR b  
true    true     true     true    
true    unknown  unknown  true    
true    false    false    true    
unknown true     unknown  true    
unknown unknown  unknown  unknown 
unknown false    false    unknown 
false   true     false    true    
false   unknown  false    unknown 
false   false    false    false   
NOT true: false
NOT unknown: unknown
NOT false: true
SQLite matches Kleene's three-valued logic: True
```

The rule that causes bugs is in the `WHERE` clause: a row is kept **only when the condition is true**; false and unknown rows are both discarded ([Wikipedia: Null (SQL)](https://en.wikipedia.org/wiki/Null_(SQL))). In the `staff` table, `ada` has no manager:

```python
def show(label, query):
    print(f"{label:<44} {db.execute(query).fetchall()}")

show("WHERE manager_id = NULL", "SELECT name FROM staff WHERE manager_id = NULL")
show("WHERE manager_id IS NULL", "SELECT name FROM staff WHERE manager_id IS NULL")
show("WHERE manager_id = 1 OR NOT manager_id = 1", "SELECT count(*) FROM staff WHERE manager_id = 1 OR NOT manager_id = 1")
show("staff who manage nobody, with NOT IN", "SELECT name FROM staff WHERE id NOT IN (SELECT manager_id FROM staff)")
show("staff who manage nobody, with NOT EXISTS",
     "SELECT name FROM staff AS s WHERE NOT EXISTS (SELECT 1 FROM staff AS m WHERE m.manager_id = s.id) ORDER BY name")
```

```text
WHERE manager_id = NULL                      []
WHERE manager_id IS NULL                     [('ada',)]
WHERE manager_id = 1 OR NOT manager_id = 1   [(3,)]
staff who manage nobody, with NOT IN         []
staff who manage nobody, with NOT EXISTS     [('eve',), ('sam',)]
```

`= NULL` is never true, so it matches nothing: test with `IS NULL`. In two-valued logic, "x = 1 or not x = 1" is always true; with `NULL` it is unknown for the row without a manager, so only 3 of the 4 rows pass. And the `NOT IN` query returns **nobody**, because the list of managers contains a `NULL`: for each candidate, "is my id not equal to every manager id?" includes a comparison with `NULL`, whose result is unknown. `NOT EXISTS` asks a yes-or-no question about matching rows and gives the expected answer.

### NULL in Aggregates, Groups, and Uniqueness

Aggregate functions skip nulls, except `count(*)`, which counts rows; ignoring a null is not the same as treating it as zero ([Wikipedia: Null (SQL)](https://en.wikipedia.org/wiki/Null_(SQL))). Grouping, `UNION`, and `DISTINCT` treat two nulls as the same (not distinct), but a `UNIQUE` constraint in SQLite treats them as different ([SQLite: NULL handling](https://www.sqlite.org/nulls.html)). SQLite's `sum()` of no values is `NULL`, while its non-standard `total()` gives 0.0 ([SQLite: Aggregate functions](https://www.sqlite.org/lang_aggfunc.html)):

```python
show("count(*), count(manager_id), avg(manager_id)", "SELECT count(*), count(manager_id), round(avg(manager_id), 3) FROM staff")
show("sum() and total() of no rows", "SELECT sum(manager_id), total(manager_id) FROM staff WHERE id > 99")
show("GROUP BY manager_id", "SELECT manager_id, count(*) FROM staff GROUP BY manager_id ORDER BY manager_id")
show("SELECT NULL UNION SELECT NULL", "SELECT NULL UNION SELECT NULL")
db.execute("CREATE TABLE badges (code TEXT UNIQUE)")
db.execute("INSERT INTO badges VALUES (NULL), (NULL)")
show("two NULLs in a UNIQUE column", "SELECT count(*) FROM badges")
```

```text
count(*), count(manager_id), avg(manager_id) [(4, 3, 1.333)]
sum() and total() of no rows                 [(None, 0.0)]
GROUP BY manager_id                          [(None, 1), (1, 2), (2, 1)]
SELECT NULL UNION SELECT NULL                [(None,)]
two NULLs in a UNIQUE column                 [(2,)]
```

The average of `manager_id` is 1.333, the mean of the three values present, not of four values with a zero. **Design advice:** declare columns `NOT NULL` unless "unknown" or "not applicable" is a real state, and when it is, remember that every comparison with that column has three outcomes.

## 🔢 The Order in Which a Query Is Evaluated

A query is written starting with `SELECT`, but it is processed in a different logical order. In PostgreSQL's description ([PostgreSQL documentation: `SELECT`](https://www.postgresql.org/docs/current/sql-select.html)):

1. `FROM`: the tables are read (and cross-joined if several are listed; join conditions apply here).
2. `WHERE`: rows that do not satisfy the condition are removed.
3. `GROUP BY` and aggregates: the remaining rows are formed into groups.
4. `HAVING`: groups that do not satisfy the condition are removed.
5. The `SELECT` list is computed for each row or group, and `DISTINCT` removes duplicates.
6. Set operators (`UNION`, `INTERSECT`, `EXCEPT`) combine results.
7. `ORDER BY` sorts, then `LIMIT` takes the first rows.

This order explains why a condition on an aggregate belongs in `HAVING`, not `WHERE`: when `WHERE` runs, there are no groups yet.

```python
try:
    db.execute("SELECT city FROM staff WHERE count(*) > 1 GROUP BY city")
except sqlite3.OperationalError as error:
    print("an aggregate in WHERE:", error)
show("the same condition in HAVING", "SELECT city, count(*) FROM staff GROUP BY city HAVING count(*) > 1 ORDER BY city")
show("WHERE first, then groups, then HAVING",
     "SELECT city, count(*) FROM staff WHERE manager_id IS NOT NULL GROUP BY city HAVING count(*) > 1")
db.close()
```

```text
an aggregate in WHERE: misuse of aggregate: count()
the same condition in HAVING                 [('London', 2), ('Paris', 2)]
WHERE first, then groups, then HAVING        [('Paris', 2)]
```

The last query first removes the staff without a manager, then groups the rest, and only then keeps groups with more than one member. (Databases differ in some details, for example in where they allow the names given in the `SELECT` list to be used, so do not rely on such extensions in portable SQL.)

## ✅ Checking the Code

The `NOT IN` and `NOT EXISTS` queries were compared with a direct Python computation of "who manages nobody" on 5,000 random staff tables: `NOT EXISTS` always matched it, while `NOT IN` returned no rows in every table that had a manager id of `NULL`.

## Common Misconceptions

- **"`NULL` equals `NULL`."** Comparing two nulls gives unknown; use `IS NULL` (or, to compare two columns where nulls should match, a null-safe comparison).
- **"`WHERE x <> 1` keeps all rows where x is not 1."** It drops the rows where x is `NULL` as well.
- **"`NOT IN` and `NOT EXISTS` are interchangeable."** They differ as soon as the subquery can return a `NULL`.
- **"`avg` treats missing values as zero."** It ignores them.
- **"SQL runs a query in the order it is written."** Logically, `FROM` and `WHERE` come before grouping and before the `SELECT` list.

## ➡️ Next

This completes The Relational Model module: relations and keys, the algebra that queries are built from, and the places where SQL departs from the model. The next module of this section, [Normalisation](../normalisation/README.md), uses keys to find and remove the redundancy that causes update anomalies.
