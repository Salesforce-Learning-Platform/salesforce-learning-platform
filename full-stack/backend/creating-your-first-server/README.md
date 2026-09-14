# Creating Your First Server

## Purpose

[Node.js Core Concepts](../nodejs-core-concepts/) covered Node's general-purpose building blocks.
This module uses one of them — the built-in `http` module — for the thing a backend actually
exists to do: **be a server**, listening for requests from a client (a browser, the
[Frontend domain's](../../frontend/README.md) own React/Next.js apps, or a tool like Postman) and
sending back responses.

## Learning Objectives

- Explain what a server actually is: a long-running process listening on a port for incoming
  connections.
- Create a working HTTP server using Node's built-in `http` module.
- Read incoming request data and send a properly-formed response.
- Implement basic routing — responding differently based on the request's method and URL.
- Choose the correct HTTP status code for a given response.

## Prerequisites

- [Node.js Core Concepts](../nodejs-core-concepts/) — this module builds directly on Node's
  built-in modules and the event loop.

## Files in This Module

| File | Covers |
|---|---|
| [creating-an-http-server.md](creating-an-http-server.md) | What a server is, and building one with Node's `http` module |
| [request-and-response.md](request-and-response.md) | Reading `req.method`/`req.url`/`req.headers`, and sending a response with `res.writeHead`/`res.end` |
| [routing-basics.md](routing-basics.md) | Responding differently based on method and URL, without a framework |
| [http-status-codes.md](http-status-codes.md) | The 1xx–5xx status code classes and when to use each specific code |

## When to Deep-Dive vs. Skim

Deep-dive [http-status-codes.md](http-status-codes.md) — choosing the *correct* status code for a
given situation is a skill that pays off on every single backend endpoint you'll ever write for the
rest of this domain, far beyond this one module.

## Quick Knowledge Check

<details>
<summary>A client sends a POST request to create a new user, and it succeeds. What status code should the response use — 200 or 201?</summary>

**201 Created** — it specifically signals that the request succeeded *and* a new resource was
created, which is more precise than the generic 200. See
[http-status-codes.md](http-status-codes.md).

</details>

<details>
<summary>Why does a raw Node http server need to check both req.method and req.url to route correctly?</summary>

Because a URL alone is ambiguous about intent — `GET /users` (list users) and `POST /users`
(create a user) share the same URL but mean completely different things. Routing on both together
is what makes each combination distinct. See [routing-basics.md](routing-basics.md).

</details>

## References

- Node.js, [HTTP](https://nodejs.org/api/http.html)
- MDN, [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)

## Continue Your Learning Path

Continue to the [Express.js Fundamentals module](../expressjs-fundamentals/) to see how a real
framework handles routing, request parsing, and response-sending far more conveniently than the
raw `http` module alone.
