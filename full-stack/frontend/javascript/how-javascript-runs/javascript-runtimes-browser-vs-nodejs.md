# 🌍 JavaScript Runtimes: Browser vs. Node.js

## The Engine Is Only Part of the Story

[javascript-engines-and-jit-compilation.md](javascript-engines-and-jit-compilation.md) covered the engine
that executes the language. But the language has no `document`, no file system, no network functions, and no
timers — those come from the **runtime** around the engine, which adds the **APIs** and the **event
loop**. As [browser-apis.md](../using-browser-functionalities/browser-apis.md) introduced, the same engine
(V8) powers Chrome and Node.js, yet their programs are very different because their runtimes are.

```
RUNTIME  =  JavaScript ENGINE  +  environment APIs  +  event loop  +  module loader
```

| Runtime | Engine | Notable character |
|---------|--------|-------------------|
| **Browser** | V8, SpiderMonkey, or JavaScriptCore | DOM, rendering, user-facing APIs; sandboxed |
| **Node.js** | V8 | Server-side: file system, processes, networking; full OS access by default |
| **Deno** | built on Rust (per its site) | Runs TypeScript directly; "secure by default" — blocks file, network, and environment access unless permitted |
| **Bun** | JavaScriptCore | An all-in-one runtime, package manager, test runner, and bundler (per its site) |

This file concentrates on browsers and Node.js, the two you will use most.

## 🔎 What Exists Where (Probed in Both)

A script checked `typeof` for the same names in a real browser and in Node.js 24:

