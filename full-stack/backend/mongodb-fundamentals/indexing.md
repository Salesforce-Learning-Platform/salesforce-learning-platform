# Indexing in MongoDB

## The Same Underlying Concept as SQL

MongoDB indexes solve the exact same problem [SQL's indexes.md](../sql-fundamentals/indexes.md)
already covered: without one, a query has to scan every document in a collection (a "collection
scan," directly comparable to SQL's full table scan) to find matches. An index is a separate,
ordered data structure — built on a B-tree, the same underlying structure many SQL databases use —
that lets the database jump directly to matching documents instead.

## Creating a Single-Field Index

```js
db.products.createIndex({ category: 1 });
```

`createIndex({ field: 1 })` indexes that field in ascending order (`-1` for descending). Once
created, a query filtering on `category` (per
[querying-documents.md](querying-documents.md)) no longer needs a full collection scan.

## The Same Tradeoff as SQL, Exactly

| | Without an index | With an index |
|---|---|---|
| Reads filtering on the indexed field | Scans every document | Looks up directly — much faster |
| Writes (insert/update/delete) | No extra work | Must also update the index |
| Storage | Just the collection | The collection, plus the index's own space |

This is genuinely the identical tradeoff [SQL's indexes.md](../sql-fundamentals/indexes.md)
covers: faster reads, slower writes, more storage — a deliberate choice for fields actually queried
frequently, not something to apply indiscriminately to every field.

## Compound Indexes

```js
db.products.createIndex({ category: 1, price: -1 });
```

A **compound index** covers multiple fields together — here, `category` ascending and `price`
descending — useful specifically for queries that filter or sort on that exact combination of
fields, the MongoDB equivalent of a multi-column SQL index.

## `_id` Is Automatically Indexed

```js
// No manual step needed — every collection automatically has a
// unique index on _id from the moment it's created
db.products.findOne({ _id: someId }); // already fast, with no setup required
```

Exactly like a SQL primary key (per [SQL's indexes.md](../sql-fundamentals/indexes.md)), MongoDB
automatically creates a unique index on `_id` — no manual `createIndex` call needed for lookups by
ID specifically.

## Common Mistakes

- Creating an index on every field "just in case," incurring the write and storage cost broadly
  without a matching read benefit — the exact same mistake, and the exact same reasoning against
  it, as in SQL.
- Building a large index on an already-populated, actively-used collection without planning for the
  temporary performance impact the build itself can have.
- Creating a compound index in the wrong field order for the actual queries it's meant to serve —
  the order fields are listed in a compound index genuinely matters for which queries it can
  efficiently support.

## Module Summary

Across this module: **MongoDB** is a document database, storing flexible, JSON-shaped documents in
collections rather than SQL's rigid rows and tables, and suited to genuinely different use cases
than the relational model (see [introduction-to-mongodb.md](introduction-to-mongodb.md)); a
**document**'s `_id` plays the same role as a SQL primary key, while a **collection**'s schema is
flexible by default, unlike a SQL table (see
[documents-and-collections.md](documents-and-collections.md)); **CRUD operations**
(`insertOne`/`find`/`updateOne`/`deleteOne`, with `$set` critical for partial updates) map directly
onto SQL's CRUD, connected to Express via Mongoose (see
[crud-operations.md](crud-operations.md)); **query operators** (`$gt`, `$in`, dot notation for
nested fields) parallel SQL's `WHERE` (see [querying-documents.md](querying-documents.md)); the
**aggregation pipeline**'s stages (`$match`, `$group`, `$sort`, `$lookup`) parallel SQL's
`WHERE`/`GROUP BY`/`ORDER BY`/`JOIN` (see [aggregation-pipeline.md](aggregation-pipeline.md));
choosing between **embedding and referencing** related data — based on actual access patterns, not
a fixed default — is MongoDB's single most consequential modeling decision (see
[data-modeling.md](data-modeling.md)); and **indexing** works identically in principle to SQL's,
trading write performance and storage for much faster reads.
