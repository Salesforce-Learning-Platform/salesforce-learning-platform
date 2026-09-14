# Documents and Collections

## A Document — MongoDB's Equivalent of a SQL Row

```js
{
  _id: ObjectId("5099803df3f4948bd2f98391"),
  name: "Mechanical Keyboard",
  price: 79.99,
  category: "electronics",
  tags: ["wireless", "rgb"],
}
```

A **document** is MongoDB's basic unit of data — a set of field-value pairs, directly comparable to
a single row in [sql-basics.md](../sql-fundamentals/sql-basics.md)'s `products` table. Internally,
MongoDB stores documents as **BSON** (Binary JSON) — a binary format supporting more data types
than plain JSON (like dates and a dedicated numeric-ID type), with a maximum document size of 16
mebibytes.

## `_id` — the Built-In Primary Key

```js
db.products.insertOne({ name: "Mouse", price: 29.99 });
// MongoDB automatically adds: _id: ObjectId("...")
```

Every document requires a unique `_id` field, playing the same structural role as a SQL table's
`PRIMARY KEY` (from [sql-basics.md](../sql-fundamentals/sql-basics.md)). If a document is inserted
without one, MongoDB's driver generates a unique `ObjectId` automatically — the direct MongoDB
equivalent of SQL's `SERIAL` auto-incrementing ID, though structurally a different kind of value
(a generated identifier rather than an incrementing integer).

## A Collection — MongoDB's Equivalent of a SQL Table

```js
db.products.find();  // "products" is a collection, grouping product documents
db.orders.find();    // "orders" is a separate collection
```

A **collection** groups documents together, directly analogous to a SQL table grouping rows. The
crucial difference: a SQL table enforces that every row shares the exact same columns; a MongoDB
collection places **no such requirement** on its documents by default.

## Flexible Schema — a Genuine, Not Superficial, Difference

```js
// Both of these can coexist in the SAME "products" collection —
// no error, no schema migration required
db.products.insertOne({ name: "Keyboard", price: 79.99 });
db.products.insertOne({ name: "Monitor", price: 249.99, warrantyYears: 3 });
```

Because MongoDB doesn't enforce a single fixed schema across a collection's documents, one document
can have a field (`warrantyYears`) that another lacks entirely — no error, and no schema migration
step required, unlike adding a new column to a SQL table. This is powerful for evolving data over
time without disruptive migrations, but it also means enforcing consistency (when it's actually
wanted) becomes the *application's* responsibility, often via a schema-validation layer like
Mongoose (covered in [crud-operations.md](crud-operations.md)) rather than the database itself.

## Common Mistakes

- Assuming MongoDB enforces the same fields across every document in a collection the way SQL
  enforces columns across every row in a table — it explicitly doesn't, by default.
- Manually setting `_id` to a value that's likely to collide with another document's — MongoDB
  enforces `_id` uniqueness, and a collision causes an insert to fail.
- Treating schema flexibility as "no schema needed at all," rather than as a deliberate tradeoff
  that shifts consistency enforcement from the database layer to the application layer.

## Next

Continue to [crud-operations.md](crud-operations.md) to create, read, update, and delete documents,
and connect MongoDB to a real Node.js application.
