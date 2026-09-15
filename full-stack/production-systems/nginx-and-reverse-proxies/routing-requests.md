# 🚦 Routing Requests to Backend Services

## `location` Blocks: Routing by URL Path

```nginx
server {
    listen 80;
    server_name myapp.com;

    location /api/ {
        proxy_pass http://localhost:3000;
    }

    location /docs/ {
        proxy_pass http://localhost:4000;
    }
}
```

Each `location` block matches a specific URL path pattern and routes matching requests to a
different backend — a request for `myapp.com/api/orders` goes to the backend on port 3000, while
`myapp.com/docs/getting-started` goes to an entirely different backend on port 4000. This is a
concrete, working example of the routing pattern from
[introduction-to-nginx.md](introduction-to-nginx.md)'s nested configuration structure.

## Preserving Real Client Information: `proxy_set_header`

```nginx
location /api/ {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://localhost:3000;
}
```

Without these headers, the backend application would see every request as coming from Nginx itself
(`localhost`) — losing the real client's actual IP address and the original `Host` header entirely.
`X-Forwarded-For` specifically preserves the genuine originating client IP, which matters for
anything relying on it: rate limiting, geolocation, or audit logging.

## Why This Matters: A Backend Reading the "Wrong" IP

```js
// WITHOUT proper header forwarding, this always logs Nginx's
// own internal IP, not the real client's
app.use((req, res) => {
  console.log("Request from:", req.socket.remoteAddress); // WRONG behind a proxy
});

// WITH X-Forwarded-For properly set AND trusted by the backend:
app.set("trust proxy", true);   // Express-specific configuration
app.use((req, res) => {
  console.log("Request from:", req.ip);   // now correctly reads
                                            // X-Forwarded-For
});
```

This is a genuinely common, easy-to-miss bug: an application behind a reverse proxy needs to be
explicitly configured to trust and read the forwarded headers — otherwise, every log entry, every
rate-limit check, and every IP-based decision silently operates on the wrong address.

## Path Rewriting — Stripping a Prefix Before Forwarding

```nginx
location /api/ {
    proxy_pass http://localhost:3000/;   # the trailing slash here
                                           # strips "/api/" before
                                           # forwarding
}
```

A trailing slash on the `proxy_pass` target URL changes the actual behavior: a request to
`myapp.com/api/orders` gets forwarded to the backend as `/orders` (the `/api/` prefix stripped),
rather than `/api/orders` — genuinely useful when the backend itself has no concept of an `/api/`
prefix and expects plain, unprefixed routes.

## Routing to Multiple Backends: a Realistic Microservice Setup

```nginx
server {
    listen 443 ssl;
    server_name myapp.com;

    location /api/orders/ { proxy_pass http://orders-service:3001/; }
    location /api/users/  { proxy_pass http://users-service:3002/; }
    location /            { proxy_pass http://frontend:3000; }
}
```

This is a realistic shape for an application with multiple backend services (as touched on briefly
in this domain's earlier [multi-agent architecture](../../artificial-intelligence/multi-agent-architecture-concerns/managing-shared-state-between-services.md)
discussion, applied here to ordinary web services) — one Nginx instance, on one public domain, quietly
routing to several genuinely separate services behind the scenes, each unaware of the others.

## Common Mistakes

- Forgetting `proxy_set_header X-Forwarded-For`, causing every backend log entry and IP-based
  decision to silently reflect Nginx's own address rather than the real client's.
- Misunderstanding the trailing-slash behavior on `proxy_pass`, causing a URL prefix to be
  unexpectedly stripped (or unexpectedly kept) when forwarding to the backend.
- Forgetting to configure the backend framework itself (e.g. Express's `trust proxy` setting) to
  actually trust and use the forwarded headers Nginx sends.

## ➡️ Next

Continue to [serving-static-files.md](serving-static-files.md) to see the other major job a reverse
proxy commonly takes on: serving files directly, without involving the backend application at all.
