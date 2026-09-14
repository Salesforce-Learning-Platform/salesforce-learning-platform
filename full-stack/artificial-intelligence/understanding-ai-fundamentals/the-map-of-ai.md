# 🗺️ The Map of AI

## Three Nested Fields, Not Three Separate Ones

```
┌─────────────────────────────────────────┐
│  Artificial Intelligence (AI)            │
│  ┌─────────────────────────────────┐     │
│  │  Machine Learning (ML)            │    │
│  │  ┌───────────────────────┐        │    │
│  │  │  Deep Learning (DL)     │       │    │
│  │  └───────────────────────┘        │    │
│  └─────────────────────────────────┘     │
└─────────────────────────────────────────┘
```

**Artificial Intelligence** is the broadest field: technology that enables a computer to simulate
tasks associated with human intelligence — understanding language, recognizing objects, making
decisions. **Machine Learning** is a specific approach *within* AI: instead of explicitly
programming every rule a system should follow, a model is trained on data and learns to make
predictions or decisions from it. **Deep Learning** is, in turn, a specific approach *within*
Machine Learning: it uses **neural networks** with many layers ("deep" refers to the number of
layers) to learn far more complex patterns than earlier, shallower ML techniques could.

## Rule-Based Systems vs. Learning-Based Systems

```
Rule-based:    if (email contains "you've won") → mark as spam
               (a human wrote this exact rule)

Learning-based: shown 100,000 labeled emails → the model learns
                its OWN patterns for what "spam" tends to look like
```

A **rule-based system** follows explicit, hand-written logic — a human decided every condition in
advance. A **learning-based system** (what modern AI almost always means) is instead shown large
amounts of data and learns its own patterns from it, without a human explicitly writing out every
rule. This is the real, foundational shift Machine Learning represents: moving from "a programmer
decided the rules" to "the system inferred the rules from data."

## Why This Matters Before Writing Any AI Code

Every later module in this domain — from
[How LLMs Actually Work](../how-llms-actually-work/) through
[Building a RAG Pipeline](../building-a-rag-pipeline/) — deals specifically with a **deep
learning** system: a large language model, itself a deep neural network. Understanding that an LLM
sits at the innermost, most specific layer of this map — AI → ML → DL → (a specific kind of deep
learning model) — makes it much easier to reason about what an LLM genuinely is and isn't capable
of, rather than treating "AI" as one undifferentiated, mysterious thing.

## Common Mistakes

- Treating "AI," "Machine Learning," and "Deep Learning" as three separate, competing technologies,
  rather than three nested layers of the same field.
- Assuming every AI system is a learning-based one — many real, useful systems (a simple
  form-validation rule, a basic chatbot's decision tree) are still genuinely rule-based, not
  learned from data at all.
- Assuming "AI" always means a large language model specifically — LLMs are one particular, very
  prominent kind of deep learning system, not a synonym for the entire field.

## ➡️ Next

Continue to [how-a-model-learns.md](how-a-model-learns.md) to see, conceptually, what "learning
from data" actually involves.
