# Application-Layer Protocols Overview

## Intuition

Every one of these protocols solves the same underlying problem as HTTP — two programs agreeing
on a message format so they can communicate — just for a different purpose. Once you understand
HTTP deeply (see [http-https-and-tls.md](../how-the-internet-works/http-https-and-tls.md)),
learning the shape of these others is mostly a matter of asking: what's the message format, and
what's it for?

## Email: SMTP, IMAP, POP3

Sending and reading email actually involves multiple distinct protocols, because "send a message"
and "retrieve my mailbox" are different problems:

| Protocol | Purpose | Default port(s) |
|---|---|---|
| **SMTP** (Simple Mail Transfer Protocol) | Sending mail from a client to a server, and relaying mail between mail servers | 25 (server-to-server), 587 (client submission) |
| **IMAP** (Internet Message Access Protocol) | Retrieving mail while keeping it synchronized on the server (read/unread state, folders) — the model used by most modern webmail and mobile clients | 143 (993 with TLS) |
| **POP3** (Post Office Protocol v3) | Retrieving mail by downloading it to one client, traditionally removing it from the server afterward | 110 (995 with TLS) |

A useful distinction: SMTP only ever *sends*; IMAP and POP3 only ever *retrieve*. A typical mail
client uses SMTP to send and IMAP (rarely POP3, today) to read — two separate protocol
conversations for what feels like one "email" feature.

## File Transfer: FTP and SFTP

**FTP** (File Transfer Protocol) is one of the Internet's oldest protocols, designed to upload and
download files between a client and server. Plain FTP transmits credentials and data
**unencrypted**, which is why it has been broadly superseded by:

- **SFTP** (SSH File Transfer Protocol) — file transfer running over an encrypted SSH connection
  (not related to FTP's own protocol design, despite the similar name).
- **FTPS** (FTP over TLS) — FTP with TLS encryption layered on, closer to how HTTPS relates to
  HTTP.

The practical takeaway: if you see plain `ftp://` in a modern system, treat it as a signal to
question why encryption isn't in use, the same way you would for plain `http://` handling
sensitive data.

## Remote Access: SSH

**SSH** (Secure Shell) provides an encrypted channel for logging into and running commands on a
remote machine, and is the modern, secure replacement for older unencrypted remote-access
protocols like Telnet. Beyond interactive shell access, SSH is the transport underneath SFTP and
underneath `git`'s SSH-based remote URLs (`git@github.com:...`) — the same encrypted-tunnel
mechanism is reused for multiple purposes.

## Real-Time Communication: WebSocket

HTTP's request-response model (client asks, server answers, connection can close) is a poor fit
for applications needing continuous, low-latency, two-way communication — a chat application, a
live collaborative document, real-time notifications. **WebSocket** solves this: a client makes an
initial HTTP request that "upgrades" the connection into a persistent, full-duplex channel, after
which either side can send messages at any time without the overhead of a new HTTP request/response
cycle for each one.

```text
HTTP (request/response):
  Client ── request ──▶ Server
  Client ◀── response ── Server
  (connection typically closes or is reused for the next independent request)

WebSocket (persistent, two-way):
  Client ── HTTP upgrade request ──▶ Server
  Client ◀── HTTP 101 Switching Protocols ── Server
  Client ◀───────── messages flow either direction, anytime ─────────▶ Server
  (connection stays open until explicitly closed)
```

WebSocket still starts as an HTTP request (the "upgrade handshake"), which is why WebSocket URLs
use `ws://` and `wss://` (the secure variant, analogous to `http://`/`https://`) and why it
inherits HTTP's addressing model even though the ongoing communication no longer looks like
HTTP at all.

## Common Mistakes

- Assuming "protocol" always means something as heavyweight as HTTP. Many protocols (like SMTP)
  are simple, plain-text, line-based exchanges.
- Believing WebSocket "replaces" HTTP. Most applications use both: HTTP for the initial page load
  and most data operations, WebSocket specifically for the subset of features needing real-time,
  persistent, bidirectional communication.
- Treating protocol choice as a purely technical/aesthetic preference rather than a direct
  consequence of the communication pattern needed — covered next.

## Next

Continue to
[choosing-and-recognizing-protocols.md](choosing-and-recognizing-protocols.md) to build the
reasoning skill for *why* a given protocol fits a given job.
