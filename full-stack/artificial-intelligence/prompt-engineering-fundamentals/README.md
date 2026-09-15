# ✍️ Prompt Engineering Fundamentals

## Purpose

[Calling LLM APIs Properly](../calling-llm-apis-properly/) covered *how* to structure a request.
This module covers *what to actually put in it* — the real, verifiable techniques that make an
LLM's output more accurate, consistent, and genuinely usable in a real application, rather than
treating prompt-writing as guesswork.

## 🎯 Learning Objectives

- Write clear, explicit instructions using the "golden rule" test.
- Use few-shot examples to reliably steer an output's format and pattern.
- Explain chain-of-thought reasoning at a high level, and how it differs from a model's built-in
  thinking capability.
- Control an LLM's output formatting deliberately, rather than fighting against its defaults.

## 📋 Prerequisites

- [Calling LLM APIs Properly](../calling-llm-apis-properly/) — this module assumes you can already
  structure a correct API request; it focuses specifically on what content produces better results.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [writing-clear-instructions.md](writing-clear-instructions.md) | The "golden rule" test, and being explicit rather than vague |
| [few-shot-examples-to-force-pattern-learning.md](few-shot-examples-to-force-pattern-learning.md) | Steering output format and tone with well-chosen examples |
| [chain-of-thought-high-level-awareness.md](chain-of-thought-high-level-awareness.md) | Asking a model to reason step by step, and how this differs from a dedicated thinking feature |
| [output-formatting-instructions-making-responses-predictable.md](output-formatting-instructions-making-responses-predictable.md) | Making an LLM's output format genuinely predictable |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive
[few-shot-examples-to-force-pattern-learning.md](few-shot-examples-to-force-pattern-learning.md) —
of every technique in this module, providing concrete examples is consistently one of the most
reliable ways to steer an LLM's actual output, and choosing genuinely good examples is a real,
learnable skill.

## ✅ Quick Knowledge Check

<details>
<summary>What's the "golden rule" test for whether a prompt is clear enough?</summary>

Show the prompt to a colleague with minimal context on the task, and ask them to follow it — if
they'd be confused about exactly what's being asked, the model will be too. See
[writing-clear-instructions.md](writing-clear-instructions.md).

</details>

<details>
<summary>To stop a model from using markdown formatting, is it better to say "do not use markdown" or to describe the format you actually want?</summary>

Describing the format you actually want (e.g., "write in smoothly flowing prose paragraphs") is
more reliable than a negative instruction — telling a model what *to* do consistently works better
than telling it what *not* to do. See
[output-formatting-instructions-making-responses-predictable.md](output-formatting-instructions-making-responses-predictable.md).

</details>

## 📚 References

- Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

## ➡️ Continue Your Learning Path

Continue to the [Structured Output in AI Systems module](../structured-output-in-ai-systems/) to
apply these prompting techniques toward producing genuinely reliable, programmatically usable
output.
