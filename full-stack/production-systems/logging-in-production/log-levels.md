# 🎚️ Log Levels

## Not Every Log Entry Is Equally Important

A production application generates a genuinely large volume of log entries — most log levels exist
specifically to let that volume be filtered by *severity*, so a team can distinguish "routine,
expected activity" from "something is actively broken" without wading through everything at once.

## The Standard Levels, From Least to Most Severe

```
DEBUG → detailed, low-level information useful ONLY during active
        development or troubleshooting - typically DISABLED in
        production

INFO  → normal, expected application activity - "server started,"
        "user logged in," "order processed successfully"

WARN  → something UNUSUAL happened, but the application recovered
        or handled it - "retrying a failed request," "using a
        fallback value"

ERROR → something GENUINELY failed - a request couldn't be
        completed, an operation didn't succeed

FATAL → the application ITSELF cannot continue running - typically
        precedes an immediate crash or shutdown
```

This is the standard hierarchy used by
[Winston and Pino](../../backend/logging-and-monitoring/structured-logging-with-winston-and-pino.md),
already covered at the application-code level earlier in this repository's Backend domain — this
module covers the same level hierarchy from the production-operations perspective: how these levels
actually get *used* once an application is running in real production.

## Setting the Right Level Per Environment

```
DEVELOPMENT: log level set to DEBUG - see EVERYTHING, for active
  troubleshooting

PRODUCTION: log level set to INFO (or WARN) - DEBUG-level noise
  is filtered out entirely, keeping logs focused on what actually
  matters at real production scale
```

This is a direct, practical application of
[environment-management.md](../devops-foundations/environment-management.md)'s "configuration, not
code, differs across environments" principle from earlier in this domain — the *same* logging
code runs everywhere; only the configured minimum log level actually differs.

## Why Logging Everything at DEBUG in Production Is a Real Problem

```
DEBUG-level logging, left enabled in production:
  - generates a MASSIVE volume of low-value log data
  - makes searching for the genuinely important ERROR/WARN
    entries meaningfully harder
  - can meaningfully increase logging infrastructure COST (storage,
    ingestion) for very little real benefit
```

This is a genuinely common, costly mistake — DEBUG logging is deliberately verbose *by design*,
which is exactly right for active local troubleshooting and exactly wrong for continuous production
operation at real scale.

## Choosing the Right Level for a Given Log Statement

```
"User successfully logged in"           → INFO (expected, routine)
"Retry attempt 2 of 3 for payment API"  → WARN (unusual, but handled)
"Failed to charge customer after all
 retries exhausted"                      → ERROR (genuine failure)
"Database connection pool exhausted,
 shutting down"                          → FATAL (can't continue)
```

Choosing the correct level for each individual log statement is what makes level-based filtering
actually useful later — a genuine error logged at `INFO` is effectively invisible to anyone
filtering for real problems, exactly defeating the entire purpose of having levels at all.

## Common Mistakes

- Leaving DEBUG-level logging enabled in production, drowning genuinely important log entries in
  low-value noise and increasing infrastructure cost unnecessarily.
- Logging a genuine error at `INFO` or `WARN` level, making it invisible to any monitoring or
  alerting configured to watch for `ERROR`-level entries specifically.
- Using `FATAL` for something the application actually recovers from — reserve it genuinely for
  conditions that precede the application being unable to continue running at all.

## ➡️ Next

Continue to [structured-logging.md](structured-logging.md) to see how a log entry's actual format
affects how usable it is once it needs to be searched and analyzed at scale.
