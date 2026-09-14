# SQL Basics

## Designing a Schema

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC(10, 2) NOT NULL,
  category TEXT
);
```

A table's **schema** declares its columns and each one's data type up front. `SERIAL PRIMARY KEY`
creates an auto-incrementing, unique identifier for every row — the **primary key**, the standard
way a specific row is uniquely referenced (exactly the `id` used throughout
[resource-based-routing.md](../rest-api-design/resource-based-routing.md)'s `/products/:id`
pattern). `NOT NULL` declares that a column can never be left empty — a database-enforced version
of the same idea behind
[request-validation.md](../rest-api-design/request-validation.md)'s required-field validation, but
guaranteed at the storage layer itself, not just at the API boundary.

## `SELECT` — Reading Data

```sql
SELECT * FROM products;
```

```sql
SELECT name, price FROM products;
```

`SELECT` reads rows from a table. `*` selects every column; naming specific columns
(`name, price`) returns only those, which is both clearer and more efficient than fetching data a
query doesn't actually need.

## `WHERE` — Filtering Rows

```sql
SELECT * FROM products WHERE category = 'electronics';

SELECT * FROM products WHERE price > 50 AND category = 'electronics';
```

`WHERE` filters which rows are returned, based on a condition — directly analogous to
[pagination-filtering-and-sorting.md](../rest-api-design/pagination-filtering-and-sorting.md)'s
API-level filtering, just expressed in SQL instead of JavaScript array `.filter()`. Conditions can
be combined with `AND`/`OR`, exactly like JavaScript's own logical operators.

## `ORDER BY` — Sorting Results

```sql
SELECT * FROM products ORDER BY price;        -- ascending, the default
SELECT * FROM products ORDER BY price DESC;   -- descending
```

`ORDER BY` sorts the result set by one or more columns — the SQL equivalent of the `sort` query
parameter convention from
[pagination-filtering-and-sorting.md](../rest-api-design/pagination-filtering-and-sorting.md).

## `LIMIT` — Restricting How Many Rows Come Back

```sql
SELECT * FROM products ORDER BY price DESC LIMIT 10;
```

`LIMIT` caps the number of rows returned — the direct SQL-level tool behind implementing
pagination: fetching page 1 of 20 items means `LIMIT 20`, and a real pagination implementation adds
`OFFSET` to skip past earlier pages.

## Putting It Together

```sql
SELECT name, price
FROM products
WHERE category = 'electronics' AND price < 100
ORDER BY price DESC
LIMIT 5;
```

A single query can combine every clause covered so far: select specific columns, filter to matching
rows, sort them, and cap the result count — SQL's clauses compose together in a fixed order
(`SELECT` → `FROM` → `WHERE` → `ORDER BY` → `LIMIT`), each one refining the result further.

## Common Mistakes

- Using `SELECT *` in production code when only specific columns are actually needed — fetching
  unnecessary data wastes bandwidth and can hide accidental dependencies on columns that might
  later be removed.
- Forgetting `WHERE` entirely and accidentally querying (or, worse, later updating/deleting) every
  row in a table instead of the intended subset.
- Writing clauses out of SQL's required order (e.g., `ORDER BY` before `WHERE`) — SQL syntax
  enforces a specific clause order that doesn't match every language's usual flexibility.

## Next

Continue to [crud-operations.md](crud-operations.md) to actually create, update, and delete data,
not just read it.
