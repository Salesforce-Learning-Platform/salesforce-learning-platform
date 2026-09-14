# API Versioning

## Why an API Needs Versioning At All

An API rarely stays frozen forever — fields get renamed, response shapes change, behavior needs to
evolve. The problem: once an API is live, other teams' or other companies' code (a mobile app
already published to app stores, a partner's integration) is already depending on its *current*
exact shape. **Versioning** is the discipline of evolving an API without silently breaking every
client that's already built against the previous version.

## URL Path Versioning — the Most Common Approach

```
GET /v1/products
GET /v2/products
```

```js
import productsV1Router from "./routes/v1/products.js";
import productsV2Router from "./routes/v2/products.js";

app.use("/v1/products", productsV1Router);
app.use("/v2/products", productsV2Router);
```

Embedding the version directly in the URL path (`/v1/...`) is simple, highly visible, and trivial
to route — Express can mount an entirely separate `Router` (per
[routing.md](../expressjs-fundamentals/routing.md)) per version, letting `v1` and `v2` coexist as
genuinely independent code paths for as long as `v1` still needs support.

## Header-Based Versioning — an Alternative

```
GET /products
Accept: application/vnd.myapi.v2+json
```

Some APIs instead put the version in a request header rather than the URL, keeping the URL itself
version-free. This is a defensible, real-world alternative — the tradeoff is that it's less
immediately visible (a developer can't tell an endpoint's version just by glancing at the URL) and
somewhat less common in practice than the URL-path approach.

## Backward-Compatible Changes Don't Need a New Version

| Change | Needs a new version? |
|---|---|
| Adding a new, optional field to a response | No — existing clients simply ignore it |
| Adding a brand-new endpoint | No — doesn't affect anything already in use |
| Removing a field a client relies on | **Yes** — a breaking change |
| Renaming a field | **Yes** — a breaking change |
| Changing a field's type or meaning | **Yes** — a breaking change |

Not every change is a **breaking** change. Adding something new, additive, and optional is safe
without bumping the version at all — this mirrors the same reasoning behind
[Semantic Versioning](../starting-with-nodejs/npm-and-package-management.md)'s major/minor/patch
distinction for npm packages: only a genuinely breaking change requires a new major version (or, for
an API, a new version number in the URL).

## Deprecating an Old Version Gracefully

```json
{
  "data": [ /* ... */ ],
  "meta": {
    "deprecationWarning": "v1 will be sunset on 2027-01-01. Please migrate to v2."
  }
}
```

Removing an old API version immediately the moment a new one ships breaks every client still using
it, with no warning. The standard pattern — directly analogous to
[consistency-at-scale.md](../../frontend/frontend-architecture/design-systems-at-scale/consistency-at-scale.md)'s
coverage of deprecating a component library API — is to keep the old version running, clearly
marked as deprecated (often with a warning header or field, and a documented sunset date), giving
every consuming team or client a real window to migrate before it's actually removed.

## Common Mistakes

- Bumping the API's version for every single change, including harmless, additive ones — creating
  unnecessary version sprawl and forcing clients to "upgrade" for changes that never actually
  affected them.
- Silently changing an existing field's meaning or removing it without a version bump at all,
  breaking every client depending on the old behavior with no warning.
- Deleting an old API version the moment a new one ships, instead of giving existing clients a
  real, communicated migration window.

## Module Summary

Across this module: **REST's core principles** — resources instead of actions, statelessness, and
a uniform interface — are what make an API predictable across every endpoint (see
[rest-principles.md](rest-principles.md)); **resource-based routing** names routes around plural
nouns, nests genuinely dependent resources, and uses action sub-routes pragmatically for real state
transitions (see [resource-based-routing.md](resource-based-routing.md)); **HTTP methods** map
directly onto CRUD, with `PUT` vs. `PATCH` and idempotency being genuinely meaningful distinctions
(see [http-methods.md](http-methods.md)); **status codes** follow REST-specific conventions per
operation — `201` for creation, `204` for an empty successful delete, `409` for a state conflict
(see [status-codes.md](status-codes.md)); **request validation**, via Zod or express-validator,
happens once at the request boundary so everything downstream can trust the data's shape (see
[request-validation.md](request-validation.md)); **pagination, filtering, and sorting**, via query
parameters, keep collection endpoints fast and usable as data grows (see
[pagination-filtering-and-sorting.md](pagination-filtering-and-sorting.md)); and **API versioning**
lets an API evolve without breaking clients already depending on its current shape.
