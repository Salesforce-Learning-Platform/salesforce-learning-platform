# 📡 Server-Sent Events

## One-Way Push, Over Plain HTTP

Many "real-time" features only need data to flow **from the server to the page**: notifications, a live
feed, a progress bar for a background job, stock prices, build logs. For those, WebSockets are more
machinery than necessary. **Server-Sent Events (SSE)** is a simple standard for exactly this case: the
page opens one ordinary HTTP request through the **`EventSource`** API, the server keeps the response open
and writes events into it as they happen, and the browser parses them and handles reconnection for you.

MDN's description: it is a one-way channel in which the server streams events to the browser and the
client cannot send events back over it; the response has `Content-Type: text/event-stream` and the stream
is UTF-8 text.

## 🧪 The Client

```js
const source = new EventSource("/events");

source.onopen = () => console.log("connected");

source.onmessage = (event) => {                       // unnamed events
  console.log(event.data, event.lastEventId);
};

source.addEventListener("tick", (event) => {           // named events (the server's `event:` field)
  console.log("tick", JSON.parse(event.data));
});

source.onerror = () => console.log("connection lost; the browser will retry");

// when you are done:
source.close();
```

`readyState` is `0` (`CONNECTING`), `1` (`OPEN`), or `2` (`CLOSED`). The `EventSource` object has just
these members: `url`, `withCredentials`, `readyState`, `close()`, and the `onopen`/`onmessage`/`onerror`
handlers — it is far smaller than `WebSocket`.

## 📄 The Stream Format

The server sends text in a simple line-based format. Each **event** is a block of `field: value` lines
ended by a **blank line**:

| Field | Meaning |
|-------|---------|
| `data:` | The payload. Several `data:` lines in one event are joined with newlines |
| `event:` | An event name; named events go to `addEventListener(name, …)`, unnamed ones to `onmessage` |
| `id:` | Sets the event's ID, remembered by the browser for reconnection |
| `retry:` | How long to wait before reconnecting, in milliseconds |
| `:` (a line starting with a colon) | A comment — ignored by the client, handy as a keep-alive |

## 🖥️ A Server (Plain Node.js)

No library is required — it is just an HTTP response that is not ended:

```js
import http from "node:http";

http.createServer((req, res) => {
  res.writeHead(200, {
    "Content-Type": "text/event-stream",     // the signal that this is an SSE stream
    "Cache-Control": "no-cache",
    Connection: "keep-alive",
  });

  res.write("retry: 200\n\n");                       // reconnect after 200 ms if the connection drops
  res.write(": keep-alive comment\n\n");             // comments are ignored by the client
  res.write("id: 1\ndata: first message\n\n");
  res.write('id: 2\nevent: tick\ndata: {"n":1}\n\n'); // a named event
  res.write("data: line one\ndata: line two\n\n");    // multi-line data

  // keep the response open and keep writing events as things happen…
}).listen(3000);
```

## 🔬 What Happens in Practice

This server and a client were run against each other (using Node's experimental `EventSource`, which
follows the same specification as the browser's). The server deliberately closed the connection twice. The
client log, with times rounded to 50 ms:

```
readyState at construction: 0
0ms   open (readyState 1)
0ms   message id="1" data="first message"
0ms   tick event, data={"n":1}
0ms   message id="2" data="line one\nline two"
50ms  error (readyState 0)
250ms open (readyState 1)
250ms message id="3" data="after reconnect"
300ms error (readyState 0)
500ms open (readyState 1)
500ms message id="4" data="third connection"
after close(): readyState 2
```

Reading it closely teaches the whole protocol:

- **Named events** reached the `tick` listener; the unnamed ones reached `onmessage`.
- **Multi-line `data`** arrived as one string joined with `\n`.
- **The last event ID is sticky.** The "line one / line two" event had no `id:` line, yet its
  `lastEventId` was still `"2"` — the browser keeps the most recent ID until a new one arrives.
- **Reconnection is automatic.** When the server ended the response, `onerror` fired with `readyState`
  back at `0` (connecting), and — after the 200 ms the server requested with `retry:` — the client
  reconnected on its own.
- **`Last-Event-ID` makes resuming possible.** The server logged the requests it received:

```
request 1:  GET  Accept: text/event-stream                       (no Last-Event-ID)
request 2:  GET  Accept: text/event-stream  Last-Event-ID: 2      ← the client reports where it left off
request 3:  GET  Accept: text/event-stream  Last-Event-ID: 3
```

A server that assigns every event an `id:` can read the `Last-Event-ID` header on reconnect and replay
exactly the events the client missed — **resumable streams with no client code at all**. (With
`WebSockets`, you build that yourself.)

`source.close()` ends the stream and prevents any further reconnection.

## ⚠️ Limitations

- **One direction only.** To send data to the server, make a normal `fetch`/`POST` request alongside.
- **`GET` requests, and no custom headers.** `EventSource` issues a plain `GET`, and its constructor takes
  only a URL and a `withCredentials` option — so you cannot set an `Authorization` header. Authenticate
  with a **cookie** (pass `{ withCredentials: true }` for cross-origin requests, which are subject to
  CORS), or stream with `fetch` instead:

```js
const response = await fetch("/events", { headers: { Authorization: `Bearer ${token}` } });
const decoder = new TextDecoder();
for await (const chunk of response.body) {
  handle(decoder.decode(chunk, { stream: true }));      // you now parse the event format yourself
}
```

  (See [async-iterators-and-for-await.md](../advanced-async-patterns/async-iterators-and-for-await.md).
  Libraries wrap this pattern.)
- **Text only.** The stream is UTF-8 text; send JSON, and encode binary data (for example Base64) if you
  must.
- **Connection limits on HTTP/1.1.** MDN: without HTTP/2, browsers allow only **6 SSE connections per
  browser and domain**, shared across all tabs; with HTTP/2 the limit is negotiated (default 100). Multiple
  tabs each opening several streams can exhaust it, so serve SSE over HTTP/2 and keep to one stream per
  page.
- **Proxies and servers must not buffer.** Anything between the app and the browser that buffers the
  response delays events; send periodic comment lines as keep-alives so idle connections are not closed.

## 🎤 Interview Angle

- **"What are Server-Sent Events?"** A standard for the server to push text events to the browser over a
  long-lived HTTP response, consumed with `EventSource`; one-way, with automatic reconnection.
- **"How does SSE resume after a dropped connection?"** The browser reconnects automatically (after the
  `retry:` delay) and sends the last `id:` it saw in a `Last-Event-ID` header; the server can replay
  missed events.
- **"SSE vs. WebSockets?"** SSE is simpler, plain HTTP, one-way, text-only, auto-reconnecting; WebSockets
  are full-duplex, support binary, but need more infrastructure and reconnection code.
- **"How do you authenticate an `EventSource`?"** With cookies, since custom headers aren't possible — or
  by streaming with `fetch` instead.

## Common Mistakes

- **Forgetting the blank line** that ends each event, so nothing is delivered.
- **Wrong `Content-Type`** (it must be `text/event-stream`).
- **Expecting to send data back** through the `EventSource`.
- **Trying to set an `Authorization` header** on `EventSource`.
- **Opening a stream per component** and running into the six-connection limit on HTTP/1.1.
- **No keep-alive comments**, so a proxy silently drops idle streams.

## ➡️ Next

Continue to [choosing-a-real-time-strategy.md](choosing-a-real-time-strategy.md) to compare polling, long
polling, SSE, and WebSockets and pick the right one.
