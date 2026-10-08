# 🔄 Transpilers, Polyfills, and Browser Support

## Writing Tomorrow's JavaScript for Today's Browsers

The language keeps gaining features — optional chaining, class fields, new array methods — but users run
many different browsers and versions, and a browser that has never heard of `?.` will not merely ignore
it: it will refuse to run the whole file. Two different tools bridge the gap, and confusing them is the
most common mistake in this area:

```
A TRANSPILER rewrites SYNTAX    — new grammar becomes older grammar.      (a build step)
A POLYFILL  adds missing APIs   — a missing function/object gets defined. (code that runs in the browser)
```

The reason there are two is the two ways an old engine can fail. New **syntax** cannot even be *parsed*, so
it must be rewritten before delivery. A new **API** (a method such as `Array.prototype.at`) parses fine but
throws a `TypeError` when called, so it needs a stand-in at runtime.

## 🔧 Transpilers: Rewriting Syntax

Babel describes itself as a toolchain used mainly to convert ECMAScript 2015+ code into a backwards
compatible version of JavaScript for older environments. **`@babel/preset-env`** selects which
transformations to apply by comparing your **targets** against its compatibility data — so you declare
*who must be supported*, not *which features to rewrite*.

Here is one modern snippet:

```js
const user = { profile: { name: "Ada" } };
const name = user?.profile?.name ?? "anonymous";
const greet = (who) => `Hello, ${who}`;
class Counter {
  count = 0;
  inc = () => { this.count++; };
}
const merged = { ...user, extra: 1 };
async function load() { return (await fetch("/x")).json(); }
```

Compiled with `@babel/preset-env` for three targets (real output, trimmed):

**Chrome 120 — the output is the input.** Every feature is natively supported, so nothing is rewritten
(20 lines in, 20 lines out).

**Chrome 58 — 27 lines.** Optional chaining and nullish coalescing, class fields, and object spread are
rewritten, and the compiler prepends small helper functions:

```js
const name = (_user$profile$name = user === null || user === void 0 || (_user$profile = user.profile) === null
  || _user$profile === void 0 ? void 0 : _user$profile.name) !== null && _user$profile$name !== void 0
  ? _user$profile$name : "anonymous";

class Counter {
  constructor() {
    _defineProperty(this, "count", 0);                          // class fields became constructor assignments
    _defineProperty(this, "inc", () => { this.count++; });
  }
}
const merged = _objectSpread(_objectSpread({}, user), {}, { extra: 1 });   // object spread via a helper
```

The arrow function, template literal, and `async`/`await` survive untouched — Chrome 58 already supports them.

**Chrome 49 — 45 lines.** Now even `async`/`await` is rewritten (via a generator-based helper and a
bundled `regenerator` runtime), `const` becomes `var`, and the helper block grows to dozens of lines.

The lesson is the **cost curve**: the older your targets, the more code you ship and the more runtime
helper work the browser does. A single `a?.b ?? c` shows it in miniature with esbuild:

```
target es2015  =>  var _a; const v = (_a = a == null ? void 0 : a.b) != null ? _a : c;
target es2020  =>  const v = a?.b ?? c;
```

So **set targets honestly**. Supporting a browser nobody uses taxes everyone else with bigger,
slower bundles.

### Where Targets Come From: Browserslist

Rather than repeating a target list in every tool, projects declare one **Browserslist** query that Babel,
Autoprefixer, ESLint plugins, and others all read. It lives in the `browserslist` key of `package.json` or
in a `.browserslistrc` file, and queries combine with "or":

```
> 0.5%, last 2 versions, not dead
```

Running `npx browserslist` lists exactly which browsers a query selects, so you can check it against your
analytics before committing to it.

### Types Are Just Erased

TypeScript and similar tools transpile too — mostly by *deleting* type annotations. esbuild turns

```ts
const n: number = 'oops' as unknown as number; interface A { x: string } function f(a: A): string { return a.x; }
```

into plain JavaScript with the types simply removed:

```js
const n = "oops";
function f(a) {
  return a.x;
}
```

Notice that nothing complained about assigning `"oops"` to a `number`: **bundler-style transpilers do not
type-check.** Running `tsc` (or your editor) for type errors is a separate step; see
[TypeScript with JavaScript projects](../../typescript/typescript-essentials/typescript-with-javascript-projects.md).

## 🩹 Polyfills: Supplying Missing APIs

MDN defines a polyfill as a piece of code, usually JavaScript on the web, that provides modern
functionality on older browsers that do not natively support it. A transpiler *cannot* do this job:
rewriting syntax does nothing for a method that doesn't exist on `Array.prototype`.

