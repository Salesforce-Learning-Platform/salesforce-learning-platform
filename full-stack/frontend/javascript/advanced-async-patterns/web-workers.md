# 🧵 Web Workers

## Real Parallelism for Heavy Work

JavaScript runs your code on a single thread, and
[timers-and-scheduling.md](timers-and-scheduling.md) showed the consequence: one long computation
freezes the page. Slicing the work helps, but it still competes with rendering and input. A
**Web Worker** is the real fix: a script that runs on a **separate thread** with its own event loop,
so heavy computation proceeds while the main thread keeps handling the user.

## 🧱 The Model

Per MDN's guide, a dedicated worker is a background thread started by a single script. The rules that
shape every worker program:

- **No DOM.** A worker cannot touch `document` or most `window` properties. It can use `fetch`,
  timers, and the standard built-ins (`Array`, `Math`, `Date`, …).
- **Own global scope.** Inside a worker, the global is `self`, a `DedicatedWorkerGlobalScope`.
- **Message passing only.** Threads communicate with `postMessage` and the `message` event.
- **Data is copied, not shared.** Messages are duplicated with the structured clone algorithm.

Checked inside a worker in a real browser:

```js
typeof document;        // "undefined"
typeof window;          // "undefined"
self.constructor.name;  // "DedicatedWorkerGlobalScope"
typeof fetch;           // "function"
typeof setTimeout;      // "function"
```

## 🚀 A First Worker

Two files — the page, and the worker:

```js
// main.js
const worker = new Worker("worker.js");

worker.postMessage({ limit: 3_000_000 });             // send work

worker.onmessage = (event) => {
  console.log(`primes found: ${event.data.count}`);   // receive the result
};
```

```js
// worker.js
self.onmessage = (event) => {
  const { limit } = event.data;
  let count = 0;
  for (let n = 2; n < limit; n++) {
    let isPrime = true;
    for (let i = 2; i * i <= n; i++) {
      if (n % i === 0) { isPrime = false; break; }
    }
    if (isPrime) count++;
  }
  self.postMessage({ count });                        // send the answer back
};
```

For a single-file demo, a worker can be built from a `Blob` URL instead of a separate file:

```js
const source = `self.onmessage = (e) => self.postMessage(e.data * 2);`;
const url = URL.createObjectURL(new Blob([source], { type: "text/javascript" }));
const worker = new Worker(url);
```

In a bundler-based project, MDN recommends the form
`new Worker(new URL("worker.js", import.meta.url))` so the bundler can find and build the worker
file; add `{ type: "module" }` to use `import` inside the worker.

### Does It Actually Help? Measured

In a browser, counting primes below 3,000,000 gave the same answer — 216,816 — both ways, in similar
time (about 340–365 ms), while a 10 ms main-thread timer measured how responsive the page stayed:

```
main thread, blocking:   337 ms of work,   0 timer ticks during it   ← page frozen
in a worker:             365 ms of work,  36 timer ticks during it   ← page responsive
```

The worker is not faster — it is *non-blocking*. Animations, scrolling, and clicks keep working while
it runs.

## 📦 Copy, Move, or Share

Data crossing the boundary is cloned by default, which has two consequences.

**Changes do not cross over.** The worker gets its own copy:

```js
const original = { n: 1 };
worker.postMessage({ obj: original });      // the worker sets obj.changed = true on ITS copy
// original is still { n: 1 }; the worker's copy was { n: 1, changed: true }
```

**Not everything can be cloned.** Functions, DOM nodes, and similar values throw a `DataCloneError`:

```js
worker.postMessage({ fn: () => 1 });
// DataCloneError: Failed to execute 'postMessage' on 'Worker': () => 1 could not be cloned.
```

(See [copying-objects-shallow-vs-deep.md](../objects-in-depth/copying-objects-shallow-vs-deep.md) for
what the structured clone algorithm supports.)

Copying a large buffer is wasteful. **Transferable objects** are *moved* instead of copied — zero-copy,
with ownership passing to the worker. MDN lists `ArrayBuffer`, `MessagePort`, `ImageBitmap`,
`OffscreenCanvas`, and streams among them (typed arrays themselves are not transferable, but their
underlying buffer is):

