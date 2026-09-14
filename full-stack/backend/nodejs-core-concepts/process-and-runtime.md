# Process and Runtime

## Exit Codes: How a Process Reports Success or Failure

```js
// A script that validates something and needs to signal failure to
// whatever ran it (a shell script, a CI pipeline, a process manager)
if (!isValidConfig(config)) {
  console.error("Invalid configuration");
  process.exitCode = 1; // exit code 1 = failure, once the event loop empties
} else {
  // exit code 0 (success) is the default — nothing to set
}
```

Every process, when it ends, reports a numeric **exit code** to whatever started it: `0`
conventionally means success, and any non-zero value means some kind of failure. Setting
`process.exitCode` and letting the process end naturally (once there's no more pending work) is the
generally preferred approach over calling `process.exit()` directly, which forces immediate
termination and can cut off in-progress writes (like a final `console.log`) before they complete.

## OS Signals and Graceful Shutdown

```js
const server = createServer(/* ... */);
server.listen(3000);

process.on("SIGTERM", () => {
  console.log("Received SIGTERM, shutting down gracefully");
  server.close(() => {
    console.log("Server closed, no longer accepting new connections");
    process.exit(0);
  });
});
```

A running server process can receive **signals** from the operating system — `SIGINT` (sent when a
developer presses Ctrl+C in a terminal) and `SIGTERM` (the standard signal a process manager, a
container orchestrator, or a deployment platform sends to request a clean shutdown) are the two
most common in backend work. Listening for `SIGTERM` and closing the server deliberately —
finishing in-flight requests, then stopping — is what "graceful shutdown" means: the alternative,
letting the process die instantly, can cut off a request mid-response for whichever user happened
to be connected at that exact moment.

## `uncaughtException` — A Last Resort, Not a Strategy

```js
process.on("uncaughtException", (err) => {
  console.error("Fatal error, shutting down:", err);
  // Only synchronous cleanup here — flushing logs, closing a file handle —
  // then let the process actually exit
  process.exitCode = 1;
  process.exit();
});
```

The `uncaughtException` event fires when a JavaScript error escapes every other error-handling
mechanism in the program. It exists purely as a last-resort safety net for emergency cleanup (like
flushing a log) immediately before the process ends — **not** as a general error-handling strategy,
and specifically not as a way to "catch the error and keep running." Node's own guidance is
explicit: a process that hit an uncaught exception is in an unknown, potentially corrupted state,
and should exit rather than continue serving requests.

## Common Mistakes

- Calling `process.exit()` immediately after an async operation without waiting for it to actually
  finish, cutting off pending file writes, network responses, or database operations mid-flight.
- Ignoring `SIGTERM` entirely, so a deployment or restart forcibly kills the process mid-request
  instead of letting it finish gracefully.
- Treating `uncaughtException` as a way to "keep the server running no matter what" — attempting to
  resume normal operation after one is explicitly unsafe, since the program's internal state at
  that point is no longer trustworthy.

## Next

Continue to [nodejs-event-loop.md](nodejs-event-loop.md) to see precisely how Node schedules all of
this asynchronous work — file reads, timers, signals — under the hood.
