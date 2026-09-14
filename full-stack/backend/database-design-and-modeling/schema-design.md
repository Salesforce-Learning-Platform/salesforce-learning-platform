# Schema Design

## Choosing the Right Primary Key

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,   -- auto-incrementing integer — simple, sequential
  sku TEXT UNIQUE NOT NULL -- a genuine business identifier, also unique, but distinct from the PK
);
```

Every table needs a **primary key** (per
[SQL's sql-basics.md](../sql-fundamentals/sql-basics.md)) — a value that uniquely identifies each
row. A simple auto-incrementing integer (`SERIAL`) is the common default: it's small, fast to
index, and carries no business meaning of its own. A genuinely meaningful business identifier (like
a product SKU) can still exist as a separate `UNIQUE` column — but using it directly as the primary
key is usually avoided, since business identifiers sometimes need to change, and a primary key
generally shouldn't.

## Choosing Data Types Deliberately

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC(10, 2) NOT NULL,   -- exact decimal — never use FLOAT for money
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

Choosing the right data type is a real design decision, not a formality: `NUMERIC` (exact decimal
arithmetic) is the correct type for money — a floating-point type can introduce tiny rounding
errors that are unacceptable for financial data. `TIMESTAMP` with a sensible `DEFAULT NOW()`
correctly captures when a row was created without requiring the application to remember to set it.
`BOOLEAN` for a true/false flag is more precise and self-documenting than an integer `0`/`1`
convention.

## Constraints Express Real Business Rules

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
  category TEXT NOT NULL CHECK (category IN ('electronics', 'clothing', 'books'))
);
```

`NOT NULL`, `UNIQUE`, and `CHECK` constraints let the schema itself express and enforce genuine
business rules — "a price can never be negative," "a category must be one of these specific
values" — directly at the database layer, per
[database-design-principles.md](database-design-principles.md)'s point about enforcing integrity as
close to the data as possible.

## Naming Conventions Matter More Than They Seem To

```sql
-- Consistent: snake_case, singular table names, "_id" suffix for foreign keys
CREATE TABLE product (
  id SERIAL PRIMARY KEY,
  category_id INTEGER REFERENCES category(id)
);
```

A consistent naming convention (commonly `snake_case` for SQL identifiers, a consistent singular or
plural choice for table names, and a predictable suffix like `_id` for foreign key columns) makes
an unfamiliar schema — someone else's, or your own months later — genuinely faster to read and
navigate, echoing the same "predictability helps everyone" reasoning behind
[REST's resource-based-routing.md](../rest-api-design/resource-based-routing.md)'s consistent URL
conventions.

## The MongoDB Equivalent: Schema Validation

```js
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      required: ["name", "price"],
      properties: {
        price: { bsonType: "number", minimum: 0 },
      },
    },
  },
});
```

MongoDB's flexible schema (per
[documents-and-collections.md](../mongodb-fundamentals/documents-and-collections.md)) doesn't mean
schema design doesn't matter there — it means enforcement is opt-in rather than automatic. MongoDB
supports its own `$jsonSchema` validation (or, more commonly in practice, Mongoose's schema layer,
covered in [MongoDB's crud-operations.md](../mongodb-fundamentals/crud-operations.md)) to bring
back the same kind of deliberate structure and constraints SQL enforces natively.

## Common Mistakes

- Using a floating-point type for monetary values instead of an exact decimal type, risking subtle
  rounding errors over time.
- Choosing a business-meaningful value (like an email or a SKU) directly as a primary key, then
  needing a disruptive schema change the first time that value legitimately needs to change.
- Skipping schema validation entirely in MongoDB just because it's optional, ending up with the
  exact inconsistent-document problem flexible schema design is meant to allow avoiding, not force.

## Next

Continue to [relationships.md](relationships.md) to model how tables and collections actually
relate to each other.
