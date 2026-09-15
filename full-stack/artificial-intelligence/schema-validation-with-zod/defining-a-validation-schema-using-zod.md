# 🏗️ Defining a Validation Schema Using Zod

## Beyond the Basics

The previous module used a simple, flat Zod schema. AI responses in real applications are often
messier than that — a field the model might reasonably omit, a response that could legitimately be
one of several different shapes, or a value that's individually well-typed but still wrong given
the other fields around it. Zod has dedicated tools for exactly these situations.

## Optional and Nullable Fields — Modeling What the Model Might Skip

```js
import { z } from "zod";

const SummarySchema = z.object({
  title: z.string(),
  summary: z.string(),
  tags: z.array(z.string()).optional(),      // the model may leave this out entirely
  sentiment: z.enum(["positive", "neutral", "negative"]).nullable(), // may be explicitly null
});
```

`.optional()` allows a field to be **missing** from the response; `.nullable()` allows it to be
**present but `null`**. These are genuinely different situations, and conflating them is a common
source of confusing validation failures — a schema expecting `.nullable()` still rejects a response
that omits the field entirely.

## `.default()` — Graceful Handling of Common Omissions

```js
const AnalysisSchema = z.object({
  score: z.number().min(0).max(100),
  confidence: z.number().min(0).max(1).default(0.5),
});

AnalysisSchema.parse({ score: 82 });
// => { score: 82, confidence: 0.5 }
```

For a field the model frequently omits despite being asked for it, `.default()` fills in a
sensible fallback automatically, rather than treating every omission as an outright validation
failure. Reach for this specifically when the omission is common enough to plan for, not for
fields whose absence should genuinely be treated as an error.

## `z.discriminatedUnion()` — Modeling "One of Several Shapes"

```js
const ClassificationResultSchema = z.discriminatedUnion("status", [
  z.object({
    status: z.literal("classified"),
    category: z.string(),
    confidence: z.number(),
  }),
  z.object({
    status: z.literal("uncertain"),
    reason: z.string(),
  }),
]);
```

Many realistic AI responses aren't one fixed shape — a classification task might return a confident
result *or* an explicit "uncertain" response with a different set of fields. `z.discriminatedUnion`
uses one shared field (here, `status`) to determine which shape to validate against, giving each
branch its own precise schema rather than one loose schema with everything marked optional.

## `.refine()` — Cross-Field Business Rules

```js
const DateRangeSchema = z.object({
  startDate: z.string(),
  endDate: z.string(),
}).refine((data) => new Date(data.endDate) > new Date(data.startDate), {
  error: "endDate must be after startDate",
});
```

Some rules genuinely depend on more than one field at once — a type-level schema alone can't
express "`endDate` must come after `startDate`". `.refine()` runs a custom function across the
already-parsed data and lets a schema enforce exactly this kind of relationship, with its own
explicit `error` message when it fails.

## When Optional/Default Becomes a Risk

```
Good use of .optional(): a "tags" field the model may reasonably skip
for short content

Bad use of .optional(): making "score" optional because the model
SOMETIMES forgets it — that's a sign the PROMPT needs fixing (per
writing-clear-instructions.md), not that validation should quietly
accept the gap
```

`.optional()` and `.default()` are tools for genuinely optional data, not a way to paper over a
prompt that isn't reliably producing a required field. Treat a required field's frequent omission
as a prompt-engineering problem to fix at the source.

## Common Mistakes

- Confusing `.optional()` and `.nullable()`, causing a schema to reject an otherwise valid response
  in the wrong situation.
- Reaching for `.default()` to hide a required field's genuine, repeated omission rather than fixing
  the underlying prompt.
- Building one large, loosely-typed schema with everything optional instead of a
  `z.discriminatedUnion()` when the response genuinely takes one of a few distinct shapes.

## ➡️ Next

Continue to
[verifying-ai-responses-against-a-schema.md](verifying-ai-responses-against-a-schema.md) to see how
to actually run these schemas against a live AI response.
