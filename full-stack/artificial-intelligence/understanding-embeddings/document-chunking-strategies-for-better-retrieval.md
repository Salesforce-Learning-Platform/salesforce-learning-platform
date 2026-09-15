# ✂️ Document Chunking Strategies for Better Retrieval

## Why a Whole Document Isn't the Right Unit to Embed

```
A 50-page policy document embedded as ONE single vector:
  → that one vector has to somehow represent EVERYTHING in 50
    pages at once, diluting any specific detail a query might
    actually be looking for
```

A single embedding vector represents the *overall* meaning of whatever text it's given — cramming
an entire long document into one embedding blurs together dozens of genuinely different topics,
making it far less useful for finding the one specific, relevant passage a query actually needs.
**Chunking** — splitting a document into smaller pieces before embedding each one separately — is
the standard solution.

## Fixed-Size Chunking — The Simplest Approach

```python
def chunk_by_size(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks
```

Splitting text into fixed-length pieces (by character or token count) is simple and predictable,
but has an obvious flaw: a fixed cutoff can slice directly through the middle of a sentence or an
important idea, splitting a single coherent thought across two separate, less useful chunks.

## The Overlap Parameter — Softening the Cutoff Problem

```
Chunk 1: "...the refund policy allows returns within 30 days of"
Chunk 2 (with overlap): "returns within 30 days of purchase, provided the item is unused..."
```

Including a small overlap between consecutive chunks means an idea that gets cut off at the end of
one chunk is very likely still fully present at the start of the next — reducing (though not
eliminating) the chance that a genuinely important detail falls entirely into the "seam" between
two chunks and can't be well-represented by either one's embedding.

## Semantic Chunking — Splitting at Natural Boundaries

```python
# Splitting on paragraph or section boundaries instead of a fixed
# character count
chunks = document.split("\n\n")  # a simple paragraph-based approach
```

A meaningfully better approach splits text at natural boundaries — paragraphs, sections, headings —
so each chunk is far more likely to represent one complete, coherent idea rather than an arbitrary
slice. This usually produces noticeably better retrieval quality than fixed-size chunking, at the
cost of chunks that vary more in length.

## Chunk Size Is a Genuine Trade-Off

```
TOO SMALL a chunk → loses surrounding context; a retrieved sentence
                     fragment may be meaningless on its own

TOO LARGE a chunk → dilutes the embedding across too many ideas at
                     once, same problem as embedding a whole document
```

There's no universally correct chunk size — it depends on the kind of content and how it will be
used. A common practical starting point is a few hundred tokens per chunk with a modest overlap,
then adjusting based on actual retrieval quality observed for the specific content.

## Contextualized Chunk Embeddings — A More Advanced Option

```
voyage-context-4: produces chunk-level vectors that capture FULL
DOCUMENT CONTEXT automatically, without manual overlap/metadata
tricks — called via contextualized_embed() rather than embed()
```

Voyage AI's `voyage-context-4` model is purpose-built for this exact problem: rather than embedding
each chunk in isolation and relying on overlap to preserve context, it produces chunk-level
embeddings that are already aware of the surrounding document — a more sophisticated alternative to
manually engineering overlap and chunk boundaries.

## Common Mistakes

- Chunking with a fixed size and no overlap at all, routinely cutting important ideas exactly at a
  chunk boundary.
- Choosing one chunk size and never revisiting it based on how retrieval quality actually performs
  for the specific content being indexed.
- Embedding an entire long document as a single vector for a use case that actually needs
  passage-level retrieval, rather than chunking it first.

## Module Summary

Across this module: **an embedding** is a numerical vector (from Voyage AI, since Anthropic doesn't
offer its own embedding model) representing a piece of text's meaning, where similar meaning
produces nearby vectors regardless of the exact words used (see
[what-embeddings-represent-in-vector-space.md](what-embeddings-represent-in-vector-space.md));
**similarity search** finds the most relevant match by computing cosine similarity (or an
equivalent dot product, for normalized vectors) between a query's embedding and every candidate
document's embedding, a technique that needs a proper vector index once a collection grows large
(see
[how-similarity-search-works-conceptually.md](how-similarity-search-works-conceptually.md));
and **document chunking** — fixed-size, overlap-softened, semantic, or a purpose-built
contextualized-chunk model — prepares long text for retrieval by splitting it into smaller,
individually coherent pieces before embedding, since a whole long document embedded as one vector
dilutes the very detail a query is looking for.
