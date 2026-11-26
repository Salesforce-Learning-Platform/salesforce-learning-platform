# 🔑 The Relational Model

## 📚 Overview

Most databases that applications rely on are relational, and the ideas behind them are older and simpler than any particular product. This module explains the **relational model** itself: data as sets of tuples, the **keys** that identify them and the references between them, the **relational algebra** that every query is built from, and the places where SQL departs from the model, with the bugs that follow. It teaches concepts; the practical lessons on writing queries are in [SQL Fundamentals](../../../backend/sql-fundamentals/README.md), and this module links to them instead of repeating them.

The module starts with relations, tuples, attributes, and domains, shows where SQL tables are not relations (duplicate rows, no promised order), finds candidate keys by brute force to show why a key is a rule about all valid data and not a property of the current rows, and covers integrity constraints and all five referential actions. It then builds relational algebra in Python (selection, projection, union, difference, product, rename, and the joins and division derived from them) and checks every operator against the matching SQL on hundreds of random databases, and shows why a query optimizer moves selections early. It ends with the traps of SQL: bags instead of sets, `NULL` and three-valued logic (including the `NOT IN` trap), nulls in aggregates and uniqueness, and the logical order in which a query is evaluated. Every example uses **SQLite**, which ships with Python; the code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54, and the operators and traps were checked against independent implementations on thousands of random inputs.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Define a relation, tuple, attribute, domain, heading, and degree, and explain how SQL tables differ from relations.
- Distinguish superkeys, candidate keys, primary and alternate keys, and explain why keys are rules about all valid data.
- State domain, key, entity, and referential integrity, and choose between the referential actions `CASCADE`, `RESTRICT`, `NO ACTION`, `SET NULL`, and `SET DEFAULT`.
- Express queries in relational algebra, build joins, semijoins, antijoins, and division from the basic operators, and translate them into SQL.
- Explain why algebraic rewriting, such as applying selections early, makes queries faster.
- Predict the results of queries that involve `NULL`, avoid the `NOT IN` trap, and describe the logical order in which a query is evaluated.

## 📋 Prerequisites

- [Introduction to DBMS](../introduction-to-dbms/README.md): why databases exist and how an entity-relationship model becomes tables.
- Helpful, not required: [SQL Basics](../../../backend/sql-fundamentals/sql-basics.md) and [Joins](../../../backend/sql-fundamentals/joins.md) for query syntax.
- Basic Python reading ability: functions, tuples, sets, dictionaries, and the standard library.
- A little familiarity with sets (union, intersection, difference); the lessons define what they use.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [relations-and-keys.md](relations-and-keys.md) | Relations and their terms, how SQL tables differ, superkeys and candidate keys, integrity constraints, SQLite's primary-key quirk, and the five referential actions |
| [relational-algebra.md](relational-algebra.md) | The basic and derived operators in Python, division, a comparison of every operator with SQL on random databases, and why queries are rewritten |
| [sql-and-the-relational-model.md](sql-and-the-relational-model.md) | Bags versus sets, `NULL` and three-valued logic, the `NOT IN` trap, nulls in aggregates, groups, and unique constraints, and the logical order of query evaluation |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [sql-and-the-relational-model.md](sql-and-the-relational-model.md) if you write SQL for real systems: the `NULL` rules cause quiet, wrong results, and the `NOT IN` trap in particular is worth learning by running it. For exams and interviews, practise [relations-and-keys.md](relations-and-keys.md) (finding candidate keys) and [relational-algebra.md](relational-algebra.md) (writing "for all" queries with division).

**Skim** the operator implementations in [relational-algebra.md](relational-algebra.md) if you already know the algebra, but read the last section on why selections are moved early, which explains much of what query optimizers do.

## 🧠 Knowledge Check

<details>
<summary>A table records bookings(room, day, guest, phone). The rules are: a room can be booked at most once per day, and a guest may book any number of rooms, also on the same day. Which sets of attributes are candidate keys? Is (room, day, guest) a key, and can (guest, day) be one?</summary>

