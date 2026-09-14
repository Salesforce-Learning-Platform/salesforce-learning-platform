# How Node.js Works

## Two Engines Working Together

Node.js is built from two separate underlying pieces:

- **V8** — Google's JavaScript engine (the same one inside Chrome) — compiles and executes the
  actual JavaScript code: your variables, functions, and logic.
- **libuv** — a C library providing the event loop and non-blocking I/O — handles everything V8
  itself can't: reading files, network sockets, timers, and coordinating with the operating system.

Node.js is the layer that connects these two: V8 runs your JavaScript, and whenever that code needs
to do something slow (read a file, query a database, wait on a network request), Node hands that
work off to libuv instead of making V8 sit and wait for it.

## Non-Blocking I/O in Practice

```js
const fs = require("node:fs");

console.log("1: starting");

fs.readFile("large-file.txt", "utf8", (err, data) => {
  console.log("3: file finished reading");
});

console.log("2: this runs before the file is done");
```

```
1: starting
2: this runs before the file is done
3: file finished reading
```

Reading a file is comparatively slow. In a **blocking** model, the whole program would freeze until
the read finished. Node's `fs.readFile` instead starts the read, immediately returns control to the
rest of the script (line `2` logs right away), and only runs the callback once the file is actually
ready — the exact same pattern you already know from
[the JavaScript event loop](../../frontend/javascript/event-loop/) and
[promises/async-await](../../frontend/javascript/asynchronous-programming-and-modules/), just now
applied to server-side operations like file and network access instead of browser `fetch` calls.

## Why This Matters for a Server Specifically

```js
// Handling many requests: while one request is waiting on a slow
// database query, Node is free to start working on the next request —
// it doesn't sit idle for the first one to finish.
```

A web server routinely needs to handle many requests arriving close together, and each request
often needs to wait on something slow — a database query, a call to another service. A traditional
thread-per-request model spins up a new operating system thread for every connection, which is
expensive in memory and coordination overhead as the number of connections grows. Node's single
main thread, combined with libuv handing off slow I/O work in the background, lets one process
handle a large number of concurrent connections efficiently, without needing a dedicated thread
sitting idle for each one.

## Common Mistakes

- Assuming Node.js is single-threaded in every sense — the *your JavaScript code* runs on a single
  main thread, but libuv itself uses a background thread pool for some operations (like file
  system access) under the hood; the concurrency model is more nuanced than "no threads exist at
  all."
- Writing genuinely CPU-heavy, synchronous JavaScript (a huge in-memory loop with no I/O) and
  expecting Node's non-blocking model to help — that model specifically addresses I/O-bound
  waiting, not CPU-bound computation, which still blocks the single JavaScript thread while it
  runs.
- Confusing "non-blocking" with "instant" — a non-blocking operation still takes real time to
  complete; it just doesn't freeze the rest of the program while it does.

## Next

Continue to [nodejs-runtime.md](nodejs-runtime.md) to see the concrete globals and objects this
runtime actually gives your code access to.
