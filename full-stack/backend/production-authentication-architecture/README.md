# 🔐 Production Authentication Architecture

## Purpose

[Authentication and Authorization](../authentication-and-authorization/) taught JWTs and sessions
as two distinct, complete mechanisms. A real production system almost always combines ideas from
both — this module covers the actual, more sophisticated architecture real applications use:
short-lived access tokens, longer-lived refresh tokens, rotation, Redis-backed storage, and
"logout everywhere," building directly on that module rather than repeating its fundamentals.

## 🎯 Learning Objectives

- Explain the full production authentication flow: access token, refresh token, rotation, Redis,
  logout everywhere.
- Implement refresh token rotation and understand reuse detection.
- Store sessions and refresh tokens in Redis, and explain why Redis specifically fits this need.
- Build a genuine "logout from all devices" feature.
- Explain the real CSRF risk in single-page applications, and the cookie-to-header mitigation
  pattern.

## 📋 Prerequisites

- [Authentication and Authorization](../authentication-and-authorization/) — this module assumes
  JWT and session fundamentals are already understood, and builds a more sophisticated system on
  top of them.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [the-production-auth-flow.md](the-production-auth-flow.md) | The full picture: browser → access token → refresh token → rotation → Redis → logout |
| [refresh-token-rotation.md](refresh-token-rotation.md) | Why a single long-lived refresh token is risky, and how rotation with reuse detection fixes it |
| [storing-sessions-in-redis.md](storing-sessions-in-redis.md) | Why Redis specifically fits session/token storage |
| [logout-from-all-devices.md](logout-from-all-devices.md) | Building a genuine, immediate "logout everywhere" feature |
| [csrf-in-spas.md](csrf-in-spas.md) | The real CSRF risk for a single-page app, and the cookie-to-header pattern |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [refresh-token-rotation.md](refresh-token-rotation.md) — reuse detection is the single
mechanism that actually catches a stolen refresh token in the real world, and precisely
understanding how it works is far more valuable than memorizing the rotation flow's steps alone.

## ✅ Quick Knowledge Check

<details>
<summary>If an attacker steals a refresh token and the legitimate user has already used it once since, what happens when the attacker tries to use their stolen copy?</summary>

The system detects a reuse of an already-exchanged refresh token and invalidates the entire token
family — every refresh token descended from that original one — forcing the legitimate user to
re-authenticate. This is exactly the security benefit rotation with reuse detection provides. See
[refresh-token-rotation.md](refresh-token-rotation.md).

</details>

<details>
<summary>Does storing a JWT in localStorage instead of a cookie eliminate CSRF risk entirely?</summary>

It removes the traditional cookie-based CSRF risk (since the browser doesn't automatically attach
localStorage data to a cross-site request the way it does cookies) — but it introduces its own
tradeoffs, and the still-recommended cookie-to-header pattern achieves similar protection while
using cookies deliberately. See [csrf-in-spas.md](csrf-in-spas.md).

</details>

## 📚 References

- Auth0, [Refresh Token Rotation](https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation)
- OWASP, [Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- Redis, [Node.js client (node-redis)](https://github.com/redis/node-redis)

## ➡️ Continue Your Learning Path

Continue to the [Real-Time Communication module](../real-time-communication/) to apply this
authenticated foundation to a WebSocket connection.
