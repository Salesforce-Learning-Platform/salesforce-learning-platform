# 🧱 Core Infrastructure for Distributed Systems

## 📚 Overview

Building on [Communication and Data Layer](../communication-and-data-layer/), this module covers
the concrete infrastructure that makes a distributed system actually scale in production: caching
strategies, CDNs, load balancing algorithms, the API Gateway pattern, message queues for
asynchronous communication, and how every piece combines into a complete microservices
architecture.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Choose between cache-aside and write-through caching strategies based on a workload's actual
  read/write pattern.
- Explain how CDNs use Points of Presence and edge servers to reduce latency across geography.
- Choose the right load balancing algorithm (round robin, least connections, IP hash) for a given
  traffic pattern.
- Apply the API Gateway pattern as Facade applied at architecture scale.
- Use message queues to decouple services and smooth traffic spikes asynchronously.
- Explain the monolith-first principle and the genuine trade-offs of microservices.

## 📋 Prerequisites

- [System Design Foundations](../system-design-foundations/) and [Communication and Data Layer](../communication-and-data-layer/) — this module's infrastructure directly serves the requirements and data-layer decisions covered there.
- [Docker and Containerization](../../../production-systems/docker-and-containerization/) — the deployment mechanics behind independently deployable microservices.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [caching-strategies.md](caching-strategies.md) | Cache-aside vs. write-through, verified against AWS's official guidance |
| [cdns-and-content-delivery.md](cdns-and-content-delivery.md) | Points of Presence, edge servers, and what CDNs are best suited for |
| [load-balancing.md](load-balancing.md) | Round robin, least connections, and IP hash, with a decision framework |
| [api-gateway-pattern.md](api-gateway-pattern.md) | Facade applied at architecture scale, with a sequence diagram |
| [message-queues.md](message-queues.md) | Producer/queue/consumer, decoupling, and sync vs. async communication |
| [microservices-fundamentals.md](microservices-fundamentals.md) | The monolith-first principle and every prior file's piece combined; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're designing or operating any system beyond a single server — every piece of
infrastructure in this module addresses a genuine, common scaling need.

**Skim** if you're already comfortable with this infrastructure from hands-on production
experience — but the monolith-first principle in
[microservices-fundamentals.md](microservices-fundamentals.md) is worth confirming even then, since
it's commonly violated in practice.

## 🧠 Knowledge Check

<details>
<summary>Why is IP hash the right load balancing algorithm specifically for stateful applications, but often unnecessary for stateless ones?</summary>

IP hash consistently routes the same client's requests to the same server — valuable when a user's
session data lives on one particular server and needs that consistency. For a genuinely stateless
system, where any server can handle any request equally well, this consistency provides no real
benefit and only adds unnecessary rigidity compared to round robin or least connections.

</details>

<details>
<summary>According to the current architectural consensus, when should a team actually adopt microservices?</summary>

Only when a monolith's genuine coupling has become a real, demonstrated bottleneck — not
preemptively. This mirrors the same "start simple, add complexity only when it demonstrably helps"
principle already established for AI agent architectures earlier in this repository; microservices
solve real problems but at a real, ongoing operational cost that should be justified by an actual,
observed need.

</details>

## 📚 References

- [AWS - Caching Best Practices](https://aws.amazon.com/caching/best-practices/) — official guidance on cache-aside and write-through strategies
- [AWS - What Is a Message Queue?](https://aws.amazon.com/message-queue/) — official producer/queue/consumer model and real-world use case
- [Microservices.io - API Gateway Pattern](https://microservices.io/patterns/apigateway.html) — a widely-referenced explanation of the API Gateway pattern

## ➡️ Continue Your Learning Path

Continue to [Advanced Distributed Systems Concepts](../advanced-distributed-systems/) to see how a
system built on this infrastructure stays reliable, observable, and secure at real scale.
