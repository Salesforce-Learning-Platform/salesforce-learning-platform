# 📋 Documenting APIs with Swagger

## The OpenAPI Specification's Structure

```yaml
openapi: 3.0.0
info:
  title: Shop API
  description: An API for managing products and orders
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /products/{id}:
    get:
      summary: Get a single product by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: The requested product
        '404':
          description: Product not found
```

The **OpenAPI Specification** (what "Swagger" commonly refers to) describes a REST API as a
structured YAML or JSON document: `info` holds the API's name, description, and version; `servers`
lists where it's actually hosted; and `paths` documents every endpoint — its parameters, and its
possible responses (mapping directly onto
[REST's status-codes.md](../rest-api-design/status-codes.md)'s conventions for each outcome).

## Why a Spec, Not Just a Written Document

A hand-written document (a wiki page, a README) describing an API drifts out of sync with the real
API over time — nothing forces it to stay accurate as endpoints change. An OpenAPI **spec**, by
contrast, is a structured, machine-readable artifact that other tools can directly consume: it's
the same underlying document that drives Swagger UI's interactive documentation, and (per
[sdk-generation.md](sdk-generation.md)) can generate actual client code — giving a real, concrete
incentive to keep it accurate, since real tooling depends on it being correct.

## Swagger UI — Turning the Spec Into Interactive Docs

Swagger UI reads an OpenAPI spec and automatically renders **interactive** documentation — a real
web page listing every endpoint, its parameters, and its expected responses, where a developer can
fill in real values and send an actual test request directly from the documentation page itself,
without needing a separate tool like Postman just to try an endpoint out.

## Documenting a Request Body

```yaml
paths:
  /products:
    post:
      summary: Create a new product
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name: { type: string }
                price: { type: number }
              required: [name, price]
      responses:
        '201':
          description: Product created
        '422':
          description: Invalid input
```

A `requestBody` schema documents exactly what a `POST`/`PUT`/`PATCH` request should send — directly
describing the same shape a [Zod schema](../rest-api-design/request-validation.md) would validate
at runtime. Keeping these two genuinely in sync (the documented shape and the actual validation
schema) is a real discipline worth maintaining deliberately, since nothing automatically keeps them
identical.

## Common Mistakes

- Writing API documentation as a separate, hand-maintained document instead of a spec that real
  tooling (Swagger UI, SDK generation) actually consumes — it reliably drifts out of date.
- Documenting only the success case for an endpoint, omitting the error responses
  ([REST's status-codes.md](../rest-api-design/status-codes.md)) a real client also needs to handle.
- Letting the OpenAPI spec's request body schema silently diverge from the API's actual runtime
  validation schema, so the documentation describes something the API no longer actually enforces.

## ➡️ Next

Continue to [postman-collections.md](postman-collections.md) to build a shareable, hands-on way
for a team to actually exercise an API.
