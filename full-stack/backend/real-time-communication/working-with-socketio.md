# 🔌 Working with Socket.io

## Emitting and Listening for Events

```js
// server.js
io.on("connection", (socket) => {
  socket.on("send-message", (message) => {
    console.log("Received:", message);
    io.emit("new-message", message); // broadcast to EVERY connected client
  });
});
```

```js
// client.js
socket.emit("send-message", "Hello, everyone!");

socket.on("new-message", (message) => {
  console.log("New message:", message);
});
```

Socket.io's entire API centers on two operations: `.emit(eventName, data)` sends a named event with
data attached, and `.on(eventName, callback)` listens for one. This is a genuinely different
mental model than [Express's request/response cycle](../expressjs-fundamentals/) — instead of a
route matching a URL and method, an event handler matches an arbitrary, application-defined event
name, and either side (client or server) can freely emit or listen at any time.

## `io.emit()` vs. `socket.emit()`

```js
io.emit("event", data);      // to EVERY connected client
socket.emit("event", data);  // to only THIS ONE client (the one this socket represents)
socket.broadcast.emit("event", data); // to every client EXCEPT this one
```

This distinction matters constantly in real code: `io` refers to the entire server, while `socket`
refers to one specific connection — choosing the wrong one either broadcasts something meant for
one user to everybody, or sends something meant for everybody to only one connection.

## Acknowledgements — a Request-Response Pattern on Top of Events

```js
// client.js
socket.emit("send-message", "Hello!", (response) => {
  console.log("Server confirmed:", response);
});
```

```js
// server.js
socket.on("send-message", (message, callback) => {
  saveMessage(message);
  callback("received"); // this reaches the client's callback above
});
```

An **acknowledgement** lets the sender receive direct confirmation that a specific event was
actually processed — a callback function, passed as `.emit()`'s last argument, is invoked by the
receiving side once it calls its own received `callback`. This layers a familiar
request-response pattern on top of Socket.io's otherwise fire-and-forget event model, useful
whenever the sender genuinely needs to know an event was handled, not just sent.

## A Realistic Chat Feature

```js
io.on("connection", (socket) => {
  socket.on("send-message", (data) => {
    const message = { text: data.text, userId: socket.userId, timestamp: Date.now() };
    io.emit("new-message", message);
  });

  socket.on("disconnect", () => {
    console.log(`${socket.userId} disconnected`);
  });
});
```

This combines emitting/listening with Socket.io's built-in `disconnect` event — automatically
fired when a client's connection closes, useful for cleanup logic (updating an "online" status, for
instance) exactly when it's genuinely needed.

## Common Mistakes

- Confusing `io.emit()` (everyone) with `socket.emit()` (just this one connection), sending an
  event to the wrong audience entirely.
- Forgetting that Socket.io event names are entirely application-defined strings — a typo in an
  event name on one side simply means the other side's listener never fires, with no error raised.
- Not handling the `disconnect` event when cleanup genuinely matters (removing a user from an
  "online users" list, for instance), leaving stale state behind after a client disconnects.

## ➡️ Next

Continue to [rooms-in-socketio.md](rooms-in-socketio.md) to broadcast to a specific subset of
connected clients, not everyone at once.
