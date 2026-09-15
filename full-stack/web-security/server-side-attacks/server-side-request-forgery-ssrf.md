# 🌐 Server-Side Request Forgery (SSRF)

## A Real Breach: Capital One, 2019

```
In 2019, Capital One suffered a breach exposing approximately 106
MILLION customer records - resulting in an $80 million regulatory
penalty and a $190 million class-action settlement. The root
cause: an SSRF vulnerability in a misconfigured Web Application
Firewall (WAF), which let the attacker make the SERVER itself
issue a request to AWS's internal metadata service
(169.254.169.254) and retrieve genuine, live IAM credentials.
```

This is one of the most significant, well-documented real-world consequences of SSRF — and it's
exactly the mechanism this file covers: tricking a *server* into making a request the application
never intended, to a destination the attacker chose.

## The Core Mechanism

```js
// VULNERABLE - fetches whatever URL the user supplies, server-side
app.post("/fetch-preview", async (req, res) => {
  const response = await fetch(req.body.url);
  res.send(await response.text());
});
```

```
A LEGITIMATE use: fetching a genuine external URL to generate a
link preview.

An ATTACKER-supplied URL instead:
http://169.254.169.254/latest/meta-data/iam/security-credentials/

The SERVER itself makes this request - not the attacker's own
browser - meaning it originates from INSIDE the application's own
trusted network, with access to internal resources an external
attacker could never reach directly.
```

This is the genuine severity of SSRF: the request comes from the *server*, carrying whatever
network-level trust and access that server itself has — including reaching internal-only services
(a cloud metadata endpoint, an internal admin panel, a database only reachable from inside the
private network) that are completely unreachable from the public internet.

## Why the Cloud Metadata Endpoint Specifically Matters

```
169.254.169.254 is a SPECIAL, non-routable address that cloud
providers (AWS, GCP, Azure) use to give a running server
TEMPORARY, LIVE credentials for whatever IAM role it's running
as - reachable ONLY from inside that specific server, never from
the outside internet.
```

This is exactly why SSRF is so severe in cloud environments specifically: a successful SSRF against
this endpoint doesn't just leak arbitrary data — it hands the attacker genuine, live cloud
credentials, often with permissions far broader than the vulnerable application itself actually
needed (directly the [least-privilege](../the-security-mindset/security-principles.md) violation
that made the Capital One breach so severe).

## Preventing SSRF: Allowlisting, Not Blocklisting

```js
const ALLOWED_HOSTS = ["images.trusted-partner.com", "cdn.trusted-partner.com"];

app.post("/fetch-preview", async (req, res) => {
  const url = new URL(req.body.url);
  if (!ALLOWED_HOSTS.includes(url.hostname)) {
    return res.status(403).json({ error: "Host not allowed" });
  }
  const response = await fetch(url.toString());
  res.send(await response.text());
});
```

Directly applying the same [structural-separation-over-blocklisting](../injection-attacks/preventing-injection-attacks.md)
principle already established for injection, earlier in this domain — an explicit **allowlist** of
genuinely trusted hosts is the correct fix, not attempting to *blocklist* dangerous-looking
addresses (which is both incomplete and bypassable, e.g. via a redirect chain or a DNS trick that
resolves to an internal address only after the initial check passes).

## Common Mistakes

- Attempting to blocklist "dangerous" hostnames or IP ranges instead of using an explicit allowlist
  of genuinely trusted destinations.
- Validating a URL's hostname once, without accounting for the actual fetch following a redirect to
  an entirely different, unvalidated destination.
- Underestimating SSRF's severity because "it's just fetching a URL," missing that the request
  originates from inside the server's own trusted network with access no external attacker could
  otherwise reach.

## ➡️ Next

Continue to [path-traversal.md](path-traversal.md) to see a related server-side attack targeting
the filesystem instead of the network.
