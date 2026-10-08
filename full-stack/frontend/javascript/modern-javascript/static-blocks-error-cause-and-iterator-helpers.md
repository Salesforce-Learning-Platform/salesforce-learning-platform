# 🧱 Static Blocks, Error Cause, and Iterator Helpers

## Three More Recent Additions Worth Knowing

This file covers three newer language features that each solve a specific, recurring problem: running
**multi-step initialization for a class** (static initialization blocks), **keeping the original error
when you re-throw** (`Error` `cause`), and **processing sequences lazily** (iterator helpers). It ends with
a short table of very recent additions to watch. Everything shown was executed in Node.js 24 and, where it
applies, in a real browser.

## 🏗️ Class Static Initialization Blocks

A `static` field can only hold a single expression. When setting up a class needs several statements —
conditional logic, a `try`/`catch`, or reading private state — a **static initialization block** runs
arbitrary code once, when the class is defined:

```js
class Config {
  static #defaults = { retries: 3 };
  static settings;

  static {
    // runs once, at class definition time; `this` is the class itself
    Config.settings = { ...Config.#defaults, loadedAt: "class definition time" };
    console.log("static block ran, this === Config:", this === Config);   // true
  }
}

console.log(Config.settings);   // { retries: 3, loadedAt: 'class definition time' }
```

MDN states the rules: the block runs synchronously during class definition, **in declaration order**
alongside static field initializers; `this` is the class constructor; and it can access the class's
**private** names — including `#defaults` above, which the block uses even though nothing outside the
class can reach it ([private-class-fields.md](../objects-in-depth/private-class-fields.md)). The order is
easy to confirm:

```js
const log = [];
class A {
  static x = (log.push("field x"), 1);
  static { log.push("block 1"); }
  static y = (log.push("field y"), 2);
  static { log.push("block 2"); }
}
console.log(log);   // [ 'field x', 'block 1', 'field y', 'block 2' ]
```

A superclass's static initialization completes before its subclasses'. Use a static block when
initialization is more than a one-liner or needs access to private statics; for simple values a plain
`static` field is clearer. MDN lists static blocks as Baseline *widely available* (since March 2023). See
[classes.md](../advanced-javascript/classes.md) for the class basics.

## 🔗 `Error` `cause`: Don't Lose the Original Error

A common pattern is catching a low-level error and throwing a higher-level one that explains *what the
program was trying to do*. Without care, the original failure — often the most useful clue — is lost.
Pass it as `cause`:

```js
function load() {
  try {
    JSON.parse("{bad");
  } catch (err) {
    throw new Error("Could not load settings", { cause: err });
  }
}

try {
  load();
} catch (e) {
  console.log(e.message);                          // Could not load settings
  console.log(e.cause.name, "-", e.cause.message);
  // SyntaxError - Expected property name or '}' in JSON at position 1 (line 1 column 2)
  console.log(e.cause instanceof SyntaxError);     // true
}
```

