# Aggregations

## Aggregate Functions — Computing One Value From Many Rows

```sql
SELECT COUNT(*) FROM products;               -- how many products exist
SELECT AVG(price) FROM products;              -- average price across all products
SELECT MAX(price) FROM products;              -- the single highest price
SELECT MIN(price) FROM products;              -- the single lowest price
SELECT SUM(quantity) FROM orders;             -- total items ordered, across every order
```

An **aggregate function** collapses many rows down into a single computed value — `COUNT`, `SUM`,
`AVG`, `MAX`, and `MIN` are the five most common. Without any grouping, an aggregate applies across
the *entire* table's matching rows (after any `WHERE` filter) at once.

## `GROUP BY` — One Aggregate Result Per Group

```sql
SELECT category, COUNT(*), AVG(price)
FROM products
GROUP BY category;
```

```
   category   | count |  avg
--------------+-------+-------
 electronics  |   12  | 145.50
 clothing     |   34  |  29.99
 books        |    8  |  14.25
```

`GROUP BY` changes an aggregate from "one result for the whole table" into "one result *per distinct
value* of the grouped column" — here, one row per `category`, each with its own count and average.
This is directly analogous to grouping data in JavaScript (reducing an array into buckets by a key)
— SQL does the same grouping and computation in one declarative statement.

## `HAVING` — Filtering *After* Grouping

```sql
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 10;
```

`WHERE` (from [sql-basics.md](sql-basics.md)) filters individual rows **before** any grouping
happens, and cannot reference an aggregate result — `HAVING` is the equivalent filter applied
**after** grouping, specifically so it *can* filter on an aggregate value (like "only categories
with more than 10 products"). This `WHERE`-before / `HAVING`-after distinction is one of the more
commonly confused points in SQL, precisely because both look like a similar filtering clause.

## A Realistic Combined Example

```sql
SELECT category, COUNT(*) AS product_count, ROUND(AVG(price), 2) AS avg_price
FROM products
WHERE price > 0
GROUP BY category
HAVING COUNT(*) >= 5
ORDER BY avg_price DESC;
```

This single query filters out any invalid zero-or-negative-priced rows first (`WHERE`), groups
the remainder by category, keeps only categories with at least 5 products (`HAVING`), and sorts the
result by average price — the kind of real analytics query (per
[pagination-filtering-and-sorting.md](../rest-api-design/pagination-filtering-and-sorting.md)'s
broader theme of summarizing large collections) that would be genuinely painful to replicate with
manual JavaScript array operations on a large dataset.

## Common Mistakes

- Using `WHERE` when the intent is actually to filter on an aggregate result (like "only groups
  with more than 10 items") — `WHERE` runs before grouping and can't reference an aggregate at all;
  `HAVING` is required for that.
- Selecting a non-aggregated column alongside `GROUP BY` without including it in the `GROUP BY`
  clause itself — most databases reject this as ambiguous, since it's unclear which row's value for
  that column should represent the whole group.
- Forgetting that `COUNT(*)` counts *rows*, while `COUNT(column_name)` counts only rows where that
  specific column isn't `NULL` — a subtle but real difference.

## Next

Continue to [subqueries.md](subqueries.md) to nest one query inside another for even more
expressive filtering.
