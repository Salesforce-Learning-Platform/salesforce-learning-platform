# 🎯 Using Model-Supported JSON Mode

## The Direct, Native Approach

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Extract the key information from this email: John Smith "
                    "(john@example.com) is interested in our Enterprise plan "
                    "and wants to schedule a demo for next Tuesday at 2pm.",
    }],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "plan_interest": {"type": "string"},
                    "demo_requested": {"type": "boolean"},
                },
                "required": ["name", "email", "plan_interest", "demo_requested"],
                "additionalProperties": False,
            },
        }
    },
)
```

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "plan_interest": "Enterprise",
  "demo_requested": true
}
```

`output_config.format` with `type: "json_schema"` invokes the model's native, schema-constrained
JSON mode directly — this is the concrete mechanism underneath
[how-structured-responses-make-ai-outputs-predictable-and-programmable.md](../structured-output-in-ai-systems/how-structured-responses-make-ai-outputs-predictable-and-programmable.md)'s
constrained decoding. The response comes back as pure, valid JSON text matching the schema exactly —
no tool-use wrapper, no surrounding prose, just the structured data itself.

## `additionalProperties: false` — Closing the Schema

```json
"additionalProperties": false
```

Setting `additionalProperties` to `false` tells the schema (and therefore the constrained
generation) that **no extra fields** beyond the ones explicitly declared are allowed — without it,
the model could technically add extra, unexpected fields the application code was never designed
to handle. This is a genuinely important detail for a schema meant to be strictly relied upon.

## `required` — Making Fields Genuinely Mandatory

```json
"required": ["name", "email", "plan_interest", "demo_requested"]
```

Listing fields in `required` guarantees they'll always be present in the response — directly
solving [why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md](../structured-output-in-ai-systems/why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md)'s
"missing fields" problem. A field left out of `required` is treated as genuinely optional, and code
consuming the response needs to handle its potential absence.

## When to Reach for This Native Mode

Native JSON mode is the right default choice whenever the actual provider and model support it
directly — it's the most direct, most reliable mechanism, with the fewest moving parts. The next
file, [guiding-models-with-schema-based-prompting.md](guiding-models-with-schema-based-prompting.md),
covers the fallback for situations where this native support isn't available or isn't being used.

## Common Mistakes

- Omitting `additionalProperties: false`, unintentionally allowing the model to add extra,
  unexpected fields the application wasn't designed to handle.
- Leaving a field that's actually always needed out of the `required` list, forcing the application
  to defensively handle an absence that should never genuinely happen.
- Using native JSON mode when the actual goal is having the model *call a real function/tool*
  rather than just return data — that's a different mechanism, covered in
  [basics-of-tool-function-calling.md](basics-of-tool-function-calling.md).

## ➡️ Next

Continue to
[guiding-models-with-schema-based-prompting.md](guiding-models-with-schema-based-prompting.md) for
a more portable technique, useful when native JSON mode isn't available.
