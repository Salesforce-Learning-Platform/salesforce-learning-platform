# The Call Stack

## JavaScript Is Single-Threaded

JavaScript executes on a single thread — one **call stack**, and only one line of JavaScript
running at any given instant. This is a genuinely different model from languages that run multiple
threads of execution truly in parallel.

## How the Stack Works

Every function call pushes a new **frame** onto the call stack; when a function returns, its frame
is popped off:

```js
function multiply(a, b) { return a * b; }
function square(n) { return multiply(n, n); }
function printSquare(n) { console.log(square(n)); }

printSquare(5);
```

```text
Call stack grows:            Call stack shrinks (as functions return):
printSquare(5)                multiply returns 25
  square(5)                    square returns 25
    multiply(5, 5)              printSquare logs 25, then returns
```

The stack is Last-In-First-Out (LIFO) — the most recently called function is the first to finish
and be removed.

## Why a Blocking Function Freezes Everything

```js
function blockForTooLong() {
  const start = Date.now();
  while (Date.now() - start < 5000) {
    // busy-wait for 5 seconds — nothing else can run during this
  }
}
```

Because there's only one call stack, a function that takes a long time to finish (or, worse, never
returns) occupies the *only* thread JavaScript has — no event handler, no timer callback, no
rendering update can happen until that function finally returns and its frame is popped. This is
exactly why a genuinely long-running synchronous operation visibly freezes a page's UI, and why
asynchronous patterns (Promises, `async`/`await`, timers) exist: to hand off waiting to something
other than the call stack, covered next in
[web-apis.md](web-apis.md).

## Stack Overflow

```js
function recurse() {
  return recurse(); // never returns — no base case
}
recurse(); // "Maximum call stack size exceeded"
```

The call stack has a finite size; a recursive function with no terminating condition eventually
exceeds it, producing a `RangeError: Maximum call stack size exceeded` — a direct, observable
consequence of the stack being a real, size-limited structure.

## Common Mistakes

- Running a long, synchronous, CPU-heavy operation directly on the main thread in a browser
  application, freezing the UI for its entire duration.
- Writing recursive functions without a correct base case, risking a stack overflow.
- Assuming JavaScript can run two pieces of code "at the same time" — it cannot; what looks like
  concurrency is the event loop interleaving separate, individually single-threaded pieces of
  execution, covered across the rest of this module.

## Next

Continue to [web-apis.md](web-apis.md) to see where waiting (for a timer, a network request)
actually happens, since it isn't on this stack.
