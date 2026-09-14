# Subqueries

## A Query Inside a Query

```sql
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

A **subquery** is a `SELECT` statement nested inside another SQL statement — here, the inner query
`(SELECT AVG(price) FROM products)` computes the average price first, and the outer query uses that
single computed value to filter. This is a **scalar subquery**: it returns exactly one row, one
column — a single usable value, directly comparable to any other value in a `WHERE` clause.

## `IN` — Matching Against a Set of Values

```sql
SELECT name FROM products
WHERE category IN (
  SELECT category FROM products WHERE price > 500
);
```

`IN (subquery)` checks whether a value matches **any** row the subquery returns — here, finding
every product whose category *also* contains at least one product priced above $500. The subquery
here returns potentially many rows, but only one column — `IN` compares the outer value against
that whole list.

## `EXISTS` — Checking Whether Any Matching Row Exists at All

```sql
SELECT name FROM products p
WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.product_id = p.id
);
```

`EXISTS (subquery)` returns `true` as soon as the subquery finds *any* matching row at all — it
doesn't care what columns the subquery actually selects (writing `SELECT 1` is a common, idiomatic
convention specifically because the selected value itself is irrelevant to `EXISTS`). This query
finds every product that has been ordered at least once — genuinely the same underlying question a
`JOIN` combined with `DISTINCT` could also answer, but often more directly readable as "does a
matching order exist?"

## Subqueries vs. Joins — Overlapping, Not Identical

```sql
-- Subquery version
SELECT name FROM products p
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.product_id = p.id);

-- JOIN + DISTINCT version, same underlying result
SELECT DISTINCT p.name FROM products p
JOIN orders o ON o.product_id = p.id;
```

Both queries above answer the same real question, but with genuinely different structure: the
subquery version reads as "products where a matching order exists," while the join version reads as
"combine products with their orders, then deduplicate." Neither is universally "correct" — which
reads more clearly, and which performs better for a given database and dataset size, can both
matter in choosing between them, and the next file's coverage of indexes is a big part of why that
performance difference can exist at all.

## Common Mistakes

- Using a scalar subquery expecting a single value when the subquery can actually return multiple
  rows — most databases raise a runtime error in that case, since a single comparison genuinely
  can't be made against more than one value.
- Writing `IN (subquery)` where the subquery's selected column doesn't match the outer comparison
  value's type or meaning, producing a query that runs without error but returns nonsensical
  results.
- Assuming a subquery is always slower (or always faster) than an equivalent `JOIN` — the right
  choice genuinely depends on the specific query, table sizes, and database, not a fixed rule.

## Next

Continue to [indexes.md](indexes.md) to see why some of these queries stay fast as a table grows
large, and why others don't.
