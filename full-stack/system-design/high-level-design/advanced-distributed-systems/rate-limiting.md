# 🚦 Rate Limiting

## Protecting the System From Excessive Load, Deliberately

[designing-rest-apis-at-scale.md](../communication-and-data-layer/designing-rest-apis-at-scale.md)
and [the API Gateway pattern](../core-infrastructure/api-gateway-pattern.md), both earlier in this
domain, already mentioned rate limiting as a genuine need. This file covers the actual algorithms
that implement it — and this is the *system-design* depth counterpart to
[Rate Limits: Handling 429](../../../artificial-intelligence/calling-llm-apis-properly/rate-limits-handling-429-backoff-and-retries.md),
already covered from the *client* perspective in this repository's AI Engineering domain — now
covering how the *server side* actually enforces a limit.

## Fixed Window: the Simplest Approach

```
Allow up to 100 requests per CLIENT, per MINUTE - counted in
FIXED, non-overlapping 60-second windows (e.g. 12:00:00-12:00:59,
then 12:01:00-12:01:59).
```

```
GENUINE problem: a client could send 100 requests at 12:00:59,
then ANOTHER 100 at 12:01:00 - 200 requests in TWO real seconds,
despite technically staying within each window's limit.
```

This is a real, well-documented weakness — fixed window "allows boundary burst amplification of up
to twice the configured limit," per widely-referenced technical sources — a client can exploit the
boundary between two windows to burst well beyond the intended rate.

## Sliding Window: Fixing the Boundary Problem

```
SLIDING WINDOW LOG: keep a timestamp for EVERY request; count how
  many fall within the LAST 60 seconds, continuously - genuinely
  ACCURATE, but memory grows with request volume

SLIDING WINDOW COUNTER: a more efficient APPROXIMATION, blending
  the current and previous fixed windows proportionally - "less
  memory... while being more accurate than fixed window"
```

The sliding window counter is a genuinely practical middle ground — meaningfully more accurate than
fixed window, without the genuinely unbounded memory cost of logging every individual request
timestamp.

## Token Bucket: Allowing Controlled Bursts

```
A bucket holds up to N tokens. Tokens REFILL at a steady rate
(e.g. 10/second). Each request CONSUMES one token; if the bucket
is EMPTY, the request is REJECTED.
```

```
A client that's been IDLE accumulates tokens (up to the bucket's
max) - allowing a genuine BURST of requests when it DOES become
active, while still enforcing the SAME average rate over time.
```

Per widely-referenced sources, token bucket is specifically well-suited when *some* burstiness is
genuinely acceptable — an idle client building up "burst credit" and then using it all at once is
often a perfectly reasonable, real usage pattern, unlike a client sustaining a high rate
indefinitely.

## Choosing the Right Algorithm

```
FIXED WINDOW   → simplest to implement; accept the real boundary-
  burst weakness for a genuinely low-stakes use case

SLIDING WINDOW → genuinely more accurate; the right choice when
  precise rate enforcement actually matters

TOKEN BUCKET   → the right choice when controlled BURSTS are
  genuinely acceptable (or even desirable) behavior
```

## Where Rate Limiting Actually Gets Enforced

```
Directly at the API Gateway, per api-gateway-pattern.md, earlier
in this domain - centralizing rate limiting at the ENTRY point
means individual backend services never need to implement this
logic themselves, and a misbehaving client is stopped BEFORE
consuming any real, downstream resources at all.
```

## Common Mistakes

- Using fixed window rate limiting for a use case where precise, consistent enforcement genuinely
  matters, missing its real, well-documented boundary-burst weakness.
- Implementing rate limiting independently in every backend service instead of centralizing it at
  the API Gateway, duplicating logic and allowing excessive traffic to consume real downstream
  resources before being stopped.
- Choosing token bucket without actually confirming that bursty traffic is genuinely acceptable for
  the specific system's real requirements.

## ➡️ Next

Continue to
[authorization-at-architecture-scale.md](authorization-at-architecture-scale.md) to see how access
control itself scales across a genuinely distributed system.
