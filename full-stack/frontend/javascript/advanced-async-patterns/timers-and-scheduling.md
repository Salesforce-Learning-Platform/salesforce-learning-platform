# ⏰ Timers and Scheduling

## Choosing *When* Code Runs

[web-apis.md](../event-loop/web-apis.md) and
[microtasks-and-macrotasks.md](../event-loop/microtasks-and-macrotasks.md) explained *how* the event
loop decides what runs next. This file is the practical side: the scheduling tools JavaScript gives
you, what each one actually guarantees, and the mistakes people make when they treat timers as
precise. As before, `delay(ms)` means `new Promise((resolve) => setTimeout(resolve, ms))`.

## ⏲️ `setTimeout`: A Minimum, Not a Promise

`setTimeout(fn, ms)` asks for `fn` to run **no sooner than** `ms` milliseconds from now. MDN lists why
it can run later:

- **Nesting clamp** — after about five levels of nested timeouts, browsers enforce a minimum 4 ms
  delay even for `0`.
- **Background-tab throttling** — inactive tabs get stricter delays (Firefox: at least one second;
  Chrome throttles progressively).
- **A busy main thread** — the callback cannot start until the code currently running finishes.

The last point is the most common in practice:

```js
const scheduled = performance.now();

setTimeout(() => {
  console.log(`ran ${Math.round(performance.now() - scheduled)} ms after scheduling`);
}, 0);

while (performance.now() - scheduled < 100) {}   // block the thread for 100 ms

// ran 100 (or a few more) ms after scheduling — a "0 ms" timer, delayed by the busy loop
```

Two more details from MDN: pass a **function**, never a string of code (a string is evaluated like
`eval` and is an XSS risk), and extra arguments after the delay are forwarded to the callback:
`setTimeout(fn, 1000, "arg")`. `clearTimeout(id)` cancels a pending timer.

## 🔁 `setInterval` and Why Recursive `setTimeout` Is Often Better

`setInterval(fn, ms)` queues `fn` every `ms` milliseconds. The pitfall is that it does **not wait for
the previous run to finish**. With synchronous callbacks that does not matter (they cannot overlap),
but with `async` work slower than the interval, runs pile up concurrently:

```js
let active = 0;
let maxActive = 0;
let started = 0;

const id = setInterval(async () => {
  started++;
  active++;
  maxActive = Math.max(maxActive, active);
  await delay(60);                  // work that takes three times as long as the interval
  active--;
}, 20);

await delay(130);
clearInterval(id);
await delay(80);

console.log({ started, maxActive });   // { started: 6, maxActive: 3 } — three runs in flight at once
```

Polling code almost always wants the opposite: "run, finish, *then* wait." A loop that awaits the
work and then the delay can never overlap, and stops cleanly with an
[`AbortSignal`](cancellation-with-abortcontroller.md):

```js
async function poll(task, intervalMs, { signal }) {
  while (!signal.aborted) {
    await task();                      // finish the work first…
    await delay(intervalMs);           // …then wait; runs can never overlap
  }
}

let active = 0;
let maxActive = 0;
let runs = 0;
const controller = new AbortController();
setTimeout(() => controller.abort(), 250);

await poll(async () => {
  runs++;
  active++;
  maxActive = Math.max(maxActive, active);
  await delay(60);
  active--;
}, 20, { signal: controller.signal });

console.log({ runs, maxActive });      // { runs: 4, maxActive: 1 }
```

Because timers drift (each run starts after the previous one *plus* delays), neither approach is
suitable for precise clocks. Measure elapsed time with `performance.now()` or `Date.now()` instead of
counting ticks.

## 🎞️ `requestAnimationFrame`: Timing Tied to the Screen

For visual updates, use `requestAnimationFrame(callback)`. Per MDN, it runs the callback **just
before the next repaint**, passes it a high-resolution timestamp, pauses automatically in background
tabs, and fires once — call it again inside the callback to keep animating.

```js
requestAnimationFrame((timestamp) => {
  // update the DOM or canvas here; `timestamp` is in milliseconds
});
```

The refresh rate is not always 60 Hz. Recording six consecutive callbacks on the test machine's
display gave these gaps between frames:

```
12.5, 8.3, 8.4, 8.3, 8.3   (milliseconds — a display refreshing at roughly 120 Hz)
```

MDN's advice follows directly: compute animation progress from the **timestamp**, not from "one step
per call," or the animation runs twice as fast on a 120 Hz screen. Cancel with
`cancelAnimationFrame(id)`.

## 🔬 Microtasks: `queueMicrotask` and Promise Callbacks

`queueMicrotask(fn)` runs `fn` after the current task finishes but before the event loop moves on to
timers or rendering. Promise callbacks use the same microtask queue, so they run in the order they
were queued:

```js
const order = [];

order.push("1 sync");
setTimeout(() => order.push("5 timeout"), 0);
queueMicrotask(() => order.push("3 queueMicrotask"));
Promise.resolve().then(() => order.push("4 promise.then"));
order.push("2 sync");

await delay(20);
console.log(order);
// [ '1 sync', '2 sync', '3 queueMicrotask', '4 promise.then', '5 timeout' ]
```

