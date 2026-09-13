# Microtasks and Macrotasks

## Two Separate Queues, Not One

[callback-queue.md](callback-queue.md) simplified slightly: there isn't just one queue — there are
two, with different priority:

| Queue | Contains | Priority |
|---|---|---|
| **Microtask queue** | Promise callbacks (`.then`/`.catch`/`.finally`, `async`/`await` continuations) | Higher |
| **Macrotask queue** ("task queue") | `setTimeout`/`setInterval` callbacks, DOM events, I/O | Lower |

## The Rule: Microtasks Are Fully Drained First

After each single macrotask finishes running, the event loop processes **every** currently queued
microtask — completely emptying the microtask queue — before it moves on to the next macrotask.

```js
console.log("1");

setTimeout(() => console.log("2"), 0);   // macrotask

Promise.resolve().then(() => console.log("3")); // microtask

console.log("4");

// Logs: 1, 4, 3, 2
```

Walking through it: `"1"` and `"4"` run first (synchronous code, no queue involved at all). Then,
before the event loop even looks at the macrotask queue (where the `setTimeout` callback is
waiting), it fully drains the microtask queue — running `"3"`. Only after the microtask queue is
completely empty does the event loop move on to the next macrotask, running `"2"` last.

## Why This Matters Practically

This is exactly why Promise-based code (including `async`/`await`, which is built on Promises —
see [async-await.md](../asynchronous-programming-and-modules/async-await.md)) consistently appears
to run "sooner" than an equivalent `setTimeout`, even a `setTimeout(fn, 0)` — it's not a
coincidence or a performance quirk, it's the specification-defined priority of microtasks over
macrotasks.

## A Practical Consequence: Starving the Macrotask Queue

Because microtasks are drained *completely* before any macrotask runs, code that keeps generating
new microtasks (a Promise chain that keeps scheduling more `.then()` callbacks indefinitely) can, in
principle, starve macrotasks — including rendering updates and timers — from ever getting a turn.
This is a genuine, known edge case worth being aware of, though it's uncommon in typical
application code.

## Common Mistakes

- Assuming all asynchronous callbacks are interchangeable in terms of scheduling priority — a
  Promise callback and a `setTimeout` callback are handled by genuinely different queues with
  different priority.
- Being surprised that Promise-chain code runs before a `setTimeout(fn, 0)` registered earlier in
  the same synchronous block, rather than understanding this as guaranteed, specification-defined
  behavior.
- Not recognizing an unbounded chain of self-scheduling microtasks as a potential cause of a page
  that seems to freeze despite having "async" code, since it can starve macrotasks (including
  rendering) from running.

## Module Summary

Across this module: JavaScript's single call stack means only one thing runs at a time, and a
long-running synchronous function blocks everything else (see [call-stack.md](call-stack.md));
Web APIs provided by the browser (or Node) handle the actual waiting for timers, network requests,
and events, entirely outside that call stack (see [web-apis.md](web-apis.md)); completed
operations are queued and only pushed back onto the call stack once it's empty, via the event loop
(see [callback-queue.md](callback-queue.md)); and microtasks (Promises) are fully drained before
any macrotask (`setTimeout`) runs, which is the specification-defined reason Promise-based code
consistently executes before an equivalent timer callback.
