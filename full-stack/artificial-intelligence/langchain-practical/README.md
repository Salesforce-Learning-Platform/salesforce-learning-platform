# 🦜 LangChain in Practice

## 📚 Overview

Every module so far in this domain has been built directly on the Anthropic Messages API. LangChain
is a framework that packages the patterns already covered — prompt templates, chains, tool-calling
agents, memory — into reusable, composable abstractions. Because this module comes after
[Understanding AI Agents](../understanding-ai-agents/) and
[Agent Design Patterns](../agent-design-patterns/), every LangChain concept here maps directly onto
something already understood from first principles.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Connect LangChain to Claude via `langchain-anthropic`, and build reusable prompt templates.
- Compose chains with the `|` operator, combining a prompt, a model, and an output parser.
- Define tools with `@tool` and attach persistent, session-based memory with
  `RunnableWithMessageHistory`.
- Build and run an agent with `create_agent`, understanding it as "Model + Harness."
- Explain the `Runnable` interface behind LCEL, and why it gives every chain streaming and batching
  for free.

## 📋 Prerequisites

- [Understanding AI Agents](../understanding-ai-agents/) and [Agent Design Patterns](../agent-design-patterns/) — every LangChain abstraction in this module maps to a concept covered in these two modules first.
- [Function Calling and Tool Calling](../function-calling-tool-calling/) — `@tool` and `bind_tools()` wrap the same underlying contract.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [introduction-to-langchain.md](introduction-to-langchain.md) | What LangChain is, installation, and when the framework is (and isn't) worth it |
| [building-chains-and-prompt-templates.md](building-chains-and-prompt-templates.md) | `ChatPromptTemplate`, the `\|` operator, and output parsers |
| [using-tools-and-memory-modules.md](using-tools-and-memory-modules.md) | `@tool`, `bind_tools()`, and `RunnableWithMessageHistory` |
| [working-with-agents.md](working-with-agents.md) | `create_agent`, reading full conversation history, and checkpointed multi-turn state |
| [overview-of-lcel-concepts.md](overview-of-lcel-concepts.md) | The `Runnable` interface, `RunnableParallel`, `RunnableLambda`, and why LCEL matters |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if your project will genuinely use several of these abstractions together — chains,
agents, and memory combined — where LangChain's consistency and ecosystem save real, ongoing
effort.

**Skim** if you mainly wanted to confirm how LangChain's concepts map onto the direct-API knowledge
already built throughout this domain, without adopting the framework itself yet.

## 🧠 Knowledge Check

<details>
<summary>Why does this module come after Understanding AI Agents and Agent Design Patterns, rather than before them?</summary>

LangChain's abstractions — chains, agents, memory — are genuinely easier to use correctly, and to
debug when something misbehaves, once the underlying mechanism (the agentic loop, prompt
structure, tool-calling contract) is already well understood. Learning the framework first would
make its abstractions feel like unexplained magic.

</details>

<details>
<summary>What makes the <code>|</code> operator work for composing a prompt, a model, and an output parser into a chain?</summary>

Every LangChain component that can appear in a chain implements the same `Runnable` interface
(`.invoke()`, `.stream()`, `.batch()`). Python's `__or__` method is overloaded so that `a | b`
produces a new `Runnable` that calls `a`, then passes its output as `b`'s input — this uniform
interface is also why every LCEL chain gets streaming and batching for free.

</details>

## 📚 References

- [LangChain - Overview](https://docs.langchain.com/oss/python/langchain/overview) — official documentation for `create_agent` and LangChain's core building blocks
- [Pinecone - LangChain Expression Language](https://www.pinecone.io/learn/series/langchain/langchain-expression-language/) — a well-known, detailed explanation of LCEL and the `Runnable` interface
- [LangChain Reference - RunnableWithMessageHistory](https://reference.langchain.com/python/langchain-core/runnables/history/RunnableWithMessageHistory) — official API reference for session-based conversation memory

## ➡️ Continue Your Learning Path

Continue to [Building a Multi-Agent Workflow](../building-a-multi-agent-workflow/) to combine
everything from this domain's agent track into one coordinated, multi-agent system.
