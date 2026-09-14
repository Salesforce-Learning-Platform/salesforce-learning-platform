# Error Handling in Express

## Synchronous Errors Are Caught Automatically

```js
app.get("/products/:id", (req, res) => {
  const product = findProductOrThrow(req.params.id); // throws if not found
  res.json(product); // never reached if the line above threw
});
```

If a route handler throws an error **synchronously**, Express automatically catches it and routes
it to its error-handling logic — no manual `try`/`catch` needed for this specific case. This is a
meaningful convenience over the raw `http` module, where an uncaught synchronous error would crash
the entire process (per
[process-and-runtime.md](../nodejs-core-concepts/process-and-runtime.md)'s coverage of
`uncaughtException`).

## Async Errors Need `next(err)` — or Just Work, Depending on Version

```js
// Modern Express (v5+): an async handler's rejected promise is
// automatically caught — no manual try/catch or next(err) needed
app.get("/products/:id", async (req, res) => {
  const product = await db.findProduct(req.params.id); // if this rejects,
  res.json(product);                                    // Express catches it
});

// Older Express (v4): must catch and forward the error explicitly
app.get("/products/:id", async (req, res, next) => {
  try {
    const product = await db.findProduct(req.params.id);
    res.json(product);
  } catch (err) {
    next(err); // manually pass the error along
  }
});
```

Async code is different from synchronous code: a rejected promise doesn't "throw" in the same
way a synchronous statement does, so older versions of Express can't catch it automatically —
`next(err)` is the explicit mechanism for handing an error to Express's error-handling logic from
inside an async or callback-based handler.

## Custom Error-Handling Middleware — Four Arguments, Always

```js
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({ error: err.message || "Something went wrong" });
});
```

An error-handling middleware function is identified purely by its **arity** — it takes exactly
**four** parameters (`err, req, res, next`), instead of the usual three. Express recognizes this
signature specifically and routes errors to it rather than treating it as regular middleware. It
must be registered **last**, after every other route and middleware, since Express only reaches it
once something upstream has passed an error along.

## The Default Error Handler

If no custom error-handling middleware is registered at all, Express falls back to its own
built-in default: it sets the response status from `err.status`/`err.statusCode` (or `500` if
neither is set, per
[http-status-codes.md](../creating-your-first-server/http-status-codes.md)'s coverage of `5xx`
codes) and sends back either the error's stack trace (in development) or a generic message (in
production). A real application almost always wants its own custom handler instead, to control
exactly what an API client receives.

## Common Mistakes

- Assuming Express automatically catches errors from callback-based async code (like a raw
  callback passed to a database driver) — only synchronous throws and (in modern Express) rejected
  promises are caught automatically; a callback-style error still needs an explicit `next(err)`.
- Registering error-handling middleware *before* the routes it's meant to catch errors from —
  Express processes middleware in registration order, so it needs to come last.
- Writing an error handler with only three parameters (forgetting `next`, even if it's genuinely
  unused) — Express won't recognize it as error-handling middleware at all without exactly four.
- Leaking a raw internal error message (or a full stack trace) directly to an API client in
  production — a custom error handler should generally send a safe, generic message externally
  while still logging the full detail server-side.

## Module Summary

Across this module: **Express** is a minimal framework built directly on Node's `http` module,
replacing manual routing, parsing, and response-writing with declarative conveniences (see
[introduction-to-express.md](introduction-to-express.md) and
[creating-an-express-server.md](creating-an-express-server.md)); **routing** methods per HTTP verb,
route parameters (`req.params`), and query strings (`req.query`) replace manual URL comparison and
parsing entirely (see [routing.md](routing.md)); **middleware** — functions with a `(req, res,
next)` signature, run in registration order — is the underlying mechanism powering routing itself,
body parsing, and everything else Express does (see [middleware.md](middleware.md)); Express's
enhanced `req`/`res` objects add `req.body`/`req.params`/`req.query` and convenience methods like
`res.json()`/`res.status()` on top of Node's raw versions (see
[request-response-objects.md](request-response-objects.md)); and **error handling** — automatic for
synchronous throws, explicit via `next(err)` for older-style async code, and customizable through
four-argument error-handling middleware registered last — determines what a client actually sees
when something goes wrong.
