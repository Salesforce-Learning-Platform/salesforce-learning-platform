# 🔐 Cookie Security Beyond the Core Attributes

## The Attributes Aren't the Whole Picture

[secure-cookie-attributes.md](secure-cookie-attributes.md) covered `Secure`, `HttpOnly`, and
`SameSite` — necessary, but not sufficient on their own. A cookie's actual *content*, *scope*, and
*lifecycle* all matter just as much for genuine security.

## Never Store Sensitive Data Directly in a Cookie

```
BAD:  Set-Cookie: user={"id":42,"role":"admin","email":"..."}

GOOD: Set-Cookie: sessionId=a1b2c3d4-e5f6...
      (an OPAQUE, random identifier - the actual user data lives
      SERVER-SIDE, looked up by this identifier)
```

Even with `HttpOnly` and `Secure` set, a cookie's *content* is still visible to the server and, in
some configurations, potentially inspectable by other means — an opaque session identifier, with
the real data kept server-side, means a compromised cookie value alone reveals nothing meaningful
about the user.

## Cookie Scope: `Domain` and `Path`

```http
Set-Cookie: sessionId=abc123; Domain=myapp.com; Path=/
```

```
Domain=myapp.com  → the cookie is sent to myapp.com AND every
                     subdomain (api.myapp.com, admin.myapp.com)

Path=/admin        → the cookie is ONLY sent for requests under
                     /admin - narrowing its actual exposure
```

Deliberately scoping a cookie as narrowly as genuinely necessary — directly applying the
[least-privilege principle](../the-security-mindset/security-principles.md) from earlier in this
domain — limits exactly which requests actually carry a given cookie, reducing its real exposure if
any one part of the system is ever compromised.

## Session Expiration and Rotation

```
A session cookie with NO expiration (or an extremely long one)
remains valid INDEFINITELY - if it's ever stolen (despite Secure/
HttpOnly), it grants access for as long as it remains valid.
```

```js
res.cookie("sessionId", newSessionId, { maxAge: 24 * 60 * 60 * 1000 });   // rotate on login
```

Setting a reasonable expiration, and **rotating** the session identifier at meaningful moments (a
successful login, a privilege change) directly limits how long a compromised session cookie remains
useful to an attacker — this is exactly the same reasoning already established for
[Let's Encrypt's deliberately short-lived certificates](../../production-systems/domains-dns-and-ssl/ssl-and-tls.md),
earlier in this repository: a shorter validity window meaningfully limits the damage from any single
compromise.

## Invalidating Sessions Server-Side

```
Deleting a cookie CLIENT-SIDE (logging out in the browser) does
NOT necessarily invalidate the session SERVER-SIDE - if the
server doesn't ALSO mark that session as invalid, a copy of the
old cookie value (if somehow obtained) would still work.
```

A genuinely secure logout needs to invalidate the session on the *server* — removing it from
whatever session store tracks valid sessions — not merely instruct the browser to discard its own
local copy, which an attacker holding a separately-obtained copy would never be affected by at all.

## Common Mistakes

- Storing meaningful user data directly inside a cookie's value instead of an opaque identifier
  looked up server-side, exposing real information if the cookie is ever inspected.
- Setting an overly broad `Domain` or `Path` scope, unnecessarily sending a sensitive cookie to
  parts of the system that never actually need it.
- Treating client-side cookie deletion as equivalent to genuine session invalidation, when only a
  server-side invalidation actually revokes a session's real validity.

## ➡️ Next

Continue to [understanding-cors.md](understanding-cors.md) to see a different browser-enforced
security mechanism: controlling which other sites can make requests to your application at all.
