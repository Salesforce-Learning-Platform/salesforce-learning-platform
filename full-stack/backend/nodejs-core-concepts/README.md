# Node.js Core Concepts

## Purpose

[Starting with Node.js](../starting-with-nodejs/) got a script running and a project's dependencies
installed. This module goes one level deeper into Node's own built-in capabilities — the module
system, file system access, path handling, environment variables, process control, and the exact
mechanics of the event loop introduced conceptually in
[how-nodejs-works.md](../starting-with-nodejs/how-nodejs-works.md) — the concrete toolkit every
later backend module in this domain builds on.

## Learning Objectives

- Split code across files using Node's module system, and explain the real differences between
  CommonJS and ES Modules.
- Read and write files using the `fs` module, choosing the right variant (sync, callback, promise)
  for a given situation.
- Build cross-platform-safe file paths with the `path` module instead of manual string
  concatenation.
- Read configuration safely from `process.env`, and load it from a `.env` file in development.
- Control a Node process's lifecycle: exit codes, OS signals, and graceful shutdown.
- Explain the Node.js event loop's actual phases, and where `process.nextTick`/Promises fit
  relative to them.

## Prerequisites

- [Starting with Node.js](../starting-with-nodejs/) — this module assumes Node and npm are already
  installed and a basic script can already run.

## Files in This Module

| File | Covers |
|---|---|
| [modules.md](modules.md) | Why code is split across files at all, and Node's module system at a conceptual level |
| [commonjs-and-es-modules.md](commonjs-and-es-modules.md) | `require`/`module.exports` vs. `import`/`export`, and how to choose between them |
| [file-system.md](file-system.md) | The `fs` module: sync, callback, and promise-based file access |
| [path-module.md](path-module.md) | `path.join`, `path.resolve`, and cross-platform path safety |
| [environment-variables.md](environment-variables.md) | `process.env`, `.env` files, and keeping secrets out of source control |
| [process-and-runtime.md](process-and-runtime.md) | Exit codes, OS signals, and graceful shutdown |
| [nodejs-event-loop.md](nodejs-event-loop.md) | The event loop's real phases, and `process.nextTick` vs. `setImmediate` |

## When to Deep-Dive vs. Skim

Deep-dive [nodejs-event-loop.md](nodejs-event-loop.md) — the conceptual, browser-facing version of
the event loop from [event-loop.md](../../frontend/javascript/event-loop/) gets you most of the way
there, but Node's *specific* phases (timers, poll, check) and the `process.nextTick`/`setImmediate`
distinction are genuinely Node-specific details worth understanding precisely, since they explain
otherwise-surprising execution-order behavior in real backend code.

## Quick Knowledge Check

<details>
<summary>Should a new Node.js project in 2026 default to CommonJS or ES Modules?</summary>

ES Modules — it's the standardized, cross-runtime module format (also used by every browser and by
your existing [Frontend](../../frontend/README.md) code), and Node's support for it is stable.
CommonJS remains extremely common in existing/legacy codebases, so recognizing it is still
essential, but new projects should generally default to ESM. See
[commonjs-and-es-modules.md](commonjs-and-es-modules.md).

</details>

<details>
<summary>Why shouldn't a real backend project commit its `.env` file to version control?</summary>

A `.env` file typically holds secrets — database credentials, API keys — that must never become
part of a public (or even private, shared) git history. It's excluded via `.gitignore`, and only a
`.env.example` template (with placeholder values) is committed instead. See
[environment-variables.md](environment-variables.md).

</details>

## References

- Node.js, [Modules: CommonJS modules](https://nodejs.org/api/modules.html)
- Node.js, [Modules: ECMAScript modules](https://nodejs.org/api/esm.html)
- Node.js, [File system](https://nodejs.org/api/fs.html)
- Node.js, [Path](https://nodejs.org/api/path.html)
- Node.js, [The Node.js Event Loop, Timers, and process.nextTick()](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
- Node.js, [Process](https://nodejs.org/api/process.html)
- Node.js, [How to read environment variables from Node.js](https://nodejs.org/en/learn/command-line/how-to-read-environment-variables-from-nodejs)

## Continue Your Learning Path

Continue to the [Creating Your First Server module](../creating-your-first-server/) to put these
core concepts to use building an actual HTTP server.
