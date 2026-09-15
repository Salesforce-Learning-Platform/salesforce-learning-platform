# 🌐 What Is High-Level Design?

## Zooming Out From a Single Component

[Low-Level Design](../../low-level-design/), the previous domain, covered a single component's
internal class structure in real depth — a Parking Lot system's actual classes. **High-Level
Design (HLD)** zooms out entirely: designing an *entire system's* architecture — which services
exist, how they communicate, where data lives, and how the whole thing scales to real,
production-level traffic.

## The LLD/HLD Distinction, Restated at the Start of This Domain

```
LOW-LEVEL DESIGN → WITHIN one component: classes, their
  responsibilities, their relationships (per LLD Foundations,
  earlier in this repository)

HIGH-LEVEL DESIGN → ACROSS an entire system: which SERVICES exist,
  how they talk to each other, which DATABASE technology to use,
  how the system handles MILLIONS of users
```

This distinction was already introduced briefly in
[what-is-low-level-design.md](../../low-level-design/lld-foundations/what-is-low-level-design.md),
at the very start of the LLD domain — this file returns to it now that the vocabulary needed to
actually cover HLD in depth is fully established.

## A Concrete Comparison: Designing a URL Shortener

```
LLD question: "What CLASSES does the URL-encoding logic need, and
  how should THEY relate to each other?"

HLD question: "How many SERVERS does this need? Should URLs live
  in a SQL or NoSQL database? Does traffic need a CACHE in front
  of the database? How does the system stay available if ONE
  server goes down?"
```

Both questions are genuinely valid and important for the *same* real system — they simply operate
at entirely different levels of abstraction. This exact URL Shortener problem is covered as a
complete, worked example in the Real-World System Design Problems module, the final module in this
domain.

## Why HLD Matters, Even for Developers Who Don't Design Entire Systems

```
Understanding HLD helps ANY developer:
  - reason about WHY an existing system is architected the way it
    is
  - make BETTER decisions about where new code should actually
    live
  - communicate EFFECTIVELY with the infrastructure and platform
    engineers already covered throughout this repository's
    DevOps/Production Systems domain
```

This directly connects HLD to the [DevOps/Production Systems](../../../production-systems/) domain,
earlier in this repository — HLD is, in a genuine sense, the *design* discipline behind decisions
that domain's tools (Docker, load balancers, databases) actually implement and operate.

## What This Module Covers

```
This module → requirements, decomposition, capacity estimation,
  a step-by-step approach

Communication and Data Layer → networking, APIs, databases at scale

Core Infrastructure → caching, CDNs, load balancing, API gateways,
  message queues, microservices

Advanced Distributed Systems → reliability, fault tolerance,
  observability, rate limiting, authorization at scale, search

Real-World System Design Problems → complete worked examples
  applying everything
```

Each subsequent module in this domain builds directly on this one — establishing genuinely
foundational vocabulary and process before diving into specific architectural components.

## Common Mistakes

- Treating HLD as relevant only to senior architects, when understanding it genuinely improves
  decision-making at every level of a codebase.
- Confusing HLD and LLD as competing approaches rather than complementary levels of the same overall
  design process — a real system needs both.
- Jumping straight to specific technologies (a specific database, a specific message queue) before
  genuinely understanding the actual requirements those technology choices are meant to serve.

## ➡️ Next

Continue to
[functional-vs-non-functional-requirements.md](functional-vs-non-functional-requirements.md) to
see the first, essential step of any real HLD process.
