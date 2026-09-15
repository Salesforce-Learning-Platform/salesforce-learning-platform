# 🏷️ Using Metadata Filters During Search

## Semantic Similarity Alone Isn't Always Enough

A pure similarity search over an entire index answers "what's most similar to this query?" — but a
real application often needs a *narrower* question: "what's most similar to this query, **among
only the documents from this category / this date range / this specific customer**?" Metadata
filters answer exactly this narrower question.

## A Filtered Query

```python
results = index.query(
    vector=query_embedding,
    top_k=3,
    filter={"category": {"$eq": "billing"}},
    include_metadata=True,
)
```

The `filter` parameter applies ordinary structured conditions — here, "only consider vectors whose
`category` metadata field equals `billing`" — **before** ranking by similarity. This is exactly the
`metadata` stored on each vector back in
[storing-embeddings-for-search-and-retrieval.md](storing-embeddings-for-search-and-retrieval.md),
now being used as the basis for a real query constraint.

## Common Filter Operators

```python
{"category": {"$eq": "billing"}}                        # exact match
{"year": {"$gte": 2024}}                                 # greater than or equal
{"category": {"$in": ["billing", "refunds", "account"]}} # any of several values
{"$and": [{"category": {"$eq": "billing"}}, {"year": {"$gte": 2024}}]}  # combined conditions
```

`$eq`, `$gte` (and its counterparts `$lte`, `$gt`, `$lt`), `$in`, and logical combinators like
`$and`/`$or`/`$not` cover the great majority of real filtering needs — narrowing a search to a
specific category, a date range, a set of allowed values, or several conditions combined together.

## The Multi-Tenant Access Control Pattern

```python
def search_for_user(user, question):
    query_embedding = vo.embed([question], model="voyage-4", input_type="query").embeddings[0]
    return index.query(
        vector=query_embedding,
        top_k=3,
        filter={"tenant_id": {"$eq": user.tenant_id}},  # NEVER trust a client-supplied filter here
        include_metadata=True,
    )
```

For any multi-tenant application, a metadata filter restricting results to the authenticated user's
own `tenant_id` is a genuine access-control mechanism, not just a search refinement — exactly the
same principle [hybrid-logic-ai-and-code.md](../function-calling-tool-calling/hybrid-logic-ai-and-code.md)
established for tool arguments: this value must always come from the application's own trusted
session state, never from anything a client or the AI supplies directly.

## Filtering vs. Namespaces — Choosing the Right Tool

```
NAMESPACE  → a hard, structural partition; queries never cross
             between namespaces even by mistake

METADATA FILTER → a soft, per-query constraint on ONE shared index;
                   flexible, but a missing or wrong filter can leak
                   across the intended boundary
```

For genuinely strict isolation — separate tenants whose data must *never* mix under any
circumstances — a namespace (or even a fully separate index) is the structurally safer choice.
Metadata filtering is better suited to flexible, query-specific narrowing (category, date range)
where the underlying collection is meant to be shared.

## Common Mistakes

- Accepting a metadata filter value directly from client input for anything access-control-related,
  rather than deriving it from the server's own trusted session/auth state.
- Reaching for metadata filtering to enforce strict tenant isolation when a namespace (or separate
  index) would be structurally safer and harder to accidentally misconfigure.
- Applying a filter so narrow it excludes every genuinely relevant document, silently returning an
  empty or poor result set instead of the intended narrowed-but-useful one.

## Module Summary

Across this module: **a vector database** stores embeddings in an index built for fast similarity
search, with each vector's `id`, `values`, and optional `metadata` upserted individually, and
namespaces available for structural partitioning (see
[storing-embeddings-for-search-and-retrieval.md](storing-embeddings-for-search-and-retrieval.md));
**querying** uses approximate nearest-neighbor search — trading a small amount of exactness for a
dramatic speed gain at scale — with `top_k` controlling how many results come back, feeding directly
into a retrieval-augmented generation pattern (see
[querying-similar-vectors-efficiently.md](querying-similar-vectors-efficiently.md)); and
**metadata filters** narrow a query to a specific subset of the collection before similarity
ranking happens, using operators like `$eq`, `$gte`, and `$in` — with any access-control-relevant
filter value always sourced from trusted server state, never client input.
