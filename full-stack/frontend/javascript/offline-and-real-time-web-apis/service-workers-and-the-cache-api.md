# 🛰️ Service Workers and the Cache API

## A Programmable Network Proxy in the Browser

A **service worker** is a script that the browser runs in the background, separate from any page, and that
sits **between your pages and the network**. web.dev describes it as a middleware proxy for a Progressive
Web App: every request from the pages it controls can be intercepted, answered from a cache, forwarded to
the network, or rewritten. That single capability enables offline support, instant repeat loads, and
resilience to flaky connections.

A service worker is a kind of [Web Worker](../advanced-async-patterns/web-workers.md) — its own thread and
global scope, no DOM access, communication by messages — with two differences: it is **event-driven** (the
browser starts it to handle events and may stop it when idle), and it has a **lifecycle** that persists
across page loads.

## 🔐 Requirements

- **A secure context.** Per MDN, service workers require HTTPS, with `localhost` exempt for development.
- **A same-origin script, at a real URL.** The browser must be able to fetch the worker file from your
  own origin. In a test on an HTTPS page, registration failed in each way you might try:

```js
await navigator.serviceWorker.register("/sw.js");
// TypeError: Failed to register a ServiceWorker for scope ('https://example.com/') with script
//            ('https://example.com/sw.js'): A bad HTTP response code (404) was received when fetching the script.

await navigator.serviceWorker.register(URL.createObjectURL(new Blob(["…"], { type: "text/javascript" })));
// TypeError: Failed to register a ServiceWorker: The URL protocol of the script ('blob:<id>') is not supported.

await navigator.serviceWorker.register("https://example.org/sw.js");
// SecurityError: Failed to register a ServiceWorker: The origin of the provided scriptURL
//                ('https://example.org') does not match the current origin ('https://example.com').
```

(Unlike ordinary Web Workers, a service worker cannot be built from a `Blob` URL.)

- **A scope.** The worker controls pages under its **scope**, which defaults to the directory of the script.
  A worker served from `/sw.js` can control the whole site; one served from `/assets/sw.js` only
  `/assets/…`.

## 🔁 The Lifecycle

```
register()  →  install  →  (waiting)  →  activate  →  controls pages → fetch events…
```

1. **Register** — the page calls `navigator.serviceWorker.register("/sw.js")`.
2. **Install** — fires once for a new version. Use it to **pre-cache** assets; call `event.waitUntil()`
   with a promise to keep the install open until caching finishes. If that promise rejects, installation
   fails.
3. **Waiting** — a new version installs but does **not** take over while the old version still controls
   open pages, so a page never switches code mid-session.
4. **Activate** — fires once the old version is retired. Use it for **cleanup** (deleting old caches).
5. **Fetch** — afterwards, every in-scope request triggers a `fetch` event; `event.respondWith()` supplies
   the response.

`self.skipWaiting()` lets a new worker skip the waiting phase, and `clients.claim()` lets an activated
worker take control of pages that are already open (otherwise they are controlled only after a reload).
Use them deliberately: switching code under a running page can break it.

## 🗃️ The Cache API

The Cache API stores **`Request`/`Response` pairs** in named caches. It is available in service workers
*and* in ordinary pages (`window.caches`), and works without a service worker:

```js
const cache = await caches.open("v1");

await cache.put(new Request("/api/hello"),
  new Response(JSON.stringify({ msg: "hi" }), { headers: { "content-type": "application/json" } }));

const hit = await cache.match("/api/hello");
console.log(hit.status, hit.headers.get("content-type"));   // 200 application/json
console.log(await hit.json());                               // { msg: 'hi' }
console.log((await cache.keys()).map((r) => new URL(r.url).pathname));   // [ '/api/hello' ]
console.log(await caches.keys());                            // [ 'v1' ]

await cache.add("/");                                        // fetch a URL and cache the response
console.log(await cache.delete("/api/hello"), await cache.delete("/api/hello"));   // true false
```

Methods: `match`, `matchAll`, `add`, `addAll`, `put`, `delete`, `keys`. Four behaviors to know:

- **A `Response` body can be read only once.** Reading it twice throws
  `TypeError: Failed to execute 'text' on 'Response': body stream already read`. To store a response *and*
  return it to the page, store a **clone**:

```js
const copy = response.clone();               // one for the cache, one for the page
cache.put(request, copy);
return response;
```

- **Only `GET` requests can be cached.** `cache.put(new Request(url, { method: "POST", body }), …)` rejects
  with `TypeError: … Request method 'POST' is unsupported`.
- **Nothing expires.** MDN: items in a `Cache` "do not get updated unless explicitly requested; they don't
  expire unless deleted." You own versioning and cleanup.
- **Caches share the origin's storage quota** with IndexedDB
  ([indexeddb.md](indexeddb.md)).

