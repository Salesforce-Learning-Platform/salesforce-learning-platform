# 🚦 Never Trust AI Output Without Validation

## A New Trust Boundary

Every backend system already treats one boundary as untrustworthy by default: user input. That's
why [request-validation.md](../../backend/rest-api-design/request-validation.md) exists — nothing
a client sends is trusted until it's checked. An LLM response is a **second, equally real trust
boundary**, even though it comes from "your own" AI provider rather than an external user.

## Why AI Output Deserves the Same Suspicion as User Input

```
USER INPUT is untrustworthy because:
  a person can type anything, including malicious or malformed data

AI OUTPUT is untrustworthy because:
  a model is fundamentally PROBABILISTIC (per
  deterministic-vs-probabilistic-outputs.md, in How LLMs Actually
  Work) — even a well-designed prompt with a schema attached can
  still produce a response that's malformed, incomplete, or simply
  wrong
```

Neither source gets to skip validation just because it's the "trusted" side of the request. A
model provider isn't adversarial the way a malicious user might be, but unpredictability alone is
enough reason to validate — intent doesn't matter, only whether the data can be relied upon.

## Structural Guarantees Still Aren't Business Guarantees

[generating-json-responses-from-llms](../generating-json-responses-from-llms/) already introduced
this distinction:

```
Native JSON mode / schema-based prompting / tool calling GUARANTEE:
  the response has the right shape and types (mostly)

NONE of them guarantee:
  the actual VALUES are correct, sensible, or safe to act on
```

This module goes one level deeper than that earlier introduction — treating Zod validation as a
first-class discipline for AI responses specifically, not just a single step tacked onto the end
of a generation call.

## The Mental Model: Validation Is the Airlock

```
AI Response → [ Zod Schema ] → Valid, typed data your code can trust
                    │
                    └─→ Invalid → handled explicitly, never silently passed through
```

Nothing produced by a model should reach a database write, a payment decision, a user-facing
message, or any other consequential action without first passing through this airlock. This is
true even when the same request already used native JSON mode or a strict tool schema — those
mechanisms narrow the space of likely failures, they don't eliminate it.

## Common Mistakes

- Assuming a provider that's usually reliable means validation can be skipped "just this once" —
  the rare failure is exactly the case validation exists to catch.
- Validating only on the "happy path" during development, then never testing what actually happens
  when the model returns something unexpected.
- Treating AI output as equivalent to internal, code-generated data — an LLM response is external
  input, structurally speaking, no matter which system produced it.

## ➡️ Next

Continue to [defining-a-validation-schema-using-zod.md](defining-a-validation-schema-using-zod.md)
to build validation schemas designed specifically for the shapes AI responses actually take.
