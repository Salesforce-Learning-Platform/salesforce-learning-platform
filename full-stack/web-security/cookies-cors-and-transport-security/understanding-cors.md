# 🌐 Understanding CORS

## The Same-Origin Policy: the Browser's Default, Restrictive Rule

Browsers enforce a **same-origin policy** by default: JavaScript running on one origin (defined by
its scheme + domain + port — `https://myapp.com`) cannot read responses from a *different* origin
(`https://api.otherapp.com`) via `fetch()` or `XMLHttpRequest`, unless that other origin explicitly
allows it. This is a genuinely important default — without it, any malicious site's JavaScript could
freely read data from any other site a victim happened to be logged into.

## CORS: an Explicit, Server-Controlled Relaxation

```http
Access-Control-Allow-Origin: https://myapp.com
```

**CORS (Cross-Origin Resource Sharing)** is the HTTP-header-based mechanism a server uses to
explicitly *opt in* to allowing specific cross-origin requests — the same-origin policy remains the
browser's default, and CORS headers are how a server deliberately, narrowly relaxes it for
legitimate cases (a separate API domain serving a frontend hosted elsewhere, for instance).

## Simple Requests vs. Preflighted Requests

```
SIMPLE requests (GET/HEAD/POST with only "safe" headers and
content types): the browser sends the request DIRECTLY, and
simply checks the Access-Control-Allow-Origin response header
before letting JavaScript read the response.

PREFLIGHTED requests (PUT/DELETE/PATCH, custom headers, or
non-simple content types like JSON): the browser sends an OPTIONS
request FIRST, asking permission, BEFORE ever sending the real
request.
```

```http
OPTIONS /users HTTP/1.1
Origin: https://myapp.com
Access-Control-Request-Method: DELETE
Access-Control-Request-Headers: content-type

HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://myapp.com
Access-Control-Allow-Methods: DELETE, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

This preflight mechanism directly matters for anyone debugging an API — a request that works fine
from a tool like `curl` but fails from browser JavaScript with no obvious error is very often a
missing or misconfigured preflight response, not a problem with the actual request itself.

## `Access-Control-Allow-Credentials`: Cookies Across Origins

```
Sending COOKIES on a cross-origin request requires TWO things
together:
  1. The client explicitly opts in: fetch(url, {credentials: "include"})
  2. The SERVER explicitly allows it:
     Access-Control-Allow-Credentials: true
```

This directly builds on [secure-cookie-attributes.md](secure-cookie-attributes.md)'s `SameSite`
coverage — CORS and `SameSite` are two genuinely separate, complementary mechanisms both governing
whether a cookie actually crosses an origin boundary, and both need to permit it for a credentialed
cross-origin request to actually succeed.

## Why CORS Is Enforced by the Browser, Not the Server

```
CORS headers are a REQUEST to the browser - the ACTUAL server
still processes and responds to the request either way. CORS
protects the BROWSER from letting malicious JavaScript READ a
response it shouldn't - it does NOT prevent the SERVER from
receiving the request in the first place.
```

This is a genuinely important, often-misunderstood detail: CORS is not a server-side access-control
mechanism at all — it's [defense-in-depth](../the-security-mindset/security-principles.md) enforced
entirely on the *browser* side, protecting a victim's browser from having its own credentials
misused by another site's JavaScript, not a substitute for genuine server-side authorization.

## Common Mistakes

- Believing CORS headers alone provide real server-side access control — a non-browser client
  (`curl`, a mobile app, another server) is entirely unaffected by CORS and can call the API freely
  regardless of any CORS configuration.
- Debugging a failed cross-origin request purely on the client side, missing that the actual fix
  almost always belongs on the server's CORS response headers.
- Assuming a `credentials: "include"` fetch call will work without the server also explicitly
  setting `Access-Control-Allow-Credentials: true`.

## ➡️ Next

Continue to [cors-misconfigurations.md](cors-misconfigurations.md) to see the specific, common
mistakes that turn CORS from a protection into a real vulnerability.
