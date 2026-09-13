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
