# Routing Basics

## Why a URL Alone Isn't Enough

```
GET  /products    →  list every product
POST /products    →  create a new product
```

Two requests can share the exact same URL (`/products`) and mean something entirely different,
depending on the HTTP **method** used. **Routing** is the logic that decides which handler code
should run for a given request — and doing it correctly means checking both `req.method` and
`req.url` together, never just one alone.

## Manual Routing With the Raw `http` Module

```js
import { createServer } from "node:http";

const server = createServer((req, res) => {
  if (req.method === "GET" && req.url === "/products") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify([{ id: 1, name: "Keyboard" }]));
  } else if (req.method === "POST" && req.url === "/products") {
    res.writeHead(201, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ id: 2, name: "New Product" }));
  } else {
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Not Found" }));
  }
});
```

With only the built-in `http` module, routing is just a chain of conditionals comparing `req.method`
and `req.url` against every combination the server needs to support, falling through to a `404`
response (per [http-status-codes.md](http-status-codes.md)) for anything unmatched.

## Handling Dynamic Segments Manually

```js
if (req.method === "GET" && req.url.startsWith("/products/")) {
  const id = req.url.split("/products/")[1]; // e.g. "42"
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ id, name: "Keyboard" }));
}
```

A route like `/products/42` (fetching one specific product by its ID) doesn't match a fixed
string — it needs to be parsed out of the URL manually, here with a simple `startsWith` check
and a string split. This works, but it's clearly getting unwieldy fast: every new dynamic route
multiplies the manual parsing logic needed.

## Why This Doesn't Scale

Manually chaining `if`/`else` conditionals, comparing raw URL strings, and hand-parsing dynamic
segments works for a handful of routes but becomes genuinely hard to maintain as a real API grows
to dozens or hundreds of endpoints — every new route means more nested conditionals, every dynamic
segment means more manual string parsing, and there's no shared, reusable way to run common logic
(like checking whether a user is logged in) across multiple routes.

This exact pain point is precisely what a web framework exists to solve —
[Express.js Fundamentals](../expressjs-fundamentals/) covers `app.get()`, `app.post()`, and
automatic URL-parameter parsing that replace all of this manual conditional logic with a much more
maintainable, declarative style.

## Common Mistakes

- Checking only `req.url` without also checking `req.method`, silently treating a `GET /products`
  and a `POST /products` request identically.
- Using exact string equality (`req.url === "/products/42"`) for what's actually meant to be a
  dynamic route, instead of recognizing the pattern and parsing it — this only works for that one
  specific ID and breaks for every other one.
- Not having a final, catch-all `else` branch — leaving the server with no defined response at all
  for a URL nothing else matches, rather than a deliberate `404`.

## Next

Continue to [http-status-codes.md](http-status-codes.md) to choose the correct status code for
every response a server like this one sends.
