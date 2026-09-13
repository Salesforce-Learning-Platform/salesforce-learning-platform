# How the Internet Works

## Purpose

Every web application — a static marketing site, a React single-page app, or a Salesforce
Experience Cloud site — ultimately depends on the same underlying machinery: computers finding
each other across a global network and exchanging data in an agreed-upon format. This module
builds a technically accurate mental model of that machinery, so that later modules (HTTP/HTTPS,
browsers, frameworks, deployment, security) have something solid to build on.

This is a **foundations** module. It intentionally stays at the level a frontend or full-stack
engineer actually needs: enough to reason correctly about latency, outages, caching, and
security, without becoming a networking specialization.

## Learning Objectives

By the end of this module, you should be able to:

- Explain what the Internet is, and how it differs from the Web.
- Describe the client-server model and identify the network components a request passes through
  (device, local network, router, ISP, backbone, destination server).
- Explain IP addressing (IPv4 and IPv6), the difference between public and private addresses, and
  what NAT does.
- Explain how DNS turns a domain name into an IP address, and name the DNS record types most
  relevant to running a web application.
- Explain the role of TCP and UDP, what a port is, and how packets are routed across networks.
- Explain how HTTP and HTTPS relate to TCP, and what TLS actually protects.
- Narrate, in order, everything that happens between typing a URL and seeing a rendered page.
- Explain what a CDN and a cache do, and define latency, bandwidth, and throughput without mixing
  them up.
- Correctly distinguish the concept pairs that beginners (and interviewers) most often confuse.

## Prerequisites

None. This module assumes no prior networking knowledge. Basic comfort with using a web browser
and the command line is helpful but not required.

## Mental Model

Before any terminology, hold onto this shape. Everything else in this module is filling in the
detail behind each arrow.

```text
You (Browser)
     │  "take me to example.com"
     ▼
Internet (a network of networks)
     │  find the right computer, carry the message there and back
     ▼
Server (a computer that is always listening for requests)
     │  runs your application, decides what to send back
     ▼
Response travels back through the same kind of path
     ▼
Browser turns the response into the page you see
```

The Internet's job, in one sentence, is to let any two connected computers exchange data
reliably, even though neither one knows the physical route the data will take.

## How This Module Is Organized

Read the files in this folder in order — each one builds on the last:

| # | File | What it covers |
|---|------|-----------------|
| 1 | [what-is-the-internet.md](what-is-the-internet.md) | Internet vs. the Web, network of networks, packet switching intuition |
| 2 | [clients-servers-and-local-networks.md](clients-servers-and-local-networks.md) | Client-server model, end devices, local networks, routers, switches, ISPs |
| 3 | [ip-addressing-and-nat.md](ip-addressing-and-nat.md) | IPv4/IPv6, MAC vs. IP, public vs. private addresses, NAT |
| 4 | [dns-and-domain-resolution.md](dns-and-domain-resolution.md) | Domain names, nameservers, DNS resolution, DNS record types |
| 5 | [tcp-ip-ports-and-routing.md](tcp-ip-ports-and-routing.md) | TCP/IP model, TCP vs. UDP, ports, packets, routing, firewalls |
| 6 | [http-https-and-tls.md](http-https-and-tls.md) | HTTP request/response, HTTPS, TLS, how they relate to TCP |
| 7 | [what-happens-when-you-enter-a-url.md](what-happens-when-you-enter-a-url.md) | The full end-to-end walkthrough, tying every prior file together |
| 8 | [cdns-caching-and-performance.md](cdns-caching-and-performance.md) | CDNs, caching, latency, bandwidth, throughput, reliability, failure points |
| 9 | [knowledge-check-and-further-reading.md](knowledge-check-and-further-reading.md) | Commonly confused concepts, exercises, interview questions, cheat sheet, references |

## Frequently Confused Concepts (Preview)

These pairs are covered in depth where they naturally arise, and summarized together in
[knowledge-check-and-further-reading.md](knowledge-check-and-further-reading.md):

- Internet vs. Web
- IP address vs. domain name
- MAC address vs. IP address
- DNS vs. HTTP
- TCP vs. HTTP
- HTTP vs. HTTPS
- Router vs. switch
- Bandwidth vs. latency
- Public IP vs. private IP
- Client vs. server
- CDN vs. origin server

## Salesforce Relevance

Salesforce is delivered as a multi-tenant cloud platform: every request to a Salesforce org,
Experience Cloud site, or Lightning component ultimately travels over the same DNS → TCP/TLS →
HTTP path described in this module. Concepts introduced here reappear directly in Salesforce
contexts:

- Custom domains and "My Domain" in Salesforce depend on DNS (CNAME records pointing at
  Salesforce-managed infrastructure).
- Experience Cloud sites are frequently served or accelerated through a CDN, which is why cache
  invalidation matters after a publish.
- Named Credentials, Remote Site Settings, and outbound integrations all depend on correct DNS
  resolution, TLS, and firewall/IP allow-listing on both ends.
- API request latency in Apex callouts is bounded by the same network fundamentals (DNS lookup
  time, TCP/TLS handshake time, round-trip time) covered here.

These connections are called out again, more concretely, in
[what-happens-when-you-enter-a-url.md](what-happens-when-you-enter-a-url.md) and
[cdns-caching-and-performance.md](cdns-caching-and-performance.md).

## When to Deep-Dive vs. Skim

If you've never studied networking before, read every file in this module in full and in order —
it's the most heavily depended-on module in the entire Frontend learning path. If you already have
networking background, you can skim the earlier files but should still read
[what-happens-when-you-enter-a-url.md](what-happens-when-you-enter-a-url.md) closely — it's the
synthesis every later module (especially
[Understanding HTTP and HTTPS](../understanding-http-and-https/) and
[CDNs, Caching, and Performance](cdns-caching-and-performance.md)) assumes you can narrate from
memory.

## Quick Knowledge Check

Try answering before revealing each answer — this is a much better test of retention than
recognizing the answer once you see it.

<details>
<summary>What's the difference between the Internet and the Web?</summary>

The Internet is the global network infrastructure (IP, routing, ISPs). The Web is one application
that runs on top of it, built from HTML documents linked together and transferred via HTTP/HTTPS.
Email, SSH, and Salesforce API calls all use the Internet without using the Web at all. See
[what-is-the-internet.md](what-is-the-internet.md).

</details>

<details>
<summary>Why does establishing an HTTPS connection take longer than plain HTTP, before any actual page data is sent?</summary>

HTTPS requires a TCP handshake, then a TLS handshake, both completed before the first HTTP request
is even sent. Each adds at least one network round trip. See
[what-happens-when-you-enter-a-url.md](what-happens-when-you-enter-a-url.md).

</details>

## Continue Your Learning Path

Next in the [Foundations sequence](../README.md):
[Client-Server Architecture](../client-server-architecture/).
