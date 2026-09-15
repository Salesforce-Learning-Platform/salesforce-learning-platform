# 🍪 Secure Cookie Attributes

## Three Attributes, Three Different Protections

[CSRF Protection](../csrf-and-clickjacking/csrf-protection.md), the previous module, already
mentioned `SameSite` as a defense. This file covers that attribute — and its two essential
companions, `Secure` and `HttpOnly` — in full depth, since a session cookie's actual configuration
is genuinely central to a web application's real security posture.

## `Secure`: HTTPS Only

```http
Set-Cookie: sessionId=abc123; Secure
```

A cookie marked `Secure` is **only ever sent over an encrypted HTTPS connection** — never over
plain HTTP, protecting it from a network-level eavesdropper (a man-in-the-middle attacker on public
WiFi, for instance) who could otherwise simply read it directly off the wire.

## `HttpOnly`: Invisible to JavaScript

```http
Set-Cookie: sessionId=abc123; HttpOnly
```

```js
// With HttpOnly set, this NEVER includes the sessionId cookie -
// it's simply invisible to JavaScript entirely
console.log(document.cookie);
```

`HttpOnly` prevents client-side JavaScript from ever reading a cookie's value at all — this is a
direct, critical defense against exactly the cookie-theft scenario covered in
[what-is-xss.md](../cross-site-scripting-xss/what-is-xss.md): even if an XSS vulnerability somehow
lets an attacker inject and execute JavaScript, an `HttpOnly` session cookie remains completely
inaccessible to that injected code.

## `SameSite`: Controlling Cross-Site Inclusion

```
Strict → the cookie is NEVER sent on a cross-site request - the
         strongest protection, directly preventing the CSRF
         mechanism from understanding-csrf.md

Lax    → sent on the cookie's own site, AND when a user navigates
         TO that site from an external link - a practical, common
         default balancing security and usability

None   → sent on BOTH same-site and cross-site requests - must be
         combined with Secure; needed for genuine third-party use
         cases (an embedded widget, cross-site analytics)
```

`SameSite=Strict` is exactly the browser-enforced mechanism that makes
[understanding-csrf.md](../csrf-and-clickjacking/understanding-csrf.md)'s forged-form attack fail
before it even reaches the server — the browser itself refuses to attach the cookie to a
cross-site request at all, regardless of anything the server does.

## A Real, Complete Session Cookie Configuration

```http
Set-Cookie: sessionId=abc123; Expires=Thu, 21 Oct 2026 07:28:00 GMT; Secure; HttpOnly; SameSite=Strict
```

This is the practical, recommended configuration for a genuine authentication/session cookie —
`Secure` protects it in transit, `HttpOnly` protects it from XSS-based theft, and `SameSite=Strict`
protects it from CSRF — three genuinely independent protections, each closing a different specific
gap, working together.

## Setting This in Express

```js
res.cookie("sessionId", sessionValue, {
  httpOnly: true,
  secure: true,
  sameSite: "strict",
  maxAge: 24 * 60 * 60 * 1000,   // 24 hours, in milliseconds
});
```

This is the practical, real Express API for setting these three attributes together — directly
applicable to the session-handling patterns already covered in
[Authentication and Authorization](../../backend/authentication-and-authorization/), earlier in
this repository's Backend domain.

## Common Mistakes

- Omitting `HttpOnly` on a session cookie, leaving it fully readable by any injected JavaScript if
  an XSS vulnerability is ever present.
- Using `SameSite=None` without a genuine cross-site use case actually requiring it, unnecessarily
  reopening the exact CSRF risk `Strict` or `Lax` would otherwise close.
- Forgetting `Secure`, allowing a session cookie to be sent over plain, unencrypted HTTP if the
  application is ever accidentally reached that way.

## ➡️ Next

Continue to [cookie-security.md](cookie-security.md) to see broader cookie-handling practices
beyond just these three core attributes.
