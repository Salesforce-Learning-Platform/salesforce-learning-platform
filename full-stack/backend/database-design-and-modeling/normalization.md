# Normalization

## The Problem Normalization Solves

```
BAD: repeating a customer's full details on every single order row
┌─────────┬───────────────┬─────────────────────┬───────┐
│ order_id│ customer_name │ customer_email      │ total │
├─────────┼───────────────┼─────────────────────┼───────┤
│    1    │ Alice Smith   │ alice@example.com   │ 79.99 │
│    2    │ Alice Smith   │ alice@example.com   │ 29.99 │  ← duplicated
└─────────┴───────────────┴─────────────────────┴───────┘
```

Storing a customer's full details redundantly on every order row creates three real, named
problems: an **update anomaly** (updating Alice's email on one order row but forgetting the other
leaves inconsistent data), an **insertion anomaly** (you can't record a customer's existence until
they place an order at all), and a **deletion anomaly** (deleting Alice's only order accidentally
erases every trace of her as a customer). **Normalization** is the discipline of structuring tables
specifically to eliminate these problems.

## First Normal Form (1NF) — Atomic Values

```
BAD (not 1NF): multiple values crammed into one field
┌────┬──────────────────────┐
│ id │ tags                 │
├────┼──────────────────────┤
│ 1  │ "wireless, rgb, usb" │  ← not atomic
└────┴──────────────────────┘

GOOD (1NF): one value per field, related values in their own table
products(id, name)          tags(product_id, tag)
```

**1NF** requires every field to hold a single, atomic value — no comma-separated lists or nested
sets crammed into one column. A field needing to hold multiple related values instead becomes its
own separate table.

## Second Normal Form (2NF) — Full Dependency on the Whole Key

**2NF** applies specifically to tables with a composite (multi-column) primary key: every other
column must depend on the **entire** key, not just part of it. If a column only actually depends on
part of a composite key, it belongs in a separate table keyed by just that part instead.

## Third Normal Form (3NF) — No Transitive Dependencies

```
BAD (not 3NF): category_description depends on category, not directly on product id
products(id, name, category, category_description)

GOOD (3NF): category_description moved to its own table
products(id, name, category_id)     categories(id, name, description)
```

**3NF** eliminates **transitive dependencies** — a non-key column that actually depends on another
non-key column, rather than depending directly on the primary key. `category_description` here
genuinely depends on `category`, not on the product's own `id` — so it belongs in its own
`categories` table instead.

## Normalization's Real Cost: More Joins

```sql
-- A fully normalized schema needs a JOIN just to show a product with its category name
SELECT products.name, categories.name AS category_name
FROM products JOIN categories ON products.category_id = categories.id;
```

Normalization isn't free — every split into a separate table is a table a query later has to
[`JOIN`](../sql-fundamentals/joins.md) back together to reconstruct the full picture. This is a
real, deliberate tradeoff: less redundancy and stronger consistency, at the cost of more complex
queries.

## When Denormalization Is the Right Call

```
Sometimes deliberately duplicating a small piece of data (like storing
a product's name directly on an order-line row, as it existed AT THE
TIME of the order) is the correct choice — even though it's technically
"redundant" by normalization's rules.
```

A fully normalized schema isn't automatically the "best" one for every situation. **Denormalization**
— deliberately duplicating some data — is a legitimate, common tradeoff when read performance
matters more than storage efficiency, or when historical accuracy genuinely requires it (an order's
line item should show the product's price *at the time of purchase*, not its current price, which
argues for storing that price directly on the order line rather than always joining to the
product's current price). The key word is *deliberate* — a good denormalization decision is a
conscious tradeoff, not an accident of not normalizing in the first place.

## Common Mistakes

- Treating "fully normalized" as an unconditional goal, rather than one end of a real tradeoff
  against query complexity and performance.
- Denormalizing accidentally, by not thinking through the relationships at all, rather than as a
  deliberate, justified performance or correctness decision.
- Forgetting that an order's historical details (price, product name at time of purchase) often
  genuinely *should* be denormalized/duplicated, since the "current" value in a normalized products
  table isn't actually what a past order should reflect.

## Next

Continue to [sql-vs-nosql.md](sql-vs-nosql.md) to bring everything in this module together into
the actual decision of which database to use for a given project.
