# 📋 Guiding Models with Schema-Based Prompting

## The Portable Fallback

[using-model-supported-json-mode-for-structured-outputs.md](using-model-supported-json-mode-for-structured-outputs.md)
covered the native, most reliable mechanism — but it isn't universally available across every
provider, model, or SDK version. **Schema-based prompting** is the underlying technique that works
regardless: describing the exact desired JSON shape directly in the prompt text itself, applying
[writing-clear-instructions.md](../prompt-engineering-fundamentals/writing-clear-instructions.md)'s
clarity principle specifically to structure.

## A Concrete Example

```
Extract the contact information from the email below and respond
with ONLY a JSON object matching this exact shape, with no other
text before or after it:

{
  "name": string,
  "email": string,
  "plan_interest": string,
  "demo_requested": boolean
}

Email:
"John Smith (john@example.com) is interested in our Enterprise plan
and wants to schedule a demo for next Tuesday at 2pm."
```

Describing the shape directly — including the exact field names and expected types — gives the
model a concrete template to follow, applying
[few-shot-examples-to-force-pattern-learning.md](../prompt-engineering-fundamentals/few-shot-examples-to-force-pattern-learning.md)'s
"show, don't just tell" principle to a schema specifically, rather than a full worked example.

## This Is a Suggestion, Not a Guarantee

Recall
[why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md](../structured-output-in-ai-systems/why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md)'s
core point: a well-written schema-based prompt is genuinely effective — models follow it correctly
the overwhelming majority of the time — but it remains fundamentally different from native
JSON mode's constrained decoding. This is exactly why
[validating-the-returned-structure-before-using-it.md](validating-the-returned-structure-before-using-it.md)'s
validation step is **more critical**, not less, when relying on schema-based prompting rather than
a genuine structural guarantee.

## Reinforcing the Instruction Explicitly

```
Respond with ONLY the JSON object — no explanation, no markdown code
fences, no additional text before or after it.
```

A common, real failure mode of schema-based prompting is the model wrapping the JSON in explanatory
prose or a markdown code fence (```json ... ```) — explicitly instructing against this, per
[output-formatting-instructions-making-responses-predictable.md](../prompt-engineering-fundamentals/output-formatting-instructions-making-responses-predictable.md)'s
positive-instruction principle, measurably reduces this specific failure.

## When This Technique Is the Right Choice

- The specific provider or model genuinely doesn't offer native structured output support.
- A quick prototype where the setup overhead of a formal schema definition isn't yet worth it.
- A situation where the exact same prompt needs to work correctly across multiple different
  providers, some of which may lack native JSON mode.

## Common Mistakes

- Assuming schema-based prompting provides the same hard guarantee as native JSON mode — it's a
  strong, effective technique, not a structural guarantee.
- Forgetting to explicitly instruct against wrapping the JSON in prose or markdown code fences, a
  common and avoidable real failure mode.
- Skipping validation entirely because the schema was clearly described in the prompt — the
  description being clear doesn't guarantee the actual response always matches it perfectly.

## ➡️ Next

Continue to [basics-of-tool-function-calling.md](basics-of-tool-function-calling.md) to see a
third technique: using tool calling itself as a structured-output mechanism.
