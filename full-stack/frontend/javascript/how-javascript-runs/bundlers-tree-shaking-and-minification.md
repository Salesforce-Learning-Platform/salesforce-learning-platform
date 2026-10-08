# 📦 Bundlers, Tree Shaking, and Minification

## From Many Modules to What Ships

You write code as many small [modules](../asynchronous-programming-and-modules/javascript-modules.md) that
`import` each other, plus dozens of third-party packages. A **bundler** follows those `import`s from an
entry point, builds the dependency graph, transforms what needs transforming (TypeScript, JSX, newer
syntax — see [transpilers-polyfills-and-browser-support.md](transpilers-polyfills-and-browser-support.md)),
and emits a few optimized files for the browser. Well-known bundlers include webpack, Rollup, esbuild, and
Parcel; the examples here use **esbuild** because it is fast and its output is easy to read. The ideas
apply to all of them.

Bundling earns its keep through more than fewer requests: it enables **tree shaking** (dropping unused
code), **minification** (shrinking what remains), **code splitting** (loading only what a page needs),
content-hashed filenames for long-term caching, and a single place to run transforms.

## 🧩 What a Bundle Looks Like

Two small modules — `main.js` uses only one of the three functions in `math.js`:

```js
// src/math.js
export function add(a, b) { return a + b; }
export function multiply(a, b) { return a * b; }
export function divide(a, b) {
  if (b === 0) throw new Error("divide by zero");
  return a / b;
}

// src/main.js
import { add } from "./math.js";
console.log(add(2, 3));
```

