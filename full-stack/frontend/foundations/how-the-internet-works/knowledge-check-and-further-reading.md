# Knowledge Check and Further Reading

## Frequently Confused Concepts — Full Comparison

Each pair below was introduced in context earlier in this module; this table consolidates them
for quick review.

| Pair | The distinction | Covered in |
|---|---|---|
| Internet vs. Web | Internet = the global network infrastructure; Web = one application (HTML/HTTP-based documents) that runs on it | [what-is-the-internet.md](what-is-the-internet.md) |
| IP address vs. domain name | IP address is what routers actually use to deliver data; domain name is a human-readable label that must first be resolved to an IP address | [dns-and-domain-resolution.md](dns-and-domain-resolution.md) |
| MAC address vs. IP address | MAC identifies physical hardware on the local network; IP identifies logical location for routing across networks | [ip-addressing-and-nat.md](ip-addressing-and-nat.md) |
| DNS vs. HTTP | DNS resolves a name to an IP address; HTTP is the protocol that then carries the actual request/response content | [dns-and-domain-resolution.md](dns-and-domain-resolution.md), [http-https-and-tls.md](http-https-and-tls.md) |
| TCP vs. HTTP | TCP is the transport-layer mechanism for reliable byte delivery; HTTP is the application-layer protocol defining request/response meaning, built on top of TCP | [http-https-and-tls.md](http-https-and-tls.md) |
| HTTP vs. HTTPS | HTTPS is HTTP plus TLS: encryption, integrity, and server authentication that plain HTTP does not provide | [http-https-and-tls.md](http-https-and-tls.md) |
| Router vs. switch | A switch forwards traffic within one local network by MAC address; a router forwards traffic between different networks by IP address | [clients-servers-and-local-networks.md](clients-servers-and-local-networks.md) |
| Bandwidth vs. latency | Bandwidth is maximum capacity; latency is how long one round trip takes — a link can have high bandwidth and still feel slow if latency is high | [cdns-caching-and-performance.md](cdns-caching-and-performance.md) |
| Public IP vs. private IP | Public addresses are globally unique and Internet-routable; private addresses are reserved ranges reused inside countless separate local networks and never routed on the public Internet | [ip-addressing-and-nat.md](ip-addressing-and-nat.md) |
| Client vs. server | A role in a given exchange (who initiates vs. who listens and responds), not a fixed identity — the same machine can be both, in different interactions | [clients-servers-and-local-networks.md](clients-servers-and-local-networks.md) |
| CDN vs. origin server | The origin is the authoritative source of content; a CDN is a distributed cache in front of it that serves cacheable content from locations closer to each user | [cdns-caching-and-performance.md](cdns-caching-and-performance.md) |

## Practical Exercises

**Guided — see it for yourself**

1. Open a terminal and run `nslookup example.com` (or `dig example.com` on macOS/Linux). Identify
   the IP address returned, and note whether it's an A or AAAA-style answer.
2. Run `traceroute example.com` (macOS/Linux) or `tracert example.com` (Windows). Count how many
   hops the packet passes through before reaching its destination.

**Independent**

3. In your browser's DevTools Network tab, load a page and inspect the timing breakdown for the
   first request (DNS lookup, initial connection, TLS handshake, waiting/TTFB, content download).
   Identify which phase, from
   [what-happens-when-you-enter-a-url.md](what-happens-when-you-enter-a-url.md), each timing bucket
   corresponds to.
4. Find the `Cache-Control` and `ETag` (or lack thereof) response headers on three different
   resources loaded by a real site (an image, a script file, and the HTML document itself). Explain
   why their caching behavior differs.

**Real-World Scenario**

5. A teammate reports: "Our site was working yesterday, but today my browser says it can't find
   the server." Using the troubleshooting table in
   [cdns-caching-and-performance.md](cdns-caching-and-performance.md), list at least three
   distinct possible root causes at different layers (DNS, network, TLS, application), and describe
   one command or check you'd use to rule each one in or out.

