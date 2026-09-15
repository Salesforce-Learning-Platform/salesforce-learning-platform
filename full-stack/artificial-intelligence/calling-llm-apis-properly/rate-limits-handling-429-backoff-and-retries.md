# 🚦 Rate Limits: Handling 429, Backoff, and Retries

## Why Rate Limits Exist

An LLM provider's API enforces limits — requests per minute, and separate input/output tokens per
minute — to prevent abuse and manage real, finite compute capacity fairly across every customer.
Exceeding any of these limits returns an HTTP **`429`** error, along with a `retry-after` header
telling the caller exactly how long to wait before trying again.

## The `retry-after` Header — Don't Guess, Read It

```js
async function callWithRateLimitHandling(requestFn) {
  const response = await requestFn();

  if (response.status === 429) {
    const retryAfter = parseInt(response.headers.get("retry-after"), 10); // in seconds
    await new Promise((resolve) => setTimeout(resolve, retryAfter * 1000));
    return callWithRateLimitHandling(requestFn); // try again, now that the wait has passed
  }

  return response;
}
```

The API itself tells the caller precisely how long to wait via the `retry-after` header — there's
no need to guess a reasonable delay; reading and honoring this value directly is the correct,
authoritative approach.

## Exponential Backoff for Transient Failures

```js
async function callWithExponentialBackoff(requestFn, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (err) {
      if (attempt === maxRetries - 1) throw err; // out of retries — let it fail for real

      const delay = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s, ...
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
}
```

For transient failures more broadly (connection errors, rate limits, and `5xx` server errors), the
standard, provider-recommended approach is **exponential backoff**: each retry waits
progressively longer than the last (1 second, then 2, then 4, and so on), rather than retrying
immediately or at a fixed interval. Official SDKs implement this automatically — retrying transient
failures with exponential backoff a small number of times by default, honoring `retry-after` when
present — configurable, but already correct out of the box for most applications.

## Why Immediate, Unbounded Retries Make Things Worse

```
Naive retry: fails → immediately retries → fails again (still
rate-limited) → immediately retries again → ... a tight loop
hammering an already-overloaded endpoint, worsening the problem
for EVERYONE, not just this one request.
```

Retrying immediately and repeatedly, with no backoff at all, doesn't just fail to solve the
problem — it actively makes it worse, adding more load to an endpoint that's already signaling it's
at capacity. This is exactly why exponential backoff (increasing delay, not a fixed or absent one)
is the standard, correct approach.

## Distinguishing a Rate Limit From Other 429-Shaped Failures

Not every `429` behaves identically — a genuine, temporary rate limit includes a `retry-after`
header and is safe to retry once that time passes; a monthly spend cap being reached also returns a
`429`-style error but has **no** `retry-after` header, and retrying (even automatically) simply
keeps failing until the next billing period. Distinguishing these cases (often via a specific error
code in the response body) matters for building genuinely correct retry logic, rather than
retrying indefinitely against something that will never succeed until a human intervenes.

## Common Mistakes

- Retrying a failed request immediately, in a tight loop, worsening an already-rate-limited
  situation instead of backing off.
- Ignoring the `retry-after` header and guessing an arbitrary delay instead, when the API already
  provides the exact, correct value to use.
- Retrying indefinitely against a genuinely non-retryable failure (like a reached spend cap),
  rather than recognizing it and surfacing a real, actionable error instead.

## Module Summary

Across this module: **message roles** — `user`, `assistant`, and the separately-provided `system`
parameter — structure a real API request, with the full conversation history needing to be resent
on every call (see [message-roles-system-user-assistant.md](message-roles-system-user-assistant.md));
**cost awareness** means recognizing that input tokens (including the entire resent conversation
history) and output tokens are billed, often at different rates, and that a bloated system prompt
is a genuinely recurring cost (see
[cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md](cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md));
**token budgeting** plans deliberately for the context window's shared limit across prompt,
history, and response, including strategies for a growing conversation or an oversized document
(see
[token-budgeting-prompt-size-response-size-and-overflow-planning.md](token-budgeting-prompt-size-response-size-and-overflow-planning.md));
and handling a **`429` rate limit** correctly means honoring the `retry-after` header and applying
exponential backoff for transient failures, never retrying immediately or indefinitely against a
non-retryable error.
