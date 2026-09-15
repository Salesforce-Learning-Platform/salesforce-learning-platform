# 🎯 Few-Shot Examples: Forcing Pattern Learning

## Showing, Not Just Telling

[writing-clear-instructions.md](writing-clear-instructions.md) covered explaining what you want in
words. **Few-shot** (or "multishot") **prompting** goes further: providing actual, concrete
examples of the exact input-output pattern you want. This is consistently one of the most reliable
ways to steer a model's output format, tone, and structure — often more reliable than a purely
verbal description alone.

## A Concrete Example

```
<examples>
<example>
Input: "The delivery was late and the box was damaged."
Output: {"sentiment": "negative", "category": "shipping"}
</example>
<example>
Input: "Fast shipping, exactly as described!"
Output: {"sentiment": "positive", "category": "shipping"}
</example>
</examples>

Now classify this review: "Great product but took forever to arrive."
```

Rather than describing the exact desired JSON shape in words alone, showing a couple of real
input-output pairs lets the model directly infer the pattern — the exact field names, the exact
value format — from concrete demonstration, which tends to produce more consistent results than a
purely abstract description.

## What Makes an Example Genuinely Good

- **Relevant** — the examples should closely mirror your actual real use case, not a
  loosely-related generic one.
- **Diverse** — examples should cover real edge cases and vary enough that the model doesn't
  accidentally pick up an *unintended* pattern (like always assuming a specific input length, or a
  specific category, just because every example happened to share that trait).
- **Structured** — wrapping examples in explicit tags (like `<example>`, with multiple examples
  inside `<examples>`) lets the model clearly distinguish them from the surrounding instructions,
  rather than risking them blending together ambiguously.

## How Many Examples Is Enough

The generally recommended range is **3 to 5** examples for solid results — few enough to keep the
prompt reasonably sized (directly connecting to
[cost-awareness](../calling-llm-apis-properly/cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md)'s
concern about unnecessary token cost), but enough to genuinely demonstrate the real pattern,
including at least one or two edge cases.

## The Risk: Accidentally Teaching the Wrong Pattern

```
If EVERY example given happens to be a short, one-sentence review,
the model may implicitly learn "reviews are always one sentence" —
an UNINTENDED pattern, not the one actually meant to be taught.
```

This is exactly why diversity in the chosen examples matters, not just relevance — a set of
examples that are too similar to each other risks teaching the model an accidental, narrower
pattern than genuinely intended, purely because every example happened to share some irrelevant
trait in common.

## Common Mistakes

- Providing only one or two very similar examples, giving the model too little signal to reliably
  distinguish the intended pattern from incidental similarities.
- Choosing examples that don't genuinely represent the real range of inputs the task will actually
  encounter, producing a model that performs well only on inputs resembling the examples closely.
- Mixing examples directly into the instructions without any clear structural separation, risking
  the model misinterpreting an example as part of the actual instructions themselves.

## ➡️ Next

Continue to
[chain-of-thought-high-level-awareness.md](chain-of-thought-high-level-awareness.md) to see a
different technique: asking the model to reason step by step, rather than showing it examples.
