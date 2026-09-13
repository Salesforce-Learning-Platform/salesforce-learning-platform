# What Happens When You Enter a URL?

## Purpose

This is the synthesis file. Every concept from the previous six files shows up here, in the order
it actually happens. If you can narrate this sequence accurately — including *why* each step
exists — you've internalized the module.

We'll trace `https://www.example.com/products/42` from keystroke to rendered page.

## The Complete Flow

```text
1. Parse the URL
   scheme=https  host=www.example.com  path=/products/42

2. DNS resolution
   Browser/OS cache → Router cache → ISP recursive resolver
   → Root nameserver → .com TLD nameserver → example.com authoritative nameserver
   Result: www.example.com → 93.184.216.34
   (see dns-and-domain-resolution.md)

3. Establish a TCP connection to 93.184.216.34 on port 443
   Three-way handshake: SYN → SYN-ACK → ACK
   (see tcp-ip-ports-and-routing.md)

4. TLS handshake (because the scheme is https)
   Client and server negotiate encryption, server presents its certificate,
   client verifies it against a trusted Certificate Authority, both derive shared keys
   (see http-https-and-tls.md)

5. Browser sends the HTTP request — now encrypted by TLS
   GET /products/42 HTTP/1.1
   Host: www.example.com

6. Request travels across the network
   Local network → router → ISP → backbone/other ISPs → destination network → server
   Routed hop-by-hop based on the destination IP address
   (see clients-servers-and-local-networks.md, tcp-ip-ports-and-routing.md)

7. Server processes the request and sends an HTTP response
   HTTP/1.1 200 OK
   Content-Type: text/html
   <!doctype html>...

8. Response travels back through the same kind of path (not necessarily the same route)

9. Browser receives the response and begins rendering
   Parses HTML → builds the DOM → fetches linked resources (CSS, JS, images —
   each of which repeats a version of steps 2–8) → paints pixels to the screen

10. Page is interactive
```

```text
 Browser                DNS                Network              Server
    │                    │                    │                    │
    │── resolve host ───▶│                    │                    │
    │◀── IP address ─────│                    │                    │
    │                                         │                    │
    │── TCP SYN ─────────────────────────────▶│───────────────────▶│
    │◀── TCP SYN-ACK ─────────────────────────│◀────────────────────
    │── TCP ACK ─────────────────────────────▶│───────────────────▶│
    │                                         │                    │
    │── TLS handshake (ClientHello...) ──────▶│───────────────────▶│
    │◀── TLS handshake (certificate, keys) ───│◀────────────────────
    │                                         │                    │
    │── HTTP GET /products/42 (encrypted) ───▶│───────────────────▶│
    │◀── HTTP 200 OK + HTML body (encrypted) ─│◀────────────────────
    │                                         │                    │
    │── render: parse HTML, fetch CSS/JS/images (repeats steps above per resource)
    │
    ▼
 Page painted, then interactive
```

## Step-by-Step Notes

**Step 1 — Parsing the URL.** The browser splits the URL into its scheme (`https`, which
determines the default port and whether TLS is required), host (`www.example.com`, used for DNS
resolution and later for the `Host` header — necessary because one IP address can host many
different domains), and path (`/products/42`, which the server's application logic interprets).

**Step 2 — DNS.** Every layer of caching described in
[dns-and-domain-resolution.md](dns-and-domain-resolution.md) is checked before a fresh recursive
lookup is performed; on a warm cache, this step can be effectively instant. On a cold cache, it's
often the single largest fixed cost before any application data moves at all.

**Steps 3–4 — Connection setup.** These are pure overhead paid *before* any application data is
exchanged: one round trip for TCP, then (with TLS 1.3) typically one more round trip for TLS. On a
connection with, say, 80ms of round-trip latency, that's already roughly 160ms spent before the
HTTP request is even sent — which is exactly why connection reuse (`keep-alive`) and protocol
improvements like TLS 1.3's reduced handshake and HTTP/2's connection multiplexing matter for
real-world performance.

**Steps 5–8 — The actual HTTP exchange.** This is the only part of the whole sequence that
web-application code (server-side frameworks, Apex controllers, Node/Express routes, LWC
`@wire` calls) directly participates in. Everything before it is infrastructure the application
code never touches, and everything after it (rendering) is the browser's job.

**Steps 9–10 — Rendering.** The browser parses the returned HTML into a DOM tree, and — critically
— any `<link>`, `<script>`, or `<img>` tag referencing another resource triggers its own
independent version of steps 2–8 (often many in parallel, or resolved instantly if the resource is
already cached). A page with 40 external resources means potentially 40 more DNS lookups and
connection setups, mitigated in practice by DNS caching, connection reuse to the same host, and
CDNs (see [cdns-caching-and-performance.md](cdns-caching-and-performance.md)). Deep rendering
mechanics (DOM construction, CSSOM, layout, paint) are covered in this platform's HTML and browser
rendering module — this file's scope stops at the network boundary.

## Frontend Relevance

Understanding this sequence directly explains real, observable behavior:

- Why the **very first request** to a new host is often noticeably slower than subsequent ones
  (DNS + TCP + TLS overhead paid once, then amortized).
- Why **`<link rel="preconnect">`** and DNS-prefetch hints exist — they let the browser start
  steps 2–4 for a known third-party host *before* the resource is actually needed.
- Why a `404` or `500` response still means DNS, TCP, and TLS all succeeded — those steps are
  independent of whether the application logic found the resource or handled the request
  correctly. A connection-level failure (DNS error, connection refused, TLS certificate error)
  looks and behaves completely differently from an application-level error, and knowing the
  sequence tells you which layer to debug first.

## Salesforce Relevance

An Apex HTTP callout via a **Named Credential** goes through exactly this sequence from the org's
servers as the client: DNS resolution of the target host, TCP connection, TLS handshake (Salesforce
requires a valid certificate on the remote endpoint), then the actual HTTP request/response your
Apex code sees. A callout that times out or throws an `UnknownHostException`-style error is failing
at step 2 or 3 of this sequence — before any of your Apex logic or the remote system's application
code has run at all. This is why callout troubleshooting starts with "can this even be resolved
and reached," not "what does my code do with the response."

## Next

Continue to [cdns-caching-and-performance.md](cdns-caching-and-performance.md) to see how much of
this sequence can be shortened or skipped entirely through caching and edge infrastructure.
