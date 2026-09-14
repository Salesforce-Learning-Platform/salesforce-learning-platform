# Status Codes for REST APIs

## Building on the General Classes

[http-status-codes.md](../creating-your-first-server/http-status-codes.md) already covered what
each status code class (2xx, 4xx, 5xx) and common specific codes mean in general. This file is
about the **convention**: which specific code a well-designed REST endpoint should return for each
CRUD operation, so an API is predictable across every resource it exposes.

## The Conventional Pairing, by Operation

| Operation | Success Code | Common Failure Codes |
|---|---|---|
| `GET` (collection) | `200 OK` | `401`, `403` |
| `GET` (single item) | `200 OK` | `404 Not Found` |
| `POST` (create) | `201 Created` | `400`/`422` (invalid input), `409` (conflict) |
| `PUT`/`PATCH` (update) | `200 OK` | `404`, `422` |
| `DELETE` | `204 No Content` | `404` |

A REST API's clients quickly learn to trust these conventions — a `201` unambiguously signals
"something new now exists," letting a frontend confidently update its UI (e.g., adding the new item
to a list) without needing to double-check by re-fetching, purely from the status code alone.

## `201 Created` — Send the New Resource Back, and a `Location` Header

```js
app.post("/products", (req, res) => {
  const newProduct = createProduct(req.body);
  res
    .status(201)
    .location(`/products/${newProduct.id}`)
    .json(newProduct);
});
```

A `201` response conventionally includes the newly created resource's full representation in the
body — the client generally needs the server-generated `id` immediately — and, where practical, a
`Location` header pointing at the new resource's URL, letting a client fetch it again later without
needing to reconstruct the URL itself.

## `204 No Content` — For a Successful Delete (or Any Empty Success)

```js
app.delete("/products/:id", (req, res) => {
  deleteProduct(req.params.id);
  res.status(204).end(); // no body at all — 204 means there's genuinely nothing to send
});
```

A successful `DELETE` has nothing meaningful left to return — the resource is gone. `204` signals
success while explicitly having an empty body, which is more precise than sending a `200` with a
body containing something like `{ "success": true }`.

## `409 Conflict` — When the Request Is Valid, But Contradicts Current State

```js
app.post("/users", (req, res) => {
  if (userAlreadyExistsWithEmail(req.body.email)) {
    return res.status(409).json({ error: "A user with this email already exists" });
  }
  // ...
});
```

`409` is distinct from `422`: a `422` request is malformed or fails validation on its own terms
(missing a required field); a `409` request is perfectly well-formed but conflicts with the
server's *current state* (trying to create a user with an email that's already taken).

## Common Mistakes

- Returning `200 OK` for every successful response regardless of operation, rather than using the
  more precise `201` for creation and `204` for a delete — technically works, but loses information
  a well-designed client could otherwise rely on.
- Sending a `200` with an empty or placeholder body for a successful delete instead of a genuine
  `204 No Content`.
- Confusing `409 Conflict` (valid request, contradicts current state) with `422` (the request
  itself is invalid) — they represent genuinely different failure reasons a client should be able
  to distinguish.

## Next

Continue to [request-validation.md](request-validation.md) to see exactly how a `422` gets
triggered — validating a request's input before any business logic runs.
