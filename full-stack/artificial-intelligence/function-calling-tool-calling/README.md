# 🔨 Function Calling and Tool Calling

## 📚 Overview

This module covers tool calling in its full, real form: letting a model genuinely trigger real
functions in your application — a database lookup, a refund, a weather check — rather than only
using the mechanism for structured data extraction. It builds directly on the narrower,
extraction-only use already introduced in
[Generating JSON Responses from LLMs](../generating-json-responses-from-llms/), extending it into a
complete picture of when, why, and how a model should call real code.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain what tool calling actually is and the specific gap it closes in a model's capabilities.
- Decide when a task genuinely needs a real, deterministic tool call versus when plain generation
  is enough.
- Design a hybrid AI+code feature where the model handles intent and code enforces business rules.
- Use `tool_choice` (`auto`, `any`, a forced specific tool, `none`) to control when and which tool
  the model calls.

## 📋 Prerequisites

- [Basics of Tool/Function Calling](../generating-json-responses-from-llms/basics-of-tool-function-calling.md) — the narrower, extraction-only preview of the same underlying mechanism.
- [Prompt Engineering Fundamentals](../prompt-engineering-fundamentals/) — writing clear instructions applies directly to writing clear tool descriptions.
- [Schema Validation with Zod](../schema-validation-with-zod/) — validating a tool's arguments before acting on them follows the same discipline as validating any other AI output.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-tool-calling-and-why-it-matters.md](what-is-tool-calling-and-why-it-matters.md) | The core mechanism: `tool_use` and `tool_result`, and the gap it closes |
| [when-to-use-it-for-deterministic-actions.md](when-to-use-it-for-deterministic-actions.md) | When a real tool call is the right choice, and when plain generation is enough |
| [hybrid-logic-ai-and-code.md](hybrid-logic-ai-and-code.md) | Splitting responsibility: the model interprets intent, code enforces business rules |
| [letting-ai-decide-which-function-to-call.md](letting-ai-decide-which-function-to-call.md) | `tool_choice` options and how the model picks between multiple available tools |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building any feature where an AI needs to trigger a real action — a
booking, a refund, a database update — rather than only generate text or structured data.

**Skim** if your use case is purely about generating well-shaped data (already covered in
[Generating JSON Responses from LLMs](../generating-json-responses-from-llms/)) with no real,
external action ever required.

## 🧠 Knowledge Check

<details>
<summary>Why should exact arithmetic or a consequential action never be handled by the model's own text generation alone?</summary>

A model is fundamentally a probabilistic text generator — it can produce a wrong number or a
wrong claim that still looks entirely confident and correct. Routing exact computation and real,
consequential actions through an actual tool call means the result is either genuinely correct (the
tool ran real code) or the call fails visibly — eliminating the specific risk of a plausible-looking
but wrong result.

</details>

<details>
<summary>Where should a business rule like "refunds over $100 require manager approval" actually be enforced?</summary>

In the tool's own implementation code — never only in the prompt or system instructions. A prompt-
only rule is a strong suggestion the model usually follows, but a genuine business rule with real
consequences needs to hold every time, which only actual code enforcement guarantees.

</details>

## 📚 References

- [Anthropic - Tool Use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — official documentation for `tool_use`, `tool_result`, and `tool_choice`
- [Anthropic - Define Tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) — writing effective tool schemas and descriptions
- [MDN Web Docs - JSON](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON) — a refresher on the JSON structures tool schemas and arguments are built from

## ➡️ Continue Your Learning Path

Continue to [Streaming AI Responses](../streaming-responses/) to see how a model's output —
including tool calls — can be delivered incrementally rather than all at once.
