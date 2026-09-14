# Express.js Fundamentals

## Purpose

[Creating Your First Server](../creating-your-first-server/) built routing, request-reading, and
response-sending entirely by hand with Node's raw `http` module — and ended by noting exactly how
that approach stops scaling. This module introduces **Express.js**, the framework that solves that
problem: the most widely used Node.js web framework, providing declarative routing, built-in
request parsing, and a composable middleware system on top of the same underlying `http` module.

## Learning Objectives

- Explain what Express adds on top of Node's raw `http` module, and why it's worth the dependency.
- Define routes for different HTTP methods, including dynamic route and query parameters.
- Explain middleware: the `(req, res, next)` signature, and how a request flows through a stack of
  middleware functions.
- Use Express's built-in middleware (`express.json()`, `express.static()`) and recognize when a
  third-party middleware package is the right tool.
- Handle errors correctly in both synchronous and asynchronous Express route handlers.

## Prerequisites

- [Creating Your First Server](../creating-your-first-server/) — this module directly compares
  Express against the manual routing approach covered there.

## Files in This Module

| File | Covers |
|---|---|
| [introduction-to-express.md](introduction-to-express.md) | What Express is, and what it adds on top of the raw `http` module |
| [creating-an-express-server.md](creating-an-express-server.md) | Setting up an Express app, and its first route |
| [routing.md](routing.md) | `app.get`/`post`/`put`/`delete`, route parameters, query strings, and `express.Router` |
| [middleware.md](middleware.md) | The `(req, res, next)` signature, middleware order, and built-in vs. third-party middleware |
| [request-response-objects.md](request-response-objects.md) | What Express adds to `req`/`res` beyond Node's raw versions |
| [error-handling.md](error-handling.md) | Automatic sync error catching, `next(err)` for async code, and custom error-handling middleware |

## When to Deep-Dive vs. Skim

Deep-dive [middleware.md](middleware.md) — middleware is the single architectural idea that
everything else in Express (routing, body parsing, error handling, and eventually authentication
and validation in later modules) is actually built on top of.

## Quick Knowledge Check

<details>
<summary>What does calling next() inside a middleware function actually do?</summary>

It passes control forward to the next middleware function (or route handler) in the stack. If a
middleware function doesn't call `next()` and doesn't itself send a response, the request hangs
indefinitely — nothing else in the stack ever runs. See [middleware.md](middleware.md).

</details>

<details>
<summary>Does Express automatically catch an error thrown inside an async route handler?</summary>

In modern Express (v5+), yes — an `async` function that throws or has its returned promise reject
automatically has that error passed to Express's error handling, the same as a synchronous throw.
Older versions require manually catching the error and calling `next(err)`. See
[error-handling.md](error-handling.md).

</details>

## References

- Express, [Hello world example](https://expressjs.com/en/starter/hello-world.html)
- Express, [Routing](https://expressjs.com/en/guide/routing.html)
- Express, [Using middleware](https://expressjs.com/en/guide/using-middleware.html)
- Express, [Error handling](https://expressjs.com/en/guide/error-handling.html)

## Continue Your Learning Path

Continue to the [REST API Design module](../rest-api-design/) to apply Express's routing and
middleware toward building a properly designed, consistent API.
