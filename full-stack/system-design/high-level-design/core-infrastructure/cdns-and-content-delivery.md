# 🌍 CDNs and Content Delivery

## Caching, Extended Across Geography

[caching-strategies.md](caching-strategies.md) covered caching at the application level — one
cache, close to one backend. A **CDN (Content Delivery Network)** applies the exact same core
idea — serve frequently-requested content from somewhere faster than the original source — but
distributed *geographically*, across the entire globe.

## The Problem: Physical Distance Is Real, Unavoidable Latency

```
A user in TOKYO requesting an image stored on a server in VIRGINIA
travels a GENUINELY long physical distance - directly the SAME
"round trip within same datacenter" latency number from Capacity
Estimation Basics, earlier in this domain, but multiplied
MASSIVELY by real, physical geographic distance.
```

No amount of server-side optimization changes the actual physical distance data has to travel — a
CDN solves this not by making the origin server faster, but by moving a *copy* of the content
physically closer to the user.

## Points of Presence and Edge Servers

```
A CDN maintains PoPs (Points of Presence) - physical server
locations distributed WORLDWIDE, each holding EDGE SERVERS that
cache content close to nearby users.

User request → routed to the NEAREST PoP (via Anycast routing,
using the internet's own BGP) → served from that EDGE server's
cache, WITHOUT ever reaching the actual origin server, if already
cached there.
```

This is directly the same cache-aside pattern already covered in
[caching-strategies.md](caching-strategies.md) — an edge server checks its own cache first, and
only fetches from the real origin server on a genuine miss, caching the result for subsequent
nearby users afterward.

## What CDNs Are Genuinely Best Suited For

```
STATIC, rarely-changing content: images, videos, CSS/JS bundles,
  downloadable files - GENUINELY well-suited, since the same
  content is served identically to many users

DYNAMIC, per-user content (a personalized dashboard): LESS
  suited - though "dynamic acceleration" techniques exist for
  genuinely optimizing even this case
```

This directly extends the static-file-serving concepts from
[Serving Static Files](../../../production-systems/nginx-and-reverse-proxies/serving-static-files.md),
already covered in this repository's Production Systems domain — a CDN is, in a genuine sense, that
same static-file-serving idea, now distributed globally rather than served from one single Nginx
instance.

## The Real, Practical Payoff

```
WITHOUT a CDN: EVERY user, worldwide, makes a request that
  travels all the way to ONE origin server, regardless of their
  own actual location.

WITH a CDN: the VAST majority of requests are served from a
  NEARBY edge server - dramatically reducing both LATENCY (for
  users) and LOAD (on the origin server itself).
```

This second benefit — reduced load on the origin — matters genuinely as much as the latency
improvement: a CDN absorbing the bulk of static-content traffic means the origin server can be
provisioned for a meaningfully smaller fraction of total real traffic.

## Common Mistakes

- Using a CDN only for genuinely dynamic, per-user content where the caching benefit is minimal,
  while missing genuinely cacheable static assets that would benefit significantly.
- Setting an inappropriately long cache duration on content that changes more frequently than
  expected, serving stale content to users worldwide.
- Assuming a CDN eliminates the need for the origin server's own capacity planning entirely, when
  cache misses and genuinely dynamic requests still reach it directly.

## ➡️ Next

Continue to [load-balancing.md](load-balancing.md) to see how traffic that does reach the origin
gets distributed across multiple backend servers.
