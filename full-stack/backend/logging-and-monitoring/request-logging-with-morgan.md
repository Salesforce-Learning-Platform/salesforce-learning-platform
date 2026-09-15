# 🌐 Request Logging with Morgan

## Automatically Logging Every Request

```js
import morgan from "morgan";
app.use(morgan("dev"));
```

**Morgan** is Express middleware — the same `(req, res, next)` pattern from
[middleware.md](../expressjs-fundamentals/middleware.md) — that automatically logs a line for
**every** incoming HTTP request, with no manual logging call needed in each individual route
handler. Registered early (per middleware ordering, from
[middleware.md](../expressjs-fundamentals/middleware.md)), it captures every request the
application receives, not just the ones a developer remembered to log manually.

## The Predefined Formats

```
dev:      GET /products 200 45.234 ms - 1024     (concise, color-coded by status)
tiny:     GET /products 200 1024 - 45.234 ms      (the absolute minimum)
short:    127.0.0.1 GET /products HTTP/1.1 200 1024 - 45.234 ms
combined: 127.0.0.1 - - [15/Jan/2026:10:23:45] "GET /products HTTP/1.1" 200 1024 "-" "Mozilla/5.0..."
```

| Format | Best fit |
|---|---|
| `dev` | Local development — concise, human-readable, color-coded by response status |
| `tiny` | The absolute minimum detail |
| `short` | A middle ground, including the requester's address |
| `combined` | Production — the detailed, standard Apache log format most log-aggregation tools expect |

## Choosing a Format Per Environment

```js
import morgan from "morgan";

const format = process.env.NODE_ENV === "production" ? "combined" : "dev";
app.use(morgan(format));
```

Directly applying
[environment-variables.md](../nodejs-core-concepts/environment-variables.md)'s configuration
pattern: using `dev`'s concise, readable output locally, while switching to `combined`'s more
complete, standardized format in production — where a log-aggregation system, not a human watching
a terminal, is the actual primary consumer of the output.

## Directing Morgan's Output Through Winston

```js
import morgan from "morgan";
import { logger } from "./logger.js"; // the Winston logger from the prior file

app.use(morgan("combined", {
  stream: { write: (message) => logger.info(message.trim()) },
}));
```

Morgan's `stream` option lets its output be redirected anywhere — here, straight into the
[Winston logger](structured-logging-with-winston-and-pino.md) already configured, so every request
log entry benefits from the same transports (console, file) and structured formatting as every
other log message in the application, rather than writing to `stdout` through a completely separate
mechanism.

## Common Mistakes

- Using `combined` format for local development, producing noisy, less readable output than `dev`
  provides for that specific use case.
- Registering `morgan` after routes that might already send a response, missing requests that never
  actually reach the middleware.
- Logging Morgan's output through a completely separate mechanism from the rest of the
  application's logs, fragmenting what should be one consistent, searchable log stream.

## ➡️ Next

Continue to
[combining-logging-with-error-handling.md](combining-logging-with-error-handling.md) to make sure
every real error is actually captured by this logging setup.
