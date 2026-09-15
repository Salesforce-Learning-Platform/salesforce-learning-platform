# 🔨 Basics of Tool/Function Calling — as a Structured Output Technique

## A Preview, Not the Full Picture

[Function Calling and Tool Calling](../function-calling-tool-calling/), later in this domain,
covers tool calling fully — as the mechanism letting an AI genuinely trigger real actions in an
application. This file covers a narrower, specific use of the same underlying feature: using tool
calling purely as **another technique for extracting reliably structured data**, even when no real
action is ever actually taken.

## Defining a "Tool" That's Really Just a Data Shape

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Extract contact info from: John Smith (john@example.com)..."}],
    tools=[
        {
            "name": "extract_contact",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
                "required": ["name", "email"],
                "additionalProperties": False,
            },
        }
    ],
)
```

This "tool" (`extract_contact`) never actually does anything when called — there's no real function
behind it performing an action. It exists purely to give the model a **structured shape to fill
in**, with `strict: true` guaranteeing the filled-in arguments genuinely match the declared schema —
directly comparable to
[using-model-supported-json-mode-for-structured-outputs.md](using-model-supported-json-mode-for-structured-outputs.md)'s
native JSON mode, just expressed through the tool-calling mechanism instead.

## The Real Difference From Native JSON Mode

```
NATIVE JSON MODE: the response is pure text, directly containing
the JSON — read `response.content[0].text`

TOOL-BASED: the structured data appears inside a "tool_use" content
block, alongside (or instead of) any plain text — read
`response.content[0].input` from that block
```

The data ends up in a genuinely different place in the response structure — tool-based extraction
wraps the result in a `tool_use` block rather than returning it as the plain response text. Both
approaches provide the same underlying structural guarantee; the choice between them is largely
about which one fits more naturally into an existing codebase, especially one that already uses
tool calling for other, genuinely action-triggering purposes.

## When Tool-Based Extraction Genuinely Makes Sense

- A codebase that already has infrastructure for handling `tool_use` responses (per the upcoming
  [Function Calling module](../function-calling-tool-calling/)), where reusing that same handling
  path for pure data extraction avoids building a second, separate code path.
- A situation combining genuine action-taking *and* structured data extraction in the same request —
  some tools that do real things, alongside one that's purely for shaping a specific piece of
  extracted data.

## Common Mistakes

- Reaching for tool calling as the default structured-output mechanism when native JSON mode (per
  [using-model-supported-json-mode-for-structured-outputs.md](using-model-supported-json-mode-for-structured-outputs.md))
  would be simpler for a case with no genuine actions involved at all.
- Forgetting `strict: true` on a tool meant purely for structured extraction, losing the schema
  guarantee that's the entire point of using it this way.
- Confusing this narrow, extraction-only use of tool calling with the full agentic capability
  covered in [Function Calling and Tool Calling](../function-calling-tool-calling/) — this file is
  specifically about the structured-output angle, not real action-taking.

## ➡️ Next

Continue to
[validating-the-returned-structure-before-using-it.md](validating-the-returned-structure-before-using-it.md)
to see why every one of these techniques still benefits from a validation step afterward.
