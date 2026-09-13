# Choosing and Recognizing Protocols

## The Underlying Questions

Every protocol choice ultimately answers a small set of requirements. Asking these questions about
any communication need will point you toward the right family of protocol, before you know any
protocol's name:

| Question | If the answer favors... | Example protocols |
|---|---|---|
| Does every message need guaranteed, ordered delivery? | Reliability | TCP-based protocols: HTTP, SMTP, FTP |
| Is a small amount of data loss acceptable in exchange for lower latency? | Speed over guarantees | UDP-based protocols: DNS queries, live video/voice |
| Is this a one-off request/response, or an ongoing conversation? | One-off → request/response; ongoing → persistent connection | HTTP for one-off; WebSocket for ongoing |
| Does the data need to be encrypted in transit? | Security | HTTPS, SFTP/FTPS, SSH — vs. their unencrypted counterparts |
| Is a human going to type this by hand, or is it purely machine-to-machine? | Human-typed protocols tend to be simple, line-based text | SMTP's plain-text command structure vs. a binary protocol |

This reasoning is more durable than memorizing a protocol list, because new protocols keep
appearing (HTTP/3's QUIC, gRPC, various pub/sub messaging protocols) and they can all be
understood by asking the same questions.

## Recognizing a Protocol in the Wild

Protocols are usually visible in plain sight, once you know where to look:

- **URL scheme**: `https://`, `ftp://`, `ws://`, `ssh://` — the part before `://` names the
  protocol being used.
- **Default port numbers**: seeing traffic on port 25 or 587 strongly suggests SMTP; port 22
  suggests SSH; port 443 suggests HTTPS. (Full port table in
  [tcp-ip-ports-and-routing.md](../how-the-internet-works/tcp-ip-ports-and-routing.md).)
- **Command-line tools that name the protocol directly**: `ssh user@host`, `git clone
  git@github.com:...` (SSH under the hood), `curl ftp://...`.
- **Browser DevTools' Network tab**: shows the actual protocol used for each request, including
  whether a connection was upgraded to WebSocket.

## A Worked Example

Suppose you're asked to design the transport for a live customer-support chat feature. Walking
through the questions above:

- Ongoing conversation, not a one-off request → favors a persistent connection over repeated HTTP
  polling.
- Low latency matters for a "live" feel → favors something lighter than repeated full HTTP
  request/response cycles.
- Needs to work through the same infrastructure (firewalls, proxies) that already allows normal
  web traffic → favors a protocol that starts as an ordinary HTTP request.

This combination of requirements is exactly why **WebSocket** (see
[application-layer-protocols-overview.md](application-layer-protocols-overview.md)) is the
standard choice for this kind of feature, rather than SMTP, FTP, or plain repeated HTTP requests —
the requirements determine the protocol, not the other way around.

## Common Mistakes

- Choosing a protocol because it's familiar rather than because it fits the requirement (e.g.,
  reaching for repeated HTTP polling for a real-time feature purely out of familiarity, when the
  requirements actually call for WebSocket).
- Assuming a protocol's presence implies security. Seeing `ftp://` or `ws://` (not `wss://`) is a
  signal to check whether encryption is actually needed and missing.
- Forgetting that most real systems combine multiple protocols for different parts of one feature
  — e.g., HTTPS for the initial page and most API calls, WebSocket only for the live-updating part.

## Module Summary

Web applications rarely use only HTTP under the hood. Recognizing SMTP/IMAP/POP3 for email,
FTP/SFTP for file transfer, SSH for secure remote access, and WebSocket for persistent real-time
communication — and reasoning from requirements (reliability, latency, statefulness, security)
rather than memorization — lets you understand *why* an unfamiliar system was built the way it
was.
