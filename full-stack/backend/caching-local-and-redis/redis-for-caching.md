# 🗄️ Redis for Caching

## A Shared Cache, Outside Any Single Server Process

```
Server A ──┐
           ├──► Redis (ONE shared cache, external to both servers)
Server B ──┘
```

[Storing Sessions in Redis](../production-authentication-architecture/storing-sessions-in-redis.md)
already introduced Redis as a fast, in-memory data store with built-in expiration — the exact same
properties that make it well-suited to caching, applied to a genuinely different purpose here.
Because Redis runs as its own, separate service, **every** server instance reads from and writes to
the *same* shared cache — directly solving
[what-is-caching.md](what-is-caching.md)'s multi-server inconsistency problem: whichever server
happens to handle a request, it sees the identical, shared cached data.

## Why Redis Specifically, Not the Application's Main Database

The application's own [SQL](../sql-fundamentals/) or [MongoDB](../mongodb-fundamentals/) database
could technically also store cached values — but a cache needs to be read constantly, extremely
fast, and expire automatically, exactly the three properties
[storing-sessions-in-redis.md](../production-authentication-architecture/storing-sessions-in-redis.md)
already established Redis excels at: in-memory speed, and TTL-based automatic expiration with no
manual cleanup job required.

## Connecting to Redis for Caching

```js
import { createClient } from "redis";
const redis = createClient();
await redis.connect();

// The SAME client setup already used for session/token storage —
// applied here to a different kind of data entirely
```

The exact same `node-redis` client setup already covered for session storage works identically for
caching — Redis itself doesn't distinguish between "a cache" and "a session store"; it's simply a
fast key-value store, and the *purpose* of a given key is entirely up to the application using it.

## A Cache and a Database Serve Genuinely Different Roles

| | The application's database (SQL/MongoDB) | Redis, used as a cache |
|---|---|---|
| Source of truth | Yes — the real, permanent data | No — a fast, temporary copy |
| Survives a restart | Yes | Not guaranteed — and that's fine, since it's just a cache |
| Speed | Slower (disk-backed, more complex queries) | Very fast (in-memory) |

A cache is never the source of truth — it's always a disposable, regenerable copy of data that
genuinely lives somewhere else. Losing a cache's contents (a Redis restart, an eviction) is
recoverable by re-fetching from the real database; losing the real database's data is not.

## Common Mistakes

- Treating Redis-as-cache as if it were the application's actual, permanent data store — a cache
  should always be regenerable from the real source of truth, never the only copy of something.
- Reaching for the application's main database to store cached values instead of Redis, missing
  out on the speed and automatic-expiration benefits Redis specifically provides.
- Assuming Redis solves caching automatically just by being fast — the actual caching *logic*
  (when to read from cache, when to bypass it, when to invalidate it) still needs to be built
  deliberately, covered next.

## ➡️ Next

Continue to [implementing-redis-caching.md](implementing-redis-caching.md) to write that actual
caching logic in a real Express route.
