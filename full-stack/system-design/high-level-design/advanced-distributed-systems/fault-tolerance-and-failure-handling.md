# 🔧 Fault Tolerance and Failure Handling

## Designing for Failure, Deliberately

[reliability-and-availability.md](reliability-and-availability.md) established *why* a system's
availability multiplies down as it depends on more services. This file covers the concrete
techniques that actually keep a genuinely large distributed system available despite individual
components genuinely, inevitably failing.

## The Core Mindset: Failures Are Not Exceptional, They're Expected

```
At real system scale (thousands of servers, millions of requests),
INDIVIDUAL component failures aren't a rare edge case - they are
a GENUINELY routine, expected, ongoing occurrence. Fault-tolerant
design assumes failure WILL happen, and designs for GRACEFUL
handling rather than PREVENTION alone.
```

This is a genuinely important mindset shift from smaller-scale development — at real distributed-
system scale, the question isn't "how do we prevent every failure?" (genuinely impossible) but "how
does the system behave correctly *despite* failures that will genuinely occur?"

## The Circuit Breaker Pattern

```
CLOSED (normal)   → requests flow through normally; the breaker
  monitors error rates and response times

OPEN (failing)     → after too many failures, the breaker REJECTS
  requests IMMEDIATELY, without even attempting to call the
  failing service - giving it time to recover, and preventing
  the CALLER from wasting time waiting on calls likely to fail

HALF-OPEN (testing) → after a timeout, a LIMITED number of test
  requests are allowed through - SUCCESS returns to CLOSED;
  FAILURE returns to OPEN
```

This is directly the same underlying idea as
[the State Pattern](../../low-level-design/behavioral-design-patterns/state-pattern.md), already
covered in the Low-Level Design domain — a circuit breaker's behavior genuinely depends on, and
transitions between, its own current internal state, with the SAME `execute()`-style call behaving
differently in each state.

```
NOTE: Netflix's own Hystrix library, historically the most
well-known circuit breaker implementation, is now DEPRECATED -
current, actively maintained alternatives include Resilience4j
and Spring Cloud Circuit Breaker.
```

## Retries, With Genuine Discipline

```
This directly extends implementing-retry-mechanisms.md, already
covered in this repository's AI Engineering domain - the SAME
discipline applies here: EXPONENTIAL backoff, and a FIRM maximum
attempt count, never an unbounded retry loop against a genuinely
failing dependency.
```

A retry without a circuit breaker can actually make a struggling service's situation *worse* —
retrying aggressively against an already-overloaded service adds exactly the additional load it can
least afford; combining retries with a circuit breaker (per above) avoids this specific, real risk.

## Redundancy: No Single Point of Failure

```
Directly extending Load Balancing, earlier in this domain - if
EVERY critical component has multiple, redundant instances (with
NO single point of failure anywhere), the failure of any ONE
instance doesn't take down the entire system.
```

This is the concrete, practical mechanism behind genuinely achieving the higher availability
targets from [reliability-and-availability.md](reliability-and-availability.md) — redundancy is
what actually makes a system's overall availability *higher* than any single instance's own
individual availability.

## Graceful Degradation

```
When a NON-CRITICAL component fails (e.g. a recommendation
service), the CORE functionality (e.g. viewing a product page)
should CONTINUE working, simply WITHOUT that non-critical feature
- rather than the entire request failing outright.
```

This is a genuinely important design discipline — deliberately distinguishing which components are
truly critical versus genuinely optional, and designing the system so a non-critical failure never
cascades into a total, user-visible outage.

## Common Mistakes

- Retrying aggressively against a failing dependency with no circuit breaker, adding exactly the
  load an already-struggling service can least handle.
- Treating every component as equally critical, missing the opportunity for graceful degradation
  when a genuinely non-essential piece fails.
- Referencing Hystrix as the current standard circuit breaker implementation, when it's now
  deprecated in favor of actively maintained alternatives.

## ➡️ Next

Continue to [observability-at-scale.md](observability-at-scale.md) to see how failures like these
are actually detected and diagnosed in a genuinely large, distributed system.
