# 🛡️ Socket.io Middleware

## Authenticating a Connection Before It's Established

```js
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  try {
    socket.userId = jwt.verify(token, process.env.JWT_SECRET).userId; // per jwt.md
    next(); // allow the connection
  } catch {
    next(new Error("Authentication failed")); // reject it
  }
});
```

`io.use((socket, next) => {...})` registers **Socket.io middleware** — running once per
connection, *before* it's actually established, directly mirroring
[Express's middleware pattern](../expressjs-fundamentals/middleware.md) from earlier in this
domain: call `next()` to allow the connection through, or `next(new Error(...))` to reject it
outright. This lets the exact same [JWT verification](../authentication-and-authorization/jwt.md)
logic used throughout the rest of this domain protect a WebSocket connection too.

## The Client Sends Credentials During the Handshake

```js
// client.js
const socket = io("http://localhost:3000", {
  auth: { token: localStorage.getItem("accessToken") },
});
```

The client attaches its access token as part of the connection's `auth` option — read on the server
side via `socket.handshake.auth.token`, exactly as shown in the middleware above. This is Socket.io's
equivalent of an HTTP request's `Authorization` header, adapted to a connection that's established
once, not sent with every individual message afterward.

## Chaining Multiple Middleware Functions

```js
io.use(authenticationMiddleware);
io.use(rateLimitMiddleware);
io.use(loggingMiddleware);
```

Just like Express middleware, multiple `io.use()` calls run in sequence — if any one of them calls
`next()` with an error, the remaining middleware never runs, and the connection is rejected with a
`connect_error` event on the client side.

## Combining Middleware With Rooms

```js
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    socket.userId = jwt.verify(token, process.env.JWT_SECRET).userId;
    next();
  } catch {
    next(new Error("Authentication failed"));
  }
});

io.on("connection", (socket) => {
  socket.join(socket.userId); // per rooms-in-socketio.md — now safely using a VERIFIED user ID
});
```

This is the realistic, complete pattern: authentication middleware verifies the connection and
attaches a genuinely trusted `socket.userId`, which every later handler (including
[Rooms](rooms-in-socketio.md)'s "one room per user" pattern) can then safely rely on — never
trusting a client-supplied user ID directly, echoing the exact same principle from
[authentication-vs-authorization.md](../authentication-and-authorization/authentication-vs-authorization.md).

## Common Mistakes

- Skipping authentication middleware entirely and trusting a `userId` sent directly by the client
  in an event's data — exactly the same client-trust mistake
  [protecting-routes.md](../authentication-and-authorization/protecting-routes.md) already warns
  against for HTTP routes.
- Forgetting that Socket.io middleware runs once per **connection**, not per individual event — an
  already-established, authenticated connection doesn't re-run this middleware for every
  subsequent `.emit()`.
- Not handling the client-side `connect_error` event at all, leaving a user with no feedback when
  their connection is rejected by authentication middleware.

## Module Summary

Across this module: the **WebSocket protocol** upgrades an HTTP connection into a persistent,
bidirectional one, letting a server push data the instant something happens rather than only
responding to requests (see [the-websocket-protocol.md](the-websocket-protocol.md)); **Socket.io**
is its own protocol built on top of WebSockets (and other transports), adding reconnection,
buffering, acknowledgements, and rooms — genuinely incompatible with raw WebSocket clients (see
[websockets-vs-socketio.md](websockets-vs-socketio.md)); its **event-based API**
(`.emit()`/`.on()`) replaces the request/response model with named events either side can send at
any time (see [working-with-socketio.md](working-with-socketio.md)); **Rooms** broadcast to a
specific, defined subset of connections rather than everyone at once, with "one room per user" a
genuinely common real pattern (see [rooms-in-socketio.md](rooms-in-socketio.md)); and **middleware**
authenticates a connection before it's established, mirroring Express's own middleware pattern and
letting every later handler trust a verified `socket.userId`.
