# ⚡ Advanced Asynchronous Patterns

## 📚 Overview

This module builds on [promises](../asynchronous-programming-and-modules/promises.md),
[async/await](../asynchronous-programming-and-modules/async-await.md), and the
[event loop](../event-loop/) with the techniques production code relies on: the exact semantics of
the promise combinators and the concurrency-limit, timeout, and retry patterns built from them;
genuine cancellation with `AbortController`; async iterators for sequences that arrive over time;
the scheduling tools and what they really guarantee; Web Workers for off-main-thread work; and the
handling of rejections nobody caught.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Choose among `Promise.all`, `allSettled`, `race`, and `any`, state their exact settle rules, and
  build a concurrency-limited task runner, a timeout wrapper, and a retry-with-backoff helper.
- Cancel `fetch` and your own async functions with `AbortController`, `AbortSignal.timeout()`, and
  `AbortSignal.any()`, and tell `AbortError` from `TimeoutError`.
- Write async generators and consume them with `for await…of`, including paginated and streamed data.
- Explain the guarantees (and non-guarantees) of `setTimeout`, `setInterval`, `requestAnimationFrame`,
  `queueMicrotask`, and `requestIdleCallback`, and keep a page responsive with chunked work.
- Move CPU-heavy work into a Web Worker, and choose between copying, transferring, and sharing data.
- Explain how browsers and Node.js treat unhandled rejections, and prevent them.

## 📋 Prerequisites

- [Promises](../asynchronous-programming-and-modules/promises.md) and [Async/Await](../asynchronous-programming-and-modules/async-await.md) — this module assumes their basics.
- [The Event Loop](../event-loop/) — microtasks, macrotasks, and Web APIs underlie every file here.
- [Iterators and Generators](../additional-javascript-topics/iterators-and-generators.md) — async iteration extends the synchronous protocol.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [promise-combinators-in-depth.md](promise-combinators-in-depth.md) | Exact semantics of `all`, `allSettled`, `race`, `any`; concurrency pools, timeouts, retries |
| [cancellation-with-abortcontroller.md](cancellation-with-abortcontroller.md) | Cooperative cancellation, timeout and combined signals, cancellable functions, listener cleanup |
| [async-iterators-and-for-await.md](async-iterators-and-for-await.md) | The async iteration protocol, async generators, backpressure, and streamed responses |
| [timers-and-scheduling.md](timers-and-scheduling.md) | Timer guarantees, `setInterval` overlap, animation frames, microtasks, idle callbacks, chunking |
| [web-workers.md](web-workers.md) | Worker model, messaging, transferables, errors, and when to use them |
| [handling-unhandled-rejections.md](handling-unhandled-rejections.md) | Browser and Node behavior, common sources, prevention; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you are preparing for interviews or building anything that talks to a network:
"implement a concurrency limit", "how do you cancel a fetch", "order of `setTimeout` and promises",
and "what happens to an unhandled rejection" are all standard questions, and each has a verified,
worked answer here.

**Skim** the Web Workers file unless you have CPU-heavy work in the browser — but read its
"when to use a worker" table, and read the unhandled-rejections file regardless: async handlers that
fail silently are among the most common production bugs.

## 🧠 Knowledge Check

<details>
<summary>What is the difference between <code>Promise.race</code> and <code>Promise.any</code>?</summary>

`Promise.race` settles with the first promise to settle, whether it fulfills or rejects, so a fast
failure wins. `Promise.any` waits for the first promise to **fulfill** and ignores rejections until
then; it rejects (with an `AggregateError` listing every reason) only if all inputs reject.

</details>

<details>
<summary>Why doesn't wrapping a slow operation in <code>Promise.race([operation, timeout])</code> cancel it?</summary>

`race` only decides which result *you* receive. The losing promise keeps running to completion —
network request, side effects, and all. To actually stop the work, pass the operation an
`AbortSignal` (for example `AbortSignal.timeout(ms)` with `fetch`) so the operation cancels itself.

</details>

## 📚 References

- [MDN: `Promise`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) and [`Promise.any()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/any) — concurrency method semantics, and [`Promise.withResolvers()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/withResolvers).
- [MDN: `AbortController`](https://developer.mozilla.org/en-US/docs/Web/API/AbortController) and [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal) — cancellation, `timeout()`, `any()`, and error names.
- [MDN: `for await…of`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of), [`async function*`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function*), [`Array.fromAsync()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/fromAsync), and [`ReadableStream`](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream) — async iteration.
- [MDN: `setTimeout()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout), [`requestAnimationFrame()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame), [`requestIdleCallback()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback), and [`queueMicrotask()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/queueMicrotask) — scheduling APIs.
- [MDN: Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) and [Transferable objects](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Transferable_objects) — the worker model and zero-copy transfer.
- [MDN: `unhandledrejection` event](https://developer.mozilla.org/en-US/docs/Web/API/Window/unhandledrejection_event) — browser behavior.
- [Node.js: `process` events](https://nodejs.org/api/process.html), [CLI `--unhandled-rejections`](https://nodejs.org/api/cli.html), and [the event loop, timers, and `process.nextTick()`](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) — Node behavior.
- [typescript-eslint: `no-floating-promises`](https://typescript-eslint.io/rules/no-floating-promises/) and [ESLint: `no-async-promise-executor`](https://eslint.org/docs/latest/rules/no-async-promise-executor) — lint rules that prevent unhandled rejections.
- [javascript.info: Promise API](https://javascript.info/promise-api), [Fetch: Abort](https://javascript.info/fetch-abort), [Async iteration and generators](https://javascript.info/async-iterators-generators), and [Scheduling: setTimeout and setInterval](https://javascript.info/settimeout-setinterval) — widely used walkthroughs.
- [W3Schools: JavaScript Asynchronous Programming](https://www.w3schools.com/js/js_async.asp) — a beginner-friendly overview.

## ➡️ Continue Your Learning Path

Continue to the Browser APIs in Depth module, the next module in this section, which covers the
observer APIs, URL and History, files and the clipboard, performance measurement, and the
debouncing and throttling that tame event-driven code.
