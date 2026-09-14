# Introduction to MongoDB

## A Different Model for the Same Underlying Problem

[SQL Fundamentals](../sql-fundamentals/) solved data persistence with the relational model — fixed
tables of rows and columns, related through foreign keys and combined with `JOIN`. **MongoDB** is a
**document database**: it stores data as flexible, JSON-shaped documents grouped into collections,
rather than rigid rows grouped into tables.

## The Core Difference, Immediately

```sql
-- SQL: a user's data spread across a fixed row shape
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
```

```js
// MongoDB: a document, shaped like the actual object the application uses
db.users.insertOne({
  name: "Alice",
  email: "alice@example.com",
  preferences: { theme: "dark", notifications: true },
});
```

A MongoDB document can contain nested objects and arrays directly — `preferences` here is a nested
object living inside the same document, with no separate table or `JOIN` required to read it back
out. This maps naturally onto how data already looks in application code (a JavaScript object), a
genuinely different starting point than SQL's flat, row-based structure.

## Why This Genuinely Matters, Not Just Syntactically

- **No object-relational mapping needed**: a MongoDB document can closely mirror the exact shape of
  a JavaScript object your application already works with, whereas SQL data typically needs
  translating between rows/columns and application objects.
- **Flexible schema**: unlike a SQL table (where every row must have the same columns), one
  document in a MongoDB collection can have fields another document in the same collection lacks
  entirely — covered fully in
  [documents-and-collections.md](documents-and-collections.md).
- **Different relationship handling**: instead of always normalizing related data into separate
  tables joined at query time (SQL's default), MongoDB commonly **embeds** related data directly
  within a document — a deliberate design choice covered in
  [data-modeling.md](data-modeling.md).

## When Document Databases Fit Well

MongoDB tends to fit naturally when an application's data is genuinely document-shaped — content
that's usually read and written as a whole unit (a user profile, a product catalog entry, a blog
post with its metadata) — and when a flexible, evolving schema across different documents in the
same collection is a real advantage rather than a liability.

## When Relational Still Wins

Data with many genuine, strict, highly interconnected relationships — and workloads that need
strong transactional guarantees across multiple related pieces of data changing together — are
often still better served by the relational model's structure, exactly why
[Database Design and Modeling](../database-design-and-modeling/) treats "SQL vs. NoSQL" as a real
design decision, not a settled question with one universally correct answer.

## Common Mistakes

- Assuming MongoDB is a strict upgrade or replacement for SQL databases — it's a genuinely
  different tool with different strengths, not a universally superior option.
- Treating MongoDB's flexible schema as license to store wildly inconsistent document shapes within
  the same collection with no discipline at all — flexibility is a tool, not an excuse to skip
  intentional design.
- Expecting MongoDB's query language to look like SQL — the syntax (covered starting in
  [documents-and-collections.md](documents-and-collections.md)) is genuinely different, even though
  many of the underlying concepts (filtering, sorting, aggregating) transfer directly.

## Next

Continue to [documents-and-collections.md](documents-and-collections.md) to see exactly what a
document and a collection actually look like.
