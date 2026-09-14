# Database Design and Modeling

## Purpose

[SQL Fundamentals](../sql-fundamentals/) and [MongoDB Fundamentals](../mongodb-fundamentals/)
taught the query language and API of two genuinely different databases. This module steps back to
the design principles that apply **across both**: how to model relationships, how to structure a
schema well, and — the question underlying everything else — how to actually choose between a
relational and a document database for a real project.

## Learning Objectives

- Apply core database design principles regardless of which database technology is used.
- Design a schema with appropriate keys, constraints, and data types.
- Model one-to-one, one-to-many, and many-to-many relationships correctly.
- Explain normalization and why it matters, alongside when denormalization is the right call.
- Choose between SQL and NoSQL for a given project, based on real tradeoffs rather than trend.

## Prerequisites

- [SQL Fundamentals](../sql-fundamentals/) and [MongoDB Fundamentals](../mongodb-fundamentals/) —
  this module assumes both, and compares them constantly.

## Files in This Module

| File | Covers |
|---|---|
| [database-design-principles.md](database-design-principles.md) | Core principles that apply regardless of database technology |
| [schema-design.md](schema-design.md) | Keys, constraints, and data types, designed deliberately |
| [relationships.md](relationships.md) | One-to-one, one-to-many, and many-to-many, modeled in both SQL and MongoDB |
| [normalization.md](normalization.md) | 1NF/2NF/3NF, the anomalies they prevent, and when denormalization is the right tradeoff |
| [sql-vs-nosql.md](sql-vs-nosql.md) | Choosing the right database for a project, based on real, concrete criteria |

## When to Deep-Dive vs. Skim

Deep-dive [sql-vs-nosql.md](sql-vs-nosql.md) — this decision has real, lasting consequences for a
real project, and making it well (rather than by trend or habit) is exactly the kind of judgment
this module exists to build.

## Quick Knowledge Check

<details>
<summary>Is a many-to-many relationship modeled the same way in SQL and MongoDB?</summary>

No — SQL requires a separate junction/join table connecting the two related tables; MongoDB
typically models it through referencing (an array of IDs on one or both sides) rather than a
dedicated third collection, since it has no equivalent join-table convention. See
[relationships.md](relationships.md).

</details>

<details>
<summary>Is a normalized schema always the "correct" one to use?</summary>

No — normalization reduces redundancy and prevents update/insert/delete anomalies, but it also
means more joins to reconstruct related data. A deliberately denormalized schema (duplicating some
data) can be the right tradeoff when read performance matters more than storage efficiency or
write-time consistency for a specific use case. See [normalization.md](normalization.md).

</details>

## References

- PostgreSQL, [Constraints: Foreign Keys](https://www.postgresql.org/docs/current/ddl-constraints.html)
- Wikipedia, [Database normalization](https://en.wikipedia.org/wiki/Database_normalization)

## Continue Your Learning Path

Continue to the [Authentication and Authorization module](../authentication-and-authorization/) to
secure the APIs and data modeled throughout this domain so far.
