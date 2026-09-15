# ⚡ Caching Strategies

## Directly Applying the Latency Lesson

[capacity-estimation-basics.md](../system-design-foundations/capacity-estimation-basics.md), earlier
in this domain, established that memory access is orders of magnitude faster than disk access.
**Caching** is the concrete architectural technique built on that exact fact — storing frequently
accessed data somewhere genuinely faster to read than its primary source, directly extending
[Caching: Local and Redis](../../../backend/caching-local-and-redis/), already covered in this
repository's Backend domain, now applied at the system-architecture level.

## Cache-Aside (Lazy Loading): the Most Common Pattern

```python
def get_url(short_code):
    cached = cache.get(short_code)
    if cached:
        return cached   # CACHE HIT - fast

    long_url = database.query(short_code)   # CACHE MISS - slower
    cache.set(short_code, long_url)
    return long_url
```

Per AWS's own official guidance: the application checks the cache first, and only queries the
database on a genuine miss, populating the cache at that point — this keeps the cache containing
only data the application actually, genuinely requests, rather than pre-loading everything
speculatively.

## Write-Through: Keeping the Cache Always Current

```python
def update_url(short_code, new_destination):
    database.update(short_code, new_destination)
    cache.set(short_code, new_destination)   # updated TOGETHER,
                                                # at write time
```

Per AWS's own framing, write-through eliminates cache misses on data that was *just* updated — the
cache is written to at the same moment as the database, so a subsequent read never has to fall back
to the slower path at all. The trade-off: this can fill the cache with data that's rarely actually
read, and adds real latency to every write.

## Choosing Between Them

```
CACHE-ASIDE  → the cache stays LEAN (only genuinely requested data)
             → the FIRST read after a miss is genuinely slower

WRITE-THROUGH → EVERY subsequent read is fast, even immediately
             after a write
             → writes are SLOWER, and unused data can accumulate
```

For the URL Shortener's redirect traffic — read-heavy, per
[capacity-estimation-basics.md](../system-design-foundations/capacity-estimation-basics.md)'s own
estimate that redirects vastly outnumber creations — cache-aside is often the more natural fit; a
write-heavy system with predictable, immediate re-reads might favor write-through instead.

## Cache Invalidation: the Genuinely Hard Part

```
"There are only two hard things in Computer Science: cache
invalidation and naming things." - a widely-repeated, genuinely
accurate observation about how DIFFICULT this specific problem is.
```

```
TTL (Time To Live) → the SIMPLEST approach: cached data
  automatically expires after a set duration, accepting some
  temporary staleness in exchange for simplicity
```

This directly connects to [Consistency vs. Performance Tradeoffs](../communication-and-data-layer/consistency-vs-performance-tradeoffs.md),
the previous module — a cache is, structurally, another form of the exact same consistency-vs-
performance trade-off: serving cached (potentially stale) data faster, versus always querying the
genuinely current source at the cost of real latency.

## Where the Cache Actually Lives: Redis

```
Redis (already covered in Caching: Local and Redis, in this
repository's Backend domain) is one of the most widely-used
IN-MEMORY caching systems specifically because it's FAST
(memory-speed access) and can be SHARED across multiple
application server instances, unlike a purely local, in-process
cache.
```

## Common Mistakes

- Caching data that changes frequently with no invalidation strategy at all, silently serving stale
  data indefinitely.
- Using a purely local, in-process cache for data that needs to be consistent across multiple
  server instances, rather than a shared cache like Redis.
- Choosing write-through for a genuinely write-heavy, rarely-re-read workload, adding real write
  latency for little corresponding benefit.

## ➡️ Next

Continue to [cdns-and-content-delivery.md](cdns-and-content-delivery.md) to see caching applied at
an even larger, geographically-distributed scale.
