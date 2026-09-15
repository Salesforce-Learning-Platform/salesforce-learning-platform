# 📝 Logging and Monitoring

## Purpose

Every module in this domain has used `console.log` at most for casual debugging. A real production
application needs genuine, structured logging — a durable record of what actually happened,
searchable and readable long after the moment it occurred, and distinct from the broader
infrastructure-level logging concepts (log aggregation, centralized log storage) covered separately
at the deployment/DevOps layer. This module covers logging specifically as a Node.js/Express
implementation concern: the actual libraries and patterns used inside application code.

## 🎯 Learning Objectives

- Explain why `console.log` isn't sufficient for production logging.
- Set up structured logging with Winston or Pino.
- Use Morgan to log HTTP requests automatically.
- Combine logging with Express's centralized error handling.

## 📋 Prerequisites

- [Error-Handling Architecture](../backend-architecture/error-handling-architecture.md) — this
  module pairs logging directly with the centralized error handler already covered there.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [why-logging-matters.md](why-logging-matters.md) | Why `console.log` isn't enough, and what real logging provides |
| [structured-logging-with-winston-and-pino.md](structured-logging-with-winston-and-pino.md) | Setting up a logger, log levels, and structured (JSON) output |
| [request-logging-with-morgan.md](request-logging-with-morgan.md) | Morgan's predefined formats, and choosing one per environment |
| [combining-logging-with-error-handling.md](combining-logging-with-error-handling.md) | Logging errors consistently through the centralized error handler |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive
[structured-logging-with-winston-and-pino.md](structured-logging-with-winston-and-pino.md) — the
shift from ad hoc `console.log` calls to genuinely structured, leveled logging is the single
biggest real-world upgrade this module teaches, and it's the foundation everything else in the
module builds on.

## ✅ Quick Knowledge Check

<details>
<summary>Is console.log("error occurred") an acceptable substitute for a real logging library in a production app?</summary>

No — it produces unstructured text with no severity level, no consistent format, and no way to
route different kinds of messages to different destinations. A real logging library (Winston,
Pino) provides levels, structured output, and configurable destinations that `console.log` alone
can't. See [why-logging-matters.md](why-logging-matters.md).

</details>

<details>
<summary>Should morgan's "combined" format be used in local development?</summary>

Not typically — "combined" is verbose, Apache-style output better suited to production log
aggregation; "dev" is the concise, color-coded format built specifically for a readable local
development experience. See [request-logging-with-morgan.md](request-logging-with-morgan.md).

</details>

## 📚 References

- Winston, [GitHub repository](https://github.com/winstonjs/winston)
- Morgan, [GitHub repository](https://github.com/expressjs/morgan)

## ➡️ Continue Your Learning Path

Continue to the [Production Authentication Architecture module](../production-authentication-architecture/)
to see logging applied to a real, security-sensitive part of the application.
