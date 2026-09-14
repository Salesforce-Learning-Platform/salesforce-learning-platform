# HTTP Methods and CRUD

## The Mapping

| HTTP Method | CRUD Operation | Example |
|---|---|---|
| `GET` | **Read** | `GET /products/42` — fetch a product |
| `POST` | **Create** | `POST /products` — create a new product |
| `PUT` | **Update** (full replace) | `PUT /products/42` — replace the entire product |
| `PATCH` | **Update** (partial) | `PATCH /products/42` — update just one or two fields |
| `DELETE` | **Delete** | `DELETE /products/42` — remove the product |

This mapping is what makes [resource-based-routing.md](resource-based-routing.md)'s pattern work:
the method carries the verb, so the URL only ever needs to identify *which* resource.

## `PUT` vs. `PATCH` — A Genuine, Meaningful Difference

```js
// PUT — the client sends the COMPLETE representation; any field left out
// is treated as intentionally cleared/reset to a default
app.put("/products/:id", (req, res) => {
  products[req.params.id] = req.body; // full replacement
});

// PATCH — the client sends ONLY the fields that should change
app.patch("/products/:id", (req, res) => {
  Object.assign(products[req.params.id], req.body); // partial merge
});
```

`PUT` conceptually **replaces** a resource entirely — if the client omits a field the resource
previously had, the correct behavior is to treat it as removed or reset, not silently preserved.
`PATCH` **merges** only the fields the client explicitly sent, leaving everything else untouched.
Using `PUT` when the intent is actually a partial update is a common, subtly incorrect pattern that
can unexpectedly wipe out fields the client didn't mean to touch.

## Idempotency: A Concept That Actually Matters in Practice

```
Idempotent:     calling it once or many times has the SAME end result
Not idempotent: calling it multiple times can have a DIFFERENT/repeated effect
```

| Method | Idempotent? |
|---|---|
| `GET` | Yes — reading never changes anything |
| `PUT` | Yes — replacing with the same data twice ends in the same state |
| `DELETE` | Yes — deleting an already-deleted resource is still "gone" either way |
| `POST` | **No** — calling it twice typically creates two resources, not one |
| `PATCH` | Generally not guaranteed |

Idempotency matters concretely for reliability: if a client's request times out and it's unsure
whether the server actually received it, safely **retrying** an idempotent request (`PUT`,
`DELETE`) is fine — retrying a non-idempotent `POST`, by contrast, risks creating a duplicate
resource (a duplicate order, a duplicate charge), which is why real payment and order-creation
APIs often add extra safeguards (like an idempotency key) specifically for non-idempotent
operations.

## `GET` Should Never Change Anything

```js
// WRONG — a GET request that has a side effect (deleting data) violates
// a core expectation of the method, and can be triggered accidentally
// (a link preview, a crawler) with destructive consequences
app.get("/products/:id/delete", (req, res) => { /* deletes the product */ });
```

Because `GET` is expected to be both safe (no side effects) and idempotent, browsers, crawlers,
caching layers, and link-preview tools all assume it's always safe to issue a `GET` request without
asking. A `GET` endpoint that actually deletes or modifies data violates that assumption in a way
that can cause real, accidental damage.

## Common Mistakes

- Using `GET` for an operation that has a side effect (creating, updating, or deleting data) —
  violates a widely-relied-upon assumption about what `GET` is safe to do.
- Using `PUT` when the actual intent is a partial update, silently clearing fields the client
  never meant to touch.
- Assuming `POST` is safe to blindly retry on a network failure — it usually isn't, unlike
  idempotent methods.

## Next

Continue to [status-codes.md](status-codes.md) to pair each of these operations with the correct
response status code.
