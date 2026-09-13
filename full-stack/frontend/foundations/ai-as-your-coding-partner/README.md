# AI as Your Coding Partner

## Purpose

AI coding assistants (chat-based assistants, inline code completion, agentic coding tools) are now
a standard part of professional software development. Used well, they meaningfully speed up
routine work and help you learn faster; used carelessly, they can introduce subtle bugs, security
issues, or a false sense of understanding. This module is about using them like a senior engineer
would — as a tool whose output you're always responsible for, never as a replacement for your own
technical judgment.

## Learning Objectives

- Identify tasks where an AI coding assistant genuinely helps, and where it's the wrong tool.
- Explain why AI-generated code must always be reviewed and validated, not merely trusted.
- Describe common, realistic AI coding failure modes so you can recognize them.
- Apply a consistent standard: you must be able to explain and defend every line of code you ship,
  regardless of who or what wrote the first draft.

## Files in This Module

| File | Covers |
|---|---|
| [using-ai-tools-effectively.md](using-ai-tools-effectively.md) | Where AI assistance genuinely helps, and how to prompt for useful results |
| [validating-ai-output-and-engineering-responsibility.md](validating-ai-output-and-engineering-responsibility.md) | Why review and validation are non-negotiable, common failure modes, and where engineering responsibility ultimately sits |

## When to Deep-Dive vs. Skim

Read both files in full regardless of how much AI-tool experience you already have — the habits in
[validating-ai-output-and-engineering-responsibility.md](validating-ai-output-and-engineering-responsibility.md)
specifically are easy to know intellectually and still skip under time pressure, which is exactly
when they matter most.

## Quick Knowledge Check

<details>
<summary>If an AI assistant generates a bug that ships to production, who is responsible?</summary>

Whoever committed the code. "The AI suggested it" is never an acceptable explanation — the
engineer reviewing and accepting a suggestion owns it exactly as if they'd written it themselves.
See
[validating-ai-output-and-engineering-responsibility.md](validating-ai-output-and-engineering-responsibility.md).

</details>

<details>
<summary>Why can an AI coding assistant generate confident, well-formatted code that calls a function which doesn't actually exist?</summary>

It's predicting a plausible continuation based on patterns in its training data, not executing or
verifying your code against your actual environment — this "hallucinated API" failure mode is a
structural consequence of how it generates output, not a rare glitch. See
[validating-ai-output-and-engineering-responsibility.md](validating-ai-output-and-engineering-responsibility.md).

</details>

## References

- [Claude Code documentation](https://code.claude.com/docs/en/overview) — one concrete example of
  an agentic coding assistant and the workflow it supports; the validation principles in this
  module apply regardless of which specific tool you use.

## Continue Your Learning Path

Next in the [Foundations sequence](../README.md):
[Reading Documentation](../reading-documentation/).
