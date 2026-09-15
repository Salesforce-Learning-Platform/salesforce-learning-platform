# 👨‍💻 Engineering WITH AI

## 📚 Overview

This module closes out the Generative AI Engineering domain by turning inward — applying every
discipline this domain has built (validation, review, trust boundaries) to AI coding tools like
Cursor, GitHub Copilot, and Claude Code. The core lesson: using an AI coding tool well doesn't mean
using it *less* critically — it means directing it clearly, reviewing its output as rigorously as
any human teammate's code, and never outsourcing accountability for what ships.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Write clear, context-rich prompts for AI coding tools that produce codebase-consistent results.
- Apply the same code review rigor to AI-generated code as to any human-written pull request.
- Identify the specific risks (edge cases, convention drift, security gaps) that need deliberate
  extra scrutiny in AI-generated code.
- Explain — and apply — the "can you defend this line?" standard before shipping AI-assisted code.

## 📋 Prerequisites

- [Understanding AI Agents](../understanding-ai-agents/) — AI coding tools use the same agentic loop covered there.
- [Schema Validation with Zod](../schema-validation-with-zod/) — the "never trust AI output without validation" principle, applied here to code instead of data.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [using-ai-coding-tools-like-a-senior-developer.md](using-ai-coding-tools-like-a-senior-developer.md) | Directing AI coding tools with clear, context-rich prompts and iterative feedback |
| [reviewing-ai-generated-code-when-to-trust-it-and-when-not-to.md](reviewing-ai-generated-code-when-to-trust-it-and-when-not-to.md) | Applying full code-review rigor, with a concrete SQL-injection example |
| [shipping-an-ai-assisted-feature-and-defending-every-line.md](shipping-an-ai-assisted-feature-and-defending-every-line.md) | The "can you defend this line?" standard and a complete pre-ship checklist; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you use any AI coding tool regularly — this module's discipline applies to every
line that tool produces, on every project, indefinitely.

**Skim** if you've already internalized a rigorous code-review discipline from experience — this
module's core message is that AI-generated code deserves exactly that same standard, no more, no
less.

## 🧠 Knowledge Check

<details>
<summary>Why isn't "the AI tool generated it" an acceptable answer when asked to explain a piece of shipped code?</summary>

Whoever opens the pull request is responsible for every line in it, regardless of who — or what —
wrote the first draft. If a developer can't explain *why* a piece of code works the way it does, not
just *that* it works, that's a clear sign the code isn't genuinely understood and isn't ready to
ship.

</details>

<details>
<summary>Why does the code-review discipline in this module matter more, not less, as AI coding tools become more capable?</summary>

A more capable tool produces code that's more plausible-looking and more often correct on the
surface — which makes it easier to under-scrutinize, exactly the same "confident but wrong" risk
covered by hallucination detection earlier in this domain, now applied to code. Rigorous review
matters most precisely when the output looks most trustworthy by default.

</details>

## 📚 References

- [Claude Code - Overview](https://code.claude.com/docs/en/overview) — official documentation for Claude Code's agentic coding capabilities
- [GitHub - About GitHub Copilot](https://docs.github.com/en/copilot/about-github-copilot) — official documentation for GitHub Copilot

## ➡️ Continue Your Learning Path

This is the final module in the Generative AI Engineering domain. Continue to
[DevOps and Infrastructure](../../production-systems/) to move from building AI-powered features to
deploying and operating production systems more broadly.
