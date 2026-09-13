# Validating AI Output and Engineering Responsibility

## The Core Principle

Whoever commits code owns it — regardless of whether a human or an AI assistant wrote the first
draft. "The AI suggested it" is never an acceptable explanation for a bug, a security issue, or a
poor design decision that reached production. This isn't a cultural preference; it follows
directly from how these tools actually work, covered below.

## Why AI-Generated Code Requires Review

Language models generate text (including code) by predicting plausible continuations based on
patterns in their training data — they do not execute your code, verify it against your specific
runtime environment, or have guaranteed knowledge of your project's actual current state unless
that information was directly provided to them. This produces specific, recurring failure modes:

| Failure mode | What it looks like |
|---|---|
| **Hallucinated APIs** | Confidently generated code calling a function, method, or library feature that doesn't actually exist, or doesn't behave the way the code assumes |
| **Outdated patterns** | Code reflecting an older version of a library or a since-changed best practice |
| **Plausible but subtly wrong logic** | Code that reads correctly and often runs without errors, but produces a wrong result for an edge case |
| **Missing context** | Code that's correct in isolation but ignores a constraint specific to your codebase (an existing convention, a security requirement, a performance concern) the assistant wasn't told about |
| **Overconfident tone** | Fluent, well-formatted, confident-sounding explanations that are not actually reliable indicators of correctness |

None of these require the tool to be "bad" — they're structural consequences of how a language
model generates output, and they apply to varying degrees across all current AI coding tools.

## What Validation Actually Looks Like

- **Read every line before accepting it.** If you can't explain what a suggested block of code
  does, you are not ready to commit it.
- **Run it.** Confirm the code actually executes and does what's intended — untested AI-generated
  code carries the same risk as untested human-written code, and arguably more, since it wasn't
  written from a mental model you already hold.
- **Apply the same code review standard you'd apply to a human contributor's pull request** —
  including for security-sensitive logic, where an extra, careful, skeptical read is warranted.
- **Verify factual or API claims independently** when they matter — check the actual library
  documentation rather than trusting a remembered-sounding claim about how it behaves.

## Maintaining Technical Understanding

The deeper risk of over-relying on AI assistance isn't any single bad suggestion — it's the slow
erosion of your own ability to reason about code, debug independently, and recognize when
something is wrong. Using an assistant to skip understanding a concept you'll need repeatedly
(rather than to accelerate work you already understand) trades short-term speed for long-term
capability. The standard worth holding yourself to: could you have written this yourself, given
enough time, and can you defend every decision in it if asked?

## Common Mistakes

- Accepting a large, multi-file AI-generated change without reading it in full, because reviewing
  it carefully feels like it defeats the purpose of using the tool.
- Using an assistant to bypass learning a foundational concept you'll need repeatedly, rather than
  to accelerate work built on concepts you already understand.
- Assuming a security-sensitive suggestion (authentication, permission checks, input handling) is
  safe by default rather than subjecting it to *more* scrutiny than routine code, not less.

## Module Summary

AI coding assistants are genuinely useful for boilerplate, exploration, and learning (see
[using-ai-tools-effectively.md](using-ai-tools-effectively.md)), but they generate plausible text,
not verified truth — every suggestion can contain hallucinated APIs, outdated patterns, or subtly
wrong logic. The engineer who commits the code is always the one responsible for it, which means
reading, testing, and being able to defend every line, regardless of how it was drafted.