Under these rules the only candidate key is **(room, day)**: the rule says that no two bookings share both values, and neither attribute alone is unique (the same room is booked on many days, and many rooms are booked on one day). **(room, day, guest)** is a **superkey**, since it contains a key, but it is not a candidate key, because `guest` can be removed. **(guest, day)** cannot be a key, because a guest may book two rooms on the same day, even if the rows currently in the table never show that: keys are rules about every valid state, and sample rows can only refute them, which [relations-and-keys.md](relations-and-keys.md) demonstrates.

</details>

<details>
<summary>A table staff(id, name, manager_id) has one row whose manager_id is NULL. Why does <code>SELECT name FROM staff WHERE id NOT IN (SELECT manager_id FROM staff)</code> return no rows, and how can you write the query correctly?</summary>

`id NOT IN (list)` means "`id` is different from every value in the list". The list contains `NULL`, and comparing anything with `NULL` gives **unknown**. For an id that is in the list the condition is false, and for any other id it is a combination of true comparisons and one unknown, which is **unknown**; `WHERE` keeps only rows whose condition is true, so no row survives. Use `NOT EXISTS`, which asks whether any row has `manager_id = s.id` (a comparison with `NULL` simply does not match), or remove the nulls from the subquery with `WHERE manager_id IS NOT NULL`. [sql-and-the-relational-model.md](sql-and-the-relational-model.md) runs both versions.

</details>

## 📚 References

- [Wikipedia: Relational model](https://en.wikipedia.org/wiki/Relational_model), [Relation (database)](https://en.wikipedia.org/wiki/Relation_(database)), [Superkey](https://en.wikipedia.org/wiki/Superkey), [Candidate key](https://en.wikipedia.org/wiki/Candidate_key), [Foreign key](https://en.wikipedia.org/wiki/Foreign_key), [Referential integrity](https://en.wikipedia.org/wiki/Referential_integrity), and [Entity integrity](https://en.wikipedia.org/wiki/Entity_integrity): relations, keys, and constraints.
- [Wikipedia: Relational algebra](https://en.wikipedia.org/wiki/Relational_algebra), [Join (relational algebra)](https://en.wikipedia.org/wiki/Join_(relational_algebra)), [Join (SQL)](https://en.wikipedia.org/wiki/Join_(SQL)), and [Null (SQL)](https://en.wikipedia.org/wiki/Null_(SQL)): operators, joins, and missing values.
- E. F. Codd, "A Relational Model of Data for Large Shared Data Banks", *Communications of the ACM*, 1970: the paper that proposed the model.
- SQLite documentation: [`CREATE TABLE`](https://www.sqlite.org/lang_createtable.html), [Foreign key support](https://www.sqlite.org/foreignkeys.html), [`SELECT`](https://www.sqlite.org/lang_select.html), [NULL handling](https://www.sqlite.org/nulls.html), and [Aggregate functions](https://www.sqlite.org/lang_aggfunc.html).
- [PostgreSQL documentation: `SELECT`](https://www.postgresql.org/docs/current/sql-select.html) (the order of evaluation and duplicate handling) and [Python docs: `sqlite3`](https://docs.python.org/3/library/sqlite3.html).
- [GeeksforGeeks: Relational Model in DBMS](https://www.geeksforgeeks.org/dbms/relational-model-in-dbms/), [Keys in Relational Model](https://www.geeksforgeeks.org/dbms/types-of-keys-in-relational-model-candidate-super-primary-alternate-and-foreign/), [Relational Algebra](https://www.geeksforgeeks.org/dbms/introduction-of-relational-algebra-in-dbms/), [SQL Joins](https://www.geeksforgeeks.org/sql/sql-join-set-1-inner-left-right-and-full-joins/), and [NULL Values in SQL](https://www.geeksforgeeks.org/sql/sql-null-values/): overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to Normalisation, the next module of this section: with keys and constraints in hand, it studies the dependencies between attributes and splits tables so that each fact is stored once, which prevents the update anomalies seen in the first module.
