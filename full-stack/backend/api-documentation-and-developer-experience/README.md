# 📖 API Documentation and Developer Experience

## Purpose

Every API built throughout this domain has been correct, but undocumented — a future consumer
(another team, a frontend developer, your own future self) has no way to know what it does without
reading the source code directly. This module covers making an API genuinely usable by someone who
has never seen its code: real documentation, shareable test collections, and a real versioning
strategy for change over time.

## 🎯 Learning Objectives

- Document a REST API with the OpenAPI Specification (Swagger).
- Build and share a Postman collection for a real API.
- Apply a deliberate API versioning strategy, building on REST API Design's coverage.
- Explain what SDK generation from an OpenAPI spec actually provides.

## 📋 Prerequisites

- [REST API Design](../rest-api-design/) — specifically
  [api-versioning.md](../rest-api-design/api-versioning.md), since this module builds directly on
  that coverage rather than repeating it.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [documenting-apis-with-swagger.md](documenting-apis-with-swagger.md) | The OpenAPI Specification's structure, and generating interactive docs with Swagger UI |
| [postman-collections.md](postman-collections.md) | Building, organizing, and sharing a Postman collection |
| [api-versioning-strategy.md](api-versioning-strategy.md) | Applying REST API Design's versioning coverage as an ongoing, real practice |
| [sdk-generation.md](sdk-generation.md) | Generating a client library directly from an OpenAPI spec |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [documenting-apis-with-swagger.md](documenting-apis-with-swagger.md) — a well-structured
OpenAPI spec is the single artifact this entire module builds on: Swagger UI, SDK generation, and
even a well-organized Postman collection can all be derived from it, directly or indirectly.

## ✅ Quick Knowledge Check

<details>
<summary>Is API documentation something to write once a project is finished, or an ongoing practice?</summary>

An ongoing practice — an API's documentation needs to change exactly when the API itself changes,
which is precisely why generating it directly from a spec (OpenAPI) that also drives real tooling
(Swagger UI, SDKs) is more reliable than a separately hand-maintained document that quietly drifts
out of date. See [documenting-apis-with-swagger.md](documenting-apis-with-swagger.md).

</details>

<details>
<summary>Can an OpenAPI spec do more than just produce human-readable documentation?</summary>

Yes — the same spec can drive Swagger UI's interactive documentation, generate client SDKs in
multiple languages, and even power a mock server for a frontend team to develop against before the
real API is finished. See [sdk-generation.md](sdk-generation.md).

</details>

## 📚 References

- Swagger, [OpenAPI Basic Structure](https://swagger.io/docs/specification/v3_0/basic-structure/)
- Postman, [Using Collections](https://learning.postman.com/docs/collections/using-collections/)

## ➡️ Continue Your Learning Path

Continue to the [Logging and Monitoring module](../logging-and-monitoring/) to observe how a
documented, real API actually behaves once other teams start depending on it.
