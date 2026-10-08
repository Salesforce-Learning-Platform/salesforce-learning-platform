# 🛑 Cancellation with AbortController

## Promises Cannot Be Cancelled — Operations Can

A promise is only a *result placeholder*; once the work behind it has started there is no
`promise.cancel()`. The previous file ended with a `race`-based timeout that stopped *waiting* but
not *working*. Real cancellation is **cooperative**: you hand the operation an **`AbortSignal`**, and
the operation watches it and stops itself. The standard Web API for this is **`AbortController`**,
which works in browsers (including Web Workers) and in Node.js.

## 🎛️ The Pieces

```js
const controller = new AbortController();   // the thing you hold, to trigger cancellation
const signal = controller.signal;            // the thing you hand to the operation

controller.abort();                          // trigger it (optionally with a reason)
```

| Piece | Purpose |
|-------|---------|
| `controller.abort(reason?)` | Marks the signal aborted. A signal can be aborted **only once** |
| `signal.aborted` | `true` once aborted |
| `signal.reason` | Why — a `DOMException` named `AbortError` by default, or whatever you passed |
| `signal.throwIfAborted()` | Throws `signal.reason` if aborted; does nothing otherwise |
| `signal.addEventListener("abort", …)` | Run code the moment cancellation happens |

## 🌐 Cancelling `fetch`

Pass the signal in the options. If it aborts, the request is cancelled and the returned promise
rejects. This example runs against a local server that takes about 300 ms to respond:

```js
const controller = new AbortController();
setTimeout(() => controller.abort(), 50);

try {
  await fetch(url, { signal: controller.signal });
} catch (error) {
  console.log(error.name);                        // AbortError
  console.log(error.message);                     // This operation was aborted
  console.log(error instanceof DOMException);     // true
  console.log(controller.signal.aborted);         // true
}
```

(Message wording differs between browsers and Node.js; test `error.name`, not the text.)

Pass a reason to `abort()` and `fetch` rejects with *that* value instead:

```js
const controller = new AbortController();
setTimeout(() => controller.abort(new Error("user navigated away")), 50);

try {
  await fetch(url, { signal: controller.signal });
} catch (error) {
  console.log(error.name, "|", error.message);    // Error | user navigated away
}
```

### Built-in Timeouts: `AbortSignal.timeout()`

Instead of wiring a timer by hand, ask for a signal that aborts itself after a delay. It fails with a
different name, `TimeoutError`, so you can tell a timeout from a user cancel:

```js
try {
  await fetch(url, { signal: AbortSignal.timeout(50) });
} catch (error) {
  console.log(error.name);      // TimeoutError
  console.log(error.message);   // The operation was aborted due to timeout
}
```

Unlike the `race` timeout, this one genuinely cancels the request: the promise rejects at the
timeout (about 40 ms in a test with a 300 ms server delay) instead of the work carrying on.

### Combining Signals: `AbortSignal.any()`

A request often has two reasons to stop: the user clicked "cancel," or too much time passed.
`AbortSignal.any` returns a signal that aborts when the *first* of its inputs does:

```js
const user = new AbortController();
const signal = AbortSignal.any([user.signal, AbortSignal.timeout(5000)]);

await fetch(url, { signal });   // aborts on user.abort() OR after 5 seconds, whichever comes first
```

In the test runs, the timeout-first case rejected with `TimeoutError` and the user-first case with
`AbortError`. MDN notes that `AbortSignal.timeout()` and `AbortSignal.any()` have more varied
support than `AbortController` itself (which has been widely available since 2019), so check its
compatibility table for older environments.

`AbortSignal.abort()` returns a signal that is *already* aborted — handing it to `fetch` rejects
immediately with `AbortError`.

## 🧰 Making Your Own Functions Cancellable

The same signal can control any async function you write. Accept `{ signal }` as an option, check it
at safe points, and use `throwIfAborted()` to bail out with the correct error:

(`delay(ms)` is the timer helper defined at the top of
[promise-combinators-in-depth.md](promise-combinators-in-depth.md).)

```js
async function processAll(items, { signal } = {}) {
  const done = [];
  for (const item of items) {
    signal?.throwIfAborted();                 // stop before starting the next item
    await delay(20);                           // stand-in for real work
    done.push(item);
  }
  return done;
}
```

