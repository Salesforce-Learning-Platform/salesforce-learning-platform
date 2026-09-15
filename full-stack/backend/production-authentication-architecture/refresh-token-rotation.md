# 🔁 Refresh Token Rotation

## Why a Single, Long-Lived Refresh Token Is Risky

```
WITHOUT rotation: one refresh token, valid for 30 days. If it's ever
stolen, the attacker has a full 30-day window of access — and
nothing distinguishes their use of it from the real user's.
```

A refresh token that stays valid, unchanged, for its entire lifetime is a genuinely attractive
target: stealing it once grants access for its whole remaining lifespan, with no way to tell
legitimate use apart from an attacker's.

## Rotation — a New Refresh Token on Every Use

```js
app.post("/auth/refresh", async (req, res) => {
  const oldRefreshToken = req.cookies.refreshToken;
  const stored = await redis.get(`refresh:${oldRefreshToken}`);

  if (!stored) return res.status(401).json({ error: "Invalid refresh token" });

  // Issue a new access token AND a new refresh token
  const newAccessToken = signAccessToken(stored.userId);
  const newRefreshToken = generateRefreshToken();

  await redis.del(`refresh:${oldRefreshToken}`); // the old one is now DEAD
  await redis.set(`refresh:${newRefreshToken}`, JSON.stringify({ userId: stored.userId }), { EX: 2592000 });

  res.cookie("refreshToken", newRefreshToken, { httpOnly: true, secure: true });
  res.json({ accessToken: newAccessToken });
});
```

**Rotation** means every single time a refresh token is exchanged for a new access token, the
**old refresh token is immediately invalidated** and a genuinely **new** one is issued in its
place. This shrinks the useful lifetime of any single refresh token down to just the gap between
one use and the next — dramatically smaller than its full, nominal lifetime.

## Reuse Detection — Catching a Stolen Token in the Act

```
Normal flow:  token A used → token B issued (A is now dead)
              token B used → token C issued (B is now dead)

STOLEN token: an attacker steals token B, and tries to use it
              AFTER the real user already used it (and got token C)
              → the server sees an ALREADY-INVALIDATED token being
                reused → this is the signal something is genuinely
                wrong
```

Because each old token is deleted immediately after use, an attacker presenting a **previously
used, already-invalidated** refresh token is a strong, specific signal of compromise — a legitimate
client would never do this, since it always receives and uses the newest token. On detecting this,
the server invalidates the **entire token family** — every token descended from that same original
login — forcing genuine re-authentication, which locks the attacker back out along with the real
user (who simply logs in again).

## Implementing Reuse Detection

```js
if (!stored) {
  // The token wasn't found — either it never existed, or (more
  // concerningly) it was ALREADY used and deleted. Treat this as a
  // possible compromise: invalidate every token tied to this session family.
  await redis.del(`family:${familyId}:*`); // conceptual — invalidate the whole chain
  return res.status(401).json({ error: "Session invalidated — please log in again" });
}
```

Tracking a **token family ID** (a value shared across every rotation descending from one original
login) is what makes invalidating the *entire* chain possible on detected reuse, rather than only
the one specific token presented.

## Common Mistakes

- Implementing refresh tokens without rotation at all, leaving a single stolen token valid for its
  entire, often lengthy, remaining lifetime.
- Rotating tokens but failing to actually delete the old one, silently allowing both the old and
  new tokens to remain valid — defeating rotation's entire purpose.
- Detecting reuse but only invalidating the one specific reused token, rather than the whole token
  family — leaving other, already-issued tokens in the same compromised chain still valid.

## ➡️ Next

Continue to [storing-sessions-in-redis.md](storing-sessions-in-redis.md) to see exactly where
these refresh tokens (and their family IDs) actually live server-side.
