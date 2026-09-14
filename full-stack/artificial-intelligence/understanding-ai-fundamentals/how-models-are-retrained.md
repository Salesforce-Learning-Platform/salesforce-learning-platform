# 🔄 How Models Are Retrained

## Why a Model Ever Needs Updating

A released model is frozen at its [knowledge cutoff](how-a-model-is-created.md) — the world keeps
changing after that point, new information keeps appearing, and real usage keeps surfacing gaps or
mistakes the original training didn't catch. A model that's never updated becomes progressively
more outdated and, over time, less useful for anything involving recent information.

## Fine-Tuning vs. Training From Scratch, Revisited for Updates

```
TRAINING FROM SCRATCH AGAIN:  full new pre-training run — extremely
                                expensive, done relatively rarely,
                                usually for a genuinely new model
                                generation

FINE-TUNING AN EXISTING MODEL: additional, targeted training on top
                                of an already-trained model — far
                                cheaper, used far more often
```

Just as [how-a-model-is-created.md](how-a-model-is-created.md) distinguished pre-training from
fine-tuning for a model's *initial* creation, the same distinction applies to keeping a model
current: a genuinely new model generation typically involves a costly new pre-training run, while
smaller updates and improvements to an existing model line are far more often achieved through
fine-tuning — targeted additional training that builds on the already-substantial capability the
original pre-training already established, without redoing that enormous initial cost.

## What This Means in Practice for a Developer

An application built against a specific model version should expect that model to eventually be
succeeded by a newer one — with a later knowledge cutoff, and often improved capability — rather
than assuming the exact model in use today will remain the best (or even available) choice
indefinitely. This directly connects to
[Calling LLM APIs Properly](../calling-llm-apis-properly/)'s later coverage of choosing and
working with a specific model version deliberately, rather than treating "the AI" as a single,
unchanging thing.

## Common Mistakes

- Assuming a model's knowledge automatically stays current over time — it only ever updates when
  its creators actually retrain or fine-tune a new version and release it.
- Treating every model update as a full, from-scratch retraining — most updates are actually
  achieved through the far cheaper, more frequent process of fine-tuning an existing base model.
- Building an application with a hardcoded assumption that today's specific model version will
  remain available and current indefinitely, rather than planning for eventual model updates.

## ➡️ Next

Continue to [the-ai-landscape.md](the-ai-landscape.md) to see how all of this — model size, cost,
and openness — shapes the real, current AI ecosystem a developer actually works within.
