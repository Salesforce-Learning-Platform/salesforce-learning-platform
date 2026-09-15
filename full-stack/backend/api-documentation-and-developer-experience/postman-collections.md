# 🗂️ Postman Collections

## A Saved, Organized Set of Real Requests

```
Shop API (collection)
├── Products
│   ├── List all products     (GET /products)
│   ├── Get a product         (GET /products/:id)
│   └── Create a product      (POST /products)
├── Orders
│   ├── List my orders        (GET /orders/mine)
│   └── Place an order        (POST /orders)
└── Auth
    ├── Register              (POST /auth/register)
    └── Login                 (POST /auth/login)
```

A **Postman collection** groups a set of saved, real HTTP requests — organized into folders,
exactly mirroring an API's actual resource structure (per
[REST's resource-based-routing.md](../rest-api-design/resource-based-routing.md)). Every request in
a collection is saved with its real method, URL, headers, and body — ready to run again at any
time, rather than manually reconstructing a request from scratch every time it needs testing.

## Why a Team Shares One Collection, Rather Than Everyone Building Their Own

Sharing a single, well-organized collection means every team member (or a new hire joining the
project) can immediately explore and test a real API without needing to read through route
definitions in the source code first — a genuinely faster onboarding path than reading raw Express
route files, and a living reference that stays close to the API's actual current shape.

## Environments — Reusing One Collection Across Dev/Staging/Production

```
{{baseUrl}}/products/{{productId}}

# Dev environment:        baseUrl = http://localhost:3000
# Staging environment:    baseUrl = https://staging.example.com
# Production environment: baseUrl = https://api.example.com
```

A Postman **environment** defines variables (like `{{baseUrl}}`) that a collection's requests
reference instead of a hardcoded URL — directly the same "don't hardcode what varies between
deploys" principle from
[configuration-management.md](../backend-architecture/configuration-management.md), applied here
to a team's testing tool rather than the application itself. Switching environments lets the exact
same collection run against a local server, staging, or production without editing a single
request.

## Collections as Living Documentation

Beyond manual testing, a well-organized collection functions as a second, more hands-on form of
documentation alongside the OpenAPI spec from
[documenting-apis-with-swagger.md](documenting-apis-with-swagger.md) — someone exploring an API for
the first time can often understand it faster by running real, pre-built requests and inspecting
real responses than by reading a static spec alone.

## Common Mistakes

- Letting every team member maintain their own separate, informal collection of requests instead of
  a single shared one, causing the same request to be recreated slightly differently by each person.
- Hardcoding a specific environment's URL directly into every request instead of using environment
  variables, making the collection unusable against any other environment without manual edits.
- Letting a shared collection go stale as the real API changes, the same "documentation drifts out
  of sync" problem [documenting-apis-with-swagger.md](documenting-apis-with-swagger.md) already
  warned about.

## ➡️ Next

Continue to [api-versioning-strategy.md](api-versioning-strategy.md) to see how both the OpenAPI
spec and a shared collection need to evolve as an API itself changes over time.
