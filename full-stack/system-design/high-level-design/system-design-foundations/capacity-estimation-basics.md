# 🔢 Capacity Estimation Basics

## Putting Real Numbers Behind a Design

[breaking-systems-into-components.md](breaking-systems-into-components.md) produced a high-level
architecture. Capacity estimation ("back-of-envelope math") is what actually validates whether that
architecture genuinely holds up — a design that "sounds right" but was never checked against real,
estimated numbers can hide a genuine bottleneck until it's already live in production.

## Estimating QPS (Queries Per Second)

```
For a URL Shortener with 100 million URL creations per DAY:

100,000,000 / (24 * 60 * 60 seconds) ≈ 1,157 creates/second (AVERAGE)

Real traffic is NEVER perfectly even - a common, reasonable
assumption: PEAK traffic is roughly 2-3x the average.

Peak QPS ≈ 1,157 * 3 ≈ 3,500 creates/second
```

This is the standard technique from widely-referenced system design resources like the System
Design Primer: convert a daily number into a per-second average, then explicitly account for
realistic peak-vs-average variance — designing only for the average leaves the system genuinely
unable to handle real, predictable traffic spikes.

## Estimating Storage

```
100 million NEW URLs per day, each record roughly 500 bytes
(short URL + long URL + metadata):

100,000,000 * 500 bytes ≈ 50 GB / day

Over 5 YEARS: 50 GB * 365 * 5 ≈ 91 TB
```

This kind of multi-year projection directly informs a real, consequential decision:
[SQL vs. NoSQL at Scale](../communication-and-data-layer/sql-vs-nosql-at-scale.md), covered next in
this domain, depends significantly on whether a dataset's genuine long-term scale fits comfortably
on a single, traditional database server or genuinely requires horizontal distribution from the
start.

## Estimating Bandwidth

```
3,500 redirects/second (assume REDIRECT traffic is ~100x CREATE
traffic, a realistic assumption for this kind of system) * 500
bytes per response:

3,500 * 100 * 500 bytes ≈ 175 MB/second
```

This directly informs whether a single server's network interface could genuinely handle this load
alone, or whether load balancing — covered in the Core Infrastructure module, later in this domain
— is a genuine architectural necessity rather than a "nice to have."

## Latency Numbers Every Programmer Should Know

```
L1 cache reference:              0.5 ns
Main memory reference:           100 ns
Read 4 KB randomly from SSD:     150,000 ns (150 μs)
Read 1 MB sequentially from SSD: 1,000,000 ns (1 ms)
Round trip within same datacenter: 500,000 ns (500 μs)
```

This widely-referenced list (originating from Jeff Dean and Peter Norvig, popularized through
resources like the System Design Primer) isn't meant to be memorized precisely — hardware numbers
genuinely change over time — but the *relative* magnitude matters enormously: a database query
hitting disk is genuinely orders of magnitude slower than one served from an in-memory cache,
which is exactly the practical justification behind caching, covered in the Core Infrastructure
module later in this domain.

## Why Rough Estimates Are Genuinely Sufficient

```
The GOAL of capacity estimation isn't a PRECISE number - it's
identifying, EARLY, whether a design is off by an ORDER OF
MAGNITUDE (needing 10 servers vs. needing 10,000) - a rough,
quick estimate is genuinely enough to catch THAT kind of mistake.
```

This is a genuinely practical, important framing — capacity estimation in a real design discussion
(or interview) doesn't need to be perfectly precise; it needs to be *directionally correct enough*
to catch a genuinely wrong architectural assumption before it's built.

## Common Mistakes

- Estimating only average load, missing the realistic peak-vs-average variance that real traffic
  patterns actually exhibit.
- Treating a rough back-of-envelope estimate as requiring perfect precision, spending disproportionate
  time on decimal-level accuracy that doesn't actually change the architectural conclusion.
- Skipping capacity estimation entirely, discovering a genuine order-of-magnitude scaling problem
  only after the system is already built and live.

## ➡️ Next

Continue to
[approaching-a-system-design-problem.md](approaching-a-system-design-problem.md) to bring
requirements, decomposition, and estimation together into one complete, repeatable process.
