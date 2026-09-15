# 🔌 Designing REST APIs at a System Level

## From a Single API to a System's Contract

[REST API Design](../../../backend/rest-api-design/), already covered in this repository's Backend
domain, established how to design *one* well-structured API. At the HLD level, this same discipline
extends to designing the *contract* between multiple, independent services — with genuinely new
concerns that only emerge at real system scale.

## Versioning: APIs Change, Consumers Can't All Update at Once

```
GET /v1/orders/42
GET /v2/orders/42   # a NEW version, with a genuinely different
                      # response shape
```

At HLD scale, an API is rarely consumed by only one, easily-updated client — multiple internal
services, external partners, and mobile apps still running older versions may all depend on the
*same* endpoint simultaneously. Explicit versioning lets an API evolve without breaking every
existing consumer the moment a change ships.

## Idempotency: Genuinely Critical for Distributed, Retry-Prone Systems

```
POST /orders   { "idempotency_key": "abc-123", "item": "widget" }
```

```
If a NETWORK failure causes a client to genuinely not know
whether its request SUCCEEDED, the SAFE behavior is to RETRY -
an idempotency key ensures that RETRYING the exact SAME request
doesn't create a SECOND, duplicate order.
```

This matters far more at HLD scale than for a single, reliable, local API call — a distributed
system's network calls (per
[networking-basics-for-system-design.md](networking-basics-for-system-design.md)) can genuinely
fail or time out in ambiguous ways, making idempotent retries a real, practical necessity rather
than a theoretical nicety.

## Pagination: Genuinely Large Result Sets

```
GET /orders?cursor=eyJpZCI6NDJ9&limit=50
```

At real system scale, a query that might return millions of rows can never be returned in a single
response — cursor-based pagination (rather than simple page-number pagination, which degrades
poorly at genuinely large offsets) is the standard, scale-appropriate approach.

## Rate Limiting at the API Boundary

```
A PUBLIC-facing API needs explicit rate limits to protect the
ENTIRE system behind it from being overwhelmed by a single,
misbehaving (or malicious) client - directly previewing Rate
Limiting, covered in full in Advanced Distributed Systems
Concepts, later in this domain.
```

This is a genuinely important system-level concern beyond a single API's own internal logic — a
well-designed API contract includes an explicit, documented rate limit precisely because, at real
scale, a single client's runaway traffic can genuinely degrade service for every other client.

## Synchronous vs. Asynchronous APIs

```
SYNCHRONOUS: the client WAITS for the full response - simple, but
  the client is BLOCKED for however long processing takes

ASYNCHRONOUS: the API immediately returns an ACKNOWLEDGMENT (e.g.
  202 Accepted with a status URL) - the client polls, or is
  notified, once the ACTUAL work completes
```

For genuinely long-running operations (video processing, a large data export), an asynchronous API
shape is often the correct choice at scale — directly previewing the message-queue-based
asynchronous communication covered in the Core Infrastructure module, later in this domain.

## Common Mistakes

- Designing a public API with no versioning strategy, making any future breaking change genuinely
  disruptive to every existing consumer at once.
- Omitting idempotency support on state-changing endpoints, making safe client-side retries
  genuinely impossible without risking duplicate operations.
- Using simple offset-based pagination for a genuinely large dataset, which degrades in performance
  as the offset grows.

## ➡️ Next

Continue to [sql-vs-nosql-at-scale.md](sql-vs-nosql-at-scale.md) to see how the data these APIs
actually serve gets stored at scale.
