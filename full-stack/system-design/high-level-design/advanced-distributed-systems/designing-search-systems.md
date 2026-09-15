# 🔍 Designing Search Systems

## A Genuinely Different Data Access Pattern

Every data access pattern covered so far in this domain —
[the URL Shortener's key-value lookups](../communication-and-data-layer/sql-vs-nosql-at-scale.md) —
has been a direct, exact lookup: "give me the value for this exact key." **Search** is
fundamentally different: "find every document that's *relevant* to this query," where relevance
itself has to be computed, not simply looked up.

## Why a Regular Database Can't Efficiently Power Search

```
SELECT * FROM articles WHERE content LIKE '%system design%'

This requires SCANNING every row's ENTIRE content, checking for a
match - genuinely, unacceptably slow across millions of documents,
and provides NO way to rank results by actual relevance.
```

A traditional database's indexes are built for exact-match or range lookups on specific columns —
they're structurally the wrong tool for "find text anywhere within a large body of content, ranked
by relevance."

## The Inverted Index: the Core Data Structure Behind Search

```
FORWARD index (a regular database): documentID -> full content

INVERTED index: WORD -> list of documentIDs containing it

"design":  [doc1, doc3, doc7, doc12]
"system":  [doc1, doc3, doc9]
"search":  [doc3, doc7]
```

Per Elastic's own official documentation, an inverted index maps each individual term to the
documents containing it — a search for "system design" becomes a fast lookup of two short lists
(intersecting them to find documents containing *both* terms), rather than scanning every
document's full content from scratch.

## Text Analysis: Preparing Text for Indexing

```
Raw text: "The Quick Brown Foxes Are Running"

After analysis (LOWERCASING, STEMMING, removing STOP WORDS):
["quick", "brown", "fox", "run"]
```

Per Elastic's own documentation, this analysis pipeline — lowercasing, stemming ("running" →
"run"), and removing common stop words ("the," "are") — happens identically to both the *indexed*
content and the *query* text, ensuring a search for "run" correctly matches a document containing
"running."

## Relevance Scoring: Ranking, Not Just Matching

```
BM25 (the default algorithm used by Elasticsearch) scores each
matching document based on:
  - TERM FREQUENCY: how OFTEN the search term appears in THIS
    document
  - DOCUMENT FREQUENCY: how RARE that term is ACROSS all documents
    (a rare term matching is a STRONGER signal than a common one)
  - DOCUMENT LENGTH: normalizing so a SHORT document isn't
    unfairly penalized against a LONG one
```

This is genuinely the key capability a plain database `LIKE` query structurally cannot provide —
search isn't just "does this match?", it's "*how well* does this match, relative to every other
result?", directly informing which results actually appear first.

## Where a Search System Fits Into the Broader Architecture

```
Directly extending microservices-fundamentals.md, earlier in this
domain - a dedicated SEARCH SERVICE, backed by Elasticsearch (or
a similar engine), typically runs ALONGSIDE a system's primary
database, kept in SYNC via the message queue infrastructure
already covered in Core Infrastructure.
```

This is a genuinely common, real architectural pattern — the primary database remains the
authoritative source of truth, while a separate, purpose-built search index (updated asynchronously,
via a message queue) serves search queries specifically, since the two data structures are
optimized for genuinely different access patterns.

## Common Mistakes

- Attempting to implement genuine full-text search using a plain database `LIKE` query, which
  scales poorly and provides no real relevance ranking.
- Applying different text analysis (or none at all) to search queries versus indexed content,
  causing genuinely matching documents to be silently missed.
- Treating the search index as the sole source of truth for data, rather than a derived,
  asynchronously-updated copy kept in sync with the primary database.

## Module Summary

Across this module: **reliability and availability**, measured precisely via "the nines," reveals
that dependent services' availability multiplies down rather than simply flooring at the weakest
link (see [reliability-and-availability.md](reliability-and-availability.md)); **fault tolerance**
— the circuit breaker pattern (structurally the State pattern from the LLD domain), disciplined
retries, redundancy, and graceful degradation — designs for failure as a genuine, expected
occurrence rather than a rare exception (see
[fault-tolerance-and-failure-handling.md](fault-tolerance-and-failure-handling.md));
**observability at scale** extends metrics/logs/traces across many independent services via
distributed tracing and consistent structured logging, with SLIs/SLOs/SLAs as precise, distinct
vocabulary (see [observability-at-scale.md](observability-at-scale.md)); **rate limiting**
algorithms — fixed window, sliding window, token bucket — each genuinely fit different accuracy and
burst-tolerance needs, centralized at the API Gateway (see [rate-limiting.md](rate-limiting.md));
**authorization at architecture scale** centralizes authentication at an Identity Provider while
distributing authorization decisions to each resource server, propagating trust via signed tokens
(see [authorization-at-architecture-scale.md](authorization-at-architecture-scale.md)); and
**search systems**, built on the inverted index and relevance scoring, solve a genuinely different
data access pattern than exact lookups, typically running as a dedicated, asynchronously-synced
service alongside a system's primary database.
