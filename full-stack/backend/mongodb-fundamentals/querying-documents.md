# Querying Documents

## The Basic Query Document

```js
db.products.find({ category: "electronics" });
```

A MongoDB query is itself a document: `{ field: value }` matches every document where that field
equals that value — directly comparable to SQL's
[`WHERE category = 'electronics'`](../sql-fundamentals/sql-basics.md), just expressed as a
JavaScript object literal instead of a SQL clause.

## Comparison Query Operators

```js
db.products.find({ price: { $gt: 50 } });               // price > 50
db.products.find({ price: { $lt: 50 } });                // price < 50
db.products.find({ price: { $gte: 50, $lte: 100 } });     // 50 <= price <= 100
db.products.find({ category: { $in: ["electronics", "books"] } }); // category IN (...)
db.products.find({ category: { $ne: "clothing" } });       // category != "clothing"
```

MongoDB's comparison operators (`$gt`, `$lt`, `$gte`, `$lte`, `$in`, `$ne`) directly parallel SQL's
`>`, `<`, `>=`, `<=`, `IN`, and `!=` — the same filtering concepts from
[sql-basics.md](../sql-fundamentals/sql-basics.md), expressed as named operators inside the query
document rather than inline comparison syntax.

## Combining Conditions

```js
// Implicit AND — both conditions must match
db.products.find({ category: "electronics", price: { $gt: 50 } });

// Explicit $or
db.products.find({ $or: [{ category: "electronics" }, { price: { $lt: 10 } }] });
```

Multiple fields in one query document are implicitly combined with **AND** — every condition must
match. An explicit `$or` operator is needed for OR logic, since it isn't the implicit default the
way AND is.

## Querying Nested Fields

```js
db.products.find({ "dimensions.weight": { $lt: 2 } });
```

A field inside a nested/embedded object (per
[documents-and-collections.md](documents-and-collections.md)'s note on nested documents) is queried
using **dot notation** — a string like `"dimensions.weight"`, with quotes required because of the
dot. This directly reflects MongoDB's ability to nest data within a single document, something a
flat SQL row structure can't do natively.

## Querying Arrays

```js
// Matches if "tags" array contains "wireless" ANYWHERE in it
db.products.find({ tags: "wireless" });

// Matches only if the array contains ALL of these values
db.products.find({ tags: { $all: ["wireless", "rgb"] } });
```

Querying a field that holds an array with a plain value (`tags: "wireless"`) matches any document
where that value appears **anywhere** in the array — a genuinely different, array-aware query
behavior with no direct single-operator SQL equivalent (SQL typically needs a separate join table
or a database-specific array function for the same result).

## `find()` Returns a Cursor, Not an Array

```js
const cursor = db.products.find({ category: "electronics" });
const results = await cursor.toArray(); // explicitly materialize into an array
```

`find()` doesn't return an array directly — it returns a **cursor**, a pointer managing the query's
results, which is then iterated or explicitly converted with `.toArray()`. This distinction matters
for large result sets: a cursor can process results incrementally rather than loading everything
into memory at once.

## Common Mistakes

- Forgetting quotes around a dotted nested-field name (`dimensions.weight` instead of
  `"dimensions.weight"`) — required syntax for the dot-notation query to parse correctly.
- Assuming multiple conditions in one query document are OR'd together by default — they're
  implicitly AND'd; `$or` must be used explicitly for OR logic.
- Treating `find()`'s return value as an already-materialized array, rather than a cursor that
  needs iteration or `.toArray()`.

## Next

Continue to [aggregation-pipeline.md](aggregation-pipeline.md) to transform and summarize data
across many documents at once.
