# 🚢 Shipping an AI-Assisted Feature and Defending Every Line

## The Standard That Doesn't Change

```
Whoever OPENS the pull request is responsible for every line in
it - regardless of whether a human or an AI tool wrote the first
draft of any given line.
```

This is the core principle this entire module has been building toward: using an AI coding tool
doesn't create a new category of "AI-authored code" with a different accountability standard. The
person shipping the feature owns it, fully, exactly as if they had typed every character themselves.

## The "Can You Defend This Line?" Test

```
Someone in review asks: "Why did you use a Map here instead of a
plain object?"

Acceptable answer: "Because this needs O(1) lookups by a
non-string key, and a Map handles that more naturally than
coercing everything to string object keys."

UNACCEPTABLE answer: "That's what [the AI tool] generated."
```

If a developer genuinely cannot explain *why* a piece of AI-generated code works the way it does —
not just *that* it works — that's a clear signal the code isn't actually ready to ship, regardless
of how confident it looked or how quickly it was produced. This test is deliberately simple and
deliberately strict.

## A Practical Pre-Ship Checklist

```
☐ I've read every changed line, not just skimmed the diff
☐ I can explain WHY each non-trivial decision was made, not just
  WHAT it does
☐ I've checked edge cases the AI tool's prompt didn't explicitly
  cover
☐ I've verified it matches this codebase's existing conventions
  (per using-ai-coding-tools-like-a-senior-developer.md)
☐ Security-sensitive code has had a genuinely careful,
  security-focused read (per reviewing-ai-generated-code-when-
  to-trust-it-and-when-not-to.md)
☐ Tests exist, pass, AND I've reasoned about what they DON'T cover
```

This checklist is deliberately not AI-specific in most of its items — it's close to what a
disciplined engineer should already be doing before shipping *any* change. The AI-tool-specific
additions are narrow: verifying convention-matching and giving security-sensitive code extra
scrutiny, precisely because those are the areas where an AI tool's output most commonly needs a
human's deliberate correction.

## Why This Discipline Matters More, Not Less, as AI Tools Improve

```
A more capable AI coding tool produces code that's MORE
plausible-looking, MORE often correct, and therefore EASIER to
under-scrutinize - exactly the same "confident but wrong" risk
covered in why-hallucination-happens-it-predicts-it-doesnt-know.md,
now applied to code instead of prose.
```

This is a genuinely important, counter-intuitive point: as AI coding tools get better, the
temptation to skip careful review grows *stronger*, precisely because the output looks more
trustworthy on the surface — which is exactly when a rigorous, deliberate review discipline matters
most, not least.

## A Realistic Workflow, End to End

```
1. Write a clear, context-rich prompt (per using-ai-coding-tools-
   like-a-senior-developer.md)
2. Review the generated code with the SAME rigor as a human
   teammate's PR (per reviewing-ai-generated-code-when-to-trust-
   it-and-when-not-to.md)
3. Iterate with specific, targeted feedback rather than accepting
   the first draft wholesale
4. Run the FULL test suite, and reason about what it doesn't cover
5. Open the PR ready to defend every non-trivial line, in your
   OWN words, not the tool's
```

This is the practical synthesis of the entire module: using an AI coding tool well doesn't mean
using it less — it means directing it clearly, reviewing its output rigorously, and never
outsourcing the actual accountability for what ends up in the codebase.

## Common Mistakes

- Shipping a change where the "why" behind a non-trivial decision is genuinely unknown to the
  person shipping it, even if the "what" is technically correct.
- Treating a fast, confident-looking AI-generated result as a reason to skip the review rigor that
  would normally apply to a change of that size or risk.
- Letting review standards quietly erode over time as AI tools produce increasingly plausible-looking
  output, rather than holding the line on genuine understanding before shipping.

## Module Summary

Across this module: **using an AI coding tool well** means directing it with clear, context-rich
prompts that reference existing codebase patterns, and iterating on its output rather than accepting
a first draft wholesale — the senior-developer mindset applied to code generation (see
[using-ai-coding-tools-like-a-senior-developer.md](using-ai-coding-tools-like-a-senior-developer.md));
**reviewing AI-generated code** demands the exact same rigor as reviewing a human teammate's code —
no lighter standard, no free pass — with particular attention to edge cases, convention-matching,
and security-sensitive paths that a quick functional check would miss (see
[reviewing-ai-generated-code-when-to-trust-it-and-when-not-to.md](reviewing-ai-generated-code-when-to-trust-it-and-when-not-to.md));
and **shipping AI-assisted code** means genuinely owning every line — able to explain not just what
it does but why it was written that way — a discipline that matters more, not less, as AI coding
tools become more capable and their output more plausible-looking by default.
