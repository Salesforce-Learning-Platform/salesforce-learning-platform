# 🔧 Configuring HTTPS for a Real Deployment

## Putting Every Piece Together

This file combines everything from this module into one real, working setup: a domain
([how-domains-work.md](how-domains-work.md)) pointed at a server via DNS records
([dns-records.md](dns-records.md)), secured with a TLS certificate
([ssl-and-tls.md](ssl-and-tls.md)) — issued, installed, and automatically renewed.

## Step 1: Point the Domain at the Server

```
myapp.com    A    203.0.113.42     (the server's real, public IP)
```

Before any certificate can be issued or validated, DNS must already correctly point the domain at
the actual server — domain validation (per [ssl-and-tls.md](ssl-and-tls.md)) depends on this being
in place first, whether validation happens via `TXT` record or via a file served over HTTP.

## Step 2: Obtain a Certificate With Certbot

```bash
sudo apt install certbot python3-certbot-nginx

sudo certbot --nginx -d myapp.com -d www.myapp.com
```

Certbot, the most widely-used ACME client for Let's Encrypt, handles the entire flow covered in
[ssl-and-tls.md](ssl-and-tls.md) automatically: requesting a certificate, completing domain
validation, and — with the `--nginx` plugin specifically — even editing the web server's own
configuration to actually use the new certificate.

## Step 3: The Resulting Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name myapp.com www.myapp.com;

    ssl_certificate     /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
    }
}

server {
    listen 80;
    server_name myapp.com www.myapp.com;
    return 301 https://$host$request_uri;   # redirect HTTP -> HTTPS
}
```

This is exactly the kind of configuration
[Nginx and Reverse Proxies](../nginx-and-reverse-proxies/), later in this domain, covers in full
depth — for now, the key detail is the second `server` block: any request arriving over plain HTTP
(port 80) is redirected to HTTPS, ensuring the encrypted connection is genuinely the *only* way
visitors actually reach the site.

## Step 4: Automatic Renewal

```bash
sudo certbot renew --dry-run   # test that renewal WOULD succeed,
                                 # without actually renewing yet

# Certbot's installer typically sets up a scheduled task
# (a systemd timer or cron job) automatically, running twice daily,
# that only actually renews certificates within 30 days of expiry
```

Directly per [ssl-and-tls.md](ssl-and-tls.md)'s "certificates expire and must be renewed" warning,
Certbot's own installation typically configures this renewal check automatically — but explicitly
verifying it with `--dry-run` is a genuinely worthwhile, cheap step to confirm the automation will
actually work before a real certificate is ever at risk of expiring unattended.

## Verifying the Full Setup

```
1. Visit http://myapp.com  → should REDIRECT to https://myapp.com
2. Visit https://myapp.com → should load with NO browser security
   warning, and a valid padlock icon
3. Check the certificate's details in the browser - confirm it
   covers BOTH myapp.com AND www.myapp.com, and check its
   expiration date
```

This is the practical, end-to-end verification that every piece — DNS, certificate issuance, web
server configuration, and the HTTP-to-HTTPS redirect — is genuinely working together correctly,
not just individually configured.

## Common Mistakes

- Running Certbot before DNS actually points the domain at the server, causing domain validation to
  fail since the CA can't verify ownership against a server that isn't actually reachable there yet.
- Forgetting the HTTP-to-HTTPS redirect, leaving the plain, unencrypted HTTP version of the site
  still fully accessible alongside the secured HTTPS version.
- Never testing renewal with `--dry-run`, only discovering an automation failure when the real
  certificate has already expired and visitors are seeing security warnings.

## Module Summary

Across this module: **domains** translate memorable names into IP addresses through DNS resolution,
with TTL and propagation delay as genuinely practical considerations for any change (see
[how-domains-work.md](how-domains-work.md)); **DNS record types** — `A`/`AAAA` for IP mapping,
`CNAME` for aliasing, `MX` for email routing, `TXT` for verification, `NS` for delegation — each
answer a distinct question about where a domain's various services actually live (see
[dns-records.md](dns-records.md)); **TLS certificates** cryptographically prove domain ownership and
encrypt traffic, issued by a trusted CA after domain validation, with Let's Encrypt's ACME protocol
making free, automated issuance and short-lived (90-day) certificates the modern standard (see
[ssl-and-tls.md](ssl-and-tls.md)); and **a real HTTPS deployment** combines all of this — correct DNS
pointing at the server, Certbot-issued and auto-renewing certificates, a web server configured to use
them, and an HTTP-to-HTTPS redirect ensuring encryption is the only way visitors actually reach the
site.
