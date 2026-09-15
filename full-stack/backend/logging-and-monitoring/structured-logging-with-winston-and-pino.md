# 🪵 Structured Logging with Winston and Pino

## Creating a Logger

```js
import winston from "winston";

const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" }),
  ],
});

logger.info("Server started on port 3000");
logger.warn("Deprecated endpoint called");
logger.error("Failed to connect to database");
```

**Winston** creates a `logger` object with dedicated methods per severity level (`.info()`,
`.warn()`, `.error()`) — directly clearer than passing a level as a plain string argument, per
[why-logging-matters.md](why-logging-matters.md)'s point about severity distinguishing messages at
a glance.

## Log Levels — Ordered by Severity

```
error (0)  →  warn (1)  →  info (2)  →  http (3)  →  verbose (4)  →  debug (5)  →  silly (6)
```

Winston's default levels are ordered numerically, most severe first. Setting `level: "info"` on a
logger means it captures `info` and everything *more* severe (`warn`, `error`) but suppresses
anything less severe (`debug`, `silly`) — a single setting that controls exactly how much detail a
given environment's logs actually capture, without needing to remove or comment out logging calls
throughout the codebase.

## Transports — Where Logs Actually Go

```js
transports: [
  new winston.transports.Console(),                                    // stdout, useful locally
  new winston.transports.File({ filename: "error.log", level: "error" }), // ONLY errors, to their own file
  new winston.transports.File({ filename: "combined.log" }),            // everything, to one file
]
```

A **transport** is a logging destination. Winston supports multiple transports simultaneously, each
optionally filtered to its own minimum level — here, `error.log` receives *only* `error`-level
messages, while `combined.log` receives everything. This is directly useful in practice: a team can
watch `error.log` specifically for anything requiring urgent attention, without it being buried
among routine informational messages.

## Structured (JSON) Output

```json
{"level":"error","message":"Failed to connect to database","timestamp":"2026-01-15T10:23:45.123Z"}
```

`winston.format.json()` outputs each log entry as a genuine JSON object, not just a formatted
string — directly the "structured output" benefit from
[why-logging-matters.md](why-logging-matters.md): a log-processing tool can parse and filter on
`level`, `timestamp`, or any custom field, rather than needing to pattern-match against
free-form text.

## Pino — a Faster Alternative With the Same Core Ideas

```js
import pino from "pino";
const logger = pino();

logger.info("Server started");
logger.error({ err }, "Failed to connect to database");
```

**Pino** follows the same fundamental model — leveled methods, structured JSON output by default —
while being specifically optimized for very high logging throughput, at the cost of a slightly less
feature-rich transport system than Winston's. Choosing between them is less about fundamentally
different capabilities and more about a specific project's raw logging volume and configuration
needs.

## Common Mistakes

- Setting a logger's level too permissively in production (e.g., `debug` or `silly`), producing an
  overwhelming volume of low-value log output that makes genuinely important messages harder to
  find.
- Logging sensitive data (a password, a full credit card number, a JWT secret) directly — logs are
  often stored and viewed by more people than the application's actual runtime data, making this a
  real security exposure.
- Choosing between Winston and Pino based on unfamiliarity rather than actual project needs — both
  solve the same core problem well; the real difference is throughput and configuration style.

## ➡️ Next

Continue to [request-logging-with-morgan.md](request-logging-with-morgan.md) to automatically log
every incoming HTTP request, not just messages your own code explicitly logs.
