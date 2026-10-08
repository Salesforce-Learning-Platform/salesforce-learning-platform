# 🔌 WebSockets

## A Persistent, Two-Way Connection

HTTP is request/response: the client asks, the server answers, and the server cannot speak first.
**WebSockets** upgrade a single HTTP connection into a **persistent, full-duplex channel**: after the
handshake, either side can send messages at any time with very little overhead. That makes them the
standard tool for chat, collaborative editing, live dashboards that also send commands, multiplayer games,
and trading screens. MDN lists the API as Baseline widely available since July 2015.

URLs use the `ws://` and `wss://` schemes (the latter is WebSocket over TLS — the equivalent of `https://`).

## 🧪 The Client API

```js
const socket = new WebSocket("wss://example.com/chat");

socket.addEventListener("open", () => {
  socket.send("hello");                       // only valid once the connection is open
});

socket.addEventListener("message", (event) => {
  console.log("received:", event.data);
});

socket.addEventListener("error", () => { /* a failure occurred; a "close" event follows */ });

socket.addEventListener("close", (event) => {
  console.log(event.code, event.reason, event.wasClean);
});
```

### `readyState`

| Constant | Value | Meaning |
|----------|:-----:|---------|
| `WebSocket.CONNECTING` | 0 | The handshake is in progress |
| `WebSocket.OPEN` | 1 | Ready to send and receive |
| `WebSocket.CLOSING` | 2 | `close()` was called; closing handshake under way |
| `WebSocket.CLOSED` | 3 | The connection is closed (or never opened) |

Calling `send()` before the connection opens throws, which is the most common first mistake:

```js
const ws = new WebSocket(url);
ws.send("too early");
// InvalidStateError: Failed to execute 'send' on 'WebSocket': Still in CONNECTING state.
```

(Chrome's wording; Node.js and other browsers phrase it differently, but all throw `InvalidStateError`.)
Observed across a normal session — connect, echo, close — `readyState` went `0 → 1 → 2 → 3`, and the
events were `open`, `message: echo: hello`, then `close code=1000 wasClean=true reason="done"`.

### Sending and Receiving Data

`send()` accepts strings and binary data (`Blob`, `ArrayBuffer`, typed arrays). For incoming binary
messages, `binaryType` chooses the representation: the default is `"blob"`; set it to `"arraybuffer"` to
get an `ArrayBuffer` you can view with a typed array
([typed-arrays-and-binary-data.md](../built-in-objects-and-collections/typed-arrays-and-binary-data.md)):

```js
socket.binaryType = "arraybuffer";
socket.send(new Uint8Array([1, 2, 3]));
socket.onmessage = (e) => console.log(e.data instanceof ArrayBuffer, [...new Uint8Array(e.data)]);
// true [ 1, 2, 3 ]
```

Most applications send **JSON text** with a type field — `{ "type": "chat", "text": "hi" }` — and dispatch
on it. Parse with `JSON.parse` and validate the shape; never trust incoming messages
([json-serialization.md](../objects-in-depth/json-serialization.md)).

### Closing, and Close Codes

`socket.close(code, reason)` starts a clean closing handshake. The `close` event reports a numeric `code`
from RFC 6455 (as summarized by MDN) and whether it was `wasClean`:

| Code | Meaning |
|:----:|---------|
| 1000 | Normal closure |
| 1001 | Going away (server shutting down, or the page navigating away) |
| 1008 | Policy violation |
| 1011 | Server internal error |
| 1006 | **Abnormal closure** — the connection dropped without a close frame |

`1006` is special: it is never sent on the wire — the browser reports it locally when the connection is
lost. In tests, a server that killed the socket produced `code=1006 wasClean=false`; a server that
called `close(1001, "going away")` produced `code=1001 wasClean=true reason="going away"`. Connecting to a
host that doesn't exist produced an `error` event followed by `close` with `code=1006`.

## 🖥️ A Minimal Server (Node.js, with the `ws` Library)

Node.js has a built-in WebSocket *client* but no server; the widely used [`ws`](https://github.com/websockets/ws)
package provides one. This broadcast server — with an Origin allowlist, explained below — was run and
tested with two valid clients and one from a disallowed origin:

```js
import { WebSocketServer, WebSocket } from "ws";

const ALLOWED_ORIGINS = new Set(["https://app.example.com"]);
const wss = new WebSocketServer({ port: 8080 });

wss.on("connection", (socket, request) => {
  if (!ALLOWED_ORIGINS.has(request.headers.origin)) {
    socket.close(1008, "origin not allowed");               // policy violation
    return;
  }

  socket.on("message", (data, isBinary) => {
    for (const client of wss.clients) {                      // broadcast to every connected client
      if (client.readyState === WebSocket.OPEN) client.send(data, { binary: isBinary });
    }
  });
});
```

Result: both allowed clients received `hello everyone`, and the other was closed with
`code=1008 reason="origin not allowed"`. The handshake itself (an HTTP `GET` with `Upgrade: websocket`, a
`Sec-WebSocket-Key`, answered with `101 Switching Protocols` and a `Sec-WebSocket-Accept`) is handled for
you; MDN's guide to writing WebSocket servers describes the details, including that client-to-server
frames are masked.

## 🔁 Reconnecting: The API Does Not Do It For You

Connections drop — Wi-Fi changes, servers deploy, proxies time out. A `WebSocket` never reconnects on its
own, so production code wraps it. Use **exponential backoff with jitter** so a thousand disconnected
clients don't all retry at the same instant:

```js
class ReconnectingSocket {
  constructor(url, { onMessage, baseDelayMs = 100, maxDelayMs = 30_000, log = () => {} } = {}) {
    Object.assign(this, { url, onMessage, baseDelayMs, maxDelayMs, log });
    this.attempt = 0;
    this.closedByUser = false;
    this.connect();
  }

  connect() {
    this.socket = new WebSocket(this.url);
    this.socket.onopen = () => { this.attempt = 0; this.log("open"); };       // success resets the backoff
    this.socket.onmessage = (event) => this.onMessage?.(event.data);
    this.socket.onclose = () => {
      if (this.closedByUser) return;
      const ceiling = Math.min(this.maxDelayMs, this.baseDelayMs * 2 ** this.attempt);
      const wait = Math.random() * ceiling;                                    // "full jitter"
      this.attempt++;
      this.log(`closed; retry #${this.attempt} in <= ${ceiling} ms`);
      setTimeout(() => this.connect(), wait);
    };
  }

  send(data) {
    if (this.socket.readyState === WebSocket.OPEN) { this.socket.send(data); return true; }
    return false;                                                              // caller decides: queue or drop
  }

  close() { this.closedByUser = true; this.socket.close(1000); }
}
```

Tested against a server that terminated the connection on demand, the log read: `open`, `got echo: one`,
`closed; retry #1 in <= 50 ms`, `open`, `got echo: two` — it reconnected and carried on. After
reconnecting, an app usually must also **re-sync state**: messages sent while disconnected are gone, so
fetch what was missed (for example, "everything since message id N") over normal HTTP.

