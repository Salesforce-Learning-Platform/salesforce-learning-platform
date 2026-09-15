# 🌟 Nginx and Reverse Proxies

## 📚 Overview

[Domains, DNS, and SSL](../domains-dns-and-ssl/) got traffic securely to a server; this module
covers what actually handles that traffic once it arrives. A reverse proxy — Nginx, the widely-used
software this module covers hands-on — sits in front of an application, routing requests to the
right backend service, serving static files efficiently, and keeping the real application server
never directly exposed to the public internet.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain what a reverse proxy does and why it's the only publicly-exposed entry point in a typical
  deployment.
- Configure Nginx's `http`/`server`/`location` structure, validating and reloading changes safely.
- Route different URL paths to different backend services with `proxy_pass`, preserving real client
  information with `proxy_set_header`.
- Serve static files directly through Nginx, with appropriate caching and single-page-application
  fallback routing.

## 📋 Prerequisites

- [Domains, DNS, and SSL](../domains-dns-and-ssl/) — this module's examples build directly on the HTTPS configuration covered there.
- [Docker and Containerization](../docker-and-containerization/) — the container networking concepts (expose vs. publish) this module applies to reverse proxy architecture.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [reverse-proxy-concepts.md](reverse-proxy-concepts.md) | Forward vs. reverse proxy, load balancing, and why the backend stays hidden |
| [introduction-to-nginx.md](introduction-to-nginx.md) | Installing Nginx, its configuration structure, and safe reload workflow |
| [routing-requests.md](routing-requests.md) | `location`/`proxy_pass`, preserving client IPs, path rewriting, multi-service routing |
| [serving-static-files.md](serving-static-files.md) | `root`/`index`/`try_files`, caching, and SPA fallback routing; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're deploying any application that needs HTTPS termination, multiple backend
services, or efficient static file serving — this is genuinely hands-on, immediately applicable
infrastructure knowledge.

**Skim** if you're working entirely within a managed platform that provisions this layer
automatically — the underlying concepts (why a reverse proxy exists, what it's actually doing) are
still worth understanding even if you're not configuring Nginx directly.

## 🧠 Knowledge Check

<details>
<summary>Why should an application's backend server never be directly, publicly exposed alongside the reverse proxy?</summary>

Routing every request through one controlled entry point (the reverse proxy) means the actual
application server can stay on a private port or internal network, meaningfully reducing the
public attack surface. If the backend is also directly exposed, an attacker can bypass the proxy's
controls (HTTPS termination, routing rules) entirely and reach the application directly.

</details>

<details>
<summary>Why does a backend application need explicit configuration (like Express's <code>trust proxy</code> setting) to correctly read a client's real IP address when running behind Nginx?</summary>

Without `proxy_set_header X-Forwarded-For` on the Nginx side and the backend trusting that header,
every request appears to originate from Nginx's own address, not the real client. Both the reverse
proxy's header forwarding and the backend's explicit trust of that header are needed together for
IP-based logic (rate limiting, logging, geolocation) to work correctly.

</details>

## 📚 References

- [NGINX - Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) — official documentation for `proxy_pass` and `proxy_set_header`
- [NGINX - Serving Static Content](https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/) — official documentation for `root`, `index`, and static file serving

## ➡️ Continue Your Learning Path

Continue to [Cloud Infrastructure Fundamentals](../cloud-infrastructure/) to see where a server
running Nginx and an application actually lives in a real cloud deployment.