Aborting 50 ms into a five-item run (20 ms per item) stops the loop with an `AbortError` after the
item in flight finishes — three items done. Cancellation happens at the *checks* you place; code
between checks runs to completion.

### An Abortable `sleep`

Waiting on a timer is the simplest case of "work you can cancel": clear the timer and reject when the
signal fires.

```js
function sleep(ms, { signal } = {}) {
  return new Promise((resolve, reject) => {
    signal?.throwIfAborted();                  // already cancelled? fail immediately
    const timer = setTimeout(resolve, ms);
    signal?.addEventListener("abort", () => {
      clearTimeout(timer);                     // release the timer
      reject(signal.reason);
    }, { once: true });
  });
}

const controller = new AbortController();
setTimeout(() => controller.abort(), 20);

try {
  await sleep(500, { signal: controller.signal });
} catch (error) {
  console.log(error.name);    // AbortError — after about 20 ms, not 500
}
```

## 🧹 Tearing Down Event Listeners

`addEventListener` accepts a `signal` option, and the listener is removed automatically when the signal
aborts — one controller can clean up any number of listeners at once:

```js
const target = new EventTarget();
const hits = [];
const controller = new AbortController();

target.addEventListener("ping", () => hits.push("A"), { signal: controller.signal });
target.addEventListener("ping", () => hits.push("B"), { signal: controller.signal });

target.dispatchEvent(new Event("ping"));   // both listeners run
controller.abort();                         // both are removed
target.dispatchEvent(new Event("ping"));   // nothing runs

console.log(hits);   // [ 'A', 'B' ]
```

This is the idiomatic cleanup for components and subscriptions (the same `EventTarget` interface
underlies DOM events).

## ⚛️ The Component Pattern

In UI code, the usual lifecycle is "start a request when something changes, cancel the stale one when
it changes again or the component goes away." A React effect expresses it directly, as covered in
[fetching-data.md](../../react/server-state-and-api-integration/fetching-data.md):

```js
useEffect(() => {
  const controller = new AbortController();

  fetch(`/api/users/${id}`, { signal: controller.signal })
    .then((response) => response.json())
    .then(setUser)
    .catch((error) => {
      if (error.name !== "AbortError") setError(error);   // an abort is expected, not a failure
    });

  return () => controller.abort();            // cleanup: cancel the stale request
}, [id]);
```

Without the cleanup, a slow response for an *old* `id` can arrive after a newer one and overwrite the
screen with stale data — a race condition that cancellation removes.

## 🎯 Distinguish Cancellation from Failure

An abort is usually an intentional event, not an error to show a user or send to monitoring. Branch
on the error name:

```js
try {
  await loadData({ signal });
} catch (error) {
  if (error.name === "AbortError") return;          // user cancelled: stay quiet
  if (error.name === "TimeoutError") showRetry();   // too slow: offer a retry
  else throw error;                                  // a real failure
}
```

## 🎤 Interview Angle

- **"Can you cancel a Promise?"** Not directly. You cancel the *operation* by passing it an
  `AbortSignal` and having it stop itself; the promise then rejects.
- **"How do you cancel a `fetch`?"** Create an `AbortController`, pass `controller.signal` to
  `fetch`, and call `controller.abort()`; the promise rejects with an `AbortError`.
- **"`AbortError` vs. `TimeoutError`?"** `AbortError` is a manual or explicit abort;
  `TimeoutError` is what `AbortSignal.timeout()` produces when its delay expires.
- **"Why abort in a React effect cleanup?"** To prevent stale responses from overwriting newer state
  and to avoid work for components that are gone.

## Common Mistakes

- **Treating a `race`-based timeout as cancellation** — the loser keeps running.
- **Reusing an aborted controller** — a signal aborts once; create a new controller per operation.
- **Reporting `AbortError` as a failure** in the UI or logs.
- **Passing a signal to an API that ignores it** — check the API's documentation; only operations that
  watch the signal can be cancelled.
- **Forgetting to clear timers or remove listeners** in your own cancellable code.

## ➡️ Next

Continue to [async-iterators-and-for-await.md](async-iterators-and-for-await.md) to handle sequences
of values that arrive over time — pages of results, streams, and events.
