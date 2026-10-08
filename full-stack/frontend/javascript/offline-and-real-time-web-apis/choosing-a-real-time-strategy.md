# 🧭 Choosing a Real-Time Strategy

## Four Ways to Get Fresh Data to the Page

"Real-time" is not one technology but a spectrum of techniques that trade simplicity against immediacy
and efficiency. There are four, and the right one is usually the simplest that meets the actual
requirement.

| Technique | How it works |
|-----------|--------------|
| **Polling** | The client asks on a timer: "anything new?" |
| **Long polling** | The client asks, and the server holds the request open until it has something (or a timeout) |
| **Server-Sent Events** | One long-lived HTTP response; the server writes events into it ([server-sent-events.md](server-sent-events.md)) |
| **WebSockets** | A persistent two-way connection ([websockets.md](websockets.md)) |

## ⏲️ Polling

The baseline: request on an interval.

```js
setInterval(async () => {
  const response = await fetch("/api/status");
  render(await response.json());
}, 5000);
```

It is trivial to build, works through every proxy and cache, and needs no special server. Its costs are
**latency** (an update waits up to a full interval) and **waste** (most requests return "nothing new").
Prefer a loop that waits for each request to finish before scheduling the next, as covered in
[timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md), so slow responses never
overlap. Polling is entirely appropriate when updates are infrequent or minutes of staleness are fine.

## ⏳ Long Polling

javascript.info's description: the server doesn't close the connection until it has a message to send.
The client reacts to each response by immediately asking again, so updates arrive almost instantly without
a special protocol — it is plain `fetch`:

(`delay(ms)` is the timer helper from
[promise-combinators-in-depth.md](../advanced-async-patterns/promise-combinators-in-depth.md).)

```js
async function longPoll(url, onMessage, { signal } = {}) {
  while (!signal?.aborted) {
    try {
      const response = await fetch(url, { signal });
      if (response.status === 200) onMessage(await response.json());
      // a 204 means "nothing new before the server's timeout" — just ask again
    } catch (error) {
      if (error.name === "AbortError") return;
      await delay(1000);                                    // back off after a network error
    }
  }
}
```

Run against a server that held each request for up to 150 ms and answered `204` on timeout, this loop
received both messages (`{ n: 1 }` at about 100 ms and `{ n: 2 }` at about 400 ms) and made 7 requests in
900 ms — the repeated empty `204`s are the price of the technique. It is the classic fallback when WebSockets
and SSE are unavailable, and it ties up one server connection per waiting client. Cancel it with an
[`AbortController`](../advanced-async-patterns/cancellation-with-abortcontroller.md), as above.

## 📡 Server-Sent Events

One-way, server-to-client push over a standard HTTP response, with **automatic reconnection and
resumption** (`Last-Event-ID`) built in. Text only; `GET` only; no custom headers; the six-connection
limit on HTTP/1.1 (MDN). Ideal for notifications, live feeds, progress updates, and dashboards that only
display.

## 🔌 WebSockets

A persistent **two-way** channel with low per-message overhead and binary support. You pay with more
infrastructure (connection-aware load balancing, an `Origin` check, authentication design) and more code
(reconnection with backoff, heartbeats, re-syncing missed messages). MDN also notes the API has **no
backpressure**. Ideal when the client and server both send frequently: chat, collaborative editing,
multiplayer, trading UIs.

## 🆚 Side by Side

| | Polling | Long polling | SSE | WebSockets |
|---|:-------:|:------------:|:---:|:----------:|
| Direction | Client → server (request/response) | Client → server (held request) | **Server → client** | **Both** |
| Latency | Up to one interval | Near-instant | Near-instant | Near-instant |
| Protocol | Plain HTTP | Plain HTTP | HTTP (`text/event-stream`) | Upgraded to WebSocket |
| Auto-reconnect | You write the loop | You write the loop | **Built in**, with resume | You write it |
| Binary data | Yes | Yes | No (text only) | **Yes** |
| Custom headers | Yes | Yes | **No** (`EventSource`) | No (browser API) |
| Server complexity | Lowest | Low | Low | Highest |
| Efficiency at scale | Poor (many empty requests) | Moderate | Good | **Best** for chatty traffic |

