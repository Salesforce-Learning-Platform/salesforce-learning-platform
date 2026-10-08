# ⏳ Top-Level `await` and Import Attributes

## Modules That Can Wait

[async-await.md](../asynchronous-programming-and-modules/async-await.md) noted a narrow exception to the
rule that `await` needs an `async` function: **top-level `await`**. In an ES module you may use `await`
directly at the top level, so a module can finish asynchronous setup — loading configuration, connecting
to a database, initializing WebAssembly — *before* any module that imports it runs. Companion feature:
**import attributes** let a module import a JSON file directly.

## 🔝 Top-Level `await`

```js
// config.mjs
const response = await fetch("https://example.com/config.json");
export const config = await response.json();
```

```js
// main.mjs
import { config } from "./config.mjs";      // main.mjs does not run until config.mjs has finished
console.log(config.apiUrl);
```

Before this feature, the usual workaround was wrapping everything in an `async` IIFE
([iife-and-the-module-pattern.md](../functional-javascript/iife-and-the-module-pattern.md)) or exporting a
promise that every consumer had to remember to await.

### Only in Modules

Top-level `await` is allowed only at the top level of an **ES module**. In a classic script or a CommonJS
file it is a syntax error, with the same message in a browser and in Node.js:

```js
await Promise.resolve(1);
// SyntaxError: await is only valid in async functions and the top level bodies of modules
```

In a browser, use `<script type="module">`. In Node.js, use a `.mjs` file or `"type": "module"` in
`package.json` (see [javascript-runtimes-browser-vs-nodejs.md](../how-javascript-runs/javascript-runtimes-browser-vs-nodejs.md)).
A test confirmed that a module script containing `await new Promise(...)` ran to completion in a real
browser, logging "before await" then "after await".

### What Waiting Means for Other Modules

MDN states the rule precisely: modules that **import** a module using top-level `await` wait for it to
finish before running, while *sibling* modules that don't depend on it can still load in the meantime.
Four tiny modules prove it:

```js
// a.mjs — has a top-level await
console.log("a: start (has top-level await)");
await new Promise((resolve) => setTimeout(resolve, 50));
console.log("a: finished waiting");
export const fromA = "A";

// b.mjs — an independent sibling
console.log("b: runs (independent sibling, no await)");

// dependsOnA.mjs
import { fromA } from "./a.mjs";
console.log("dependsOnA: runs only after a finished, fromA =", fromA);

// main.mjs
import "./a.mjs";
import "./b.mjs";
import "./dependsOnA.mjs";
console.log("main: all dependencies ready");
```

Running `node main.mjs` prints:

```
a: start (has top-level await)
b: runs (independent sibling, no await)
a: finished waiting
dependsOnA: runs only after a finished, fromA = A
main: all dependencies ready
```

