# 🧩 Building Structured Profile Analysis Data

## The Scenario: Analyzing a User Profile

A real application — a professional networking platform, a job-matching service — wants to use an
LLM to analyze a user's profile and produce structured feedback: an overall score, a list of
strengths, and concrete suggestions for improvement. This combines every technique from this module
into one complete, realistic example.

## Step 1: Define the Schema

```js
import { z } from "zod";

const ProfileAnalysisSchema = z.object({
  overallScore: z.number().min(0).max(100),
  strengths: z.array(z.string()).min(1).max(5),
  suggestions: z.array(
    z.object({
      area: z.string(),
      suggestion: z.string(),
      priority: z.enum(["low", "medium", "high"]),
    })
  ).min(1),
});
```

This Zod schema does double duty: it defines the shape used for
[validating-the-returned-structure-before-using-it.md](validating-the-returned-structure-before-using-it.md),
and its structure directly informs the JSON schema passed to the model.

## Step 2: Generate with Native JSON Mode

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Analyze this professional profile and provide structured "
                    f"feedback:\n\n{profile_text}",
    }],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "overallScore": {"type": "number", "minimum": 0, "maximum": 100},
                    "strengths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                        "maxItems": 5,
                    },
                    "suggestions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "area": {"type": "string"},
                                "suggestion": {"type": "string"},
                                "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                            },
                            "required": ["area", "suggestion", "priority"],
                            "additionalProperties": False,
                        },
                        "minItems": 1,
                    },
                },
                "required": ["overallScore", "strengths", "suggestions"],
                "additionalProperties": False,
            },
        }
    },
)
```

Directly per
[using-model-supported-json-mode-for-structured-outputs.md](using-model-supported-json-mode-for-structured-outputs.md),
this guarantees the response's shape and types before it's ever validated in the application.

## Step 3: Validate Before Trusting It

```js
const result = ProfileAnalysisSchema.safeParse(JSON.parse(response.content[0].text));

if (!result.success) {
  logInvalidAiResponse(result.error); // per validating-the-returned-structure-before-using-it.md
  throw new AppError("Profile analysis failed — please try again", 500);
}

const analysis = result.data; // now genuinely, fully trustworthy
```

Even with the schema-constrained guarantee from Step 2, this validation step still catches anything
the JSON schema alone couldn't fully express, and gives the application a clean, explicit failure
path rather than silently trusting unvalidated data.

## Step 4: Use the Result

```js
app.post("/profile/analyze", requireAuth, async (req, res) => {
  const analysis = await analyzeProfile(req.user.profile); // Steps 1-3, wrapped together
  await saveAnalysisToDatabase(req.user.id, analysis);
  res.status(201).json(analysis);
});
```

The fully validated `analysis` object now flows directly into the rest of the application exactly
like any other trusted, well-shaped data — persisted to the database (per
[Database Design and Modeling](../../backend/database-design-and-modeling/)) and returned to the
client through an ordinary REST response (per
[REST API Design](../../backend/rest-api-design/)), with no special-casing needed anywhere
downstream for the fact that this particular data originated from an LLM.

## Common Mistakes

- Skipping the validation step because the schema-constrained generation "already guarantees it's
  correct" — the guarantee covers shape and type, not every business rule.
- Defining the Zod schema and the JSON schema passed to the model inconsistently, letting them
  quietly drift apart over time as one is updated without the other.
- Treating a validation failure as a reason to crash the whole request instead of returning a
  clear, well-formed error the client can actually act on.

## Module Summary

Across this module: **native JSON mode**, via `output_config.format`, provides the most direct,
reliable structural guarantee when a provider supports it (see
[using-model-supported-json-mode-for-structured-outputs.md](using-model-supported-json-mode-for-structured-outputs.md));
**schema-based prompting** is a portable, effective fallback describing the desired shape directly
in the prompt, without the same hard guarantee (see
[guiding-models-with-schema-based-prompting.md](guiding-models-with-schema-based-prompting.md));
**tool calling** offers a third technique for structured extraction specifically, distinct from its
full agentic use (see [basics-of-tool-function-calling.md](basics-of-tool-function-calling.md));
**validation** with Zod remains essential even after schema-constrained generation, since a schema
guarantees shape and type but never genuine business-rule correctness (see
[validating-the-returned-structure-before-using-it.md](validating-the-returned-structure-before-using-it.md));
and a complete, realistic pipeline — schema definition, generation, validation, then use — combines
every technique into one trustworthy, production-ready flow.
