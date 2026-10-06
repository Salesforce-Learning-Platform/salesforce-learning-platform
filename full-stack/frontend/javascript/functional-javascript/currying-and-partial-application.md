# 🍛 Currying and Partial Application

## Two Related Ideas That Are Often Confused

Both techniques build a *specialized* function out of a general one by supplying arguments in
stages. They differ in what they promise:

```
CURRYING             transforms f(a, b, c) into f(a)(b)(c) — a chain of
                     functions that each take ONE argument.

PARTIAL APPLICATION  fixes SOME arguments of f now and returns a function
                     that takes the REST — in a single further call.
```

Both depend on closures ([closures.md](../functions/closures.md)): each returned function remembers
the arguments supplied so far.

## 🔗 Currying by Hand

```js
const curriedAdd = (a) => (b) => (c) => a + b + c;

console.log(curriedAdd(1)(2)(3));   // 6

const addOne = curriedAdd(1);       // a specialized function, ready to reuse
console.log(addOne(2)(3));          // 6
```

Each call returns another function until all three arguments have arrived, then the final sum is
computed.

## 🏭 A General `curry` Helper

Writing every function in nested-arrow form is awkward. A helper can curry any ordinary function by
using its declared parameter count, `fn.length`:

```js
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);                 // enough arguments: call the original
    }
    return function (...moreArgs) {
      return curried.apply(this, [...args, ...moreArgs]);   // otherwise keep collecting
    };
  };
}

const add3 = curry((a, b, c) => a + b + c);

console.log(add3(1)(2)(3));   // 6
console.log(add3(1, 2)(3));   // 6
console.log(add3(1)(2, 3));   // 6
console.log(add3(1, 2, 3));   // 6
```

This version is more flexible than strict one-argument-at-a-time currying: you may supply any number
of arguments per call, and it only runs the function once enough have arrived.

### The `fn.length` Caveat

`fn.length` is the number of declared parameters, but MDN specifies that rest parameters are not
counted, and that only the parameters *before the first one with a default value* count:

```js
console.log(((a, b) => {}).length);        // 2
console.log(((a, b = 2) => {}).length);    // 1
console.log(((...r) => {}).length);        // 0
console.log(((a, ...r) => {}).length);     // 1
console.log(((a, b = 1, c) => {}).length); // 1
```

So `curry` misjudges functions with defaults or rest parameters:

```js
const c = curry((a, b = 2) => a + b);
console.log(c(1));   // 3 — it ran immediately instead of waiting for `b`
```

When a function has optional parameters, give `curry` the arity explicitly. A one-line change —
`function curry(fn, arity = fn.length)`, comparing `args.length >= arity` — handles it:

```js
const c = curry((a, b = 2) => a + b, 2);   // treat it as a two-argument function
console.log(typeof c(1));                   // "function" — now it waits for `b`
console.log(c(1)(5), c(1, 5));              // 6 6
```

## ✂️ Partial Application

Fixing the first few arguments, then supplying the rest in one go:

```js
function partial(fn, ...preset) {
  return (...later) => fn(...preset, ...later);
}

const greet = (greeting, name) => `${greeting}, ${name}!`;

const sayHello = partial(greet, "Hello");
console.log(sayHello("Ada"));                      // Hello, Ada!
console.log(greet.bind(null, "Hello")("Grace"));   // Hello, Grace! — bind does the same
```

`bind` (see [call-apply-and-bind.md](call-apply-and-bind.md)) already provides partial application
for the leading arguments; a `partial` helper is only needed for more flexibility.

## 🆚 Currying vs. Partial Application

| | Currying | Partial application |
|---|----------|---------------------|
| What it does | Restructures a function into stages | Pre-fills some arguments |
| Result | A function (or chain) taking arguments over several calls | A function taking *all* the remaining arguments |
| Typical tool | A `curry` helper | `bind` or a `partial` helper |

They combine well: a curried function makes partial application effortless, because supplying fewer
arguments *is* partial application.

## 🎯 Where It Pays Off

The practical win is configuring a function once and reusing it where a one-argument callback is
expected — `map`, `filter`, and pipelines
([function-composition-and-pipelines.md](function-composition-and-pipelines.md)):

```js
const greaterThan = curry((min, n) => n > min);

console.log([3, 7, 10].filter(greaterThan(5)));   // [ 7, 10 ]
```

`greaterThan(5)` is a ready-made predicate; compare it with writing `(n) => n > 5` inline each time.
The benefit is real when the specialized function is reused or named, and marginal when it is used
once — extra closures and a more abstract call style are the cost.

## 🎤 Interview Angle

- **"What is currying?"** Turning `f(a, b, c)` into `f(a)(b)(c)`, so a function can be applied one
  argument at a time, with each step returning a function until all arguments are supplied.
- **"Currying vs. partial application?"** Currying changes the *shape* of a function into a chain of
  single-argument functions; partial application pre-fills some arguments and returns a function for
  the rest.
- **"Implement `curry`."** Compare collected arguments to `fn.length`; call the original when there
  are enough, otherwise return a function that collects more.
- **A well-known variant — `sum(1)(2)(3)()`:** with no declared arity, an empty call signals the
  end:

```js
function sum(a) {
  return function next(b) {
    return b === undefined ? a : sum(a + b);
  };
}

console.log(sum(1)(2)(3)());   // 6
```

## Common Mistakes

- **Using `curry` on functions with default or rest parameters**, where `fn.length` undercounts.
- **Currying everything by habit** — it helps when a specialized function is reused, not when each
  call supplies all the arguments anyway.
- **Confusing the two terms** — a function that merely fixes the first argument is partial
  application, not currying.
- **Forgetting argument order** — put the arguments you will configure *first* (`greaterThan(min, n)`,
  not `(n, min)`), or partial application becomes awkward.

## ➡️ Next

Continue to [function-composition-and-pipelines.md](function-composition-and-pipelines.md) to chain
small, single-purpose functions into larger ones.
