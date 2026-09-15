# 🔢 API Versioning Strategy, in Practice

## Building Directly on Existing Coverage

[REST API Design's api-versioning.md](../rest-api-design/api-versioning.md) already covers the
mechanics: URL-path vs. header-based versioning, what counts as a breaking change, and graceful
deprecation. This file is about applying that strategy specifically to the documentation and
tooling covered throughout this module — a genuinely ongoing practice, not a one-time setup step.

## Versioning the OpenAPI Spec Itself

```yaml
# v1/openapi.yaml
info:
  title: Shop API
  version: 1.0.0
servers:
  - url: https://api.example.com/v1

# v2/openapi.yaml
info:
  title: Shop API
  version: 2.0.0
servers:
  - url: https://api.example.com/v2
```

When an API's `/v1/` and `/v2/` routes genuinely coexist (per
[REST's api-versioning.md](../rest-api-design/api-versioning.md)'s URL-path versioning), the
OpenAPI spec documenting them should exist as **separate versioned documents** too — each
describing exactly one version's actual routes and shapes, rather than one increasingly complex
spec trying to describe every version's differences at once.

## Versioning a Postman Collection

```
Shop API v1 (collection) — kept exactly as-is, for existing clients
Shop API v2 (collection) — the new version's requests
```

A shared [Postman collection](postman-collections.md) benefits from the same treatment: a
genuinely new API version gets its own collection (or a clearly-versioned folder within one),
rather than silently updating the existing collection's requests to point at new endpoints — which
would break anyone relying on the old collection to test the still-supported old version.

## Communicating Deprecation Through Documentation

```yaml
paths:
  /v1/products:
    get:
      deprecated: true
      description: >
        Deprecated — use /v2/products instead. This endpoint will be
        removed on 2027-01-01.
```

OpenAPI's `deprecated: true` flag lets Swagger UI visually mark an endpoint as deprecated directly
in the generated documentation — a concrete, visible implementation of
[REST's api-versioning.md](../rest-api-design/api-versioning.md)'s graceful deprecation practice,
seen directly by anyone browsing the docs, not just mentioned in a separate changelog someone might
never read.

## Documentation Versioning Is Part of the Real Contract

An API's versioning strategy isn't complete without its documentation and tooling versioned
alongside it — a `/v2/` API with only `/v1/`'s documentation still published is, in a practical
sense, still undocumented for anyone trying to use the new version correctly.

## Common Mistakes

- Maintaining only one OpenAPI spec that tries to describe multiple, genuinely different API
  versions at once, producing confusing, hard-to-follow documentation.
- Updating a shared Postman collection's existing requests in place when a new API version ships,
  breaking the collection for any team still relying on it to test the still-supported old version.
- Deprecating an endpoint in practice without ever reflecting that in the documentation, leaving
  new consumers with no visible signal to migrate away from it.

## ➡️ Next

Continue to [sdk-generation.md](sdk-generation.md) to see one more concrete thing a well-maintained,
versioned OpenAPI spec can produce automatically.
