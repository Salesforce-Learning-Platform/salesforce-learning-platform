# 🏭 How a Model Is Created

## The Real Pipeline: Five Stages

```
1. Data Collection   →  2. Data Cleaning  →  3. Training  →  4. Evaluation
   (gather a huge         (remove noise,       (per how-a-       (test against
    corpus)                 duplicates,          model-learns.md)  benchmarks)
                            bad examples)
```

Creating a real foundation model follows roughly this pipeline: **collecting** a massive corpus of
data from diverse sources; **cleaning** it (removing duplicates, low-quality or harmful content,
inconsistencies); **training** it through the loss-reduction cycle covered in
[how-a-model-learns.md](how-a-model-learns.md); and **evaluating** its resulting performance
against standardized benchmarks to guide further improvement before it's considered ready.

## Pre-Training vs. Fine-Tuning

```
PRE-TRAINING:  a massive, general, mostly unlabeled dataset →
               a broadly capable base model (extremely expensive,
               done rarely, by very few organizations)

FINE-TUNING:   a smaller, labeled, task-specific dataset, applied to
               an already-pre-trained model → a model specialized for
               one particular use case (far cheaper, done routinely)
```

**Pre-training** is the original, most expensive step: training a model from scratch (or near it)
on an enormous, general corpus, using self-supervised learning to build broad language
understanding. **Fine-tuning** takes an already pre-trained model and further trains it on a
smaller, more specific, often labeled dataset — adapting a general-purpose model toward a
particular task or domain without redoing the enormous, costly pre-training step from scratch.

## Why GPUs and Compute Clusters Are Essential

Training, per [how-a-model-learns.md](how-a-model-learns.md), means running an enormous number of
small weight adjustments across an enormous volume of data — a computation that's naturally
**parallelizable** (many independent calculations happening at once). **GPUs** (Graphics Processing
Units) are built specifically for exactly this kind of massively parallel computation, which is why
they — not standard CPUs — became the essential hardware for training modern models, typically
coordinated across large **compute clusters** of many GPUs working together.

## Training Costs

Developing a foundation model from scratch is explicitly described, even by the organizations that
build them, as "a costly, computationally intensive and time-consuming process" — the compute
required for large-scale pre-training runs into genuinely enormous sums, which is exactly why only
a small number of well-resourced organizations pre-train frontier models from scratch, while a much
larger ecosystem builds on top of them via fine-tuning.

## Checkpoints and Knowledge Cutoffs

```
Training runs for a long time → periodic CHECKPOINTS save the
model's state at that point → the final released model is trained
using data available up to some point in time — its KNOWLEDGE CUTOFF
```

A **checkpoint** is a saved snapshot of a model's weights at a particular point during (or at the
end of) training — useful both for resuming training and for comparing versions. A model's
**knowledge cutoff** is the point in time its training data was gathered up to — the model has no
direct knowledge of anything that happened after that date, since nothing after it was part of what
it was trained on.

## Common Mistakes

- Assuming every AI application involves training a model from scratch — the overwhelming majority
  of real AI application development (covered throughout the rest of this domain) builds on top of
  already-trained models via APIs, never touching pre-training at all.
- Confusing fine-tuning with pre-training — fine-tuning is a much smaller, cheaper, more common
  step layered on top of an already-expensive pre-training run, not a replacement for it.
- Assuming a model "knows" about events after its knowledge cutoff — without an external source
  of current information (a technique covered later in this domain), it genuinely has no way to
  know about anything after that date.

## ➡️ Next

Continue to [how-models-are-retrained.md](how-models-are-retrained.md) to see how a model's
knowledge is actually updated over time.
