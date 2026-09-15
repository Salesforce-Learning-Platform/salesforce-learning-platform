# 🧭 Understanding Embeddings

## 📚 Overview

Every module in this domain so far has focused on generation — a model producing text or
structured data. This module introduces the foundation of a genuinely different capability:
**retrieval** — finding the most relevant existing information out of a large collection, based on
meaning rather than exact keyword overlap. Embeddings are the mechanism that makes this possible,
and this module covers what they represent, how similarity search actually works, and how
documents are prepared before being embedded.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain what an embedding vector represents and why Anthropic recommends Voyage AI rather than
  offering its own embedding model.
- Compute and interpret cosine similarity (and the normalized dot-product shortcut) between
  embeddings to find the most relevant match.
- Explain why brute-force similarity search doesn't scale to very large collections.
- Choose an appropriate document chunking strategy — fixed-size, overlap, semantic, or
  contextualized — for a given retrieval use case.

## 📋 Prerequisites

- [How LLMs Actually Work](../how-llms-actually-work/) — general familiarity with how models represent and process text.
- No prior retrieval or vector-database experience is assumed — this module is the starting point for that track.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-embeddings-represent-in-vector-space.md](what-embeddings-represent-in-vector-space.md) | What an embedding vector is, and why similar meaning produces nearby vectors |
| [how-similarity-search-works-conceptually.md](how-similarity-search-works-conceptually.md) | Cosine similarity, nearest-neighbor search, and why it doesn't scale as a brute-force loop |
| [document-chunking-strategies-for-better-retrieval.md](document-chunking-strategies-for-better-retrieval.md) | Fixed-size, overlap, semantic, and contextualized chunking strategies |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building any feature involving search over a body of documents — a support
knowledge base, a document Q&A tool, or a RAG pipeline — since embeddings are the foundational
concept every one of those features is built on.

**Skim** if your AI features so far are purely generative, with no need to search or retrieve
existing content — you can return to this module once a retrieval use case comes up.

## 🧠 Knowledge Check

<details>
<summary>Why does Anthropic recommend Voyage AI for embeddings instead of using Claude directly?</summary>

Anthropic's own documentation states plainly that Anthropic does not offer its own embedding model,
and recommends Voyage AI as its embeddings partner instead. Embeddings and text generation are
genuinely different capabilities, provided by different, purpose-built models.

</details>

<details>
<summary>Why would a whole 50-page document embedded as a single vector make retrieval worse, not better?</summary>

One embedding vector represents the *overall* meaning of whatever text it's given. Cramming an
entire long document into a single vector blurs together many different topics at once, diluting
any specific detail a query might be looking for — which is exactly the problem document chunking
solves by embedding smaller, more focused pieces separately.

</details>

## 📚 References

- [Anthropic - Embeddings](https://platform.claude.com/docs/en/build-with-claude/embeddings) — official documentation covering Voyage AI, available models, and a full quickstart example
- [Pinecone - Vector Similarity Explained](https://www.pinecone.io/learn/vector-similarity/) — a deeper, well-known explanation of cosine similarity and other distance metrics

## ➡️ Continue Your Learning Path

Continue to [Integrating Vector Databases](../integrating-vector-databases/) to see how embeddings
are stored and searched efficiently at a scale beyond what a brute-force loop can handle.
