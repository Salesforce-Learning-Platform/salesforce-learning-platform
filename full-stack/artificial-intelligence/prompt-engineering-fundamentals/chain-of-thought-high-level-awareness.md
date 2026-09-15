# 🔗 Chain-of-Thought: High-Level Awareness

## Asking a Model to Reason Before Answering

**Chain-of-thought prompting** is a foundational, well-established prompting technique: explicitly
asking a model to work through its reasoning step by step *before* giving a final answer, rather
than jumping directly to a conclusion. This is a genuinely simple idea with a real, measurable
effect — for problems involving multiple steps or real logical reasoning, walking through the
reasoning first tends to produce more accurate final answers than a direct, unreasoned response.

## A Simple Illustration

```
WITHOUT chain-of-thought:
"What's 15% of 340, minus 12?" → a direct guess at a final number

WITH chain-of-thought:
"What's 15% of 340, minus 12? Think through this step by step
before giving your final answer."
→ "15% of 340 is 0.15 × 340 = 51. Then 51 - 12 = 39."
```

Explicitly requesting the intermediate steps gives the model a chance to genuinely work through the
problem — much like a person solving a multi-step problem on paper is generally more accurate than
trying to compute it entirely in their head.

## A General Technique, Not Tied to Any One Provider

Chain-of-thought prompting is a well-established, general prompting technique that works across
virtually any capable LLM — it's simply a matter of how the prompt is worded, not a special API
parameter. This is exactly why it's worth understanding at this "high-level awareness" — a genuinely
portable skill, not something specific to one provider's implementation.

## How This Differs From a Model's Built-In "Thinking" Feature

This is a real, important distinction: chain-of-thought **prompting** is asking the model to show
its reasoning *within its regular response*, through wording in the prompt alone. Some modern
models (including Claude) additionally offer a genuinely separate, dedicated **thinking**
capability — a distinct mode where the model reasons in a structured way before producing its
visible response, calibrated automatically based on the query's complexity, rather than reasoning
being requested purely through prompt phrasing. The general chain-of-thought *technique* still
applies broadly across providers and models that don't have a dedicated thinking feature at all;
the built-in thinking capability is a more specific, provider-level mechanism doing something
related but architecturally distinct.

## When Chain-of-Thought Genuinely Helps

```
GENUINELY HELPS: multi-step math, logical reasoning, a task with
several interdependent decisions

LESS USEFUL: a simple, single-step factual lookup or a
straightforward formatting task — reasoning through it explicitly
adds tokens (per cost-awareness) without adding real accuracy
```

Chain-of-thought isn't free — it lengthens the response (and directly the
[cost](../calling-llm-apis-properly/cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md)),
so it's worth applying deliberately for tasks that genuinely benefit from explicit, multi-step
reasoning, rather than by default for every single request.

## Common Mistakes

- Assuming chain-of-thought prompting is the same thing as a model's dedicated thinking
  capability — they're related in spirit but genuinely different mechanisms.
- Applying chain-of-thought reasoning to every single request regardless of task complexity,
  incurring unnecessary token cost for tasks that didn't actually need it.
- Assuming chain-of-thought reasoning is purely for show — for genuinely complex, multi-step
  problems, it has a real, measurable effect on the accuracy of the final answer, not just its
  presentation.

## ➡️ Next

Continue to
[output-formatting-instructions-making-responses-predictable.md](output-formatting-instructions-making-responses-predictable.md)
to make an LLM's actual output format reliably predictable.
