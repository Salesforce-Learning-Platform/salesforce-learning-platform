# SQL Fundamentals

## Purpose

Every module so far has stored data in memory — an in-memory array of products, gone the moment
the server restarts. This module introduces **relational databases** and **SQL**, the language
almost every production backend uses to persist data reliably, across server restarts, and to many
concurrent requests at once.

## Learning Objectives

- Explain the relational model: tables, rows, columns, and why data is organized this way.
- Design a basic table schema with appropriate keys.
- Read, create, update, and delete data with `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
- Combine data from multiple tables using `JOIN`.
- Summarize data with aggregate functions, `GROUP BY`, and `HAVING`.
- Use a subquery to filter based on another query's result.
- Explain what a database index does, and its fundamental tradeoff.

## Prerequisites

- [REST API Design](../rest-api-design/) — this module gives the APIs already designed there a
  real place to persist data.

## Files in This Module

| File | Covers |
|---|---|
| [introduction-to-relational-databases.md](introduction-to-relational-databases.md) | Tables, rows, columns, and why relational databases run the industry |
| [sql-basics.md](sql-basics.md) | Designing a schema, and `SELECT`/`WHERE`/`ORDER BY`/`LIMIT` |
| [crud-operations.md](crud-operations.md) | `INSERT`, `UPDATE`, `DELETE`, and connecting SQL to an Express API |
| [joins.md](joins.md) | `INNER JOIN` and `LEFT JOIN` — combining data across tables |
| [aggregations.md](aggregations.md) | `COUNT`/`SUM`/`AVG`, `GROUP BY`, and `HAVING` |
| [subqueries.md](subqueries.md) | Nesting a query inside another with `IN`, `EXISTS`, and scalar subqueries |
| [indexes.md](indexes.md) | Why queries get fast — and why they get slow without one |

## When to Deep-Dive vs. Skim

Deep-dive [joins.md](joins.md) — real-world data is almost never confined to a single table, and
correctly combining related tables (a `products` table and an `orders` table, say) is the single
most-used SQL skill in actual backend work.

## Quick Knowledge Check

<details>
<summary>What's the difference between an INNER JOIN and a LEFT JOIN?</summary>

An `INNER JOIN` only returns rows that have a match in both tables — a row with no match on either
side is excluded entirely. A `LEFT JOIN` returns every row from the left table regardless of
whether it has a match, filling in `NULL` for any right-table columns when there's no match. See
[joins.md](joins.md).

</details>

<details>
<summary>Why does adding an index make reads faster but writes slower?</summary>

An index is a separate, ordered data structure that lets the database locate matching rows quickly
instead of scanning the whole table — but every `INSERT`, `UPDATE`, or `DELETE` now also has to
keep that structure correctly ordered, which is extra work on every write. See
[indexes.md](indexes.md).

</details>

## References

- PostgreSQL, [The SQL Language: Concepts](https://www.postgresql.org/docs/current/tutorial-concepts.html)
- PostgreSQL, [Querying a Table](https://www.postgresql.org/docs/current/tutorial-select.html)
- PostgreSQL, [Joins Between Tables](https://www.postgresql.org/docs/current/tutorial-join.html)
- PostgreSQL, [Aggregate Functions](https://www.postgresql.org/docs/current/tutorial-agg.html)
- PostgreSQL, [Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html)
- PostgreSQL, [Data Manipulation](https://www.postgresql.org/docs/current/dml.html)
- Use The Index, Luke, [Anatomy of an Index](https://use-the-index-luke.com/sql/anatomy)

## Continue Your Learning Path

Continue to the [MongoDB Fundamentals module](../mongodb-fundamentals/) to see how a document
database solves the same data-persistence problem with a genuinely different model.
