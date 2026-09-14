# 🧠 Understanding AI Fundamentals

## Purpose

Before writing a single line of AI-powered application code — the focus of every other module in
this domain, starting with
[How LLMs Actually Work](../how-llms-actually-work/) — it's worth understanding, conceptually, what
AI actually is, how a model learns at all, and what determines its real capability. This module is
that foundation: no code, no APIs, just the concepts underneath everything else in this domain.

## 🎯 Learning Objectives

- Explain what AI, Machine Learning, and Deep Learning actually are, and how each nests inside the
  other.
- Distinguish rule-based systems from learning-based systems.
- Explain, at a conceptual level, how a model actually learns from data.
- Explain what "parameters" are, and why a bigger model isn't automatically a better one.
- Describe the real pipeline that produces a trained model, and why it's so resource-intensive.
- Explain why and how models get updated after their initial release.
- Describe the current AI landscape: open vs. closed models, and the real costs involved.

## 📋 Prerequisites

None — this module is intentionally the starting point for the Artificial Intelligence domain,
requiring no prior programming or AI-specific background.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [the-map-of-ai.md](the-map-of-ai.md) | AI, Machine Learning, and Deep Learning — how each fits inside the other |
| [how-a-model-learns.md](how-a-model-learns.md) | Data, patterns, weights, training, and loss |
| [what-parameters-mean.md](what-parameters-mean.md) | What "billions of parameters" actually means, and why bigger isn't always better |
| [how-a-model-is-created.md](how-a-model-is-created.md) | The real pipeline: data collection through evaluation, and why it's so resource-intensive |
| [how-models-are-retrained.md](how-models-are-retrained.md) | Why models need updating, and fine-tuning vs. training from scratch |
| [the-ai-landscape.md](the-ai-landscape.md) | Open vs. closed models, token pricing and compute costs, and where AI fits in a developer's workflow |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [what-parameters-mean.md](what-parameters-mean.md) — parameter count is the single most
commonly cited (and most commonly misunderstood) number in any discussion of AI models, and
understanding precisely what it does and doesn't tell you is genuinely useful well beyond this one
module.

## ✅ Quick Knowledge Check

<details>
<summary>Is Deep Learning a separate field from Machine Learning, or a part of it?</summary>

A part of it — Deep Learning is a **subset** of Machine Learning, specifically the subset that uses
multi-layered neural networks. Machine Learning is itself a subset of the broader field of
Artificial Intelligence. See [the-map-of-ai.md](the-map-of-ai.md).

</details>

<details>
<summary>Does a model with more parameters always perform better than one with fewer?</summary>

Not automatically — more parameters generally increase a model's capacity to capture complex
patterns, but the relationship isn't strictly linear, and a larger model demands significantly more
compute to train and run. A smaller, well-targeted model is often the better practical choice for a
resource-constrained or narrowly-scoped task. See
[what-parameters-mean.md](what-parameters-mean.md).

</details>

## 📚 References

- IBM, [What Is Artificial Intelligence (AI)?](https://www.ibm.com/think/topics/artificial-intelligence)
- Google, [What is loss?](https://developers.google.com/machine-learning/crash-course/linear-regression/loss)
- IBM, [What Are Large Language Models (LLMs)?](https://www.ibm.com/think/topics/large-language-models)
- IBM, [What Is a Foundation Model?](https://www.ibm.com/think/topics/foundation-models)
- IBM, [Open-Source AI](https://www.ibm.com/think/topics/open-source-ai)

## ➡️ Continue Your Learning Path

Continue to [How LLMs Actually Work](../how-llms-actually-work/) to apply these foundational
concepts specifically to the large language models this entire domain is built around.
