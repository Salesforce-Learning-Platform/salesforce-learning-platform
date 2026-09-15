# 🧩 Agent Design Patterns

## 📚 Overview

[Understanding AI Agents](../understanding-ai-agents/) established the basic agentic loop and the
discipline for when added complexity is actually justified. This module covers the recurring, named
patterns real agent systems build on top of that loop — planner-executor, researcher-writer,
critic-refiner, and routing — each directly grounded in Anthropic's own documented workflow
patterns (orchestrator-workers, prompt chaining, evaluator-optimizer, and routing).

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Implement a planner-executor (orchestrator-workers) split for tasks whose subtasks can't be
  predetermined.
- Design a researcher-writer handoff that avoids context pollution through a clean, purpose-built
  summary.
- Build a critic-refiner (evaluator-optimizer) loop using a genuinely separate evaluation call.
- Choose between plain `tool_choice: "auto"` routing and a dedicated router step for classifying
  and directing an incoming request.

## 📋 Prerequisites

- [Understanding AI Agents](../understanding-ai-agents/) — every pattern in this module builds directly on the agentic loop and "start simple" discipline from that module.
- [Function Calling and Tool Calling](../function-calling-tool-calling/) — forced tool use (`tool_choice`) is used throughout this module's critic and router examples.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [planner-to-executor-workflow.md](planner-to-executor-workflow.md) | Dynamic task decomposition and delegation (orchestrator-workers) |
| [researcher-to-writer-pattern.md](researcher-to-writer-pattern.md) | Sequential handoff (prompt chaining) separating research from prose |
| [critic-to-refiner-loop.md](critic-to-refiner-loop.md) | Iterative improvement via a genuinely separate evaluator (evaluator-optimizer) |
| [router-agents-that-decide-which-tool-to-call.md](router-agents-that-decide-which-tool-to-call.md) | Classifying and directing requests to specialized handling |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're designing any non-trivial agent feature — recognizing which named pattern
(if any) fits a given task is what separates a deliberate architecture from an ad hoc one.

**Skim** if your current agent need is simple enough that the basic agentic loop from
[Understanding AI Agents](../understanding-ai-agents/) already covers it without any of these
additional patterns.

## 🧠 Knowledge Check

<details>
<summary>Why does the critic-refiner loop use a genuinely separate LLM call for evaluation, rather than asking the same call to review its own work?</summary>

A model asked to review its own output tends to be lenient with itself, since it already committed
to the reasoning behind the original draft. A separate call, given only the draft and the task's
requirements, judges it more objectively — closer to how a fresh, independent reviewer would.

</details>

<details>
<summary>What's the key difference between the planner-executor pattern and simple parallelization?</summary>

In parallelization, the application already knows the fixed set of subtasks in advance. In the
planner-executor (orchestrator-workers) pattern, the set of subtasks is itself determined
dynamically, per request, by the planner — the decomposition is genuinely decided by the model, not
predetermined by the application.

</details>

## 📚 References

- [Anthropic Engineering - Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — the source of every named pattern in this module (prompt chaining, routing, orchestrator-workers, evaluator-optimizer)
- [Function Calling and Tool Calling: Letting AI Decide Which Function to Call](../function-calling-tool-calling/letting-ai-decide-which-function-to-call.md) — the `tool_choice` mechanics used throughout this module's examples

## ➡️ Continue Your Learning Path

Continue to [LangChain in Practice](../langchain-practical/) to see how a framework handles much of
this pattern implementation for you.
