# 🔐 Cookies, CORS, and Transport Security

## 📚 Overview

This module covers the browser-enforced security mechanisms underlying much of what earlier modules
in this domain assumed: secure cookie attributes closing the gaps left by transit interception, XSS,
and CSRF; CORS deliberately relaxing the browser's same-origin policy through explicit server
control; and HTTPS/TLS as the transport-layer foundation every other defense in this module
implicitly depends on.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Configure `Secure`, `HttpOnly`, and `SameSite` cookie attributes correctly, and explain what
  distinct gap each one closes.
- Apply broader cookie security practices: opaque identifiers, narrow scoping, and genuine
  server-side session invalidation.
- Explain how CORS relaxes the same-origin policy, and the difference between simple and
  preflighted requests.
- Identify and fix common CORS misconfigurations, especially blind origin reflection.
- Explain why HTTPS/TLS, including HSTS, is foundational to every cookie and CORS protection in
  this module.

## 📋 Prerequisites

- [CSRF and Clickjacking](../csrf-and-clickjacking/) — this module's `SameSite` coverage builds directly on the CSRF mechanism covered there.
- [Domains, DNS, and SSL](../../production-systems/domains-dns-and-ssl/) — this module's HTTPS/TLS file revisits that content from a security-practitioner's perspective.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [secure-cookie-attributes.md](secure-cookie-attributes.md) | `Secure`, `HttpOnly`, `SameSite` — what each one protects against |
| [cookie-security.md](cookie-security.md) | Opaque identifiers, scoping, expiration, and server-side session invalidation |
| [understanding-cors.md](understanding-cors.md) | Same-origin policy, simple vs. preflighted requests, credentialed CORS |
| [cors-misconfigurations.md](cors-misconfigurations.md) | The wildcard+credentials rejection, and the blind-origin-reflection trap |
| [https-and-tls.md](https-and-tls.md) | HSTS, certificate validation, and mixed content; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you configure session cookies, build an API consumed from a different origin, or
manage HTTPS for a real deployment — every file here is directly, practically applicable.

**Skim** if you exclusively use a framework or platform that handles cookie attributes and CORS
configuration automatically — the underlying reasoning still helps you recognize a misconfiguration
if one occurs.

## 🧠 Knowledge Check

<details>
<summary>Why is <code>Access-Control-Allow-Origin: *</code> combined with <code>Access-Control-Allow-Credentials: true</code> rejected by browsers, and why is dynamically reflecting the request's <code>Origin</code> header just as dangerous?</summary>

The explicit wildcard-plus-credentials combination is rejected by the browser itself, since it
would let any origin make fully authenticated requests. Reflecting the request's own `Origin` header
back unconditionally achieves the identical effect — it grants every origin credentialed access, one
at a time — while superficially looking like a properly scoped, specific-origin configuration.

</details>

<details>
<summary>Why does the <code>Secure</code> cookie attribute offer little real protection if an application is still reachable over plain HTTP at all?</summary>

`Secure` only controls whether the browser sends an existing cookie over HTTP — it doesn't prevent
the application itself from being reached over plain HTTP in the first place. An attacker could
still intercept an unencrypted connection (a downgrade attack) and capture credentials submitted
before HTTPS is ever engaged, which is exactly why an HTTP-to-HTTPS redirect and HSTS matter as much
as the cookie attribute itself.

</details>

## 📚 References

- [MDN - HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies) — official documentation for `Secure`, `HttpOnly`, and `SameSite`
- [MDN - Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) — official documentation for CORS mechanics and the credentials/wildcard restriction
- [MDN - Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security) — official documentation for HSTS syntax

## ➡️ Continue Your Learning Path

Continue to [Authentication Attacks](../authentication-attacks/) to see how session and token
mechanisms themselves can be attacked, beyond the cookie-transport concerns covered here.
