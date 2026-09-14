# Error-Handling Architecture

## Beyond a Single Route's `try`/`catch`

[Express's error-handling.md](../expressjs-fundamentals/error-handling.md) covered the mechanics:
automatic sync-error catching, `next(err)`, and four-argument error-handling middleware. This file
is about applying those mechanics **consistently, architecturally**, across an entire real
application — not ad hoc, differently, in every individual route.

## Custom Error Classes — Giving Errors Real Meaning

```js
// errors/AppError.js
export class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
  }
}

export class NotFoundError extends AppError {
  constructor(message = "Resource not found") {
    super(message, 404);
  }
}

export class ConflictError extends AppError {
  constructor(message) {
    super(message, 409);
  }
}
```

Custom, named error classes (extending JavaScript's built-in `Error`) let a
[service](controllers-services-and-repositories.md) throw something meaningful
(`throw new NotFoundError("Product not found")`) instead of either a generic `Error` or manually
constructing an HTTP response — remember, the service layer shouldn't know about HTTP status codes
at all. Attaching `statusCode` directly onto the error object is what lets a **single**, central
error handler (covered next) translate any of these errors into the correct response automatically.

## One Central Error-Handling Middleware, Not Scattered Per-Route Logic

```js
// middleware/errorHandler.js
export function errorHandler(err, req, res, next) {
  const statusCode = err.statusCode || 500;
  const message = statusCode === 500 ? "Internal server error" : err.message;

  if (statusCode === 500) {
    console.error(err.stack); // log the FULL detail server-side...
  }

  res.status(statusCode).json({ error: message }); // ...but never leak it to the client
}
```

```js
// app.js — registered LAST, per error-handling.md
app.use(errorHandler);
```

Rather than each controller individually deciding how to format an error response (per
[error-handling.md](../expressjs-fundamentals/error-handling.md)'s coverage of four-argument
middleware), one centralized `errorHandler` runs for the entire application — every controller
simply calls `next(err)` for anything it doesn't explicitly handle itself, trusting this single
place to format the response consistently. This directly guarantees API consistency, echoing
[REST's rest-principles.md](../rest-api-design/rest-principles.md)'s "uniform interface" idea
applied specifically to error responses.

## Never Leak Internal Detail to the Client

Notice the deliberate distinction above: a genuine `500` (an unexpected, unhandled error) logs its
**full** detail server-side (the stack trace, useful for debugging) but sends the client only a
generic `"Internal server error"` message — never the raw error or stack trace itself, which could
expose internal implementation details, file paths, or even fragments of a database query to
anyone who triggers an error. A known, expected error (like a `404` from a custom `NotFoundError`)
is safe to send its actual message, since it was deliberately written to be client-facing.

## Async Errors: Avoiding Repeated `try`/`catch` Boilerplate

```js
// A small wrapper that catches a rejected promise and forwards it to next()
function asyncHandler(fn) {
  return (req, res, next) => fn(req, res, next).catch(next);
}
```

```js
router.post("/", asyncHandler(async (req, res) => {
  const order = await orderService.placeOrder(req.body.productId, req.body.quantity);
  res.status(201).json(order);
}));
```

Wrapping every async controller in a repeated `try`/`catch` block, per
[Express's error-handling.md](../expressjs-fundamentals/error-handling.md)'s older-Express pattern,
gets repetitive fast across many routes. A small `asyncHandler` utility, applied once per route,
automatically forwards any rejected promise to `next()` — removing the need to repeat the same
boilerplate in every single async controller.

## Common Mistakes

- Formatting error responses differently in different controllers, producing an API whose error
  shape is inconsistent from one endpoint to the next.
- Sending a raw error message or stack trace directly to the client for an unexpected `500` error,
  leaking internal implementation detail.
- Forgetting `asyncHandler` (or an equivalent) on an async route, letting a rejected promise go
  completely unhandled in an older Express version that doesn't catch it automatically.

## Next

Continue to [scalable-backend-structure.md](scalable-backend-structure.md) to see how every piece
covered in this module fits together into one real, production-shaped project structure.
