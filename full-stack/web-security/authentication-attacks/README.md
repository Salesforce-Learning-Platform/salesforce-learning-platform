# 🔑 Authentication Attacks

## 📚 Overview

Earlier modules in this domain covered attacks around authentication — stealing cookies, forging
requests. This module covers attacks on authentication itself: JWT-specific vulnerabilities,
session fixation and hijacking, brute force and credential stuffing against the login process, and
how credentials should actually be stored to limit damage from an eventual breach.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain the `alg: none` and algorithm-confusion JWT attacks, and prevent both by explicitly
  pinning the verification algorithm.
- Distinguish session hijacking from session fixation, and prevent fixation with session
  regeneration on login.
- Mitigate brute force and credential stuffing with rate limiting, thoughtful lockout policy, and
  MFA.
- Explain why password hashing must be deliberately slow (bcrypt/argon2), never a fast
  general-purpose hash.

## 📋 Prerequisites

- [Production Authentication Architecture](../../backend/production-authentication-architecture/) — this module attacks the mechanisms implemented there.
- [Cookies, CORS, and Transport Security](../cookies-cors-and-transport-security/) — session attack mitigations build directly on the cookie attributes covered there.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [jwt-security.md](jwt-security.md) | `alg: none`, algorithm confusion, and weak-secret brute-forcing |
| [session-attacks.md](session-attacks.md) | Session hijacking vs. fixation, and regeneration on login |
| [brute-force-attacks.md](brute-force-attacks.md) | Rate limiting, lockout trade-offs, CAPTCHA, and MFA |
| [credential-security.md](credential-security.md) | One-way, slow password hashing and salting; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you implement or maintain any authentication system — every attack in this module
targets a mechanism nearly every real application relies on.

**Skim** if authentication is fully delegated to a managed third-party identity provider — the
underlying reasoning still helps you evaluate whether that provider's own implementation is sound.

## 🧠 Knowledge Check

<details>
<summary>Why is explicitly pinning the expected algorithm during JWT verification more important than simply rejecting the "none" algorithm specifically?</summary>

Rejecting `none` alone doesn't close the algorithm-confusion attack, where a server expecting RS256
can be tricked into verifying an HS256-signed token using the (publicly known) RSA public key as an
HMAC secret. Explicitly specifying the expected algorithm(s) in the verification call — rather than
trusting whatever the token's own header claims — closes both attacks at once, since attacker-
controlled input never decides how the server validates it.

</details>

<details>
<summary>Why must a password-hashing algorithm be deliberately slow, when speed is normally a desirable property in cryptography?</summary>

A fast hash is exactly the wrong property for password storage — it makes offline brute-forcing of
stolen hashes dramatically faster for an attacker. A deliberately slow algorithm like bcrypt adds a
negligible delay to one legitimate login but a genuinely significant barrier when an attacker tries
to crack millions of stolen hashes at scale.

</details>

## 📚 References

- [Auth0 - Critical Vulnerabilities in JSON Web Token Libraries](https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/) — official source for the `alg: none` and algorithm-confusion attacks
- [OWASP Top 10:2025](https://top10.owasp.org/2025) — Authentication Failures remains a current, severe risk category

## ➡️ Continue Your Learning Path

Continue to [Server-Side Attacks](../server-side-attacks/) to see attacks that target the server
itself, beyond authentication specifically.
