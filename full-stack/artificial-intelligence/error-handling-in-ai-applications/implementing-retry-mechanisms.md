# 🔁 Implementing Retry Mechanisms

## Three Different Retries, One Unified Strategy

This domain has now introduced three genuinely different retry situations, each covered in its own
module:

```
1. RATE LIMIT (429)         → covered in Calling LLM APIs Properly's
                               rate-limits-handling-429-backoff-and-retries.md
2. VALIDATION FAILURE        → covered in Schema Validation with Zod's
                               implementing-retry-strategies-for-broken-outputs.md
3. TRANSIENT INFRASTRUCTURE
   FAILURE (timeout/overload/
   500)                      → this file
```

This file completes the picture: a transient infrastructure failure — the previous file's `504`,
`529`, or `500` — needs its own retry handling, and a production application benefits from
combining all three into one coherent retry layer rather than three separate, inconsistent ones.

## The SDK's Built-In Retry Behavior

```
The official Anthropic SDKs automatically retry transient failures
(connection errors, rate limits, 5xx server errors) with exponential
backoff — TWICE by default, honoring the retry-after header when
present.
```

For the exact failure categories this file and
[rate-limits-handling-429-backoff-and-retries.md](../calling-llm-apis-properly/rate-limits-handling-429-backoff-and-retries.md)
cover, the official SDK already retries automatically out of the box — meaning a real application
often doesn't need to hand-roll this logic at all for infrastructure-level failures specifically.

```python
client = anthropic.Anthropic(max_retries=4)  # override the SDK's default of 2
```

The retry count is configurable per client, and can be disabled entirely (`max_retries=0`) for a
codepath that needs to handle retries itself instead — for example, one already wrapped in its own
application-level retry-with-user-feedback loop.

## When Hand-Rolled Retry Logic Is Still Worth It

```
Reason 1: retrying needs to be VISIBLE to the user ("Retrying...")
          rather than silently absorbed inside the SDK call
Reason 2: a validation failure (this domain's Schema Validation with
          Zod module) isn't a transient infrastructure failure at
          all — the SDK's built-in retry logic doesn't cover it
Reason 3: the retry needs DIFFERENT logic depending on failure type
          (e.g. feeding validation errors back into the next prompt)
```

The SDK's automatic retries handle the infrastructure category well, but validation failures — a
structurally different problem — always need application-level handling, since the SDK has no way
to know a response was "successfully" received but still wrong for the application's purposes.

## A Unified Retry Wrapper

```js
async function callAiWithFullRetryStrategy(promptFn, schema, { maxAttempts = 3 } = {}) {
  let lastError;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const raw = await callLlm(promptFn(lastError)); // pass prior error for feedback, if any
      const parsed = await getStructuredAiResponse(schema, raw, { context: "unified-retry" });

      if (parsed.ok) return parsed.data;
      lastError = parsed; // schema/parse failure — retry with feedback
    } catch (infraError) {
      // the SDK already retried transient infra failures internally;
      // reaching here means even ITS retries were exhausted
      lastError = infraError;
    }
  }

  throw new Error(`AI request failed after ${maxAttempts} attempts: ${JSON.stringify(lastError)}`);
}
```

This wrapper leans on the SDK's own built-in retries for the infrastructure category, while adding
its own application-level loop specifically for the validation-failure category — combining both
retry concerns without duplicating logic the SDK already handles well.

## A Firm Ceiling, Always

```
Every retry strategy in this domain — rate limits, validation,
infrastructure — shares ONE non-negotiable rule: a firm, small
maximum attempt count, after which the failure is surfaced
explicitly rather than retried indefinitely.
```

Regardless of which failure category triggered it, an unbounded retry loop is never acceptable —
it risks real cost (repeated API calls) and a request that simply hangs from the user's perspective
instead of failing in a way the application can respond to.

## Common Mistakes

- Hand-rolling retry logic for transient infrastructure failures the SDK already retries
  automatically, duplicating behavior instead of just configuring `max_retries`.
- Treating a validation failure and an infrastructure failure with the identical retry logic, when
  only the former benefits from feeding the specific error back into the next prompt.
- Omitting a firm maximum attempt count on any hand-rolled retry loop, risking an effectively
  unbounded retry under a persistent, non-transient failure.

## ➡️ Next

Continue to
[logging-ai-requests-and-responses-for-debugging.md](logging-ai-requests-and-responses-for-debugging.md)
to see how every failure this module covers becomes something an engineer can actually diagnose
after the fact.
