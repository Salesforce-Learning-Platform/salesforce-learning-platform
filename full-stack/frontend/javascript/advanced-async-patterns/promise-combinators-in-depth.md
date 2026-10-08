# 🧮 Promise Combinators in Depth

## Beyond the Short Table

[promises.md](../asynchronous-programming-and-modules/promises.md) introduced `Promise.all`,
`Promise.allSettled`, and `Promise.race` in a short table, and
[async-await.md](../asynchronous-programming-and-modules/async-await.md) showed `Promise.all` as the
fix for needlessly sequential `await`s. This file pins down the exact semantics of all four
combinators (adding `Promise.any`), then builds the patterns real code needs on top of them: running
tasks with a **concurrency limit**, adding **timeouts**, and **retrying** failures.

The examples use two tiny helpers:

```js
const delay = (ms, value) => new Promise((resolve) => setTimeout(resolve, ms, value));
const fail = (ms, message) =>
  new Promise((_, reject) => setTimeout(() => reject(new Error(message)), ms));
```

## 📋 The Four Combinators, Precisely

| Method | Fulfills when | Rejects when | Result | Empty input |
|--------|---------------|--------------|--------|-------------|
| `Promise.all` | **all** input promises fulfill | **any** rejects (the first rejection) | Array of values, in **input order** | Fulfills with `[]` |
| `Promise.allSettled` | **all** have settled | **never** | Array of outcome objects | Fulfills with `[]` |
| `Promise.race` | the **first to settle** fulfills | the first to settle rejects | That first outcome | **Stays pending forever** |
| `Promise.any` | the **first to fulfill** | **all** reject, with an `AggregateError` | The first fulfilled value | Rejects with an `AggregateError` |

These match MDN's "Promise concurrency" reference. Each combinator accepts any iterable, and
non-promise values are treated as already-fulfilled.

### `all`: results in input order, rejection on the first failure

```js
console.log(await Promise.all([delay(60, "slow"), delay(20, "fast")]));
// [ 'slow', 'fast' ]  — input order, not completion order; takes about 60 ms

console.log(await Promise.all([1, Promise.resolve(2), delay(10, 3)]));
// [ 1, 2, 3 ]         — plain values are fine

console.log(await Promise.all([]));
// []                  — empty input fulfills immediately
```

It is **fail-fast**: the returned promise rejects as soon as any input rejects, without waiting for
the others.

```js
try {
  await Promise.all([delay(50, "a"), fail(20, "boom"), delay(80, "c")]);
} catch (error) {
  console.log(error.message);   // boom — at about 20 ms; the other two keep running, unobserved
}
```

Rejections that arrive *after* the first are not reported as unhandled: `Promise.all` attaches a
handler to every input. The in-flight work is not cancelled, though (see
[cancellation-with-abortcontroller.md](cancellation-with-abortcontroller.md)).

### `allSettled`: wait for everything, never throw

```js
console.log(await Promise.allSettled([delay(10, "ok"), fail(20, "bad")]));
// [
//   { status: 'fulfilled', value: 'ok' },
//   { status: 'rejected', reason: Error: bad ... }
// ]
```

Use it when partial success is acceptable — for example loading several independent dashboard
panels, where one failure should not blank the others. Inspect each `status` yourself.

### `race`: the first to settle wins — even if it is a failure

```js
console.log(await Promise.race([delay(30, "a"), delay(10, "b")]));   // b

try {
  await Promise.race([delay(50, "slow"), fail(10, "fast fail")]);
} catch (error) {
  console.log(error.message);   // fast fail — a rejection that settles first wins
}
```

An empty `race` never settles, which is a classic way to hang a program:

```js
console.log(await Promise.race([Promise.race([]), delay(30, "timer won")]));   // timer won
```

### `any`: the first success wins

`Promise.any` ignores rejections until something fulfills — the opposite emphasis from `race`:

```js
console.log(await Promise.any([fail(10, "x"), delay(30, "winner")]));   // winner
```

Only when **every** input rejects does it reject, with an `AggregateError` whose `errors` array
holds the reasons in input order:

```js
try {
  await Promise.any([fail(10, "x"), fail(20, "y")]);
} catch (error) {
  console.log(error.name);                      // AggregateError
  console.log(error.message);                   // All promises were rejected
  console.log(error.errors.map((e) => e.message));   // [ 'x', 'y' ]
  console.log(error instanceof AggregateError); // true
}
```

A typical use is racing redundant sources — several mirrors of the same resource — and taking the
first that works.

## ⏱️ A Promise Starts When It Is *Created*

Passing promises to `Promise.all` does not start them; they were already running. What matters is
when you *create* them:

```js
// Sequential: the second delay starts only after the first finishes — about 80 ms
await delay(40);
await delay(40);

// Created together: both timers run at once — about 40 ms
const a = delay(40);
const b = delay(40);
await a;
await b;
```

## 🪤 The `forEach(async …)` Trap

`forEach` ignores the promises its callback returns, so nothing waits for them:

```js
const done = [];
[1, 2, 3].forEach(async (n) => {
  await delay(20);
  done.push(n);
});
console.log(done);   // []  — forEach returned long before any callback finished
await delay(50);
console.log(done);   // [ 1, 2, 3 ]
```

To run the items concurrently and wait for all of them, map to promises and combine them. To run
them one at a time, use a `for...of` loop with `await`:

```js
const doubled = await Promise.all([1, 2, 3].map(async (n) => {
  await delay(20);
  return n * 2;
}));
console.log(doubled);   // [ 2, 4, 6 ] — about 20 ms total, results in input order
```

## 🚦 Limiting Concurrency

