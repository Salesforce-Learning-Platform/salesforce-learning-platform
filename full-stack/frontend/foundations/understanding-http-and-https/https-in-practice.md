# HTTPS in Practice

## Recap

[http-https-and-tls.md](../how-the-internet-works/http-https-and-tls.md) explained what TLS
mechanically provides — encryption, integrity, and server authentication via a certificate. This
file covers what that means operationally for a team actually running a production web
application.

## Certificates: What They Actually Prove

A TLS certificate, issued by a trusted **Certificate Authority (CA)**, binds a public key to a
domain name and is used during the TLS handshake to let a client verify it's talking to the
genuine server for that domain — not an impostor performing a **man-in-the-middle** attack. A
certificate proves *domain control and identity of the connection endpoint*; it says nothing about
whether the application behind it is well-built or trustworthy in any broader sense.

Certificates expire (commonly after 90 days to a year, depending on the issuer) and must be
renewed before expiry — an expired certificate causes browsers to show a hard warning and refuse
the connection by default, which is why automated renewal (widely done today via the ACME protocol
and services like Let's Encrypt) is standard practice rather than manual tracking.

## Enforcing HTTPS

Simply having HTTPS available isn't the same as requiring it. Production systems typically:

- **Redirect all HTTP requests to HTTPS** (a `301` redirect from `http://` to `https://`), so a
  user who types a bare domain or clicks an old `http://` link is upgraded automatically.
- **Set `Strict-Transport-Security` (HSTS)**, a response header instructing the browser to *never*
  attempt a plain HTTP connection to this domain again for a specified duration — closing the
  window where even the very first request could be intercepted before the redirect happens.

## Mixed Content

A page loaded over HTTPS that then loads a subresource (an image, script, or stylesheet) over
plain HTTP creates **mixed content** — undermining the page's own security guarantee, since that
one insecure resource can be tampered with in transit. Modern browsers block "active" mixed
content (scripts, stylesheets) outright and warn on "passive" mixed content (images). The fix is
always to serve every resource, including third-party ones, over HTTPS.

## Common Mistakes

- Treating "the site has a padlock" as proof the whole page is secure, when a mixed-content
  resource or an outdated TLS configuration can still leave real gaps.
- Letting a certificate lapse due to manual renewal being forgotten — a fully preventable outage
  given automated renewal is standard and widely available.
- Assuming HTTPS alone protects an API from unauthorized use. HTTPS protects data *in transit*; it
  does nothing about authentication or authorization of *who* is allowed to call the API — those
  remain separate concerns (see
  [state-management-across-the-boundary.md](../client-server-architecture/state-management-across-the-boundary.md)).

## Salesforce Relevance

Outbound Apex callouts via Named Credentials fail at the TLS handshake if the remote server's
certificate is expired, self-signed, or doesn't match the requested hostname — before any
application-level error is even possible. This is why "callout failing with no useful error
message" is often a certificate problem on the *remote* system, not a bug in the calling Apex.

## Module Summary

Across this module: HTTP methods carry precise safety/idempotency semantics that affect what's
safe to retry (see
[http-methods-in-depth.md](http-methods-in-depth.md)); status codes tell you, by their first
digit alone, which side of a request is responsible for an outcome (see
[http-status-codes-in-depth.md](http-status-codes-in-depth.md)); headers carry the metadata that
drives content negotiation, caching, authentication, and CORS (see
[http-headers-in-depth.md](http-headers-in-depth.md)); and HTTPS in production is a matter of
enforcement (redirects, HSTS) and certificate hygiene, not just having a certificate installed at
all.
