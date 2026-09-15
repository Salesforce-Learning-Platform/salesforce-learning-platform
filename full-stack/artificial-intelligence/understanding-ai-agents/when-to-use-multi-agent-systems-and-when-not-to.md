# ⚖️ When to Use Multi-Agent Systems — and When Not To

## The Core Recommendation: Start Simple

```
Anthropic's own guidance on building effective agents:

"Find the simplest solution possible, and only increase complexity
when needed... you should consider adding complexity ONLY when it
demonstrably improves outcomes."
```

This is the single most important idea in this file, stated directly by Anthropic's own engineering
guidance: the natural pull toward building something sophisticated — multiple coordinating agents,
elaborate orchestration — should be resisted until a genuinely simpler approach has actually been
tried and shown to fall short.

## The Escalation Path, in Order

```
1. A single, well-optimized LLM call (with good retrieval/examples)
2. A workflow — fixed code paths, with LLM calls as steps
3. A single agent — one model directing its own tool usage
4. MULTIPLE agents, coordinating — the most complex, most
   expensive option, reserved for when 1-3 genuinely aren't enough
```

Each step up this path adds real cost — more tokens, more latency, more ways for something to go
wrong, more surface area to test and debug. Multi-agent systems sit at the very top of this
escalation path, not as a default starting point.

## When a Single Agent Genuinely Isn't Enough

```
A single agent handling "research a topic AND write a polished
report AND fact-check every claim" all in one context:
  → the context grows huge and unfocused, and the model has to
    context-switch between genuinely different KINDS of work
    within the same reasoning trace

Splitting into SEPARATE agents — a researcher, a writer, a fact-
checker, each with its OWN focused context and tools:
  → each agent's context stays focused on ONE kind of work
```

Multi-agent systems earn their complexity specifically when a task genuinely decomposes into
distinct sub-problems that each benefit from their own focused context, their own specialized tools,
or even their own separate conversation history — not merely because a task feels large.

## A Concrete Signal: Context Pollution

```
One agent, one long conversation, doing research AND writing:
  → by the time it's writing the final report, the context is full
    of raw research notes, search results, and intermediate
    reasoning that has nothing to do with prose quality

Two agents: a research agent hands off a CLEAN summary to a
separate writing agent, which never sees the raw research noise
```

A genuinely useful, concrete signal for reaching for multiple agents: if a single agent's context
is filling up with information that's relevant to *one* part of the task but actively distracting
for another part, splitting into separate agents with a clean handoff between them is often the
right fix.

## The Real Costs of Going Multi-Agent

```
Cost:      MORE total tokens (each agent has its own context and
           overhead)
Latency:   coordination between agents adds real round trips
Complexity: debugging WHICH agent made a wrong decision, and WHY,
           is genuinely harder with more moving pieces
```

These costs are real and compound — this is exactly why Anthropic's own guidance frames added
complexity as something to justify with measured, demonstrated improvement, not something to add on
the assumption that "more agents" means "better results."

## A Simple Decision Checklist

```
Does the task genuinely decompose into distinct sub-problems?  → maybe
Would each sub-problem benefit from its OWN focused context?    → maybe
Has a SIMPLER approach (single agent, workflow) actually been
  tried and shown to fall short?                                 → REQUIRED
Is the added cost/latency/complexity justified by a MEASURED
  improvement, not just an assumption?                           → REQUIRED
```

The two "required" questions matter most — reaching for multiple agents without first trying (and
measuring) a simpler approach is exactly the premature complexity Anthropic's own guidance warns
against.

## Common Mistakes

- Designing a multi-agent system from the very start of a project, before a single agent or plain
  workflow has even been tried and measured.
- Splitting agents along lines that don't actually reduce context pollution or add genuine
  specialization, just adding coordination overhead for no real benefit.
- Underestimating the debugging difficulty of a multi-agent system, where a wrong final result can
  originate from any one of several agents' decisions.

## Module Summary

Across this module: **an agent** is a genuinely different shape from a workflow — the model itself
directs its own sequence of actions, rather than the application dictating a fixed sequence in
advance (see [agent-vs-single-llm-call.md](agent-vs-single-llm-call.md)); **the agentic loop** —
keyed on `stop_reason == "tool_use"`, always behind a firm iteration ceiling — is the concrete
mechanism that lets a model reason about each tool result and decide what to do next (see
[agent-reasoning-and-tool-usage.md](agent-reasoning-and-tool-usage.md)); and **multi-agent
systems** are the most expensive, most complex option on an escalation path that should start with
a single, well-optimized LLM call, earning their added cost only when a task genuinely decomposes
into distinct sub-problems and a simpler approach has already been tried and measurably fallen
short.
