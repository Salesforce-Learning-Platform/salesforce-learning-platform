# 🛡️ CSRF in Single-Page Applications

## The Classic CSRF Attack, Briefly

A classic **Cross-Site Request Forgery (CSRF)** attack exploits the fact that browsers
automatically attach cookies to *every* request to a given domain — including one triggered by a
malicious page the user happens to have open in another tab. If an authentication cookie is
automatically sent along, an attacker's page can trigger a real, authenticated action (like
transferring funds) without the user ever intending it.

## Why localStorage Feels Like It Avoids This — and the Real Tradeoff

```js
// Storing the access token in localStorage:
localStorage.setItem("accessToken", token);

// The browser does NOT automatically attach this to any request —
// the application's own code must explicitly read it and attach it
fetch("/api/orders", {
  headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
});
```

Storing a token in `localStorage` instead of a cookie removes the classic CSRF vector entirely: the
browser never automatically sends `localStorage` data anywhere — only the application's own
JavaScript can read and attach it, meaning a malicious external page genuinely can't trigger an
authenticated request the way it could with an auto-sent cookie. The real tradeoff: `localStorage`
is readable by **any** JavaScript running on the page, making it more exposed to a cross-site
scripting (XSS) vulnerability than a properly-configured `HttpOnly` cookie would be — trading one
risk for a different one, not eliminating risk altogether.

## The Recommended Pattern: Cookie-to-Header

```js
// 1. Server sets the token in a cookie readable by JavaScript
//    (deliberately NOT HttpOnly) with SameSite protection
res.cookie("csrfToken", token, { httpOnly: false, sameSite: "strict", secure: true });
```

```js
// 2. Client reads the cookie's value and attaches it as a CUSTOM HEADER
fetch("/api/orders", {
  method: "POST",
  headers: { "X-CSRF-Token": getCookie("csrfToken") },
});
```

```js
// 3. Server verifies the header matches the cookie
if (req.headers["x-csrf-token"] !== req.cookies.csrfToken) {
  return res.status(403).json({ error: "CSRF validation failed" });
}
```

This **cookie-to-header** pattern is the current recommended approach specifically because a
request carrying a **custom header** is subject to the browser's same-origin policy — a malicious
external page genuinely cannot add a custom header to a cross-site request the way it can rely on
automatic cookie attachment. Combined with `SameSite=Strict`/`Lax` on the cookie itself (per
[sessions.md](../authentication-and-authorization/sessions.md)'s cookie security attributes), this
gives strong protection while still using cookies deliberately.

## The One Thing That Defeats All of This: XSS

Every mitigation covered in this file assumes the application has **no XSS vulnerability** — if an
attacker can run arbitrary JavaScript on the page at all, they can simply read `localStorage`
directly, or read the CSRF cookie and attach the matching header themselves, defeating every
CSRF-specific protection covered here. This is exactly why the platform's dedicated web security
content on injection and XSS prevention matters as a genuine prerequisite to real authentication
security, not a separate, unrelated concern.

## Common Mistakes

- Assuming `localStorage` storage alone makes an application immune to all related attacks — it
  removes the classic CSRF vector specifically, while genuinely increasing exposure to XSS.
- Implementing the cookie-to-header pattern without also setting `SameSite` on the cookie itself,
  losing a real, additional layer of the intended protection.
- Treating CSRF protection as sufficient on its own without also addressing XSS — an XSS
  vulnerability defeats essentially every CSRF mitigation covered in this file.

## Module Summary

Across this module: the **production auth flow** combines a short-lived JWT access token with a
longer-lived, server-tracked refresh token, taking the best of both prior approaches' tradeoffs
(see [the-production-auth-flow.md](the-production-auth-flow.md)); **refresh token rotation**, with
reuse detection invalidating an entire compromised token family, is what actually catches a stolen
refresh token in practice (see [refresh-token-rotation.md](refresh-token-rotation.md)); **Redis**'s
speed and built-in TTL expiration make it purpose-fit for this session/token storage (see
[storing-sessions-in-redis.md](storing-sessions-in-redis.md)); **logout from all devices** tracks
every active refresh token per user and invalidates them all at once, bounded by how short the
access token's own lifetime is (see
[logout-from-all-devices.md](logout-from-all-devices.md)); and **CSRF in SPAs** requires a
deliberate mitigation — the cookie-to-header pattern being the current recommended approach — that
remains entirely dependent on the application also being free of XSS vulnerabilities.
