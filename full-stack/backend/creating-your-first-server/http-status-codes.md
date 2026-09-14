# HTTP Status Codes

## Five Classes, by First Digit

| Class | Range | Meaning |
|---|---|---|
| **1xx** | 100–199 | Informational — the request was received, processing continues |
| **2xx** | 200–299 | Success — the request was handled correctly |
| **3xx** | 300–399 | Redirection — the client needs to go somewhere else |
| **4xx** | 400–499 | Client error — the request itself was wrong somehow |
| **5xx** | 500–599 | Server error — the server failed to handle a valid request |

A status code's *first digit alone* tells a client, at a glance, which broad category a response
falls into — even a client that doesn't recognize the exact specific code can still react sensibly
based on its class.

## The 2xx Codes You'll Use Constantly

```js
res.writeHead(200); // OK — a GET succeeded, here's the data
res.writeHead(201); // Created — a POST succeeded, a new resource now exists
res.writeHead(204); // No Content — succeeded, but there's genuinely nothing to send back
```

`200 OK` is the general-purpose success code. `201 Created` is more *specific*, and preferred over
plain `200` specifically for a request that successfully created a new resource (a new user, a new
product) — the distinction genuinely communicates something a generic `200` doesn't. `204 No
Content` fits a successful action with no meaningful response body to return, like a successful
`DELETE`.

## The 4xx Codes: The Client Did Something Wrong

```js
res.writeHead(400); // Bad Request — malformed input, e.g. broken JSON
res.writeHead(401); // Unauthorized — not authenticated at all
res.writeHead(403); // Forbidden — authenticated, but not allowed to do this
res.writeHead(404); // Not Found — this resource/route doesn't exist
res.writeHead(422); // Unprocessable Content — well-formed, but semantically invalid
```

`401` vs. `403` is a common point of confusion: **401** means "I don't know who you are" (no valid
credentials at all — log in first), while **403** means "I know who you are, and you're still not
allowed to do this" (a real permissions problem, not a missing-login problem). `422` is distinct
from `400`: a `400` request is malformed at the syntax level (invalid JSON); a `422` request is
syntactically fine JSON but fails validation (a required field is missing, an email isn't actually
a valid email).

## The 5xx Codes: The Server Did Something Wrong

```js
res.writeHead(500); // Internal Server Error — something broke on the server's side
```

A `5xx` code is a direct admission that a genuinely *valid* request from the client still couldn't
be handled correctly, because of a problem on the server's own side — an unhandled exception, a
database connection failure. This is a meaningfully different signal than any `4xx` code: `4xx`
tells the client "fix your request"; `5xx` tells the client "your request was fine, we failed."

## Choosing the Right Code Is Part of the API's Contract

A well-designed API's status codes let a client program its error-handling logic *generically*,
without needing to parse a human-readable error message to figure out what actually happened — a
client can reliably branch on "was this a 401 (prompt a login) or a 404 (show a not-found page) or
a 500 (show a generic retry message)" purely from the status code itself.

## Common Mistakes

- Returning `200 OK` for every response regardless of what actually happened, forcing clients to
  parse the response body just to determine whether something actually succeeded.
- Confusing `401` and `403` — returning `401` when a logged-in user simply lacks permission for an
  action (that's `403`), or vice versa.
- Using a generic `400` for every validation failure instead of the more precise `422` where a
  request is well-formed but fails business-logic validation.

## Module Summary

Across this module: a **server** is a long-running process listening on a port, built here with
Node's `http.createServer()` (see [creating-an-http-server.md](creating-an-http-server.md));
`req`/`res` carry the incoming request's method, URL, headers, and streamed body, and the outgoing
response's status, headers, and body (see
[request-and-response.md](request-and-response.md)); **routing** without a framework means manually
comparing `req.method` and `req.url`, which works but scales poorly as an API grows (see
[routing-basics.md](routing-basics.md)); and choosing the precise **HTTP status code** — the right
2xx, 4xx, or 5xx for a given outcome — is part of an API's actual contract with its clients, not a
cosmetic detail.
