# ✅ Validating the Returned Structure Before Using It

## What a Schema Guarantee Actually Covers — and Doesn't

Every technique in this module — native JSON mode, schema-based prompting, tool-based extraction —
guarantees (with varying strength) that a response has the **correct shape and types**. None of
them guarantee the **values themselves make genuine business sense**. A `score` field that's
technically a valid number, correctly typed, could still be `-5` or `9999` — structurally perfect,
but nonsensical for a scale meant to run from 0 to 100.

## Validating With Zod — Applying What You Already Know

```js
import { z } from "zod";

const CompatibilitySchema = z.object({
  score: z.number().min(0).max(100),
  matchingFactors: z.array(z.string()).min(1),
  explanation: z.string().min(10),
});

const result = CompatibilitySchema.safeParse(aiResponse);
if (!result.success) {
  // handle a response that's structurally valid JSON, but fails a
  // genuine BUSINESS rule — e.g. score out of the expected 0-100 range
  logInvalidAiResponse(result.error);
  return fallbackResponse();
}
```

This is the exact same [Zod validation pattern](../../backend/rest-api-design/request-validation.md)
already covered for validating REST API input — applied here to AI-generated data instead of
user-submitted data. `.min()`/`.max()` constraints catch exactly the kind of "technically valid,
actually wrong" value a bare type check alone would miss.

## Why This Matters Even With Native JSON Mode's Strong Guarantee

```
Native JSON mode GUARANTEES: score is a real number
Native JSON mode does NOT guarantee: score is actually between 0-100,
matchingFactors has at least one real, meaningful entry, or
explanation is genuinely substantive rather than a single word
```

A JSON schema (the kind used by `output_config.format`) can express *some* of these constraints
directly (a `minimum`/`maximum` on a number, for instance) — but real business logic often goes
beyond what a JSON schema alone can practically express, which is exactly where a dedicated
validation library earns its place even on top of an already schema-constrained response.

## A Realistic, Layered Approach

```
1. Generate with native JSON mode or a tool — structural guarantee
2. Validate with Zod — business-rule guarantee
3. On validation failure — retry, use a fallback, or surface a clear
   error, NEVER silently pass through invalid data
```

Treating structural guarantee and business-rule validation as two genuinely separate, layered
steps — never assuming one covers the other — is the practically correct approach for any AI
response that feeds into real, consequential downstream logic.

## What to Do When Validation Actually Fails

A validation failure on AI-generated data shouldn't be treated identically to a validation failure
on user input (per
[request-validation.md](../../backend/rest-api-design/request-validation.md)) — while a user
genuinely made an input mistake, an AI response failing validation despite a correct schema often
signals a legitimate model error worth logging and monitoring, and sometimes worth a single retry
(the same reasoning
[Error Handling in AI Applications](../error-handling-in-ai-applications/), later in this domain,
covers in full).

## Common Mistakes

- Assuming a schema-constrained response needs no further validation at all, missing real
  business-rule violations a type-level schema alone can't express.
- Silently accepting an invalid AI response rather than logging it, retrying, or falling back —
  losing visibility into how often the model is genuinely producing incorrect results.
- Writing validation logic that only checks types, duplicating exactly what the schema already
  guaranteed, rather than checking the genuinely new, business-specific constraints that matter.

## ➡️ Next

Continue to
[building-structured-profile-analysis-data-with-scores-strengths-and-suggestions.md](building-structured-profile-analysis-data-with-scores-strengths-and-suggestions.md)
to see every technique from this module combined into one complete, realistic example.
