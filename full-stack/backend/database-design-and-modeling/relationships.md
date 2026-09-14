# Relationships

## One-to-One

```sql
-- SQL: a foreign key with a UNIQUE constraint enforces "at most one"
CREATE TABLE user_profiles (
  user_id INTEGER UNIQUE REFERENCES users(id),
  bio TEXT
);
```

```js
// MongoDB: commonly just embedded directly, per data-modeling.md
{ _id: "u1", name: "Alice", profile: { bio: "..." } }
```

A **one-to-one** relationship means each record on one side relates to exactly one record on the
other. In SQL, a foreign key with a `UNIQUE` constraint enforces this at the database level. In
MongoDB, a one-to-one relationship is frequently just embedded directly (per
[MongoDB's data-modeling.md](../mongodb-fundamentals/data-modeling.md)) rather than split across
two collections at all, since there's no real benefit to separating data that's always exactly
paired.

## One-to-Many

```sql
-- SQL: the foreign key lives on the "many" side
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id)
);
```

```js
// MongoDB: referencing (for a large/unbounded "many") ...
{ _id: "o1", userId: "u1", total: 79.99 }

// ... or embedding (for a small, bounded "many")
{ _id: "u1", name: "Alice", recentOrders: [{ total: 79.99 }] }
```

A **one-to-many** relationship (one user, many orders) is modeled in SQL with the foreign key placed
on the "many" side — each order row points back to exactly one user. MongoDB can model the same
relationship either way, per
[MongoDB's data-modeling.md](../mongodb-fundamentals/data-modeling.md)'s embed-vs-reference
decision: referencing for an unbounded number of orders, embedding for a small, bounded, always
together-accessed set.

## Many-to-Many — the Genuinely Different Case

```sql
-- SQL: requires a separate JUNCTION (join) table
CREATE TABLE order_items (
  order_id INTEGER REFERENCES orders(id),
  product_id INTEGER REFERENCES products(id),
  quantity INTEGER NOT NULL,
  PRIMARY KEY (order_id, product_id)
);
```

```js
// MongoDB: no junction-table convention — typically an array of
// references on one (or both) sides instead
{
  _id: "o1",
  items: [
    { productId: "p1", quantity: 2 },
    { productId: "p2", quantity: 1 },
  ],
}
```

A **many-to-many** relationship (an order can contain many products, and a product can appear in
many orders) genuinely can't be expressed with a single foreign key on either table — SQL requires
a dedicated **junction table** (`order_items`) whose own rows represent each specific pairing, often
carrying relationship-specific data of its own (`quantity`) beyond just the two IDs. MongoDB has no
equivalent junction-collection convention — this relationship is usually modeled with an embedded
array of references (as above), since MongoDB's document model makes storing a list of related IDs
(or small related objects) directly inside a document entirely natural.

## Referential Integrity — SQL's Built-In Guarantee

```sql
product_id INTEGER REFERENCES products(id) ON DELETE RESTRICT
```

A SQL foreign key, once declared, is actively **enforced** by the database — attempting to insert
an order referencing a `product_id` that doesn't exist in `products` simply fails. `ON DELETE`
options (`RESTRICT`, `CASCADE`, `SET NULL`) control exactly what happens to related rows when a
referenced row is deleted: `RESTRICT` blocks the deletion outright, `CASCADE` automatically deletes
the dependent rows too, and `SET NULL` clears the reference instead of deleting anything. MongoDB
has no equivalent automatic enforcement — a reference to a deleted document silently becomes a
"dangling" ID unless the application explicitly checks for and handles that case itself.

## Common Mistakes

- Modeling a many-to-many relationship in SQL with two separate one-to-many foreign keys instead of
  a proper junction table — this can't actually represent the full relationship correctly.
- Assuming MongoDB enforces referential integrity the way SQL's foreign keys do — it doesn't
  automatically prevent or clean up references to a deleted document; that's the application's
  responsibility if it's needed at all.
- Choosing `ON DELETE CASCADE` without genuinely intending for related data to disappear
  automatically — a common, sometimes destructive mistake when the actual intent was `RESTRICT` or
  `SET NULL`.

## Next

Continue to [normalization.md](normalization.md) to see the deeper reasoning behind why SQL
schemas are typically split into many related tables in the first place.
