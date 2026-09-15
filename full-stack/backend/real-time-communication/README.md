# ⚡ Real-Time Communication — WebSockets and Socket.io

## Purpose

Every API covered throughout this domain follows the same shape: the client asks, the server
answers, the connection closes. This module covers the genuinely different case — a **persistent**
connection where the server can push data to the client at any moment, with no new request
needed — the foundation of live chat, real-time notifications, and collaborative features.

## 🎯 Learning Objectives

- Explain the WebSocket protocol: the handshake, and the persistent, bidirectional connection it
  establishes.
- Explain why WebSockets are a genuine improvement over HTTP polling for real-time features.
- Distinguish Socket.io from raw WebSockets, and explain what Socket.io adds.
- Build a real-time feature with Socket.io: emitting and listening for events.
- Use Rooms to broadcast to a specific subset of connected clients.
- Apply authentication to a Socket.io connection with middleware.

## 📋 Prerequisites

- [Authentication and Authorization](../authentication-and-authorization/) — this module's
  middleware coverage authenticates a WebSocket connection the same way Express middleware
  authenticates an HTTP request.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [the-websocket-protocol.md](the-websocket-protocol.md) | The handshake, persistent connection, and WebSockets vs. HTTP polling |
| [websockets-vs-socketio.md](websockets-vs-socketio.md) | What Socket.io adds on top of raw WebSockets, and why they're not interoperable |
| [working-with-socketio.md](working-with-socketio.md) | Setting up a server and client, emitting and listening for events |
| [rooms-in-socketio.md](rooms-in-socketio.md) | Broadcasting to a specific subset of connected clients |
| [socketio-middleware.md](socketio-middleware.md) | Authenticating a connection before it's ever established |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [the-websocket-protocol.md](the-websocket-protocol.md) — understanding exactly why a
persistent connection genuinely differs from repeated HTTP requests is what makes every later
Socket.io-specific file in this module make sense, rather than feeling like arbitrary new syntax.

## ✅ Quick Knowledge Check

<details>
<summary>Can a plain WebSocket client connect directly to a Socket.io server?</summary>

No — Socket.io uses WebSocket as one of its underlying transports, but adds its own protocol-level
metadata to every packet that a plain WebSocket client doesn't understand. A Socket.io server needs
a genuine Socket.io client, not just any WebSocket client. See
[websockets-vs-socketio.md](websockets-vs-socketio.md).

</details>

<details>
<summary>How would you send a real-time update to only one specific user, across all of their open tabs/devices?</summary>

Join every socket connection belonging to that user to a Room named after their user ID, then emit
to that room — every one of their active connections receives it, without needing to track
individual socket IDs manually. See [rooms-in-socketio.md](rooms-in-socketio.md).

</details>

## 📚 References

- MDN, [The WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- Socket.io, [Official documentation](https://socket.io/docs/v4/)
- Socket.io, [Rooms](https://socket.io/docs/v4/rooms/)
- Socket.io, [Middlewares](https://socket.io/docs/v4/middlewares/)

## ➡️ Continue Your Learning Path

Continue to the [Caching — Local and Redis module](../caching-local-and-redis/) to keep a
real-time application's data fast as its traffic grows.