| Name | Browser | Node.js | Belongs to |
|------|:-------:|:-------:|-----------|
| `window`, `document` | object | undefined | Browser only (DOM) |
| `localStorage` | object | undefined (no flag) | Browser |
| `process`, `Buffer`, `setImmediate` | undefined | present | Node only |
| `require`, `module`, `__dirname` | undefined | present in CommonJS files | Node (CommonJS) |
| `global` | undefined | object | Node only |
| `fetch`, `URL`, `TextEncoder`, `AbortController` | present | present | Shared web standards |
| `structuredClone`, `queueMicrotask`, `performance`, `crypto` | present | present | Shared web standards |
| `WebSocket`, `BroadcastChannel` | present | present | Shared web standards |
| `navigator` | object | object (`Node.js/24` user agent) | Both (Node's is partial) |
| `globalThis` | object | object | Both |

The takeaway is encouraging: Node has adopted many **web-standard globals** — its documentation lists
`fetch`, `Request`/`Response`, `URL`, `AbortController`, `TextEncoder`, `structuredClone`, `Blob`,
`BroadcastChannel`, streams, and `crypto` among them — so code using only those can run in both places
(this is called *isomorphic* or *universal* code). The environment-specific APIs (DOM in the browser;
`fs`, `process`, `Buffer` in Node) are where code stops being portable.

### `globalThis`: One Name for the Global Object

The global object has been `window` in pages, `self` in workers, and `global` in Node. MDN explains that
`globalThis` was introduced to give one standard name for it:

```js
globalThis === window;   // true in a browser page
globalThis === global;   // true in Node.js
// in a worker: globalThis === self (a DedicatedWorkerGlobalScope)
```

Use `globalThis` in code meant to run anywhere. (Node's docs call `global` legacy and recommend
`globalThis`.)

### Top-Level `this` Differs Too

```js
// Node.js CommonJS file:    this === module.exports          → true
// Node.js ES module:        this                              → undefined
// Browser classic script:   this === window                   → true
// Browser module script:    this                              → undefined
```

All four were confirmed by running. Module code is [strict](../execution-context-and-hoisting/strict-mode.md)
and has no implicit global `this`.

### Detecting the Environment

Test for the capability, not a name — but when you must know where you are, check for the defining
objects:

```js
const isNode = typeof process !== "undefined" && process.versions?.node != null;
const isBrowser = typeof window !== "undefined" && typeof document !== "undefined";
// Node.js → isNode: true,  isBrowser: false
// Browser → isNode: false, isBrowser: true
```

## 📚 Two Module Systems in Node

### CommonJS (CJS)

The original Node format. Per Node's docs, each file is wrapped in a function so top-level variables stay
private:

```js
(function (exports, require, module, __filename, __dirname) { /* your file */ });
```

That wrapper is why `require`, `module`, `exports`, `__filename`, and `__dirname` appear to be globals even
though, as the docs put it, they are not — they are per-module parameters. A CommonJS module exports with
`exports.name = …` or `module.exports = …` and loads with `require()`, **synchronously**.

### ES Modules (ESM)

The standard format, shared with browsers: `import`/`export`, always strict, asynchronous loading. Node
treats a file as ESM if it has a `.mjs` extension or its nearest `package.json` has `"type": "module"`;
`.cjs` or `"type": "commonjs"` forces CommonJS. In an ES module the CommonJS globals do not exist:

```js
// in an .mjs file
typeof require;           // "undefined"
typeof module;            // "undefined"
typeof __dirname;         // "undefined"

import.meta.url;         // "file:///…/this-file.mjs"
import.meta.dirname;      // the directory path (string)   — replaces __dirname
import.meta.filename;     // the file path (string)        — replaces __filename

undeclared = 1;           // ReferenceError — modules are strict
```

(`import.meta.dirname` and `import.meta.filename` are documented in Node's ESM guide; for older Node
versions use `fileURLToPath(import.meta.url)`.)

### Making the Two Work Together

- **ESM importing CommonJS** always works through the **default** import (`module.exports`):

```js
// lib.cjs:  module.exports = { named: "n", other: 1 };
import cjs from "./lib.cjs";
console.log(cjs);                 // { named: 'n', other: 1 }
const { named } = cjs;            // destructure from the default
```

  *Named* imports from CommonJS depend on Node **statically analyzing** the source to guess its exports,
  which its docs describe as covering many common patterns — and only heuristically. Tested:

```js
import { named, other } from "./lib-exports.cjs";   // lib: exports.named = "n"; exports.other = 1;   → works
import { named }        from "./lib-shorthand.cjs"; // lib: const named = "n"; module.exports = { named };  → works
import { named }        from "./lib-literal.cjs";   // lib: module.exports = { named: "n", other: 1 };   → fails
// SyntaxError: Named export 'named' not found. The requested module './lib-literal.cjs' is a CommonJS module,
//              which may not support all module.exports as named exports.
```

  When in doubt, use the default import and destructure.

- **CommonJS loading ESM.** Historically impossible with `require`; use dynamic `import()`, which returns a
  promise and works from CommonJS:

```js
import("./esm-dep.mjs").then((m) => console.log(m.answer));   // 42
```

  Node's docs now state that `require()` of an ES module works **without a flag** (unflagged in v22.12.0
  and v23.0.0), with one restriction: the module — and everything it imports — must be fully synchronous.
  With a top-level `await` inside, `require()` throws `ERR_REQUIRE_ASYNC_MODULE`. Confirmed:

```js
const ns = require("./esm-dep.mjs");
console.log(Object.keys(ns), ns.default());   // [ '__esModule', 'answer', 'default' ] hi from ESM
require("./esm-tla.mjs");                      // ERR_REQUIRE_ASYNC_MODULE (it contains top-level await)
```

For new code, write ES modules; it is the format browsers, bundlers, and Node all share
([javascript-modules.md](../asynchronous-programming-and-modules/javascript-modules.md)).

## ⏱️ The Event Loop Differs, Too

Both runtimes use an event loop ([event-loop](../event-loop/)), but the surrounding machinery differs. A
browser interleaves it with **rendering** (`requestAnimationFrame`, style, layout, paint). Node has its own
phases and extras such as `setImmediate` and `process.nextTick`, described in
[timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md). Code that depends on the
exact ordering of `setTimeout(fn, 0)` relative to `setImmediate` from the main module is non-deterministic
in Node.

