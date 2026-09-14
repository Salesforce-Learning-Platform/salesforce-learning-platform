# SQL vs. NoSQL

## The Decision This Module Has Been Building Toward

Every concept so far — [design principles](database-design-principles.md),
[schema design](schema-design.md), [relationships](relationships.md), and
[normalization](normalization.md) — applies to both models, but expresses itself differently in
each. This file makes the actual, concrete decision: given a real project, which one to reach for.

## What "NoSQL" Actually Means

"NoSQL" is a broad umbrella term covering several genuinely different non-relational database
types — MongoDB (document), Redis (key-value), and others each work differently. This module, and
this comparison, focuses specifically on the document model covered in
[MongoDB Fundamentals](../mongodb-fundamentals/), since that's the NoSQL style most directly
comparable to SQL's row-based model for typical backend application data.

## Real Decision Criteria, Not Trend-Following

| Consider **SQL (relational)** when | Consider **MongoDB (document)** when |
|---|---|
| Data has many genuine, strict relationships that need enforcement | Data is naturally document-shaped, read/written as whole units |
| Strong consistency and transactional guarantees across related data matter a lot | Schema needs to evolve flexibly, without disruptive migrations |
| The schema is relatively stable and well-understood upfront | The exact shape of the data isn't fully known yet, or varies across records |
| Complex, ad hoc queries across many relationships are common | Most access patterns are known and can be optimized via embedding |

Neither database is universally "better" — the right choice depends on the actual shape of the
data and the actual access patterns of the application being built, not on which one is currently
more popular or trending.

## A Concrete Worked Example: An E-Commerce Platform

- **Order and payment records**: strong candidate for SQL — these need strict consistency (an
  order's total must always match its line items exactly), clear relationships (an order belongs
  to exactly one user), and transactional guarantees (a payment and an inventory decrement should
  either both succeed or both fail together).
- **Product catalog with widely varying attributes** (a book has an author and ISBN; a t-shirt has
  a size and color; a laptop has dozens of technical specs): a strong candidate for MongoDB — the
  flexible schema (per
  [MongoDB's documents-and-collections.md](../mongodb-fundamentals/documents-and-collections.md))
  naturally accommodates wildly different product types without forcing every product into the
  same fixed set of SQL columns, most of which would be empty for any given product type.

A real production system often genuinely uses **both** — different databases for different parts
of the same application, each chosen for the specific data it's actually best suited to.

## It's Not "SQL Is Old, NoSQL Is Modern"

Both models remain heavily used in real, current production systems — this isn't a story of one
technology superseding the other over time. MongoDB doesn't replace PostgreSQL any more than
PostgreSQL replaces MongoDB; they solve overlapping but genuinely different problems well.

## Common Mistakes

- Choosing a database technology because it's currently popular or because a tutorial used it,
  rather than because its actual model fits the project's real data and access patterns.
- Assuming an entire application must use exactly one database technology throughout — using
  different databases for different parts of a system, each fitted to its own data, is a
  completely normal, common real-world architecture.
- Treating "NoSQL" as one single thing — document databases (MongoDB), key-value stores (Redis),
  and other NoSQL categories work quite differently from each other, and this comparison
  specifically addresses the document model.

## Module Summary

Across this module: good database design applies **domain-driven modeling** and **access-pattern
awareness** regardless of the underlying technology (see
[database-design-principles.md](database-design-principles.md)); a deliberately designed **schema**
— the right primary key choice, precise data types, and constraints — enforces real business rules
directly at the database layer, in both SQL and (via schema validation) MongoDB (see
[schema-design.md](schema-design.md)); **relationships** — one-to-one, one-to-many, and
many-to-many — map differently onto each model, with SQL's junction tables and foreign-key
referential integrity having no direct MongoDB equivalent (see [relationships.md](relationships.md));
**normalization** eliminates redundancy and real anomalies in SQL schemas, at the cost of more
joins, making deliberate denormalization a legitimate tradeoff in the right situations (see
[normalization.md](normalization.md)); and choosing between **SQL and NoSQL** for a real project
comes down to the actual shape of the data and its access patterns, not trend — and a real system
often uses both, each for the part of its data it fits best.
