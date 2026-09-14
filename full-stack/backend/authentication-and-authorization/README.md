# Authentication and Authorization

## Purpose

Every module so far has built APIs anyone could call. This module answers the two questions every
real backend eventually has to answer: **who is making this request** (authentication), and **what
are they allowed to do** (authorization) — securing the routes, resources, and data modeled
throughout the rest of this domain.

## Learning Objectives

- Explain the distinction between authentication and authorization precisely.
- Hash passwords correctly with bcrypt, and explain why a plain hash (MD5/SHA256) isn't enough.
- Explain session-based authentication, and its cookie security attributes.
- Implement JWT-based authentication, and explain what a JWT actually guarantees.
- Protect Express routes with authentication middleware.
- Implement role-based access control (RBAC) for authorization.

## Prerequisites

- [Express.js Fundamentals](../expressjs-fundamentals/) — this module builds authentication as
  Express middleware.
- [Database Design and Modeling](../database-design-and-modeling/) — a `users` table/collection is
  assumed throughout.

## Files in This Module

| File | Covers |
|---|---|
| [authentication-vs-authorization.md](authentication-vs-authorization.md) | The precise distinction, and why 401 vs. 403 depends on it |
| [password-hashing.md](password-hashing.md) | bcrypt, salt, and why plain or weakly-hashed passwords are a real vulnerability |
| [sessions.md](sessions.md) | Session-based authentication, and cookie security attributes (HttpOnly, Secure, SameSite) |
| [jwt.md](jwt.md) | JWT structure, signing/verification, and stateless authentication |
| [protecting-routes.md](protecting-routes.md) | Authentication middleware, protecting Express routes |
| [role-based-access-control.md](role-based-access-control.md) | RBAC, and authorization beyond "is this user logged in at all" |

## When to Deep-Dive vs. Skim

Deep-dive [jwt.md](jwt.md) — JWTs are the most widely used authentication mechanism in modern APIs,
and precisely understanding what a JWT's signature does and doesn't guarantee is essential to using
it safely.

## Quick Knowledge Check

<details>
<summary>A logged-in user tries to delete another user's order. Should the API respond with 401 or 403?</summary>

**403 Forbidden** — the user is authenticated (the server knows exactly who they are), but not
authorized to perform this specific action. `401` would be the correct response only if the user
weren't authenticated at all. See
[authentication-vs-authorization.md](authentication-vs-authorization.md).

</details>

<details>
<summary>Why is storing a password with plain SHA256 still considered insecure, even though it's a real cryptographic hash?</summary>

SHA256 is deliberately *fast* — exactly the wrong property for password hashing, since it lets an
attacker with a stolen password database try billions of guesses per second. bcrypt is
deliberately slow and tunable (via salt rounds) specifically to make that kind of brute-force
attack impractical. See [password-hashing.md](password-hashing.md).

</details>

## References

- JWT.io, [Introduction to JSON Web Tokens](https://jwt.io/introduction)
- bcrypt (node.bcrypt.js), [GitHub repository](https://github.com/kelektiv/node.bcrypt.js)
- MDN, [Using HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies)

## Continue Your Learning Path

Continue to the [Backend Architecture module](../backend-architecture/) to organize everything
built across this domain — routes, database access, and now authentication — into a genuinely
scalable project structure.
