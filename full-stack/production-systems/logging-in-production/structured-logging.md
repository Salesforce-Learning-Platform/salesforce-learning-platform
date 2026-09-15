# 🧱 Structured Logging

## Text Logs vs. Structured Logs

```
PLAIN TEXT log: "2026-09-15 14:32:01 ERROR Failed to process
  order 4821 for user 892: payment timeout"

STRUCTURED (JSON) log:
{
  "timestamp": "2026-09-15T14:32:01Z",
  "level": "error",
  "message": "Failed to process order",
  "orderId": "4821",
  "userId": "892",
  "reason": "payment_timeout"
}
```

A plain-text log entry is readable by a human scanning a file directly — but a **structured** log
entry (typically JSON) is readable by *both* a human and, critically, by machines: a log aggregation
system can query, filter, and analyze structured fields directly, without needing to parse free-form
text with fragile regular expressions.

## Why This Matters at Real Production Scale

```
"Find every failed order for user 892 in the last 24 hours"

Plain text: requires a REGEX search across potentially millions
  of unstructured log lines, hoping the format is consistent

Structured (JSON): a direct, precise QUERY -
  level=error AND userId=892 AND timestamp > (24 hours ago)
```

This is the real, practical payoff: a structured field like `userId` can be queried directly and
precisely, while the same information embedded in free-form text requires fragile pattern-matching
that breaks the moment a log message's wording changes even slightly.

## Consistent Field Names Across an Entire System

```
Service A logs: { "user_id": "892", ... }
Service B logs: { "userId": "892", ... }        ← INCONSISTENT

vs.

Service A logs: { "userId": "892", ... }
Service B logs: { "userId": "892", ... }        ← CONSISTENT
```

For a system with multiple services (directly building on
[managing-shared-state-between-services.md](../../artificial-intelligence/multi-agent-architecture-concerns/managing-shared-state-between-services.md)'s
multi-service context, earlier in this repository), consistent field naming *across every service*
is what actually makes cross-service log queries possible at all — inconsistent naming defeats the
entire purpose of structuring logs in the first place.

## A Request ID: Tying Related Logs Together

```json
{ "timestamp": "...", "level": "info", "message": "Request received", "requestId": "req-a1b2c3" }
{ "timestamp": "...", "level": "info", "message": "Database query executed", "requestId": "req-a1b2c3" }
{ "timestamp": "...", "level": "error", "message": "Payment failed", "requestId": "req-a1b2c3" }
```

Including a shared `requestId` on every log entry generated while handling one specific request is
directly the same tracing idea already established in
[logging-every-step-of-the-pipeline.md](../../artificial-intelligence/multi-agent-architecture-concerns/logging-every-step-of-the-pipeline.md)'s
`pipeline_run_id` — a consistent identifier that lets every log entry related to one specific
request or transaction be reconstructed together, in order, regardless of how many separate log
lines it actually produced.

## Common Mistakes

- Using inconsistent field names for the same concept across different services, breaking the
  ability to query logs consistently across an entire system.
- Logging in structured JSON format but still embedding the genuinely important detail inside a
  single unstructured `message` string, losing most of the actual benefit of structuring at all.
- Omitting a request/transaction ID from related log entries, making it much harder to reconstruct
  the full sequence of what happened for one specific request.

## ➡️ Next

Continue to [centralized-logging.md](centralized-logging.md) to see where structured logs like
these actually get sent, stored, and searched at real scale.
