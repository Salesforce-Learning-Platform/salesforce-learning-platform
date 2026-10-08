# 🕳️ Finding and Fixing Memory Leaks

## What a Leak Actually Is

In a garbage-collected language a leak is not memory the program forgot to free — the collector frees
what it can. A **leak is memory that is still *reachable* but no longer *needed***: something holds a
reference you forgot about, so the collector must keep the object alive
([memory-management-and-garbage-collection.md](memory-management-and-garbage-collection.md)). Leaks show up
as memory that climbs steadily, a page that gets sluggish over a long session, or a server that is
eventually killed for running out of memory.

Every cause below is the same mistake in different clothing: **a long-lived thing references a
short-lived thing.**

## 🔎 The Usual Suspects (Each Reproduced)

All numbers below come from real runs in Node.js with forced collections, so `heapUsed` reflects live
objects rather than uncollected garbage.

### 1. Unbounded caches and collections

A module-level `Map` that only ever grows is the single most common server-side leak. Adding entries and
collecting after each round:

```js
const cache = new Map();
for (let round = 1; round <= 4; round++) {
  for (let i = 0; i < 50_000; i++) cache.set(`key-${round}-${i}`, new Array(20).fill(round));
  global.gc();
  console.log(`${round * 50_000} entries -> ${heapMB()} MB`);
}
// 50000 entries -> 17 MB | 100000 -> 30 MB | 150000 -> 45 MB | 200000 -> 56 MB
```

Memory grows with every entry even though a collection runs each round — every entry is reachable through
`cache`. The fix is to **bound it**. A small least-recently-used (LRU) cache evicts the oldest entry
(a `Map` iterates in insertion order, which makes this easy; see
[map-and-set.md](../built-in-objects-and-collections/map-and-set.md) and the memoization version in
[memoization.md](../functional-javascript/memoization.md)):

```js
function lru(limit) {
  const map = new Map();
  return {
    set(key, value) {
      map.delete(key);                             // refresh recency
      map.set(key, value);
      if (map.size > limit) map.delete(map.keys().next().value);   // evict the oldest
    },
    get size() { return map.size; },
  };
}
// 50000 inserted, 10000 kept -> 7 MB | 100000 inserted -> 7 MB | 150000 -> 7 MB | 200000 -> 7 MB
```

Flat at 7 MB regardless of how much passes through. If the cache is keyed by *objects*, use a `WeakMap`
instead ([weakmap-weakset-and-weakref.md](../built-in-objects-and-collections/weakmap-weakset-and-weakref.md)).

### 2. Timers that are never cleared

An active `setInterval` keeps its callback alive, and the callback keeps everything it captured alive:

```js
function startPolling() {
  const payload = { data: new Array(1000).fill("x") };
  const id = setInterval(() => payload.data.length, 1000);
  return { id, ref: new WeakRef(payload) };
}

const { id, ref } = startPolling();
// after a GC:   ref.deref() !== undefined   -> true: the running interval keeps `payload` alive
clearInterval(id);
// after a GC:   ref.deref() === undefined   -> true: once the timer is cleared, `payload` is collected
```

Every `setInterval` and `setTimeout` needs a matching `clear…` when its owner goes away.

### 3. Event listeners that are never removed

Each `addEventListener` (or `emitter.on`) stores your handler — and its closure — on the target. In Node,
`EventEmitter` even warns you: its default limit is 10 listeners per event, and adding an eleventh prints

```
MaxListenersExceededWarning: Possible EventEmitter memory leak detected.
11 data listeners added to [EventEmitter]. MaxListeners is 10. Use emitter.setMaxListeners() to increase limit
```

The warning does not stop anything (the listener is still added) — it is a smell test. Do not silence it
with `setMaxListeners` before understanding why so many listeners accumulate. In the browser there is no
warning, so the discipline is yours: remove what you add. The cleanest approach pairs every
subscription with one teardown, using an `AbortController` signal for listeners
([cancellation-with-abortcontroller.md](../advanced-async-patterns/cancellation-with-abortcontroller.md)):

```js
function mount() {
  const controller = new AbortController();
  window.addEventListener("resize", onResize, { signal: controller.signal });
  window.addEventListener("online", onOnline, { signal: controller.signal });
  const timer = setInterval(tick, 1000);

  return function unmount() {          // call this when the component goes away
    controller.abort();                // removes BOTH listeners
    clearInterval(timer);
  };
}
```

### 4. Closures that capture more than they need

A closure keeps alive the variables it *references*. When V8 can see a large local is not referenced by
any closure, it can free it; reference it from the closure and it stays:

