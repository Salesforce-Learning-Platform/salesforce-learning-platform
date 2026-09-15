# 🔍 Verifying AI Responses Against a Schema

## `safeParse()` Over `parse()` — Always, for AI Output

```js
// AVOID for AI responses — throws on failure
const data = ResponseSchema.parse(aiResponse);

// PREFER for AI responses — never throws
const result = ResponseSchema.safeParse(aiResponse);
if (result.success) {
  // result.data is fully typed and validated
} else {
  // result.error holds the validation failure details
}
```

`.parse()` throws an exception the instant validation fails. For AI responses specifically —
inherently unpredictable, per
[never-trust-ai-output-without-validation.md](never-trust-ai-output-without-validation.md) —
an uncaught throw is exactly the kind of surprise a production system shouldn't have to guard
against with a wrapping `try`/`catch` everywhere it happens. `.safeParse()` returns a plain result
object instead, making the failure path an explicit, ordinary branch in the code rather than an
exception to catch.

## Reading a Failed Result

```js
const result = ResponseSchema.safeParse(aiResponse);

if (!result.success) {
  console.log(result.error.issues);
  // [{ code: "invalid_type", path: ["score"], message: "..." }, ...]
}
```

`result.error` is a `ZodError` whose `.issues` array lists every individual problem found — each
with a `path` (which field failed) and a `message` (why). This is already enough detail for a
console log during development, but real applications usually want the errors reshaped for
logging or monitoring, not the raw array.

## `z.flattenError()` — Errors From a Flat Schema

```js
import { z } from "zod";

const flat = z.flattenError(result.error);
// {
//   formErrors: [],
//   fieldErrors: { score: ["Number must be <= 100"] }
// }
```

For a schema without deep nesting, `z.flattenError()` reorganizes the issues into `fieldErrors`
(keyed by field name) and `formErrors` (top-level problems not tied to one field) — a shape that's
immediately useful for logging exactly which fields the model got wrong, without walking the raw
issues array manually.

## `z.treeifyError()` — Errors From a Nested Schema

```js
const tree = z.treeifyError(result.error);
// {
//   properties: {
//     suggestions: {
//       items: [{ errors: ["priority must be one of low, medium, high"] }]
//     }
//   }
// }
```

For a schema with nested objects or arrays of objects (like `building-structured-profile-analysis-
data-with-scores-strengths-and-suggestions.md`'s `suggestions` array, from the previous module),
`z.treeifyError()` produces a structure that mirrors the schema's own shape — making it far easier
to find exactly which nested field, inside which array item, actually failed.

## A Reusable Verification Helper

```js
function verifyAiResponse(schema, rawResponse, { context } = {}) {
  const result = schema.safeParse(rawResponse);

  if (!result.success) {
    console.error(`AI response failed validation${context ? ` (${context})` : ""}:`,
                   z.flattenError(result.error));
    return { ok: false, error: result.error };
  }

  return { ok: true, data: result.data };
}
```

Wrapping `.safeParse()` plus structured logging into one small, reusable function — used
consistently across every place an AI response gets validated — keeps the failure-handling logic in
one place rather than repeated ad hoc at every call site.

## Common Mistakes

- Using `.parse()` on AI output and letting the resulting exception crash an unrelated part of the
  request instead of handling it deliberately.
- Logging only `result.error` directly (a dense, nested `ZodError` object) instead of
  `z.flattenError()` or `z.treeifyError()`, making the logs far harder to actually read later.
- Checking `result.success` but then never actually reading `result.error` on failure, losing the
  detail needed to understand and eventually fix the pattern of failure.

## ➡️ Next

Continue to
[handling-invalid-or-mismatched-responses.md](handling-invalid-or-mismatched-responses.md) to
decide what an application should actually do once a validation failure like this is detected.
