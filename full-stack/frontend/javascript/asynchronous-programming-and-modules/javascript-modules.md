# JavaScript Modules

## The Problem: One Giant File Doesn't Scale

Without modules, every script sharing a page shares one single global scope — any variable
declared at the top level of any script is visible (and can conflict) with every other script on
the page. Modules solve this by giving each file its **own** scope, with explicit `export`/`import`
statements controlling exactly what's shared between files.

## Named Exports and Imports

```js
// math.js
export function add(a, b) { return a + b; }
export function subtract(a, b) { return a - b; }

// app.js
import { add, subtract } from "./math.js";
add(2, 3); // 5
```

Named exports allow a module to share multiple, individually named values — imports must reference
those exact names (though they can be renamed with `as`: `import { add as sum } from "./math.js"`).

## Default Exports

```js
// User.js
export default class User {
  constructor(name) { this.name = name; }
}

// app.js
import User from "./User.js"; // any name works for a default import
```

A module can have **one** default export, imported without curly braces and under any name the
importer chooses — commonly used when a module's primary purpose is exporting exactly one main
thing (a single class, a single component).

## Mixing Named and Default Exports

```js
export default function App() { /* ... */ }
export const version = "1.0.0";

import App, { version } from "./App.js";
```

## Module Files Run Once, Are Cached

Importing the same module multiple times from different files doesn't re-execute it each time —
JavaScript caches the module's result after its first evaluation and reuses it for every subsequent
import, which is why module-level state (a value defined at a module's top level) is genuinely
shared across every file that imports it.

## Dynamic Imports

```js
button.addEventListener("click", async () => {
  const { showModal } = await import("./modal.js");
  showModal();
});
```

`import()` (as a function call, not the static `import` statement) loads a module **on demand**,
returning a Promise — useful for loading code only when it's actually needed (like a modal that
most visitors never open), rather than including it in the initial page load unconditionally. This
is the underlying mechanism behind code-splitting, covered in more depth in React's
performance-optimization module.

## Common Mistakes

- Using more than one default export in a single module — only one is allowed per file.
- Assuming importing the same module twice runs its top-level code twice — it's cached and
  evaluated only once, then reused.
- Overusing dynamic `import()` for code that's actually needed immediately on every page load,
  adding unnecessary complexity where a normal static `import` would be simpler and sufficient.

## Module Summary

Across this module: callbacks are JavaScript's original async mechanism but scale poorly for
chained operations (see [callbacks.md](callbacks.md)); Promises provide a consistent, chainable
interface with unified error handling via `.catch()` (see [promises.md](promises.md));
`async`/`await` is syntax built directly on Promises that reads like synchronous code, with
ordinary `try`/`catch` handling rejections (see [async-await.md](async-await.md)); the Fetch API
is the standard way to make HTTP requests, with the critical gotcha that HTTP error statuses don't
reject the Promise on their own (see [fetch-api.md](fetch-api.md)); and JavaScript modules give
each file its own scope, with `export`/`import` (including dynamic `import()`) controlling exactly
what's shared between files.