`Promise.all(items.map(task))` starts *everything at once*. With thousands of items — API calls,
file reads — that can overwhelm a server or exhaust sockets. A **worker pool** runs at most `limit`
tasks at a time:

```js
async function mapLimit(items, limit, fn) {
  const results = new Array(items.length);
  let next = 0;

  async function worker() {
    while (next < items.length) {
      const index = next++;                      // claim the next item (safe: no await in between)
      results[index] = await fn(items[index], index);
    }
  }

  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}
```

Each of the `limit` workers repeatedly claims the next unclaimed index, so results land in input
order. Instrumenting it confirms the cap:

```js
let running = 0;
let maxRunning = 0;

const square = async (n) => {
  running++;
  maxRunning = Math.max(maxRunning, running);
  await delay(20 + (n % 3) * 10);
  running--;
  return n * n;
};

console.log(await mapLimit([1, 2, 3, 4, 5, 6, 7, 8], 3, square));
// [ 1, 4, 9, 16, 25, 36, 49, 64 ]
console.log(maxRunning);   // 3
```

### Failure behavior needs a decision

In that version, if one task throws, `Promise.all` rejects — but the other workers keep claiming and
running the remaining items. Run with a limit of 2 and a task that fails on item 2, and all eight
items still start. To stop scheduling new work after the first failure, add a flag:

```js
async function mapLimitStop(items, limit, fn) {
  const results = new Array(items.length);
  let next = 0;
  let failed = false;

  async function worker() {
    while (!failed && next < items.length) {
      const index = next++;
      try {
        results[index] = await fn(items[index], index);
      } catch (error) {
        failed = true;                          // tell the other workers to stop claiming items
        throw error;
      }
    }
  }

  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}
```

With the same failing task, only items 1, 2, and 3 start. (Tasks already running still finish —
stopping *them* needs cancellation.)

## ⏳ Timeouts with `race` — and Their Limit

A timeout is a race between the real work and a timer. Clear the timer afterwards so it does not keep
the program alive:

```js
function withTimeout(promise, ms) {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`Timed out after ${ms} ms`)), ms);
  });
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
}

console.log(await withTimeout(delay(10, "fast enough"), 100));   // fast enough
```

The important caveat: `race` only chooses which result you *see*. The losing promise is not
stopped.

```js
const slow = delay(80).then(() => {
  console.log("slow task finished anyway");
  return "done";
});

try {
  await withTimeout(slow, 20);
} catch (error) {
  console.log(error.message);   // Timed out after 20 ms
}
await delay(100);               // logs "slow task finished anyway" — the work was never cancelled
```

If the operation costs money, bandwidth, or server capacity, a timeout must also *cancel* it — the
subject of [cancellation-with-abortcontroller.md](cancellation-with-abortcontroller.md).

## 🔁 Retrying with Exponential Backoff

Transient failures (a network blip, a briefly overloaded server) often succeed on a second attempt.
Waiting longer after each failure — **exponential backoff** — avoids hammering a struggling service:

```js
async function retry(fn, { retries = 3, delayMs = 100 } = {}) {
  let lastError;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn(attempt);
    } catch (error) {
      lastError = error;
      if (attempt < retries) {
        await delay(delayMs * 2 ** attempt);    // 100, 200, 400, ... ms
      }
    }
  }
  throw lastError;
}

let calls = 0;
const result = await retry(async () => {
  calls++;
  if (calls < 3) throw new Error("transient");
  return `ok on attempt ${calls}`;
}, { retries: 3, delayMs: 20 });

console.log(result);   // ok on attempt 3 — attempts ran at about 0, 20, and 60 ms
```

Only retry errors that are plausibly transient and operations that are safe to repeat
(idempotent); adding random "jitter" to the delay stops many clients from retrying in lockstep. The
Generative AI section covers the same idea for model calls in
[implementing-retry-mechanisms.md](../../../artificial-intelligence/error-handling-in-ai-applications/implementing-retry-mechanisms.md).

## 🧩 `Promise.withResolvers()`

Sometimes you need to settle a promise from *outside* its constructor — for example, resolving it
when a later event fires. `Promise.withResolvers()` returns the promise together with its `resolve`
and `reject` functions, replacing the old pattern of capturing them from the executor. MDN lists it as
Baseline widely available since March 2024:

```js
const { promise, resolve } = Promise.withResolvers();

setTimeout(resolve, 10, "resolved from outside");
console.log(await promise);   // resolved from outside
```

## 🎤 Interview Angle

- **"What is the difference between `Promise.race` and `Promise.any`?"** `race` settles with the first
  promise to settle, success or failure; `any` waits for the first *fulfillment* and rejects (with
  an `AggregateError`) only if all reject.
- **"What does `Promise.all` do when one promise rejects?"** It rejects immediately with that reason;
  the other promises keep running but their results are ignored.
- **"How would you limit concurrency to N?"** A pool of N workers, each pulling the next item until
  none remain.
- **"Does `Promise.race` with a timer cancel the slow operation?"** No — it only stops waiting for it.

## Common Mistakes

- **Using `forEach(async …)`** and expecting the code after it to run when the work is done.
- **Awaiting independent promises one after another** instead of creating them together.
- **Using `Promise.all` where partial results are fine** — one failure discards all of them; use
  `allSettled`.
- **Expecting a `race`-based timeout to cancel the work.**
- **Calling `Promise.race([])`** or building the input list dynamically without guarding the empty case.
- **Retrying non-idempotent operations** (such as a payment) or retrying immediately in a tight loop.

## ➡️ Next

Continue to [cancellation-with-abortcontroller.md](cancellation-with-abortcontroller.md) to see how
to actually stop in-flight work instead of merely ignoring it.
