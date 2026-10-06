# 🔝 Higher-Order Functions

## Functions Are Values

In JavaScript a function is a value like any other: it can be stored in a variable, kept in an
object or array, passed as an argument, and returned from another function. MDN calls this being a
**first-class function**. That one property is the foundation of the whole module, because it makes
a new kind of function possible:

```
A HIGHER-ORDER FUNCTION is a function that takes one or more functions as
arguments, returns a function, or both.
```

You have been using them since [array-methods.md](../arrays-and-objects/array-methods.md) —
`map`, `filter`, and `reduce` all take a function. This file shows how to *write* them, which is
where the idea starts paying off.

## 📦 First-Class Functions in Action

```js
const double = (n) => n * 2;

const operations = { double, square: (n) => n * n };   // functions stored in an object

console.log(operations.square(4));   // 16
console.log([1, 2, 3].map(double));  // [ 2, 4, 6 ] — a function passed as an argument
```

## 📥 Taking a Function: Pass In the Behavior

A function that accepts another function lets the *caller* decide what happens, while the function
itself owns the repeated structure:

```js
function repeat(times, action) {
  for (let i = 0; i < times; i++) {
    action(i);
  }
}

repeat(3, (i) => console.log("tick", i));
// tick 0
// tick 1
// tick 2
```

`repeat` knows how to loop; the caller supplies what to do on each pass. A function passed in this
way is usually called a **callback** — "callback" describes the *role* a function plays, "higher-order"
describes the function that receives or returns it.

## 📤 Returning a Function: Function Factories

```js
function multiplier(factor) {
  return (n) => n * factor;
}

const triple = multiplier(3);
console.log(triple(5));   // 15
```

Each call to `multiplier` produces a new function that remembers its own `factor` — a
[closure](../functions/closures.md) over the call's environment (see
[execution-contexts-and-the-scope-chain.md](../execution-context-and-hoisting/execution-contexts-and-the-scope-chain.md)
for how that environment survives). Returning functions is how configuration gets "baked in".

## 🎁 Wrapping a Function: Decorating Behavior

The most powerful use of both ideas together is a function that takes a function and returns an
enhanced version of it, without touching the original:

```js
function withLogging(fn) {
  return function (...args) {
    console.log(`calling ${fn.name} with`, args);
    const result = fn.apply(this, args);
    console.log(`${fn.name} returned`, result);
    return result;
  };
}

const add = (a, b) => a + b;
const loggedAdd = withLogging(add);

loggedAdd(2, 3);
// calling add with [ 2, 3 ]
// add returned 5
```

Two details make a wrapper well-behaved: collecting arguments with a rest parameter
(`...args`, see [parameters-and-return-values.md](../functions/parameters-and-return-values.md)) so it
works for any arity, and forwarding with `fn.apply(this, args)` so the original's `this` and
arguments pass through unchanged (see [call-apply-and-bind.md](call-apply-and-bind.md)). And the
wrapper must `return` the result — forgetting that silently turns the wrapped function into one that
returns `undefined`.

Here is a second, tiny wrapper that restricts *how often* a function runs:

```js
function once(fn) {
  let called = false;
  let result;
  return function (...args) {
    if (!called) {
      called = true;
      result = fn.apply(this, args);
    }
    return result;
  };
}

const init = once(() => {
  console.log("initializing");
  return 42;
});

console.log(init());   // logs "initializing", then 42
console.log(init());   // 42 — the original did not run again
```

## 🧰 Higher-Order Functions You Already Use

| Where | The function you pass |
|-------|-----------------------|
| `array.map`, `filter`, `reduce`, `find`, `some`, `every` | A transformation or predicate |
| `array.sort(compare)` | A comparator |
| `setTimeout(fn, ms)`, `addEventListener(type, fn)` | A callback to run later |
| `promise.then(fn)` | A continuation (see [promises.md](../asynchronous-programming-and-modules/promises.md)) |

A comparator is worth a closer look, because the default behavior surprises people:

```js
console.log([10, 9, 1].sort());                // [ 1, 10, 9 ] — default sort compares as strings
console.log([10, 9, 1].sort((a, b) => a - b)); // [ 1, 9, 10 ] — the comparator you pass wins
```

## ⚠️ A Classic Trap: `map(parseInt)`

`map` calls its callback with *three* arguments — the element, its index, and the array — and
`parseInt` happens to take a second parameter, the radix. MDN documents this exact gotcha:

```js
console.log(["1", "2", "3"].map(parseInt));            // [ 1, NaN, NaN ]
console.log(["1", "2", "3"].map(Number));              // [ 1, 2, 3 ]
console.log(["1", "2", "3"].map((s) => parseInt(s, 10))); // [ 1, 2, 3 ]
```

The index becomes the radix, so `parseInt("2", 1)` and `parseInt("3", 2)` are invalid and give `NaN`.
The lesson generalizes: before passing an existing function as a callback, check how many
parameters it accepts and what the caller will actually pass.

## 🎤 Interview Angle

- **"What is a higher-order function?"** One that accepts a function, returns a function, or both —
  made possible because JavaScript functions are first-class values. `map`, `filter`, and `reduce`
  are built-in examples.
- **"Write a function that runs a callback only once."** The `once` wrapper above: a closure holding
  a `called` flag and the cached result.
- **"What does `['1','2','3'].map(parseInt)` return, and why?"** `[1, NaN, NaN]` — the index is
  passed as `parseInt`'s radix.

## Common Mistakes

- **Calling the function instead of passing it** — `setTimeout(sayHi(), 1000)` runs `sayHi`
  immediately and hands its return value to `setTimeout`; pass `sayHi` (or `() => sayHi()`).
- **Forgetting to `return` from a wrapper**, or to forward `this` and the arguments.
- **Passing a multi-parameter function straight to `map`/`filter`** and getting surprising behavior
  from the extra index and array arguments.
- **Relying on `sort()` without a comparator** for numbers.

## ➡️ Next

Continue to [call-apply-and-bind.md](call-apply-and-bind.md) to see how to control the `this` and
arguments of the functions you pass around.