A polyfill is **feature-detected** — it only installs itself if the feature is missing, so modern browsers
keep their faster native version. Here is `Array.prototype.at` as a small example. To test it, the script
first deleted the native method to imitate an old engine:

```js
// (simulating an old engine: delete Array.prototype.at;)
console.log(typeof [].at);                 // undefined

if (!Array.prototype.at) {                 // feature detection: only add it when missing
  Object.defineProperty(Array.prototype, "at", {
    value: function at(index) {
      const i = Math.trunc(index) || 0;
      const k = i < 0 ? this.length + i : i;
      return this[k];
    },
    writable: true,
    configurable: true,                    // enumerable defaults to false, so for...in is unaffected
  });
}

console.log(typeof [].at, [1, 2, 3].at(-1), [1, 2, 3].at(0), [1, 2, 3].at(9));   // function 3 1 undefined
```

Two details worth copying from that snippet: define the method with `Object.defineProperty` so it is
**non-enumerable** (an assigned `Array.prototype.at = …` would show up in every `for...in` over an array,
as covered in [property-descriptors-and-getters-setters.md](../objects-in-depth/property-descriptors-and-getters-setters.md)),
and always guard with a detection check.

In real projects you don't hand-write polyfills; you use **core-js**, a large library of standards-compliant
polyfills. Babel's `@babel/preset-env` does **not** polyfill by default — per its docs, polyfills come from
core-js through the `useBuiltIns` and `corejs` options (and note that Babel 8 removes `useBuiltIns`, so
check the docs for your version). Only polyfill what your targets need; core-js can add a lot of weight.

## 🧪 Feature Detection, Not Browser Sniffing

Decide with the *feature*, never with the browser's name or version string:

```js
if (typeof structuredClone === "function") {
  copy = structuredClone(value);
} else {
  copy = fallbackClone(value);             // your own fallback or a polyfill
}

if ("IntersectionObserver" in window) { /* use it */ } else { /* load everything eagerly */ }
```

User-agent strings are unreliable and change; a direct test of "does this exist?" is always accurate. In
CSS the equivalent is `@supports`.

## 🧭 Deciding What to Support

- **Baseline.** MDN's Baseline label summarizes cross-browser support for a feature. *Widely available*
  means it has worked in every Baseline browser for at least 30 months (two and a half years) — a safe
  default to use freely. *Newly available* features work in the latest versions of each major browser but
  may fail in older ones, so use them where you can tolerate that or progressively enhance. *Limited
  availability* features need fallbacks. Baseline does not cover older devices, webviews, or assistive
  technology, which you must test separately.
- **Can I Use** ([caniuse.com](https://caniuse.com/)) shows browser support tables for individual features.
- **Your analytics** are the real authority: support the browsers your users actually have.
- **Progressive enhancement** — build a working baseline, then layer on newer capabilities where they
  exist — costs far less than transpiling everything for the oldest browser.

## 📊 Summary

| | Transpiler | Polyfill |
|---|-----------|----------|
| Fixes | New **syntax** | Missing **APIs** |
| When | Build time | Runtime (in the browser) |
| Examples | Babel, esbuild, SWC, `tsc` | core-js, hand-written feature-detected shims |
| Cost | Bigger code, helper functions | Extra bytes loaded and parsed |
| Input | Your targets (Browserslist) | Your targets and a detection check |

## 🎤 Interview Angle

- **"Transpiler vs. polyfill?"** A transpiler rewrites unsupported *syntax* at build time; a polyfill
  supplies a missing *API* at runtime. You often need both.
- **"What does `@babel/preset-env` do?"** Compiles modern syntax down to what the declared targets
  (Browserslist) need; polyfills are separate (core-js).
- **"Why can't Babel make `Array.prototype.at` work?"** It's a missing function, not unparseable syntax;
  a polyfill must define it.
- **"How do you decide what to support?"** Browser analytics, Browserslist targets, and Baseline status.
- **"Why feature-detect instead of checking the user agent?"** UA strings are unreliable; detection tests
  the capability itself.

## Common Mistakes

- **Expecting a transpiler to add APIs**, then hitting `TypeError: … is not a function` in old browsers.
- **Targeting very old browsers by default**, inflating every user's bundle.
- **Polyfilling everything** instead of only what the targets need.
- **Sniffing the user agent** rather than feature-detecting.
- **Assuming Babel/esbuild type-check TypeScript.**
- **Defining polyfilled methods by plain assignment**, making them enumerable.

## ➡️ Next

Continue to [bundlers-tree-shaking-and-minification.md](bundlers-tree-shaking-and-minification.md) to see
how the transformed modules are combined, pruned, and shrunk into what actually ships.
