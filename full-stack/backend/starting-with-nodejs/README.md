# Starting with Node.js

## Purpose

Every domain so far has run entirely in the browser. This module starts the **Backend** domain,
beginning with **Node.js** — the JavaScript runtime that lets the same language you've already
learned throughout the [Frontend domain](../../frontend/README.md) run on a server, outside any
browser at all.

## Learning Objectives

- Explain what Node.js is: a JavaScript runtime built on Chrome's V8 engine, distinct from a
  browser environment.
- Describe Node's event-driven, non-blocking I/O model at a conceptual level, and why it matters
  for a server handling many connections at once.
- Set up a local Node.js development environment.
- Use npm to manage a project's dependencies via `package.json`.

## Prerequisites

- The full [JavaScript domain](../../frontend/javascript/) — Node.js runs the same JavaScript
  language; this module is about the *runtime environment* around it, not the language itself.

## Files in This Module

| File | Covers |
|---|---|
| [what-is-nodejs.md](what-is-nodejs.md) | Node.js as a JavaScript runtime, and how it differs from running JavaScript in a browser |
| [how-nodejs-works.md](how-nodejs-works.md) | The V8 engine, libuv, and Node's event-driven, non-blocking I/O model |
| [nodejs-runtime.md](nodejs-runtime.md) | The `global` object, the `process` object, and what's available in Node but not a browser |
| [setting-up-nodejs.md](setting-up-nodejs.md) | Installing Node.js, version management, and running your first script |
| [npm-and-package-management.md](npm-and-package-management.md) | npm, `package.json`, dependencies vs. devDependencies, and semantic versioning |

## When to Deep-Dive vs. Skim

Deep-dive [how-nodejs-works.md](how-nodejs-works.md) — Node's non-blocking I/O model is the single
architectural idea that explains *why* backend JavaScript code is commonly written the way it is
(callbacks, promises, `async`/`await`), a pattern you'll see constantly for the rest of this
domain.

## Quick Knowledge Check

<details>
<summary>Is Node.js a different programming language from the JavaScript you already know?</summary>

No — it's the same JavaScript language, running in a different environment. A browser's JavaScript
engine gives you APIs like `document` and `window`; Node's runtime instead gives you APIs for
things a server needs, like file system access and network sockets, built on the same underlying
V8 engine that also powers Chrome. See [what-is-nodejs.md](what-is-nodejs.md).

</details>

<details>
<summary>Why can Node.js handle many simultaneous connections efficiently without spawning a new thread for each one?</summary>

Because of its non-blocking I/O model: instead of a thread sitting idle while waiting on a slow
operation (reading a file, querying a database), Node hands that operation off and moves on to
other work, coming back via a callback once the operation completes. See
[how-nodejs-works.md](how-nodejs-works.md).

</details>

## References

- Node.js, [About Node.js](https://nodejs.org/en/about)
- npm Docs, [About npm](https://docs.npmjs.com/about-npm)

## Continue Your Learning Path

Continue to the [Node.js Core Concepts module](../nodejs-core-concepts/) to go deeper into Node's
built-in capabilities: modules, the file system, and the process environment.
