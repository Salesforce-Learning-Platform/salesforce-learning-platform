# Resource-Based Routing

## Naming Routes Around Nouns

```
GET    /products          list all products
GET    /products/:id      get one specific product
POST   /products          create a new product
PUT    /products/:id      replace a product entirely
PATCH  /products/:id      partially update a product
DELETE /products/:id      remove a product
```

Every route is built around the **resource** (`products`), a plural noun, with the HTTP method
(covered fully in [http-methods.md](http-methods.md)) expressing the actual operation. This one
consistent pattern — resource name, optional ID, method decides the action — scales predictably to
every resource an API needs, rather than requiring a bespoke URL scheme invented per endpoint.

## Plural, Not Singular

```
GOOD: /products, /products/42
AVOID: /product, /product/42
```

The convention is to use the **plural** form of a resource name consistently, even for a route
that returns exactly one item (`GET /products/42` — the plural `products` collection, filtered
down to ID `42`). This keeps the pattern uniform across both collection routes (`GET /products`)
and single-item routes, rather than switching the noun's form depending on which one is being
addressed.

## Nested Resources for Real Relationships

```
GET  /orders/42/items         all line items belonging to order 42
POST /orders/42/items         add a new item to order 42
GET  /orders/42/items/7       one specific item within order 42
```

When one resource genuinely only exists *within* the context of another (an order's line items
don't make sense without an order), nesting the route expresses that ownership directly in the
URL. `req.params` (from
[routing.md](../expressjs-fundamentals/routing.md)) captures both `:orderId` and `:itemId` as
separate values on a route like `/orders/:orderId/items/:itemId`.

## When Not to Nest

```
AVOID: /users/5/orders/42/items/7/reviews/3   (too deep, hard to reason about)
PREFER: /reviews/3                             (a review can stand on its own)
```

Nesting is best reserved for genuinely dependent relationships, and generally shouldn't go more
than one or two levels deep. A resource that has its own independent identity and can be looked up
directly (a review, identifiable by its own ID) is usually better exposed at its own top-level
route, even if it's also reachable through a parent — deeply nested URLs quickly become unwieldy to
both design and consume.

## Action-Oriented Sub-Routes: A Pragmatic Exception

```
POST /orders/42/cancel     cancel order 42
POST /orders/42/ship       mark order 42 as shipped
```

Some real-world operations are genuinely state transitions that don't map cleanly onto a plain
field update — "cancel an order" is more than just `PATCH`ing a `status` field; it might trigger a
refund, release inventory, and send a notification. A resource-oriented action sub-route
(`POST /orders/42/cancel`) is a common, pragmatic pattern for exactly this case — still organized
around the resource, but naming a specific, meaningful action on it.

## Common Mistakes

- Mixing singular and plural resource names inconsistently across an API (`/product` here,
  `/orders` there) — pick one convention (plural) and apply it everywhere.
- Nesting resources so deeply that the resulting URLs become difficult to read, write, and reason
  about — a sign the resource actually deserves its own top-level route.
- Using an action-oriented sub-route (`/orders/42/cancel`) for something that's really just a plain
  field update better expressed with `PATCH /orders/42`, adding unnecessary special-case routes to
  the API's surface.

## Next

Continue to [http-methods.md](http-methods.md) to see exactly which HTTP method belongs on each
kind of route, and why idempotency matters.
