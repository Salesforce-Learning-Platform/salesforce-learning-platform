# 🔌 Communication and Data Layer

## 📚 Overview

Building on [System Design Foundations](../system-design-foundations/), this module covers how
components actually communicate and store data at real scale: networking fundamentals underlying
every service boundary, designing REST APIs for a multi-consumer system, choosing between SQL and
NoSQL, scaling databases through replication and sharding, and the CAP theorem framework for
reasoning about the consistency-vs-availability trade-off every distributed system genuinely faces.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain how HTTP, TCP, and DNS apply to service-to-service communication, and why latency
  compounds across service boundaries.
- Design REST APIs with versioning, idempotency, and appropriate sync/async shape for
  system-level consumption.
- Choose deliberately between SQL and NoSQL per component, rather than as a single system-wide
  decision.
- Apply replication and sharding as complementary database scaling techniques, with their
  respective trade-offs.
- Apply the CAP theorem to reason concretely about consistency vs. availability, per piece of data.

## 📋 Prerequisites

- [System Design Foundations](../system-design-foundations/) — this module's examples continue the URL Shortener running example established there.
- [REST API Design](../../../backend/rest-api-design/), [SQL Fundamentals](../../../backend/sql-fundamentals/), and [MongoDB Fundamentals](../../../backend/mongodb-fundamentals/) — this module extends each to system scale.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [networking-basics-for-system-design.md](networking-basics-for-system-design.md) | HTTP/TCP/DNS applied to service-to-service communication and compounding latency |
| [designing-rest-apis-at-scale.md](designing-rest-apis-at-scale.md) | Versioning, idempotency, pagination, rate limiting, sync vs. async |
| [sql-vs-nosql-at-scale.md](sql-vs-nosql-at-scale.md) | The real trade-offs, verified against AWS's official comparison, and hybrid approaches |
| [database-replication-and-sharding.md](database-replication-and-sharding.md) | Distributing reads vs. distributing the dataset itself |
| [consistency-vs-performance-tradeoffs.md](consistency-vs-performance-tradeoffs.md) | The CAP theorem, applied per piece of data; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're designing any system spanning multiple services or needing to scale beyond
a single database server — every concept here is a genuine, common architectural decision point.

**Skim** if you're already comfortable reasoning about CAP trade-offs and database scaling — but
the REST-APIs-at-scale file's idempotency coverage is worth a look even then, since it's commonly
under-implemented in practice.

## 🧠 Knowledge Check

<details>
<summary>Why does the CAP theorem force a real, unavoidable choice between consistency and availability specifically during a network partition?</summary>

Because real networks do experience partitions, a distributed system must tolerate them (partition
tolerance isn't optional). During an actual partition, a node can either refuse to answer with
possibly-stale data (choosing consistency) or answer anyway with what it currently has (choosing
availability) — it genuinely cannot do both at once for that request.

</details>

<details>
<summary>Why might a system choose SQL for one component and NoSQL for another, rather than one database technology for the entire system?</summary>

Different components often have genuinely different data shapes and access patterns — a component
needing strong relational integrity and transactional consistency (like billing) is a strong SQL
fit, while a component with simple, high-volume, flexible-schema data (like a URL Shortener's
key-value lookups) is a strong NoSQL fit. A hybrid approach, chosen deliberately per component, is
genuinely common in real production systems.

</details>

## 📚 References

- [AWS - NoSQL Databases](https://aws.amazon.com/nosql/) — official comparison of SQL and NoSQL trade-offs
- [PingCAP - Understanding CAP Theorem Basics](https://www.pingcap.com/article/understanding-cap-theorem-basics-in-distributed-systems/) — a widely-referenced explanation of the CAP theorem and CA/CP/AP system examples

## ➡️ Continue Your Learning Path

Continue to the Core Infrastructure module to see the caching, load balancing, and messaging
infrastructure that makes systems like these genuinely scale in production.
