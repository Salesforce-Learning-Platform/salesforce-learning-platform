# 🧠 How LLMs Actually Work

## Purpose

[Understanding AI Fundamentals](../understanding-ai-fundamentals/) covered how models learn and
what parameters are, in general. This module gets specific about **large language models** — the
kind of model every remaining file in this domain is actually built around — covering the concrete
mechanics that shape how an LLM API genuinely behaves: tokens, context windows, sampling, and why
hallucination happens at all.

## 🎯 Learning Objectives

- Explain what tokens are, and why an LLM processes text as tokens rather than whole words.
- Explain what a context window is, and what happens when it's exceeded.
- Explain temperature and sampling, and their effect on an LLM's output.
- Explain why hallucination happens, as a direct consequence of how an LLM actually works.
- Explain the real, practical difference between deterministic and probabilistic output.

## 📋 Prerequisites

- [Understanding AI Fundamentals](../understanding-ai-fundamentals/) — this module assumes the
  general concepts of training, parameters, and models already covered there.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [what-are-tokens-and-why-everything-becomes-tokens.md](what-are-tokens-and-why-everything-becomes-tokens.md) | What a token is, and why LLMs process text this way |
| [what-is-a-context-window-and-why-prompts-get-cut.md](what-is-a-context-window-and-why-prompts-get-cut.md) | The model's "working memory," and what happens when it's exceeded |
| [sampling-basics-temperature-and-randomness-control.md](sampling-basics-temperature-and-randomness-control.md) | Temperature, and controlling how predictable or creative an output is |
| [why-hallucination-happens-it-predicts-it-doesnt-know.md](why-hallucination-happens-it-predicts-it-doesnt-know.md) | Prediction vs. knowledge, and real mitigation techniques |
| [deterministic-vs-probabilistic-outputs.md](deterministic-vs-probabilistic-outputs.md) | Why the same prompt can produce a different result each time |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive
[why-hallucination-happens-it-predicts-it-doesnt-know.md](why-hallucination-happens-it-predicts-it-doesnt-know.md) —
understanding hallucination as a direct, structural consequence of how an LLM works (not a random
bug) is the single most important mental model for building any real, trustworthy AI-powered
feature, covered throughout the rest of this domain.

## ✅ Quick Knowledge Check

<details>
<summary>If you send the exact same prompt to an LLM twice with temperature set to 0, are you guaranteed the exact same output both times?</summary>

Not fully guaranteed — even at temperature 0, real-world API behavior can still produce
non-identical outputs across calls, for reasons outside the temperature setting alone (such as how
computation is distributed across hardware). Temperature 0 makes output far more consistent, but
"deterministic" isn't an absolute guarantee in practice. See
[deterministic-vs-probabilistic-outputs.md](deterministic-vs-probabilistic-outputs.md).

</details>

<details>
<summary>Does an LLM "know" it doesn't know something, the way a person can say "I'm not sure"?</summary>

Not inherently — an LLM predicts plausible next tokens based on patterns in its training data; it
has no built-in mechanism for genuinely verifying whether a specific claim is true. Explicitly
prompting it to say "I don't know" when uncertain is a real, effective mitigation, but it's a
prompting technique, not the model consulting some internal fact-checker. See
[why-hallucination-happens-it-predicts-it-doesnt-know.md](why-hallucination-happens-it-predicts-it-doesnt-know.md).

</details>

## 📚 References

- Anthropic, [Glossary](https://platform.claude.com/docs/en/about-claude/glossary)
- Anthropic, [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

## ➡️ Continue Your Learning Path

Continue to the [Calling LLM APIs Properly module](../calling-llm-apis-properly/) to apply these
concepts to real, production API calls.
