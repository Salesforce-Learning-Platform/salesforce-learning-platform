# 📊 Assigning Confidence Scores

## Why Confidence Matters Beyond a Binary Right/Wrong

A response isn't simply "correct" or "hallucinated" — it exists somewhere on a spectrum, and a
well-designed application surfaces that uncertainty to the user rather than presenting every answer
with equal, unearned confidence. This is exactly what
[building-structured-profile-analysis-data-with-scores-strengths-and-suggestions.md](../generating-json-responses-from-llms/building-structured-profile-analysis-data-with-scores-strengths-and-suggestions.md)'s
`confidence` field and
[build-a-document-qa-system-returning-structured-json.md](../building-a-rag-pipeline/build-a-document-qa-system-returning-structured-json.md)'s
`confidence` enum were building toward — this file covers where that value should actually come
from.

## Option 1: Asking the Model to Self-Report

```python
output_config={
    "format": {
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "answer": {"type": "string"},
                "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            },
            "required": ["answer", "confidence"],
        },
    }
}
```

The simplest approach: explicitly ask the model to rate its own confidence as part of a structured
response. This is easy to implement and often reasonably useful, but has a real, known limitation
worth understanding clearly before relying on it.

## The Honest Limitation of Self-Reported Confidence

```
A model's self-reported "confidence" is itself just GENERATED TEXT —
produced the same way as any other output, not derived from an
internal, measurable certainty signal the model has genuine
introspective access to.
```

This is an important, easy-to-overstate nuance: a model saying "confidence: high" is not the same
kind of signal as, say, a classifier's actual probability output. It's a genuinely useful heuristic
— models trained with reinforcement learning from human feedback do tend to correlate self-reported
confidence with actual accuracy reasonably well in practice — but it should be treated as one input
among several, not as ground truth.

## Option 2: Deriving Confidence From Retrieval Quality

```python
def derive_confidence_from_retrieval(top_similarity_score):
    if top_similarity_score > 0.85:
        return "high"
    elif top_similarity_score > 0.65:
        return "medium"
    return "low"
```

For a [RAG system](../building-a-rag-pipeline/) specifically, the actual similarity score from
[querying-similar-vectors-efficiently.md](../integrating-vector-databases/querying-similar-vectors-efficiently.md)
provides a genuinely independent, non-self-reported signal: if the best-matching retrieved chunk
only weakly resembles the query, that's real, objective evidence the system may not have found
genuinely relevant information — regardless of how confidently the model then phrases its answer.

## Option 3: Combining Multiple Signals

```python
def compute_final_confidence(model_self_reported, retrieval_score, consistency_check_passed):
    if not consistency_check_passed or retrieval_score < 0.5:
        return "low"
    if model_self_reported == "high" and retrieval_score > 0.8:
        return "high"
    return "medium"
```

The most reliable approach combines several independent signals — self-reported confidence,
retrieval quality, [self-consistency](detecting-hallucinations.md) — rather than trusting any
single one alone. Each individual signal has known blind spots; combining them, with retrieval
quality and consistency able to *override* an unjustified "high" self-report, produces a more
trustworthy final result.

## Displaying Confidence Honestly to Users

```
"high"   → shown normally, with sources
"medium" → shown with a subtle "verify important details" note
"low"    → shown with a clear caveat, or the response is withheld
           entirely for high-stakes use cases
```

A confidence score is only useful if it actually changes what the user sees — computing it and then
displaying every answer identically regardless of its value defeats the entire purpose of
calculating it in the first place.

## Common Mistakes

- Treating a model's self-reported confidence as an objective, calibrated probability rather than
  one useful-but-imperfect signal among several.
- Computing a confidence score but displaying every response identically regardless of its value.
- Deriving confidence purely from retrieval similarity for a request that wasn't actually
  retrieval-based, where that signal doesn't meaningfully apply.

## ➡️ Next

Continue to [evaluating-retrieval-quality.md](evaluating-retrieval-quality.md) to see how the
retrieval half of a RAG system is measured and improved on its own.
