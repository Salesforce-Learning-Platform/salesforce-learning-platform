# ⚖️ Understanding That Multi-Agent Systems Are Not Always the Best Solution

## Bringing Every Cost Together

This module has covered four genuine, concrete costs of a multi-agent architecture: added
[latency and operational cost](increased-latency-and-higher-operational-cost.md), harder
[debugging](debugging-difficulty-across-agents.md), added
[shared-state complexity](managing-shared-state-between-services.md), and the
[non-negotiable logging infrastructure](logging-every-step-of-the-pipeline.md) needed just to make
the system operable. None of these costs are hypothetical — every one of them shows up in a real,
production multi-agent system.

## The Anthropic Guidance, Restated With Full Context

```
"Find the simplest solution possible, and only increase complexity
when needed... you should consider adding complexity ONLY when it
demonstrably improves outcomes."
```

[when-to-use-multi-agent-systems-and-when-not-to.md](../understanding-ai-agents/when-to-use-multi-agent-systems-and-when-not-to.md)
introduced this principle before this module's costs were fully explored. Now, with latency, cost,
debugging difficulty, state management, and logging infrastructure all made concrete, this
guidance reads less like caution and more like a genuinely quantified trade-off: every one of these
costs is real, measurable, and ongoing — not a one-time setup tax.

## A Complete Decision Framework

```
1. Has a SINGLE, well-optimized LLM call actually been tried?
2. Has a SINGLE AGENT (with tools) actually been tried?
3. Does the task GENUINELY decompose into distinct sub-problems,
   each needing its own focused context (per the context-pollution
   signal from Understanding AI Agents)?
4. Is the team prepared to build and maintain: per-stage logging,
   shared-state management (if multi-service), and debugging
   tooling for a genuinely distributed system?
5. Has the improvement from splitting into multiple agents been
   MEASURED (per increased-latency-and-higher-operational-cost.md),
   not just assumed?
```

Questions 1–2 should genuinely be answered "yes, and it wasn't enough" before questions 3–5 even
apply. This ordering matters: a multi-agent system is the answer to "a simpler approach was tried
and measurably fell short," never the default starting architecture.

## A Realistic Example of "Not Worth It"

```
Task: "Summarize this support ticket and suggest a response."

Multi-agent version: a summarizer agent, then a response-drafter
  agent, then a critic agent reviewing the draft
  → 3x the latency, 3x+ the token cost, a genuinely harder system
    to debug and log

Single-agent (or even single-call) version: one well-crafted
  prompt asking for BOTH a summary and a suggested response in
  one structured response
  → almost certainly just as good, for a fraction of the cost
    and complexity
```

For a task this straightforward, every cost covered in this module is being paid for essentially no
quality benefit — this is exactly the scenario Anthropic's "start simple" guidance is warning
against, made concrete with this module's specific costs attached.

## A Realistic Example of "Worth It"

```
Task: "Research a complex, multi-faceted topic from several
angles, write a polished long-form report, and have it reviewed
against explicit quality criteria before publishing."

Here: the researcher's context would genuinely balloon with
  research noise if combined with writing; the critic's review is
  genuinely a distinct skill from either; the added latency and
  cost are worth it for a report that will actually be published
  and read
```

The difference isn't the *presence* of multiple steps — it's whether those steps genuinely need
separate, focused contexts and specialized handling badly enough to justify this module's very real
costs.

## Module Summary

Across this module: **latency and operational cost** increase with every agent boundary — more
round trips, more total tokens processed across the pipeline, not less — and should be measured,
not assumed (see
[increased-latency-and-higher-operational-cost.md](increased-latency-and-higher-operational-cost.md));
**debugging difficulty** compounds because a wrong final result could originate from any stage, and
because each stage's own probabilistic nature multiplies across the pipeline's end-to-end failure
rate (see [debugging-difficulty-across-agents.md](debugging-difficulty-across-agents.md));
**shared state** between separately-deployed agent services needs deliberate design — direct
request passing for simple pipelines, a shared persistent store for more complex coordination — with
real distributed-systems concerns like race conditions (see
[managing-shared-state-between-services.md](managing-shared-state-between-services.md));
**per-stage, run-linked logging** is non-negotiable infrastructure, not an optional nicety, for
making a multi-stage pipeline's failures genuinely diagnosable (see
[logging-every-step-of-the-pipeline.md](logging-every-step-of-the-pipeline.md)); and, tying it all
together, **a multi-agent architecture earns its very real, ongoing costs only when a simpler
approach has actually been tried and measurably fallen short** — never as a default starting
architecture.
