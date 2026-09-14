# REST Principles

## What REST Actually Means

**REST** (Representational State Transfer) is an architectural style for designing networked
APIs — a set of principles, not a specific technology or library. An API described as "RESTful"
is one that follows these principles closely, using plain HTTP as its underlying protocol rather
than a custom one.

## Principle 1: Resources, Not Actions

```
GOOD:  GET /users/123            (accessing the "user 123" resource)
POOR:  GET /getUser?id=123       (action-based — a remote procedure call in disguise)
```

REST organizes an API around **resources** (nouns — a user, an order, a product) rather than
**actions** (verbs — `getUser`, `createOrder`). The HTTP method itself (covered in
[http-methods.md](http-methods.md)) already expresses the action; the URL's job is only to
identify *which resource*.

## Principle 2: Statelessness

```
Every request must carry everything the server needs to understand it —
an auth token in a header, all necessary parameters — rather than relying
on the server having "remembered" something from a previous request.
```

A **stateless** API means the server doesn't retain any client-specific context between requests —
each request is handled entirely on its own information. This matters practically: a stateless
server can freely route any given request to any available server instance (critical for scaling
horizontally, a concept returned to in the upcoming
[Backend Architecture module](../backend-architecture/)), since no server needs to have
"remembered" anything about a specific client from an earlier request.

## Principle 3: The Uniform Interface

REST APIs commit to a small, consistent, predictable interface rather than inventing bespoke
conventions per endpoint:

- The same small set of HTTP methods (GET, POST, PUT, PATCH, DELETE) means the same thing on
  every resource, everywhere in the API.
- The same status codes mean the same thing everywhere (covered in
  [status-codes.md](status-codes.md)).
- Resources are identified consistently by URL, and manipulated through their representation (the
  JSON returned/sent), rather than through custom, resource-specific mechanisms.

This consistency is REST's real practical payoff: a developer who understands *one* well-designed
REST endpoint in an API can correctly predict how every other endpoint in that same API behaves,
without needing to read documentation for each one individually.

## "RESTful" in Practice vs. Strict REST

The original academic definition of REST (from Roy Fielding's dissertation) includes constraints
most real-world APIs don't fully implement (like HATEOAS — responses containing links to related
actions). In practice, "a RESTful API" colloquially means an HTTP API organized around resources,
using standard HTTP methods and status codes sensibly — which is the practical, achievable
standard this module teaches toward.

## Common Mistakes

- Designing action-based URLs (`/api/createUser`, `/api/getOrderById`) instead of resource-based
  ones — this is really a remote procedure call wearing an HTTP API's clothing, not REST.
- Storing client-specific session state in server memory between requests, violating
  statelessness and making horizontal scaling far harder later.
- Treating strict, academic REST as a hard requirement everywhere — most real production APIs are
  pragmatically "RESTful" without implementing every original constraint, and that's a completely
  reasonable, common choice.

## Next

Continue to [resource-based-routing.md](resource-based-routing.md) to apply the resource-based
principle concretely, including handling relationships between resources.