**Architecture Challenge**

6. You're advising a team launching a product globally, with users concentrated in North America,
   Europe, and Southeast Asia, served from a single origin data center in one of those regions.
   Using the concepts of latency, CDNs, and caching from this module, explain what you would
   recommend to reduce perceived load time for users far from the origin, and what portion of the
   traffic (if any) a CDN cannot help with.

## Interview Questions

These are designed to test understanding and reasoning, not memorized trivia.

- Walk me through everything that happens, network-wise, between entering a URL and seeing a
  rendered page. Where does DNS end and HTTP begin?
- Why does HTTPS typically take longer to establish a connection than plain HTTP, and why is that
  overhead usually worth it?
- A user reports a "connection timed out" error, and another reports a "404 Not Found." Which one
  tells you more about where in the stack the problem is, and why?
- Why can't an external server usually initiate a connection directly to a laptop sitting behind a
  home router, without extra configuration?
- If a request to an API is slow, how would you determine whether the cause is DNS resolution,
  connection setup, network latency, or the server's own processing time?
- What would you check first if a DNS record change you made an hour ago still isn't visible to
  some users?
- Why is TCP the right choice for loading a web page, but UDP the right choice for a live video
  call?
- What does a CDN actually solve, and what problems does it *not* solve (e.g., for highly dynamic,
  personalized responses)?

## Cheat Sheet / Revision Summary

- **Internet** = network of networks; **Web** = one application (HTTP + HTML) running on it.
- **IP address** locates a machine; **DNS** lets you use a name instead of memorizing that
  address; **domain names** resolve through a hierarchy of nameservers (root → TLD → authoritative).
- **MAC address** = physical hardware identity (local network only); **IP address** = logical,
  routable location.
- **Private IP ranges** (`10.x`, `172.16–31.x`, `192.168.x`) stay inside a local network; **NAT**
  lets many private-addressed devices share one public IP.
- **TCP** = reliable, ordered, connection-oriented (three-way handshake); **UDP** = fast,
  connectionless, no delivery guarantee.
- **Ports** identify which program on a machine a connection is for (80 = HTTP, 443 = HTTPS, 53 =
  DNS).
- **HTTP** = the request/response protocol built on top of TCP; **HTTPS** = HTTP + **TLS**
  (encryption, integrity, server authentication).
- Loading a page = DNS → TCP handshake → (TLS handshake, if HTTPS) → HTTP request/response →
  browser rendering — repeated per external resource.
- **Caching** avoids repeating work; a **CDN** serves cached content from locations near the user
  instead of always hitting the origin.
- **Latency** (time per round trip) ≠ **bandwidth** (maximum capacity) ≠ **throughput** (actual
  achieved rate) — high bandwidth does not fix a high-latency problem.

## References

Primary and standards sources used and recommended for further study:

- IETF, [RFC 791 — Internet Protocol (IPv4)](https://www.rfc-editor.org/rfc/rfc791)
- IETF, [RFC 8200 — Internet Protocol, Version 6 (IPv6)](https://www.rfc-editor.org/rfc/rfc8200)
- IETF, [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918)
- IETF, [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293)
- IETF, [RFC 768 — User Datagram Protocol (UDP)](https://www.rfc-editor.org/rfc/rfc768)
- IETF, [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- IETF, [RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- IETF, [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034) / [RFC 1035 — Domain Names (concepts and implementation)](https://www.rfc-editor.org/rfc/rfc1035)
- MDN Web Docs, [How does the Internet work?](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Web_mechanics/How_does_the_Internet_work)
- MDN Web Docs, [An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)
- Salesforce Developers, [Named Credentials](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/sforce_api_calls_named_credentials.htm)
- Salesforce Help, [My Domain](https://help.salesforce.com/s/articleView?id=sf.domain_name_overview.htm)