## 🧠 A Decision Guide

Ask these questions in order:

1. **How fresh must the data be?** If seconds or minutes of delay are fine and updates are rare, **poll**.
2. **Does data flow only from server to client?** (Notifications, feeds, progress, live scores.) Use
   **SSE** — it is simpler than a WebSocket and resumes for free.
3. **Does the client also send frequent, low-latency messages?** (Chat, shared editing, games.) Use
   **WebSockets**.
4. **Are you constrained by infrastructure** that blocks or mishandles long-lived or upgraded connections?
   Fall back to **long polling**.

A common, sensible design is hybrid: **SSE or WebSockets for live updates, plus ordinary `fetch` calls for
actions and for fetching anything missed after a reconnect** — the same split behind the delivery
channels in the platform's
[notification system design](../../../system-design/high-level-design/real-world-system-design-problems/designing-a-notification-system.md).

## 🏗️ Infrastructure Realities

Persistent connections change what the layers around your app must do:

- **Load balancers and proxies** must allow long-lived connections and must not buffer streamed
  responses; idle timeouts can drop quiet connections (use keep-alives or heartbeats). See
  [load-balancing.md](../../../system-design/high-level-design/core-infrastructure/load-balancing.md).
- **Servers hold state per connection**, so a message for a user connected elsewhere needs a shared
  channel between servers — typically a broker
  ([message-queues.md](../../../system-design/high-level-design/core-infrastructure/message-queues.md)).
- **Reconnection storms:** after a deploy or outage, every client reconnects at once. Backoff with jitter
  on the client, and capacity headroom on the server.
- **Security still applies:** use TLS (`https://`/`wss://`), authenticate the connection, validate
  messages, and check `Origin` for WebSockets.
- **Start simple:** polling or SSE is often enough, and moving up later is easier than operating
  WebSocket infrastructure you did not need.

## 🎤 Interview Angle

- **"Polling vs. long polling vs. SSE vs. WebSockets?"** Use the comparison table: direction, latency,
  reconnection, binary support, and operational cost.
- **"When would you pick SSE over WebSockets?"** For server-to-client-only data — notifications, feeds,
  progress — where simplicity, plain HTTP, and built-in resumption outweigh duplex communication.
- **"What problems do persistent connections create at scale?"** Per-connection server state, sticky
  routing, cross-server fan-out, idle timeouts, and reconnection storms.
- **"How do you not lose messages across a disconnect?"** Give events IDs and replay from the last one
  (SSE does this natively), or re-fetch missed data over HTTP after reconnecting.

## Common Mistakes

- **Reaching for WebSockets by default** when the data only flows one way.
- **Polling too frequently** without need, or with overlapping slow requests.
- **Assuming no message is lost** across reconnects.
- **Forgetting intermediaries** — proxies that buffer, load balancers that time out.
- **Not planning reconnection behavior** for the moment a server restarts.

## Module Summary

Across this module: **IndexedDB** is the asynchronous, transactional, indexed object database for large
structured data, with schema changes confined to `upgradeneeded` and transactions that auto-commit (see
[indexeddb.md](indexeddb.md)); **service workers and the Cache API** make a site work offline by proxying
requests through caching strategies — cache first, network first, stale-while-revalidate — under a
versioned lifecycle (see [service-workers-and-the-cache-api.md](service-workers-and-the-cache-api.md));
**WebSockets** give a persistent two-way channel that demands your own reconnection, heartbeat, and
security design (see [websockets.md](websockets.md)); **Server-Sent Events** give simple one-way push with
automatic reconnection and `Last-Event-ID` resumption (see
[server-sent-events.md](server-sent-events.md)); and choosing among **polling, long polling, SSE, and
WebSockets** is a matter of direction, latency, and operational cost — start with the simplest that works
(see this file).

## ➡️ Next

Continue to the How JavaScript Runs module, the next module in this section, which looks under the hood:
engines and JIT compilation, memory and garbage collection, transpilation, bundling, and runtimes.
