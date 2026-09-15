# 🔒 Domains, DNS, and SSL

## 📚 Overview

A containerized application (per [Docker and Containerization](../docker-and-containerization/))
running on a server isn't yet reachable by a real, memorable web address, and isn't yet secure. This
module covers the two pieces that close that gap: DNS, which translates a domain name into the
server's actual IP address, and TLS/SSL, which encrypts and authenticates the connection once a
visitor gets there — ending with a complete, real HTTPS deployment.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain how DNS resolution works, and why changes propagate gradually rather than instantly.
- Choose the correct DNS record type (`A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS`) for a given need.
- Explain what a TLS certificate actually proves, and how Let's Encrypt automates issuance and
  renewal via the ACME protocol.
- Configure a complete, real HTTPS deployment: DNS pointing at a server, an issued certificate, and
  an HTTP-to-HTTPS redirect.

## 📋 Prerequisites

- [Docker and Containerization](../docker-and-containerization/) — this module assumes an application is already running on a real server, ready to be made reachable and secure.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [how-domains-work.md](how-domains-work.md) | The domain hierarchy, DNS resolution process, and TTL/propagation |
| [dns-records.md](dns-records.md) | `A`/`AAAA`, `CNAME`, `MX`, `TXT`, and `NS` records, each answering a different question |
| [ssl-and-tls.md](ssl-and-tls.md) | What a certificate proves, domain validation, and Let's Encrypt's ACME protocol |
| [https-configuration.md](https-configuration.md) | A complete, real deployment: Certbot, an Nginx config, and verification; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you'll be deploying and securing any real, publicly-reachable application — every
concept here is a genuine, hands-on prerequisite for a production launch.

**Skim** if you're working entirely within a managed platform that already handles DNS and HTTPS
automatically (many PaaS providers do) — the underlying concepts are still worth knowing, but you
won't need to configure them by hand.

## 🧠 Knowledge Check

<details>
<summary>Why doesn't a DNS change take effect instantly for every visitor?</summary>

DNS answers are cached at multiple levels (resolvers, ISPs, browsers) according to each record's
TTL (Time To Live). A change only becomes visible to a given cache once that cache's TTL expires and
it re-queries — which is why lowering a record's TTL in advance of a planned change helps the
eventual cutover propagate faster.

</details>

<details>
<summary>Why are Let's Encrypt certificates deliberately short-lived (90 days) instead of valid for years?</summary>

The short lifespan is a deliberate design choice specifically to encourage fully automated renewal
rather than an easily-forgotten manual process. A properly configured ACME client (like Certbot)
renews well before expiration automatically — an expired certificate causes a hard security warning
for every visitor, which automation is meant to make effectively impossible.

</details>

## 📚 References

- [Cloudflare - DNS Record Types](https://developers.cloudflare.com/dns/manage-dns-records/reference/dns-record-types/) — official documentation covering `A`, `AAAA`, `CNAME`, `MX`, `TXT`, and `NS` records
- [Let's Encrypt - How It Works](https://letsencrypt.org/how-it-works/) — the official explanation of the ACME protocol, domain validation, and certificate issuance

## ➡️ Continue Your Learning Path

Continue to [Nginx and Reverse Proxies](../nginx-and-reverse-proxies/) to see the web server
technology that actually terminates HTTPS connections and routes traffic to a real application.
