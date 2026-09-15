# ⚖️ WebSockets vs. Socket.io

## Socket.io Is Not a WebSocket Implementation

This is a genuinely important, easy-to-misunderstand distinction: **Socket.io is not just a
convenience wrapper around the raw WebSocket API** covered in
[the-websocket-protocol.md](the-websocket-protocol.md) — it's its own protocol, layered on top.
Socket.io adds its own metadata to every packet it sends, which means **a plain WebSocket client
cannot connect to a Socket.io server, and vice versa** — they're genuinely incompatible, despite
Socket.io using WebSockets as one of its underlying transports.

## What Socket.io Actually Adds

- **Automatic transport fallback** — if a raw WebSocket connection genuinely can't be established
  (a restrictive network, an older environment), Socket.io automatically falls back to HTTP
  long-polling instead, rather than simply failing.
- **Automatic reconnection** — with exponential backoff, Socket.io reconnects on its own after a
  dropped connection, rather than leaving the application to detect and handle that manually.
- **Packet buffering while disconnected** — messages sent during a brief disconnection aren't
  silently lost; they're buffered and delivered once reconnected.
- **Acknowledgements** — a request-response pattern *on top of* the persistent connection, letting
  one side confirm a specific message was actually received and processed.
- **Rooms and broadcasting** — sending an event to a specific subset of connected clients, covered
  fully in [rooms-in-socketio.md](rooms-in-socketio.md).

## When Raw WebSockets Are Still the Right Choice

A minimal, tightly-controlled real-time feature — where both the client and server are fully under
your own control, and none of Socket.io's extra reliability features are genuinely needed — can
reasonably use the raw WebSocket API directly, avoiding an additional dependency. Socket.io earns
its place specifically when its reconnection handling, fallback transport, and room-based
broadcasting genuinely save real, otherwise-manual implementation work.

## Installing and Connecting

```bash
npm install socket.io socket.io-client
```

```js
// server.js
import { Server } from "socket.io";
const io = new Server(3000);

io.on("connection", (socket) => {
  console.log("A client connected:", socket.id);
});
```

```js
// client.js
import { io } from "socket.io-client";
const socket = io("http://localhost:3000");
```

This is the Socket.io equivalent of
[the-websocket-protocol.md](the-websocket-protocol.md)'s raw `new WebSocket(...)` — a server
listening for connections, and a client establishing one, but through Socket.io's own protocol and
library, not the raw browser WebSocket API directly.

## Common Mistakes

- Assuming a raw WebSocket client can connect to a Socket.io server (or the reverse) — the two
  protocols are genuinely incompatible despite sharing WebSocket as an underlying transport option.
- Choosing Socket.io out of habit for a project that has no real need for its reconnection,
  fallback, or room features — adding an unnecessary dependency for capability that goes unused.
- Forgetting that Socket.io's automatic fallback to HTTP long-polling means a "WebSocket
  connection" in a Socket.io app might not actually be using a real WebSocket at all, in a
  restrictive network environment.

## ➡️ Next

Continue to [working-with-socketio.md](working-with-socketio.md) to build an actual real-time
feature with Socket.io's event-based API.
