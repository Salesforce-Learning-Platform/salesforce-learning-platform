# ⚖️ Load Balancing

## The Mechanism Behind Horizontal Scaling

[Reverse Proxy Concepts](../../../production-systems/nginx-and-reverse-proxies/reverse-proxy-concepts.md),
already covered in this repository's Production Systems domain, introduced load balancing at a
high level — Nginx distributing requests across multiple backend instances. This file covers the
*specific algorithms* a load balancer actually uses to decide, and grounds them in real, verified
detail.

## Round Robin: the Simplest Algorithm

```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A   (cycles back to the start)
```

Round robin distributes requests in strict rotation, regardless of each server's current actual
load. It genuinely works best, per widely-referenced guidance, when servers have *equal* processing
power and requests are *stateless* — a strong fit for something like the URL Shortener's redirect
handling, where every request is essentially interchangeable.

## Least Connections: Adapting to Real, Current Load

```
Server A: 12 active connections
Server B: 3 active connections   ← the NEXT request goes HERE
Server C: 8 active connections
```

Least connections routes each new request to whichever server currently has the *fewest* active
connections — genuinely better suited than round robin when requests take meaningfully varying
amounts of time to process, or when server capacities aren't perfectly uniform, since it adapts to
*actual*, real-time load rather than blindly rotating.

## IP Hash: Consistent Routing for the Same Client

```
hash(client_IP) % number_of_servers → the SAME client's requests
  CONSISTENTLY route to the SAME server, every time
```

This is the right choice specifically when **session persistence** genuinely matters — a stateful
application where a user's session data lives on one particular server benefits from that user's
requests always landing on that same server, rather than being routed unpredictably across the
whole pool.

## Choosing the Right Algorithm for a Given System

```
STATELESS, uniform requests (the URL Shortener's redirects)
  → Round Robin, often genuinely sufficient

VARIABLE request duration, uneven server capacity
  → Least Connections

STATEFUL sessions needing consistency
  → IP Hash
```

This is a genuinely practical decision framework — the "best" algorithm depends entirely on the
actual characteristics of the specific system's traffic, not a single universally-correct choice.

## Health Checks: Removing Failed Servers Automatically

```
A load balancer PERIODICALLY checks each backend server's health
(directly the SAME health-check concept from Application
Monitoring, already covered in this repository's Production
Systems domain) - a server FAILING its health check is
AUTOMATICALLY removed from rotation, until it recovers.
```

This directly connects load balancing to reliability — a load balancer isn't merely a traffic
distributor; it's also the first line of defense against routing real traffic to a genuinely
unhealthy server, directly previewing
[reliability-and-availability.md](../advanced-distributed-systems/reliability-and-availability.md),
covered later in this domain.

## Horizontal Scaling, Made Genuinely Possible

```
Without a load balancer: adding MORE servers doesn't help, since
  clients would need to know WHICH specific server to talk to.

With a load balancer: clients talk to ONE stable address, and the
  load balancer transparently DISTRIBUTES traffic across however
  MANY servers actually exist behind it - directly enabling the
  horizontal scaling already introduced in Virtual Machines,
  earlier in this repository's Production Systems domain.
```

## Common Mistakes

- Using IP hash for a genuinely stateless system, adding unnecessary rigidity with no real
  session-persistence benefit to justify it.
- Configuring no health checks at all, letting a load balancer continue routing real traffic to a
  server that's already genuinely failing.
- Choosing round robin for a system with genuinely uneven request processing times, leaving some
  servers overloaded while others sit comparatively idle.

## ➡️ Next

Continue to [api-gateway-pattern.md](api-gateway-pattern.md) to see a related, but genuinely
distinct, pattern for managing traffic entering a microservices architecture.
