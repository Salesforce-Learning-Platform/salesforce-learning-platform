# 🗄️ Storing Embeddings for Search and Retrieval

## From an In-Memory List to a Real Database

[how-similarity-search-works-conceptually.md](../understanding-embeddings/how-similarity-search-works-conceptually.md)
computed similarity across a handful of documents held directly in a Python list — fine for a
demo, but not something that scales, persists across restarts, or handles millions of vectors. A
**vector database** is purpose-built infrastructure for storing embeddings and searching them
efficiently at real scale.

## Creating an Index

```python
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

pc = Pinecone(api_key="YOUR_API_KEY")

if not pc.has_index("support-articles"):
    pc.create_index(
        name="support-articles",
        vector_type="dense",
        dimension=1024,       # must match your embedding model's output size
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
```

An **index** is a vector database's core structure — conceptually similar to a table in a
relational database, but built specifically for vector similarity search rather than exact-match
lookups. The `dimension` parameter must exactly match the embedding model's output size — `1024`
for Voyage AI's `voyage-4`, per
[what-embeddings-represent-in-vector-space.md](../understanding-embeddings/what-embeddings-represent-in-vector-space.md)
— and `metric` specifies how similarity is measured (`cosine` is the standard choice for most
embedding models).

## Upserting Vectors

```python
index = pc.Index(host="INDEX_HOST")

index.upsert(vectors=[
    {
        "id": "article-042",
        "values": embedding_vector,  # the 1024-number list from Voyage AI
        "metadata": {"category": "billing", "title": "How refunds are processed"},
    },
])
```

"Upsert" (insert-or-update) is the standard operation for adding a vector to an index: each entry
needs a unique `id`, the actual embedding as `values`, and an optional `metadata` object — ordinary
key-value data stored *alongside* the vector, covered fully in
[using-metadata-filters-during-search.md](using-metadata-filters-during-search.md).

## The Full Pipeline From Document to Stored Vector

```python
def index_document(doc_id, text, metadata):
    embedding = vo.embed([text], model="voyage-4", input_type="document").embeddings[0]
    index.upsert(vectors=[{"id": doc_id, "values": embedding, "metadata": metadata}])
```

Combining [Understanding Embeddings](../understanding-embeddings/)'s embedding step with a vector
database's storage step gives the complete "indexing" half of a retrieval system — this function is
what actually runs (once per document, or once per chunk — per
[document-chunking-strategies-for-better-retrieval.md](../understanding-embeddings/document-chunking-strategies-for-better-retrieval.md))
to build up a searchable collection in the first place.

## Namespaces — Keeping Separate Collections Apart

```python
index.upsert(vectors=[...], namespace="customer-abc")  # tenant isolation
index.upsert(vectors=[...], namespace="customer-xyz")
```

A **namespace** partitions one index into logically separate sub-collections that can be queried
independently — a common, practical use is per-tenant isolation in a multi-tenant application,
ensuring one customer's search never returns results from another customer's data.

## Common Mistakes

- Setting an index's `dimension` to a value that doesn't match the actual embedding model's output
  size, causing every upsert to fail.
- Re-embedding and re-upserting a document's full collection from scratch on every change instead
  of upserting only what actually changed (an upsert by the same `id` simply overwrites it).
- Storing every tenant's or user's data in one shared namespace when queries should never cross
  between them.

## ➡️ Next

Continue to
[querying-similar-vectors-efficiently.md](querying-similar-vectors-efficiently.md) to see how a
stored collection like this is actually searched.
