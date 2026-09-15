# 🚪 Rooms in Socket.io

## Why Broadcasting to Everyone Isn't Always Right

[working-with-socketio.md](working-with-socketio.md)'s `io.emit()` sends to **every** connected
client — fine for a global announcement, but wrong for something scoped to a specific chat channel,
a specific order's status updates, or a specific user's own notifications across their multiple
open tabs. **Rooms** solve exactly this: a way to broadcast to a defined, specific subset of
connections.

## Joining a Room

```js
io.on("connection", (socket) => {
  socket.join("order-42-updates");
});
```

`socket.join(roomName)` subscribes that one connection to an arbitrary, application-defined room
name — a socket can join any number of rooms, and a room is created automatically the first time
any socket joins it, with no separate setup step required.

## Broadcasting to a Room

```js
io.to("order-42-updates").emit("status-changed", { status: "shipped" });
```

```js
// From inside a socket handler — sends to everyone in the room EXCEPT the sender
socket.to("order-42-updates").emit("status-changed", { status: "shipped" });
```

`io.to(roomName).emit(...)` sends an event only to sockets currently in that room — directly
solving the "not everyone" problem `io.emit()` alone couldn't. `socket.to(roomName)` is a variant
specifically for broadcasting **from** a socket that's itself in the room, deliberately excluding
that sender from receiving its own broadcast back.

## A Practical Pattern: One Room Per User

```js
io.on("connection", async (socket) => {
  const userId = await getUserIdFromAuth(socket); // per socketio-middleware.md
  socket.join(userId); // this user's OWN room, named after their ID

  // Later, from anywhere in the application:
  io.to(userId).emit("notification", { message: "Your order has shipped!" });
});
```

Joining every one of a user's connections (their laptop, their phone, a second browser tab) to a
room named after their own user ID is a genuinely practical, common pattern: notifying that user
means emitting to their room, reaching every one of their active devices/tabs at once, without the
application ever needing to track individual socket IDs manually.

## A Practical Pattern: One Room Per Chat Channel

```js
socket.on("join-channel", (channelId) => {
  socket.join(`channel-${channelId}`);
});

socket.on("send-message", ({ channelId, text }) => {
  io.to(`channel-${channelId}`).emit("new-message", { text, from: socket.userId });
});
```

The same pattern applies directly to a chat application: each channel is its own room, and a
message sent to a channel only reaches the other clients who've actually joined that specific
channel — never leaking into an unrelated channel's conversation.

## Common Mistakes

- Using `io.emit()` for something that should genuinely be scoped to a room, unintentionally
  broadcasting to every connected client regardless of relevance.
- Forgetting that a socket needs to explicitly `.join()` a room — simply knowing a room's name
  doesn't automatically add a connection to it.
- Using `io.to(...)` when the intent was actually to exclude the sender (`socket.to(...)`), causing
  a client to receive its own broadcast echoed back to it.

## ➡️ Next

Continue to [socketio-middleware.md](socketio-middleware.md) to make sure only genuinely
authenticated users can even establish a connection in the first place.
