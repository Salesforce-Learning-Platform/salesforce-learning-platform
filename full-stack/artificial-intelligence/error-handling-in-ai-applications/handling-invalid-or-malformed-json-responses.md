# 🩹 Handling Invalid or Malformed JSON Responses

## Bringing the Pieces Together

Several earlier modules already built the individual pieces this file assembles into one coherent
picture: [Schema Validation with Zod](../schema-validation-with-zod/) covered detecting and
responding to a validation failure, and
[Generating JSON Responses from LLMs](../generating-json-responses-from-llms/) covered the
techniques that produce structured output in the first place. This file is about the application-
wide *pattern* for handling this specific failure category consistently, everywhere it can occur.

## The Failure Category, Precisely

```
"Invalid or malformed JSON" covers TWO distinct sub-cases:

1. Not valid JSON at all — e.g. the model wrapped it in prose or
   a markdown fence despite instructions not to
2. Valid JSON, but failing the SCHEMA — e.g. missing a required
   field, or a value out of range
```

These two sub-cases need slightly different first steps, even though both end up going through the
same Zod validation step eventually.

## Step 1: Safely Attempting to Parse

```js
function safeJsonParse(rawText) {
  try {
    return { ok: true, data: JSON.parse(rawText) };
  } catch (err) {
    return { ok: false, error: err };
  }
}
```

Sub-case 1 — text that isn't valid JSON at all — needs to be caught *before* Zod ever sees it,
since `JSON.parse()` itself throws on malformed input. Wrapping this in its own explicit
`try`/`catch` keeps this specific failure distinguishable from a schema-validation failure.

## Step 2: Stripping Common Wrapping Artifacts First

```js
function stripMarkdownFence(text) {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
  return fenced ? fenced[1] : text;
}
```

A very common, specific failure mode — the model wrapping otherwise-valid JSON in a ` ```json `
code fence despite being told not to (per
[guiding-models-with-schema-based-prompting.md](../generating-json-responses-from-llms/guiding-models-with-schema-based-prompting.md))
— is worth handling as a small, deliberate pre-processing step before attempting to parse, rather
than treating it as a hard failure. This single fix recovers a meaningful fraction of "malformed
JSON" failures in practice.

## Step 3: The Full Pipeline

```js
async function getStructuredAiResponse(schema, rawText, context) {
  const cleaned = stripMarkdownFence(rawText);
  const parsed = safeJsonParse(cleaned);

  if (!parsed.ok) {
    logAiFailure({ context, stage: "json_parse", rawText });
    return { ok: false, reason: "not_valid_json" };
  }

  const validated = schema.safeParse(parsed.data);
  if (!validated.success) {
    logAiFailure({ context, stage: "schema_validation", errors: z.flattenError(validated.error) });
    return { ok: false, reason: "schema_mismatch" };
  }

  return { ok: true, data: validated.data };
}
```

This combined pipeline distinguishes exactly *where* a response failed — not valid JSON at all,
versus valid JSON that doesn't match the schema — which matters enormously for diagnosing a
recurring problem later (a topic
[logging-ai-requests-and-responses-for-debugging.md](logging-ai-requests-and-responses-for-debugging.md),
later in this module, covers in full).

## Common Mistakes

- Letting `JSON.parse()` throw uncaught, crashing a request instead of treating a parse failure as
  an ordinary, expected outcome to handle.
- Treating "not valid JSON" and "valid JSON that fails the schema" as the same failure, losing the
  diagnostic value of knowing which one actually happened.
- Reaching immediately for a full retry (the next file's territory) for a case a simple, cheap fix
  like stripping a markdown fence could resolve without another API call.

## ➡️ Next

Continue to
[managing-partial-responses-and-timeouts.md](managing-partial-responses-and-timeouts.md) for the
second major failure category: a response that never fully arrives at all.
