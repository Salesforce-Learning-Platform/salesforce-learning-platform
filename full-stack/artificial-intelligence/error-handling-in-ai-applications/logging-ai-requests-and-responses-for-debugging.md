# 📝 Logging AI Requests and Responses for Debugging

## Why AI Failures Need Their Own Logging Discipline

An ordinary application error is usually reproducible — the same input reliably produces the same
bug. An AI failure often isn't: the same prompt can succeed nine times and fail the tenth, purely
from a model's probabilistic nature (per
[deterministic-vs-probabilistic-outputs.md](../how-llms-actually-work/deterministic-vs-probabilistic-outputs.md)).
This makes thorough, structured logging genuinely more important here than for most other kinds of
application failures — it may be the *only* record of a failure that never happens again.

## What to Actually Log

```js
function logAiInteraction({ context, model, promptSummary, success, failureReason, requestId, durationMs }) {
  logger.info("ai_interaction", {
    context,          // e.g. "profile-analysis", "refund-tool-call"
    model,
    promptSummary,     // a SHORT summary or hash, not always the full raw prompt
    success,
    failureReason,     // "not_valid_json" | "schema_mismatch" | "timeout" | undefined
    requestId,         // the API's own request-id header/field — critical for support
    durationMs,
    timestamp: new Date().toISOString(),
  });
}
```

The `requestId` field deserves special attention: Anthropic's API returns a unique `request-id`
with every response (`message._request_id` in the Python/TypeScript SDKs), and including it in
every log line is exactly what turns a vague "it failed sometime yesterday" report into something
Anthropic's own support team — or a future engineer reading the logs — can actually look up
precisely.

## Logging the Failure Categories From This Module

```js
// From handling-invalid-or-malformed-json-responses.md's pipeline
logAiInteraction({
  context: "profile-analysis", success: false,
  failureReason: "schema_mismatch", requestId: response._request_id,
});
```

Every failure branch introduced earlier in this module —
[a JSON parse failure or schema mismatch](handling-invalid-or-malformed-json-responses.md), [a
timeout or mid-stream error](managing-partial-responses-and-timeouts.md), [an exhausted retry
sequence](implementing-retry-mechanisms.md) — should route through the same logging function, with
a consistent `failureReason` taxonomy. This consistency is what makes it possible to later ask "how
often does `schema_mismatch` actually happen in production?" as a real, answerable question rather
than a guess.

## What NOT to Log

```
NEVER log, even for debugging:
  - full user PII embedded in a prompt, beyond what's strictly
    needed to diagnose the specific failure
  - API keys or auth tokens
  - a full raw AI response containing sensitive user data, without
    a clear retention and access policy for those logs
```

AI request/response logs can easily become a much larger source of sensitive data than typical
application logs, simply because prompts often contain substantial free-text user content.
Treating these logs with the same access-control and retention discipline as any other store of
user data — never as a lower-stakes debugging convenience — is essential.

## Turning Logs Into a Signal, Not Just a Record

```
A single validation failure           → noise, expected occasionally
The SAME failureReason, on the SAME
prompt template, happening repeatedly → a genuine pattern worth
                                          investigating and fixing
                                          at the prompt/schema level
```

This is the payoff [implementing-retry-strategies-for-broken-outputs.md](../schema-validation-with-zod/implementing-retry-strategies-for-broken-outputs.md)
pointed toward earlier: structured, consistent logging is exactly what makes a *pattern* of
failures visible — a dashboard or alert built on `failureReason` counts, grouped by `context`, can
surface a systematically broken prompt long before it becomes a widespread user-facing problem.

## Common Mistakes

- Logging only that "an AI call failed" without the `requestId`, the specific failure category, or
  enough context to diagnose it later.
- Logging full raw prompts and responses indiscriminately, turning application logs into an
  unintentional, poorly-governed store of sensitive user data.
- Never actually reviewing the aggregated failure logs, so a systematic, fixable problem goes
  unnoticed indefinitely even though every individual failure was technically recorded.

## Module Summary

Across this module: **invalid or malformed JSON** is handled by safely parsing (never letting a
throw go uncaught), stripping common wrapping artifacts like markdown fences, and distinguishing a
parse failure from a schema-validation failure (see
[handling-invalid-or-malformed-json-responses.md](handling-invalid-or-malformed-json-responses.md));
**partial responses and timeouts** — `504`, `529`, `500`, and mid-stream `error` events — are best
mitigated by preferring streaming for long requests and deciding deliberately what to do with any
already-accumulated partial text (see
[managing-partial-responses-and-timeouts.md](managing-partial-responses-and-timeouts.md));
**retry mechanisms** combine the SDK's own built-in exponential backoff for infrastructure failures
with application-level retry logic specifically for validation failures, always behind a firm
attempt ceiling (see [implementing-retry-mechanisms.md](implementing-retry-mechanisms.md)); and
**structured, consistent logging** — with a `requestId`, a clear failure-category taxonomy, and
careful handling of sensitive content — turns individually rare, hard-to-reproduce AI failures into
a genuine, actionable signal over time.
