# 🔗 The RAG Workflow

## RAG: Retrieval-Augmented Generation

**RAG** combines everything from the last two modules — embeddings, similarity search, a vector
database — with generation, to ground a model's answer in an application's own real, current data
instead of relying purely on what the model learned during training. This is one of the most
common, practical architectures in real production AI applications.

## The Four-Stage Workflow

```
1. QUERY    → the user asks a question in natural language
2. RETRIEVE → embed the query, search the vector database for
              the most relevant stored chunks
3. INJECT   → insert the retrieved chunks into the prompt as context
4. ANSWER   → the model generates a response grounded in that
              retrieved context, rather than its own unaided memory
```

Every piece of this workflow was already built in earlier modules:
[Understanding Embeddings](../understanding-embeddings/) and
[Integrating Vector Databases](../integrating-vector-databases/) cover stages 1–2, while stages 3–4
are ordinary prompt construction and generation, exactly as covered throughout this domain. RAG's
real contribution is the specific *combination*, not any single new technique.

## Why RAG Exists — the Problem It Solves

```
WITHOUT RAG: "What's our company's current refund policy?"
  → the model answers from its TRAINING DATA, which knows nothing
    about your company's specific, possibly recently-changed policy

WITH RAG: the actual, current policy document is retrieved and
  injected into the prompt → the model answers using YOUR real,
  up-to-date information
```

A model's training data is frozen at a point in time and contains no knowledge of an
organization's private, internal, or frequently-changing information. RAG closes this gap without
retraining or fine-tuning the model at all — it simply supplies the relevant information directly
in the prompt, every time.

## A Complete, Working Implementation

```python
def rag_answer(question, index, vo, client):
    # STAGE 1 & 2: embed the query, retrieve relevant chunks
    query_embedding = vo.embed([question], model="voyage-4", input_type="query").embeddings[0]
    results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

    # STAGE 3: inject retrieved chunks into the prompt
    context = "\n\n---\n\n".join(m["metadata"]["text"] for m in results["matches"])
    prompt = f"""Answer the question using ONLY the context below. If the
context doesn't contain the answer, say so explicitly.

Context:
{context}

Question: {question}"""

    # STAGE 4: generate a grounded answer
    response = client.messages.create(
        model="claude-opus-5", max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
```

This is the complete RAG loop, start to finish — every line traces back to a technique already
covered in an earlier module in this domain.

## The Critical Instruction: "Using ONLY the Context"

```
Without this instruction: the model may blend retrieved context
WITH its own training knowledge, making it unclear which parts of
the answer actually came from your real data

With this instruction: the model is explicitly constrained to the
provided context, and told to say so explicitly if the answer
genuinely isn't there
```

This single instruction — applying
[writing-clear-instructions.md](../prompt-engineering-fundamentals/writing-clear-instructions.md)'s
clarity principle specifically to RAG — is what actually makes an answer *grounded*, rather than
merely *influenced by*, the retrieved context. Without it, a model may still confidently answer
from its own training data even when the real, retrieved context says something different or
doesn't cover the question at all.

## Common Mistakes

- Retrieving relevant chunks but never explicitly instructing the model to rely *only* on them,
  losing RAG's core grounding guarantee.
- Injecting far more retrieved context than the question actually needs, wasting tokens (per
  [cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md](../calling-llm-apis-properly/cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md))
  without improving answer quality.
- Assuming RAG eliminates hallucination entirely — it dramatically reduces it for genuinely covered
  questions, but a model can still hallucinate details even from real, provided context.

## ➡️ Next

Continue to
[build-a-document-qa-system-returning-structured-json.md](build-a-document-qa-system-returning-structured-json.md)
to build this workflow into a complete, production-shaped feature returning structured, validated
answers.
