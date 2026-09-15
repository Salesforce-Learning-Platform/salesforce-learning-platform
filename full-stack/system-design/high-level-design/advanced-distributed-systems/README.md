# 🛡️ Advanced Distributed Systems Concepts

## 📚 Overview

Building on [Core Infrastructure](../core-infrastructure/), this module covers what keeps a real,
large distributed system reliable, observable, and secure: precisely measured availability and how
it multiplies across dependent services, fault tolerance techniques like the circuit breaker
pattern, distributed tracing and SLIs/SLOs/SLAs, rate limiting algorithms, authorization at
architecture scale, and the inverted-index foundations of search systems.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Calculate availability precisely and explain why dependent services' availability multiplies
  down.
- Apply the circuit breaker pattern and disciplined retries to design for expected, not
  exceptional, failure.
- Extend metrics/logs/traces across many services via distributed tracing, and distinguish
  SLIs, SLOs, and SLAs.
- Choose the right rate limiting algorithm (fixed window, sliding window, token bucket) for a
  given accuracy/burst-tolerance need.
- Explain the centralized-IdP, distributed-authorization pattern for microservices.
- Explain why full-text search requires an inverted index rather than a database scan.

## 📋 Prerequisites

- [Core Infrastructure](../core-infrastructure/) — this module covers the reliability, observability, and security concerns for the architecture built there.
- [Monitoring and Observability](../../../production-systems/monitoring-and-observability/) and [Web Security](../../../web-security/) — this module extends both to system-design scale.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [reliability-and-availability.md](reliability-and-availability.md) | The nines, and why dependent services' availability multiplies |
| [fault-tolerance-and-failure-handling.md](fault-tolerance-and-failure-handling.md) | The circuit breaker pattern, disciplined retries, redundancy, graceful degradation |
| [observability-at-scale.md](observability-at-scale.md) | Distributed tracing, consistent structured logging, SLIs/SLOs/SLAs |
| [rate-limiting.md](rate-limiting.md) | Fixed window, sliding window, and token bucket algorithms |
| [authorization-at-architecture-scale.md](authorization-at-architecture-scale.md) | Centralized IdP, distributed authorization, JWT propagation, OAuth2/OIDC |
| [designing-search-systems.md](designing-search-systems.md) | The inverted index and relevance scoring; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're operating any system with real availability requirements or multiple
services — every concept here addresses a genuine, common production concern.

**Skim** if you already have hands-on production reliability experience — but the availability-
multiplication math in
[reliability-and-availability.md](reliability-and-availability.md) is worth confirming even then,
since it's a commonly overlooked consequence of microservices architecture.

## 🧠 Knowledge Check

<details>
<summary>If a request depends on three services, each with 99.9% availability, why is the overall availability lower than 99.9%?</summary>

Dependent services' availability multiplies rather than simply flooring at the weakest link: 0.999 ×
0.999 × 0.999 ≈ 99.7%. Every additional service a request genuinely depends on compounds this
effect, which is why a system composed of many individually "reliable" services can have
surprisingly lower overall availability — directly relevant when deciding how many services a
single request should genuinely need to touch.

</details>

<details>
<summary>Why can't a traditional database efficiently power full-text search the way an inverted index does?</summary>

A database's indexes are built for exact-match or range lookups on specific columns. A `LIKE` query
searching for text within content requires scanning every row's full content and provides no
relevance ranking. An inverted index maps each term directly to the documents containing it, making
lookups fast, and enables scoring algorithms like BM25 to rank results by actual relevance.

</details>

## 📚 References

- [Better Stack - Availability Table](https://betterstack.com/community/guides/incident-management/availability-table/) — the nines and their corresponding downtime
- [GeeksforGeeks - Circuit Breaker Pattern](https://www.geeksforgeeks.org/system-design/what-is-circuit-breaker-pattern-in-microservices/) — the closed/open/half-open states
- [Microservices.io - Authorization Using JWT-Based Access Tokens](https://microservices.io/post/architecture/2025/07/22/microservices-authn-authz-part-3-jwt-authorization.html) — centralized IdP and distributed authorization pattern
- [Elastic Docs - How Full-Text Search Works](https://www.elastic.co/docs/solutions/search/full-text/how-full-text-works) — the inverted index and BM25 relevance scoring

## ➡️ Continue Your Learning Path

Continue to the Real-World System Design Problems module to apply every concept from this entire
domain to complete, interview-style worked examples.
