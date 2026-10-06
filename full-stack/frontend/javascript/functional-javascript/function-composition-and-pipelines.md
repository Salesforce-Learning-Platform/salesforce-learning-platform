# 🔗 Function Composition and Pipelines

## Building Big Behavior From Small Functions

**Composition** combines small functions into a new one, feeding each function's output into the
next. Instead of one long function that trims, lowercases, and slugifies a string, you write three
tiny functions that are each easy to test, and join them. That is the payoff of everything in this
module so far: [higher-order functions](higher-order-functions.md) let a function build functions,
and [currying](currying-and-partial-application.md) lets you shape them to fit.

## ➕ `compose` and `pipe`

```js
const compose = (...fns) => (x) => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe    = (...fns) => (x) => fns.reduce((acc, fn) => fn(acc), x);
```

Both take functions and return a new function. They differ only in direction:

```
compose(f, g, h)(x)   =   f(g(h(x)))       reads right to left, like math
pipe(f, g, h)(x)      =   h(g(f(x)))       reads left to right, like steps
```

```js
const inc = (x) => x + 1;
const double = (x) => x * 2;

console.log(compose(double, inc)(5));   // 12 — double(inc(5))
console.log(pipe(double, inc)(5));      // 11 — inc(double(5))
```

Same two functions, different order, different answers — so the order is part of the design. Many
people prefer `pipe` because the code reads in the order the work happens.

## 🧪 A Realistic Example: Building a URL Slug

```js
const trim = (s) => s.trim();
const toLower = (s) => s.toLowerCase();
const slugify = (s) => s.replace(/\s+/g, "-");

const toSlug = pipe(trim, toLower, slugify);

console.log(toSlug("  Hello Functional World "));   // hello-functional-world
```

`toSlug` is itself a function, so it can be passed to `map`, composed again, or tested alone. Each
step stays tiny and independently testable — and changing the process (say, adding an
accent-stripping step) means inserting one function into the list.

## 1️⃣ Why Pipeline Steps Take One Argument

`pipe` passes exactly one value from step to step, so every function in it must accept one argument
and return one value. Functions that naturally need more arguments are adapted with the earlier
techniques — [partial application or currying](currying-and-partial-application.md):

```js
const add = curry((a, b) => a + b);   // `curry` from the previous file

console.log(pipe(add(1), double)(5));   // 12 — add(1) is a one-argument function
```

## 🔍 Debugging a Pipeline With `tap`

A pipeline hides its intermediate values. A tiny helper that logs and passes the value along lets
you inspect any step without changing the result:

```js
const tap = (label) => (x) => {
  console.log(label, x);
  return x;                       // pass the value through unchanged
};

console.log(pipe(trim, tap("after trim"), toLower)("  Hi  "));
// after trim Hi
// hi
```

The `return x` is essential. Putting `console.log` itself in a pipeline breaks it, because
`console.log` returns `undefined`:

```js
pipe(trim, console.log, toLower)("  Hi  ");
// Hi
// TypeError: Cannot read properties of undefined (reading 'toLowerCase')
```

## ⏳ Composing Asynchronous Steps

Steps that return promises can be piped by chaining with `.then` (see
[promises.md](../asynchronous-programming-and-modules/promises.md)):

```js
const pipeAsync = (...fns) => (x) =>
  fns.reduce((acc, fn) => acc.then(fn), Promise.resolve(x));

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const addAsync = async (n) => {
  await wait(1);
  return n + 1;
};

pipeAsync(addAsync, addAsync, (n) => n * 10)(1).then((v) => console.log(v));   // 30
```

Each step may return a plain value or a promise; `.then` handles both.

## 🆚 Composition vs. Method Chaining

`numbers.filter(...).map(...).reduce(...)` (see
[array-methods.md](../arrays-and-objects/array-methods.md)) is composition too — but it only works
because those methods exist on arrays and return arrays. `pipe` works with *any* functions over *any*
values, including your own domain functions. The two combine naturally: a pipeline step can be a
function that runs an array chain internally.

## 🎤 Interview Angle

- **"Implement `compose` (or `pipe`)."** Use `reduce` (`reduceRight` for `compose`) to thread the
  value through the list of functions, as shown above.
- **"What is the difference between `compose` and `pipe`?"** Only the order: `compose` applies right
  to left, `pipe` left to right.
- **"Why do composed functions usually take one argument?"** Each step receives exactly the previous
  step's single return value; multi-argument functions are adapted with currying or partial
  application.

## Common Mistakes

- **Getting the order backwards** between `compose` and `pipe`.
- **Putting a side-effecting function with no return value** (like `console.log`) in a pipeline.
- **Passing multi-argument functions directly**, leaving later parameters `undefined`.
- **Over-abstracting** — a pipeline of one-line functions with cryptic names is harder to read than
  a clear three-line function; compose when it genuinely clarifies the steps.
- **Mutating the input inside a step**, which makes the whole pipeline unpredictable — see
  [pure-functions-and-immutability.md](pure-functions-and-immutability.md).

## ➡️ Next

Continue to [pure-functions-and-immutability.md](pure-functions-and-immutability.md) to see what
makes a function safe to compose, cache, and reason about.
