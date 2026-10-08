# 🚨 Handling Unhandled Rejections

## The Errors Nobody Catches

A synchronous `throw` with no `catch` is hard to miss: the stack trace appears and execution stops. A
**rejected promise with no handler** is easier to lose, because the code that created it has usually
moved on. These are **unhandled rejections**, and they are among the most common causes of
silent failures in browsers and outright crashes in Node.js. This file covers how each environment
detects them, where they come from, and how to prevent them. The `try`/`catch` basics are in
[try-catch-finally.md](../error-handling-and-debugging/try-catch-finally.md), and error types in
[errors.md](../error-handling-and-debugging/errors.md).

## 🔎 What the Platform Does

A rejection is "unhandled" if the promise is rejected and still has no handler by the time the
engine checks — shortly after the current turn of the event loop. Node's documentation phrases it as
"no handler is attached within a turn of the event loop."

### In the browser

The window receives an **`unhandledrejection`** event with the rejected `promise` and its `reason`.
Calling `event.preventDefault()` suppresses the default console error. If a handler is attached
*later*, a **`rejectionhandled`** event follows:

```js
window.addEventListener("unhandledrejection", (event) => {
  console.warn("Unhandled rejection:", event.reason);
  event.preventDefault();                          // optional: suppress the console error
});

window.addEventListener("rejectionhandled", () => {
  console.log("a previously unhandled rejection now has a handler");
});
```

Recorded in a real browser, in order, for three scenarios:

```
Promise.reject(new Error("boom")), no handler          → unhandledrejection  (reason: "boom")
…then promise.catch(() => {}) attached 50 ms later     → rejectionhandled
an async click handler that throws                     → unhandledrejection  (reason: "async handler failed")
```

### In Node.js

