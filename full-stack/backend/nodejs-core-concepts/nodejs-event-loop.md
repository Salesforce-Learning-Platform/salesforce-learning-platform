# The Node.js Event Loop

## From Concept to Concrete Mechanism

[how-nodejs-works.md](../starting-with-nodejs/how-nodejs-works.md) and
[event-loop.md](../../frontend/javascript/event-loop/) covered the event loop conceptually: Node
hands off slow work and comes back to it via a callback once ready. This file goes one level
deeper — the event loop's **actual phases**, which explain execution-order behavior that the
conceptual model alone doesn't predict.

## The Six Phases, in Order

```
   ┌───────────────────────────┐
┌─>│           timers           │  setTimeout, setInterval callbacks
│  └─────────────┬───────────────┘
│  ┌─────────────┴───────────────┐
│  │     pending callbacks       │  some deferred I/O callbacks (e.g. TCP errors)
│  └─────────────┬───────────────┘
│  ┌─────────────┴───────────────┐
│  │       idle, prepare         │  internal use only
│  └─────────────┬───────────────┘
│  ┌─────────────┴───────────────┐
│  │            poll             │  fetch new I/O events; most callbacks run here
│  └─────────────┬───────────────┘
│  ┌─────────────┴───────────────┐
│  │            check            │  setImmediate callbacks
│  └─────────────┬───────────────┘
│  ┌─────────────┴───────────────┐
└──┤       close callbacks       │  e.g. socket.on('close', ...)
   └───────────────────────────┘
```

Each full pass through these six phases is one **tick** of the event loop. **timers** runs any
`setTimeout`/`setInterval` callbacks whose time has elapsed; **poll** is where the loop spends most
of its time in a typical server, waiting for and handling actual I/O (an incoming request, a
finished file read); **check** runs anything scheduled with `setImmediate()`; and **close
callbacks** handles cleanup events like a closed socket.

## `process.nextTick` and Promises Aren't a Phase At All

```js
console.log("1: synchronous code");

setTimeout(() => console.log("4: timer phase"), 0);

process.nextTick(() => console.log("2: nextTick queue"));

Promise.resolve().then(() => console.log("3: microtask queue"));
```

```
1: synchronous code
2: nextTick queue
3: microtask queue
4: timer phase
```

`process.nextTick()` callbacks and resolved-Promise (`.then()`) callbacks are **not** one of the
six phases — they run in their own queues, processed immediately after whatever's currently
executing finishes, *before* the event loop is allowed to move into its next phase. `nextTick`
specifically runs before Promise microtasks. This is why both of these consistently run before any
timer, even a `setTimeout(fn, 0)`: the loop clears both queues completely before continuing to the
next phase at all.

## `setImmediate` vs. `setTimeout(fn, 0)`

```js
import { readFile } from "node:fs";

readFile(__filename, () => {
  setTimeout(() => console.log("timeout"), 0);
  setImmediate(() => console.log("immediate")); // runs first, reliably
});
```

Outside an I/O callback, the order between `setTimeout(fn, 0)` and `setImmediate(fn)` isn't
guaranteed. But **inside** an I/O callback (as above), `setImmediate` reliably runs first — because
that code is already executing during the **poll** phase, and `check` (where `setImmediate`
callbacks run) is the very next phase, arriving before the loop cycles back around to **timers**.

## Why Starving the Loop Is a Real Danger

```js
// AVOID — this callback keeps re-scheduling itself via nextTick,
// which runs before the loop can ever advance to the poll phase —
// meaning no real I/O (a request, a file read) can ever be handled
function recursiveNextTick() {
  process.nextTick(recursiveNextTick);
}
```

Because `process.nextTick`'s queue is fully drained before the loop can proceed to its next phase,
code that keeps re-scheduling itself via `nextTick` can prevent the loop from ever reaching
**poll** — meaning the server stops handling any real I/O at all, even though it looks like it's
still "running." Node's own guidance is to prefer `setImmediate()` for most deferred-work use
cases specifically because it doesn't carry this starvation risk.

## Common Mistakes

- Assuming `process.nextTick` and Promise `.then()` callbacks are part of one of the six labeled
  phases — they aren't; they run in their own queues between every single phase transition.
- Writing code that recursively re-schedules itself with `process.nextTick`, unintentionally
  starving the event loop of the ability to handle real I/O.
- Assuming `setTimeout(fn, 0)` and `setImmediate(fn)` always run in a fixed, predictable order —
  outside an I/O callback, that order is genuinely not guaranteed.

## Module Summary

Across this module: Node's **module system** — whether CommonJS's `require`/`module.exports` or
the standardized ES Modules' `import`/`export` — splits code into files with an explicit public
surface (see [modules.md](modules.md) and
[commonjs-and-es-modules.md](commonjs-and-es-modules.md)); the **`fs` module** offers sync,
callback, and promise-based file access, with the sync variant reserved for startup only (see
[file-system.md](file-system.md)); the **`path` module** builds file paths that work correctly
regardless of operating system (see [path-module.md](path-module.md)); **`process.env`** and `.env`
files keep configuration and secrets out of source code (see
[environment-variables.md](environment-variables.md)); **exit codes, signals, and graceful
shutdown** control how a process starts and, just as importantly, ends cleanly (see
[process-and-runtime.md](process-and-runtime.md)); and the event loop's actual **six phases**, plus
the `nextTick`/microtask queues that run between every one of them, explain precisely why
asynchronous Node code executes in the order it does.
