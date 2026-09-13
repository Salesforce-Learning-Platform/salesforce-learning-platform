# Understanding HTTP and HTTPS

## Purpose

[http-https-and-tls.md](../how-the-internet-works/http-https-and-tls.md) explained HTTP and HTTPS
at the network-layering level — how they relate to TCP and TLS. This module is the practitioner's
view: the actual vocabulary you use every day building or debugging web applications — HTTP
methods, the full status-code taxonomy, and the headers that control caching, content
negotiation, and authentication.

## Learning Objectives

- Choose the correct HTTP method for a given operation, and explain the difference between safe,
  idempotent, and neither.
- Read an HTTP status code and correctly identify which side (client or server) is responsible for
  the outcome it describes.
- Categorize HTTP headers by purpose and explain what the most common ones actually do.
- Explain, precisely, what HTTPS adds to HTTP and why a valid certificate is not optional for
  production systems.

## Prerequisites

[http-https-and-tls.md](../how-the-internet-works/http-https-and-tls.md).

## Files in This Module

| File | Covers |
|---|---|
| [http-methods-in-depth.md](http-methods-in-depth.md) | GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS — semantics, safety, idempotency |
| [http-status-codes-in-depth.md](http-status-codes-in-depth.md) | The full status-code taxonomy and how to reason about which one to return or expect |
| [http-headers-in-depth.md](http-headers-in-depth.md) | Request/response headers grouped by purpose: content, caching, auth, CORS |
| [https-in-practice.md](https-in-practice.md) | What a production team actually needs to get right about certificates and HTTPS enforcement |