By default (since Node 15, per the CLI documentation's `--unhandled-rejections` modes), an
unhandled rejection is **raised as an uncaught exception** — it prints the error and **terminates
the process with exit code 1**:

```bash
node -e 'Promise.reject(new Error("boom")); setTimeout(() => console.log("never printed"), 50)'
# prints the error and its stack trace to stderr; exit code 1; "never printed" never appears
```

You can intercept it with a process-level listener, which receives the `reason` and the `promise`:

```js
process.on("unhandledRejection", (reason, promise) => {
  console.log("caught:", reason.message);
});

Promise.reject(new Error("boom"));
setTimeout(() => console.log("still running"), 50);
// caught: boom
// still running      — exit code 0
```

The `--unhandled-rejections=mode` flag changes the policy: `throw` (the default), `strict`, `warn`
(print a warning and continue), `none` (ignore silently), and `warn-with-error-code`. With `warn`,
the same script prints `UnhandledPromiseRejectionWarning: Error: boom` to stderr, keeps running, and
exits with code 0.

Handlers must be attached **synchronously**. In Node's default mode, attaching a `.catch` in a later
timer is too late — the process has already crashed:

```js
const p = Promise.reject(new Error("late"));
setTimeout(() => p.catch(() => console.log("handled late")), 20);
// the process exits with code 1 before the timer fires
```

If an `unhandledRejection` listener *is* installed, Node emits `rejectionHandled` when a late handler
is finally attached.

## 🧭 Where Unhandled Rejections Come From

### 1. A promise nobody awaited or returned

```js
async function save(data) { /* may throw */ }

function onSubmit(data) {
  save(data);                 // BUG: floating promise — its failure has no handler
}
```

Fix: `await` it inside a `try`/`catch`, `return` it to a caller that will, or attach `.catch(...)`.

### 2. `async` event handlers and listeners

The caller of an event handler ignores its return value, so an `async` handler's rejection goes
nowhere:

```js
button.addEventListener("click", async () => {
  throw new Error("async handler failed");       // → an unhandledrejection event
});
```

In Node, an `async` listener on an `EventEmitter` that throws crashes the process the same way (exit
code 1). Wrap the body in `try`/`catch`:

```js
button.addEventListener("click", async () => {
  try {
    await save();
  } catch (error) {
    showError(error);
  }
});
```

### 3. `forEach(async …)` and `new Promise(async …)`

`forEach` discards the promises its callback returns (see
[promise-combinators-in-depth.md](promise-combinators-in-depth.md)), so any rejection is unhandled.
And an `async` function passed as a promise *executor* loses its errors: the thrown error rejects the
`async` function's own hidden promise, not the one you created, which then never settles:

```js
new Promise(async () => {
  throw new Error("lost in executor");        // the outer promise stays pending forever
}).then(
  () => console.log("resolved"),
  (error) => console.log("rejected", error.message),   // never runs
);
// the error surfaces only as an unhandled rejection (a crash in Node's default mode)
```

ESLint's core [`no-async-promise-executor`](https://eslint.org/docs/latest/rules/no-async-promise-executor)
rule flags this pattern.

### 4. A chain that ends without `.catch`

```js
fetchUser()
  .then(render);              // if fetchUser or render fails, nobody handles it
```

End chains with `.catch(...)`, or use `await` inside `try`/`catch`.

## ✅ What Is *Not* a Problem

`Promise.all` and friends attach their own handlers to every input, so extra rejections after the
first do not become unhandled:

```js
Promise.all([Promise.reject(new Error("first")), Promise.reject(new Error("second"))])
  .catch((error) => console.log("caught:", error.message));   // caught: first
// exit code 0; no unhandled-rejection report for "second"
```

(In the browser test, a `Promise.all` whose second input rejected after the first produced zero
`unhandledrejection` events.)

## 🛡️ Prevention and Safety Nets

1. **Handle at the boundary.** Every entry point — an event handler, a request handler, a `setTimeout`
   callback, `main()` — should either catch errors or hand its promise to code that does.
2. **Lint for it.** typescript-eslint's
   [`no-floating-promises`](https://typescript-eslint.io/rules/no-floating-promises/) rule flags a
   promise-valued statement that isn't awaited, returned, `.catch`-ed, or explicitly discarded with
   `void`; ESLint's `no-async-promise-executor` covers the executor trap above.
3. **Install a global handler as a net, not as control flow.** Use `unhandledrejection` /
   `process.on("unhandledRejection")` to *log and report* — send the error to your monitoring system
   — so none disappear silently. The platform's production content covers where those reports go:
   [Logging in Production](../../../production-systems/logging-in-production/) and
   [Monitoring and Observability](../../../production-systems/monitoring-and-observability/).
4. **In Node servers, prefer crashing and restarting.** The default exit is intentional: Node's own
   documentation warns that after an uncaught exception the application is in an undefined state,
   and recommends doing only synchronous cleanup before exiting. Let a process manager restart a
   clean process rather than limping on after an unknown error.

## 🎤 Interview Angle

- **"What is an unhandled promise rejection?"** A promise that rejects and still has no rejection
  handler when the engine checks — shortly after the current turn of the event loop.
- **"What happens to one in the browser vs. in Node?"** The browser fires `unhandledrejection` on
  `window` and logs an error; Node (default mode) treats it as an uncaught exception and exits with
  code 1.
- **"How do async event handlers fail?"** Their rejection is ignored by the caller and surfaces as an
  unhandled rejection, so they need their own `try`/`catch`.
- **"Why is `new Promise(async …)` an anti-pattern?"** Errors thrown inside never reject the outer
  promise.

## Common Mistakes

- **Calling an `async` function without `await`, `return`, or `.catch`** (a floating promise).
- **Leaving `async` event handlers without `try`/`catch`.**
- **Attaching a `.catch` after a delay** and assuming it will still count in Node.
- **Using a global handler to swallow errors** rather than to report them.
- **Using `forEach(async …)`** or `async` promise executors.

## Module Summary

Across this module: the four **promise combinators** differ in when they settle and what they return,
and patterns for **concurrency limits, timeouts, and retries** build on them — while a `race`-based
timeout only stops waiting (see [promise-combinators-in-depth.md](promise-combinators-in-depth.md));
**`AbortController`** provides real, cooperative cancellation for `fetch` and for your own async
functions, with `AbortSignal.timeout()` and `AbortSignal.any()` for timeouts and combined triggers
(see [cancellation-with-abortcontroller.md](cancellation-with-abortcontroller.md)); **async
iterators and `for await…of`** consume sequences that arrive over time, sequentially and with natural
backpressure (see [async-iterators-and-for-await.md](async-iterators-and-for-await.md));
**timers and scheduling** tools each make weaker guarantees than they appear to, and long tasks should
be sliced or moved off the main thread (see [timers-and-scheduling.md](timers-and-scheduling.md));
**Web Workers** provide real parallelism through message passing, copy-by-default data, and
transferables (see [web-workers.md](web-workers.md)); and **unhandled rejections** crash Node and
raise `unhandledrejection` in browsers, so every promise must be awaited, returned, or caught (see
this file).

## ➡️ Next

Continue to the Browser APIs in Depth module, the next module in this section, which covers the
observer APIs, URL and History, files and the clipboard, performance measurement, and the
debouncing and throttling that tame event-driven code.
