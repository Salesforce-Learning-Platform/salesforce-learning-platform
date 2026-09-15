# ⚡ Querying Similar Vectors Efficiently

## Why "Efficiently" Is the Whole Point

[how-similarity-search-works-conceptually.md](../understanding-embeddings/how-similarity-search-works-conceptually.md)
ended on an unsolved problem: comparing a query against every single document in a large collection
doesn't scale. A vector database's core value is answering the same question — "what's most
similar to this vector?" — using an internal index structure built for fast **approximate** nearest-
neighbor search, instead of a brute-force scan over every stored vector.

## The Basic Query

```python
query_embedding = vo.embed([user_question], model="voyage-4", input_type="query").embeddings[0]

results = index.query(
    vector=query_embedding,
    top_k=3,
    include_metadata=True,
)

for match in results["matches"]:
    print(match["id"], match["score"], match["metadata"])
```

`top_k` specifies how many of the closest matches to return — `3` here means "give me the 3 most
similar stored vectors." `score` is the similarity value for each match (higher generally means
more similar, for the `cosine` metric configured on the index), and `include_metadata=True` returns
each match's stored metadata alongside its `id`, so the application doesn't need a separate lookup
just to know *what* was actually matched.

## Approximate, Not Exact — and Why That's the Right Trade-Off

```
EXACT nearest-neighbor search: guaranteed to find the TRUE closest
match, but requires comparing against every vector → slow at scale

APPROXIMATE nearest-neighbor search: uses an index structure to
find a match that's almost always the true closest (or very close
to it) → dramatically faster, at a tiny, usually acceptable
accuracy trade-off
```

Vector databases use specialized indexing algorithms (built on structures with names like HNSW)
specifically to make this trade-off favorably — for the overwhelming majority of real applications,
retrieving the 3rd-closest match instead of the true 1st-closest occasionally is a negligible cost
compared to the massive speed gain at scale.

## Choosing `top_k`

```
top_k too LOW  → risks missing a genuinely relevant document that
                  happened to score just outside the cutoff

top_k too HIGH → returns more results than actually useful, adding
                  noise (and more tokens, if fed into a prompt) for
                  no real benefit
```

There's no universal correct value — a common starting point for feeding results into an LLM
prompt (the [RAG pattern](../building-a-rag-pipeline/), covered later in this domain) is a small
number like 3–5, then tuning up or down based on observed retrieval quality for the specific use
case.

## Combining Results With Generation

```python
def answer_with_retrieval(question):
    query_embedding = vo.embed([question], model="voyage-4", input_type="query").embeddings[0]
    results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

    context = "\n\n".join(m["metadata"]["text"] for m in results["matches"])
    prompt = f"Using ONLY this context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"

    return client.messages.create(
        model="claude-opus-5", max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
```

This is retrieval and generation working together, in miniature — the query result's stored
`metadata` (here, the original chunked text) becomes the context injected into a generation prompt,
grounding the model's answer in the application's own real data rather than relying purely on its
training knowledge. The full version of this pattern, with its own dedicated considerations, is
[Building a RAG Pipeline](../building-a-rag-pipeline/), later in this domain.

## Common Mistakes

- Treating a vector database's results as guaranteed to be the mathematically exact closest
  matches — approximate search is, by design, occasionally not perfectly exact.
- Setting `top_k` far higher than actually needed, adding unnecessary token cost and noise to a
  downstream generation prompt.
- Forgetting `include_metadata=True` and then needing a separate lookup just to know what each
  returned `id` actually corresponds to.

## ➡️ Next

Continue to
[using-metadata-filters-during-search.md](using-metadata-filters-during-search.md) to see how a
query can be narrowed to a specific subset of the collection before similarity is even considered.
