# 🔗 Combining Logging with Error Handling

## Logging Inside the Centralized Error Handler

```js
// middleware/errorHandler.js
import { logger } from "../logger.js";

export function errorHandler(err, req, res, next) {
  const statusCode = err.statusCode || 500;

  if (statusCode === 500) {
    logger.error({
      message: err.message,
      stack: err.stack,
      path: req.path,
      method: req.method,
    });
  }

  const message = statusCode === 500 ? "Internal server error" : err.message;
  res.status(statusCode).json({ error: message });
}
```

[Error-handling-architecture.md](../backend-architecture/error-handling-architecture.md) already
established one **centralized** error handler as the single place every unhandled error passes
through. That same central location is exactly where logging belongs too — logging the full error
detail (message, stack trace, the request path and method that triggered it) in **one place**,
rather than scattering `logger.error()` calls throughout individual route handlers.

## Why Centralizing Both Together Matters

Recall [error-handling-architecture.md](../backend-architecture/error-handling-architecture.md)'s
point about never leaking a raw error message or stack trace to the client — logging the full
detail server-side, while sending the client only a safe, generic message, is exactly what pairing
logging with the centralized error handler accomplishes in one place: the client-facing response
and the internal, detailed log entry are produced together, consistently, for every single error
the application ever encounters.

## Logging Expected vs. Unexpected Errors Differently

```js
if (statusCode >= 500) {
  logger.error({ message: err.message, stack: err.stack }); // genuinely unexpected — needs investigation
} else {
  logger.info({ message: err.message, statusCode }); // an expected 4xx — routine, not urgent
}
```

Not every error deserves the same log severity: a genuine `500` (an unhandled, unexpected failure)
warrants `error`-level logging that should draw real attention; a routine `404` or `422` (a user
requesting a resource that doesn't exist, or submitting invalid input) is expected, normal traffic
that doesn't need the same urgency — logging it at `info` level keeps `error`-level logs
meaningfully reserved for things that actually need investigation.

## A Complete, Realistic Setup

```js
import express from "express";
import morgan from "morgan";
import { logger } from "./logger.js";
import { errorHandler } from "./middleware/errorHandler.js";
import ordersRouter from "./routes/orders.js";

const app = express();

app.use(express.json());
app.use(morgan("combined", { stream: { write: (msg) => logger.info(msg.trim()) } }));
app.use("/orders", ordersRouter);
app.use(errorHandler); // always last, logs any real errors before responding
```

This combines every piece from this module and from
[scalable-backend-structure.md](../backend-architecture/scalable-backend-structure.md): request
logging via Morgan piped through Winston, application routes, and a centralized error handler that
logs genuine failures with full detail while still returning a safe response to the client.

## Common Mistakes

- Scattering `logger.error()` calls throughout individual route handlers instead of relying on the
  one centralized error handler, producing inconsistent logging coverage across the application.
- Logging every error at the same severity regardless of whether it's a genuine, unexpected `500`
  or a routine, expected `4xx`, burying real problems among normal traffic.
- Logging the full error detail (stack trace, internal message) and *also* sending that same detail
  directly to the client — the whole point of centralizing both together is keeping those two
  outputs correctly separated.

## Module Summary

Across this module: **`console.log` alone is insufficient** for production logging, lacking
severity levels, structure, and configurable destinations (see
[why-logging-matters.md](why-logging-matters.md)); **Winston** (or **Pino**) provides leveled,
structured (JSON) logging with configurable transports, letting different severities route to
different destinations (see
[structured-logging-with-winston-and-pino.md](structured-logging-with-winston-and-pino.md));
**Morgan** automatically logs every HTTP request, with formats chosen per environment and piped
through the same logger as the rest of the application (see
[request-logging-with-morgan.md](request-logging-with-morgan.md)); and pairing logging with the
**centralized error handler** ensures every genuine error is logged with full detail exactly once,
while the client only ever receives a safe, appropriately-generic response.
