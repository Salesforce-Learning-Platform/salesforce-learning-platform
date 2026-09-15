# 👤 Pipeline 1: Profile Analyzer → Bio Improver → Conversation Starter Generator

## The Task, and Why It's a Genuine Sequential Pipeline

Consider a dating or professional-networking app feature: given a user's raw profile text, (1)
analyze its strengths and weaknesses, (2) rewrite the bio to be more engaging, and (3) generate
personalized conversation starters someone else could use to break the ice. This is the
**researcher-writer pattern** from
[Agent Design Patterns](../agent-design-patterns/researcher-to-writer-pattern.md), extended to three
stages instead of two — each stage's output becomes the next stage's input, and each stage does one
genuinely distinct kind of work.

## Stage 1: Profile Analyzer

```python
from pydantic import BaseModel, Field
from typing import Literal

class Analysis(BaseModel):
    strengths: list[str] = Field(min_length=1)
    weaknesses: list[str] = Field(min_length=1)
    tone: Literal["formal", "casual", "playful", "flat"]

def analyze_profile(bio_text):
    response = client.messages.create(
        model="claude-opus-5", max_tokens=512,
        messages=[{"role": "user", "content": f"Analyze this profile bio:\n\n{bio_text}"}],
        output_config={"format": {"type": "json_schema", "schema": ANALYSIS_JSON_SCHEMA}},
    )
    try:
        return Analysis.model_validate_json(response.content[0].text)
    except ValueError as e:
        raise PipelineStageError("profile-analyzer", e)
```

This stage does exactly one job — analysis — and returns validated, structured data. Here the
validation uses Pydantic (Python's standard data-validation library — the direct equivalent of the
Zod pattern this domain has used throughout [Schema Validation with Zod](../schema-validation-with-zod/)
for a Python pipeline), never returning prose. Its output is meant to be *read by the next stage*,
not by a human directly.

## Stage 2: Bio Improver

```python
def improve_bio(bio_text, analysis: Analysis):
    prompt = f"""Original bio: {bio_text}

Identified strengths: {analysis.strengths}
Identified weaknesses: {analysis.weaknesses}
Detected tone: {analysis.tone}

Rewrite this bio to fix the weaknesses while keeping the strengths
and the same overall tone. Return ONLY the improved bio text."""

    response = client.messages.create(
        model="claude-opus-5", max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()
```

Notice this stage's prompt directly consumes Stage 1's *structured* output (`analysis.weaknesses`,
not a paragraph the improver would have to re-interpret) — this is exactly the "clean, purpose-built
handoff" principle from
[researcher-to-writer-pattern.md](../agent-design-patterns/researcher-to-writer-pattern.md): each
stage hands the next exactly what it needs, already extracted and structured.

## Stage 3: Conversation Starter Generator

```python
class Starters(BaseModel):
    starters: list[str] = Field(min_length=3, max_length=5)

def generate_starters(improved_bio):
    response = client.messages.create(
        model="claude-opus-5", max_tokens=512,
        messages=[{"role": "user", "content": f"Based on this bio, generate 3-5 personalized "
                                                f"conversation starters a stranger could use:\n\n{improved_bio}"}],
        output_config={"format": {"type": "json_schema", "schema": STARTERS_JSON_SCHEMA}},
    )
    try:
        return Starters.model_validate_json(response.content[0].text)
    except ValueError as e:
        raise PipelineStageError("conversation-starter-generator", e)
```

The final stage returns to structured output — `starters` is a real array the frontend can render
as a list, exactly like
[build-a-document-qa-system-returning-structured-json.md](../building-a-rag-pipeline/build-a-document-qa-system-returning-structured-json.md)'s
approach earlier in this domain.

## Wiring the Full Pipeline Together

```python
def run_profile_pipeline(bio_text):
    analysis = analyze_profile(bio_text)          # Stage 1
    improved_bio = improve_bio(bio_text, analysis) # Stage 2
    starters = generate_starters(improved_bio)     # Stage 3

    return {
        "original_bio": bio_text,
        "improved_bio": improved_bio,
        "analysis": analysis,
        "conversation_starters": starters.starters,
    }
```

This is a **workflow**, not an agent, in the precise sense from
[agent-vs-single-llm-call.md](../understanding-ai-agents/agent-vs-single-llm-call.md) — the sequence
of three stages is fixed by the application code, not decided dynamically by a model. This is a
deliberate, correct choice here: the three-step sequence genuinely is always the same, so a fixed
pipeline is simpler, cheaper, and more predictable than a full agent would be.

## Handling a Mid-Pipeline Failure

```python
def run_profile_pipeline_safely(bio_text):
    try:
        return {"ok": True, "data": run_profile_pipeline(bio_text)}
    except PipelineStageError as e:
        logAiInteraction({"context": f"profile-pipeline-{e.stage}", "success": False})
        return {"ok": False, "failedStage": e.stage}
```

Exactly per [Error Handling in AI Applications](../error-handling-in-ai-applications/)'s structured
logging discipline, each stage's own validation failure is caught and attributed to the *specific*
stage that failed — critical for diagnosing which of the three stages is actually the weak link,
rather than treating "the pipeline failed" as one opaque event.

## Common Mistakes

- Passing Stage 1's raw, unstructured text output to Stage 2 instead of the validated, structured
  data — losing the clean-handoff benefit this pipeline shape is built around.
- Building this as a full agent (letting a model decide the stage order dynamically) when the
  sequence is genuinely always fixed — unnecessary complexity per
  [agent-vs-single-llm-call.md](../understanding-ai-agents/agent-vs-single-llm-call.md).
- Catching a failure at the top level without attributing it to the specific stage that failed,
  losing critical debugging information.

## ➡️ Next

Continue to
[image-metadata-extractor-to-seo-optimizer-to-tag-categorizer.md](image-metadata-extractor-to-seo-optimizer-to-tag-categorizer.md)
for a second, complete pipeline example applying the same shape to a genuinely different domain.
