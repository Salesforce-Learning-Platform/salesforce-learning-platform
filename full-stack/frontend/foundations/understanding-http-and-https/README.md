# Understanding HTTP and HTTPS

## Purpose

[http-https-and-tls.md](../how-the-internet-works/http-https-and-tls.md) explained HTTP and HTTPS
at the network-layering level — how they relate to TCP and TLS. This module is the practitioner's
view: the actual vocabulary you use every day building or debugging web applications — HTTP
methods, the full status-code taxonomy, and the headers that control caching, content
negotiation, and authentication.

## Learning Objectives

- Choose the correct HTTP method for a given operation, and explain the difference between safe,
  idempotent, and neither.
- Read an HTTP status code and correctly identify which side (client or server) is responsible for
  the outcome it describes.
- Categorize HTTP headers by purpose and explain what the most common ones actually do.
- Explain, precisely, what HTTPS adds to HTTP and why a valid certificate is not optional for
  production systems.

## Prerequisites

[http-https-and-tls.md](../how-the-internet-works/http-https-and-tls.md).

## Files in This Module

| File | Covers |
|---|---|
| [http-methods-in-depth.md](http-methods-in-depth.md) | GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS — semantics, safety, idempotency |
| [http-status-codes-in-depth.md](http-status-codes-in-depth.md) | The full status-code taxonomy and how to reason about which one to return or expect |
| [http-headers-in-depth.md](http-headers-in-depth.md) | Request/response headers grouped by purpose: content, caching, auth, CORS |
| [https-in-practice.md](https-in-practice.md) | What a production team actually needs to get right about certificates and HTTPS enforcement |

## When to Deep-Dive vs. Skim

If you'll be designing or consuming APIs regularly, read
[http-methods-in-depth.md](http-methods-in-depth.md) and
[http-status-codes-in-depth.md](http-status-codes-in-depth.md) closely — the
safe/idempotent distinction and the 401-vs-403 distinction are two of the most common real-world
mistakes. If you're purely doing frontend UI work against an already-built API, you can skim
methods and status codes but should still read
[http-headers-in-depth.md](http-headers-in-depth.md) for the CORS section, since CORS errors are a
near-universal early frontend debugging experience.

## Quick Knowledge Check

<details>
<summary>Is it safe to automatically retry a failed POST request the same way you would a failed GET request?</summary>

No. GET is both safe and idempotent, so retrying it is harmless. POST is generally not idempotent
— resending it can create a duplicate (e.g., a duplicate order or comment) if the original request
actually succeeded but its response was lost. See
[http-methods-in-depth.md](http-methods-in-depth.md).

</details>

<details>
<summary>A user is logged in but sees an error trying to view another user's private data. Should that be a 401 or a 403?</summary>

403 Forbidden — the server knows exactly who they are (they're authenticated), and the answer is
still no. 401 Unauthorized means the server doesn't know who's asking at all. See
[http-status-codes-in-depth.md](http-status-codes-in-depth.md).

</details>

## References

- IETF, [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- MDN Web Docs, [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- MDN Web Docs, [Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
- MDN Web Docs, [HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)

## Continue Your Learning Path

Next in the [Foundations sequence](../README.md):
[Preparing Your Machine](../preparing-your-machine/).
