# 📋 Functional vs. Non-Functional Requirements

## The Same Discipline, at System Scale

[requirement-analysis.md](../../low-level-design/lld-problem-solving-and-machine-coding/requirement-analysis.md),
from the LLD domain, already established that requirements come before design. At the HLD level,
this becomes genuinely more structured: requirements split explicitly into two categories that
shape architecture in fundamentally different ways.

## Functional Requirements: What the System Must Do

```
For a URL Shortener:
  - a user can submit a long URL and receive a SHORT one
  - visiting the short URL REDIRECTS to the original long URL
  - a user can (optionally) set a CUSTOM alias
  - a shortened URL can EXPIRE after a set time
```

Functional requirements describe genuine, observable *behavior* — the specific things the system
must actually do, from a user's or another system's perspective.

## Non-Functional Requirements: How Well the System Must Do It

```
For the SAME URL Shortener:
  - AVAILABILITY: the redirect must work 99.99% of the time
  - LATENCY: a redirect must genuinely happen in under 100ms
  - SCALE: the system must handle 100 million URL creations per
    day, and REDIRECT traffic roughly 100x that
  - CONSISTENCY: is it acceptable for a NEWLY created short URL to
    take a few seconds to become available everywhere? (covered in
    depth in Consistency vs. Performance Tradeoffs, the next
    module in this domain)
```

Non-functional requirements describe *qualities* of the system's behavior — and these are
genuinely what drive most of the actual architectural decisions in HLD: a system needing 99.99%
availability requires fundamentally different architecture than one where occasional downtime is
acceptable.

## Why Non-Functional Requirements Drive Architecture More Than Functional Ones

```
Functional requirement "redirect a short URL to its original" can
be satisfied by a TRIVIAL single-server implementation.

The NON-FUNCTIONAL requirements - handling millions of requests
per DAY, sub-100ms latency, 99.99% availability - are what
ACTUALLY require a load balancer, a cache, database replication,
and every other architectural component covered later in this
domain.
```

This is a genuinely important, often underappreciated insight: the *functional* requirements of
many real systems are often surprisingly simple — it's the *non-functional* requirements that
demand genuine architectural sophistication.

## Prioritizing Requirements: Not Everything Can Be Optimized at Once

```
A system CANNOT simultaneously optimize for EVERY non-functional
requirement at maximum level - genuine trade-offs exist (covered
directly in Consistency vs. Performance Tradeoffs, next in this
domain) - a real design process REQUIRES explicitly prioritizing
which qualities matter MOST for THIS specific system.
```

For a banking transaction system, consistency likely outweighs raw latency; for a social media
feed, the reverse is often true — there's no universally "correct" priority order, only the order
that's genuinely appropriate for a *specific* system's actual, real needs.

## A Practical Requirements Checklist for Any HLD Problem

```
FUNCTIONAL:
☐ What are the CORE user-facing actions?
☐ What's explicitly OUT of scope, for now?

NON-FUNCTIONAL:
☐ What SCALE (users, requests/second, data volume)?
☐ What AVAILABILITY target?
☐ What LATENCY target?
☐ Is STRONG or EVENTUAL consistency acceptable?
```

## Common Mistakes

- Spending most of a design discussion on functional requirements alone, when non-functional
  requirements are typically what actually drives the architecture's real complexity.
- Assuming every non-functional requirement can be maximized simultaneously, without acknowledging
  the genuine trade-offs between them.
- Never explicitly asking about scale, treating "handle real traffic" as an assumption rather than
  a number worth pinning down.

## ➡️ Next

Continue to
[breaking-systems-into-components.md](breaking-systems-into-components.md) to see how these
requirements actually translate into a system's real architectural pieces.
