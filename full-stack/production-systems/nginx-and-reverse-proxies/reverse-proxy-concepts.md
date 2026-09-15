# 🔀 What a Reverse Proxy Does

## The Missing Piece From the Last Module

[https-configuration.md](../domains-dns-and-ssl/https-configuration.md), in the previous module,
already showed an Nginx configuration block handling HTTPS and forwarding requests to a backend
service — without fully explaining *why* that forwarding step exists at all. This file covers
exactly that: what a reverse proxy is, and the real problems it solves.

## Forward Proxy vs. Reverse Proxy — the Direction Matters

```
FORWARD proxy: sits in front of CLIENTS, hiding who's making a
  request (a corporate network's outbound proxy, a VPN)

REVERSE proxy: sits in front of SERVERS, hiding what's actually
  handling a request - the CLIENT only ever talks to the proxy,
  never directly to the real backend
```

This directional distinction is the source of frequent confusion — a **reverse** proxy protects and
manages access to servers, which is the role Nginx plays in a typical web deployment.

## The Core Job: Intercept, Forward, Return

```
1. A client sends a request to myapp.com
2. Nginx (the reverse proxy) RECEIVES it first
3. Nginx forwards the request to the REAL backend server
   (e.g. a Node.js process running on localhost:3000)
4. The backend responds to Nginx
5. Nginx returns that response to the CLIENT
```

From the client's perspective, it only ever interacts with Nginx — the actual application server
handling the request is never directly exposed to the outside world at all.

## Why Not Just Expose the Backend Directly?

```
Without a reverse proxy: the Node.js/Express backend itself would
  need to handle HTTPS termination, static file serving, load
  balancing, and be directly exposed to the public internet

With a reverse proxy: the backend focuses PURELY on application
  logic, running on a private port - Nginx handles everything
  else in front of it
```

This is a genuine separation of concerns: application code (already covered throughout this
repository's Backend domain) shouldn't need to also implement HTTPS termination, load balancing, or
static file serving — a reverse proxy is purpose-built infrastructure for exactly those concerns,
leaving the backend free to focus only on its actual job.

## Load Balancing — One Reverse Proxy, Multiple Backends

```
Client requests → Nginx → distributes across MULTIPLE backend
                            instances (app-server-1, app-server-2,
                            app-server-3)
```

Beyond a single backend, a reverse proxy can distribute incoming requests across *multiple*
identical backend instances — directly enabling horizontal scaling (running more copies of the same
application to handle more traffic) without the client ever needing to know how many actual backend
instances exist behind the proxy.

## Security: the Backend Is Never Directly Reachable

```
The Node.js process listens ONLY on localhost:3000 (or an
internal Docker network, per container-networking.md) - it is
NEVER published directly to the public internet.

ONLY Nginx (on ports 80/443) is actually publicly reachable.
```

This directly extends the expose-vs-publish distinction from
[container-networking.md](../docker-and-containerization/container-networking.md): the reverse
proxy is deliberately the *only* publicly-published entry point, while the actual application
servers behind it stay privately reachable only by the proxy itself — a meaningfully smaller,
more controlled public attack surface.

## Common Mistakes

- Directly exposing a backend application server to the public internet alongside the reverse proxy,
  defeating the security benefit of routing everything through one controlled entry point.
- Confusing a forward proxy with a reverse proxy — they solve genuinely different problems, despite
  sharing the word "proxy."
- Assuming a reverse proxy is only useful at large scale — even a single-backend deployment benefits
  from HTTPS termination and static file serving being handled outside the application code.

## ➡️ Next

Continue to [introduction-to-nginx.md](introduction-to-nginx.md) to see the specific, widely-used
reverse proxy software this module covers hands-on.
