# Layered Architecture

## The Problem With Putting Everything in One Place

```js
// Everything crammed into a single route handler:
// HTTP handling, business logic, AND raw database access, all mixed together
app.post("/orders", async (req, res) => {
  if (!req.body.productId || !req.body.quantity) {
    return res.status(422).json({ error: "Invalid input" });
  }
  const product = await db.query("SELECT * FROM products WHERE id = $1", [req.body.productId]);
  if (product.rows[0].stock < req.body.quantity) {
    return res.status(409).json({ error: "Insufficient stock" });
  }
  const order = await db.query("INSERT INTO orders ...", [/* ... */]);
  await db.query("UPDATE products SET stock = stock - $1 WHERE id = $2", [req.body.quantity, req.body.productId]);
  res.status(201).json(order.rows[0]);
});
```

This works, but it mixes three genuinely different concerns into one function: handling the raw
HTTP request/response, applying real business rules (checking stock), and talking directly to the
database. As a real application grows past a handful of routes, this pattern makes every route
handler progressively harder to read, test, and reuse logic from.

## Separating Concerns Into Layers

```
Request → [Controller] → [Service] → [Repository] → Database
           HTTP only      business      data access
                           logic only    only
```

**Layered architecture** deliberately separates a backend into distinct layers, each with one
clear responsibility, and each layer only ever talking to the layer directly below it. This isn't
a new idea specific to backend work — it's the same underlying discipline behind
[Frontend Architecture's design-systems-at-scale](../../frontend/frontend-architecture/design-systems-at-scale/)
and [React's component-architecture-and-composition](../../frontend/react/component-architecture-and-composition/):
each unit should do one job well, and depend on clear, stable boundaries rather than reaching
directly into unrelated concerns.

## Why This Actually Matters, Not Just Aesthetically

- **Testability**: business logic (the service layer) can be tested directly, with a fake/mock
  repository, without needing a real running database or a real HTTP request at all.
- **Reusability**: the same service-layer logic (like "place an order, checking stock") can be
  called from multiple places — an HTTP route, a scheduled background job, a CLI script — without
  duplicating the actual business rule.
- **Maintainability**: changing *how* data is stored (switching from
  [SQL to MongoDB](../database-design-and-modeling/sql-vs-nosql.md), say) only requires changing
  the repository layer — the business logic and HTTP handling above it don't need to change at
  all, since they only ever depended on the repository's interface, not its implementation.

## The Concrete Layers Used in This Module

| Layer | Responsibility | Analogous to |
|---|---|---|
| **Controller** | Read the HTTP request, call the service, send the HTTP response | An Express route handler's *only* job |
| **Service** | Business logic and rules — the actual "what should happen" | The application's real domain logic |
| **Repository** | Talk to the database — the actual "how data is stored and retrieved" | [SQL](../sql-fundamentals/) or [MongoDB](../mongodb-fundamentals/) queries, isolated in one place |

[controllers-services-and-repositories.md](controllers-services-and-repositories.md) makes this
concrete with real Express code.

## Common Mistakes

- Skipping layering entirely for a "quick" project, then finding the same tangled, all-in-one-file
  pattern impossible to untangle once the project inevitably grows larger than originally planned.
- Over-layering a genuinely tiny project — a five-route prototype rarely needs the same rigor as a
  production system serving real, growing traffic; the right amount of structure scales with the
  project's actual complexity.
- Letting a "higher" layer (a controller) reach directly into a "lower" layer it shouldn't touch
  (raw database access), defeating the whole point of having layer boundaries at all.

## Next

Continue to
[controllers-services-and-repositories.md](controllers-services-and-repositories.md) to see this
pattern applied concretely to a real Express codebase.
