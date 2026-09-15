# 🤝 The WebSocket Protocol

## Every Prior API Has Been Request-Response

```
Client: "GET /products"  →  Server: "here's the data"  →  connection closes
```

Every endpoint covered throughout [REST API Design](../rest-api-design/) follows this exact
shape — the client always initiates, the server always responds, and the connection doesn't
persist. This is fundamentally unsuited to something like a live chat message arriving, or a stock
price updating — the server has no way to push that new information to the client without the
client first asking for it.

## The Handshake — Upgrading From HTTP

```
Client → Server: a normal-looking HTTP request, but with special headers:
  Upgrade: websocket
  Sec-WebSocket-Key: <a randomly generated value>

Server → Client: confirms the upgrade:
  Sec-WebSocket-Accept: <computed from the client's key>

... the connection now stays open, as a WebSocket, not HTTP ...
```

A WebSocket connection actually **begins** as a normal HTTP request, carrying special headers
(`Upgrade: websocket`, a `Sec-WebSocket-Key`) signaling the client's intent. If the server agrees,
it responds with a computed `Sec-WebSocket-Accept` header, and the underlying TCP connection is then
**upgraded** — it stops behaving like HTTP entirely and becomes a persistent WebSocket connection.

## A Persistent, Bidirectional Connection

```js
const socket = new WebSocket("ws://localhost:8080");

socket.addEventListener("open", () => {
  socket.send("Hello Server!");
});

socket.addEventListener("message", (event) => {
  console.log("Message from server:", event.data);
});
```

Once established, the connection stays open indefinitely — either side (client **or** server) can
send a message to the other **at any time**, with no need to re-establish a connection or wait for
a request first. This is the genuinely new capability: the server can now push data to the client
the instant something happens, rather than only ever responding to a request the client happened to
send.

## Why This Beats HTTP Polling

```
POLLING (the old workaround): the client sends a new HTTP request
every few seconds, just to ask "anything new?" — mostly wasted
requests, and updates only arrive as fast as the polling interval.

WEBSOCKET: the server pushes an update the INSTANT it happens — no
wasted requests, no polling-interval delay at all.
```

Before WebSockets, real-time-*feeling* features were approximated with **polling** — repeatedly
sending new HTTP requests just to check for updates. This wastes significant bandwidth and server
resources on requests that usually find nothing new, and introduces real, felt latency bounded by
however often the client happens to poll. A genuine WebSocket connection eliminates both problems:
no repeated requests, and updates arrive the moment they happen.

## Common Mistakes

- Confusing a WebSocket connection with a single HTTP request/response — it's fundamentally a
  different kind of connection, persistent rather than one-shot.
- Assuming polling is always the wrong choice — for infrequent updates where true real-time
  delivery genuinely doesn't matter, polling's simplicity can still be a reasonable, valid choice.
- Forgetting that a WebSocket connection, once open, needs its own lifecycle handling (`open`,
  `message`, `close`, `error`) — it doesn't behave like a single request that naturally completes.

## ➡️ Next

Continue to [websockets-vs-socketio.md](websockets-vs-socketio.md) to see the library this module
actually uses to work with WebSockets in a real Node.js application.
