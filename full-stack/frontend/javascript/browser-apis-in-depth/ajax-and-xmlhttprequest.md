# 📡 AJAX and XMLHttpRequest

## The Technique That Made Single-Page Apps Possible

**AJAX** — "Asynchronous JavaScript And XML" — is the technique of requesting data from a server in the
background and updating part of a page, without reloading it. The name is historical: the
**`XMLHttpRequest`** (XHR) object at its heart can fetch any type of data, not just XML, and today most
payloads are JSON. XHR was the foundation of every interactive web app from the mid-2000s on.

Modern code uses [`fetch`](../asynchronous-programming-and-modules/fetch-api.md), which MDN describes as
the promise-based replacement that integrates with service workers and CORS, where XHR "uses callbacks."
But you will keep meeting XHR in older codebases, in libraries that wrap it, and in interview
questions about how AJAX works. Understanding it
also clarifies what `fetch` improved.

## 🧱 The Basic Shape

```js
const xhr = new XMLHttpRequest();

xhr.open("GET", "/api/data");          // configure: method + URL (nothing is sent yet)
xhr.responseType = "json";             // ask the browser to parse the body

xhr.onload = () => {
  console.log(xhr.status, xhr.response);
};
xhr.onerror = () => console.error("Network error");

xhr.send();                            // send the request; returns immediately (async by default)
```

Request headers are added with `setRequestHeader` after `open()` and before `send()`; response headers
are read with `getResponseHeader`:

```js
xhr.open("POST", "/api/items");
xhr.setRequestHeader("Content-Type", "application/json");
xhr.send(JSON.stringify({ name: "Ada" }));

// later, in onload:
xhr.getResponseHeader("content-type");     // e.g. "text/html; charset=utf-8" in a test GET of a page
```

### `readyState`: Five Stages

The request moves through numbered states; `onreadystatechange` fires on each change:

| `readyState` | Name | Meaning |
|:------------:|------|---------|
| 0 | `UNSENT` | Created, `open()` not yet called |
| 1 | `OPENED` | `open()` called |
| 2 | `HEADERS_RECEIVED` | Response headers have arrived |
| 3 | `LOADING` | The body is downloading |
| 4 | `DONE` | The operation is complete (success **or** failure) |

Observed in a real browser for a successful `GET`, the handler fired for states `1, 2, 3, 4`. Today
you almost always use the friendlier `load`, `error`, `abort`, and `progress` events instead of
checking `readyState === 4` by hand.

### `responseType`

`responseType` chooses the shape of `xhr.response`: `"text"` (the default), `"json"`, `"blob"`,
`"arraybuffer"`, or `"document"`.

```js
xhr.responseType = "blob";
xhr.onload = () => console.log(xhr.response instanceof Blob, xhr.response.type);   // true text/html
```

With `"json"`, a body that is not valid JSON yields `xhr.response === null` rather than throwing — in a
test, requesting an HTML page with `responseType = "json"` gave `status: 200, response: null`.

## 🧯 Errors: HTTP Failures Are Not Network Failures

XHR and `fetch` agree on a point that confuses many beginners: an HTTP error **status** is a *successful
exchange* as far as the network is concerned.

```js
// A request for a page that does not exist:
//   XHR:    onload fires, with xhr.status === 404          (onerror does NOT fire)
//   fetch:  the promise resolves, with response.ok === false and response.status === 404
```

Both test results confirmed it. MDN says the same of `fetch`: it fulfills with a `Response` for
statuses like 404, so you must check `response.ok` and throw yourself. The `error` event (XHR) or a
rejection (`fetch`) means the request never completed — a dropped connection, a DNS failure, a CORS
block:

```js
// XHR, unreachable host:   onerror fires; xhr.status is 0
// fetch, unreachable host: rejects with TypeError: Failed to fetch
```

## 🪄 Wrapping XHR in a Promise

Before `fetch`, libraries wrapped XHR in promises. The pattern is short and instructive:

```js
function xhrRequest(method, url) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onload = () => resolve({ status: xhr.status, body: xhr.responseText });
    xhr.onerror = () => reject(new Error("Network error"));
    xhr.send();
  });
}

const page = await xhrRequest("GET", "/");            // status 200, body present
const missing = await xhrRequest("GET", "/nope");     // resolves with status 404 — not a rejection
```

Notice the wrapper reproduces the same rule as `fetch`: it *resolves* for a 404 and rejects only on
network errors.

## 📊 Progress Events and Cancellation

XHR exposes progress directly. Per MDN, downloads fire `progress` events on the request, and uploads fire
the same events on `xhr.upload`:

```js
xhr.upload.onprogress = (event) => {
  if (event.lengthComputable) {
    console.log(`${Math.round((event.loaded / event.total) * 100)}% uploaded`);
  }
};
xhr.onprogress = (event) => { /* download progress */ };
```

