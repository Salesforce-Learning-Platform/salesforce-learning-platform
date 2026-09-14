# 🌐 The AI Landscape

## Open Models vs. Closed Models

```
OPEN:    the model's weights are published and can be downloaded,
         run, and modified freely — cost-efficient, transparent,
         customizable, but requires you to host/run it yourself

CLOSED:  the model runs only behind the creator's own API — you
         never download its weights — with dedicated support and
         managed infrastructure, at a cost per use
```

An **open** model publishes its actual trained weights, letting anyone download, run, and even
modify it — genuinely free to use, highly customizable, and transparent (its behavior can be
audited directly), but the *responsibility* of hosting, running, and securing it shifts entirely to
whoever deploys it. A **closed (proprietary)** model instead runs only behind its creator's own
API — access is metered and paid for, but the creator handles hosting, scaling, support, and
ongoing updates.

## Token Pricing, Compute Costs, and Latency

Using a closed model's API is typically priced **per token** — the same [tokenization
unit](../how-llms-actually-work/) covered in the next module — meaning cost scales directly with
how much text is sent to and received from the model. Running an open model yourself instead
incurs **compute cost** directly (GPU time, whether rented from a cloud provider or owned
hardware), and **latency** — how quickly a response actually comes back — depends heavily on model
size and the hardware it's running on, connecting directly back to
[what-parameters-mean.md](what-parameters-mean.md)'s point about larger models being slower and
more expensive to run.

## Neither Choice Is Universally "Correct"

| Favor **open** when | Favor **closed** when |
|---|---|
| Full customization or on-premises hosting is required | Minimal operational overhead is preferred |
| Cost predictability from owned infrastructure matters | Access to the absolute newest, most capable models matters |
| Data must never leave your own infrastructure | A managed, supported API is worth its per-use cost |

This is a genuine engineering tradeoff, evaluated per project — directly the same kind of judgment
[SQL vs. NoSQL](../../backend/database-design-and-modeling/sql-vs-nosql.md) required for choosing a
database, applied here to choosing an AI model and how to access it.

## How AI Fits Into a Modern Developer's Workflow

The rest of this domain — [Calling LLM APIs Properly](../calling-llm-apis-properly/),
[Prompt Engineering](../prompt-engineering-fundamentals/), and everything through
[Engineering WITH AI](../engineering-with-ai/) — assumes a developer working *with* an already
existing, already-trained model via its API, not training or fine-tuning one from scratch. This is
overwhelmingly how real AI-powered applications are actually built today: as a client calling a
model's API, applying the concepts from this foundational module to use that model well, safely,
and cost-effectively.

## Common Mistakes

- Assuming "using AI" in an application means training a model — the vast majority of real AI
  application development, covered throughout the rest of this domain, means calling an
  already-trained model's API, not building one.
- Choosing a closed model's API purely out of habit without considering whether an open model's
  cost/customization tradeoff would genuinely fit a specific project better.
- Ignoring token-based pricing entirely when designing an AI feature, leading to unexpectedly high
  costs once real usage volume arrives — a concern directly addressed in
  [Calling LLM APIs Properly](../calling-llm-apis-properly/).

## Module Summary

Across this module: **AI, Machine Learning, and Deep Learning** are nested fields, not separate
technologies, with rule-based and learning-based systems as a genuinely different foundational
distinction (see [the-map-of-ai.md](the-map-of-ai.md)); a model **learns** by repeatedly adjusting
its weights to reduce **loss** across a huge volume of training data, making data quality often more
decisive than algorithmic sophistication (see [how-a-model-learns.md](how-a-model-learns.md));
**parameters** are those adjustable weights, and their count is a rough capacity proxy, not a
direct measure of real-world usefulness for any specific task (see
[what-parameters-mean.md](what-parameters-mean.md)); a model is actually created through a
data-collection-to-evaluation pipeline, with pre-training as the enormously expensive foundation and
fine-tuning as the far cheaper specialization layered on top, producing checkpoints and a fixed
knowledge cutoff (see [how-a-model-is-created.md](how-a-model-is-created.md)); models are **updated
over time** mostly through fine-tuning rather than repeated full retraining (see
[how-models-are-retrained.md](how-models-are-retrained.md)); and the current **AI landscape** —
open vs. closed models, token pricing, and compute cost — is the real, practical context every
later module in this domain builds directly on top of.
