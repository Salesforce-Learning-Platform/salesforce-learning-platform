# 🏎️ How JavaScript Runs: Engines, Memory, and Tooling

## 📚 Overview

This module looks under the hood of JavaScript programs: how an engine such as V8 interprets and
optimizes your code, how garbage collection decides what memory to reclaim, how memory leaks arise and
are found, how transpilers and polyfills make modern code run on older browsers, how bundlers shrink and
split what ships, and how the runtimes — browsers and Node.js — differ in globals, modules, and security.
Every claim is backed by a real experiment: V8's own diagnostic flags, forced garbage collections, real
Babel and esbuild output, and the same probes run in a browser and in Node.js.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Describe the Ignition → Sparkplug → Maglev → TurboFan pipeline, read basic bytecode, and explain
  optimization, deoptimization, and why object shape matters.
- Explain reachability-based garbage collection and V8's generational design, and measure memory use.
- Recognize the common causes of memory leaks, reproduce them, and use heap snapshots to find and fix them.
- Distinguish transpilers from polyfills, configure targets with Browserslist, and decide what to support
  using Baseline and feature detection.
- Explain tree shaking (and why it needs ES modules and respects `sideEffects`), minification, source
  maps, code splitting, and content hashing.
- Compare the browser and Node.js runtimes, including globals, `globalThis`, CommonJS vs. ES modules, and
  how to write portable code.

## 📋 Prerequisites

- [The Event Loop](../event-loop/) — the runtime's scheduling model underlies the runtime comparison.
- [Execution Context, Hoisting and Strict Mode](../execution-context-and-hoisting/) — how code is run at the language level.
- [JavaScript Modules](../asynchronous-programming-and-modules/javascript-modules.md) — bundling and the CommonJS/ESM discussion assume them.
- [Built-in Objects and Collections](../built-in-objects-and-collections/) — weak references, used in the GC and leak experiments.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [javascript-engines-and-jit-compilation.md](javascript-engines-and-jit-compilation.md) | V8's tiers, bytecode, optimization and deoptimization traces, hidden classes |
| [memory-management-and-garbage-collection.md](memory-management-and-garbage-collection.md) | Reachability, mark-and-sweep, generational GC, `--trace-gc`, measuring memory |
| [finding-and-fixing-memory-leaks.md](finding-and-fixing-memory-leaks.md) | Six common leaks reproduced with numbers, heap snapshots, and fix patterns |
| [transpilers-polyfills-and-browser-support.md](transpilers-polyfills-and-browser-support.md) | Real Babel/esbuild output, polyfills, Browserslist, Baseline |
| [bundlers-tree-shaking-and-minification.md](bundlers-tree-shaking-and-minification.md) | Real bundles: tree shaking, `sideEffects`, minification, source maps, code splitting |
| [javascript-runtimes-browser-vs-nodejs.md](javascript-runtimes-browser-vs-nodejs.md) | Globals probed in both, `globalThis`, CommonJS vs. ESM and their interop; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** the leaks and bundling files if you ship real applications — leak-hunting and bundle-size
work are everyday front-end and Node.js tasks — and the runtime comparison for any full-stack role.

**Skim** the engine file unless you are interested in performance internals or interviews that probe them;
its practical conclusion ("measure first, keep hot-path types and shapes stable") fits in a sentence.

## 🧠 Knowledge Check

<details>
<summary>Why does a V8 function that was optimized for numbers get <em>deoptimized</em> when you call it with strings?</summary>

Optimization is speculative. The compiler specialized the function for the types it had observed (small
integers), inserting guards for that assumption. When strings arrive the guard fails, so V8 discards the
optimized code ("bailout … not a Smi") and falls back to the interpreter, which handles any type. If the
function stays hot, V8 optimizes it again.

</details>

<details>
<summary>Why did importing one function from <code>lodash</code> produce a 72 KB bundle but importing it from <code>lodash-es</code> only 3.4 KB?</summary>

Tree shaking relies on the static structure of ES modules. `lodash` is a CommonJS package, whose
`require`/`module.exports` are dynamic, so the bundler cannot tell which parts are used and must include
all of it. `lodash-es` uses `import`/`export`, so the bundler can include only `debounce` and its
dependencies.

</details>

## 📚 References

- [V8 blog: Launching Ignition and TurboFan](https://v8.dev/blog/launching-ignition-and-turbofan), [Sparkplug](https://v8.dev/blog/sparkplug), [Maglev](https://v8.dev/blog/maglev), and [hidden classes](https://v8.dev/docs/hidden-classes) — V8's pipeline and object model.
- [V8 blog: Trash talk — the Orinoco garbage collector](https://v8.dev/blog/trash-talk) and [MDN: Memory management](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Memory_management) — garbage collection.
- [Chrome DevTools: Memory problems](https://developer.chrome.com/docs/devtools/memory-problems), [Node.js `v8` module](https://nodejs.org/api/v8.html), and [Node.js events](https://nodejs.org/api/events.html) — finding leaks and the `MaxListeners` warning.
- [Babel: `@babel/preset-env`](https://babeljs.io/docs/babel-preset-env), [Browserslist](https://github.com/browserslist/browserslist), [core-js](https://github.com/zloirock/core-js), [MDN: Polyfill](https://developer.mozilla.org/en-US/docs/Glossary/Polyfill), [MDN: Baseline](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility), and [Can I Use](https://caniuse.com/) — compatibility tooling.
- [MDN: Tree shaking](https://developer.mozilla.org/en-US/docs/Glossary/Tree_shaking), [webpack: Tree shaking](https://webpack.js.org/guides/tree-shaking/), and [esbuild API](https://esbuild.github.io/api/) — bundling concepts and the tool used in the examples.
- [Node.js: Modules (CommonJS)](https://nodejs.org/api/modules.html), [ES modules](https://nodejs.org/api/esm.html), [globals](https://nodejs.org/api/globals.html), and [MDN: `globalThis`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis) — runtime differences.
- [Deno](https://deno.com/) and [Bun](https://bun.sh/) — the other major runtimes.
- [javascript.info: Garbage collection](https://javascript.info/garbage-collection) — a widely used walkthrough of reachability.

## ➡️ Continue Your Learning Path

Continue to the Modern JavaScript Additions module (extending the existing Modern JavaScript module with
ES2020+ features), the next module in this section.
