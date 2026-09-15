# 🔁 Implementing Retry Strategies for Broken Outputs

## A Different Kind of Retry

[Rate Limits: Handling 429, Backoff and Retries](../calling-llm-apis-properly/rate-limits-handling-429-backoff-and-retries.md)
already covered retrying a request that failed for an *infrastructure* reason — a `429`, a
timeout, a transient network error. This file covers a genuinely different situation: the request
**succeeded**, the model responded, but the response **failed schema validation**. The failure
mode is different, so the retry strategy needs to be different too.

## Strategy 1: The Naive Retry

```js
async function generateWithRetry(schema, promptFn, maxAttempts = 2) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const raw = await callLlm(promptFn());
    const result = schema.safeParse(raw);
    if (result.success) return result.data;
  }
  throw new Error("AI response failed validation after all retry attempts");
}
```

Simply asking again, with the exact same prompt, works reasonably often — a model's
probabilistic nature (per
[deterministic-vs-probabilistic-outputs.md](../how-llms-actually-work/deterministic-vs-probabilistic-outputs.md))
means the *same* prompt can genuinely produce a *different*, this time valid, response. This is
the simplest strategy, and a reasonable default for a single retry.

## Strategy 2: Retry With Error Feedback

```js
async function generateWithFeedbackRetry(schema, basePrompt, maxAttempts = 2) {
  let prompt = basePrompt;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const raw = await callLlm(prompt);
    const result = schema.safeParse(raw);
    if (result.success) return result.data;

    const errors = z.flattenError(result.error);
    prompt = `${basePrompt}\n\nYour previous response had these problems: ` +
             `${JSON.stringify(errors.fieldErrors)}. Please correct them and respond again.`;
  }
  throw new Error("AI response failed validation after all retry attempts");
}
```

A meaningfully stronger strategy: feed the *actual validation errors* from
[verifying-ai-responses-against-a-schema.md](verifying-ai-responses-against-a-schema.md)'s
`z.flattenError()` back into the next prompt. This gives the model concrete, specific feedback
about exactly what went wrong, rather than asking it to blindly try again — meaningfully raising
the odds the second attempt actually succeeds.

## A Retry Budget — Never Retry Forever

```js
const MAX_VALIDATION_RETRIES = 2; // total attempts = 1 original + 2 retries = 3
```

Every retry strategy needs a firm, small upper bound. Unlike a `429`, a validation failure isn't
guaranteed to be transient — a poorly-designed prompt can fail validation consistently, and an
unbounded retry loop against that prompt would burn real API cost (per
[cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md](../calling-llm-apis-properly/cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md))
without ever succeeding. Two or three total attempts is a reasonable, common default — beyond that,
[handling-invalid-or-mismatched-responses.md](handling-invalid-or-mismatched-responses.md)'s error/
fallback/escalation options take over.

## Recognizing a Persistent Failure Pattern

```
A single validation failure → probabilistic noise, worth a retry

The SAME field failing validation across many DIFFERENT requests
→ a genuine, systematic prompt or schema problem, not something a
  retry will ever fix
```

If a particular field fails validation on a meaningful fraction of requests over time, that's a
signal to go back and strengthen the prompt (per
[Prompt Engineering Fundamentals](../prompt-engineering-fundamentals/)) or reconsider the schema
itself — not a signal to simply raise the retry budget. Logging every validation failure (as
`handling-invalid-or-mismatched-responses.md` covered) is exactly what makes a pattern like this
visible in the first place.

## Looking Ahead

[Error Handling in AI Applications](../error-handling-in-ai-applications/), later in this domain,
covers the broader picture this file's retry logic fits into — combining validation retries with
infrastructure retries, timeouts, and circuit breakers into one coherent error-handling strategy
for an AI-powered application as a whole.

## Common Mistakes

- Retrying with the exact same prompt indefinitely instead of injecting the specific validation
  errors, missing a meaningfully more effective and equally simple technique.
- Setting no retry budget at all, letting a systematically broken prompt burn cost on requests that
  were never going to succeed.
- Treating a validation retry and a rate-limit retry as the same mechanism — they're triggered by
  genuinely different failures and call for genuinely different responses.

## Module Summary

Across this module: **AI output is a genuine trust boundary**, deserving the same validation
discipline as user input, regardless of provider reliability (see
[never-trust-ai-output-without-validation.md](never-trust-ai-output-without-validation.md));
**Zod schemas built for AI responses** use `.optional()`, `.nullable()`, `.default()`,
`z.discriminatedUnion()`, and `.refine()` to model the genuinely varied shapes and cross-field rules
real AI output can take (see
[defining-a-validation-schema-using-zod.md](defining-a-validation-schema-using-zod.md));
**`.safeParse()`**, combined with `z.flattenError()` or `z.treeifyError()`, is the right way to
verify an AI response without risking an uncaught exception (see
[verifying-ai-responses-against-a-schema.md](verifying-ai-responses-against-a-schema.md));
**a validation failure calls for a deliberate response** — a clear error, a safe fallback, or
escalation for human review, chosen by the actual stakes of the data (see
[handling-invalid-or-mismatched-responses.md](handling-invalid-or-mismatched-responses.md));
and **retrying a validation failure** — ideally with the actual errors fed back into the next
prompt, and always within a firm retry budget — is a genuinely different concern from retrying an
infrastructure failure like a rate limit.
