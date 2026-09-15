# 🗄️ SQL vs. NoSQL at Scale

## A Decision That Compounds at Real Scale

[SQL Fundamentals](../../../backend/sql-fundamentals/) and
[MongoDB Fundamentals](../../../backend/mongodb-fundamentals/), already covered in this
repository's Backend domain, taught the actual query languages and data modeling for each. At HLD
scale, the *choice between them* becomes a genuinely consequential architectural decision — one
that's often far more disruptive to change later than earlier in a system's life.

## The Core Trade-Offs, Verified

```
SQL:
  - RIGID schema, normalized tables - strong RELATIONAL integrity
  - STRICT ACID guarantees (Atomicity, Consistency, Isolation,
    Durability)
  - traditionally scales VERTICALLY (a bigger server)

NoSQL:
  - FLEXIBLE schema - key-value, document, or graph models
  - RELAXES some ACID guarantees in exchange for scale
  - designed to scale HORIZONTALLY across many servers, natively
```

Per AWS's own official comparison — this is the fundamental trade-off: SQL's strict guarantees
come with real scaling constraints; NoSQL's native horizontal scalability comes at the cost of some
of those same guarantees.

## When SQL Is the Right Choice at Scale

```
Genuinely strong candidates for SQL:
  - a system needing STRONG transactional consistency (a banking
    ledger, per REST API Design's own examples, earlier in this
    repository) - OLTP workloads
  - data with GENUINELY complex relationships needing real
    relational integrity
  - ANALYTICAL processing over structured, well-understood data
```

## When NoSQL Is the Right Choice at Scale

```
Genuinely strong candidates for NoSQL:
  - data with a RAPIDLY evolving or genuinely flexible schema
  - a NEED for horizontal scaling FAR beyond what a single,
    even large, server can handle
  - SEMI-structured or unstructured data (a URL Shortener's
    simple key-value lookups, for instance)
  - PERFORMANCE prioritized over strict, immediate consistency
```

## A Concrete Application: the URL Shortener

```
A URL Shortener's CORE data model - short_code -> long_url - is
genuinely a SIMPLE key-value lookup, with NO complex relational
queries needed at all. This is a GENUINELY strong fit for a
NoSQL key-value store, precisely matching AWS's own "flexible
schema, horizontal scale" NoSQL use case.
```

This directly applies the trade-offs above to the running example from
[capacity-estimation-basics.md](../system-design-foundations/capacity-estimation-basics.md), the
previous module — the 91 TB, multi-year storage estimate calculated there is exactly the kind of
scale that makes NoSQL's native horizontal scalability genuinely compelling for this specific
system.

## A Hybrid Approach Is Often the Real, Practical Answer

```
Per AWS's own guidance: "a hybrid approach is quite common" - a
REAL system often uses SQL for genuinely relational, transactional
data (user accounts, billing) and NoSQL for high-volume,
simpler-shaped data (the URL Shortener's actual redirect lookups)
- in the SAME overall system, simultaneously.
```

This is a genuinely important, practical corrective to treating this as a single, system-wide,
binary decision — real production systems frequently use *both*, choosing deliberately per
component based on that specific component's actual data shape and access pattern.

## Common Mistakes

- Treating SQL vs. NoSQL as a single, all-or-nothing decision for an entire system, rather than a
  choice made deliberately per component based on that component's genuine needs.
- Choosing NoSQL purely for its "scale" reputation without a genuine flexible-schema or
  horizontal-scaling need actually driving the decision.
- Choosing SQL out of familiarity for data that's genuinely simple, high-volume, and would benefit
  from NoSQL's native horizontal scaling.

## ➡️ Next

Continue to
[database-replication-and-sharding.md](database-replication-and-sharding.md) to see how either
database type actually scales beyond a single server.
