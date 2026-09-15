# 🌐 Networking Basics for System Design

## Every Component Boundary Is a Network Boundary

[breaking-systems-into-components.md](../system-design-foundations/breaking-systems-into-components.md),
in the previous module, drew a diagram with arrows connecting services. Every one of those arrows
is a genuine network call — and understanding what actually happens along it is essential for
reasoning about a real system's latency and reliability.

## HTTP: the Application-Level Protocol

```
Every REST API call already covered throughout this repository's
Backend domain - GET/POST/PUT/DELETE requests, status codes,
headers - IS the application-level protocol most services
communicate over, at HLD scale exactly as much as within a single
backend.
```

This directly builds on [REST API Design](../../../backend/rest-api-design/), already covered in
depth in this repository's Backend domain — at the HLD level, the same HTTP fundamentals apply, just
now considered across potentially many services communicating with each other, not only a single
client talking to a single backend.

## TCP: the Reliable Transport Underneath

```
TCP (Transmission Control Protocol) provides:
  - GUARANTEED delivery (retransmits lost packets)
  - ORDERED delivery (data arrives in the order it was sent)
  - a CONNECTION handshake BEFORE any real data is sent
```

Every HTTP request rides on top of a TCP connection — this reliability doesn't come free: the
initial TCP handshake itself adds real, measurable latency before the actual HTTP request even
begins, which matters directly for the latency numbers already covered in
[capacity-estimation-basics.md](../system-design-foundations/capacity-estimation-basics.md), the
previous module.

## Why Latency Compounds Across Service Boundaries

```
A single user request touching THREE separate services, each
adding its OWN network round trip:

Client -> Service A -> Service B -> Service C -> (response travels
                                                    all the way back)

If EACH hop takes ~50ms, the TOTAL latency is AT LEAST 150ms -
BEFORE any actual processing time at each service is even counted.
```

This is a genuinely important, practical consequence of the component-boundary decisions made in
[breaking-systems-into-components.md](../system-design-foundations/breaking-systems-into-components.md) —
every additional service boundary a request must cross adds real, compounding network latency, which
is exactly why that file's "split only when genuinely justified" guidance matters at the network
level, not merely the organizational one.

## DNS: Turning a Service Name Into a Reachable Address

```
This directly extends How Domains Work, already covered in depth
in this repository's Production Systems domain - at HLD scale,
INTERNAL service-to-service communication often uses its OWN
internal DNS (or a service discovery mechanism) to resolve a
service NAME into its actual, current network address, which can
change as instances scale up and down.
```

This is a genuinely important nuance beyond the public-facing DNS already covered in
[How Domains Work](../../../production-systems/domains-dns-and-ssl/how-domains-work.md) — internal
service discovery solves the same fundamental problem (name → address), but needs to handle
addresses that change far more frequently than a public domain's DNS records typically do.

## Common Mistakes

- Designing an architecture with many, deeply chained service-to-service calls without accounting
  for the real, compounding latency each additional network hop adds.
- Treating network calls as though they were free, local function calls, rather than genuinely
  distinct operations that can fail independently and add real latency.
- Assuming an internal service's network address is stable and unchanging, rather than accounting
  for the genuine need for service discovery in a scaling, dynamic system.

## ➡️ Next

Continue to
[designing-rest-apis-at-scale.md](designing-rest-apis-at-scale.md) to see how these networking
fundamentals inform API design specifically at the system level.
