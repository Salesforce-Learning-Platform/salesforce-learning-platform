# 🔗 Building a RAG Pipeline

## 📚 Overview

This module is a capstone for the retrieval track of this domain: it combines
[Understanding Embeddings](../understanding-embeddings/) and
[Integrating Vector Databases](../integrating-vector-databases/) with the structured-generation and
validation techniques from earlier in the domain into Retrieval-Augmented Generation (RAG) — an
architecture that grounds a model's answer in an application's own real, current data. The module
ends with a complete, production-shaped document Q&A system returning structured, validated
answers with confidence and citations.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain the four-stage RAG workflow (query → retrieve → inject → answer) and why it exists.
- Write the explicit "use only this context" instruction that makes an answer genuinely grounded.
- Build a complete document Q&A feature combining retrieval, schema-constrained generation, Zod
  validation, and structured error handling into one production-shaped endpoint.

## 📋 Prerequisites

- [Understanding Embeddings](../understanding-embeddings/) and [Integrating Vector Databases](../integrating-vector-databases/) — the retrieval half of this module.
- [Generating JSON Responses from LLMs](../generating-json-responses-from-llms/) and [Schema Validation with Zod](../schema-validation-with-zod/) — the structured-generation half.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [the-rag-workflow.md](the-rag-workflow.md) | The four-stage RAG workflow and why explicit grounding instructions matter |
| [build-a-document-qa-system-returning-structured-json.md](build-a-document-qa-system-returning-structured-json.md) | A complete, production-shaped Q&A system: retrieval + JSON mode + Zod validation |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building any feature where an AI needs to answer questions using an
organization's own private or frequently-changing documents — support content, internal policies,
product documentation.

**Skim** if you've already built a RAG-shaped feature before and mainly want to see how it combines
with this domain's structured-output and validation techniques specifically.

## 🧠 Knowledge Check

<details>
<summary>Why is the "answer using ONLY the context below" instruction critical to RAG actually working as intended?</summary>

Without it, a model may still answer using its own training knowledge instead of (or blended with)
the retrieved context — even when real, current, retrieved information is available and directly
relevant. This single instruction is what turns retrieval-*influenced* generation into genuinely
*grounded* generation.

</details>

<details>
<summary>Why does the document Q&A example include an explicit <code>answerFoundInContext</code> boolean rather than just returning the model's best guess?</summary>

Retrieved context won't always actually contain the answer to a given question. An explicit,
structured signal for this case lets the application respond honestly — showing a "not found"
notice rather than presenting an unsupported guess as though it were a grounded, sourced answer.

</details>

## 📚 References

- [Anthropic - Embeddings: Quickstart Example](https://platform.claude.com/docs/en/build-with-claude/embeddings#quickstart-example) — the official retrieval example this module's RAG workflow builds on
- [AWS - What Is RAG (Retrieval-Augmented Generation)?](https://aws.amazon.com/what-is/retrieval-augmented-generation/) — a well-known, vendor-neutral explanation of the RAG architecture

## ➡️ Continue Your Learning Path

Continue to [Evaluating AI Systems](../evaluating-ai-systems/) to see how a feature like this
document Q&A system is actually tested and measured for quality before and after shipping it.
