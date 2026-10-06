# 🔧 `call`, `apply`, and `bind` in Practice

## Beyond the Basics

[this-keyword.md](../advanced-javascript/this-keyword.md) introduced explicit binding: `call`,
`apply`, and `bind` let you choose `this`. This file covers what that module deliberately left out —
how the three differ in practice, the situations that call for each, a few behaviors that surprise
people, and how `bind` works under the hood.

## 📋 The Three at a Glance

| Method | Runs the function? | Arguments are passed as | Returns |
|--------|--------------------|-------------------------|---------|
| `fn.call(thisArg, a, b)` | Immediately | Separate values | The function's result |
| `fn.apply(thisArg, [a, b])` | Immediately | One array (or array-like) | The function's result |
| `fn.bind(thisArg, a)` | **No** | Optional preset arguments | A **new** function |

A common memory aid: **c**all takes a **c**omma-separated list, **a**pply takes an **a**rray.

```js
function introduce(greeting, punctuation) {
  return `${greeting}, I'm ${this.name}${punctuation}`;
}

const ada = { name: "Ada" };

console.log(introduce.call(ada, "Hello", "!"));     // Hello, I'm Ada!
console.log(introduce.apply(ada, ["Hello", "!"]));  // Hello, I'm Ada!

const introAda = introduce.bind(ada, "Hello");      // greeting is preset
console.log(introAda("?"));                          // Hello, I'm Ada?
```

## 🛠️ Everyday Uses

### 1. Borrowing a method for an array-like

An object with numeric keys and a `length` — an *array-like* — has no array methods of its own, but
it can borrow them:

```js
const arrayLike = { 0: "a", 1: "b", length: 2 };

console.log(Array.prototype.map.call(arrayLike, (x) => x.toUpperCase()));   // [ 'A', 'B' ]
```

Modern code usually converts with `Array.from(arrayLike)` or spread instead, but you will meet this
pattern in older code and interviews.

### 2. Spreading an array into arguments

```js
console.log(Math.max.apply(null, [3, 9, 2]));   // 9 — the historical way
console.log(Math.max(...[3, 9, 2]));            // 9 — spread replaced it
```

### 3. Fixing a lost `this`

Passing a method as a callback detaches it from its object (the "losing `this`" bug in
[this-keyword.md](../advanced-javascript/this-keyword.md)). `bind` repairs it:

```js
const user = {
  name: "Ada",
  greet() { return "Hello, " + this.name; },
};

const fixed = user.greet.bind(user);
console.log(fixed());   // Hello, Ada — even if `fixed` is passed around and called bare
```

### 4. Partial application

Presetting leading arguments is a form of *partial application* (the subject of
[currying-and-partial-application.md](currying-and-partial-application.md)); the `this` slot can be
`null` when the function does not use `this`:

```js
function add3(a, b, c) { return a + b + c; }
const addTo1 = add3.bind(null, 1);

console.log(addTo1(2, 3));   // 6
```

## 🔬 Behaviors Worth Knowing

### `bind` is permanent

MDN states that once a function is bound, `call` and `apply` can no longer change its `this`:

```js
function who() { return this.name; }

const bound = who.bind({ name: "Ada" });
console.log(bound.call({ name: "Grace" }));   // Ada — the bound `this` wins
```

### Bound functions keep a trace of how they were made

```js
function add3(a, b, c) { return a + b + c; }
const b1 = add3.bind(null, 1);

console.log(add3.name, b1.name);       // add3 bound add3
console.log(add3.length, b1.length);   // 3 2 — one parameter was preset
```

The `name` gains a `bound ` prefix, and `length` (the declared parameter count) shrinks by the number
of preset arguments — a detail the currying file leans on.

### Arrow functions ignore the `this` you pass

Arrow functions have no `this` of their own (see [arrow-functions.md](../functions/arrow-functions.md)),
so `call`, `apply`, and `bind` cannot change it — they only pass arguments through:

```js
const team = {
  name: "Core",
  getNameLater() {
    return () => this.name;      // lexical `this`
  },
};

const arrow = team.getNameLater();
console.log(arrow.call({ name: "Other" }));   // Core
```

### `null` or `undefined` as `thisArg` depends on the mode

```js
function f() { return this === globalThis; }
console.log(f.call(null));          // true  — sloppy mode substitutes the global object
```

```js
function g() { "use strict"; return this; }
console.log(g.call(null), g.call(undefined));   // null undefined — strict mode keeps exactly what you passed
```

See [strict-mode.md](../execution-context-and-hoisting/strict-mode.md) for the broader picture.

## 🧪 How `bind` Works: A Simplified Version

Writing your own `bind` is a classic exercise, and it shows that there is no magic — only a closure
and `apply`:

```js
Function.prototype.myBind = function (thisArg, ...presetArgs) {
  const fn = this;                                   // the function being bound
  return function (...laterArgs) {
    return fn.apply(thisArg, [...presetArgs, ...laterArgs]);
  };
};

function greet(greeting, punctuation) {
  return greeting + ", " + this.name + punctuation;
}

console.log(greet.myBind({ name: "Ada" }, "Hi")("!"));   // Hi, Ada!
```

This version omits `new` support (MDN notes that a bound function used with `new` ignores the bound
`this` but still applies preset arguments). It is an exercise — adding methods to
`Function.prototype` in production code is discouraged.

## 🎤 Interview Angle

- **"What is the difference between `call`, `apply`, and `bind`?"** `call` and `apply` invoke the
  function immediately — arguments as a list versus an array. `bind` returns a new function with
  `this` (and optionally leading arguments) fixed, without calling it.
- **"Can you rebind a bound function?"** No — `call`, `apply`, and further `bind` calls cannot
  change its `this`.
- **"Implement `bind`."** Capture `this`, return a function that calls it with `apply`, merging
  preset and later arguments.

## Common Mistakes

- **Expecting `bind` to call the function** — it returns a new function you must still call.
- **Calling `fn.apply(obj, a, b)`** — `apply` takes a single array of arguments, not a list.
- **Using `call` or `bind` on an arrow function to change `this`** — it has no effect.
- **Creating a fresh bound function on every render or loop pass** when one bound reference would
  do — each `bind` call allocates a new function.

## ➡️ Next

Continue to [currying-and-partial-application.md](currying-and-partial-application.md) to see how
presetting arguments grows into a general technique.
