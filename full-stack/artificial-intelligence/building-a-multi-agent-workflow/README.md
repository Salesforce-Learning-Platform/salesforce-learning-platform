# 🔀 Building a Multi-Agent Workflow

## 📚 Overview

This module is a capstone applying nearly everything from this domain's agent and structured-output
tracks to two complete, realistic multi-stage pipelines: a profile-analysis pipeline (text in,
text out) and an image-processing pipeline (image in, structured metadata out). Both pipelines
demonstrate the same core lesson — a fixed, multi-stage **workflow** (not a dynamic agent) is often
the right, simpler choice when a task's stages are genuinely predictable.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Build a multi-stage pipeline where each stage does one distinct job and hands the next stage
  clean, validated, structured data.
- Recognize when a fixed workflow is the right choice over a dynamic agent for a multi-step task.
- Apply schema validation (via Pydantic, this module's Python equivalent to Zod) and per-stage
  error attribution across an entire pipeline.
- Identify independent pipeline stages that can run in parallel for a real latency improvement.

## 📋 Prerequisites

- [Agent Design Patterns](../agent-design-patterns/) and [Understanding AI Agents](../understanding-ai-agents/) — this module's pipelines apply the researcher-writer and workflow-vs-agent distinctions directly.
- [Schema Validation with Zod](../schema-validation-with-zod/) — the validation discipline applied throughout, here via Pydantic.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [profile-analyzer-to-bio-improver-to-conversation-starter-generator.md](profile-analyzer-to-bio-improver-to-conversation-starter-generator.md) | A three-stage text pipeline: analysis → rewrite → generation |
| [image-metadata-extractor-to-seo-optimizer-to-tag-categorizer.md](image-metadata-extractor-to-seo-optimizer-to-tag-categorizer.md) | A three-stage multimodal pipeline: image → SEO content → categorization; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building any feature that transforms one input through several distinct,
predictable AI-powered stages — content pipelines, data enrichment, multi-step generation features.

**Skim** if you've already built a multi-stage pipeline before and mainly want to see two complete,
concrete worked examples for reference.

## 🧠 Knowledge Check

<details>
<summary>Why are both pipelines in this module built as fixed workflows rather than dynamic agents?</summary>

In both cases, the sequence of stages is genuinely always the same — analysis always precedes bio
improvement, which always precedes starter generation. Per
<a href="../understanding-ai-agents/agent-vs-single-llm-call.md">agent-vs-single-llm-call.md</a>,
a fixed workflow is simpler, cheaper, and more predictable than a full agent whenever the actual
sequence of steps is already known and doesn't need to be decided dynamically.

</details>

<details>
<summary>In the image pipeline, why can the SEO optimizer and tag categorizer stages run in parallel?</summary>

Both stages depend only on Stage 1's extracted metadata, not on each other's output — neither
stage's input requires the other stage to have already run. This independence is exactly what makes
them a good fit for `RunnableParallel` (or any concurrent execution), cutting real latency compared
to running them one after another for no genuine reason.

</details>

## 📚 References

- [Pydantic - JSON Validation](https://pydantic.dev/docs/validation/latest/concepts/json/) — official documentation for `model_validate_json()`, used throughout this module's Python pipeline examples
- [Anthropic - Vision (Image Understanding)](https://platform.claude.com/docs/en/build-with-claude/vision) — official documentation for the image content block format used in Pipeline 2

## ➡️ Continue Your Learning Path

Continue to
[Multi-Agent Architecture Concerns](../multi-agent-architecture-concerns/) to see the deeper
architectural trade-offs — cost, coordination, debugging — that come with scaling this kind of
multi-stage system further.
