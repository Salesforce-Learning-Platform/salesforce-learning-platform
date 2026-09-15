# 🗄️ Storing Sessions in Redis

## Why Not Just the Application's Own Database?

The [SQL](../sql-fundamentals/) or [MongoDB](../mongodb-fundamentals/) database already covered in
this domain genuinely *could* store refresh tokens — but a refresh token needs to be looked up on
essentially every authenticated request, and needs to expire automatically after a fixed time. A
general-purpose database isn't specifically optimized for either of those two needs the way a
dedicated, in-memory data store is.

## Why Redis Specifically Fits This Job

- **Speed** — Redis is an in-memory data store, making a token lookup on every request
  dramatically faster than a disk-backed database query for the same job.
- **Built-in expiration (TTL)** — Redis keys can be set with an automatic time-to-live; a refresh
  token record simply *disappears* on its own once expired, with no separate cleanup job needed at
  all.
- **Simple key-value access pattern** — a refresh token lookup is fundamentally "given this token
  string, find its associated data" — exactly Redis's core, optimized use case.

## Storing a Refresh Token With Automatic Expiration

```js
import { createClient } from "redis";
const redis = createClient();
await redis.connect();

// Store a refresh token, set to expire automatically in 30 days
await redis.set(
  `refresh:${refreshToken}`,
  JSON.stringify({ userId: user.id, familyId }),
  { EX: 30 * 24 * 60 * 60 } // TTL in seconds
);
```

The `EX` option sets the key's TTL directly — after 30 days, Redis automatically removes it with no
separate scheduled job or manual cleanup query required, directly solving the "how do we make sure
expired tokens don't linger forever" problem that a plain database table would need extra logic to
handle.

## Looking Up a Token on Every Refresh Request

```js
const stored = await redis.get(`refresh:${refreshToken}`);
if (!stored) {
  // either genuinely invalid, or already used — per refresh-token-rotation.md
}
```

This lookup runs on every single token-refresh request — exactly the operation Redis's raw
in-memory speed makes practical at scale, in a way that would add real, noticeable latency against
a general-purpose disk-backed database under heavy traffic.

## Common Mistakes

- Storing refresh tokens in the primary application database without setting any expiration logic,
  requiring a separate scheduled cleanup job to remove stale records — something Redis's TTL
  already handles automatically.
- Using Redis as if it were a permanent, general-purpose database for data that genuinely needs to
  persist indefinitely — Redis's typical role here is specifically for short-lived,
  frequently-accessed session/token data, not an application's core, permanent records.
- Forgetting to actually set a TTL on a Redis key at all, leaving tokens stored indefinitely with
  no automatic expiration.

## ➡️ Next

Continue to [logout-from-all-devices.md](logout-from-all-devices.md) to use this same Redis-backed
storage to build a genuine, immediate logout feature.
