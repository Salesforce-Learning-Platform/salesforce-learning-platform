# 🗄️ Integrating Vector Databases

## 📚 Overview

[Understanding Embeddings](../understanding-embeddings/) computed similarity across a handful of
in-memory vectors — a useful mental model, but not something that scales or persists. This module
introduces vector databases: purpose-built infrastructure for storing embeddings, searching them
efficiently at real scale using approximate nearest-neighbor search, and narrowing results with
metadata filters.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Create a vector index and upsert embeddings with associated metadata.
- Query a vector database for the most similar stored vectors, choosing an appropriate `top_k`.
- Explain why approximate nearest-neighbor search is the right trade-off at scale.
- Apply metadata filters to narrow a search, and know when to reach for a namespace instead for
  genuine access-control isolation.

## 📋 Prerequisites

- [Understanding Embeddings](../understanding-embeddings/) — this module builds directly on the embedding and similarity-search concepts introduced there.
- [Function Calling and Tool Calling](../function-calling-tool-calling/) — familiarity with trusted-context handling, applied here to access-control filters.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [storing-embeddings-for-search-and-retrieval.md](storing-embeddings-for-search-and-retrieval.md) | Creating an index, upserting vectors, and namespaces for partitioning |
| [querying-similar-vectors-efficiently.md](querying-similar-vectors-efficiently.md) | Approximate nearest-neighbor search, `top_k`, and combining results with generation |
| [using-metadata-filters-during-search.md](using-metadata-filters-during-search.md) | Filter operators, multi-tenant access control, and filters vs. namespaces |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building a search, Q&A, or RAG feature over a real, growing collection of
documents — the concepts here are the operational foundation those features run on.

**Skim** if you're only prototyping with a handful of documents held in memory — the concepts from
[Understanding Embeddings](../understanding-embeddings/) alone may be enough until the collection
genuinely needs to scale.

## 🧠 Knowledge Check

<details>
<summary>Why does a vector database use approximate, rather than exact, nearest-neighbor search?</summary>

Exact search requires comparing a query against every single stored vector, which becomes too slow
at real-world scale (millions of vectors, queried repeatedly). Approximate nearest-neighbor search
uses specialized index structures to find a match that's almost always the true closest (or very
close to it), trading a small, usually negligible amount of exactness for a dramatic gain in query
speed.

</details>

<details>
<summary>For strict multi-tenant data isolation, should you rely on a metadata filter or a namespace?</summary>

A namespace, when the isolation genuinely must never fail — it's a hard, structural partition that
queries can't accidentally cross. A metadata filter is a soft, per-query constraint on a shared
index; it's well suited to flexible narrowing (category, date range) but a missing or misconfigured
filter can leak across an intended boundary in a way a namespace structurally can't.

</details>

## 📚 References

- [Pinecone - Upsert Data](https://docs.pinecone.io/guides/index-data/upsert-data) — official documentation for creating an index and upserting vectors
- [Pinecone - Filter by Metadata](https://docs.pinecone.io/guides/search/filter-by-metadata) — official documentation for metadata filter operators
- [IBM - What Is a Vector Database?](https://www.ibm.com/think/topics/vector-database) — a well-known, accessible explanation of vector database concepts

## ➡️ Continue Your Learning Path

Continue to [Building a RAG Pipeline](../building-a-rag-pipeline/) to combine embeddings, vector
storage, and generation into a complete retrieval-augmented generation system.
