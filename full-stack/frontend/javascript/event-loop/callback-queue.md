# The Callback Queue and the Event Loop

## Getting Back onto the Call Stack

Once a Web API operation completes (a timer elapses, a network response arrives), its associated
callback doesn't run immediately — it's placed into a **queue**, waiting its turn.

## The Event Loop's Job

The **event loop** is a continuously running process with one simple job: check whether the call
stack is empty, and if it is, take the next callback from the queue and push it onto the stack to
run.

```text
        ┌─────────────┐
        │  Call Stack   │◀──── event loop pushes the next
        └─────────────┘        queued callback here, but
              ▲                  ONLY when the stack is empty
              │
        ┌─────────────┐
        │Callback Queue │◀──── completed Web API callbacks
        └─────────────┘        wait here
```

This is why `setTimeout(fn, 0)` doesn't run `fn` synchronously, immediately: it still has to wait
in the queue, and the queue is only drained once the call stack is completely empty — meaning any
currently executing synchronous code always finishes first, no matter how short the requested
delay was.

```js
console.log("1");
setTimeout(() => console.log("2"), 0);
console.log("3");
// Logs: 1, 3, 2 — NOT 1, 2, 3
```

`"2"` is logged last because its callback must wait in the queue until the synchronous code
(`console.log("1")` and `console.log("3")`) has finished and the call stack is empty.

## Order Is Not Guaranteed to Match Registration Alone

Multiple timers, network responses, and other queued callbacks generally run in the order their
underlying operation actually completed — but since real-world completion timing (a network
response, in particular) isn't perfectly predictable, code that depends on a strict ordering
between multiple independent async operations should use explicit coordination (like
`Promise.all()`, from [promises.md](../asynchronous-programming-and-modules/promises.md)) rather
than assuming a specific order.

## Common Mistakes

- Expecting `setTimeout(fn, 0)` to run synchronously or "immediately" — it always waits for the
  current synchronous code to finish and the queue to be reached.
- Assuming queued callbacks always run in exactly the order they were registered, when their
  actual completion time (especially for network requests) can vary.
- Writing code that only "happens to work" because of a currently observed execution order, rather
  than explicitly coordinating dependent asynchronous operations.

## Next

Continue to
[microtasks-and-macrotasks.md](microtasks-and-macrotasks.md) — there isn't actually just one
queue, and the distinction explains several otherwise-confusing ordering questions.
