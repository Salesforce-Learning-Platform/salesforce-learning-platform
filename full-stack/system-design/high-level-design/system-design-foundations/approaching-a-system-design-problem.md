# 🎯 A Step-by-Step Approach to Any System Design Problem

## A Repeatable Process, Named Explicitly

Every concept covered so far in this module — requirements, decomposition, estimation — follows a
genuine, repeatable sequence. This file names that sequence explicitly, directly paralleling
[approaching-machine-coding-problems.md](../../low-level-design/lld-problem-solving-and-machine-coding/approaching-machine-coding-problems.md)'s
six-step LLD process from the previous domain, now at system scale.

## The Four-Step HLD Process

```
1. CLARIFY requirements - functional AND non-functional (per
   functional-vs-non-functional-requirements.md)
2. ESTIMATE capacity - rough QPS, storage, bandwidth numbers (per
   capacity-estimation-basics.md)
3. DESIGN the high-level architecture - components, data flow (per
   breaking-systems-into-components.md)
4. DEEP-DIVE and IDENTIFY bottlenecks - pick 1-2 components to
   discuss in genuine depth, and discuss how the design scales
```

This is directly the same four-step structure widely referenced in resources like the System
Design Primer — a proven, repeatable sequence rather than an improvised, ad hoc approach invented
fresh for every new problem.

## Why This Order Genuinely Matters

```
Estimating capacity BEFORE designing architecture (step 2 before
step 3) means the architecture is shaped BY real numbers, rather
than numbers being retrofitted to JUSTIFY an already-chosen
design.
```

This ordering is a genuinely deliberate, important detail — reversing steps 2 and 3 risks designing
an architecture based on intuition alone, then cherry-picking numbers afterward to rationalize it,
rather than letting the actual estimated scale genuinely inform which architectural choices are
warranted.

## Time Management, Directly Paralleling the LLD Process

```
A common, PRACTICAL time allocation for a 45-60 minute HLD
interview:
  ~10 min: clarifying requirements (step 1)
  ~5 min: capacity estimation (step 2)
  ~15 min: high-level architecture (step 3)
  ~15-20 min: deep-diving 1-2 components, discussing bottlenecks
    and scaling (step 4)
  ~5 min: wrapping up, discussing trade-offs made
```

This directly mirrors the time-management guidance already established in
[approaching-machine-coding-problems.md](../../low-level-design/lld-problem-solving-and-machine-coding/approaching-machine-coding-problems.md)
from the LLD domain — the same practical lesson applies here: spending the entire available time on
one step (commonly, over-designing the initial architecture) at the expense of the deep-dive
discussion is a common, avoidable mistake.

## Choosing What to Deep-Dive Into

```
Genuinely worth asking: "which component, if POORLY designed,
would cause the SYSTEM to fail its non-functional requirements?"
- for a URL Shortener, likely the REDIRECT path (since it handles
  the VAST majority of real traffic) rather than the less
  frequently used creation path.
```

This is a genuinely practical, important judgment call — the deep-dive step shouldn't be chosen
arbitrarily; it should target whichever component most directly determines whether the system's
actual non-functional requirements (from step 1) are genuinely achievable.

## Common Mistakes

- Designing the high-level architecture before genuinely estimating capacity, risking numbers being
  retrofitted to justify an already-chosen design rather than informing it.
- Spending disproportionate time on the initial architecture sketch, leaving little time for the
  genuinely valuable deep-dive and bottleneck discussion.
- Choosing an arbitrary component to deep-dive into, rather than the one most likely to determine
  whether the system's actual requirements are achievable.

## Module Summary

Across this module: **High-Level Design** designs an entire system's architecture — services,
communication, data storage, scale — genuinely complementary to, not competing with, Low-Level
Design's component-internal focus (see
[what-is-high-level-design.md](what-is-high-level-design.md)); **functional and non-functional
requirements** split into what a system does versus how well it does it, with non-functional
requirements typically driving the real architectural complexity (see
[functional-vs-non-functional-requirements.md](functional-vs-non-functional-requirements.md));
**breaking systems into components** applies Single Responsibility at the service level, splitting
a system when genuinely different scaling needs or responsibilities justify the added complexity
(see [breaking-systems-into-components.md](breaking-systems-into-components.md)); **capacity
estimation** — rough QPS, storage, and bandwidth math, verified against widely-referenced latency
numbers and estimation techniques — validates whether a design genuinely holds up, aiming for
directional correctness rather than precision (see
[capacity-estimation-basics.md](capacity-estimation-basics.md)); and **a repeatable four-step
process** — clarify, estimate, design, deep-dive — ties every concept in this module together into
one practical, time-managed approach for any new system design problem.
