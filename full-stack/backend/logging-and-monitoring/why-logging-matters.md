# ❓ Why Logging Matters

## The Problem With `console.log` in Production

```js
console.log("user logged in");
console.log("error:", err);
```

`console.log` works fine for casual, local debugging — but it has real, practical limits in
production: every message is treated identically (no way to distinguish a routine info message
from a genuine error at a glance), output isn't structured (searching or filtering thousands of
lines of plain text is genuinely painful), and there's no built-in way to route different messages
to different destinations (a file, a monitoring service, the console) based on their severity.

## What Real Logging Actually Provides

- **Severity levels** — distinguishing a routine informational message from a warning from a
  genuine error, so a team can filter for what actually matters.
- **Structured output** — logging as data (commonly JSON) rather than a plain string, making logs
  genuinely searchable and machine-parseable, not just human-readable.
- **Configurable destinations** — sending different severities to different places (errors to one
  file, everything to another, or to an external monitoring service) without changing the actual
  logging calls scattered throughout the application code.

## A Real, Concrete Example of Why This Matters

```
Without leveled logging: 50,000 lines of undifferentiated console
output, no way to quickly find just the errors from a specific
incident.

With leveled logging: filter to only "error" level, from a specific
time window, in seconds.
```

When something genuinely goes wrong in production — an unexpected error, a spike in failed
requests — the actual investigation depends entirely on being able to find the relevant log entries
quickly. Plain `console.log` output, with no levels and no structure, makes that investigation
dramatically harder than it needs to be.

## Where This Module Fits vs. Infrastructure-Level Logging

This module covers logging specifically as **application code** — the libraries and patterns used
directly inside an Express app (covered starting in
[structured-logging-with-winston-and-pino.md](structured-logging-with-winston-and-pino.md)). The
broader infrastructure concern of **centralizing** logs from many running server instances into one
searchable system is a genuinely separate, deployment-level topic — this module produces the
well-structured log output that a centralized logging system would later collect and aggregate.

## Common Mistakes

- Relying entirely on `console.log` for a real production application, losing severity levels,
  structure, and configurable destinations.
- Logging so much routine, low-value information that genuinely important messages get buried in
  noise — logging deliberately, not exhaustively, matters just as much as logging at all.
- Assuming logging is purely an infrastructure/DevOps concern with nothing to do with application
  code — the quality of what's actually logged is set entirely by the application itself.

## ➡️ Next

Continue to
[structured-logging-with-winston-and-pino.md](structured-logging-with-winston-and-pino.md) to set
up real, leveled logging in an Express application.