## 🔐 Security Model

A browser runs untrusted code from the internet, so it **sandboxes** it: no file system, no arbitrary
processes, same-origin and CORS rules for network access. Node.js runs *your* code with the operating-system
permissions of the process, so a dependency can read your files and make network calls — which is why
[supply-chain care](../../../web-security/security-in-practice/) matters for server-side JavaScript. Deno
makes the opposite default choice, denying file, network, and environment access unless granted.

## 🧭 Writing Portable Code

- Use **web-standard APIs** (`fetch`, `URL`, `AbortController`, `TextEncoder`) rather than
  environment-specific ones when you want one code base for both.
- Reference the global through **`globalThis`**.
- Keep environment-specific code (DOM, `fs`) in separate modules behind a small interface, and choose the
  implementation at build time or via a feature check.
- Use **ES modules** and `import.meta` rather than CommonJS globals.
- Set `"type"` in `package.json` deliberately, and use `.mjs`/`.cjs` when mixing.

## 🎤 Interview Angle

- **"What is the difference between Node.js and the browser?"** Same language (and often the same V8
  engine), different runtimes: the browser provides the DOM and sandboxed web APIs; Node provides the file
  system, processes, and networking with full OS access.
- **"What is `globalThis`?"** The standard name for the global object across environments (`window`, `self`,
  `global`).
- **"CommonJS vs. ES modules?"** CommonJS: `require`/`module.exports`, synchronous, wrapper-function
  scope; ESM: `import`/`export`, static, asynchronous, always strict, with `import.meta`.
- **"Why is `__dirname` undefined in my ES module?"** ESM has no CommonJS wrapper; use `import.meta.dirname`.
- **"Can you `require()` an ES module?"** In current Node, yes if it has no top-level `await`; otherwise
  use `import()`.

## Common Mistakes

- **Using `window` or `document` in code that also runs on the server** (and crashing during
  server-side rendering).
- **Using `__dirname`/`require` inside ES modules.**
- **Assuming named imports from a CommonJS package always work.**
- **Assuming a Node.js feature (`Buffer`, `process.env`) exists in the browser**, or the reverse.
- **Mixing `.js` module types without setting `"type"`**, then fighting resolution errors.

## Module Summary

Across this module: an **engine** like V8 interprets your code to bytecode and speculatively optimizes hot
functions with Sparkplug, Maglev, and TurboFan, deoptimizing when type assumptions break — and consistent
object shapes keep property access fast (see
[javascript-engines-and-jit-compilation.md](javascript-engines-and-jit-compilation.md)); **garbage
collection** frees only what is unreachable, using a cheap generational design (see
[memory-management-and-garbage-collection.md](memory-management-and-garbage-collection.md)); **leaks** are
reachable-but-unneeded memory — unbounded caches, uncleared timers, unremoved listeners, over-capturing
closures, detached DOM — found with heap snapshots and fixed by pairing every start with a stop (see
[finding-and-fixing-memory-leaks.md](finding-and-fixing-memory-leaks.md)); **transpilers** rewrite
unsupported syntax and **polyfills** supply missing APIs, both driven by honest browser targets (see
[transpilers-polyfills-and-browser-support.md](transpilers-polyfills-and-browser-support.md));
**bundlers** combine modules and use **tree shaking** (ES modules only, honoring `sideEffects`),
**minification**, **code splitting**, and **source maps** to ship less (see
[bundlers-tree-shaking-and-minification.md](bundlers-tree-shaking-and-minification.md)); and
**runtimes** — browsers, Node.js, Deno, Bun — wrap an engine with different APIs, global objects, and
module systems, so portable code sticks to web standards and `globalThis` (see this file).

## ➡️ Next

Continue to the Modern JavaScript Additions module (extending the existing Modern JavaScript module with
ES2020+ features), the next module in this section.
