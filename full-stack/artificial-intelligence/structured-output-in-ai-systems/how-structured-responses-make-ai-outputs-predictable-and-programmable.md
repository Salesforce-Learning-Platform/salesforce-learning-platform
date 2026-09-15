# 🔧 How Structured Responses Make AI Outputs Predictable and Programmable

## From "Strong Suggestion" to Genuine Guarantee

[why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md](why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md)
established the problem: a prompt-level JSON request is a strong suggestion, not a guarantee.
**Structured outputs** solve this with a genuinely different mechanism: **constrained decoding** —
the model is technically restricted, during generation itself, to only produce tokens that keep the
output valid according to a defined schema. This isn't "the model was asked nicely and complied";
it's "the model was structurally prevented from producing anything else."

## Defining the Shape You Want

```python
from pydantic import BaseModel

class ContactInfo(BaseModel):
    name: str
    email: str
    plan_interest: str
    demo_requested: bool
```

A **schema** (here, a Pydantic model — a Python equivalent of the
[Zod schemas](../../backend/rest-api-design/request-validation.md) already covered for validating
REST API input) declares exactly what fields the response must have, and their exact types —
`name` must be a string, `demo_requested` must be a genuine boolean, not a string that merely looks
like one.

## The Actual Request

```python
response = client.messages.parse(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Extract info from: John Smith (john@example.com) wants Enterprise plan demo Tuesday 2pm"
    }],
    output_format=ContactInfo,
)

print(response.parsed_output)
# ContactInfo(name='John Smith', email='john@example.com',
#             plan_interest='Enterprise', demo_requested=True)
```

Passing the schema as `output_format` (rather than merely describing the desired shape in the
prompt text) is what actually invokes constrained decoding — the response comes back already
validated against the schema, ready to use directly as a real, typed object, with no manual
`JSON.parse()` or defensive shape-checking required at all.

## What This Genuinely Guarantees

- **Always valid JSON** — no `JSON.parse()` failure is structurally possible.
- **Type-safe fields** — every field is guaranteed to actually be the declared type, not just
  something that superficially resembles it.
- **No schema-violation retries needed** — since the response can't violate the schema in the first
  place, the retry logic that would otherwise be needed for malformed output becomes unnecessary
  for this specific failure mode.

## Two Related, Complementary Features

Structured output for an entire response and **strict tool use** (validating a tool's *parameters*
against a schema, covered in [Function Calling](../function-calling-tool-calling/)) are related but
distinct: one guarantees the overall shape of a response; the other guarantees the shape of
arguments passed to a specific callable action. Real, more advanced agentic workflows frequently use
both together.

## Common Mistakes

- Confusing a prompt-level request for JSON with genuine, schema-constrained structured output —
  only the latter provides an actual structural guarantee, per
  [why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md](why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md).
- Defining an overly loose or vague schema (every field optional, permissive types), losing much of
  the real value structured output is meant to provide.
- Still writing defensive JSON-parsing logic downstream of a genuinely structured-output request,
  duplicating a guarantee the feature itself already provides.

## ➡️ Next

Continue to
[applications-resume-parsing-product-metadata-generation-moderation-systems-and-compatibility-scoring-engines.md](applications-resume-parsing-product-metadata-generation-moderation-systems-and-compatibility-scoring-engines.md)
to see real, concrete systems built on exactly this guarantee.