(The `JSON.parse` message is V8's wording, identical in Node.js and Chrome; other engines phrase it differently.)

MDN notes the cause can be **any value**, not only an `Error` (`new Error("outer", { cause: { code: 42 } })`
has `.cause` equal to `{ code: 42 }`), and it is an *own property only if you supply it* — a plain
`new Error("x")` has no `cause`. Runtimes and logging tools display chained causes, so the full story
survives into your logs ([errors.md](../error-handling-and-debugging/errors.md) covers custom errors; the
production material on [logging](../../../production-systems/logging-in-production/) explains why the
context matters). MDN lists the feature as Baseline *widely available*.

Habit to adopt: **whenever you wrap an error, pass the original as `cause`** instead of copying only its
message.

## 🌊 Iterator Helpers

Arrays have `map`, `filter`, and friends — but iterators and generators did not, forcing a conversion to
an array first (impossible for an infinite sequence). **Iterator helpers** add those methods to all
iterators, and they are **lazy**: each value flows through the whole chain one at a time, only as far as
is actually consumed. MDN lists the helpers:

| Lazy, chainable (return a new iterator) | Consuming (return a result) |
|-----------------------------------------|------------------------------|
| `map`, `filter`, `take`, `drop`, `flatMap` | `toArray`, `reduce`, `forEach`, `some`, `every`, `find` |

```js
function* naturals() {
  let n = 1;
  while (true) yield n++;                 // an INFINITE sequence
}

const result = naturals()
  .filter((n) => n % 2 === 0)             // keep even numbers
  .map((n) => n * n)                       // square them
  .take(5)                                 // stop after five
  .toArray();

console.log(result);   // [ 4, 16, 36, 64, 100 ]
```

That would hang forever with arrays, because `naturals()` never ends; `take(5)` ends the chain once five
results have been produced. The laziness is measurable:

```js
const pulled = [];
function* source() {
  for (let i = 1; i <= 100; i++) { pulled.push(i); yield i; }
}

const first = source().map((n) => n * 2).filter((n) => n % 3 === 0).take(2).toArray();
console.log(first, pulled.length);   // [ 6, 12 ] 6
```

The source could produce 100 values, but only the first **6** were ever generated — just enough to find two
that passed the filter. An array pipeline would have processed all 100 at every step.

The helpers exist on any iterator, including those from arrays, sets, and maps, and `Iterator.from()`
wraps any object with a `next()` method so it gains them:

```js
console.log([10, 20, 30, 40].values().drop(1).take(2).toArray());   // [ 20, 30 ]
console.log([1, 2, 3].values().reduce((a, b) => a + b));            // 6
console.log([1, 2, 3].values().some((n) => n > 2));                 // true
console.log(Iterator.from({ next() { return { done: true }; } }).toArray());   // []
```

Note the starting point: helpers are on **iterators** (the result of `.values()`, a generator call, etc.),
not on arrays themselves. `[1, 2, 3].map(...)` is the array method; `[1, 2, 3].values().map(...)` is the
lazy iterator helper. See [iterators-and-generators.md](../additional-javascript-topics/iterators-and-generators.md)
for the underlying protocol and [async-iterators-and-for-await.md](../advanced-async-patterns/async-iterators-and-for-await.md)
for the asynchronous cousin.

Availability: iterator helpers are the newest of the three. MDN's page for `Iterator.prototype.map()` marks
it Baseline *newly available* (since March 2025), meaning it works in the latest browsers but may be missing
in older ones, and the other helpers in the table above were present in both Node.js 24.19 and the test
Chrome 152. MDN's `Iterator` page lists a few more helpers — `includes()`, `join()`, `chunks()`, and
`windows()` — and flags `chunks()` as experimental; none of the four existed in either test engine, so do
not rely on them yet. **Check MDN's compatibility table for each helper** before using it
where older environments matter.

## 👀 Other Recent Additions to Watch

These existed in the engines used for testing (Node.js 24 and a current Chromium); treat them as
"check before using" rather than universally available:

| Feature | What it does |
|---------|--------------|
| `Promise.try(fn)` | Runs `fn` and returns a promise even if `fn` throws synchronously (`Promise.try(() => { throw … })` becomes a rejection) |
| `RegExp.escape(string)` | Escapes a string for safe use inside a regular expression |
| `Float16Array` | A typed array of 16-bit floats |
| `Set` methods (`union`, `intersection`, …) | Covered in [map-and-set.md](../built-in-objects-and-collections/map-and-set.md) |
| `Array.fromAsync`, `Promise.withResolvers` | Covered in the async modules |

Runtimes also differ from each other. `Uint8Array.fromBase64` and `Math.sumPrecise` were `undefined` in
Node.js 24.19 yet were functions in the test Chrome 152 — a reminder that "standardized" does not mean
"in every runtime you ship to." The reliable process: check MDN's compatibility table and the
[Baseline](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility) status, test in your
actual targets, and add a [polyfill or fallback](../how-javascript-runs/transpilers-polyfills-and-browser-support.md)
where needed.

## 🎤 Interview Angle

- **"What is a static initialization block?"** A `static { … }` block in a class that runs once at class
  definition time, in order with static fields, with `this` as the class and access to private statics.
- **"How do you preserve the original error when re-throwing?"** `throw new Error("context", { cause: err })`
  and read it back from `error.cause`.
- **"What are iterator helpers, and why are they lazy?"** Methods like `map`, `filter`, and `take` on
  iterators; they pull one value at a time through the chain, so infinite sequences and early exits work
  without building intermediate arrays.
- **"Difference between `[1,2,3].map` and `[1,2,3].values().map`?"** The first is eager and returns an
  array; the second is lazy and returns an iterator.

## Common Mistakes

- **Using a static block for one-line initialization** where a static field suffices.
- **Re-throwing a new error without `cause`**, losing the stack and message of the original.
- **Calling iterator helpers directly on arrays** (`[1, 2, 3].take(2)` does not exist; use `.values()`).
- **Forgetting to end an infinite pipeline** with `take`, `find`, or `some`.
- **Assuming a newly standardized feature exists in every runtime.**

## ➡️ Next

Continue to the [JavaScript Interview Puzzles](../interview-puzzles/README.md) module, the next module in
this section, which tests everything in this section with "predict the output" exercises.
