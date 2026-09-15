# ⚡ Caching — Local and Redis

## Purpose

Every database query covered throughout [SQL Fundamentals](../sql-fundamentals/) and
[MongoDB Fundamentals](../mongodb-fundamentals/) hits the real database, every single time — even
for data that barely changes. This module covers **caching**: storing a fast-to-read copy of
expensive-to-compute or slow-to-fetch data, specifically as an application-code implementation
concern (distinct from caching strategy at a system-design/architecture level, covered separately
and more conceptually elsewhere in this platform).

## 🎯 Learning Objectives

- Explain what caching is, and cache locally with a simple in-memory approach.
- Explain why Redis specifically fits application caching.
- Implement Redis caching in a real Express route.
- Explain the cache invalidation problem, and apply TTL-based expiration correctly.
- Use Redis's Pub/Sub feature for a basic event-driven pattern.

## 📋 Prerequisites

- [SQL Fundamentals](../sql-fundamentals/) or [MongoDB Fundamentals](../mongodb-fundamentals/) —
  this module caches the result of a real database query.
- [Storing Sessions in Redis](../production-authentication-architecture/storing-sessions-in-redis.md) —
  this module reuses the same Redis client setup, applied to a different purpose.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [what-is-caching.md](what-is-caching.md) | The core idea, and a simple local, in-memory cache |
| [redis-for-caching.md](redis-for-caching.md) | Why Redis specifically fits this job, beyond session storage |
| [implementing-redis-caching.md](implementing-redis-caching.md) | The cache-aside pattern in a real Express route |
| [the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md) | Why "cache invalidation is hard," and TTL-based strategies |
| [advanced-redis-features.md](advanced-redis-features.md) | TTL details, complex data structures, and Pub/Sub |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive
[the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md) — knowing *how* to
cache something is the easy half of this topic; knowing *when a cached value has gone stale* is
the genuinely hard, famous problem this module exists to teach a real, practical approach to.

## ✅ Quick Knowledge Check

<details>
<summary>If you're unsure exactly how to invalidate a specific cached value after an update, what's the simplest safe default?</summary>

Just delete the cache key — the next read will find nothing cached, fetch the real, current data
from the database, and repopulate the cache automatically (the same "lazy caching" pattern from
[implementing-redis-caching.md](implementing-redis-caching.md)). This is simpler and safer than a
complex, error-prone manual update of the cached value itself. See
[the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md).

</details>

<details>
<summary>Should every cached value use the exact same TTL?</summary>

No — a rapidly-changing value (like a live leaderboard) needs a short TTL (seconds), while a
rarely-changing value can use a much longer TTL (hours or days) as a safety net. See
[the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md).

</details>

## 📚 References

- AWS, [Caching Best Practices](https://aws.amazon.com/caching/best-practices/)
- Redis, [node-redis Pub/Sub](https://github.com/redis/node-redis/blob/master/docs/pub-sub.md)

## ➡️ Continue Your Learning Path

Continue to the [Payments Integration module](../payments-integration/) to see a genuinely
different kind of backend integration, building on the Express foundation this domain has
established throughout.