(MDN's note: attach the listeners **before** calling `open()`, or the `progress` events will not fire.)
A download `progress` event did fire in a test. Progress bars for file uploads are a common reason
developers still reach for XHR. `fetch`, for its part, hands you the response body as a stream you can
read incrementally ([async-iterators-and-for-await.md](../advanced-async-patterns/async-iterators-and-for-await.md));
check current browser support before relying on streaming for upload progress.

To cancel, call `xhr.abort()`: the request stops, an `abort` event fires, and `status` is `0`. In the
test, `readyState` was `4` (DONE) inside the `abort` handler. The `fetch` equivalent is an
[`AbortController`](../advanced-async-patterns/cancellation-with-abortcontroller.md).

## ⚠️ Synchronous XHR

`open()`'s third argument, `async`, defaults to `true`. Passing `false` makes `send()` **block** until
the response arrives. MDN's guide notes that synchronous requests freeze the interface outside of
workers, which is why they are restricted to web workers. On the main thread they are a bug waiting to
happen: never write `xhr.open("GET", url, false)` there.

## 🆚 XHR vs. `fetch`

| | `XMLHttpRequest` | `fetch` |
|---|------------------|---------|
| Style | Events and callbacks | Promises (works with `async`/`await`) |
| HTTP error statuses | `load` with a 4xx/5xx `status` | Resolves; check `response.ok` |
| Network failure | `error` event, `status` 0 | Rejects with `TypeError` |
| Cancellation | `xhr.abort()` | `AbortController` signal |
| Progress events | Built in (`progress`, `xhr.upload`) | Response body is a readable stream |
| Response parsing | `responseType` + `response` | `response.json()`, `.text()`, `.blob()`, … |
| Integration | Older API | Designed alongside service workers and CORS |

Both are subject to the same browser security model: the same-origin policy and CORS apply to either.
For anything new, use `fetch`; read XHR fluently so you can maintain and migrate existing code.

## 🎤 Interview Angle

- **"What is AJAX?"** A technique, not a technology: making asynchronous HTTP requests from JavaScript
  and updating the page without a reload. Originally via `XMLHttpRequest`, now usually `fetch`.
- **"Walk me through an XHR request."** `new XMLHttpRequest()`, `open(method, url)`, optionally set
  headers and `responseType`, attach `onload`/`onerror`, then `send()`.
- **"What are the `readyState` values?"** 0 UNSENT, 1 OPENED, 2 HEADERS_RECEIVED, 3 LOADING, 4 DONE.
- **"Does a 404 trigger `onerror` (or reject a `fetch`)?"** No — it is a completed exchange with a 404
  status; check `status` / `response.ok`.
- **"XHR vs. `fetch`?"** `fetch` is promise-based and streaming-friendly; XHR is callback-based and has
  built-in upload/download progress events.

## Common Mistakes

- **Expecting `onerror` (or a rejection) for a 404 or 500.**
- **Calling `send()` before `open()`**, or setting headers before `open()`.
- **Attaching progress listeners after `open()`.**
- **Using synchronous XHR on the main thread.**
- **Forgetting that `status` is `0` on network failure and abort.**
- **Rewriting working XHR code to `fetch` without checking for features (progress events) it relied on.**

## Module Summary

Across this module: the **observer APIs** replace polling and scroll listeners — `IntersectionObserver`
for visibility, `MutationObserver` (microtask-batched) for DOM changes you don't control, and
`ResizeObserver` for element size (see
[intersection-mutation-and-resize-observers.md](intersection-mutation-and-resize-observers.md));
**`URL` and `URLSearchParams`** replace string-built URLs, while the **History API** changes the address
bar without reloading — `pushState` does not fire `popstate` (see
[url-and-history-apis.md](url-and-history-apis.md)); **`Blob`, `File`, object URLs, and the Clipboard
API** handle binary data and copy-and-paste, each with lifetime or permission rules (see
[files-blobs-and-clipboard.md](files-blobs-and-clipboard.md)); the **performance APIs** —
`performance.now()`, marks and measures, `PerformanceObserver`, navigation and paint timing — measure
real behavior (see [performance-apis.md](performance-apis.md)); **debouncing** (run after the calls stop)
and **throttling** (run at most once per interval) control event frequency (see
[debouncing-and-throttling.md](debouncing-and-throttling.md)); the **Constraint Validation API** and
`FormData` provide native form validation and value collection — useful, but never a security boundary
(see [forms-and-constraint-validation.md](forms-and-constraint-validation.md)); and **AJAX with
`XMLHttpRequest`** is the callback-based ancestor of `fetch`, still found in existing code (see this
file).

## ➡️ Next

Continue to the Offline Storage and Real-Time Web APIs module, the next module in this section, which
covers IndexedDB, service workers and the Cache API, WebSockets, and Server-Sent Events.
