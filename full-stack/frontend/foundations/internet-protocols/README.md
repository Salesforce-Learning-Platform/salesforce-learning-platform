# Internet Protocols

## Purpose

[How the Internet Works](../how-the-internet-works/) went deep on the protocols every web request
depends on: IP, TCP/UDP, DNS, and HTTP/HTTPS. This module steps back and surveys the wider
protocol landscape — the other agreed-upon "languages" systems use to communicate — so you can
recognize what's actually happening when you see `ftp://`, `ssh user@host`, or a WebSocket
connection in a codebase, and reason about *why* a given protocol was chosen for a given job.

## Learning Objectives

- Name the major application-layer protocols beyond HTTP and explain what each is for.
- Identify whether a protocol is connection-oriented or connectionless, and why that matters for
  its use case.
- Explain what makes WebSocket different from ordinary HTTP request/response.
- Reason about *why* a particular protocol fits a particular communication need — the core skill
  this module builds toward, not the memorization of a protocol list.

## Prerequisites

[How the Internet Works](../how-the-internet-works/), especially
[tcp-ip-ports-and-routing.md](../how-the-internet-works/tcp-ip-ports-and-routing.md) and
[http-https-and-tls.md](../how-the-internet-works/http-https-and-tls.md).

## Files in This Module

| File | Covers |
|---|---|
| [application-layer-protocols-overview.md](application-layer-protocols-overview.md) | Email, file transfer, remote access, and real-time protocols |
| [choosing-and-recognizing-protocols.md](choosing-and-recognizing-protocols.md) | The requirements that drive protocol choice, and how to spot a protocol in real tooling |

## A Quick Map of What's Already Covered Elsewhere

| Protocol | Layer | Covered in |
|---|---|---|
| IP (IPv4/IPv6) | Internet | [ip-addressing-and-nat.md](../how-the-internet-works/ip-addressing-and-nat.md) |
| TCP / UDP | Transport | [tcp-ip-ports-and-routing.md](../how-the-internet-works/tcp-ip-ports-and-routing.md) |
| DNS | Application | [dns-and-domain-resolution.md](../how-the-internet-works/dns-and-domain-resolution.md) |
| HTTP / HTTPS / TLS | Application | [http-https-and-tls.md](../how-the-internet-works/http-https-and-tls.md) |

This module does not repeat those — it adds to the map.

## When to Deep-Dive vs. Skim

If you're only building conventional HTTP-based web applications, you can skim this module — its
main value is recognition (knowing what `ws://` or `ftp://` mean when you see them) rather than
daily use. Deep-dive
[application-layer-protocols-overview.md](application-layer-protocols-overview.md) specifically if
you're about to build a real-time feature (chat, live notifications) and need to justify choosing
WebSocket over repeated HTTP polling.

## Quick Knowledge Check

<details>
<summary>Why does WebSocket start as an HTTP request, even though the ongoing communication doesn't look like HTTP at all?</summary>

The initial "upgrade handshake" reuses HTTP's addressing and negotiation so the connection can pass
through the same infrastructure (proxies, firewalls) that already allows ordinary web traffic,
before switching to a persistent, full-duplex channel. See
[application-layer-protocols-overview.md](application-layer-protocols-overview.md).

</details>

<details>
<summary>What question should you ask first when choosing between two protocols for a new feature?</summary>

Whether the communication is a one-off request/response or an ongoing conversation, and whether
guaranteed delivery matters more than low latency — the requirement should determine the protocol,
not familiarity. See
[choosing-and-recognizing-protocols.md](choosing-and-recognizing-protocols.md).

</details>

## Continue Your Learning Path

Next in the [Foundations sequence](../README.md):
[Understanding HTTP and HTTPS](../understanding-http-and-https/).
