# Database Design Principles

## Principles That Outlive Any Specific Technology

[SQL Fundamentals](../sql-fundamentals/) and [MongoDB Fundamentals](../mongodb-fundamentals/)
taught two genuinely different query languages and storage models. Underneath both, though, the
same design principles apply — a well-designed PostgreSQL schema and a well-designed MongoDB
collection layout are both the product of the same underlying discipline, just expressed
differently.

## Model the Real Domain, Not an Arbitrary Structure

```
A "product" isn't just "whatever fields are convenient to store" —
it's a deliberate model of a real thing the business actually deals
with: it has a name, a price, a category, and a genuine relationship
to orders, reviews, and inventory.
```

Good database design starts from understanding the actual domain — the real entities (products,
orders, users) and how they genuinely relate to each other — rather than shaping a schema around
whatever happens to be easiest to code against today. A schema that accurately reflects the real
domain tends to stay stable and extend cleanly; one that doesn't tends to accumulate awkward
special cases as requirements evolve.

## Design for How Data Will Actually Be Accessed

This is the same underlying idea behind
[MongoDB's data-modeling.md](../mongodb-fundamentals/data-modeling.md)'s "data accessed together
should be stored together" principle — but it applies to SQL schema design too, in the form of
choosing sensible indexes (per [SQL's indexes.md](../sql-fundamentals/indexes.md)) for the queries
an application will actually run most often. Designing a schema in a vacuum, without any thought to
the real queries it needs to serve, routinely produces a structure that's technically correct but
practically slow or awkward to query.

## Enforce Data Integrity as Close to the Data as Possible

```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  product_id INTEGER NOT NULL REFERENCES products(id),
  quantity INTEGER NOT NULL CHECK (quantity > 0)
);
```

A `NOT NULL` constraint, a foreign key (per
[relationships.md](relationships.md)), or a `CHECK` constraint enforces a rule directly at the
database layer — meaning it's genuinely impossible to violate, regardless of which application code
path writes the data. This is a stronger guarantee than validating the same rule only in
application code (per
[REST's request-validation.md](../rest-api-design/request-validation.md)), which protects against
mistakes only in the code paths that actually run that validation.

## Plan for Change, Without Over-Engineering for It

A schema should be able to evolve as real requirements change — but designing excessive flexibility
"just in case" for changes that may never actually happen adds real complexity for no realized
benefit. The right amount of flexibility is guided by genuine, reasonably foreseeable future needs,
not unlimited hypothetical ones.

## Common Mistakes

- Designing a schema around what's easiest to code today rather than what accurately reflects the
  real domain, producing awkward special cases as real requirements surface later.
- Relying entirely on application-level validation for a rule that could be enforced directly by
  the database, leaving a gap any code path that skips the validation can slip through.
- Over-engineering a schema for hypothetical future flexibility that never actually materializes,
  adding real complexity the application never benefits from.

## Next

Continue to [schema-design.md](schema-design.md) to apply these principles concretely — choosing
keys, constraints, and data types deliberately.
