# 🧰 Advanced Redis Features

## TTL — Beyond a Simple Expiration Time

```js
await redis.set("key", "value", { EX: 300 }); // expires in 300 seconds

const remaining = await redis.ttl("key"); // check how much time is left, in seconds
await redis.expire("key", 600);            // change an existing key's TTL
await redis.persist("key");                // remove a key's TTL entirely — it never expires
```

Beyond setting a TTL at creation time (per
[the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md)), Redis lets an
already-set TTL be checked, extended, or removed entirely — useful for a value whose "freshness
window" needs to be reset in response to real application activity (extending a session's timeout
on genuine user activity, for instance).

## Complex Data Structures, Not Just Strings

```js
// A Set — useful for tracking unique membership, like Logout from
// All Devices' per-user refresh token tracking
await redis.sAdd("user:42:refreshTokens", "token-abc");
await redis.sMembers("user:42:refreshTokens"); // every member

// A Hash — useful for storing an object's fields without a full
// JSON.stringify/parse round trip for the whole thing
await redis.hSet("product:42", { name: "Keyboard", price: "79.99" });
await redis.hGet("product:42", "price");
```

Redis isn't limited to simple string key-value pairs — **Sets** (already used for
[logout-from-all-devices.md](../production-authentication-architecture/logout-from-all-devices.md)'s
per-user token tracking) and **Hashes** (storing an object's individual fields directly, without a
full JSON serialize/deserialize round trip) are genuinely useful, purpose-built structures for
specific caching and data-tracking needs beyond plain `GET`/`SET`.

## Pub/Sub — Event-Driven Communication

```js
// Subscriber — needs its own DEDICATED connection
const subscriber = redis.duplicate();
await subscriber.connect();
await subscriber.subscribe("product-updated", (message) => {
  console.log("Product changed:", message);
  cache.del(`product:${JSON.parse(message).id}`); // react by invalidating a cache entry
});

// Publisher — from anywhere else in the application
await redis.publish("product-updated", JSON.stringify({ id: 42 }));
```

Redis **Pub/Sub** lets one part of an application publish a message to a named channel, while any
number of other parts (potentially on entirely different server processes) subscribe and react —
directly comparable to [Socket.io's event-based model](../real-time-communication/working-with-socketio.md),
but for server-to-server communication rather than server-to-browser. A genuinely practical use: a
service that updates a product publishes an event, and any number of other services (including one
specifically responsible for cache invalidation) can subscribe and react, decoupling the actual
update logic from every consumer that needs to know about it.

## Why Pub/Sub Needs a Dedicated Connection

A client actively subscribed to a channel can't simultaneously issue other Redis commands over that
same connection — subscribing effectively "takes over" the connection for receiving messages. This
is exactly why the subscriber above uses `redis.duplicate()` to create a genuinely separate
connection, keeping the original client free to continue issuing normal `GET`/`SET` commands.

## Common Mistakes

- Trying to issue regular Redis commands on the same connection that's actively subscribed to a
  Pub/Sub channel — a dedicated, duplicated connection is required for subscribing.
- Reaching for a complex data structure (a Hash, a Set) when a plain string value would have been
  simpler and entirely sufficient for the actual need.
- Using Pub/Sub for something that genuinely needs guaranteed delivery — Redis Pub/Sub messages are
  fire-and-forget; a subscriber that isn't currently connected simply misses the message entirely,
  unlike a proper message queue.

## Module Summary

Across this module: **caching** stores a fast copy of expensive-to-produce data, with a simple
local, in-memory cache working for a single server but breaking down across multiple instances
(see [what-is-caching.md](what-is-caching.md)); **Redis**, already familiar from session storage,
fits caching for the same reasons — speed and built-in TTL — now shared across every server
instance (see [redis-for-caching.md](redis-for-caching.md)); the **cache-aside pattern** — check
cache, fetch on a miss, populate for next time — is the standard, self-healing way to implement
this in a real route (see [implementing-redis-caching.md](implementing-redis-caching.md));
**cache invalidation** is a genuinely hard, famous problem, made manageable with TTL as a safety
net and "just delete the key" as a safe default when precise invalidation logic is unclear (see
[the-cache-invalidation-challenge.md](the-cache-invalidation-challenge.md)); and Redis's
**advanced features** — TTL management, Sets/Hashes, and Pub/Sub for event-driven communication —
extend well beyond basic caching into the broader session and real-time patterns already covered
elsewhere in this domain.
