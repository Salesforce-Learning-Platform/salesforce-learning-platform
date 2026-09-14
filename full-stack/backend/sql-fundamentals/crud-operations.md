# CRUD Operations

## `INSERT` — Creating a Row

```sql
INSERT INTO products (name, price, category)
VALUES ('Keyboard', 79.99, 'electronics')
RETURNING id;
```

`INSERT INTO table (columns) VALUES (values)` creates a new row. `id` isn't listed — it's
`SERIAL`, so the database generates it automatically. The `RETURNING` clause hands back the
newly-created row's data (here, just the generated `id`) directly from the `INSERT` itself,
avoiding a separate query to fetch what was just created — exactly the data a REST endpoint's
`201 Created` response (per
[status-codes.md](../rest-api-design/status-codes.md)) needs to send back to the client.

## `UPDATE` — Modifying Existing Rows

```sql
UPDATE products
SET price = 69.99
WHERE id = 1;
```

`UPDATE table SET column = value WHERE condition` modifies existing rows matching the condition.
**The `WHERE` clause is not optional in practice** — omitting it updates *every single row* in the
table, a genuinely dangerous, easy mistake with real consequences.

## `DELETE` — Removing Rows

```sql
DELETE FROM products WHERE id = 1;
```

Same structural pattern, same critical caution: `DELETE FROM table WHERE condition` removes only
matching rows — `DELETE FROM products` with no `WHERE` at all deletes **every row in the table**.

## Connecting SQL to an Express API

```js
import pg from "pg";

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });

app.post("/products", async (req, res) => {
  const { name, price, category } = req.body;
  const result = await pool.query(
    "INSERT INTO products (name, price, category) VALUES ($1, $2, $3) RETURNING *",
    [name, price, category]
  );
  res.status(201).json(result.rows[0]);
});
```

A Node.js driver like `pg` (for PostgreSQL) lets an Express route handler
(per [Express.js Fundamentals](../expressjs-fundamentals/)) run real SQL queries — `pool.query`
is asynchronous, fitting naturally into an `async` route handler exactly like any other awaited
operation covered throughout this domain. Notice `$1`, `$2`, `$3` as **placeholders** rather than
directly embedding `req.body` values into the SQL string — covered next.

## Why Placeholders, Not String Concatenation

```js
// DANGEROUS — never do this: directly embeds user input into the query
// string, opening the door to SQL injection (covered in the platform's
// upcoming Web Security content)
const query = `SELECT * FROM products WHERE name = '${req.query.name}'`;

// SAFE — the driver handles escaping the value correctly, no matter
// what it contains
await pool.query("SELECT * FROM products WHERE name = $1", [req.query.name]);
```

Directly concatenating user-supplied input into a SQL string is a serious, well-known
vulnerability — a malicious value could be crafted to change the query's actual meaning entirely.
**Parameterized queries** (the `$1`, `$2`, ... placeholders) let the database driver handle
inserting the value safely, treating it strictly as data, never as part of the SQL syntax itself.
This is a non-negotiable default, not an optional best practice.

## Common Mistakes

- Running an `UPDATE` or `DELETE` without a `WHERE` clause, unintentionally modifying or destroying
  every row in a table.
- Building SQL queries with string concatenation or template literals using untrusted input,
  instead of parameterized placeholders — a direct security vulnerability.
- Forgetting `await` on an async database call, letting a route handler send a response before the
  query has actually completed.

## Next

Continue to [joins.md](joins.md) to query across more than one related table at once.