In the browser the order was the same, with a `requestAnimationFrame` callback arriving after the
timeout in that run (`rAF` waits for the next frame, so its position relative to a timer varies).
Use `queueMicrotask` to defer work to the end of the current task without waiting for a timer; just
remember the warning from the event-loop module — microtasks that keep queueing more microtasks
starve everything else.

## 😴 `requestIdleCallback`: Work for Quiet Moments

`requestIdleCallback(fn, { timeout })` runs low-priority work when the browser has spare time; the
callback receives a deadline object whose `timeRemaining()` tells you how much of the idle period is
left. MDN marks it as **limited availability** — Safari does not support it — so feature-detect and
fall back:

```js
const whenIdle = globalThis.requestIdleCallback
  ? (fn, options) => requestIdleCallback(fn, options)
  : (fn) => setTimeout(() => fn({ didTimeout: false, timeRemaining: () => 0 }), 1);

whenIdle((deadline) => {
  // analytics, prefetching, cache warm-up: nothing the user is waiting on
}, { timeout: 2000 });
```

Give it a `timeout` if the work must eventually happen even on a busy page.

## 🍰 Keeping a Page Responsive: Slice Long Work

A long synchronous loop blocks everything — timers, input, rendering — because the event loop only
runs between tasks. If work cannot move off the main thread (see
[web-workers.md](web-workers.md)), cut it into slices and **yield** between them. This script runs
the same total computation two ways while a 5 ms "heartbeat" interval counts how often the event loop
got a turn:

```js
const work = (n) => {
  let sum = 0;
  for (let i = 0; i < n; i++) sum += Math.sqrt(i);
  return sum;
};

async function countTicks(job) {
  let ticks = 0;
  const id = setInterval(() => ticks++, 5);          // a heartbeat that needs the event loop
  await new Promise((resolve) => setTimeout(resolve, 0));
  const start = performance.now();
  await job();
  const ms = Math.round(performance.now() - start);
  clearInterval(id);
  return { ticks, ms };
}

console.log("blocking:", await countTicks(async () => {
  work(3e7);                                          // one long, uninterrupted task
}));

console.log("chunked: ", await countTicks(async () => {
  for (let i = 0; i < 30; i++) {
    work(1e6);                                        // the same total work, in 30 slices
    await new Promise((resolve) => setTimeout(resolve, 0));   // yield to the event loop
  }
}));

// blocking: { ticks: 0, ms: 21 }
// chunked:  { ticks: 10, ms: 54 }
```

The blocked version finished sooner overall but the heartbeat — standing in for clicks, scrolling, and
repaints — got **zero** turns. The chunked version took about two and a half times longer in total,
yet stayed responsive. (Numbers vary by machine; the zero is the point.) Chunking trades throughput
for responsiveness.

## 🟢 Node.js Extras: `setImmediate` and `process.nextTick`

Node adds two scheduling functions. The Node guide describes `process.nextTick` as "not technically
part of the event loop": its queue is drained after the current operation finishes, before the loop
continues, and recursive `nextTick` calls can starve I/O. `setImmediate` runs in the loop's *check*
phase, right after I/O polling. Observed order of all four from a script's top level:

```
sync
nextTick
promise
setTimeout 0
setImmediate
```

Treat the tail of that list with care: the guide states that from the main module the order of
`setTimeout(fn, 0)` and `setImmediate(fn)` is **non-deterministic** (it depends on process
performance), while inside an I/O callback `setImmediate` always runs first. Prefer promises and
`queueMicrotask` unless you specifically need Node's phases. Debouncing and throttling — rate-limiting
callbacks built on these timers — are covered in the Browser APIs in Depth module, later in this
section.

## 🎤 Interview Angle

- **"What does `setTimeout(fn, 0)` do?"** Schedules `fn` as a task to run after the current code and
  any queued microtasks, no sooner than the delay (clamped to a minimum in browsers) — never "now."
- **"What is the order: sync, `setTimeout 0`, `Promise.then`, `queueMicrotask`?"** Sync code first,
  then microtasks in queue order (`queueMicrotask` and `.then` together), then the timer.
- **"Why is `setInterval` unreliable for async work?"** It does not wait for the previous run, so
  slow async callbacks overlap; use a loop that awaits the work and then the delay.
- **"`requestAnimationFrame` vs. `setTimeout` for animation?"** `rAF` syncs with the display and
  pauses in background tabs; `setTimeout` knows nothing about repaints.

## Common Mistakes

- **Treating a timer's delay as exact** or expecting `setTimeout(fn, 0)` to run immediately.
- **Using `setInterval` with `async` callbacks** that can outlast the interval.
- **Tying animation speed to the number of frames** instead of elapsed time.
- **Assuming `requestIdleCallback` exists everywhere.**
- **Running long synchronous loops on the main thread** and wondering why the page froze.
- **Forgetting `clearTimeout`/`clearInterval`** — leaked timers keep callbacks (and what they
  reference) alive.

## ➡️ Next

Continue to [web-workers.md](web-workers.md) to move heavy computation off the main thread entirely.
