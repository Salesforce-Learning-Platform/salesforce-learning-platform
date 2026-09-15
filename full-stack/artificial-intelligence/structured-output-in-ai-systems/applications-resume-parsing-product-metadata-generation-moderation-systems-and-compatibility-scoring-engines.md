# 🏗️ Real Applications of Structured Output

## Resume Parsing

```python
class ParsedResume(BaseModel):
    name: str
    email: str
    years_of_experience: int
    skills: list[str]
    most_recent_title: str
```

A hiring platform extracting structured candidate data from an uploaded resume's raw text needs a
**consistent, guaranteed** shape to actually store in its database (per
[Database Design and Modeling](../../backend/database-design-and-modeling/)) and search against —
an occasionally-malformed or inconsistently-shaped extraction would silently corrupt real
candidate records.

## Product Metadata Generation

```python
class ProductMetadata(BaseModel):
    category: str
    tags: list[str]
    suggested_price_range: str
    target_audience: str
```

An e-commerce platform generating structured metadata for a newly listed product — tags for search,
a suggested category, a target audience — needs that output to slot directly into the exact same
[REST API](../../backend/rest-api-design/)'s expected request shape used for manually-entered
product data, with no special-case handling for "AI-generated" versus "human-entered" data.

## Content Moderation Systems

```python
class ModerationResult(BaseModel):
    flagged: bool
    reason: str | None
    severity: str  # "low" | "medium" | "high"
```

A moderation system reviewing user-generated content needs a **reliably actionable** result — code
downstream needs to know, with certainty, whether `flagged` is genuinely `true` or `false`, not a
value that might occasionally arrive as a string or be missing entirely. This is a genuinely
high-stakes case: an unpredictable or malformed moderation response could mean real, harmful
content slipping through entirely undetected.

## Compatibility Scoring Engines

```python
class CompatibilityScore(BaseModel):
    score: float  # 0.0 to 1.0
    matching_factors: list[str]
    explanation: str
```

A system scoring compatibility between two entities (candidates and job postings, users on a
matching platform) needs a numeric `score` genuinely guaranteed to be a real, usable number — not
a value that might arrive as `"pretty high"` in one response and `0.87` in another, which would
make any kind of reliable sorting or ranking logic impossible to build on top of.

## What These Examples Have in Common

Every one of these systems has the same underlying shape: **an LLM's output feeds directly into
real, automated downstream logic** — a database write, a ranking algorithm, a moderation decision —
with no human reviewing and manually correcting the raw output first. This is exactly the situation
where the genuine, structural guarantee from
[how-structured-responses-make-ai-outputs-predictable-and-programmable.md](how-structured-responses-make-ai-outputs-predictable-and-programmable.md)
stops being a nice-to-have and becomes a real requirement.

## Common Mistakes

- Using structured output for a case where a human always reviews the raw response before it's
  used — the guarantee matters most specifically for fully-automated downstream logic.
- Designing a schema that's technically valid but doesn't actually capture what the downstream
  system genuinely needs (a `score` field with no defined range, for instance).
- Underestimating the real, concrete risk of unstructured output specifically in a high-stakes case
  like content moderation, where a malformed response could mean real harm going undetected.

## Module Summary

Across this module: unstructured, free-text LLM output causes real, concrete problems for
downstream application code — parsing failures, missing fields, type inconsistencies — none of
which "asking nicely" in a prompt reliably prevents (see
[why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md](why-unstructured-ai-responses-are-difficult-to-use-in-real-systems.md));
**structured outputs**, via schema-constrained decoding, provide a genuine structural guarantee —
always-valid, always-typed output — rather than a mere suggestion (see
[how-structured-responses-make-ai-outputs-predictable-and-programmable.md](how-structured-responses-make-ai-outputs-predictable-and-programmable.md));
and this guarantee earns its real value specifically in systems — resume parsing, product metadata,
moderation, compatibility scoring — where an LLM's output feeds directly into fully-automated
downstream logic with no human reviewing it first.
