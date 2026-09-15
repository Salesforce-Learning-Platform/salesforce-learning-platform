# 🔑 Credential Security

## Limiting the Damage From an Eventual Breach

Every attack covered so far in this module assumes credentials remain safely stored. This file
covers the deliberately pessimistic complement: given that a breach is *always* a genuine
possibility, how credentials are actually stored determines how much real damage that breach
eventually causes.

## Never Store Passwords in Plain Text

```
If a database is ever breached, PLAIN-TEXT passwords are
IMMEDIATELY usable by the attacker - for THIS application, and
(per credential stuffing, from brute-force-attacks.md) for every
OTHER service where a user reused the same password.
```

This should already be an absolute, non-negotiable baseline — a plain-text password breach doesn't
just compromise one application, it compromises every other service a user happens to have reused
that same password on.

## Hashing: One-Way, by Design

```js
import bcrypt from "bcrypt";

const passwordHash = await bcrypt.hash(plainPassword, 12);   // 12 = cost factor

const isValid = await bcrypt.compare(submittedPassword, passwordHash);
```

A password **hash** is deliberately, mathematically **one-way** — there's no operation that
reverses a hash back into the original password. Verifying a login means hashing the *submitted*
password the same way and comparing the two hashes, never storing or comparing the plain-text value
at all. `bcrypt` (and similar algorithms like `argon2`) are specifically designed to be
computationally *slow* — deliberately, since this directly limits how fast an attacker holding
stolen hashes could brute-force them offline.

## Why the Cost Factor Matters

```
A HIGHER cost factor (bcrypt's "12" above) makes EACH individual
hash computation slower - genuinely negligible for ONE real login
attempt, but genuinely significant when an attacker is trying to
brute-force MILLIONS of stolen hashes offline.
```

This is the deliberate design trade-off behind algorithms like bcrypt — a fraction-of-a-second delay
on a single legitimate login is imperceptible to a real user, but multiplied across an attacker's
attempt to crack millions of stolen hashes, that same delay becomes a genuinely significant,
practical barrier.

## Never Use Fast, General-Purpose Hashes for Passwords

```
MD5, SHA-256 (used correctly elsewhere, e.g. for file integrity)
→ WRONG for passwords - they're designed to be FAST, which is
  EXACTLY the wrong property for something an attacker wants to
  brute-force offline.

bcrypt, argon2, scrypt → RIGHT for passwords - deliberately slow,
  by design, specifically to resist offline brute-forcing.
```

This is a genuinely common, real mistake worth naming explicitly: an algorithm being cryptographically
"strong" in a general sense doesn't automatically make it appropriate for password storage
specifically — the deliberate slowness of a password-hashing algorithm is a *feature*, not a
performance flaw to work around.

## Salting: Defeating Precomputed Attacks

```
A SALT is random data mixed into each password BEFORE hashing -
bcrypt handles this AUTOMATICALLY, generating and storing a
unique salt per password, so identical passwords produce
DIFFERENT hashes.
```

Without a salt, an attacker could precompute a lookup table (a "rainbow table") of common password
hashes once and reuse it against any breached database — a unique salt per password defeats this
precomputation entirely, forcing a genuinely fresh brute-force attempt against each individual
hash.

## Common Mistakes

- Storing passwords in plain text or with reversible encryption instead of a genuinely one-way
  hash, turning any future breach into an immediate, total credential compromise.
- Using a fast, general-purpose hash (MD5, plain SHA-256) for passwords specifically, missing that
  deliberate slowness is the actual desired property here.
- Implementing manual salting incorrectly (a single, shared salt for every password) instead of
  relying on bcrypt's own automatic, per-password salt generation.

## Module Summary

Across this module: **JWT attacks** — the `alg: none` bypass, algorithm confusion, and weak-secret
brute-forcing — are prevented by explicitly pinning the expected algorithm during verification and
using a genuinely strong secret, verified against Auth0's own documented guidance (see
[jwt-security.md](jwt-security.md)); **session attacks** — hijacking (stealing a valid session) and
fixation (pre-establishing a known one) — are addressed by `HttpOnly`/`Secure` cookies and
regenerating the session ID on every successful login (see [session-attacks.md](session-attacks.md));
**brute force and credential stuffing** target the login process itself, mitigated by rate
limiting, thoughtfully-designed lockout policies, and MFA closing off the category entirely (see
[brute-force-attacks.md](brute-force-attacks.md)); and **credential security** — one-way,
deliberately slow hashing (bcrypt/argon2) with automatic per-password salting, never plain text or
a fast general-purpose hash — determines how much real damage an eventual breach actually causes.
