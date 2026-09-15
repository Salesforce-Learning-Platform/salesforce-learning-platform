# ⚖️ Consistency vs. Performance Tradeoffs

## The Trade-Off Every Prior File Already Previewed

[database-replication-and-sharding.md](database-replication-and-sharding.md)'s replication lag,
[sql-vs-nosql-at-scale.md](sql-vs-nosql-at-scale.md)'s "relaxed ACID guarantees" — every prior file
in this module has already touched this same underlying tension. This file names it directly, with
the formal framework distributed systems use to reason about it: the **CAP theorem**.

## The CAP Theorem, Precisely

```
A distributed system can guarantee, AT MOST, TWO of these THREE
properties SIMULTANEOUSLY:

CONSISTENCY  → every client sees the SAME data, no matter which
               node it connects to

AVAILABILITY → every request genuinely gets a response, even if
               some nodes are down

PARTITION TOLERANCE → the system keeps WORKING despite a network
               failure between nodes
```

Formally proven by Seth Gilbert and Nancy Lynch (building on Eric Brewer's original 1999
conjecture) — and genuinely, practically important: since real networks *do* experience partitions
(a network failure between two data centers, for instance), a real distributed system must tolerate
partitions, which forces an actual, unavoidable choice between consistency and availability during
that partition.

## Why This Isn't Just Theoretical

```
During an ACTUAL network partition between two database replicas:

CHOOSE CONSISTENCY (CP) → the system REFUSES to answer from the
  node that might have STALE data, until the partition resolves -
  some requests genuinely FAIL

CHOOSE AVAILABILITY (AP) → the system ANSWERS anyway, from
  whatever data IS currently available - the answer might be
  STALE, but a response is genuinely returned
```

This is the real, unavoidable choice a distributed system's design makes — not hypothetically, but
concretely, the moment a genuine partition actually occurs in production.

## Applying This to the URL Shortener

```
CREATING a new short URL: STRONG consistency probably matters -
  two users should NEVER be assigned the SAME short code
  simultaneously.

REDIRECTING via an EXISTING short URL: availability likely
  matters MORE - it's usually ACCEPTABLE if a newly created URL
  takes a few seconds to become available EVERYWHERE, but a
  redirect FAILING entirely is a genuinely worse user experience.
```

This directly answers the exact question raised, but left open, in
[functional-vs-non-functional-requirements.md](../system-design-foundations/functional-vs-non-functional-requirements.md),
the previous module — the CAP theorem gives a concrete, structured way to actually reason through
that trade-off, rather than leaving it as an unexamined assumption.

## Strong vs. Eventual Consistency

```
STRONG consistency: every read reflects the MOST RECENT write,
  immediately - genuinely necessary for a banking transaction

EVENTUAL consistency: reads MIGHT return slightly stale data
  temporarily, but the system GUARANTEES all replicas eventually
  converge to the same state - acceptable for many read-heavy,
  less consequential use cases (a social media "like" count,
  for instance)
```

This directly connects back to [sql-vs-nosql-at-scale.md](sql-vs-nosql-at-scale.md)'s "relaxed
ACID" characterization of many NoSQL systems — eventual consistency is precisely the specific
relaxation being made, in exchange for the genuine performance and availability benefits already
covered throughout this module.

## A Practical Decision Framework

```
Ask, for EACH piece of data specifically (not the whole system
uniformly): "what's the REAL cost if a user sees SLIGHTLY stale
data here, versus the cost of the request FAILING entirely?"
```

This is the genuinely practical takeaway — consistency requirements aren't uniform across an
entire system; different pieces of data within the *same* system often warrant genuinely different
points on this trade-off, exactly as the URL Shortener's creation-vs-redirect example demonstrates.

## Common Mistakes

- Treating consistency as a single, system-wide setting rather than a decision made deliberately
  per piece of data, based on that data's actual real-world stakes.
- Assuming "eventual consistency" means "no consistency guarantee at all," rather than a genuine,
  bounded guarantee that replicas do eventually converge.
- Choosing strong consistency by default everywhere, without weighing the genuine availability and
  performance cost it imposes for data that didn't actually need it.

## Module Summary

Across this module: **networking basics** — HTTP, TCP, and DNS — apply directly to service-to-
service communication, with latency compounding across every additional service boundary a request
crosses (see [networking-basics-for-system-design.md](networking-basics-for-system-design.md));
**REST APIs at scale** need explicit versioning, idempotency for safe retries, cursor-based
pagination, and deliberate sync/async design beyond what a single, simple API requires (see
[designing-rest-apis-at-scale.md](designing-rest-apis-at-scale.md)); **SQL vs. NoSQL**, verified
against AWS's own official comparison, is rarely a single system-wide choice — a hybrid approach
choosing deliberately per component is genuinely common in real production systems (see
[sql-vs-nosql-at-scale.md](sql-vs-nosql-at-scale.md)); **replication and sharding** are
complementary scaling techniques — replication distributing reads, sharding distributing both reads
and writes across independent data subsets — each with genuine trade-offs (replication lag,
cross-shard query complexity) (see
[database-replication-and-sharding.md](database-replication-and-sharding.md)); and **the CAP
theorem**, formally verified, provides the structured framework for the consistency-vs-availability
trade-off every distributed system genuinely faces during a real network partition, applied
deliberately per piece of data rather than uniformly across an entire system.
