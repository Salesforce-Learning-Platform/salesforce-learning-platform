# 👻 Detecting Hallucinations

## From "Why It Happens" to "How to Catch It"

[why-hallucination-happens-it-predicts-it-doesnt-know.md](../how-llms-actually-work/why-hallucination-happens-it-predicts-it-doesnt-know.md),
early in this domain, explained *why* a model can confidently state something false — it predicts
plausible text, it doesn't consult a source of truth. This file covers the practical, applied side:
how to actually detect when this has happened in a real system's output.

## The Easiest Case: Grounded (RAG) Responses

```python
def check_grounding(answer, context):
    """A cheap, practical heuristic: does the answer reference
    content that's actually present in the provided context?"""
    response = client.messages.create(
        model="claude-opus-5", max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"""Context:\n{context}\n\nClaimed answer:\n{answer}\n\n
Is every factual claim in the answer directly supported by the
context above? Respond with ONLY "supported" or "unsupported".""",
        }],
    )
    return response.content[0].text.strip().lower() == "supported"
```

For [RAG-based systems](../building-a-rag-pipeline/), this is the most tractable case: since the
answer is supposed to come *only* from the retrieved context, a second, focused check — sometimes
even a second, cheaper model call — can verify whether the claimed answer is actually traceable
back to that context. This "LLM-as-a-judge" pattern is a common, practical technique specifically
because verifying a claim against a known source is a much easier task than generating a fully
correct answer from scratch.

## The Harder Case: Ungrounded, Open-Ended Generation

```
For a request with NO retrieved context to check against (e.g.
"explain quantum entanglement"), there's no external source of
truth readily available to automatically verify the answer against.
```

Detecting hallucination in a purely generative response — no retrieved context, no external
document to cross-check — is a fundamentally harder problem. Practical approaches here rely on
techniques like self-consistency (asking the same question multiple times and checking whether the
answers agree) rather than a single, definitive grounding check.

## Self-Consistency Checking

```python
def check_consistency(question, num_samples=3):
    answers = [
        client.messages.create(
            model="claude-opus-5", max_tokens=256,
            messages=[{"role": "user", "content": question}],
        ).content[0].text
        for _ in range(num_samples)
    ]
    # A simple heuristic: if the model's answers to the SAME question
    # diverge meaningfully across samples, that's a signal of low
    # confidence — a fact the model is SURE of tends to come back
    # consistently; ask about something the training data underrepresents,
    # and it can drift
    return answers
```

Asking the same question multiple times (per
[sampling-basics-temperature-and-randomness-control.md](../how-llms-actually-work/sampling-basics-temperature-and-randomness-control.md)'s
introduction to sampling randomness) and comparing the results is a genuinely useful, low-effort
signal: genuine, well-supported facts tend to come back consistently across samples, while a
fabricated or uncertain answer is more likely to vary from one sample to the next.

## Domain-Specific Fact Checking

```
For a NARROW, well-defined domain (e.g. a product catalog, a known
set of policies), a targeted check against that specific known data
source is far more reliable than a general-purpose consistency check.
```

Where the domain is narrow enough, a dedicated, deterministic check — does the mentioned product ID
actually exist in the catalog? does the cited policy section actually say that? — is more reliable
than any general-purpose hallucination-detection technique, precisely because it checks against a
known, authoritative source rather than inferring likely correctness indirectly.

## Common Mistakes

- Treating hallucination detection as a solved, guaranteed process — every technique here is a
  useful signal, not a guarantee of catching every false statement.
- Applying the expensive, general-purpose self-consistency technique when a much cheaper,
  domain-specific deterministic check would work better for a narrow, well-defined use case.
- Skipping grounding checks entirely for a RAG system, on the assumption that retrieval alone
  prevents hallucination — a model can still hallucinate details even when given correct context.

## ➡️ Next

Continue to [assigning-confidence-scores.md](assigning-confidence-scores.md) to see how a
system communicates its own uncertainty rather than only detecting outright fabrication.
