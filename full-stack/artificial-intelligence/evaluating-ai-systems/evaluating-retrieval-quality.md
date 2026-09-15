# 🎯 Evaluating Retrieval Quality

## A Separate Concern From Answer Quality

A [RAG system](../building-a-rag-pipeline/) can fail in two genuinely independent ways: the
**retrieval** step can fetch the wrong (or no) relevant chunks, or the **generation** step can
produce a poor answer even from good chunks. Measuring these separately is essential — a system
that "gives bad answers" might actually have excellent generation and simply broken retrieval, and
the fix for each problem is completely different.

## Precision@k — "Of What Was Retrieved, How Much Was Actually Relevant?"

```
Query: "What's our refund policy for damaged items?"
Retrieved top 3 chunks:
  1. Damaged item refund policy        ← relevant
  2. General shipping FAQ              ← NOT relevant
  3. Damaged item return process       ← relevant

Precision@3 = 2 relevant / 3 retrieved = 0.67
```

Precision@k measures how much of what was actually retrieved is genuinely relevant to the query.
Low precision means the retrieval step is pulling in noise alongside (or instead of) genuinely
useful content — often a sign the embeddings, chunking strategy, or `top_k` value needs
adjustment.

## Recall@k — "Of What's Actually Relevant, How Much Was Retrieved?"

```
Suppose there are 4 genuinely relevant chunks in the ENTIRE
document collection for this query, and the system retrieved 2
of them within its top-k results.

Recall@k = 2 relevant retrieved / 4 relevant that exist = 0.5
```

Recall@k measures how much of the *total* relevant content actually got surfaced, regardless of how
much irrelevant content came along with it. Low recall means genuinely relevant information exists
in the collection but isn't being found — a different problem than low precision, often pointing to
a chunking or embedding-model issue rather than a `top_k` issue.

## Mean Reciprocal Rank (MRR) — "How High Did the Best Result Rank?"

```
Query 1: first genuinely relevant result at position 1  → 1/1 = 1.0
Query 2: first genuinely relevant result at position 3  → 1/3 ≈ 0.33
Query 3: first genuinely relevant result at position 2  → 1/2 = 0.5

MRR = average(1.0, 0.33, 0.5) ≈ 0.61
```

MRR specifically measures ranking quality — not just *whether* a relevant result appears, but *how
high up* it ranks. This matters because a relevant chunk buried at position 8 out of a `top_k` of 3
is effectively invisible to the downstream generation step, even though it technically exists in
the broader collection.

## Building a Small, Real Evaluation Set

```python
eval_set = [
    {"query": "What's our refund policy for damaged items?", "relevant_doc_ids": ["policy-042", "policy-043"]},
    {"query": "How do I reset my password?", "relevant_doc_ids": ["support-019"]},
    # ...20-50 real, representative queries with known-correct answers
]

def evaluate_retrieval(eval_set, index, vo):
    scores = []
    for case in eval_set:
        query_embedding = vo.embed([case["query"]], model="voyage-4", input_type="query").embeddings[0]
        results = index.query(vector=query_embedding, top_k=3)
        retrieved_ids = {m["id"] for m in results["matches"]}
        relevant_retrieved = retrieved_ids & set(case["relevant_doc_ids"])
        scores.append(len(relevant_retrieved) / len(case["relevant_doc_ids"]))
    return sum(scores) / len(scores)  # average recall@3 across the eval set
```

This is genuinely important, practical infrastructure: a small (even 20–50 query) evaluation set
with known-correct relevant documents, checked periodically, is what turns "retrieval seems fine"
into an actual, trackable, comparable number — one that can catch a regression the moment a chunking
strategy or embedding model changes.

## Common Mistakes

- Only ever measuring end-to-end answer quality, never isolating whether retrieval specifically is
  the actual source of a poor answer.
- Never building a real evaluation set, relying entirely on informal, ad hoc spot-checking instead
  of a number that can be tracked and compared over time.
- Optimizing purely for precision (fewer, more relevant results) without checking recall, silently
  missing genuinely relevant content that exists in the collection but never surfaces.

## ➡️ Next

Continue to
[observability-and-monitoring-basics.md](observability-and-monitoring-basics.md) to see how these
same evaluation ideas extend into ongoing, production monitoring rather than a one-time check.