`esbuild src/main.js --bundle --format=esm` produces (comments are esbuild's own):

```js
// src/math.js
function add(a, b) {
  return a + b;
}

// src/main.js
console.log(add(2, 3));
```

The two modules are concatenated into one file, and `multiply` and `divide` are **gone**. That is
**tree shaking**.

## 🌳 Tree Shaking

MDN defines tree shaking as the removal of dead code. It works because ES module `import` and `export`
are **static**: a bundler can read them without running anything and know exactly which exports are used.
webpack's guide states the requirement plainly — it relies on the static structure of ES2015 module
syntax, so don't let a transpiler convert `import`/`export` to CommonJS before the bundler sees it
(with Babel's `@babel/preset-env`, set `modules: false`).

### CommonJS Cannot Be Shaken

`require()` and `module.exports` are dynamic — a bundler can't be sure which properties are used.
esbuild's documentation states that tree shaking "works with ECMAScript modules but not with CommonJS
modules." The same logic written in CommonJS:

```js
// src/cjs-math.cjs
exports.add = function add(a, b) { return a + b; };
exports.multiply = function multiply(a, b) { return a * b; };
exports.divide = function divide(a, b) { if (b === 0) throw new Error("divide by zero"); return a / b; };

// src/main-cjs.cjs
const { add } = require("./cjs-math.cjs");
console.log(add(2, 3));
```

bundled the same way keeps **all three functions**, wrapped in a module-loader helper. Minified:

```
ESM version:       48 bytes      (just add, plus the call)
CommonJS version:  326 bytes     (all three functions, plus helpers)
```

On a real library the difference is dramatic. Importing one function, `debounce`, bundled and minified:

```
lodash     (CommonJS, import _ from "lodash")              72.1 KB minified    26.3 KB gzip
lodash-es  (ES modules, import { debounce } from "lodash-es")   3.4 KB minified     1.7 KB gzip
```

Same function, roughly twenty times the size. Prefer **ES-module builds** of libraries and **named
imports** so the bundler can see what you use.

### Side Effects: The Reason Unused Imports Sometimes Stay

An `import` runs the imported file. If that file does something at its top level — logs, registers a
global, patches a prototype — dropping it would change behavior, so a bundler must keep it unless told
it's safe. Package authors declare that with the **`"sideEffects"`** field in `package.json`; webpack's
guide documents `"sideEffects": false` (no file has side effects) or a list of the files that do. A test
with a library module that logs when evaluated:

```js
// node_modules/side-lib/index.js
console.log("library module evaluated");
export const used = () => "used";
export const unused = () => "unused";

// src/main-se.js
import { used } from "side-lib";          // imported, but never used
console.log("app started");
```

```
side-lib WITHOUT "sideEffects": false  →  the bundle keeps  console.log("library module evaluated")
side-lib WITH    "sideEffects": false  →  the whole module is dropped; only "app started" remains
```

And when the import *is* used, the unused export is still removed but the side-effect statement stays:

```js
// bundle of: import { used } from "side-lib"; console.log(used());
console.log("library module evaluated");
var used = () => "used";           // `unused` was shaken away
console.log(used());
```

A warning from webpack's guide: marking a package `sideEffects: false` while it has imports that *are*
side-effect-only — CSS files are the classic case — silently drops those styles, so list such files
explicitly. (webpack also supports `/* #__PURE__ */` annotations to mark individual calls as removable.)

## 🗜️ Minification

Minification rewrites code to be as small as possible **without changing behavior**: it removes
whitespace and comments, shortens local variable and function names, and simplifies expressions.

```js
// before
// Calculates the total price including tax
export function calculateTotalPrice(basePrice, taxRate) {
  const taxAmount = basePrice * taxRate;
  const totalPrice = basePrice + taxAmount;
  return totalPrice;
}

// after (esbuild --minify)
function a(t,o){const c=t*o;return t+c}export{a as calculateTotalPrice};
```

Local names became `a`, `t`, `o`, `c`, while the **exported** name was preserved (renaming it would break
importers). Minification is a transformation of *text*; compression (gzip or Brotli, applied by the
server) is a separate step on top, and the two stack — as the lodash numbers above show, 72.1 KB minified
is 26.3 KB after gzip.

### Source Maps: Debugging Minified Code

Minified code is unreadable in a stack trace. A **source map** is a file linking positions in the output to
the original source. esbuild's `--sourcemap` emits `app.js.map` and appends a pointer comment to the bundle:

```
//# sourceMappingURL=app.js.map
```

The map is a JSON file whose keys are `version`, `sources`, `sourcesContent`, `mappings`, and `names`.
Browser DevTools (and error-reporting services) use it to show the original file and line. Decide
deliberately whether to publish source maps to the public.

## ✂️ Code Splitting

Shipping one giant bundle makes every visitor download code for pages they may never open. **Code
splitting** breaks the bundle into chunks loaded on demand, driven by dynamic `import()`:

```js
// src/main-split.js
document.getElementById("show").onclick = async () => {
  const { heavy } = await import("./heavy.js");     // loaded only when the button is clicked
  console.log(heavy().length);
};
```

`esbuild src/main-split.js --bundle --splitting --format=esm --minify --outdir=out` writes two files:

```
main-split.js
heavy-<hash>.js
```

and the main file requests the second one lazily, only when the click handler runs:

```js
document.getElementById("show").onclick=async()=>{let{heavy:o}=await import("./heavy-<hash>.js");console.log(o().length)};
```

Per esbuild's documentation, splitting currently requires the `esm` output format and an output directory
(`outdir`). Note the **hash in the chunk's filename**: it comes from the file's content, so a changed
chunk gets a new name (forcing a fresh download) and an unchanged one keeps its name and stays cached
indefinitely — the foundation of long-term caching. Frameworks expose this as route-based splitting and
lazy components; see [code-splitting.md](../../react/performance-optimization-in-react/code-splitting.md) and
[lazy-loading.md](../../react/performance-optimization-in-react/lazy-loading.md).

## 🛠️ Practical Guidance

| Goal | Do this |
|------|---------|
| Smaller bundles | Use ESM builds of libraries; use named imports; avoid importing a whole library for one helper |
| Make tree shaking possible | Keep `import`/`export` as ES modules; mark side-effect-free packages with `"sideEffects"` |
| Faster first load | Split by route/feature with dynamic `import()`; load heavy widgets on demand |
| Good caching | Content-hashed filenames; serve with long cache lifetimes |
| Debuggability | Emit source maps; upload them to your error-monitoring service rather than serving them publicly if needed |
| Know where the bytes go | Use your bundler's size report or an analyzer, and measure with the
[performance tools](../../performance/frontend-performance-fundamentals/measuring-performance.md) |

Also remember `process.env.NODE_ENV`: esbuild documents that with minification enabled it defaults to
`"production"`, which lets libraries drop their development-only checks. And put the build in your
pipeline ([CI/CD pipelines](../../../production-systems/ci-cd-pipelines/)) so every deploy is built the same
way.

## 🎤 Interview Angle

- **"What does a bundler do?"** Follows imports to build a dependency graph, transforms code, and emits
  optimized files — with tree shaking, minification, and code splitting.
- **"What is tree shaking and why does it need ES modules?"** Removing unused exports; ES `import`/`export`
  are statically analyzable, while CommonJS `require` is dynamic.
- **"What is the `sideEffects` field?"** A `package.json` flag telling bundlers which modules can be safely
  dropped when their exports are unused.
- **"Minification vs. compression?"** Minification rewrites the source to be smaller; compression
  (gzip/Brotli) encodes the bytes for transfer. They stack.
- **"Why content-hash filenames?"** So changed files get new URLs and unchanged files stay cached.

## Common Mistakes

- **Importing a whole CommonJS library** (`import _ from "lodash"`) for one function.
- **Transpiling `import` to `require` before bundling**, defeating tree shaking.
- **Marking a package `sideEffects: false` that has side-effect-only imports** (like CSS).
- **Shipping one monolithic bundle** with no splitting.
- **Never checking what's in the bundle** until the page is slow.
- **Serving source maps you didn't intend to publish**, or not uploading them to error monitoring.

## ➡️ Next

Continue to [javascript-runtimes-browser-vs-nodejs.md](javascript-runtimes-browser-vs-nodejs.md) to
compare the environments your code runs in, and how modules and globals differ between them.