## 📜 A Complete Minimal Service Worker

```js
// sw.js
const CACHE = "app-v1";
const PRECACHE = ["/", "/styles.css", "/app.js", "/offline.html"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)));
});

self.addEventListener("activate", (event) => {
  // delete every cache that isn't the current version
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
    )
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;          // let non-GET requests go to the network
  event.respondWith(networkFirst(event.request, event));   // strategy functions: see the next section
});
```

```js
// in the page
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js");
}
```

The versioned cache name is the update mechanism: ship `app-v2`, and the new worker's `install` fills the
new cache while old pages keep using `app-v1`; its `activate` then deletes everything else (the pattern
MDN's guide recommends).

## 🎯 Caching Strategies

The `fetch` handler is where the design decisions live. These three functions were run against the real
Cache API in a browser:

```js
// 1. CACHE FIRST — fastest; for assets that rarely change (fonts, versioned JS/CSS)
async function cacheFirst(request, event) {
  const cached = await caches.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  const copy = response.clone();
  event.waitUntil(caches.open(CACHE).then((cache) => cache.put(request, copy)));
  return response;
}

// 2. NETWORK FIRST — freshest; for data and HTML, with an offline fallback
async function networkFirst(request, event) {
  const cache = await caches.open(CACHE);
  try {
    const response = await fetch(request);
    event.waitUntil(cache.put(request, response.clone()));
    return response;
  } catch (error) {
    const cached = await cache.match(request);
    if (cached) return cached;
    throw error;                                      // nothing cached and no network
  }
}

// 3. STALE WHILE REVALIDATE — instant AND self-refreshing; for content where "a little old" is fine
async function staleWhileRevalidate(request, event) {
  const cache = await caches.open(CACHE);
  const cached = await cache.match(request);

  const networkFetch = fetch(request).then((response) => {
    event.waitUntil(cache.put(request, response.clone()));   // update the cache in the background
    return response;
  });

  if (cached) {
    event.waitUntil(networkFetch.catch(() => {}));            // keep the worker alive; ignore offline errors
    return cached;                                             // answer immediately with the stale copy
  }
  return networkFetch;
}
```

What the test showed:

- **Cache first:** the first call went to the network (status 200) and cached the response; the second
  was served from the cache.
- **Network first:** online, the network answered; offline, a cached copy was returned — and with *no*
  cached copy and no network, the original `TypeError: Failed to fetch` propagated.
- **Stale while revalidate:** with a cached copy, the call returned the stale content **immediately** while
  a background fetch replaced the cache entry with fresh content; the next call was served the fresh copy;
  offline with a cached copy, it still answered and swallowed the failed refresh.

| Strategy | Choose it for | Trade-off |
|----------|---------------|-----------|
| Cache first | Versioned/immutable assets | May serve outdated content forever unless the URL or cache name changes |
| Network first | HTML pages, API data that must be fresh | Slow when the network is slow; falls back only on failure |
| Stale while revalidate | Avatars, feeds, non-critical API data | Users may briefly see old content |

`event.waitUntil()` around the `cache.put` calls matters: without it, the browser may stop the worker
before the background write finishes.

## 🧩 What Else Service Workers Enable

Push notifications and background sync build on the same worker (their browser support varies — check
MDN's compatibility tables), and a service worker plus a web app manifest is what makes a site an
installable **Progressive Web App**. web.dev's
[service workers guide](https://web.dev/learn/pwa/service-workers) covers that route.

## 🎤 Interview Angle

- **"What is a service worker?"** An event-driven background script acting as a programmable proxy
  between a page and the network, enabling offline use and caching; it needs HTTPS and has its own
  lifecycle.
- **"Explain the lifecycle."** Register → install (pre-cache) → waiting (until old pages close) →
  activate (clean up) → fetch events; `skipWaiting` and `clients.claim` shortcut the waiting and
  control steps.
- **"Name three caching strategies."** Cache first, network first, stale-while-revalidate — with when
  each fits.
- **"Why `response.clone()`?"** A body can be consumed once; clone one copy for the cache and return the
  other.
- **"Why can't I register a service worker from a Blob URL (or another origin)?"** The script must be a
  same-origin, fetchable URL.

## Common Mistakes

- **Caching with no versioning or cleanup**, so users are stuck on old files.
- **Forgetting `event.waitUntil`** around background work.
- **Returning a response and caching the same object** without cloning.
- **Trying to cache `POST` requests.**
- **Cache-first for HTML**, trapping users on a stale app shell.
- **Testing without understanding the waiting phase** — a new worker may not control the page until all
  old tabs close or you call `skipWaiting`.

## ➡️ Next

Continue to [websockets.md](websockets.md) to move from caching data to streaming it live over a
persistent two-way connection.