`b` ran while `a` was still waiting (it doesn't depend on `a`), but `dependsOnA` and `main` waited for it.
The whole application's startup is therefore delayed by the slowest awaited dependency on its critical path.

### When It Fails

If an awaited promise rejects, the module fails to evaluate — and so does everything importing it:

```js
// failing.mjs
await Promise.reject(new Error("config could not be loaded"));
export const x = 1;

// importsFailing.mjs
import "./failing.mjs";
console.log("never printed");
```

`node importsFailing.mjs` prints the error and exits with code `1`; the `console.log` never runs. If
failure is acceptable, handle it where it happens. A common pattern is an optional dependency with a
fallback:

```js
let marked;
try {
  ({ default: marked } = await import("this-package-does-not-exist"));
} catch {
  marked = (s) => `<p>${s}</p>`;           // simple fallback when the package isn't available
}
console.log("fallback used:", marked("hi"));   // fallback used: <p>hi</p>
```

(That uses [dynamic `import()`](../asynchronous-programming-and-modules/javascript-modules.md), which
returns a promise.)

### Good Uses and Bad Uses

| Good | Avoid |
|------|-------|
| An application's **entry module** loading config or initial data before the app starts | A **shared library module** that awaits slow work — it delays every importer |
| Initializing WebAssembly or a database connection once | Awaiting network calls that could be deferred until first use |
| Choosing an implementation with a dynamic `import()` and fallback | Anything on the critical path of page load when a lazy approach works |

Rule of thumb: top-level `await` is convenient for **applications**, risky for **libraries**. A library
that awaits at the top level forces every consumer to wait (and to be an ES module).

### Interop Limits

- **`require()` of an ES module with top-level `await` fails** with `ERR_REQUIRE_ASYNC_MODULE` in Node.js
  — load it with `import()` instead.
- **Bundlers** must support it. In a test, esbuild bundled `const x = await Promise.resolve(1)` fine for
  `--format=esm --target=es2022`, but refused otherwise:

```
--format=esm  --target=es2020  →  ERROR: Top-level await is not available in the configured target environment ("es2020")
--format=iife --target=es2022  →  ERROR: Top-level await is currently not supported with the "iife" output format
--format=cjs  --target=es2022  →  ERROR: Top-level await is currently not supported with the "cjs" output format
```

  (See [bundlers-tree-shaking-and-minification.md](../how-javascript-runs/bundlers-tree-shaking-and-minification.md).)

## 📄 Import Attributes: Importing JSON (and More)

JSON files are data, not code, so importing one needs an explicit declaration of what it is. **Import
attributes** add that declaration with the `with` keyword:

```js
import data from "./data.json" with { type: "json" };

console.log(data);          // { name: 'demo', version: 1 }
console.log(typeof data);   // object
```

MDN explains the purpose: the `type` attribute makes the import **fail** if the file isn't really JSON,
so the server (or a compromised host) can't make the browser silently execute it as JavaScript. Leave the
attribute out and the import is rejected; Node.js reports:

```
TypeError [ERR_IMPORT_ATTRIBUTE_MISSING]: Module ".../data.json" needs an import attribute of "type: json"
```

Dynamic imports take the attributes as the `with` property of a second argument:

```js
const again = await import("./data.json", { with: { type: "json" } });
console.log(again.default.name);   // demo
```

Notes:

- The keyword is **`with`**; an earlier proposal used `assert`, which MDN now describes as non-standard —
  update any old `assert { type: "json" }` code.
- The imported value is the parsed JSON, available as the **default export**.
- MDN lists other types such as `"css"` and `"text"` in the specification's scope; support varies by
  platform, so check compatibility before using anything other than `"json"`.
- MDN marks import attributes as Baseline *newly available* (since April 2025): fine for current
  browsers, but older ones and some tools may not support the syntax. A bundler or `fetch(...).then(r => r.json())`
  remains the portable alternative.

## 🎤 Interview Angle

- **"What is top-level `await`?"** The ability to use `await` at the top level of an ES module, making
  the module (and anything importing it) wait for asynchronous setup.
- **"Where can you use it?"** Only in ES modules — not classic scripts or CommonJS.
- **"How does it affect modules that import the awaiting module?"** They wait until it finishes; unrelated
  siblings are not blocked.
- **"What happens if the awaited promise rejects?"** The module fails to evaluate, and so do its importers.
- **"What are import attributes?"** The `with { type: "json" }` clause that declares how an imported file
  must be interpreted — required to import JSON modules.

## Common Mistakes

- **Putting top-level `await` in a CommonJS file** or classic script.
- **Awaiting slow work at the top of a library module**, delaying every consumer.
- **Forgetting that a rejection stops the whole import chain.**
- **Writing `import data from "./x.json"` without the `type` attribute.**
- **Using the obsolete `assert` keyword.**
- **Bundling top-level `await` into an `iife`/`cjs` output** or an older target.

## ➡️ Next

Continue to [static-blocks-error-cause-and-iterator-helpers.md](static-blocks-error-cause-and-iterator-helpers.md)
for the remaining recent additions: class static blocks, error chaining, and lazy iterator helpers.
