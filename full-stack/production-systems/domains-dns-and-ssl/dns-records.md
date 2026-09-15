# 📋 DNS Record Types

## Each Record Type Answers a Different Question

[how-domains-work.md](how-domains-work.md) covered the *process* of DNS resolution. A DNS
**record** is the actual data being resolved — and different record types exist because a domain
needs to answer several genuinely different questions: "what IP address is this?", "where should
email go?", "who else is authorized to speak for this domain?"

## `A` and `AAAA` — Mapping a Name to an IP Address

```
A record:    myapp.com    →  203.0.113.42        (IPv4)
AAAA record: myapp.com    →  2001:db8::1          (IPv6)
```

These are the most fundamental record types — a direct mapping from a domain name to the actual
numeric address a browser connects to. Every domain needs at least one of these (`A` or `AAAA`) to
be reachable at all.

## `CNAME` — Aliasing One Name to Another

```
CNAME record: www.myapp.com  →  myapp.com
```

A `CNAME` record doesn't point to an IP address directly — it points to *another domain name*,
which is then resolved in turn. This is genuinely useful for keeping multiple names in sync: if
`myapp.com`'s underlying IP address ever changes, `www.myapp.com` (aliased via `CNAME`) automatically
follows, without needing its own separate update.

```
IMPORTANT: a CNAME's target must eventually resolve to a real A/
AAAA record - and a domain's ROOT (myapp.com, with no
subdomain) technically cannot use a CNAME record at all, per the
DNS specification - only a subdomain (www.myapp.com) can.
```

## `MX` — Where Email for This Domain Goes

```
MX record: myapp.com  →  10 mail.myapp.com
                          (priority: 10, mail server: mail.myapp.com)
```

An `MX` (Mail Exchange) record tells other mail servers where to actually deliver email addressed
to `@myapp.com` — genuinely separate infrastructure from whatever serves the actual website, which
is exactly why a domain can have its website hosted by one provider and its email handled entirely
by a different one (a common real-world setup).

## `TXT` — Arbitrary Text, Commonly Used for Verification

```
TXT record: myapp.com  →  "google-site-verification=abc123..."
TXT record: myapp.com  →  "v=spf1 include:_spf.google.com ~all"
```

A `TXT` record holds arbitrary text — in practice, most commonly used to *prove domain ownership*
(many services ask you to add a specific `TXT` record to verify you control a domain) or to
configure email authentication (SPF, DKIM records, which help prevent email spoofing). This is also
exactly the mechanism [ssl-and-tls.md](ssl-and-tls.md), next in this module, uses for one method of
certificate domain validation.

## `NS` — Delegating Authority for a Subdomain

```
NS record: staging.myapp.com  →  ns1.otherprovider.com
```

An `NS` record delegates authority over a specific subdomain to a different set of nameservers —
useful when, for instance, a `staging` subdomain's DNS needs to be managed by a completely separate
team or provider from the main domain's DNS.

## Putting Several Record Types Together

```
myapp.com          A      203.0.113.42
www.myapp.com      CNAME  myapp.com
api.myapp.com      A      203.0.113.99
myapp.com          MX     10 mail.myapp.com
myapp.com          TXT    "v=spf1 include:_spf.google.com ~all"
```

A real domain's DNS configuration is typically a *combination* of several record types working
together — the root domain and an API subdomain each pointing to their own server via `A` records,
`www` aliased via `CNAME`, and separate `MX`/`TXT` records handling email entirely independently.

## Common Mistakes

- Attempting to add a `CNAME` record at a domain's root (with no subdomain), which the DNS
  specification doesn't actually allow.
- Forgetting that email (`MX`) and website (`A`/`AAAA`) records are entirely independent — changing
  one has no effect on the other, and both need to be configured correctly for a domain to fully
  function.
- Removing a `TXT` record used for domain verification (or certificate issuance) after it's served
  its initial purpose, when some services periodically re-check it.

## ➡️ Next

Continue to [ssl-and-tls.md](ssl-and-tls.md) to see how a domain's traffic is actually secured, once
DNS correctly points it at the right server.