```js
const buffer = new ArrayBuffer(8);
worker.postMessage({ buffer }, [buffer]);   // second argument: the list of things to transfer

console.log(buffer.byteLength);             // 0 — the original is now detached and unusable here
// the worker saw byteLength 8 and could read and write the data
```

Without the transfer list the buffer is cloned and the original is untouched
(`byteLength` stays 8). For genuinely *shared* memory, `SharedArrayBuffer` exists, but MDN notes it
requires the page to be **cross-origin isolated**, and it brings real concurrency hazards — treat it as
an advanced tool. For more on buffers see
[typed-arrays-and-binary-data.md](../built-in-objects-and-collections/typed-arrays-and-binary-data.md).

## 💥 Errors and Shutdown

An uncaught error inside a worker is reported on the worker object as an `error` event; the worker
itself does not crash the page:

```js
worker.addEventListener("error", (event) => {
  console.log(event.message);               // Uncaught Error: worker exploded
  event.preventDefault();                   // suppress the console error if you've handled it
});
```

Stop a worker you no longer need with `worker.terminate()` — an idle worker still holds a thread and
memory. From inside the worker, `self.close()` does the same.

## 🔌 Giving a Worker a Promise API

Raw `postMessage` is event-based. Wrapping a request in a promise makes a worker feel like any other
async function:

```js
function request(worker, data) {
  return new Promise((resolve, reject) => {
    const cleanup = () => {
      worker.removeEventListener("message", onMessage);
      worker.removeEventListener("error", onError);
    };
    const onMessage = (event) => { cleanup(); resolve(event.data); };
    const onError = (event) => { cleanup(); reject(new Error(event.message)); };

    worker.addEventListener("message", onMessage);
    worker.addEventListener("error", onError);
    worker.postMessage(data);
  });
}

const { count } = await request(worker, { limit: 3_000_000 });
```

This version assumes one request in flight at a time. To run several concurrently, include an `id` in
each message and have the worker echo it back so replies can be matched to their requests.

## ✅ When to Use a Worker

| Good fit | Poor fit |
|----------|----------|
| Parsing or transforming large data (CSV, JSON, images) | Waiting on the network — `fetch` is already asynchronous |
| Compression, hashing, cryptography, search indexing | Tiny tasks — messaging and startup cost more than the work |
| Physics, simulation, or heavy layout math | Anything that must touch the DOM |
| Keeping a UI smooth during unavoidable CPU work | Code that needs shared mutable state with the page |

Other kinds exist: **shared workers** serve several pages at once, and **service workers** sit
between the page and the network for offline support and caching — the subject of the Offline Storage
and Real-Time Web APIs module, later in this section. Node.js has its own `worker_threads` module for
the same purpose with a different API.

## 🎤 Interview Angle

- **"JavaScript is single-threaded — so how can workers exist?"** The *language* has no shared-state
  threading model; a worker is a separate JavaScript environment with its own event loop that
  communicates only by messages.
- **"How do the main thread and a worker share data?"** By copying (structured clone), by
  transferring ownership of transferable objects, or — with cross-origin isolation — via a
  `SharedArrayBuffer`.
- **"What can't a worker do?"** Access the DOM or `window`.
- **"When is a worker *not* worth it?"** For I/O-bound work and tiny tasks.

## Common Mistakes

- **Moving I/O-bound work into a worker** — `fetch` already doesn't block.
- **Posting functions or DOM nodes**, which cannot be cloned.
- **Copying huge buffers repeatedly** instead of transferring them.
- **Using a transferred buffer afterwards** — it is detached (length 0).
- **Forgetting `terminate()`** and leaking threads.
- **Expecting a worker to make the same computation faster** — it makes the page *responsive*; speed
  needs more cores (several workers) or a better algorithm.

## ➡️ Next

Continue to [handling-unhandled-rejections.md](handling-unhandled-rejections.md) to close the module
with what happens when an async error has nobody to catch it.
