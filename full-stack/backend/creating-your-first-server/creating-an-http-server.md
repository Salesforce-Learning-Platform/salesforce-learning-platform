# Creating an HTTP Server

## What a Server Actually Is

A **server**, in the most literal sense, is just a program that keeps running indefinitely,
listening on a specific network **port** for incoming connections, and responding to each one. It's
not fundamentally different from any other Node.js program — it just never naturally reaches the
end of its script, because `server.listen()` keeps the event loop alive, waiting for the next
request.

## Building One With `http.createServer()`

```js
import { createServer } from "node:http";

const server = createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Hello, Node.js server!");
});

server.listen(3000, () => {
  console.log("Server running at http://localhost:3000");
});
```

`createServer()` takes a single callback — the **request listener** — and returns a server object.
That callback runs once for *every* incoming request, receiving a request object (`req`) and a
response object (`res`), covered fully in
[request-and-response.md](request-and-response.md). `server.listen(3000)` starts the server
actually accepting connections on port `3000` — until this line, nothing is listening at all.

## What Happens on Each Request

```
Browser/client                    Node.js server
     │                                  │
     │──── GET http://localhost:3000/ ─>│
     │                                  │  createServer's callback runs
     │                                  │  with a fresh req/res for THIS
     │                                  │  request specifically
     │<──── 200 OK, "Hello, Node.js" ───│
```

Every single incoming request triggers a brand-new call to the request-listener callback, with its
own fresh `req` and `res` objects — one server handles arbitrarily many requests over its lifetime,
and (per
[how-nodejs-works.md](../starting-with-nodejs/how-nodejs-works.md)'s non-blocking model) can be in
the middle of handling several at once.

## Ports

```js
server.listen(3000); // "please let me use port 3000 on this machine"
```

A **port** is a number identifying a specific "channel" on a machine that a program can claim to
receive network traffic on. `3000` and `8080` are common conventions for local development (ports
below `1024` are typically reserved and require elevated permissions on most operating systems); a
real production deployment usually serves standard web traffic on port `80` (HTTP) or `443`
(HTTPS), often through infrastructure — a reverse proxy or load balancer — that forwards it to
whatever port the application itself actually listens on.

## Common Mistakes

- Forgetting to call `server.listen()` at all — `createServer()` alone only *creates* the server
  object; nothing is actually listening for connections until `.listen()` runs.
- Trying to `.listen()` on a port another already-running process has claimed, producing an
  `EADDRINUSE` error — a common source of confusion the first time a previous server instance
  wasn't properly stopped.
- Assuming the request-listener callback only runs once — it runs fresh for *every single request*
  the server ever receives, for as long as it keeps running.

## Next

Continue to [request-and-response.md](request-and-response.md) to actually read what the client
sent, and send back something meaningful in return.
