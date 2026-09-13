# Closures

## The Definition, Made Concrete

A **closure** is a function bundled together with references to the variables from the scope it
was defined in — and critically, it retains access to those variables even after the outer
function has finished running and would otherwise have "gone away."

```js
function makeCounter() {
  let count = 0;
  return function () {
    count++;
    return count;
  };
}

const counter = makeCounter();
counter(); // 1
counter(); // 2
counter(); // 3
```

`makeCounter()` runs and returns — normally, its local variable `count` would be discarded once the
function finishes. But because the returned inner function references `count`, JavaScript keeps it
alive for as long as that inner function (the closure) exists. Each call to `counter()` still
accesses and updates the *same* `count`, because it's the same closure over the same variable.

## Why This Is Genuinely Useful

Closures are the mechanism behind several extremely common JavaScript patterns:

- **Private state**: `count` in the example above is inaccessible from outside `makeCounter` — the
  only way to interact with it is through the returned function, effectively creating an
  encapsulated, private variable with no formal "private" keyword needed.
- **Event handlers and callbacks**: a callback passed to `addEventListener` or `setTimeout`
  commonly relies on a closure over variables from its surrounding scope, remaining available when
  the callback actually runs later.
- **Function factories**: `makeCounter` is itself an example — a function that creates and returns
  a customized function, each with its own independent closure.

## Each Call Creates a New, Independent Closure

```js
const counterA = makeCounter();
const counterB = makeCounter();
counterA(); // 1
counterA(); // 2
counterB(); // 1 — an entirely separate closure with its own independent `count`
```

`counterA` and `counterB` each close over their *own* separate `count` variable, created by their
own separate call to `makeCounter()` — they don't share state.

## The Classic Loop-and-Closure Bug

```js
// Buggy with var:
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // logs 3, 3, 3
}

// Correct with let:
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // logs 0, 1, 2
}
```

With `var` (function-scoped), all three callbacks close over the *same single* `i`, whose final
value (`3`) is whatever it was when the loop finished by the time the callbacks actually run. With
`let` (block-scoped), each loop iteration gets its **own** separate `i`, so each callback closes
over a distinct value — this is a well-known, concrete, real-world reason `let` is preferred over
`var`, directly connecting back to [variables.md](../introduction-to-javascript/variables.md).

## Common Mistakes

- Believing closures "copy" a variable's value at the time the closure is created — they hold a
  live *reference*, which is exactly why the classic loop bug above happens with `var`.
- Creating closures unnecessarily in a performance-sensitive hot path, holding onto more memory
  than needed for the closure's captured variables (a genuine but usually minor concern, not a
  reason to avoid closures generally).
- Missing that closures are the underlying mechanism behind seemingly unrelated features
  encountered later in this platform, including React's `useState`/`useEffect` hooks.

## Module Summary

Across this module: declarations are hoisted while expressions are not (see
[function-declarations-and-expressions.md](function-declarations-and-expressions.md)); arrow
functions' defining feature is lexical `this`, not just shorter syntax (see
[arrow-functions.md](arrow-functions.md)); default and rest parameters are the modern way to
handle optional and variable arguments (see
[parameters-and-return-values.md](parameters-and-return-values.md)); lexical scope and the scope
chain determine what a function can see, based on where it's written (see [scope.md](scope.md));
and closures — a function retaining access to its defining scope's variables even after that scope
has finished executing — underlie private state, callbacks, and much of idiomatic JavaScript.
