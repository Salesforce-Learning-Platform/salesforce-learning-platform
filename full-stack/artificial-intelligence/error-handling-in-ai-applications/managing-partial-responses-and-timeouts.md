# ⏱️ Managing Partial Responses and Timeouts

## A Response That Never Finishes

The previous file covered a response that arrived complete but was invalid. This file covers the
opposite problem: a request that never gets a complete response at all — cut short by a timeout, a
dropped connection, or the API being overloaded.

## The Relevant Error Types

```
504 timeout_error    → the request timed out while processing
529 overloaded_error → the API is temporarily overloaded
500 api_error        → an unexpected internal error — worth
                        retrying with backoff
```

Anthropic's own API documentation lists these as the specific status codes a long-running or
poorly-timed request can hit. `504` and `529` are both explicitly framed as *transient* — the kind
of failure retrying is actually likely to fix, unlike (for instance) a `400` validation error,
which will fail identically no matter how many times it's retried.

## Preferring Streaming for Long Requests

```
Non-streaming request, large max_tokens, poor network:
  → a dropped idle connection loses the ENTIRE response, with
    nothing usable recovered

Streaming request, same scenario:
  → everything received before the drop is already in hand
```

For any request expected to take a while — a long `max_tokens`, a complex generation — Anthropic's
own guidance is to prefer [the streaming API](../streaming-responses/) specifically because a
network issue partway through a streamed response still leaves whatever text arrived before the
drop, rather than losing the entire response as a single failed unit.

## Handling a Genuine Mid-Stream Error

```
event: error
data: {"type": "error", "error": {"type": "overloaded_error", "message": "..."}}
```

As introduced in
[improving-ux-in-ai-driven-applications.md](../streaming-responses/improving-ux-in-ai-driven-applications.md),
a stream itself can carry an explicit `error` event after the connection has already returned a
success status — this needs to be handled as its own distinct case, separate from an HTTP-level
error on the initial request.

```js
try {
  for await (const event of stream) {
    if (event.type === "error") {
      handlePartialFailure({ partialText, error: event.error });
      return;
    }
    // ... normal event handling
  }
} catch (networkError) {
  handlePartialFailure({ partialText, error: networkError });
}
```

Both a genuine `error` event and a lower-level network exception during iteration end up needing
the same decision: what to do with the `partialText` that's already been accumulated. Discarding it
silently, or leaving a visibly truncated response on screen with no explanation, are both worse
than a clear, deliberate choice — an inline "response was interrupted, try again" notice, paired
with the partial text if it's still meaningfully useful on its own.

## Setting Sensible Timeouts

```js
const response = await client.messages.create(
  { model: "claude-opus-5", max_tokens: 1024, messages },
  { timeout: 30_000 }, // an explicit, application-level timeout
);
```

For a non-streaming request, an explicit application-level timeout — shorter than whatever default
the underlying HTTP client uses — keeps a single slow request from holding a resource (a request
handler, a connection) open indefinitely, giving the application a predictable point at which to
treat the request as failed and respond accordingly.

## Common Mistakes

- Using a very large `max_tokens` on a non-streaming request without considering that a dropped
  connection loses the entire response, not just what came after the drop.
- Treating a stream's mid-stream `error` event identically to a total connection failure, when the
  former still has a real, complete `partialText` worth potentially preserving.
- Leaving no application-level timeout at all, letting a single unusually slow request hold
  resources indefinitely.

## ➡️ Next

Continue to [implementing-retry-mechanisms.md](implementing-retry-mechanisms.md) to see how these
transient failures — timeouts, overload, internal errors — should actually be retried.
