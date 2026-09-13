# HTTP Methods in Depth

## The Methods

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) defines HTTP's methods (also called "verbs").
The ones that matter for building web applications:

| Method | Intent | Typical use |
|---|---|---|
| `GET` | Retrieve a resource | Loading a page, fetching a record |
| `POST` | Submit data, often creating something | Creating a new record, submitting a form |
| `PUT` | Replace a resource entirely | Overwriting a record with a full new representation |
| `PATCH` | Partially update a resource | Updating just one or two fields of a record |
| `DELETE` | Remove a resource | Deleting a record |
| `HEAD` | Like `GET`, but response has no body | Checking whether a resource exists or has changed, without downloading it |
| `OPTIONS` | Ask what methods/headers are allowed | Used automatically by browsers for CORS preflight checks |

## Safe and Idempotent — Precise Definitions

These two properties are frequently used loosely, but they have exact meanings that matter for
correct API design and for reasoning about what's safe to retry.

- **Safe**: the method should not change server state at all. `GET`, `HEAD`, and `OPTIONS` are
  safe — a client (or an intermediary like a cache or a search-engine crawler) should be able to
  make these requests without causing any side effect.
- **Idempotent**: making the same request multiple times has the same effect as making it once.
  `GET`, `HEAD`, `PUT`, `DELETE`, and `OPTIONS` are idempotent. `POST` is generally **not**
  idempotent (submitting the same "create a comment" request twice typically creates two
  comments). `PATCH` is not guaranteed idempotent by the specification, though many APIs implement
  it idempotently in practice.

| Method | Safe | Idempotent |
|---|---|---|
| `GET` | Yes | Yes |
| `HEAD` | Yes | Yes |
| `OPTIONS` | Yes | Yes |
| `PUT` | No | Yes |
| `DELETE` | No | Yes |
| `POST` | No | No |
| `PATCH` | No | Not guaranteed |

## Why This Distinction Is Practically Important

Idempotency is exactly what makes it safe for a browser, a proxy, or a retry mechanism to
automatically resend a request after a network failure without asking the user. If a `PUT` request
to update a record times out, retrying it is safe — sending the same full replacement again
produces the same end state. Automatically retrying a `POST` that might have already succeeded on
the server (but whose response was lost) risks creating a duplicate — which is why "resubmitting a
form" typically needs a confirmation, while reloading a `GET`-driven page does not.

## PUT vs. PATCH — A Common Point of Confusion

Both update an existing resource, but differently:

- `PUT` conceptually replaces the *entire* resource with what's sent — any field not included is
  implicitly considered absent/reset in a strict interpretation.
- `PATCH` sends only the fields that changed, leaving everything else untouched.

A request that updates just a user's email address is a natural fit for `PATCH`; a request that
sends a complete, fully-formed replacement object is a natural fit for `PUT`. Many real-world APIs
are pragmatic about this distinction, but understanding the intended semantics helps you design
(and consume) APIs predictably.

## Common Mistakes

- Using `GET` for an operation that changes server state (e.g., a "delete" link that triggers a
  `GET` request) — this breaks the safety guarantee and can cause accidental deletions from link
  prefetching, crawlers, or browser history navigation.
- Assuming `POST` is idempotent and safe to blindly retry without deduplication logic.
- Using `PUT` when only a partial update was intended, potentially wiping fields the client didn't
  mean to touch.

## Next

Continue to
[http-status-codes-in-depth.md](http-status-codes-in-depth.md) to see how a server communicates
the outcome of a request.
