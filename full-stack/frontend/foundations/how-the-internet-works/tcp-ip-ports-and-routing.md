# TCP/IP, Ports, and Routing

## Intuition

Knowing a destination's address (IP) isn't enough — you also need rules for how to package the
message, how to make sure it arrives intact and in order, and how to tell the destination *which*
of its many running programs the message is for. That's what this file covers: the transport
mechanics between "I know the IP address" and "the right application on that machine received my
data correctly."

## The TCP/IP Model

Networking is commonly explained using a layered model, where each layer only worries about its
own job and hands off to the layer below or above it. The practical, widely used version is the
four-layer **TCP/IP model** (a simplified relative of the more academic seven-layer OSI model):

| Layer | Responsibility | Examples |
|---|---|---|
| Application | The actual data/protocol your program cares about | HTTP, DNS, SMTP |
| Transport | End-to-end delivery between programs, using ports | TCP, UDP |
| Internet | Addressing and routing between networks | IP (IPv4/IPv6) |
| Link | Delivery across one physical/local network segment | Ethernet, Wi-Fi |

Each layer wraps the layer above it in its own header as data moves down the stack to be sent, and
unwraps it in reverse on the receiving end — this is called **encapsulation**.

```text
HTTP request (Application)
   ↓ wrapped in
TCP segment, with source/destination PORT (Transport)
   ↓ wrapped in
IP packet, with source/destination IP ADDRESS (Internet)
   ↓ wrapped in
Ethernet/Wi-Fi frame, with source/destination MAC ADDRESS (Link)
   ↓
Physical transmission (cable / radio waves)
```

## Packets and Packet Switching

Data sent over IP is broken into **packets** — bounded-size chunks, each carrying a header (source
IP, destination IP, and other control information) plus a portion of the actual payload. Each
packet is routed independently; as covered briefly in
[what-is-the-internet.md](what-is-the-internet.md), packets belonging to the same
conversation can travel different physical paths and still be reassembled correctly at the
destination, because each carries enough information to be delivered and sequenced on arrival.

## Routing

**Routing** is the process by which routers decide, packet by packet, which direction to forward
traffic so it gets closer to its destination IP address. Routers maintain **routing tables**
mapping ranges of IP addresses to the next router ("next hop") that traffic for that range should
be sent to. No single router knows the complete path to every destination on the Internet — each
one only needs to know a *better* next hop than "just guess," and routers exchange routing
information with each other (using protocols such as BGP between large networks) to keep those
tables reasonably accurate as the network changes.

A helpful way to see this yourself: the `traceroute` (or `tracert` on Windows) command sends
packets designed to reveal each router hop along the path to a destination, which is a genuinely
useful troubleshooting tool when you suspect an issue is "somewhere in the network" rather than in
your application.

## TCP vs. UDP

**TCP** and **UDP** are the two dominant transport-layer protocols, and they make fundamentally
different tradeoffs.

### TCP (Transmission Control Protocol)

TCP ([RFC 9293](https://www.rfc-editor.org/rfc/rfc9293)) provides a **reliable, ordered,
connection-oriented** stream between two endpoints:

- Before any data is sent, the two sides perform a **three-way handshake** (`SYN` →
  `SYN-ACK` → `ACK`) to establish a connection.
- Every segment is acknowledged; lost segments are automatically retransmitted.
- Segments are reassembled in the correct order even if they arrive out of sequence.
- This reliability has a cost: extra round trips for the handshake, and retransmission delay when
  packets are lost.

TCP is what HTTP (and therefore virtually all web traffic), plus email and file transfer, are
built on — correctness matters more than raw speed for a web page or an API response.

### UDP (User Datagram Protocol)

UDP ([RFC 768](https://www.rfc-editor.org/rfc/rfc768)) is **connectionless and unreliable** by
design: it sends datagrams without a handshake, without guaranteed delivery, and without guaranteed
ordering. There's no automatic retransmission — if a datagram is lost, it's simply gone unless the
application itself handles that.

This sounds strictly worse than TCP, but the lack of overhead is exactly the point for use cases
where a late retransmitted packet is *worse than useless*: live video/voice calls, DNS lookups
(a single small request/response, where TCP's handshake overhead would be wasteful for most
queries), and online gaming, where an old, retransmitted position update is worthless once new
ones exist.

| | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented (handshake required) | Connectionless |
| Reliability | Guaranteed delivery, automatic retransmission | Best-effort, no retransmission |
| Ordering | Guaranteed | Not guaranteed |
| Overhead | Higher (handshake, acknowledgments) | Lower |
| Typical uses | HTTP/HTTPS, email, file transfer | DNS queries, video/voice calls, live gaming |

## Ports

An IP address gets a packet to the correct *machine*; a **port** gets it to the correct
*program* running on that machine. A port is a 16-bit number (0–65535) that, combined with an IP
address and a transport protocol, uniquely identifies one endpoint of a network connection (this
combination — IP + port + protocol — is called a **socket**).

Certain "well-known ports" are conventionally reserved for specific protocols:

| Port | Protocol |
|---|---|
| 80 | HTTP |
| 443 | HTTPS |
| 53 | DNS |
| 22 | SSH |
| 25 | SMTP (email) |

This is why a URL like `https://example.com:8443/` explicitly names a port — when no port is
given, the browser assumes the default for the scheme (80 for `http://`, 443 for `https://`).

## Firewalls

A **firewall** is a system that inspects traffic against a set of rules and allows or blocks it —
most commonly based on IP address, port, and protocol. At the foundational level relevant here:
firewalls are why a server can run software listening on many ports but only expose the ones
intentionally opened to the outside world, and why Salesforce and many enterprise integrations
require **IP allow-listing** or specific outbound-port rules to permit a connection at all. A
firewall is a policy-enforcement point, not a form of encryption or authentication by itself.

## Common Mistakes

- Believing "the connection failed" always means a code bug. It can just as easily mean a
  firewall rule blocking the port, an incorrect port in the URL, or a broken route somewhere
  between client and server.
- Assuming TCP is always the "better" choice because it's reliable. UDP is the *correct* choice
  when low latency matters more than perfect delivery of every packet.
- Thinking a port number belongs to a machine rather than to a specific listening program on that
  machine — two different applications on the same server can both accept connections, as long as
  each binds to a different port.

## Next

Continue to [http-https-and-tls.md](http-https-and-tls.md) to see the application-layer protocol
built on top of TCP that actually carries web page requests and responses.
