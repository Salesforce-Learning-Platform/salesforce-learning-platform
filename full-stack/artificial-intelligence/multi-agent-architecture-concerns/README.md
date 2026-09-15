# ⚖️ Multi-Agent Architecture Concerns

## 📚 Overview

[Understanding AI Agents](../understanding-ai-agents/) introduced the judgment call for when a
multi-agent system is worth its added complexity. This module makes that judgment concrete: the
real, ongoing costs of latency, operational spend, debugging difficulty, shared-state management,
and logging infrastructure that come with a genuine multi-agent or multi-service pipeline — and a
complete decision framework for when those costs are actually worth paying.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain why splitting a task into multiple agents usually increases total token cost and latency,
  and measure this rather than assume it.
- Diagnose which stage of a multi-agent pipeline is responsible for a failure, understanding how
  probabilistic errors compound across stages.
- Choose an appropriate shared-state strategy for a multi-service agent architecture.
- Design per-stage, run-linked logging that makes a multi-agent pipeline genuinely debuggable.
- Apply a complete decision framework for whether a multi-agent architecture is actually justified.

## 📋 Prerequisites

- [Understanding AI Agents](../understanding-ai-agents/) and [Agent Design Patterns](../agent-design-patterns/) — this module deepens the cost/complexity trade-offs introduced there.
- [Building a Multi-Agent Workflow](../building-a-multi-agent-workflow/) — concrete pipeline examples this module's concerns apply directly to.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [increased-latency-and-higher-operational-cost.md](increased-latency-and-higher-operational-cost.md) | Why more agents means more round trips and more total tokens, and how to measure it |
| [debugging-difficulty-across-agents.md](debugging-difficulty-across-agents.md) | Attributing failures to a specific stage, and compounding probabilistic error rates |
| [managing-shared-state-between-services.md](managing-shared-state-between-services.md) | Direct state passing vs. a shared store for multi-service agent architectures |
| [logging-every-step-of-the-pipeline.md](logging-every-step-of-the-pipeline.md) | Run-linked, per-stage logging as non-negotiable infrastructure |
| [understanding-that-multi-agent-systems-are-not-always-the-best-solution.md](understanding-that-multi-agent-systems-are-not-always-the-best-solution.md) | A complete decision framework, with worked "worth it" and "not worth it" examples |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** before committing any real project to a multi-agent architecture — every cost in this
module is real, ongoing, and easy to underestimate until it's actually been measured.

**Skim** if your current work uses a single agent or a fixed, simple workflow — return to this
module specifically when genuinely considering splitting into multiple coordinating agents.

## 🧠 Knowledge Check

<details>
<summary>If each stage of a three-stage pipeline is individually correct 95% of the time, why is the pipeline's actual end-to-end success rate lower than 95%?</summary>

Each stage's error is independent and probabilistic. If a pipeline requires every stage to succeed,
the combined success rate is closer to 0.95³ ≈ 86% — the individual stage failure rates compound
across the pipeline rather than the pipeline inheriting any single stage's own success rate.

</details>

<details>
<summary>Why does splitting a task into multiple specialized agents usually increase total token cost, even though each individual agent's context is smaller?</summary>

Each agent's own instructions are sent again on top of the shared task context, a clean handoff
summary between stages is additional generated content (not a reduction), and any added evaluator
or critic step is entirely additional generation. The total tokens processed across the whole
pipeline typically goes up, even as each individual call's context shrinks.

</details>

## 📚 References

- [Anthropic Engineering - Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — the source of this module's "add complexity only when it demonstrably improves outcomes" guidance
- [Backend: Caching - Local and Redis](../../backend/caching-local-and-redis/) — the shared-store patterns this module's shared-state guidance builds on

## ➡️ Continue Your Learning Path

Continue to [Engineering WITH AI](../engineering-with-ai/) to close out the Generative AI
Engineering domain with practices for using AI tools effectively in the development process itself.
