# 🛠️ Implementing Redis Caching

## The Cache-Aside Pattern

```js
app.get("/products/featured", async (req, res) => {
  const cacheKey = "featured-products";

  // 1. Check the cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return res.json(JSON.parse(cached)); // FAST — no database hit
  }

  // 2. Cache miss — fetch the real data
  const products = await db.query("SELECT * FROM products WHERE featured = true");

  // 3. Populate the cache for NEXT time, with a TTL
  await redis.set(cacheKey, JSON.stringify(products), { EX: 300 }); // 5 minutes

  res.json(products);
});
```

This is the **cache-aside** pattern (also called "lazy caching"): check the cache first; on a
**miss** (nothing cached, or expired), fetch the real data from the database, then populate the
cache for next time. This is the most common, practical caching pattern precisely because it's
simple and self-healing — a cache that's empty, cleared, or expired just gets naturally
repopulated on the very next request, per
[the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md)'s "when in doubt,
delete the key" guidance.

## Why JSON Serialization Is Needed

```js
await redis.set(cacheKey, JSON.stringify(products), { EX: 300 }); // store as a STRING
const cached = await redis.get(cacheKey);
const products = JSON.parse(cached); // parse it back into a real object/array
```

Redis's basic `SET`/`GET` commands store and retrieve **strings** — a real JavaScript array or
object needs to be explicitly serialized with `JSON.stringify()` before storing, and parsed back
with `JSON.parse()` after retrieving. Forgetting either step is a common, easy mistake: storing an
object directly (without stringifying) stores the unhelpful literal string `"[object Object]"`
instead of the actual data.

## Choosing What to Cache

```
GOOD candidates: a featured-products list (changes rarely, read
constantly), a user's profile data (read on nearly every request),
an expensive aggregate calculation

POOR candidates: data that's genuinely different on every single
request anyway (a personalized, real-time search result), or data
where staleness is genuinely unacceptable (a real-time stock price
feeding an actual trade)
```

Caching is worth the added complexity specifically for data that's **read often** relative to how
**often it actually changes** — the bigger that ratio, the more a cache pays for itself. Data that
changes just as often as it's read gains little from caching, since the cache would need
invalidating almost as often as it's used.

## Cache Key Naming — a Real, Practical Convention

```js
const cacheKey = `product:${productId}`;           // one specific product
const cacheKey = `products:category:${category}`;  // one category's listing
const cacheKey = `user:${userId}:cart`;             // one user's own cart
```

A consistent, descriptive key naming convention (directly analogous to
[REST's resource-based-routing.md](../rest-api-design/resource-based-routing.md)'s consistent URL
naming) makes a cache's contents predictable and makes targeted invalidation (deleting exactly the
right key, per [the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md))
genuinely possible, rather than needing to guess or clear the entire cache indiscriminately.

## Common Mistakes

- Forgetting `JSON.stringify()`/`JSON.parse()` when caching a real object or array, storing an
  unusable literal string instead of the actual data.
- Caching data that changes on nearly every request, adding real complexity for little to no
  actual performance benefit.
- Using vague, inconsistent cache key names, making it hard to know exactly what's cached or to
  invalidate precisely the right entry later.

## ➡️ Next

Continue to
[the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md) to see the genuinely
hard half of caching: knowing when a cached value has gone stale.
