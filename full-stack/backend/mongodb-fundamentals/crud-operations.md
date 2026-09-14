# CRUD Operations

## The Four Basic Operations

```js
db.products.insertOne({ name: "Keyboard", price: 79.99 });   // Create
db.products.find({ category: "electronics" });                // Read
db.products.updateOne({ _id: id }, { $set: { price: 69.99 } }); // Update
db.products.deleteOne({ _id: id });                             // Delete
```

MongoDB's CRUD operations map directly onto the same four operations
[SQL's `INSERT`/`SELECT`/`UPDATE`/`DELETE`](../sql-fundamentals/crud-operations.md) already
cover — the concepts are identical; only the syntax (a JavaScript-like method call and object,
rather than a SQL statement) differs.

## Update Operators — `$set` Is Not Optional

```js
// WRONG — this REPLACES the entire document with just { price: 69.99 },
// silently deleting every other field the document had
db.products.updateOne({ _id: id }, { price: 69.99 });

// CORRECT — $set updates only the specified field, leaving everything else untouched
db.products.updateOne({ _id: id }, { $set: { price: 69.99 } });
```

This is one of MongoDB's most common early mistakes: an update document without `$set` is treated
as a **full replacement** of the document — directly analogous to
[http-methods.md](../rest-api-design/http-methods.md)'s distinction between `PUT` (full replace)
and `PATCH` (partial update). `$set` is what makes `updateOne` behave like a partial update instead
of silently wiping every other field.

## Connecting MongoDB to Express With Mongoose

```js
import mongoose from "mongoose";

await mongoose.connect(process.env.MONGODB_URI);

const productSchema = new mongoose.Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  category: String,
});

const Product = mongoose.model("Product", productSchema);
```

```js
app.post("/products", async (req, res) => {
  const product = await Product.create(req.body);
  res.status(201).json(product);
});

app.get("/products/:id", async (req, res) => {
  const product = await Product.findById(req.params.id);
  if (!product) return res.status(404).json({ error: "Not found" });
  res.json(product);
});
```

**Mongoose** is an Object Data Modeling (ODM) library — it lets a Node.js application define a
`Schema` (declaring expected fields and types, re-introducing schema *enforcement at the
application layer*, per [documents-and-collections.md](documents-and-collections.md)'s note on
flexible schema), compiles it into a `Model`, and provides convenient methods
(`Product.create`, `Product.findById`) on top of MongoDB's raw driver — fitting naturally into an
Express route handler exactly like the `pg` driver did for SQL in
[SQL's crud-operations.md](../sql-fundamentals/crud-operations.md).

## `insertMany`, `updateMany`, `deleteMany`

```js
db.products.insertMany([{ name: "A" }, { name: "B" }]);
db.products.updateMany({ category: "electronics" }, { $set: { onSale: true } });
db.products.deleteMany({ discontinued: true });
```

Every basic operation has a "many" variant, affecting every document matching the given filter,
rather than only the first match — directly comparable to a SQL `UPDATE`/`DELETE` with a `WHERE`
clause matching multiple rows at once.

## Common Mistakes

- Forgetting `$set` in an update, accidentally replacing an entire document instead of updating
  just the intended field(s).
- Using `updateOne`/`deleteOne` when the intent was actually to affect every matching document —
  the "One" variants only ever touch the first match.
- Reaching for Mongoose's schema `required`/type options and assuming they're enforced by MongoDB
  itself at the database level — they're actually enforced by Mongoose, in the application layer,
  not by MongoDB's own storage engine.

## Next

Continue to [querying-documents.md](querying-documents.md) to filter results with MongoDB's query
operators.
