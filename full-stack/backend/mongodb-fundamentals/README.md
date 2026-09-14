# MongoDB Fundamentals

## Purpose

[SQL Fundamentals](../sql-fundamentals/) covered the relational model — rigid tables, related
through foreign keys. This module introduces **MongoDB**, a **document database**, solving the
same core problem (persisting data durably) with a genuinely different model: flexible,
JSON-shaped documents instead of rigid rows and columns. Every concept in this module is compared
directly against its SQL equivalent, since that's the model you already know.

## Learning Objectives

- Explain what a MongoDB document and collection are, and how they differ from a SQL row and
  table.
- Perform CRUD operations and write basic queries with MongoDB's operators.
- Use the aggregation pipeline to transform and summarize data.
- Connect MongoDB to a Node.js/Express application with Mongoose.
- Choose between embedding and referencing related data — MongoDB's core modeling decision.
- Explain MongoDB indexing, building on the general concept already covered for SQL.

## Prerequisites

- [SQL Fundamentals](../sql-fundamentals/) — this module makes constant direct comparisons back to
  the relational concepts covered there.

## Files in This Module

| File | Covers |
|---|---|
| [introduction-to-mongodb.md](introduction-to-mongodb.md) | What MongoDB is, and why/when a document database differs meaningfully from a relational one |
| [documents-and-collections.md](documents-and-collections.md) | BSON documents, `_id`, collections, and flexible schema |
| [crud-operations.md](crud-operations.md) | `insertOne`, `find`, `updateOne`, `deleteOne`, and connecting MongoDB to Node.js with Mongoose |
| [querying-documents.md](querying-documents.md) | Query operators (`$gt`, `$in`, ...), querying nested fields and arrays |
| [aggregation-pipeline.md](aggregation-pipeline.md) | `$match`, `$group`, `$sort`, `$project`, `$lookup` |
| [data-modeling.md](data-modeling.md) | Embedding vs. referencing — MongoDB's core relationship-modeling decision |
| [indexing.md](indexing.md) | Indexing in MongoDB, and how it compares to the SQL concept already covered |

## When to Deep-Dive vs. Skim

Deep-dive [data-modeling.md](data-modeling.md) — the embed-vs-reference decision has no single
"correct" answer the way a SQL foreign key almost always does; making it well, based on an
application's actual access patterns, is the single hardest and most consequential skill in this
module.

## Quick Knowledge Check

<details>
<summary>Does every document in a MongoDB collection need to have the exact same fields, the way every row in a SQL table needs the same columns?</summary>

No — this is one of the most fundamental differences from the relational model. MongoDB's schema is
flexible by default: one document in a collection can have fields another document in the same
collection doesn't have at all. See
[documents-and-collections.md](documents-and-collections.md).

</details>

<details>
<summary>For a blog post's comments, should they usually be embedded in the post document, or stored in a separate collection and referenced?</summary>

It depends on the actual access pattern and expected growth — a small, bounded number of comments
typically read alongside the post favors embedding; a large or unbounded number of comments (or
ones queried independently of any post) favors referencing. See
[data-modeling.md](data-modeling.md).

</details>

## References

- MongoDB, [Documents](https://www.mongodb.com/docs/manual/core/document/)
- MongoDB, [Query Documents](https://www.mongodb.com/docs/manual/tutorial/query-documents/)
- MongoDB, [Aggregation Pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)
- MongoDB, [Data Modeling Introduction](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/)
- Mongoose, [Documentation](https://mongoosejs.com/docs/index.html)

## Continue Your Learning Path

Continue to the [Database Design and Modeling module](../database-design-and-modeling/) to see the
principles that apply across both SQL and MongoDB, and how to choose between them for a given
project.
