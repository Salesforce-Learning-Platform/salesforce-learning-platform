# Introduction to Relational Databases

## The Problem: Data That Needs to Outlive the Process

```js
// Every module so far: data disappears the instant the server restarts
const products = [{ id: 1, name: "Keyboard" }];
```

Every example across [Creating Your First Server](../creating-your-first-server/),
[Express.js Fundamentals](../expressjs-fundamentals/), and
[REST API Design](../rest-api-design/) stored data as a plain in-memory JavaScript array — it
works for learning, but it's gone the instant the Node process restarts, and a second server
instance (needed for real scale) wouldn't share it at all. A real backend needs data that
**persists**: stored somewhere durable, outside the running process itself.

## Tables, Rows, and Columns

```
products
┌────┬──────────────┬───────┐
│ id │ name         │ price │
├────┼──────────────┼───────┤
│ 1  │ Keyboard     │ 79.99 │
│ 2  │ Mouse        │ 29.99 │
└────┴──────────────┴───────┘
```

A **relational database** organizes data into **tables** — each one a named collection of
**rows** (individual records), where every row has the same set of **columns** (named fields, each
with a specific data type). This `products` table is the durable, database-backed equivalent of
the in-memory `products` array used throughout earlier modules.

## What "Relational" Actually Means

```
products                          orders
┌────┬──────────┐                 ┌────┬────────────┐
│ id │ name     │                 │ id │ product_id │
├────┼──────────┤                 ├────┼────────────┤
│ 1  │ Keyboard │  <──referenced──│ 1  │     1      │
└────┴──────────┘   by product_id └────┴────────────┘
```

"Relational" refers to how tables **relate** to each other — an `orders` table doesn't repeat a
product's full name and price in every row; it stores a reference (`product_id`) pointing back to
the `products` table. [joins.md](joins.md) covers combining related tables back together in a
single query.

## Why Relational Databases Run the Industry

Relational databases (PostgreSQL, MySQL, and others) enforce a rigid, well-defined structure — every
row in a table genuinely has the same columns, of the same types — and provide strong guarantees
(covered more fully in the upcoming
[Database Design and Modeling module](../database-design-and-modeling/)) about data staying
consistent even under many simultaneous writes. This structure and reliability is exactly why the
relational model has remained the default choice for a huge share of real-world production backends
for decades.

## PostgreSQL as This Module's Reference Database

This module's examples use **PostgreSQL** syntax — one of the most widely used open-source
relational databases in the industry, and syntactically very close to the broader SQL standard, so
the concepts transfer directly to MySQL or any other relational database with only minor syntax
differences.

## Common Mistakes

- Assuming an in-memory array (as used in earlier modules) is a real substitute for a database in
  anything beyond a learning example — it has no durability and can't be shared across multiple
  server instances.
- Treating "relational" as just a fancy word for "table-based" — the actual relationships between
  tables (like `product_id` referencing `products`) are the concept's real substance.
- Assuming SQL syntax is wildly different across databases — the core language (covered in the
  rest of this module) is standardized enough that PostgreSQL knowledge transfers to MySQL and
  others with only minor adjustments.

## Next

Continue to [sql-basics.md](sql-basics.md) to design a real table and query it with `SELECT`.
