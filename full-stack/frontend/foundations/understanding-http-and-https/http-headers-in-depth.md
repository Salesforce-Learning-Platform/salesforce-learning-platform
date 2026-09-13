# HTTP Headers in Depth

## Intuition

If the method and path say *what* is being requested, headers say almost everything else about
*how* — format, identity, caching behavior, and cross-origin permissions. Headers are simple
`Name: Value` pairs, and both requests and responses carry them.

## Headers Grouped by Purpose

### Content

| Header | Direction | Purpose |
|---|---|---|
| `Content-Type` | Request & response | The media type of the body, e.g. `application/json`, `text/html` |
| `Content-Length` | Response | Size of the body in bytes |
| `Accept` | Request | What media types the client can handle in the response |

### Caching

| Header | Direction | Purpose |
|---|---|---|
| `Cache-Control` | Response (also request) | Directives like `max-age=3600`, `no-store`, `public`/`private` — controls whether and how long a response may be cached |
| `ETag` | Response | An opaque identifier for a specific version of a resource |
| `If-None-Match` | Request | Sent with a previously received `ETag`; server replies `304 Not Modified` if it still matches |

These directly implement the caching behavior introduced in
[cdns-caching-and-performance.md](../how-the-internet-works/cdns-caching-and-performance.md).

### Authentication and Identity

| Header | Direction | Purpose |
|---|---|---|
| `Authorization` | Request | Carries credentials, e.g. `Authorization: Bearer <token>` |
| `Cookie` | Request | Sends cookies previously set by the server |
| `Set-Cookie` | Response | Instructs the client to store a cookie |

### Cross-Origin (CORS)

| Header | Direction | Purpose |
|---|---|---|
| `Origin` | Request | The origin (scheme + host + port) the request is coming from |
| `Access-Control-Allow-Origin` | Response | Which origins the server permits to read this response from browser JavaScript |

CORS headers exist because browsers, by default, block a page's JavaScript from reading responses
from a different origin than the page itself — a security boundary called the **same-origin
policy**. `Access-Control-Allow-Origin` is the server explicitly opting a given origin back in.
This is a browser-enforced restriction on *reading* cross-origin responses from script — it does
not prevent the request from reaching the server, and it is not itself an authentication
mechanism.

## Request vs. Response Headers — Same Concept, Different Direction

Some headers only make sense in one direction (`Set-Cookie` only ever appears in responses,
`Accept` only in requests); others can appear in both with related meaning (`Cache-Control`).
There's no universal list — the same "carries metadata as name/value pairs" mechanism is reused
for whatever purpose each specific header is defined for.

## Reading Headers in Practice

Browser DevTools' Network tab shows the full set of request and response headers for any call —
this is the fastest way to confirm what's actually being sent or returned, rather than assuming
from application code alone. It's also the first place to check when debugging a caching issue
(is `Cache-Control` set the way you expect?) or a CORS error (is `Access-Control-Allow-Origin`
present and correct?).

## Common Mistakes

- Treating `Authorization` header presence as proof of a valid, verified identity — the server
  must still validate the credential; a header being sent proves nothing by itself.
- Assuming a CORS error means "the request failed." The request often *did* reach the server and
  get processed — the browser is specifically blocking the *page's script* from reading the
  response, which is why CORS errors are sometimes invisible in server-side logs even though the
  browser console shows one.
- Forgetting that `Cache-Control` on a response the *server* controls, while `If-None-Match` is
  something the *client* sends — confusing which side is responsible for setting which header.

## Next

Continue to [https-in-practice.md](https-in-practice.md) for what actually matters operationally
about running HTTPS in production.
