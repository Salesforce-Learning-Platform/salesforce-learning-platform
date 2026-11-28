# 🏗️ System Design

## 📚 Overview

System design is covered at two levels. Low-level design is how to structure the classes inside one component: class relationships, the SOLID principles, design patterns, and a complete machine-coding example. High-level design is how a whole system fits together: requirements, data, infrastructure, reliability, and worked design problems. Start with low-level design, because high-level design builds on it.

## 🧭 The Learning Path

Work through the modules in this order. The last column names the earlier modules each one relies on, so you can also start partway through; links point to modules in other areas.

### 🧱 Low-Level Design

| # | Module | What it covers | Builds on |
|---|--------|----------------|-----------|
| 1 | [LLD Foundations](low-level-design/lld-foundations/README.md) | Objects and classes, class relationships, UML diagrams, and interface design | Basic object-oriented programming |
| 2 | [SOLID Principles](low-level-design/solid-principles/README.md) | The five SOLID principles, each with a before-and-after example | LLD Foundations |
| 3 | [Creational Design Patterns](low-level-design/creational-design-patterns/README.md) | Singleton, Factory Method, Abstract Factory, Builder, and Prototype | SOLID Principles |
| 4 | [Structural Design Patterns](low-level-design/structural-design-patterns/README.md) | Adapter, Facade, Proxy, Decorator, and Composite | Creational Design Patterns, SOLID Principles |
| 5 | [Behavioral Design Patterns](low-level-design/behavioral-design-patterns/README.md) | Observer, Strategy, State, Command, and Template Method | Creational Design Patterns, Structural Design Patterns, SOLID Principles |
| 6 | [LLD Problem Solving and Machine Coding](low-level-design/lld-problem-solving-and-machine-coding/README.md) | A parking lot designed from requirements to tests, and a repeatable process | All the low-level design modules above |

### 🌐 High-Level Design

| # | Module | What it covers | Builds on |
|---|--------|----------------|-----------|
| 7 | [System Design Foundations (HLD)](high-level-design/system-design-foundations/README.md) | Requirements, components, capacity estimates, and a four-step approach | Low-level design (above) |
| 8 | [Communication and Data Layer](high-level-design/communication-and-data-layer/README.md) | Networking, API design at scale, SQL or NoSQL, replication, sharding, and CAP | HLD Foundations, [REST API Design](../backend/rest-api-design/README.md), [SQL](../backend/sql-fundamentals/README.md), [MongoDB](../backend/mongodb-fundamentals/README.md) |
| 9 | [Core Infrastructure for Distributed Systems](high-level-design/core-infrastructure/README.md) | Caching, CDNs, load balancing, API gateways, message queues, and microservices | HLD Foundations, Communication and Data, [Docker](../production-systems/docker-and-containerization/README.md) |
| 10 | [Advanced Distributed Systems Concepts](high-level-design/advanced-distributed-systems/README.md) | Availability, fault tolerance, tracing and service levels, rate limiting, authorization, and search | Core Infrastructure, [Monitoring and Observability](../production-systems/monitoring-and-observability/README.md), [Web Security](../web-security/README.md) |
| 11 | [Real-World System Design Problems](high-level-design/real-world-system-design-problems/README.md) | A URL shortener, a rate limiter, and a notification system, designed end to end | All the high-level design modules above |

## ➡️ Start Here

Begin with [LLD Foundations](low-level-design/lld-foundations/README.md). After the last module, the course continues with [Data Structures and Algorithms](../data-structures-and-algorithms/README.md).
