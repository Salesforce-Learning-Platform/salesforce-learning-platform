# 🤖 Understanding AI Agents

## 📚 Overview

Every technique in this domain so far — even a [tool call](../function-calling-tool-calling/), even
a [RAG pipeline](../building-a-rag-pipeline/) — has followed a fixed, application-decided sequence
of steps. This module introduces a genuinely different shape: an **agent**, where the model itself
decides what to do next, repeatedly, based on its own reasoning about each tool result — and the
disciplined judgment for when this added complexity is actually worth it.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Distinguish a workflow (fixed, code-decided steps) from an agent (model-decided steps).
- Implement the agentic loop, correctly handling every `stop_reason` value and enforcing a firm
  iteration ceiling.
- Apply Anthropic's own "start simple, add complexity only when it demonstrably helps" guidance to
  decide when a single agent — or multiple, coordinating agents — is actually justified.

## 📋 Prerequisites

- [Function Calling and Tool Calling](../function-calling-tool-calling/) — the agentic loop is built directly on the `tool_use`/`tool_result` mechanism from this module.
- [Error Handling in AI Applications](../error-handling-in-ai-applications/) — the same retry/ceiling discipline applies to an agentic loop's iteration count.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [agent-vs-single-llm-call.md](agent-vs-single-llm-call.md) | Workflows (code-decided) vs. agents (model-decided), with a concrete side-by-side comparison |
| [agent-reasoning-and-tool-usage.md](agent-reasoning-and-tool-usage.md) | The agentic loop mechanism, `stop_reason` handling, and iteration ceilings |
| [when-to-use-multi-agent-systems-and-when-not-to.md](when-to-use-multi-agent-systems-and-when-not-to.md) | Anthropic's "start simple" guidance and a concrete decision checklist for multi-agent systems |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building any feature where the right sequence of actions genuinely can't be
known in advance — open-ended research, complex troubleshooting, multi-step problem solving.

**Skim** if your feature's steps are actually predictable and fixed — a plain workflow, per this
module's own guidance, is very often the better, simpler choice.

## 🧠 Knowledge Check

<details>
<summary>What's the precise technical difference between a workflow that calls an LLM and a genuine agent?</summary>

In a workflow, the application's code decides the sequence of steps in advance — an LLM call might
be one step, but the overall path is fixed. In an agent, the model itself dynamically directs its
own process and tool usage — the sequence of tool calls, and when to stop, is decided by the
model's own reasoning about each result, not predetermined by the application.

</details>

<details>
<summary>According to Anthropic's own guidance, when is added complexity (like a multi-agent system) actually justified?</summary>

Only when it demonstrably improves outcomes over a simpler approach that's actually been tried
first. The recommended path starts with a single, well-optimized LLM call, escalating to a
workflow, then a single agent, and only to multiple coordinating agents when a task genuinely
decomposes into distinct sub-problems and a simpler approach has measurably fallen short.

</details>

## 📚 References

- [Anthropic - How Tool Use Works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) — official documentation for the agentic loop and `stop_reason` handling
- [Anthropic Engineering - Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — the source of this module's "start simple" guidance and the workflows-vs-agents distinction

## ➡️ Continue Your Learning Path

Continue to [Agent Design Patterns](../agent-design-patterns/) to see the recurring, named patterns
— beyond the basic loop — that real agent implementations use.
