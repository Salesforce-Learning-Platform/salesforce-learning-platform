# 🚪 Logout from All Devices

## Why This Is Genuinely Hard With JWTs Alone

Recall [jwt.md](../authentication-and-authorization/jwt.md)'s central limitation: a plain JWT
access token, once issued, stays cryptographically valid until it naturally expires — there's no
built-in way to revoke one early. "Logout from all devices" specifically requires exactly that
early revocation, across every device a user is currently logged in on — which is precisely why
this feature depends on the Redis-backed refresh token storage from
[storing-sessions-in-redis.md](storing-sessions-in-redis.md), not the access token itself.

## Tracking Every Active Session Per User

```js
// When a user logs in on a new device, store the refresh token
// under a set keyed by their user ID, not just its own key
await redis.sAdd(`user:${user.id}:refreshTokens`, refreshToken);
await redis.set(`refresh:${refreshToken}`, JSON.stringify({ userId: user.id }), { EX: 2592000 });
```

Storing every active refresh token in a set associated with the user (`user:${id}:refreshTokens`),
in addition to its own individual key, makes it possible to find and invalidate **every** session
belonging to that user at once — not just the one currently being used.

## Implementing "Logout Everywhere"

```js
app.post("/auth/logout-all", requireAuth, async (req, res) => {
  const tokens = await redis.sMembers(`user:${req.user.userId}:refreshTokens`);

  for (const token of tokens) {
    await redis.del(`refresh:${token}`);
  }
  await redis.del(`user:${req.user.userId}:refreshTokens`);

  res.json({ message: "Logged out from all devices" });
});
```

This deletes every refresh token tied to the user across every device — the next time any of those
devices tries to use its now-deleted refresh token, per
[refresh-token-rotation.md](refresh-token-rotation.md)'s reuse-detection logic, it fails and forces
a fresh login. Existing access tokens on those devices remain technically valid until they
naturally expire (per [the-production-auth-flow.md](the-production-auth-flow.md)'s point about
short access-token lifetimes) — this is exactly why keeping the access token's lifetime genuinely
short matters: it caps how long a "logged out everywhere" device can still make authenticated
requests using an already-issued access token.

## A Realistic Use Case

A user suspects their account has been compromised, or simply lost a device with an active
session — "logout from all devices" lets them immediately invalidate every other session without
needing to individually track down or wait for each one to expire naturally.

## Common Mistakes

- Deleting only the current session's refresh token when the user actually wanted to log out
  everywhere, leaving other devices' sessions untouched.
- Assuming "logout everywhere" also instantly invalidates already-issued access tokens — it only
  ever revokes the *refresh* tokens; a short access-token lifetime is what actually bounds how long
  a stale session can still make requests.
- Forgetting to also remove the now-empty tracking set (`user:${id}:refreshTokens`) after logging
  out everywhere, leaving stale bookkeeping data behind.

## ➡️ Next

Continue to [csrf-in-spas.md](csrf-in-spas.md) to see a genuinely different, browser-specific
security concern this whole authentication architecture also needs to account for.
