# HTTP, HTTPS, and TLS

## Intuition

TCP gets a reliable, ordered stream of bytes from one program to another. It has no opinion about
what those bytes *mean*. HTTP is the agreement about meaning — a request format ("give me this
page"), a response format ("here it is, and here's its status"), and a shared vocabulary
(methods, status codes, headers) that both a browser and a server understand.

## HTTP: Request/Response

**HTTP (HyperText Transfer Protocol)** — most recently formalized as HTTP semantics in
[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) — is a **stateless, request/response**
application-layer protocol. "Stateless" means each request is handled independently, with no
built-in memory of previous requests (which is exactly why applications need cookies, tokens, or
sessions to maintain any continuity between requests — a topic covered elsewhere in this
platform).

A request carries, at minimum:

- A **method** describing the intended action (`GET` retrieve, `POST` submit/create, `PUT`
  replace, `PATCH` partially update, `DELETE` remove).
- A **path** identifying the resource (`/products/42`).
- **Headers** — metadata such as `Host`, `Content-Type`, `Authorization`, `Accept`.
- Optionally, a **body** (for `POST`/`PUT`/`PATCH`), carrying the actual data being sent.

A response carries:

- A **status code** in one of five classes:

| Range | Class | Example |
|---|---|---|
| 1xx | Informational | `100 Continue` |
| 2xx | Success | `200 OK`, `201 Created` |
| 3xx | Redirection | `301 Moved Permanently`, `304 Not Modified` |
| 4xx | Client error | `404 Not Found`, `401 Unauthorized` |
| 5xx | Server error | `500 Internal Server Error`, `503 Service Unavailable` |

- **Headers** (`Content-Type`, `Set-Cookie`, caching directives).
- A **body** — the actual page, JSON payload, image, etc.

```text
GET /index.html HTTP/1.1
Host: example.com
Accept: text/html
                                    ──────────▶
                                                    HTTP/1.1 200 OK
                                                    Content-Type: text/html
                                                    Content-Length: 1256
                                                    <!doctype html>...
                                    ◀──────────
```

## HTTP vs. TCP — the Layering, Made Concrete

HTTP doesn't move bytes across the network itself; it defines *what the bytes mean* and hands the
actual transmission off to TCP underneath. Confusing the two is common because both are involved
in "loading a web page," but they solve entirely different problems.

| | TCP | HTTP |
|---|---|---|
| Layer | Transport | Application |
| Concerned with | Reliable, ordered delivery of bytes between two endpoints | The meaning of those bytes — methods, status codes, headers |
| Knows about URLs, methods, status codes? | No | Yes |
| Runs on top of | IP | TCP (traditionally; HTTP/3 runs on UDP-based QUIC) |

A useful way to internalize this: TCP is the reliable envelope-delivery service; HTTP is the
letter-writing convention (salutation, subject, body) used by two parties who trust that service
to actually deliver the envelope.

## HTTPS and TLS

**HTTPS** is HTTP layered on top of **TLS (Transport Layer Security)** — most current deployments
use **TLS 1.3** ([RFC 8446](https://www.rfc-editor.org/rfc/rfc8446)), the successor to the older
and now-deprecated SSL protocol (the term "SSL certificate" persists in casual usage even though
the underlying protocol in modern use is TLS).

TLS provides three guarantees that plain HTTP does not:

1. **Encryption** — data exchanged between client and server is unreadable to anyone intercepting
   the connection in transit (protects against eavesdropping on shared networks, ISPs, or anyone
   sitting between the two endpoints).
2. **Integrity** — any tampering with data in transit is detectable.
3. **Authentication** — the client can cryptographically verify it is actually talking to the
   server it intended to reach, via a **certificate** issued by a trusted **Certificate
   Authority (CA)**, rather than an impostor.

### Where TLS Fits Relative to TCP and HTTP

```text
Application data (HTTP request/response)
        ↓
TLS  — encrypts everything above this line, including the HTTP request itself
        ↓
TCP  — reliable, ordered byte delivery (three-way handshake happens first)
        ↓
IP   — addressing and routing
```

Establishing an HTTPS connection therefore involves two handshakes in sequence: first the TCP
three-way handshake (see
[tcp-ip-ports-and-routing.md](tcp-ip-ports-and-routing.md)), then a **TLS handshake** during which
the client and server agree on encryption algorithms, the server proves its identity via its
certificate, and both sides derive shared encryption keys — after which the actual HTTP request
finally travels, now encrypted. TLS 1.3 reduced this handshake to a single round trip in the
common case (down from two in TLS 1.2), which measurably improves the time before the first byte
of a page arrives.

### HTTP vs. HTTPS

| | HTTP | HTTPS |
|---|---|---|
| Default port | 80 | 443 |
| Encrypted? | No — readable by anyone on the network path | Yes, via TLS |
| Server identity verified? | No | Yes, via a certificate from a trusted CA |
| Modern browser treatment | Marked "Not Secure"; many features (geolocation, service workers, etc.) are disabled | Required for most modern web platform features |

Plain HTTP is not merely "less polished" than HTTPS — it offers no protection against an
on-path attacker reading or modifying traffic, including credentials submitted in a form. This is
why HTTPS is now the effective default for any production web application, and mandatory for
anything handling authentication, payments, or personal data.

## Common Mistakes

- **Thinking TLS/HTTPS "hides" that you visited a site from your ISP entirely.** TLS encrypts the
  content and most request details, but the destination server's IP address (and, absent
  additional protections, the domain name via TLS's SNI field or the earlier DNS query) is
  typically still visible to intermediate network operators.
- **Assuming HTTP/HTTPS and TCP are the same layer.** As shown above, HTTP is what your
  application logic reasons about; TCP (and TLS) operate beneath it and are usually invisible to
  application code entirely — the browser and OS handle them.
- **Treating "has a padlock icon" as "is trustworthy."** The padlock only confirms the connection
  is encrypted and the certificate is valid for that domain — it says nothing about whether the
  site itself is legitimate or safe.

## Salesforce Relevance

Every Salesforce org is served exclusively over HTTPS, and outbound integrations (Named
Credentials, HTTP callouts from Apex) require valid TLS on the remote endpoint by default — a
callout to a server with an expired or misconfigured certificate fails at the TLS handshake stage,
before any Apex code or HTTP logic runs.

## Next

Continue to
[what-happens-when-you-enter-a-url.md](what-happens-when-you-enter-a-url.md) to walk through the
complete sequence — DNS, TCP, TLS, HTTP, and rendering — from start to finish.
