# 🌐 System Design Foundations (HLD)

## 📚 Overview

This module opens the High-Level Design domain, zooming out from
[Low-Level Design](../../low-level-design/)'s single-component focus to an entire system's
architecture. It covers what HLD actually is, how functional and non-functional requirements shape
architecture differently, how to break a system into genuine components, back-of-envelope capacity
estimation, and a repeatable four-step process for approaching any new system design problem.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Distinguish High-Level Design from Low-Level Design, and explain why both matter.
- Separate functional from non-functional requirements, and explain why the latter typically
  drives architectural complexity.
- Apply Single Responsibility at the service level to identify genuine component boundaries.
- Perform rough capacity estimation (QPS, storage, bandwidth) to validate a design's feasibility.
- Follow a repeatable four-step process — clarify, estimate, design, deep-dive — for any system
  design problem.

## 📋 Prerequisites

- [Low-Level Design](../../low-level-design/) — this module directly extends its requirements-analysis and Single-Responsibility concepts to system scale.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-high-level-design.md](what-is-high-level-design.md) | HLD vs. LLD, with a concrete URL Shortener comparison |
| [functional-vs-non-functional-requirements.md](functional-vs-non-functional-requirements.md) | What a system does vs. how well it does it, and why the latter drives architecture |
| [breaking-systems-into-components.md](breaking-systems-into-components.md) | Single Responsibility applied at the service level, with a Mermaid architecture diagram |
| [capacity-estimation-basics.md](capacity-estimation-basics.md) | QPS/storage/bandwidth math, and the widely-referenced latency numbers every programmer should know |
| [approaching-a-system-design-problem.md](approaching-a-system-design-problem.md) | A repeatable four-step process with practical interview time management; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** regardless of experience level — this module establishes the vocabulary and process
every later module in this domain assumes throughout.

**Skim** if you already have real system design interview or architecture experience — but the
capacity estimation file's order-of-magnitude framing is worth a look even then, since it's easy to
over-invest in precision that doesn't actually change the architectural conclusion.

## 🧠 Knowledge Check

<details>
<summary>Why do non-functional requirements typically drive a system's architectural complexity more than functional requirements?</summary>

A system's core functional behavior (like redirecting a short URL to its original) is often
satisfiable with a trivial, single-server implementation. It's the non-functional requirements —
handling millions of requests, sub-100ms latency, 99.99% availability — that actually demand load
balancers, caches, database replication, and every other architectural component covered later in
this domain.

</details>

<details>
<summary>Why does capacity estimation come before high-level architecture design in the recommended four-step process, rather than after?</summary>

Estimating first means the architecture is shaped by real, even if rough, numbers. Reversing the
order risks designing an architecture based on intuition alone, then retroactively finding numbers
to justify it — rather than letting the actual estimated scale genuinely inform which architectural
choices are warranted.

</details>

## 📚 References

- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer) — a widely-referenced resource for capacity estimation technique and the four-step system design approach
- [Latency Numbers Every Programmer Should Know (Gist)](https://gist.github.com/jboner/2841832) — the original, widely-cited latency reference list

## ➡️ Continue Your Learning Path

Continue to [Communication and Data Layer](../communication-and-data-layer/) to see how components
like these actually talk to each other and store data at scale.
