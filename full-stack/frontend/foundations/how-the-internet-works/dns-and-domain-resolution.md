# DNS and Domain Resolution

## Intuition

Remembering `142.250.premium.number.here` for every site you visit would be unworkable. DNS
exists so humans can type names like `salesforce.com` while computers still route traffic using
IP addresses underneath. DNS is often described as "the phonebook of the Internet" — you look up
a name, and it gives you back a number.

## Domain Names

A **domain name** (`example.com`, `mohitveer.netlify.app`) is a human-readable label registered
through a **domain registrar** and organized hierarchically, read right to left:

```text
   www  .  example  .  com
    │        │         │
    │        │         └── Top-Level Domain (TLD)
    │        └── Second-level domain (the registered name)
    └── Subdomain / host label
```

- The **TLD** (`.com`, `.org`, `.dev`, country codes like `.in`) is managed by a registry under
  ICANN oversight.
- The **second-level domain** (`example`) is the name an organization registers.
- A **subdomain** (`www`, `api`, `mail`) is a further subdivision the domain owner controls freely
  — this is exactly what a Salesforce "My Domain" (`yourcompany.my.salesforce.com`) or an
  Experience Cloud custom domain is.

## Domain Name vs. IP Address

A domain name and an IP address are not the same kind of thing, even though one resolves to the
other:

| | Domain Name | IP Address |
|---|---|---|
| Audience | Humans | Machines/routing |
| Stability | Can stay the same indefinitely | Can change (server migration, load balancer, DNS-based failover) |
| Who assigns it | You, via a registrar | The network / hosting provider |
| What actually routes traffic | Nothing — it's just a label | This is what routers use |

This is precisely why DNS is needed: the browser (and every router along the way) needs an IP
address to actually deliver anything; the domain name is purely a lookup key that gets translated
before any packet is sent.

## Nameservers and the Resolution Hierarchy

DNS is a distributed, hierarchical database — no single server holds every answer. A lookup for
`www.example.com` walks down this hierarchy:

1. **Recursive resolver** — usually run by your ISP or a public service (e.g., a well-known
   public resolver), this is the server your device asks first. It does the legwork of walking the
   hierarchy on your behalf and caches the result for other users.
2. **Root nameservers** — know only which server is authoritative for each TLD (`.com`, `.org`,
   etc.). There are 13 logical root server addresses, operated by multiple organizations, and
   heavily replicated worldwide.
3. **TLD nameservers** — know which nameservers are authoritative for each domain registered under
   that TLD (e.g., who to ask about `example.com`).
4. **Authoritative nameservers** — the servers the domain owner has configured (often through
   their DNS host/registrar) that hold the actual DNS records for `example.com` and return the
   final answer.

```text
Browser/OS
   │  "what's the IP for www.example.com?"
   ▼
Recursive Resolver (ISP or public resolver)
   │
   ├─▶ Root nameserver        → "ask the .com TLD servers"
   ├─▶ .com TLD nameserver    → "ask example.com's nameservers"
   └─▶ example.com authoritative nameserver → "it's 93.184.216.34"
   │
   ▼
Answer cached and returned to the browser
```

In practice, most of this hierarchy is skipped on repeat lookups because of **caching** at every
level (your OS, your router, your ISP's resolver) — each answer is stored for a duration set by
its **TTL (Time To Live)**, which is why DNS changes can take time to "propagate": every cache
holding the old answer has to expire before everyone sees the new one.

## DNS Record Types Relevant to Web Applications

| Record | Purpose |
|---|---|
| **A** | Maps a name directly to an IPv4 address |
| **AAAA** | Maps a name directly to an IPv6 address |
| **CNAME** | Maps a name to *another name* (an alias), which is then resolved further. Commonly used to point a custom domain at a vendor's infrastructure — this is how a Salesforce custom domain or Experience Cloud site, or a Netlify/Vercel custom domain, is typically wired up. |
| **MX** | Specifies which mail servers accept email for the domain |
| **TXT** | Arbitrary text, widely used for domain ownership verification and email anti-spoofing policies (SPF, DKIM, DMARC) |
| **NS** | Declares which nameservers are authoritative for the domain |

A concrete, realistic example: to serve a site at `app.example.com` from a third-party platform,
you typically add a **CNAME** record pointing `app.example.com` at a hostname the vendor gives you
(e.g. `example-app.vendor-platform.net`), rather than an A record — because the vendor's
underlying IP addresses may change, but the hostname they control does not.

## Common Mistakes

- **Confusing DNS with HTTP.** DNS only answers "what IP address does this name point to?" It
  never carries the actual page content — that's HTTP's job, which happens *after* DNS resolution
  completes. See [http-https-and-tls.md](http-https-and-tls.md).
- **Expecting DNS changes to take effect instantly.** Because of caching and TTLs, a change to a
  DNS record can take anywhere from minutes to (rarely) days to be visible everywhere, depending on
  the TTL set on the old record.
- **Treating a domain name as a permanent, unique identifier for a server.** The same domain can
  resolve to different IPs over time, or to different IPs for different users (common with CDNs
  and geographically distributed infrastructure — see
  [cdns-caching-and-performance.md](cdns-caching-and-performance.md)).

## Next

Continue to [tcp-ip-ports-and-routing.md](tcp-ip-ports-and-routing.md) to see what happens once an
IP address is known: how data actually gets carried across the network to reach it.
