# 📁 Serving Static Files

## Why Not Let the Application Serve Its Own Static Files?

```
An Express/Node.js backend CAN serve static files (images, CSS,
compiled JavaScript bundles) itself — but doing so means every
static file request still goes through the ENTIRE application
runtime, for work that's genuinely just "read a file, send it."
```

Nginx, written specifically for this kind of high-throughput, low-overhead file serving, handles
static content dramatically more efficiently than routing every image or CSS file request through an
application server's full request-handling pipeline — freeing the backend to spend its resources
purely on genuine application logic.

## The `root` Directive

```nginx
server {
    root /var/www/myapp/public;

    location / {
        index index.html;
    }
}
```

`root` tells Nginx where to look for files on disk — Nginx appends the request's URL path to this
root directory. A request for `myapp.com/logo.png` looks for the file at
`/var/www/myapp/public/logo.png`; `index index.html` specifies which file to serve by default when
a request ends in a slash (like `myapp.com/`).

## A Dedicated `location` Block for Static Assets

```nginx
server {
    root /var/www/myapp/public;

    location /static/ {
        # requests here are served DIRECTLY from disk, never
        # touching the backend application at all
    }

    location /api/ {
        proxy_pass http://localhost:3000;
    }
}
```

This is the complete picture, combining
[routing-requests.md](routing-requests.md)'s proxying with this file's static serving in one
configuration: requests under `/static/` are served directly from the filesystem, while requests
under `/api/` are proxied to the real backend — one Nginx instance cleanly handling both genuinely
different kinds of request in the same server block.

## Caching Static Assets Aggressively

```nginx
location /static/ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

Static assets — especially ones with a content hash in their filename (`app.a3f92c.js`, a common
build-tool convention) — genuinely never change once built, making them ideal candidates for
long, aggressive browser caching. This directly reduces both server load and page-load time for
repeat visitors, since the browser simply reuses its own cached copy instead of re-requesting the
file.

## Serving a Single-Page Application's `index.html` as a Fallback

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

For a client-side-routed single-page application, a direct URL like `myapp.com/dashboard/settings`
doesn't correspond to a real file on disk — `try_files` handles this by falling back to serving
`index.html` for any path that doesn't match a real file, letting the frontend's own client-side
router (already covered in this repository's Frontend domain) take over from there.

## Common Mistakes

- Routing every static asset request through the backend application server, adding unnecessary
  overhead for work Nginx handles far more efficiently.
- Applying long-lived caching to a file whose content can actually change without its filename also
  changing, causing users to see a stale cached version indefinitely.
- Forgetting the `try_files ... /index.html` fallback for a single-page application, causing a
  direct link to a client-side route to return a 404 instead of correctly loading the app.

## Module Summary

Across this module: **a reverse proxy** intercepts client requests and forwards them to a real
backend server, keeping the backend itself never directly exposed to the public internet — enabling
load balancing and a cleaner separation of concerns (see
[reverse-proxy-concepts.md](reverse-proxy-concepts.md)); **Nginx** is the widely-used software
implementing this, with a nested `http`/`server`/`location` configuration structure, validated with
`nginx -t` and applied gracefully with `reload` rather than `restart` (see
[introduction-to-nginx.md](introduction-to-nginx.md)); **routing requests** uses `location` blocks
and `proxy_pass` to direct different URL paths to different backend services, with
`proxy_set_header` preserving the real client's IP and host information the backend needs (see
[routing-requests.md](routing-requests.md)); and **serving static files** directly through Nginx's
`root`/`index`/`try_files` directives — rather than routing them through the application server —
is dramatically more efficient, with aggressive caching and single-page-application fallback
routing as genuinely practical, real-world refinements.
