# 🔒 SSL/TLS Certificates

## HTTP vs. HTTPS: What's Actually Different

```
HTTP:  data travels between browser and server in PLAIN TEXT -
       anyone intercepting the connection (a public WiFi network,
       an ISP) can read it directly

HTTPS: the SAME HTTP traffic, but ENCRYPTED using TLS (Transport
       Layer Security) - an interceptor sees only unreadable,
       encrypted bytes
```

"SSL" (Secure Sockets Layer) is the older, now-retired name for this technology; "TLS" is its
modern successor and the term actually in use today, though "SSL" persists informally (and in
product names like "SSL certificate") even when TLS is what's actually running underneath.

## What a Certificate Actually Proves

```
A TLS certificate cryptographically proves: "the entity presenting
this certificate genuinely controls THIS domain" - issued and
digitally signed by a trusted CERTIFICATE AUTHORITY (CA).
```

A certificate isn't just an encryption key — it's a verified, signed *claim of identity*. A
browser trusts a certificate specifically because it was issued by a CA the browser itself already
trusts (a pre-installed list of trusted CAs), and because the CA verified domain ownership before
issuing it.

## How Domain Validation Actually Works

```
Before issuing a certificate, a CA needs PROOF you control the
domain. Two common methods:

1. DNS validation: add a specific TXT record (per dns-records.md)
   the CA can look up
2. HTTP validation: place a specific file at a specific URL path
   on the domain, which the CA fetches to confirm
```

This directly connects back to [dns-records.md](dns-records.md)'s coverage of `TXT` records — DNS-
based domain validation is one of the most common ways a certificate authority confirms genuine
domain ownership before issuing a certificate for it.

## Let's Encrypt: Free, Automated Certificates

```
Let's Encrypt is a widely-used, FREE certificate authority using
the ACME protocol to automate the ENTIRE process:

1. An ACME client (e.g. Certbot) requests a certificate
2. Let's Encrypt issues a CHALLENGE (a DNS record to add, or a
   file to host)
3. The client completes the challenge
4. Let's Encrypt VALIDATES it (from multiple network vantage
   points, to prevent interception) and issues the certificate
```

This automation is a genuinely significant, relatively recent shift in how HTTPS is deployed — it
used to require manually purchasing a certificate from a commercial CA and manually installing it;
Let's Encrypt and the ACME protocol turned this into a fully scriptable, automatable process.

## Certificates Expire — and Must Be Renewed

```
Let's Encrypt certificates are valid for 90 DAYS - deliberately
SHORT, specifically to encourage AUTOMATED renewal rather than
manual, easily-forgotten processes.

A properly configured ACME client (Certbot) re-runs the SAME
validation process automatically, well before expiration.
```

This is a genuinely important operational detail: an expired certificate causes browsers to show a
hard security warning to every visitor — automating renewal (rather than relying on someone
remembering to renew manually) is essential, not optional, for any real production deployment.

## Common Mistakes

- Treating certificate renewal as a manual, calendar-reminder task instead of a fully automated
  process — a missed manual renewal directly causes a production outage in the form of browser
  security warnings.
- Confusing "HTTPS is configured" with "the connection is fully secure" — a valid certificate
  proves domain identity and encrypts the connection, but doesn't protect against every possible
  application-level vulnerability.
- Assuming a certificate for `myapp.com` automatically covers `api.myapp.com` — a certificate must
  explicitly cover every subdomain it's meant to secure (or use a wildcard certificate that covers
  them all).

## ➡️ Next

Continue to [https-configuration.md](https-configuration.md) to see how a certificate like this
actually gets installed and configured on a real, running server.
