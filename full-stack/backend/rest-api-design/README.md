# REST API Design

## Purpose

[Express.js Fundamentals](../expressjs-fundamentals/) taught you *how* to define routes and send
responses. This module teaches you *how to design them well* — the REST conventions that make an
API predictable, consistent, and pleasant for any client (including your own
[React](../../frontend/react/) or [Next.js](../../frontend/nextjs/) frontend) to consume, instead
of an ad hoc collection of endpoints that each work slightly differently.

## Learning Objectives

- Explain REST's core principles: resource-based URLs, statelessness, and the uniform interface.
- Design resource-based routes correctly, including nested resources.
- Map HTTP methods to the correct CRUD operation, and understand idempotency.
- Choose the correct status code for a REST-specific outcome.
- Validate request input before it reaches business logic.
- Implement pagination, filtering, and sorting for collection endpoints.
- Version an API without breaking existing clients.

## Prerequisites

- [Express.js Fundamentals](../expressjs-fundamentals/) — this module designs the APIs built with
  the routing and middleware covered there.

## Files in This Module

| File | Covers |
|---|---|
| [rest-principles.md](rest-principles.md) | Resource-based URLs, statelessness, and the uniform interface |
| [resource-based-routing.md](resource-based-routing.md) | Naming routes around resources, not actions, including nested resources |
| [http-methods.md](http-methods.md) | GET/POST/PUT/PATCH/DELETE mapped to CRUD, and idempotency |
| [status-codes.md](status-codes.md) | REST-specific status code conventions for common API outcomes |
| [request-validation.md](request-validation.md) | Validating input with Zod (or express-validator) before it reaches business logic |
| [pagination-filtering-and-sorting.md](pagination-filtering-and-sorting.md) | Query-parameter conventions for large collection endpoints |
| [api-versioning.md](api-versioning.md) | Versioning strategies, and evolving an API without breaking existing clients |

## When to Deep-Dive vs. Skim

Deep-dive [resource-based-routing.md](resource-based-routing.md) — thinking in resources instead
of actions is the single mental-model shift that makes every other convention in this module (HTTP
methods, status codes, nesting) click into place naturally, rather than feeling like arbitrary
rules to memorize.

## Quick Knowledge Check

<details>
<summary>Should an endpoint to mark an order as shipped be POST /orders/42/ship or PATCH /orders/42?</summary>

Strictly, resource-based REST favors `PATCH /orders/42` (partially updating the order's status
field) — but `POST /orders/42/ship` (a resource-oriented "action" sub-route) is also a common,
pragmatic real-world pattern for state transitions that don't map cleanly to a plain field update.
Either can be defensible; what matters is applying the choice consistently across the whole API.
See [resource-based-routing.md](resource-based-routing.md).

</details>

<details>
<summary>Why should request validation happen before any business logic runs, not after?</summary>

Because business logic (checking permissions, querying a database) shouldn't have to defend
against malformed input at every single step — validating once, at the boundary, guarantees
everything downstream can trust the shape of the data it receives, and fails fast with a clear
`422` instead of an unpredictable error deeper in the code. See
[request-validation.md](request-validation.md).

</details>

## References

- MDN, [REST](https://developer.mozilla.org/en-US/docs/Glossary/REST)
- Zod, [Introduction](https://zod.dev/)

## Continue Your Learning Path

Continue to the [SQL Fundamentals module](../sql-fundamentals/) to give the APIs designed here a
real relational database to persist data in.
