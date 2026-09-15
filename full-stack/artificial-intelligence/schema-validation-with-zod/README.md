# 🛡️ Schema Validation with Zod for AI Responses

## 📚 Overview

An AI provider returning a response doesn't mean the response is safe to use. This module builds a
dedicated Zod validation discipline specifically for AI-generated data — schemas that model the
genuinely varied shapes an LLM response can take, a reliable way to check a response against them
without risking an uncaught exception, a deliberate policy for what happens when validation fails,
and retry strategies specific to a validation failure rather than an infrastructure one.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain why AI output is a genuine trust boundary, just like user input.
- Build Zod schemas using `.optional()`, `.nullable()`, `.default()`, `z.discriminatedUnion()`, and
  `.refine()` to model realistic AI response shapes and cross-field rules.
- Use `.safeParse()` and `z.flattenError()`/`z.treeifyError()` to verify a response and produce
  readable, structured error details.
- Choose between returning an error, falling back to a safe default, or escalating to human review
  when validation fails.
- Implement a bounded retry strategy — including feeding validation errors back into the next
  prompt — for a response that fails validation.

## 📋 Prerequisites

- [Generating JSON Responses from LLMs](../generating-json-responses-from-llms/) — this module
  builds directly on the Zod validation pattern introduced there.
- [REST API Design](../../backend/rest-api-design/) — familiarity with
  [request-validation.md](../../backend/rest-api-design/request-validation.md)'s validation
  patterns for ordinary user input.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [never-trust-ai-output-without-validation.md](never-trust-ai-output-without-validation.md) | Why AI output is a genuine trust boundary, not just an edge case worth occasionally checking |
| [defining-a-validation-schema-using-zod.md](defining-a-validation-schema-using-zod.md) | Building Zod schemas for the real, varied shapes AI responses take |
| [verifying-ai-responses-against-a-schema.md](verifying-ai-responses-against-a-schema.md) | `.safeParse()` and structured error formatting with `z.flattenError()`/`z.treeifyError()` |
| [handling-invalid-or-mismatched-responses.md](handling-invalid-or-mismatched-responses.md) | Choosing between an error, a safe fallback, or escalation when validation fails |
| [implementing-retry-strategies-for-broken-outputs.md](implementing-retry-strategies-for-broken-outputs.md) | Bounded retries, including feeding validation errors back into the next prompt |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building any feature where an LLM response feeds directly into a database
write, a user-facing decision, or another system — anywhere a malformed or wrong value would cause
a real, visible problem downstream.

**Skim** if you've already internalized Zod validation from
[REST API Design](../../backend/rest-api-design/) and
[Generating JSON Responses from LLMs](../generating-json-responses-from-llms/) — the core mental
model here is the same discipline, applied to a second, equally real source of untrusted data.

## 🧠 Knowledge Check

<details>
<summary>Why does <code>.safeParse()</code> matter more for AI responses than it might for typical internal data?</summary>

Because AI output is inherently probabilistic — even a well-designed prompt with a schema attached
can occasionally produce something malformed. `.safeParse()` turns that possibility into an
ordinary, explicit branch in the code (`result.success`) instead of an uncaught exception that
could crash an unrelated part of the request.

</details>

<details>
<summary>When should a validation failure be retried with the same prompt vs. retried with the validation errors fed back in vs. not retried at all?</summary>

A single, apparently random failure is often worth a naive retry, since the model's probabilistic
nature means the same prompt can produce a different result. If a retry is warranted and the
specific errors are known, feeding them back into the next prompt meaningfully raises the odds of
success. If the *same* field fails validation repeatedly across many different requests, that's a
systematic prompt or schema problem — no amount of retrying will fix it, and the real fix is
strengthening the prompt or schema itself.

</details>

## 📚 References

- [Zod - Error Formatting](https://zod.dev/error-formatting) — official docs for `z.flattenError()`, `z.treeifyError()`, and `z.prettifyError()`
- [Zod - API Reference](https://zod.dev/api) — official docs for `.optional()`, `.nullable()`, `.default()`, `z.discriminatedUnion()`, and `.refine()`
- [Understanding JSON Schema - The Basics](https://json-schema.org/understanding-json-schema/basics) — the official, beginner-friendly introduction to schema-based data validation concepts

## ➡️ Continue Your Learning Path

Continue to
[Function Calling and Tool Calling](../function-calling-tool-calling/) to see how an AI can trigger
real actions in an application, building on the structured-output and validation foundations from
this module and the one before it.
