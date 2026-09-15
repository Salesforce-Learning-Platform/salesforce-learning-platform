# 🛡️ Reliability and Availability

## From Building to Staying Up

[Core Infrastructure](../core-infrastructure/) covered how a system scales to handle real traffic.
This module covers a genuinely different, equally essential concern: staying *up* and *correct*
once it's built — starting with the concrete, measurable meaning of "availability."

## Availability, Measured Precisely: "The Nines"

```
99.9%   (three nines)  → ~8 hours 46 minutes of downtime PER YEAR
99.99%  (four nines)   → ~53 minutes of downtime PER YEAR
99.999% (five nines)   → ~5 minutes 15 seconds of downtime PER YEAR
```

This isn't a vague marketing term — it's a precise, calculable measurement:
`(Total Time − Downtime) / Total Time × 100`. Each additional "nine" cuts allowed downtime by
roughly 90%, and — critically — each additional nine requires genuinely more sophisticated,
expensive infrastructure to actually achieve: three nines is achievable with a single on-call
engineer and good alerting; five nines genuinely requires fault-tolerant architecture and automated
recovery, covered in
[fault-tolerance-and-failure-handling.md](fault-tolerance-and-failure-handling.md), next in this
module.

## A Genuinely Important, Easy-to-Miss Fact: Availability Multiplies

```
Service A: 99.9% available
Service B: 99.9% available

A request depending on BOTH A and B: 0.999 * 0.999 ≈ 99.8%
AVAILABLE - LOWER than either individual service alone.
```

This is a genuinely counter-intuitive, important consequence directly connecting back to
[microservices-fundamentals.md](../core-infrastructure/microservices-fundamentals.md), the
previous module — every additional service a request genuinely depends on *multiplies* the overall
availability calculation, meaning a system composed of many "reliable" individual services can
still have surprisingly lower *overall* availability than any single piece.

## Reliability vs. Availability: a Genuine Distinction

```
AVAILABILITY: is the system UP and RESPONDING right now?

RELIABILITY: does the system produce CORRECT results, CONSISTENTLY,
  over time - even when technically "available"?
```

A system can genuinely be "available" (responding to every request) while being unreliable (
returning incorrect data, silently corrupting state) — these are related but genuinely distinct
qualities, both worth measuring and designing for deliberately.

## Setting a Realistic Availability Target

```
This directly extends functional-vs-non-functional-requirements.md,
from earlier in this domain - a REAL project should choose an
availability target DELIBERATELY, based on the actual cost of
downtime for THIS specific system, not simply aim for "as high as
possible" by default.
```

For a personal blog, occasional downtime is a minor inconvenience; for a payment processing
system, even a few minutes of downtime carries genuine, real financial and trust consequences —
the *appropriate* target genuinely varies, and pursuing five-nines reliability for a system that
doesn't actually need it wastes real engineering effort that could go elsewhere.

## Common Mistakes

- Assuming a system's overall availability equals its weakest individual component's availability,
  missing that dependent services' availability actually *multiplies* rather than simply floors at
  the minimum.
- Pursuing an availability target far higher than the system's actual, real-world needs justify,
  spending disproportionate engineering effort for limited real benefit.
- Conflating availability (is it up?) with reliability (is it correct?) as though they were the
  same measurable quality.

## ➡️ Next

Continue to
[fault-tolerance-and-failure-handling.md](fault-tolerance-and-failure-handling.md) to see the
concrete techniques that actually achieve a genuinely high availability target.
