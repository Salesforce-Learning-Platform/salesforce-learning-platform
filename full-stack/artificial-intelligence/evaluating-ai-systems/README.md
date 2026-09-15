# 📈 Evaluating AI Systems

## 📚 Overview

Building an AI feature — generation, RAG, tool calling — is only half the work; knowing whether it
actually works well, and staying aware of when it stops, is the other half. This module covers
detecting hallucinations, assigning meaningful confidence scores, measuring retrieval quality
independently from answer quality, and the observability practices that keep a system's real
production behavior visible over time.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Apply grounding checks and self-consistency sampling to detect likely hallucinations.
- Combine multiple signals into a confidence score more reliable than a model's self-report alone.
- Measure retrieval quality with precision@k, recall@k, and MRR against a real evaluation set.
- Track latency, cost, error rate, and quality metrics through request-level tracing, and set
  alerts on genuine, sustained shifts rather than individual expected failures.

## 📋 Prerequisites

- [Building a RAG Pipeline](../building-a-rag-pipeline/) — retrieval-quality evaluation builds directly on this module's vector search and Q&A patterns.
- [Error Handling in AI Applications](../error-handling-in-ai-applications/) — observability extends this module's structured logging discipline.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [detecting-hallucinations.md](detecting-hallucinations.md) | Grounding checks and self-consistency sampling for catching fabricated content |
| [assigning-confidence-scores.md](assigning-confidence-scores.md) | Combining self-reported, retrieval-based, and consistency signals into one confidence value |
| [evaluating-retrieval-quality.md](evaluating-retrieval-quality.md) | Precision@k, recall@k, MRR, and building a real evaluation set |
| [observability-and-monitoring-basics.md](observability-and-monitoring-basics.md) | Tracing, core metrics, and alerting on genuine production shifts |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're preparing to ship any AI feature to real users — evaluation and
observability are what separate a working demo from a system a team can actually trust and
maintain in production.

**Skim** if you're still in early prototyping with no real users yet — return to this module once a
feature is close to shipping.

## 🧠 Knowledge Check

<details>
<summary>Why is a model's self-reported confidence score not the same kind of signal as, say, a classifier's probability output?</summary>

Self-reported confidence is itself just generated text, produced the same way as any other model
output — not derived from genuine internal introspective access to a measurable certainty value.
It's a useful heuristic that tends to correlate reasonably with accuracy, but it should be combined
with independent signals (like retrieval similarity) rather than trusted as ground truth on its
own.

</details>

<details>
<summary>Why measure retrieval quality (precision@k, recall@k, MRR) separately from overall answer quality in a RAG system?</summary>

A RAG system can fail in two independent ways — bad retrieval or bad generation from otherwise-good
retrieval — and each has a completely different fix. Measuring retrieval on its own (with a
dedicated evaluation set) makes it possible to tell which half of the pipeline is actually
responsible for a poor answer.

</details>

## 📚 References

- [Langfuse - LLM Observability & Application Tracing](https://langfuse.com/docs/observability/overview) — an open-source, purpose-built LLM observability platform
- [LangSmith - Agent & LLM Observability Platform](https://www.langchain.com/langsmith/observability) — a widely-used LLM tracing and evaluation platform

## ➡️ Continue Your Learning Path

Continue to [Understanding AI Agents](../understanding-ai-agents/) to move from evaluating a single
request-response cycle into systems that plan and act across multiple steps.
