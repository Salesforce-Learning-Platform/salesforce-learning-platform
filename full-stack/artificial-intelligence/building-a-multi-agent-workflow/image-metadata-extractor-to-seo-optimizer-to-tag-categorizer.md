# 🖼️ Pipeline 2: Image Metadata Extractor → SEO Optimizer → Tag Categorizer

## A Second Domain, the Same Pipeline Shape

Consider an e-commerce or content platform feature: given an uploaded product image, (1) extract a
description and key visual attributes, (2) generate SEO-optimized alt text and a title, and (3)
categorize it into the platform's existing tag taxonomy. This pipeline follows the exact same
sequential shape as
[the profile pipeline](profile-analyzer-to-bio-improver-to-conversation-starter-generator.md), but
applied to a genuinely different domain and, this time, starting from an **image** rather than
text.

## Stage 1: Image Metadata Extractor

```python
from pydantic import BaseModel, Field

class ImageMetadata(BaseModel):
    description: str
    dominant_colors: list[str] = Field(min_length=1, max_length=5)
    detected_objects: list[str]

def extract_metadata(image_base64):
    response = client.messages.create(
        model="claude-opus-5", max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_base64}},
                {"type": "text", "text": "Describe this product image: its description, dominant colors, and visible objects."},
            ],
        }],
        output_config={"format": {"type": "json_schema", "schema": METADATA_JSON_SCHEMA}},
    )
    return ImageMetadata.model_validate_json(response.content[0].text)
```

This stage uses Claude's native multimodal capability — an `image` content block alongside `text`,
in the same `content` array structure covered throughout this domain — to turn raw pixel data into
structured, textual metadata the next two stages can actually work with. Neither later stage ever
needs to see the image itself again.

## Stage 2: SEO Optimizer

```python
class SeoContent(BaseModel):
    title: str = Field(max_length=60)      # a real, common SEO constraint
    alt_text: str = Field(max_length=125)  # a real, common accessibility/SEO constraint

def optimize_seo(metadata: ImageMetadata):
    prompt = f"""Product description: {metadata.description}
Colors: {metadata.dominant_colors}
Objects: {metadata.detected_objects}

Generate an SEO-optimized product title (max 60 characters) and
descriptive alt text (max 125 characters) for accessibility."""

    response = client.messages.create(
        model="claude-opus-5", max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": SEO_JSON_SCHEMA}},
    )
    return SeoContent.model_validate_json(response.content[0].text)
```

Notice the schema itself encodes real, domain-specific constraints — a 60-character title limit and
a 125-character alt-text limit are genuine, well-known SEO/accessibility conventions, not arbitrary
numbers. This is the same idea as
[defining-a-validation-schema-using-zod.md](../schema-validation-with-zod/defining-a-validation-schema-using-zod.md)'s
guidance: a schema should encode real business rules, not just basic types.

## Stage 3: Tag Categorizer

```python
class Categorization(BaseModel):
    category: str
    tags: list[str] = Field(min_length=1, max_length=10)

EXISTING_CATEGORIES = ["Apparel", "Electronics", "Home & Garden", "Sporting Goods"]  # your real taxonomy

def categorize(metadata: ImageMetadata):
    prompt = f"""Product description: {metadata.description}
Objects detected: {metadata.detected_objects}

Choose the SINGLE best-fitting category from this exact list:
{EXISTING_CATEGORIES}

Then generate up to 10 relevant search tags."""

    response = client.messages.create(
        model="claude-opus-5", max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": CATEGORY_JSON_SCHEMA}},
    )
    result = Categorization.model_validate_json(response.content[0].text)

    if result.category not in EXISTING_CATEGORIES:  # a business-rule check the schema alone can't express
        raise PipelineStageError("tag-categorizer", f"Unknown category: {result.category}")
    return result
```

This stage includes an extra check beyond schema validation: confirming the returned `category` is
genuinely one of the platform's *existing* categories. This is exactly the distinction
[verifying-ai-responses-against-a-schema.md](../schema-validation-with-zod/verifying-ai-responses-against-a-schema.md)
established — a schema guarantees `category` is a string, but only an explicit business-rule check
guarantees it's a category that actually exists in the platform's real taxonomy.

## The Complete Pipeline

```python
def run_image_pipeline(image_base64):
    metadata = extract_metadata(image_base64)   # Stage 1
    seo = optimize_seo(metadata)                 # Stage 2
    categorization = categorize(metadata)         # Stage 3 (runs independently of Stage 2)

    return {
        "metadata": metadata,
        "seo": seo,
        "category": categorization.category,
        "tags": categorization.tags,
    }
```

Notice Stages 2 and 3 both depend only on Stage 1's output, not on each other — this pipeline could
run Stage 2 and Stage 3 **concurrently** using
[LCEL's `RunnableParallel`](../langchain-practical/overview-of-lcel-concepts.md), directly applying
the parallelization pattern from [Agent Design Patterns](../agent-design-patterns/) to cut real
latency, since neither stage needs to wait on the other.

## Common Mistakes

- Re-sending the raw image to Stages 2 and 3, wasting tokens and cost on data neither stage actually
  needs once Stage 1 has already extracted the relevant metadata.
- Running Stage 2 and Stage 3 sequentially when they're genuinely independent, missing an easy
  latency win from running them in parallel.
- Trusting a returned `category` value as valid just because it passed schema validation, without
  checking it against the platform's actual, real taxonomy.

## Module Summary

Across this module: both pipelines — profile analysis and image metadata processing — demonstrate
the same underlying shape: a **fixed, multi-stage workflow** (not a dynamic agent, per
[agent-vs-single-llm-call.md](../understanding-ai-agents/agent-vs-single-llm-call.md)) where each
stage does one distinct job and hands the next stage clean, validated, structured data rather than
raw prose or raw media; **schema validation at every stage** (via Pydantic here, the same discipline
as [Schema Validation with Zod](../schema-validation-with-zod/)) catches both structural problems and
real business-rule violations a type check alone can't express; **per-stage error attribution** makes
a multi-stage pipeline's failures genuinely diagnosable, rather than treating "the pipeline failed"
as one opaque event; and **independent stages can run in parallel** — as the SEO and categorization
stages in the second pipeline could — applying this domain's parallelization pattern for a real,
practical latency improvement.
