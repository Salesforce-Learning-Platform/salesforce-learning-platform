# 🎫 JWT Security

## Attacking the Mechanism That Proves Identity

Every module so far in this domain covered attacks *around* authentication — stealing a session
cookie, forging a request. This module turns to attacking **authentication itself** — starting with
JSON Web Tokens (JWTs), already covered from the implementation side in
[Production Authentication Architecture](../../backend/production-authentication-architecture/),
earlier in this repository's Backend domain.

## Attack 1: The `alg: none` Vulnerability

```
A JWT has three parts: HEADER.PAYLOAD.SIGNATURE

The "none" algorithm exists in the JWT spec for situations
where integrity is ALREADY verified some other way - but some
JWT LIBRARIES historically accepted a token claiming "alg": "none"
as VALID, with NO signature check at all.
```

```json
{"alg": "none", "typ": "JWT"}.{"userId": 42, "role": "admin"}.
```

An attacker who discovers a vulnerable library can simply construct a token claiming `alg: none`,
set whatever claims they want (`role: admin`), attach an empty signature, and have it accepted as
fully valid — no secret key knowledge required at all. Per Auth0's own documented guidance, modern
libraries now reject `none` when a secret key is configured, but the underlying lesson remains: never
let a token's own header dictate which algorithm the server uses to verify it.

## Attack 2: Algorithm Confusion (RS256 → HS256)

```
The server expects RS256 (asymmetric: a PRIVATE key signs, a
PUBLIC key verifies) - but if the verification code doesn't
EXPLICITLY pin the expected algorithm, an attacker can sign a
forged token using HS256, with the PUBLIC key (which is, by
design, publicly known) as the HMAC secret.
```

This is a genuinely subtle, severe attack: the public key is meant to be public — that's the entire
point of asymmetric cryptography — but if the server's verification logic doesn't explicitly demand
RS256 specifically, it can be tricked into treating that same public value as a symmetric HMAC
secret, letting the attacker "sign" a forged token the server then accepts as genuinely valid.

## Attack 3: Weak Secret Brute-Forcing

```
HS256 uses an arbitrary STRING as its signing secret - if that
secret is short, guessable, or a common word, an attacker can
BRUTE-FORCE it directly against a KNOWN, legitimate token
(dictionary tools like jwt_tool or jwt-cracker exist specifically
for this).
```

Once an attacker recovers the actual signing secret, they can forge *any* token they want, with any
claims — including an admin role, per Attack 1's example — and have it accepted as fully,
legitimately valid, since it's now genuinely signed with the real secret.

## The Fix: All Three Attacks, One Underlying Discipline

```
1. NEVER trust the "alg" field from an incoming token - the
   verification code should EXPLICITLY specify the expected
   algorithm(s), never read it from the token itself
2. Use a CRYPTOGRAPHICALLY STRONG secret (32+ random bytes) for
   HMAC algorithms - never a short, guessable string
3. NEVER hardcode a secret in source code - manage it per
   Secrets Management, later in this domain
```

```js
jwt.verify(token, secret, { algorithms: ["HS256"] });   // explicit, pinned
```

Explicitly pinning the expected algorithm in the verification call itself — rather than trusting
whatever the token's own header claims — closes both the `none` and the algorithm-confusion attacks
at once, directly by never letting attacker-controlled input decide how the server validates it.

## Token Theft: the Remaining, Genuine Risk

```
Even with PERFECT JWT implementation, a STOLEN, genuinely valid
token remains valid and usable until it EXPIRES - this is why
short token lifetimes and refresh-token ROTATION (already covered
in Production Authentication Architecture) matter as much as the
JWT's own cryptographic correctness.
```

## Common Mistakes

- Reading the algorithm to use for verification from the token's own header, rather than explicitly
  pinning it in the verification call.
- Using a short, common, or hardcoded string as an HMAC secret, leaving it vulnerable to
  dictionary-based brute-forcing.
- Treating a cryptographically correct JWT implementation as sufficient on its own, without the
  short-lived-token and rotation discipline that limits the damage from genuine token theft.

## ➡️ Next

Continue to [session-attacks.md](session-attacks.md) to see the equivalent attacks against
traditional, cookie-based session authentication.
