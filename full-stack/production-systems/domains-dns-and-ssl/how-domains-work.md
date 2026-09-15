# 🌐 How Domains Work

## From an IP Address to a Memorable Name

Every server on the internet — including the containers and infrastructure covered in
[Docker and Containerization](../docker-and-containerization/) and
[DevOps Foundations](../devops-foundations/) — is actually reachable by a numeric **IP address**
(like `203.0.113.42`). A **domain name** (`myapp.com`) exists purely for human convenience: the
Domain Name System (DNS) is the mechanism that translates a memorable name into the actual IP
address a browser needs to connect to.

## The Domain Hierarchy

```
myapp.com
  │    │
  │    └── TOP-LEVEL DOMAIN (TLD): .com, .org, .io, .dev, etc.
  │        - managed by an organization accredited by ICANN
  │
  └── SECOND-LEVEL DOMAIN: "myapp" - the part an organization
      actually registers and owns

api.myapp.com  ← a SUBDOMAIN of myapp.com, commonly used to
                  separate different services (an API, a
                  marketing site, a docs site) under one domain
```

Registering a domain means claiming the second-level portion (`myapp`) under a specific top-level
domain (`.com`) through a domain **registrar** — this registration is what gives an organization the
authority to control where that domain actually points.

## The DNS Resolution Process, Step by Step

```
1. Browser asks: "What's the IP address for myapp.com?"
2. A DNS RESOLVER (often run by an ISP or a public service like
   1.1.1.1) checks its cache first
3. If not cached, the resolver queries a chain of DNS SERVERS -
   root servers, then the .com TLD servers, then myapp.com's own
   AUTHORITATIVE nameservers
4. The authoritative nameserver returns the actual IP address
5. The browser connects DIRECTLY to that IP address
```

This entire lookup process typically happens in milliseconds and is cached at multiple levels along
the way — which is exactly why a DNS change (like pointing a domain at a new server) doesn't take
effect instantly everywhere; it has to **propagate** as various caches expire and refresh.

## DNS Propagation and TTL

```
TTL (Time To Live) → how long a DNS record's answer should be
  CACHED before a resolver is required to ask again

A LOW TTL (e.g. 300 seconds) → changes propagate quickly, but
  every resolver re-queries more often (more DNS traffic)

A HIGH TTL (e.g. 86400 seconds = 24 hours) → less DNS traffic, but
  a change takes MUCH longer to be visible everywhere
```

A genuinely practical, real-world implication: before making a significant DNS change (like
migrating to a new server), deliberately lowering the TTL in advance means the eventual cutover
propagates faster — a detail experienced teams plan for ahead of time, not something to discover
mid-migration.

## Nameservers: Who's Actually Authoritative

```
A domain's NAMESERVERS (set at the registrar) determine which
DNS provider actually controls that domain's records - often the
registrar itself, or a dedicated DNS provider (Cloudflare, AWS
Route 53) for more advanced DNS management features.
```

This is a genuinely important distinction: registering a domain (who legally owns it) and managing
its DNS records (where it actually points) are related but separate responsibilities — a domain can
be registered with one company while its actual DNS is managed entirely by a different provider.

## Common Mistakes

- Expecting a DNS change to take effect instantly everywhere, without accounting for caching and
  TTL-driven propagation delay.
- Confusing domain *registration* with DNS *management* — they're related but genuinely separate
  responsibilities, sometimes handled by different providers entirely.
- Setting an unnecessarily long TTL on a record that's expected to change soon, making a future
  migration take much longer to propagate than necessary.

## ➡️ Next

Continue to [dns-records.md](dns-records.md) to see the specific record types that actually define
what a domain points to.
