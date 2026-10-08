# 📶 Offline Storage and Real-Time Web APIs

## 📚 Overview

This module covers the browser APIs that make web apps behave like native ones: storing large amounts of
structured data locally with IndexedDB, working offline through service workers and the Cache API, and
exchanging live data with a server using WebSockets or Server-Sent Events. It closes with a decision guide
for choosing between polling, long polling, SSE, and WebSockets. It extends
[local-storage.md](../using-browser-functionalities/local-storage.md), which pointed to IndexedDB for data
that outgrows `localStorage`.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Create and migrate an IndexedDB database, write and query it with transactions and indexes, and avoid
  the transaction auto-commit and `upgradeneeded` pitfalls.
- Explain the service worker lifecycle and use the Cache API with cache-first, network-first, and
  stale-while-revalidate strategies, including versioning and cleanup.
- Use `WebSocket` correctly — `readyState`, close codes, binary data, reconnection with backoff and
  jitter — and secure it with `wss://`, an Origin allowlist, and message validation.
- Consume Server-Sent Events with `EventSource`, explain `id`, `retry`, and `Last-Event-ID`, and state
  their limits.
- Choose among polling, long polling, SSE, and WebSockets for a given requirement.

## 📋 Prerequisites

- [Local Storage](../using-browser-functionalities/local-storage.md) and [Browser APIs](../using-browser-functionalities/browser-apis.md) — the storage and API context this module extends.
- [Advanced Asynchronous Patterns](../advanced-async-patterns/) — promises, `AbortController`, and Web Workers underlie every file.
- [Objects in Depth](../objects-in-depth/) — structured cloning explains what IndexedDB can store.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [indexeddb.md](indexeddb.md) | Object stores, indexes, transactions, migrations, quotas, and promise helpers |
| [service-workers-and-the-cache-api.md](service-workers-and-the-cache-api.md) | Lifecycle, registration rules, the Cache API, and three caching strategies |
| [websockets.md](websockets.md) | The client API, close codes, a tested server, reconnection, backpressure, and security |
| [server-sent-events.md](server-sent-events.md) | The `text/event-stream` format, automatic reconnection, `Last-Event-ID`, and limits |
| [choosing-a-real-time-strategy.md](choosing-a-real-time-strategy.md) | Polling vs. long polling vs. SSE vs. WebSockets; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you build apps that must work offline or update live — and for interviews: "design a chat
system", "WebSockets vs. SSE", and "how do service workers work" are standard questions, answered here with
tested behavior.

**Skim** the IndexedDB file if your app's data lives entirely on the server — but read the transaction
section, since the auto-commit rule surprises almost everyone. Read the security parts of the WebSocket
file regardless.

## 🧠 Knowledge Check

<details>
<summary>Why does an IndexedDB write throw <code>TransactionInactiveError</code> after an <code>await</code> on a timer or <code>fetch</code>?</summary>

A transaction commits automatically as soon as it has no pending requests and control returns to the
event loop. Awaiting something that isn't an IndexedDB request (a timer, a network call) lets the event
loop run with nothing pending, so the transaction finishes; the next `put` on it then throws
`TransactionInactiveError` ("The transaction has finished"). Do slow work first, then open a short
transaction.

</details>

<details>
<summary>How does Server-Sent Events resume a stream after the connection drops, without any client code?</summary>

`EventSource` reconnects automatically (after the server's `retry:` delay). It remembers the last `id:` it
received and sends it in a `Last-Event-ID` request header on the new connection, so a server that assigns
IDs can replay exactly the events the client missed.

</details>

## 📚 References

- [MDN: Using IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB) and [Storage quotas and eviction criteria](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria) — the data model, transactions, versioning, and limits.
- [MDN: Using Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers) and [`Cache`](https://developer.mozilla.org/en-US/docs/Web/API/Cache) — the lifecycle and cache API.
- [MDN: `WebSocket`](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket), [`CloseEvent`](https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent), and [Writing WebSocket servers](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers) — the client API, close codes, and the handshake.
- [MDN: Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) and [`EventSource`](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) — the stream format and client.
- [OWASP: WebSocket Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html) — `wss://`, Origin validation, authentication, and limits.
- [web.dev: Service workers](https://web.dev/learn/pwa/service-workers) — the Progressive Web App perspective.
- [`idb` on GitHub](https://github.com/jakearchibald/idb) and [`ws` on GitHub](https://github.com/websockets/ws) — the promise wrapper for IndexedDB and the Node.js WebSocket server library used in the examples.
- [javascript.info: IndexedDB](https://javascript.info/indexeddb), [WebSocket](https://javascript.info/websocket), [Server Sent Events](https://javascript.info/server-sent-events), and [Long polling](https://javascript.info/long-polling) — widely used walkthroughs.
- [W3Schools: Server-Sent Events API](https://www.w3schools.com/html/html5_serversentevents.asp) — a beginner-friendly overview.

## ➡️ Continue Your Learning Path

Continue to the How JavaScript Runs module, the next module in this section, which looks under the hood:
engines and JIT compilation, memory and garbage collection, transpilation, bundling, and runtimes.
