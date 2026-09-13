# CDNs, Caching, and Performance

## Intuition

If every request for a popular site had to travel all the way to one origin server on the other
side of the world, and be recomputed from scratch every time, the web would feel far slower than
it does. Two ideas fix most of this: **cache the answer close to the person asking**, and **don't
recompute or refetch what hasn't changed**.

## Caching

**Caching** is storing a copy of a response so a future, identical (or equivalent) request can be
satisfied without repeating the full round trip described in
[what-happens-when-you-enter-a-url.md](what-happens-when-you-enter-a-url.md). Caching happens at
multiple layers simultaneously:

| Layer | What it caches |
|---|---|
| DNS resolvers (OS, router, ISP) | Domain-name-to-IP-address answers, per their TTL |
| Browser | Full HTTP responses (HTML, CSS, JS, images), per `Cache-Control` headers |
| CDN / edge cache | Copies of origin server responses, served from locations near the requester |
| Application / database | Computed query results or rendered fragments, to avoid repeating expensive work |

An HTTP response controls its own cacheability via headers such as `Cache-Control`
(`max-age=3600`, `no-store`, `public`/`private`) and validators like `ETag` — which let a client
ask "has this changed since I last saw it?" and get back a cheap `304 Not Modified` instead of the
full payload again if it hasn't.

## CDNs (Content Delivery Networks)

A **CDN** is a geographically distributed network of servers ("edge" or "PoP" — Point of Presence
— servers) that cache and serve copies of an origin server's content from a location physically
closer to each requester, rather than every request traveling all the way to one origin.

```text
Without a CDN:
  User (Sydney) ─────────────────────────▶ Origin server (Virginia, USA)
                     long round trip

With a CDN:
  User (Sydney) ──▶ Edge server (Sydney, cached copy) ──╮
                                                          ├─▶ (only on cache miss)
  User (Tokyo)  ──▶ Edge server (Tokyo, cached copy)  ──╯       Origin server (Virginia)
```

Benefits, beyond raw distance:

- **Lower latency** for static and cacheable content, since fewer network hops and shorter
  physical distance are involved.
- **Reduced origin load**, since repeated requests for the same content are absorbed at the edge.
- **Improved resilience**, since a spike in traffic (or even a partial origin outage) can often
  still be served from cached edge copies.

### CDN vs. Origin Server

| | Origin Server | CDN (Edge Server) |
|---|---|---|
| Role | The authoritative source of the content/application | A distributed cache in front of the origin |
| Location | Wherever the application is actually hosted | Many points of presence worldwide |
| Serves | Everything, including dynamic/uncacheable responses | Cacheable content; forwards ("proxies") to origin on a cache miss |
| Content freshness | Always current by definition | Can be briefly stale until cache expiry or explicit invalidation |

A cache miss or an intentionally uncacheable request (e.g., a personalized API response) still
travels through to the origin — the CDN is a shortcut for the parts of the traffic that *can* be
shared across users, not a full replacement for the origin.

## Latency, Bandwidth, and Throughput — Three Different Things

These three terms are routinely used interchangeably in casual conversation, but they measure
different properties of a network path, and conflating them leads to real misdiagnoses (e.g.,
buying more bandwidth to fix a problem that is actually latency).

| Term | What it measures | Analogy |
|---|---|---|
| **Latency** | Time for a single unit of data (or a round trip) to travel from source to destination | How long it takes one truck to complete the drive |
| **Bandwidth** | The maximum theoretical data-transfer capacity of a link, per unit time | How many lanes the highway has |
| **Throughput** | The actual, achieved rate of data transfer, which can be lower than bandwidth due to congestion, protocol overhead, or latency | How many trucks actually get through per hour, in practice |

A high-bandwidth connection with high latency (a classic case: satellite internet) can still feel
sluggish for interactive use, because every round trip (DNS lookup, TCP handshake, TLS handshake,
each HTTP request) pays the latency cost regardless of how much raw capacity is available. This is
precisely why the handshake overhead discussed in
[what-happens-when-you-enter-a-url.md](what-happens-when-you-enter-a-url.md) matters — reducing
the *number of round trips* often improves perceived performance more than adding bandwidth does.

## Reliability, Availability, and Common Failure Points

**Reliability** is whether a system consistently behaves correctly; **availability** is whether
it's up and reachable at all, usually expressed as a percentage of uptime (e.g., "99.9%
availability"). A system can be perfectly reliable while unavailable (correctly refusing
connections during planned maintenance) or available but unreliable (up, but returning wrong or
inconsistent data).

Given everything covered in this module, an "I can't reach the site" report can genuinely originate
at any of these points, and distinguishing them is the core practical skill this module builds
toward:

| Symptom | Likely layer | What to check |
|---|---|---|
| `DNS_PROBE_FINISHED_NXDOMAIN` / "server not found" | DNS | Is the domain registered? Are DNS records correct and propagated? |
| Connection times out with no response at all | Network / routing / firewall | Is the destination reachable (`ping`, `traceroute`)? Is a firewall blocking the port? |
| `ERR_CONNECTION_REFUSED` | Server, but nothing listening on that port | Is the service actually running and bound to the expected port? |
| Certificate warning / `ERR_CERT_*` | TLS | Is the certificate valid, unexpired, and for the right domain? |
| Connects, but very slow | Latency, bandwidth, or an overloaded origin | Where's the round-trip time? Is a CDN/cache in front of it? Is the origin under load? |
| Connects fast, but wrong/stale content | Caching | Is a CDN or browser cache serving an old version? Check `Cache-Control`/`ETag` and invalidate if needed |
| `404`/`500` and similar | Application, not network | DNS, TCP, and TLS all already succeeded — this is now an application-logic problem |

## Salesforce Relevance

- Experience Cloud sites are commonly fronted by a CDN; after publishing changes, a stale cached
  copy at the edge is a frequent, non-code explanation for "I don't see my update yet."
- Apex callout timeouts and intermittent failures are often latency or availability issues in the
  remote system or the network path, not bugs in the calling Apex code — the troubleshooting table
  above applies directly.
- Governor limits on callout time in Apex are, in effect, a hard ceiling on how much
  latency-plus-processing time a single external call is allowed to consume.

## Next

Continue to
[knowledge-check-and-further-reading.md](knowledge-check-and-further-reading.md) to consolidate
the module's most commonly confused concepts, test your understanding, and find primary-source
references for further study.
