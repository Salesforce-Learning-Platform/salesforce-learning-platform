# 🛠️ SDK Generation

## Turning a Spec Into Real, Usable Client Code

```
openapi-generator generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./generated-client
```

```ts
// Generated, typed client code — no hand-written fetch calls needed
import { ProductsApi } from "./generated-client";

const api = new ProductsApi();
const product = await api.getProduct({ id: 42 }); // fully typed
```

**OpenAPI Generator** (and similar tools) reads the same OpenAPI spec from
[documenting-apis-with-swagger.md](documenting-apis-with-swagger.md) and produces a real,
ready-to-use **client SDK** — supporting 50+ target languages — with typed methods for every
documented endpoint, automatic request construction, and response parsing already built in.

## What a Generated SDK Actually Saves

Without a generated SDK, a frontend team consuming this API would hand-write its own `fetch`
calls, manually matching URLs, request shapes, and response types against whatever the backend
documentation says — exactly the kind of manual, error-prone process
[REST API Design](../rest-api-design/) exists to make predictable, but still requiring real,
repeated effort per consumer. A generated SDK automates that translation entirely: the same spec
that documents an endpoint also produces the exact typed function a consumer calls to use it,
directly reducing the risk of a frontend team's hand-written request drifting out of sync with the
real API.

## Why This Requires an Accurate, Well-Maintained Spec

```
A spec missing a field, or describing an outdated response shape,
generates an SDK with that SAME mistake baked directly into it —
now shipped as "official" client code.
```

A generated SDK is only as accurate as the spec it's generated from — this is precisely why
[documenting-apis-with-swagger.md](documenting-apis-with-swagger.md)'s point about keeping the spec
genuinely in sync with the real API matters so much: an inaccurate spec doesn't just mislead a human
reading documentation, it actively generates *incorrect client code* that other teams then build
real applications on top of.

## When SDK Generation Is Actually Worth Setting Up

SDK generation earns its setup cost specifically when an API has **multiple, separate consumers** —
different frontend teams, external partners, or multiple internal services — each of which would
otherwise need to write and maintain its own hand-written client against the same API. For an API
with a single, tightly-coupled frontend already sharing a monorepo (or otherwise easily kept in
sync), the manual `fetch`-based approach used throughout the rest of this platform's frontend
content remains completely reasonable.

## Common Mistakes

- Generating an SDK from a spec that's known to be out of date, effectively shipping the same
  inaccuracy as "official," seemingly-trustworthy client code.
- Setting up SDK generation for an API with a single, simple, tightly-coupled consumer where the
  added tooling complexity isn't actually justified by real reuse.
- Manually editing a generated SDK's output directly instead of fixing the underlying spec — any
  regeneration overwrites those manual edits, since the generated code is meant to be a build
  artifact, not a hand-maintained file.

## Module Summary

Across this module: the **OpenAPI Specification** documents an API as a structured, machine-readable
artifact rather than a document that drifts out of sync, with **Swagger UI** turning it into
interactive, testable documentation (see
[documenting-apis-with-swagger.md](documenting-apis-with-swagger.md)); a shared **Postman
collection**, organized to mirror an API's real resource structure and using environment variables
for portability, functions as living, hands-on documentation for a whole team (see
[postman-collections.md](postman-collections.md)); **versioning** applies to the documentation and
tooling themselves, not just the API's routes, with deprecation communicated directly and visibly
in the docs (see [api-versioning-strategy.md](api-versioning-strategy.md)); and **SDK generation**
turns an accurate, well-maintained spec directly into real, typed client code for any consumer,
specifically earning its cost when an API has multiple genuinely separate consumers to serve.