## 🚰 No Backpressure, No Ping API

- **`bufferedAmount`** is the number of bytes queued but not yet sent. `send()` always returns
  immediately and just queues; sending 5 MB of text left `bufferedAmount > 0` until it drained
  (`0` a moment later in the test). MDN is explicit that the API has **no backpressure**: if messages
  arrive faster than you process them, memory can be exhausted or the app can become unresponsive. For
  large or fast streams check `bufferedAmount` before sending more, and see MDN's note on
  `WebSocketStream`, a stream-based alternative that applies backpressure (check its compatibility —
  it is not available in every browser).
- **Heartbeats are your job.** The protocol has ping/pong control frames, but the browser's `WebSocket`
  object exposes no `ping()` or `pong()` — listing its members showed only `send`, `close`, `binaryType`,
  `bufferedAmount`, `extensions`, `protocol`, `readyState`, `url`, and the event handlers. To detect dead
  connections and keep idle ones open through proxies, send your own small messages on a timer and
  reconnect if replies stop.

## 🛡️ Security

OWASP's WebSocket Security Cheat Sheet is direct about the essentials:

- **Use `wss://`**, never plain `ws://`, in production. (Browsers enforce part of this: from an HTTPS page,
  opening an insecure WebSocket throws `SecurityError: … An insecure WebSocket connection may not be
  initiated from a page loaded over HTTPS.`)
- **Validate the `Origin` header** in the handshake against a strict allowlist. WebSockets are not
  restricted by the same-origin policy, so without this check any website a logged-in user visits can open
  a socket to your server using the user's cookies — *Cross-Site WebSocket Hijacking*. The server snippet
  above does it.
- **Authenticate and authorize.** Check permissions for each action, close sockets when sessions end, and
  for browser clients send a token in the **first message** rather than in the URL — query strings leak
  into logs.
- **Treat every message as untrusted:** validate its structure, parse JSON with `JSON.parse` (never
  `eval`), and enforce size and rate limits.

See [Cookies, CORS, and Transport Security](../../../web-security/cookies-cors-and-transport-security/)
for how cookies and origins interact.

## 📈 Scaling Notes

A WebSocket is a long-lived, stateful connection, which changes how you scale: a load balancer must keep
each connection pinned to one server, and a message meant for a user connected to *another* server needs a
shared channel between servers (a message broker or pub/sub). The platform's system-design material covers
those mechanics in [load-balancing.md](../../../system-design/high-level-design/core-infrastructure/load-balancing.md),
[message-queues.md](../../../system-design/high-level-design/core-infrastructure/message-queues.md), and the
worked [notification system design](../../../system-design/high-level-design/real-world-system-design-problems/designing-a-notification-system.md).

## 🎤 Interview Angle

- **"What is a WebSocket and how does it differ from HTTP?"** A persistent, full-duplex connection started
  with an HTTP upgrade handshake; either side can send at any time, unlike request/response.
- **"What happens if you call `send()` too early?"** It throws `InvalidStateError` — wait for `open`.
- **"Does the browser reconnect automatically?"** No — you implement it, with backoff and jitter.
- **"What is close code 1006?"** An abnormal closure reported locally when the connection dropped without
  a close frame.
- **"What is Cross-Site WebSocket Hijacking?"** A malicious page opening a WebSocket to your server with
  the victim's cookies; prevented by validating `Origin` (and authenticating properly).

## Common Mistakes

- **Sending before `open`.**
- **No reconnection logic**, or reconnecting with no backoff (a "thundering herd").
- **Putting tokens in the URL.**
- **Skipping the Origin check.**
- **Ignoring `bufferedAmount`** when streaming lots of data.
- **Assuming messages arrive during a disconnect** — re-sync after reconnecting.
- **Using `ws://` from an HTTPS page** (blocked) or in production.

## ➡️ Next

Continue to [server-sent-events.md](server-sent-events.md) for the simpler, one-way alternative built on
plain HTTP, with automatic reconnection included.