```js
function makeHandler() {
  const huge = new Array(1_000_000).fill(1);
  const summary = huge.length;
  return () => summary;                 // captures only `summary`
}
// heapUsed after holding this handler: 4 MB — `huge` could be freed

function makeBadHandler() {
  const huge = new Array(1_000_000).fill(1);
  return () => huge.length;             // captures `huge` itself
}
// heapUsed after holding this handler: 11 MB — `huge` stays alive as long as the handler does
```

Compute what you need up front and capture the small result, not the large source.

### 5. Detached DOM nodes (browser)

Removing an element from the page does not free it if JavaScript still references it. Chrome DevTools'
Memory panel documents this: filtering a heap snapshot for **"Detached"** reveals DOM trees that were
removed from the page but are still referenced by JavaScript, so they cannot be collected. The usual
culprits are a cached `querySelector` result, a listener closure that captured the element, or an array of
"previously rendered" nodes. Drop those references when you remove the node.

### 6. Accidental globals and forgotten module state

An assignment to an undeclared variable creates a global (in sloppy mode) that lives for the whole page —
[strict-mode.md](../execution-context-and-hoisting/strict-mode.md) turns it into an error. Likewise any
array, map, or object hanging off a module that never shrinks is effectively global.

## 🧰 Finding the Leak

**Confirm there is one.** Watch memory over time under steady load: a sawtooth that returns to a stable
baseline after each collection is healthy; a baseline that keeps rising is a leak. In Node, log
`process.memoryUsage().heapUsed` periodically; in production, graph process memory with an alert
([Monitoring and Observability](../../../production-systems/monitoring-and-observability/)).

**Find what is retaining memory — heap snapshots.** A heap snapshot is a dump of every live object and
what references it. The workflow that works:

1. Load the page (or start the process) and do the suspect action *once* so one-time setup is out of the way.
2. Take a snapshot.
3. Repeat the suspect action many times — open and close the dialog, navigate away and back, send many requests.
4. Take another snapshot and compare: which object types increased in count, and what is holding them?

In the browser, Chrome's Memory panel provides heap snapshots, **allocation timelines** (blue bars mark
new allocations that are still alive), and **allocation sampling** by function. In Node.js:

- `v8.writeHeapSnapshot()` writes a `.heapsnapshot` file (a JSON document with `snapshot`, `nodes`,
  `edges`, and `strings` sections, as a test confirmed) that you open in Chrome DevTools.
- `node --heapsnapshot-signal=SIGUSR2 app.js` writes one when the process receives that signal, which is
  how you capture a snapshot from a running service.
- **Cost warning from the Node docs:** taking a snapshot needs roughly twice the heap's current size in
  memory and is synchronous, blocking the event loop — be careful doing it on a production process that is
  already close to its limit.
- `v8.getHeapStatistics()` includes `number_of_detached_contexts`; the Node docs note a non-zero value can
  indicate a potential leak.

**Read the retainers.** In a snapshot, pick a leaked object and follow its *retainer path* up to a root.
That chain — "global → cache Map → array → entry" — names the reference you must cut.

## 🛠️ Fix Patterns

| Cause | Fix |
|-------|-----|
| Unbounded cache | Bound it (LRU / max size / TTL), or key it weakly (`WeakMap`) |
| Timer | Store the id; `clearInterval`/`clearTimeout` on teardown |
| Listener | Remove it, or add it with an `AbortController` signal and abort on teardown |
| Closure over big data | Capture only the small values you need |
| Detached DOM | Null out references when removing nodes |
| Global/module state | Use scoped variables; reset or bound shared collections |
| Subscriptions (stores, sockets, observers) | Always return and call an unsubscribe/disconnect function |

The preventive habit behind every row: **whenever you write the line that starts something, write the
line that stops it in the same place.**

## 🎤 Interview Angle

- **"What is a memory leak in a garbage-collected language?"** Memory that is still reachable but no
  longer needed, so the collector cannot free it.
- **"Name common causes."** Unbounded caches, uncleared timers, unremoved event listeners, closures
  capturing large data, detached DOM nodes, accidental globals.
- **"How would you debug one?"** Confirm rising baseline memory, take heap snapshots before and after
  repeating the suspect action, compare, and follow retainer paths to the root.
- **"What does the Node `MaxListenersExceededWarning` mean?"** More than 10 listeners were added for an
  event — a possible leak from listeners that are never removed.

## Common Mistakes

- **Silencing `MaxListenersExceededWarning`** instead of finding the missing `off`.
- **Debugging by reading one `heapUsed` number.**
- **Taking a heap snapshot on a nearly full production process.**
- **Adding "cleanup" code for the wrong reference** — follow the retainer path first.
- **Treating `null`-ing variables as the fix** when the real holder is a cache, timer, or listener.

## ➡️ Next

Continue to [transpilers-polyfills-and-browser-support.md](transpilers-polyfills-and-browser-support.md)
to see how code written with modern features is made to run in environments that don't support them.
