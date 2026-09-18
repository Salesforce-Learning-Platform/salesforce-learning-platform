# 🚦 Designing a Rate Limiter

## A Second Worked Example, Genuinely Different in Shape

[designing-a-url-shortener.md](designing-a-url-shortener.md) walked through a full-stack system
serving real user traffic. A **rate limiter** is a genuinely different kind of design problem — a
smaller, focused piece of infrastructure, but one that sits directly in the critical path of every
request an entire system receives.

## Step 1: Clarify Requirements

```
FUNCTIONAL: limit each client to N requests per time window;
  reject requests EXCEEDING the limit with a clear error

NON-FUNCTIONAL: the limiter itself must add MINIMAL latency
  (it sits in front of EVERY request); must work CORRECTLY across
  MULTIPLE load-balanced instances of the service it protects
  (per Load Balancing, earlier in this domain)
```

The second non-functional requirement is genuinely the crux of this entire problem — a rate
limiter's own real difficulty comes specifically from needing to work correctly in a
*distributed*, multi-instance environment, not from the core counting logic itself.

## Step 2: Choose the Algorithm

```
Per rate-limiting.md, earlier in this domain: TOKEN BUCKET is
often the right choice - it allows CONTROLLED bursts (a
genuinely common, real traffic pattern) while still enforcing a
consistent AVERAGE rate over time.
```

## Step 3: the Naive, Single-Instance Design

```python
buckets = {}   # client_id -> {tokens, last_refill}

def is_allowed(client_id):
    bucket = buckets.setdefault(client_id, {"tokens": 10, "last_refill": now()})
    elapsed = now() - bucket["last_refill"]
    bucket["tokens"] = min(10, bucket["tokens"] + elapsed * REFILL_RATE)
    bucket["last_refill"] = now()

    if bucket["tokens"] >= 1:
        bucket["tokens"] -= 1
        return True
    return False
```

```
This works CORRECTLY for a SINGLE instance - but per Load
Balancing, earlier in this domain, real traffic is distributed
ACROSS multiple server instances. EACH instance's own in-memory
"buckets" dictionary is GENUINELY separate - a client could
receive N tokens' worth of allowance from EACH instance
SEPARATELY, multiplying the real, effective limit.
```

## Step 4: the Distributed Fix — a Shared, Centralized Store

```python
import redis
r = redis.Redis()

def is_allowed(client_id):
    key = f"rate_limit:{client_id}"
    current = r.get(key)
    if current is None:
        r.setex(key, 60, 1)   # first request: set count=1, EXPIRE in 60s
        return True
    if int(current) < 100:
        r.incr(key)
        return True
    return False
```

This directly applies [Redis](../../../backend/caching-local-and-redis/), already covered in this
repository's Backend domain, as a genuinely shared, centralized counter — every load-balanced
instance reads and writes the *same* Redis key, correctly enforcing one true, consistent limit
across the entire distributed system, directly solving Step 3's real problem.

## Where the Rate Limiter Actually Lives in the Architecture

```
Directly per api-gateway-pattern.md, earlier in this domain -
centralizing the rate limiter at the API GATEWAY means every
individual downstream service is protected automatically, without
each one needing its OWN separate rate-limiting logic.
```

## A Genuine Trade-Off: the Rate Limiter's Own Availability

```
If the SHARED Redis instance the rate limiter depends on becomes
UNAVAILABLE, does the system FAIL OPEN (allow all traffic through,
unprotected) or FAIL CLOSED (reject everything)?

This is a REAL, deliberate design decision - directly the SAME
consistency-vs-availability trade-off from the CAP theorem,
earlier in this domain, now applied specifically to the rate
limiter's OWN dependency.
```

For most real systems, failing *open* (allowing traffic through unprotected, temporarily) is the
more common, pragmatic choice — a rate limiter that itself becomes a hard dependency capable of
taking down the entire system it's meant to protect would be a genuinely worse outcome than
briefly running unprotected.

## Common Mistakes

- Implementing rate limiting with purely local, in-memory state, which fails silently once traffic
  is distributed across multiple load-balanced instances.
- Never explicitly deciding whether the rate limiter fails open or closed when its own dependency
  (Redis) becomes unavailable.
- Implementing rate limiting separately in every individual service instead of centralizing it at
  the API Gateway.

## ➡️ Next

Continue to
[designing-a-notification-system.md](designing-a-notification-system.md) for the third, final
worked example in this module.
