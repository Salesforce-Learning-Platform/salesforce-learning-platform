# 🗺️ The Production Auth Flow

## Combining Ideas From Both Prior Approaches

```
1. User logs in with correct credentials (per password-hashing.md)
2. Server issues TWO tokens:
   - a short-lived ACCESS TOKEN (a JWT, per jwt.md)
   - a longer-lived REFRESH TOKEN (stored server-side, in Redis)
3. Every API request carries the access token
4. When the access token expires, the client uses the refresh
   token to get a NEW access token (and, per rotation, a new
   refresh token too)
5. Logging out (or "logout everywhere") invalidates the refresh
   token(s) in Redis immediately
```

Recall [jwt.md](../authentication-and-authorization/jwt.md)'s core tradeoff: a JWT is stateless
and scalable, but genuinely hard to revoke early. Recall
[sessions.md](../authentication-and-authorization/sessions.md)'s opposite tradeoff: sessions are
instantly revocable, but require server-side storage. This production flow deliberately combines
both: a **short-lived JWT access token** for fast, stateless request verification, paired with a
**longer-lived, server-tracked refresh token** for the instant-revocability sessions provide.

## Why the Access Token Is Deliberately Short-Lived

```
Access token expiresIn: "15m"   ← short, so a stolen one is only
                                   usable for a brief window
Refresh token expiresIn: "30d"  ← longer, but tracked and revocable
                                   server-side, unlike the access token
```

A short access-token lifetime directly limits the damage a stolen token can do — even if one leaks,
it naturally stops working within minutes. The refresh token bears the actual "stay logged in for a
long time" responsibility instead, but — unlike the access token — its validity is tracked
server-side (in Redis, per [storing-sessions-in-redis.md](storing-sessions-in-redis.md)), so it can
genuinely be revoked at any moment, unlike a JWT.

## Where Each Piece Fits

| Concept | Covered in |
|---|---|
| Password verification | [password-hashing.md](../authentication-and-authorization/password-hashing.md) |
| Access token structure | [jwt.md](../authentication-and-authorization/jwt.md) |
| Refresh token rotation | [refresh-token-rotation.md](refresh-token-rotation.md) |
| Server-side token storage | [storing-sessions-in-redis.md](storing-sessions-in-redis.md) |
| Revoking access instantly | [logout-from-all-devices.md](logout-from-all-devices.md) |

## Common Mistakes

- Giving the access token itself a long lifetime "for convenience," reintroducing exactly the
  revocation problem short-lived access tokens exist to limit.
- Treating this as a replacement for everything in
  [Authentication and Authorization](../authentication-and-authorization/) rather than a more
  sophisticated architecture built directly on top of it.
- Storing the refresh token the same way as the access token (e.g., also as a stateless JWT with no
  server-side record) — that would lose the entire revocability benefit this architecture exists to
  provide.

## ➡️ Next

Continue to [refresh-token-rotation.md](refresh-token-rotation.md) to see exactly how the refresh
token itself is kept secure over its longer lifetime.
