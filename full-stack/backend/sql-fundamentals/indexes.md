# Indexes

## Why a Query Can Get Slow as a Table Grows

```sql
SELECT * FROM products WHERE name = 'Keyboard';
```

Without any help, the database has to check `name` against **every single row** in `products` to
find matches — a **full table scan**. With 100 rows, that's instant. With 10 million rows, that
same query becomes noticeably, then unacceptably, slow — the query itself hasn't changed at all;
only the amount of data it has to scan through has.

## What an Index Actually Is

```sql
CREATE INDEX idx_products_name ON products (name);
```

An **index** is a separate, ordered data structure the database maintains alongside a table,
specifically to make lookups on a given column (or columns) fast — directly comparable to a printed
book's index: instead of reading every page to find a topic, you look it up in an ordered list that
points straight to the right page. Once `idx_products_name` exists, `WHERE name = 'Keyboard'` no
longer needs to scan the whole table — it can jump almost directly to matching rows.

## The Real Tradeoff: Faster Reads, Slower Writes, More Storage

| | Without an index | With an index |
|---|---|---|
| `SELECT ... WHERE name = ...` | Scans every row | Looks up directly — much faster |
| `INSERT`/`UPDATE`/`DELETE` | No extra work | Must also update the index's own structure |
| Storage | Just the table | The table, plus the index's own space |

An index is not a free performance upgrade — every `INSERT`, `UPDATE`, or `DELETE` on an indexed
table now has to also keep the index itself correctly updated, and the index consumes its own real
disk space. This is exactly why databases don't index every column by default: an index is a
deliberate tradeoff, worth making specifically for columns that are actually queried frequently
(especially in a `WHERE` clause or a `JOIN`'s `ON` condition), not applied indiscriminately.

## What to Index

```sql
-- A primary key is automatically indexed — no need to add one manually
CREATE TABLE products (id SERIAL PRIMARY KEY, ...);

-- Columns frequently used in WHERE, JOIN ... ON, or ORDER BY are
-- strong candidates for an explicit index
CREATE INDEX idx_orders_product_id ON orders (product_id);
```

A **primary key** (like `products.id`) is automatically indexed by the database — no manual step
needed. Beyond that, columns genuinely worth indexing are the ones actually used to filter
(`WHERE category = ...`), join (`orders.product_id`, from [joins.md](joins.md)'s example), or sort
(`ORDER BY price`) — indexing a column that's never queried on its own provides no read benefit
while still paying the full write-and-storage cost.

## Common Mistakes

- Indexing every column "just in case," incurring the write and storage cost broadly without a
  corresponding read benefit for columns that are rarely, if ever, actually queried.
- Not indexing a column that's genuinely queried constantly (like a foreign key column used in
  frequent `JOIN`s), leaving a real, avoidable performance problem as the table grows.
- Assuming an index automatically speeds up *every* query on that table — an index specifically
  helps queries that filter, join, or sort on the indexed column; it does nothing for a query that
  never references it.

## Module Summary

Across this module: **relational databases** organize durable data into tables, rows, and columns,
with related tables connected through reference columns rather than duplicated data (see
[introduction-to-relational-databases.md](introduction-to-relational-databases.md)); `SELECT`,
`WHERE`, `ORDER BY`, and `LIMIT` read and filter data, after a table's schema is designed with
appropriate types and constraints (see [sql-basics.md](sql-basics.md)); `INSERT`, `UPDATE`, and
`DELETE` create, modify, and remove rows — always with a deliberate `WHERE` clause, and always via
parameterized queries when driven by user input (see [crud-operations.md](crud-operations.md));
`JOIN`s combine related tables, with `INNER JOIN` vs. `LEFT JOIN` being a genuine design decision
about which rows to include (see [joins.md](joins.md)); aggregate functions with `GROUP BY` and
`HAVING` summarize large datasets directly in the database (see
[aggregations.md](aggregations.md)); **subqueries** nest one query inside another for expressive
filtering, overlapping meaningfully with what a `JOIN` can also express (see
[subqueries.md](subqueries.md)); and an **index** trades write performance and storage for much
faster reads on the specific columns it covers.
