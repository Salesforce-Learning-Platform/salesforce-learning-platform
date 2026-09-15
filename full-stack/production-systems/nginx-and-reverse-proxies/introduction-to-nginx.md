# 🌟 Introduction to Nginx

## A Widely-Used, Proven Reverse Proxy

**Nginx** (pronounced "engine-x") is one of the most widely-deployed web servers and reverse
proxies in production use today — the actual software behind the concepts covered in
[reverse-proxy-concepts.md](reverse-proxy-concepts.md), and the same tool already used in
[https-configuration.md](../domains-dns-and-ssl/https-configuration.md)'s Certbot example from the
previous module.

## Installing and Running Nginx

```bash
# On a typical Linux server
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx   # start automatically on boot
```

```dockerfile
# Or, containerized (per Docker and Containerization, earlier in this domain)
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

Nginx runs equally well installed directly on a server or as its own container — the containerized
approach directly applies [Writing Dockerfiles](../docker-and-containerization/writing-dockerfiles.md)'s
patterns from earlier in this domain to Nginx itself.

## The Configuration File Structure

```nginx
http {
    server {
        listen 80;
        server_name myapp.com;

        location / {
            proxy_pass http://localhost:3000;
        }
    }
}
```

```
http block    → the OUTERMOST block, containing settings shared
                across every server Nginx handles
server block  → ONE virtual host — a specific domain/port
                combination Nginx listens for
location block → a specific URL PATH pattern within that server,
                with its own handling rules
```

This nested structure — `http` → `server` → `location` — is the foundational shape every Nginx
configuration follows, and it's exactly what
[routing-requests.md](routing-requests.md), next in this module, builds on to handle multiple
different backend services from one Nginx instance.

## Multiple `server` Blocks — Hosting Several Domains

```nginx
server {
    listen 80;
    server_name myapp.com;
    location / { proxy_pass http://localhost:3000; }
}

server {
    listen 80;
    server_name docs.myapp.com;
    location / { proxy_pass http://localhost:4000; }
}
```

A single Nginx instance can handle multiple, entirely separate `server_name` values simultaneously —
each routed to a genuinely different backend — directly matching the subdomain concept from
[how-domains-work.md](../domains-dns-and-ssl/how-domains-work.md), earlier in this domain.

## Reloading Configuration Without Downtime

```bash
sudo nginx -t          # TEST the configuration for syntax errors
                        # BEFORE applying it
sudo systemctl reload nginx   # apply changes WITHOUT dropping
                               # existing connections
```

`nginx -t` is a genuinely important habit — validating a configuration file's syntax *before*
applying it catches a typo or mistake before it can take down a live, running proxy. `reload`
(rather than `restart`) applies configuration changes gracefully, without interrupting requests
already in progress.

## Common Mistakes

- Applying a configuration change with `restart` instead of `reload`, unnecessarily interrupting
  active, in-progress connections.
- Skipping `nginx -t` before applying a configuration change, risking a syntax error taking down a
  live, production reverse proxy.
- Forgetting that `server_name` must match the actual domain in the incoming request's `Host`
  header — a request for the wrong domain won't route to the intended `server` block.

## ➡️ Next

Continue to [routing-requests.md](routing-requests.md) to see how Nginx routes different URL paths
to different backend services.
