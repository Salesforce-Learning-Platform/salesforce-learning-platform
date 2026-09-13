# Web APIs

## Where Waiting Actually Happens

If JavaScript has only one call stack, how does `setTimeout` or `fetch` avoid blocking it for the
entire wait? The answer: they don't wait on the call stack at all. `setTimeout`, `fetch`, DOM event
listeners, and similar APIs are provided by the **browser** (or Node's runtime, for its
equivalents) — not by the JavaScript engine itself, echoing the distinction introduced in
[browser-apis.md](../using-browser-functionalities/browser-apis.md).

```text
JavaScript engine (call stack)         Browser-provided environment
        │                                        │
        │── setTimeout(fn, 1000) ───────────────▶│ starts a 1000ms timer here,
        │                                        │ OUTSIDE the call stack
        │◀── call stack is immediately free ─────│ (setTimeout itself returns right away)
        │                                        │
        │                              ...1000ms pass, handled by the browser...
        │                                        │
        │◀── fn is placed in a queue ────────────│ (see callback-queue.md)
```

When you call `setTimeout(fn, 1000)`, the call itself returns *immediately* — the actual waiting
happens inside the browser's own timer mechanism, completely separate from JavaScript's call
stack. The same applies to `fetch()` (the browser's networking stack handles the actual request)
and DOM event listeners (the browser watches for the event, entirely independent of whatever
JavaScript is or isn't currently executing).

## Why This Design Enables Non-Blocking Behavior

This is the actual mechanism that makes JavaScript's asynchronous model work despite being
single-threaded: the *waiting* is delegated entirely to the browser environment, freeing the call
stack to continue running other code immediately. Only once the browser's part is done (the timer
elapses, the network response arrives, the event fires) does the corresponding callback get handed
back to JavaScript — placed in a queue, waiting for the call stack to be empty enough to run it.

## Common Mistakes

- Assuming `setTimeout`/`fetch` are handled by the same single-threaded JavaScript engine that runs
  your code — they're handled by the surrounding browser (or Node) environment specifically so they
  don't block it.
- Believing `setTimeout(fn, 0)` runs `fn` immediately — it still goes through this same
  queue-and-wait mechanism, guaranteeing only that it runs *after* the current synchronous code
  finishes, not literally instantly.
- Forgetting that Node.js provides a different set of these environment APIs than a browser does
  (as introduced in [browser-apis.md](../using-browser-functionalities/browser-apis.md)) — the
  underlying event-loop mechanism is conceptually similar, but the exact APIs differ by
  environment.

## Next

Continue to [callback-queue.md](callback-queue.md) to see exactly how a completed Web API
operation makes its way back onto the call stack.
