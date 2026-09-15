# 📝 Logging Fundamentals

## The Third Pillar, in Depth

[what-is-observability.md](../monitoring-and-observability/what-is-observability.md), the previous
module, named logs as one of the three pillars of observability alongside metrics and traces. This
module covers logging specifically at the *production infrastructure* level — distinct from
[Logging and Monitoring](../../backend/logging-and-monitoring/)'s coverage of the actual Node.js
libraries (Winston, Pino) used to generate those logs in application code.

## What a Log Actually Is

```
A LOG is a discrete, TIMESTAMPED record of something that
happened - one specific event, at one specific moment, with
enough detail to understand what occurred.

"2026-09-15T14:32:01Z ERROR Failed to process order #4821:
 connection to payment gateway timed out"
```

Where a metric answers "how many errors occurred in the last hour?" (an aggregated number), a log
answers "what *specifically* happened, in this one case?" — the detailed, individual record metrics
alone can never provide.

## Why Logs Matter More in Production Than in Development

```
LOCAL development: a bug can be reproduced by re-running the code
  with a debugger attached, directly

PRODUCTION: the exact moment something went wrong is GONE the
  instant it happens - a debugger can't be attached retroactively.
  LOGS ARE THE ONLY RECORD of what actually occurred.
```

This is genuinely the core reason production logging matters as much as it does — unlike local
development, there's no way to go back and re-investigate a production incident directly; the logs
captured *at the time* are the only evidence that will ever exist of what actually happened.

## What Belongs in a Log Entry

```
- WHAT happened (a clear, specific message)
- WHEN it happened (a precise timestamp)
- WHERE it happened (which service, which server/instance)
- Enough CONTEXT to actually investigate (a request ID, a user
  ID, relevant parameters) - directly the same discipline already
  established in logging-ai-requests-and-responses-for-
  debugging.md, earlier in this repository's AI Engineering domain
```

A log entry that only says "an error occurred," with no further context, is close to useless for
actual investigation — the same principle already established for AI request logging applies
identically here: enough detail to genuinely diagnose the problem later, without needing to
reproduce it from scratch.

## What Should Never Be Logged

```
NEVER log: passwords, full credit card numbers, API keys/secrets,
or more personal user data than a specific investigation
genuinely requires.
```

This directly echoes the same sensitive-data discipline already established for AI interaction
logs — production application logs are just as real a potential source of leaked sensitive data,
and deserve the identical access-control and retention discipline.

## Common Mistakes

- Logging vague, contextless messages ("something went wrong") that provide no actual basis for
  investigating a real production incident later.
- Assuming a bug can always be reproduced locally, when the actual production conditions that
  triggered it may never be reproducible outside production itself.
- Logging sensitive data (passwords, full payment details) without considering that logs are a real,
  persistent store of data requiring the same protection as any other sensitive data.

## ➡️ Next

Continue to [log-levels.md](log-levels.md) to see how logs are categorized by severity, and why
that categorization genuinely matters.
