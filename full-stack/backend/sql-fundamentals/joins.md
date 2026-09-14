# Joins

## Why a Single Table Isn't Enough

Recall [introduction-to-relational-databases.md](introduction-to-relational-databases.md)'s
`orders` table, which stores a `product_id` rather than repeating each product's full details. A
query against `orders` alone can only ever show that raw ID — actually displaying "Order #7:
Keyboard, $79.99" requires combining data from **both** tables. A `JOIN` is exactly this: a single
query that pulls matching rows from more than one table at once.

## `INNER JOIN` — Only Matching Rows

```sql
SELECT orders.id, orders.quantity, products.name, products.price
FROM orders
INNER JOIN products ON orders.product_id = products.id;
```

```
 id | quantity |   name   | price
----+----------+----------+-------
  1 |    2     | Keyboard | 79.99
  2 |    1     | Mouse    | 29.99
```

An `INNER JOIN` returns only rows that have a match on **both** sides of the `ON` condition — an
order referencing a `product_id` that no longer exists in `products` (say, a deleted product) would
simply be **excluded** from the result entirely.

## `LEFT JOIN` — Every Row From the Left Table, Matched or Not

```sql
SELECT products.name, orders.id AS order_id
FROM products
LEFT JOIN orders ON products.id = orders.product_id;
```

```
   name   | order_id
----------+----------
 Keyboard |    1
 Mouse    |    2
 Monitor  |   NULL     ← never ordered, but still shown
```

A `LEFT JOIN` returns **every** row from the "left" table (`products`, listed first), whether or
not it has a match in the "right" table (`orders`) — any columns from the unmatched side simply
come back as `NULL`. This is the right choice specifically when the goal is "show me every product,
including ones that have never been ordered" — something an `INNER JOIN` would silently exclude.

## Choosing Between Them

| | `INNER JOIN` | `LEFT JOIN` |
|---|---|---|
| Returns | Only rows with a match on both sides | Every row from the left table, matched or not |
| Use when | You only care about rows that genuinely relate to both tables | You need every row from one table, even without a related row |
| Example | "Show every order, with its product's name" | "Show every product, including ones never ordered" |

The choice is a real design decision, not a stylistic preference — picking the wrong one either
silently drops rows a query was supposed to include, or unexpectedly includes rows with `NULL`
gaps where a match was actually expected.

## Qualifying Column Names

```sql
-- AMBIGUOUS if both tables have an "id" column — which one?
SELECT id, name FROM products JOIN orders ON products.id = orders.product_id;

-- CLEAR — explicitly qualified
SELECT products.id, products.name FROM products JOIN orders ON products.id = orders.product_id;
```

Once a query involves more than one table, any column name that exists in both (like `id`) becomes
ambiguous unless explicitly qualified with its table name — a good habit to apply consistently in
any join, even when a particular column name happens not to collide yet.

## Common Mistakes

- Defaulting to `INNER JOIN` when a `LEFT JOIN` was actually needed, silently dropping rows (like
  products that have never been ordered) that should have appeared in the result.
- Forgetting to qualify a column name that exists in multiple joined tables, causing an ambiguity
  error — or worse, an unintended column being selected.
- Joining on the wrong columns entirely (e.g., matching `products.id` to `orders.id` instead of
  `orders.product_id`), producing a query that runs without error but returns meaningless results.

## Next

Continue to [aggregations.md](aggregations.md) to summarize data across many rows — totals,
counts, and averages — instead of just listing them individually.
