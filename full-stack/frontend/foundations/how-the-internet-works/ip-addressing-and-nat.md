# IP Addressing and NAT

## Intuition

For a letter to reach you, it needs a unique, unambiguous address. Every device on a network
needs the digital equivalent: an **IP address** — a numeric label that identifies where it is on
the network, so other devices know where to send data.

## IPv4

An **IPv4** address (defined in [RFC 791](https://www.rfc-editor.org/rfc/rfc791)) is a 32-bit
number, conventionally written as four decimal numbers from 0–255 separated by dots — "dotted
quad" notation — for example `93.184.216.34`.

32 bits gives roughly 4.3 billion possible addresses. That sounds like a lot, but with billions of
phones, laptops, servers, and IoT devices in the world, the pool of available public IPv4
addresses has effectively been exhausted for years. Two things have kept IPv4 usable this long:

- **NAT** (Network Address Translation — see below), which lets many devices share one public
  address.
- **IPv6**, a larger address space designed to eventually replace IPv4 rather than patch around
  its limits.

## IPv6

**IPv6** ([RFC 8200](https://www.rfc-editor.org/rfc/rfc8200)) uses 128-bit addresses, written as
eight groups of hexadecimal digits separated by colons, for example
`2606:2800:220:1:248:1893:25c8:1946`. Consecutive groups of zeros can be compressed once with
`::`, e.g. `2001:db8::1`.

128 bits provides an astronomically larger address space (approximately 3.4 × 10³⁸ addresses) —
enough that every device can be assigned a globally unique address without relying on NAT for
address conservation. IPv6 adoption is still gradual and uneven across networks; most production
systems today need to support both IPv4 and IPv6 ("dual stack").

| | IPv4 | IPv6 |
|---|---|---|
| Address size | 32 bits | 128 bits |
| Example | `93.184.216.34` | `2606:2800:220:1:248:1893:25c8:1946` |
| Total address space | ~4.3 billion | ~3.4 × 10³⁸ |
| Needs NAT for conservation? | Yes, in practice | No — designed with enough space to avoid it |
| Notation | Dotted decimal | Colon-separated hexadecimal |

## Public vs. Private IP Addresses

Not every IP address is reachable from the wider Internet. Certain address ranges are reserved by
[RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) for **private** use inside local networks:

- `10.0.0.0 – 10.255.255.255`
- `172.16.0.0 – 172.31.255.255`
- `192.168.0.0 – 192.168.255.255`

Devices inside your home or office network are typically assigned a private address from one of
these ranges by your router (via **DHCP**, the protocol that automatically hands out addresses to
new devices). Private addresses are reused in millions of unrelated networks simultaneously —
your home router almost certainly assigns addresses starting with `192.168.` and so does your
neighbor's, with no conflict, because private addresses are never routed across the public
Internet.

A **public** IP address, by contrast, is globally unique and reachable from anywhere on the
Internet — this is the address your ISP assigns to your router itself (not to every individual
device inside your home).

## NAT (Network Address Translation)

**NAT** is the mechanism, typically running on your router, that lets every device on your private
network share a single public IP address. When a device with a private address (say
`192.168.1.42`) sends a request out to the Internet, the router rewrites the packet's source
address to its own public IP, keeps a translation table entry recording which internal device made
that request, and rewrites the destination address of the reply back to the correct private
address when it comes back.

```text
Laptop (192.168.1.42) ──┐
Phone  (192.168.1.55) ──┼──▶ Router / NAT (public IP: 203.0.113.9) ──▶ Internet
Smart TV (192.168.1.61)─┘             (translation table tracks who asked what)
```

This is why, from the outside, every device behind a typical home router appears to come from the
same public IP address, and why an external server generally cannot initiate a connection
*into* a device sitting behind NAT without extra configuration (port forwarding) — the router has
no standing rule for unsolicited inbound traffic to a private address it hasn't seen requested.

## MAC Address vs. IP Address

These are two different addresses assigned to the same network interface, operating at different
layers and for different purposes — a frequent point of confusion.

| | MAC Address | IP Address |
|---|---|---|
| What it identifies | The physical network hardware (network interface card) | A device's logical location on a network |
| Assigned by | The hardware manufacturer, burned in at manufacture (though it can be overridden in software) | The network (statically configured, or dynamically via DHCP) |
| Format | 48-bit, e.g. `3C:5A:B4:11:22:33` | 32-bit (IPv4) or 128-bit (IPv6) |
| Scope | Only meaningful on the local network segment | Globally meaningful for routing across networks |
| Changes when...? | Effectively never (it's tied to the physical hardware) | Frequently — a laptop gets a new IP on every network it joins |

A useful analogy: the MAC address is like a device's permanent serial number; the IP address is
like its current street address. A switch uses MAC addresses to deliver frames within one
building; a router uses IP addresses to figure out which building to send something to at all.

## Common Mistakes

- Thinking a device has exactly one IP address for life. Most devices get a new (often private)
  IP address every time they join a network, and a laptop can hold different IPs on Wi-Fi vs.
  Ethernet simultaneously.
- Assuming a public IP address always identifies a single physical machine. Many servers sit
  behind load balancers or NAT gateways of their own, and one public IP may front many backend
  machines.
- Confusing "private IP address" with "hidden/secure." Private addressing is about routability and
  address conservation, not encryption or security — it happens to make direct inbound attacks
  from the public Internet harder, but it is not itself a security control.

## Next

Continue to [dns-and-domain-resolution.md](dns-and-domain-resolution.md) — IP addresses are how
computers find each other, but humans use names. DNS is the system that translates between them.
