# 💡 What Is Caching?

## Storing a Fast Copy of Slow-to-Get Data

```js
// Without caching: EVERY request re-runs the real, expensive query
app.get("/products/featured", async (req, res) => {
  const products = await db.query("SELECT * FROM products WHERE featured = true"); // every time
  res.json(products);
});
```

**Caching** means storing a fast-to-read copy of a value that's expensive or slow to produce — a
database query result, a computed value — so that a repeated request for the same thing can be
answered from the fast copy instead of redoing the expensive work every single time.

## A Simple Local, In-Memory Cache

```js
const cache = new Map();

app.get("/products/featured", async (req, res) => {
  if (cache.has("featured-products")) {
    return res.json(cache.get("featured-products")); // FAST — no database hit at all
  }

  const products = await db.query("SELECT * FROM products WHERE featured = true");
  cache.set("featured-products", products);
  res.json(products);
});
```

A plain JavaScript `Map` (or even a simple object) held in the server's own memory is the simplest
possible cache — genuinely useful for a single-server application with data that changes
infrequently. The tradeoff: this cache exists only in *this one process's* memory — restarting the
server clears it entirely, and (per
[Backend Architecture](../backend-architecture/scalable-backend-structure.md)'s scaling concerns) a
second server instance would have its own, completely separate, out-of-sync copy.

## Why Local Caching Doesn't Scale to Multiple Servers

```
Server A's cache: "featured-products" → [Keyboard, Mouse]
Server B's cache: "featured-products" → EMPTY (never populated on this instance)

A user's request could land on EITHER server — the cache benefit
is inconsistent, and the two servers' cached data can drift apart
entirely.
```

The moment an application runs on more than one server instance — a real, common production
scenario — a local, in-memory cache stops being reliably useful: each instance maintains its own,
independent copy, with no way to keep them in sync, and no shared benefit from one instance's cache
being warmed by traffic another instance actually received.

## Common Mistakes

- Relying on local, in-memory caching for an application already running on (or planning to scale
  to) multiple server instances, producing an inconsistent, unreliable caching benefit.
- Caching something that changes on every single request anyway — caching only helps when the
  same value is genuinely requested repeatedly without changing in between.
- Never clearing a local cache at all, letting genuinely stale data linger indefinitely with no
  expiration mechanism.

## ➡️ Next

Continue to [redis-for-caching.md](redis-for-caching.md) to see the shared, external caching
layer that actually solves the multi-server problem.
