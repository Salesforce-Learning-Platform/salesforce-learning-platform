# 🧭 What Embeddings Represent in Vector Space

## From Generation to Retrieval

Every module so far in this domain has focused on **generation** — a model producing text, JSON, or
a tool call. Embeddings are the foundation of a different, equally important capability:
**retrieval** — finding the most relevant piece of existing information out of a large collection,
based on meaning rather than exact keyword matches. This module builds that foundation; later
modules ([Integrating Vector Databases](../integrating-vector-databases/),
[Building a RAG Pipeline](../building-a-rag-pipeline/)) build on top of it.

## What an Embedding Actually Is

```python
import voyageai

vo = voyageai.Client()
result = vo.embed(["The cat sat on the mat."], model="voyage-4", input_type="document")
print(result.embeddings[0])
# [-0.013131560757756233, 0.019828535616397858, ... ]  ← 1024 numbers
```

An embedding is simply a list of numbers — a **vector** — that represents a piece of text's
*meaning*. `voyage-4` (Voyage AI's current general-purpose model) produces a 1024-dimensional
vector by default for any input text, whether it's a single word or several paragraphs.

## Anthropic Doesn't Offer Its Own Embedding Model

```
Anthropic's own documentation states directly:
"Anthropic does not offer its own embedding model."
Anthropic recommends Voyage AI as its embeddings partner instead.
```

This is a genuinely important, easy-to-miss detail: everything in this domain so far has used
Anthropic's Messages API directly, but embeddings specifically come from a separate, dedicated
provider — Voyage AI — rather than from Claude itself.

## The Core Idea: Similar Meaning → Nearby Vectors

```
"The cat sat on the mat."     →  vector A
"A feline rested on the rug." →  vector B  (semantically similar
                                              to A, even with
                                              completely different
                                              words)
"Stock prices rose sharply
 today."                       →  vector C  (semantically UNRELATED
                                              to A and B)

Distance(A, B) is SMALL
Distance(A, C) is LARGE
```

This is the entire point of an embedding: text with similar *meaning* ends up as vectors that are
mathematically close together in this 1024-dimensional space, even when the actual words used are
completely different — while unrelated text ends up far apart. This is fundamentally different from
keyword search, which would find no overlap at all between "cat" and "feline."

## `input_type` — Documents and Queries Aren't Embedded Identically

```python
doc_embedding = vo.embed(["..."], model="voyage-4", input_type="document").embeddings[0]
query_embedding = vo.embed(["..."], model="voyage-4", input_type="query").embeddings[0]
```

Voyage's own guidance is explicit: for any retrieval use case, always specify `input_type` as
either `"document"` (for the content being stored and searched) or `"query"` (for the search text
itself) — never omit it. Behind the scenes, this prepends a different instruction to each ("Represent
the document for retrieval: " vs. "Represent the query for retrieving supporting documents: "),
which measurably improves retrieval quality over embedding both the same way.

## Common Mistakes

- Assuming embeddings come from the same Claude models used for text generation — they come from a
  separate, dedicated provider (Voyage AI, per Anthropic's own recommendation).
- Omitting the `input_type` parameter, or using the same one for both documents and queries, losing
  a real, measurable improvement in retrieval quality.
- Expecting an embedding vector's individual numbers to be individually meaningful or interpretable
  — the *meaning* lives in a vector's position relative to other vectors, not in any single number.

## ➡️ Next

Continue to
[how-similarity-search-works-conceptually.md](how-similarity-search-works-conceptually.md) to see
exactly how "distance" between vectors is measured and used to find the most relevant results.
