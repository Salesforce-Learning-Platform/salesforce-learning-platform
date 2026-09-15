# 🔭 What Is Observability?

## Knowing an Application Deployed Successfully Isn't Enough

[CI/CD Pipelines](../ci-cd-pipelines/), the previous module, covered getting code deployed reliably.
But a successful deployment only confirms code is *running* — it says nothing about whether that
running application is actually healthy, fast, or serving users correctly, right now, in production.
**Observability** is the practice of answering exactly that ongoing question.

## Monitoring vs. Observability — a Real Distinction

```
MONITORING: watching a set of PREDEFINED signals - "is CPU usage
  above 80%?", "did this endpoint return a 500?" - answers
  questions you already thought to ask in advance

OBSERVABILITY: having ENOUGH detailed, structured data about a
  system that you can answer questions you DIDN'T think to ask in
  advance, while actually investigating a real problem
```

This distinction genuinely matters: monitoring is reactive to *known* failure modes; observability
is what lets an engineer investigate a *novel*, unanticipated problem by exploring the system's
actual real behavior, rather than being limited to whatever dashboards were pre-built.

## The Three Pillars: Metrics, Logs, and Traces

```
METRICS → numerical measurements over time (request count, error
          rate, latency) - covered in metrics.md, next in this
          module

LOGS    → discrete, timestamped events with detail (a specific
          error, a specific request) - directly building on
          Logging in Production, the next module in this domain

TRACES  → the path of ONE request as it flows through multiple
          services - directly the same idea as
          logging-every-step-of-the-pipeline.md's pipeline-run-ID
          tracing, already covered earlier in this repository for
          multi-agent AI pipelines
```

These three pillars are complementary, not competing — a real production incident is typically
investigated using all three together: metrics reveal *that* something is wrong (an error rate
spike), traces reveal *where* in a multi-service request it's happening, and logs reveal the
specific *detail* of what actually went wrong at that point.

## Why This Matters More as Systems Grow More Complex

```
A SINGLE server running ONE application: "is it working?" is a
  simple question to answer by directly checking it

MULTIPLE services, behind a reverse proxy, across MULTIPLE cloud
  instances: "is it working?" requires observability tooling -
  no human can manually check every piece at once
```

This is directly the same complexity-driven need already established in
[debugging-difficulty-across-agents.md](../../artificial-intelligence/multi-agent-architecture-concerns/debugging-difficulty-across-agents.md) —
a system with more moving pieces genuinely needs more deliberate infrastructure just to remain
understandable, and observability tooling is that infrastructure at the production-systems level.

## Common Mistakes

- Treating "we have a dashboard" as equivalent to "we have observability" — a small set of
  pre-built dashboards only answers the specific questions someone thought to build them for.
- Adding observability tooling only after a serious incident already happened, rather than as a
  standard, built-in part of shipping any production system.
- Confusing monitoring (watching known signals) with observability (the ability to investigate
  genuinely unknown problems) as though they were the same thing.

## ➡️ Next

Continue to [application-monitoring.md](application-monitoring.md) to see what's actually watched
day-to-day for a running application's health.
