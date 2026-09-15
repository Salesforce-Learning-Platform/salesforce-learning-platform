# 🔒 HTTPS/TLS in Practice

## The Foundation Every Other Defense in This Module Assumes

Every defense covered so far in this module — `Secure` cookies, CORS's credential handling — has an
unstated precondition: the connection itself is actually encrypted. This file connects back to
[SSL/TLS Certificates](../../production-systems/domains-dns-and-ssl/ssl-and-tls.md), earlier in
this repository's Production Systems domain, specifically from the security-practitioner's
perspective: *why* this transport-layer protection is genuinely load-bearing for everything else.

## Why `Secure` Cookies Depend Entirely on HTTPS Actually Being Used

```
The Secure attribute (per secure-cookie-attributes.md) tells the
BROWSER never to send a cookie over plain HTTP.

But this protection means NOTHING if the application itself is
still REACHABLE over plain HTTP at all - an attacker could simply
strip HTTPS entirely (a "downgrade attack") and capture
credentials submitted over the resulting unencrypted connection.
```

This is exactly why [https-configuration.md](../../production-systems/domains-dns-and-ssl/https-configuration.md)'s
HTTP-to-HTTPS redirect matters so much from a security perspective, not merely a convenience one —
without it, an application remains reachable over plain HTTP, and every cookie-security attribute
covered in this module offers meaningfully weaker real protection.

## HSTS: Preventing the Downgrade Attack Structurally

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

**HTTP Strict Transport Security (HSTS)** instructs the *browser itself* to never attempt a plain
HTTP connection to this domain again, for the specified duration — even if a user explicitly types
`http://` or clicks an old HTTP link, the browser automatically upgrades to HTTPS before ever
sending the request. This closes the downgrade-attack gap structurally, at the browser level,
rather than relying solely on a server-side redirect that a sufficiently active
man-in-the-middle could otherwise interfere with on that very first request.

## Certificate Validation: What "the Padlock" Actually Confirms

```
A valid TLS certificate confirms:
  1. The connection is ENCRYPTED (an eavesdropper can't read it)
  2. The server genuinely CONTROLS the domain it claims to be
```

Per [ssl-and-tls.md](../../production-systems/domains-dns-and-ssl/ssl-and-tls.md), earlier in this
repository, this is exactly why domain validation (proving genuine ownership before a CA issues a
certificate) matters as much as the encryption itself — HTTPS without genuine certificate validation
would still be vulnerable to an attacker presenting their *own* valid certificate for a *different*,
attacker-controlled server.

## Mixed Content: a Real, Common HTTPS Pitfall

```html
<!-- On an HTTPS page, loading a script over plain HTTP -->
<script src="http://cdn.example.com/library.js"></script>
```

```
Browsers BLOCK (or at minimum warn loudly about) "mixed content" -
an HTTPS page loading a SUB-RESOURCE over plain HTTP - precisely
because that sub-resource could be tampered with in transit,
undermining the security of the entire page around it.
```

This is a genuinely common, practical issue worth checking for directly: every resource an HTTPS
page loads — scripts, stylesheets, images — should itself be loaded over HTTPS, or the page's own
security guarantee is only as strong as its weakest, plain-HTTP-loaded piece.

## Common Mistakes

- Configuring a valid TLS certificate but never actually redirecting or blocking plain HTTP access,
  leaving the application reachable — and therefore still exploitable — over an unencrypted
  connection.
- Omitting HSTS, relying solely on a server-side redirect that remains vulnerable on a user's very
  first, not-yet-upgraded connection attempt.
- Loading any page sub-resource over plain HTTP on an otherwise HTTPS page, undermining the page's
  overall security guarantee through mixed content.

## Module Summary

Across this module: **secure cookie attributes** — `Secure`, `HttpOnly`, and `SameSite` — each
close a genuinely distinct gap (transit interception, XSS-based theft, and CSRF, respectively),
verified against MDN's official documentation (see
[secure-cookie-attributes.md](secure-cookie-attributes.md)); **cookie security more broadly**
means storing only opaque identifiers, scoping cookies narrowly, and genuinely invalidating sessions
server-side, not just client-side (see [cookie-security.md](cookie-security.md)); **CORS**
deliberately relaxes the browser's default same-origin policy through explicit server headers,
enforced entirely browser-side rather than as server-side access control (see
[understanding-cors.md](understanding-cors.md)); **CORS misconfigurations** — especially blindly
reflecting the request's own `Origin` header — functionally defeat CORS's entire purpose, fixed
with an explicit, validated allowlist (see
[cors-misconfigurations.md](cors-misconfigurations.md)); and **HTTPS/TLS**, including HSTS and
avoiding mixed content, is the transport-layer foundation every other defense in this module
implicitly depends on actually being in place.
