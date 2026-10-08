# 🔒 Closures and Scope Puzzles

## 🧩 Why Puzzles?

Interviewers rarely ask "define a closure." They show eight lines of code and ask what it prints, because
the answer reveals whether you can *trace* how the engine creates scopes, captures variables, and decides
when functions run. The eleven puzzles below cover the situations that come up again and again: loops and
timers, counters and factories, shadowing, default parameters, and a few surprises about function names.

Each puzzle has an answer that was **produced by running the code** (three times, to confirm the output is
stable), followed by an explanation that points back to the concept files in this platform.

## 🛠️ How to Use This File

1. **Cover the answer** and predict the output, including the order of lines.
2. **Trace, don't guess.** For each function ask: *where was it written* (that decides which scope it can
   see) and *when does it run* (that decides which values it sees).
3. **Open the answer** and compare. If you were wrong, find the exact step in your trace that diverged.

Two notes on the printed output. The `text` blocks show what **Node.js 24** printed; browsers format arrays
and objects differently in the console, but the values and the order are the same (all eleven puzzles were
also run in Chrome 152 with identical results). And error-message
wording (such as `Cannot access 'x' before initialization`) is V8's, the engine in Chrome and Node.js.

The concept files behind these puzzles are [scope.md](../functions/scope.md),
[closures.md](../functions/closures.md), and
[execution-contexts-and-the-scope-chain.md](../execution-context-and-hoisting/execution-contexts-and-the-scope-chain.md).

## 🧪 The Puzzles

### Puzzle 1 — The loop and the timers

*Difficulty: ⭐ Warm-up*

```js
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log("var:", i), 0);
}

for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log("let:", j), 0);
}
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
var: 3
var: 3
var: 3
let: 0
let: 1
let: 2
```

The callbacks do not run until the loops have finished, because timers always wait for the current
synchronous code. What each callback *sees* then depends on the variable it captured:

- `var i` is **one** variable for the whole function (or file), shared by every callback. By the time the
  timers fire, the loop has ended with `i === 3`, so all three callbacks print `3`.
- `let j` in a `for` header creates a **fresh binding for each iteration**. Each callback closes over its
  own `j`, so they print `0`, `1`, `2`.

The `var` timers print first only because their timers were registered first (equal delays run in
registration order). See [closures.md](../functions/closures.md) ("The Classic Loop-and-Closure Bug") and
[timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md).

</details>

### Puzzle 2 — Two counters

*Difficulty: ⭐ Warm-up*

```js
function makeCounter() {
  let n = 0;
  return { inc: () => ++n, get: () => n };
}

const a = makeCounter();
const b = makeCounter();
a.inc();
a.inc();
b.inc();
console.log(a.get(), b.get());

const c = a;
c.inc();
console.log(a.get(), c.get());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
2 1
3 3
```

Every call to `makeCounter()` creates a **new** environment containing its own `n`. `a` and `b` therefore
count independently (`2` and `1`). But `const c = a` copies a *reference to the same object*, whose
methods close over the same `n`, so incrementing through `c` is visible through `a` (`3` and `3`).

Rule: new function call → new variables; new reference to the same object → same variables. See
[closures.md](../functions/closures.md) ("Each Call Creates a New, Independent Closure").

</details>

### Puzzle 3 — Capturing variables, not values

*Difficulty: ⭐ Warm-up*

```js
let message = "first";
const show = () => console.log(message);
message = "second";
show();

function outer() {
  let x = 1;
  const read = () => x;
  x = 2;
  return read;
}
console.log(outer()());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
second
2
```

A closure keeps a connection to the **variable**, not a snapshot of the value it held when the function was
created. `show` reads `message` at the moment it *runs*, after it was reassigned. The same goes for `read`
inside `outer`: `x` was changed to `2` before `read` was ever called, even though `read` was created while
`x` was `1`.

Interview phrasing: "closures capture bindings by reference, so they see later updates." See
[execution-contexts-and-the-scope-chain.md](../execution-context-and-hoisting/execution-contexts-and-the-scope-chain.md)
("Why Closures Work: Environments Outlive Contexts").

</details>

### Puzzle 4 — Fixing the loop two ways

*Difficulty: ⭐⭐ Interview standard*

```js
const fixed = [];
for (var i = 0; i < 3; i++) {
  fixed.push((function (n) { return () => n * 10; })(i));
}
console.log(fixed.map((f) => f()));

const broken = [];
for (var k = 0; k < 3; k++) {
  broken.push(() => k * 10);
}
console.log(broken.map((f) => f()));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
[ 0, 10, 20 ]
[ 30, 30, 30 ]
```

Before `let`, the standard fix was an IIFE (see [iife-and-the-module-pattern.md](../functional-javascript/iife-and-the-module-pattern.md)):
calling `(function (n) { … })(i)` *immediately* copies the current `i` into a parameter `n`, and that
parameter is a separate variable per call. The arrow functions in `fixed` close over those separate `n`s.

The `broken` loop has no such copy, so all three arrows share the single `k`, which ends at `3` — giving
`30` three times. Changing `var k` to `let k` would fix it with no IIFE.

</details>

### Puzzle 5 — What `let` really does in a for loop

*Difficulty: ⭐⭐⭐ Tricky*

```js
const fns = [];
for (let i = 0; i < 3; i++) {
  fns.push(() => i);
  i++;
}
console.log(fns.map((f) => f()));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
[ 1, 3 ]
```

`let` in a `for` header gives each iteration its own copy of `i`, but the copy is made *between*
iterations: at the end of an iteration the engine creates the next iteration's binding with the **current
value**, and only then runs the `i++` of the loop header. Trace it:

1. Iteration 1: `i` is `0`. The arrow is pushed, then the body's `i++` makes *this* iteration's `i` equal
   `1`. The loop header copies `1` to a new binding and increments it to `2`.
2. Iteration 2: `i` is `2` (still `< 3`). The arrow is pushed, then the body makes it `3`. The copy becomes
   `3`, the header increments it to `4`, and `4 < 3` is false, so the loop ends.

There were only two iterations, and each closure sees the final value of *its own* iteration's binding:
`1` and `3`. If you predicted `[0, 2]`, you forgot that the body's `i++` changed the binding the closure
already captured. See [scope.md](../functions/scope.md).

</details>

### Puzzle 6 — Scope is decided where code is written

*Difficulty: ⭐⭐ Interview standard*

```js
const x = "global";

function outer() {
  const x = "outer";
  function inner() {
    return x;
  }
  return inner;
}

function caller() {
  const x = "caller";
  return outer()();
}

console.log(caller());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
outer
```

JavaScript uses **lexical** (static) scoping: `inner` looks for `x` in the scopes that *surround its
definition* — `inner`'s own scope, then `outer`'s — not in the scopes of whoever happens to call it. The
`x` inside `caller` is irrelevant even though `caller` is on the call stack when `inner` runs. (Contrast
with `this`, which *is* decided by the call; see [this-and-prototype-puzzles.md](this-and-prototype-puzzles.md).)

See [scope.md](../functions/scope.md) ("The Scope Chain") and
[execution-contexts-and-the-scope-chain.md](../execution-context-and-hoisting/execution-contexts-and-the-scope-chain.md)
("The Outer Link Is Fixed Where a Function Is Written").

</details>

### Puzzle 7 — Values captured at different times

*Difficulty: ⭐⭐ Interview standard*

```js
function schedule() {
  let count = 0;
  const snapshot = count;
  const box = { count };

  setTimeout(() => console.log(count, snapshot, box.count), 0);

  count = 5;
  box.count = 7;
}

schedule();
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
5 0 7
```

Three different things are read inside the callback:

- `count` is read through the closure when the callback runs, so it sees the updated `5`.
- `snapshot` is a **separate variable** that received a copy of `0` when it was declared. Nothing changes it,
  so it stays `0`.
- `box.count` was initialised from `count` (`0`) but is its own property. The assignment `box.count = 7`
  changed it, so the callback sees `7`; the later change to the variable `count` would not have affected it.

The lesson: a closure sees changes to the *variables it captured*; copies made earlier are independent.

</details>

### Puzzle 8 — Block scope vs. function scope

*Difficulty: ⭐ Warm-up*

```js
function test() {
  if (true) {
    var a = 1;
    let b = 2;
  }
  console.log(a);
  console.log(typeof b);
  try {
    console.log(b);
  } catch (e) {
    console.log(e.name + ": " + e.message);
  }
}

test();
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
1
undefined
ReferenceError: b is not defined
```

`var` ignores blocks: `a` belongs to the whole function, so it is readable after the `if` block. `let`
belongs to the block, so `b` no longer exists afterwards. Reading it throws a `ReferenceError`, but
`typeof` on a name that is not declared anywhere returns `"undefined"` instead of throwing — which is why
the second line prints `undefined` rather than failing.

See [scope.md](../functions/scope.md) ("Block Scope vs. Function Scope, Revisited").

</details>

### Puzzle 9 — The function name nobody can see

*Difficulty: ⭐⭐ Interview standard*

```js
const f = function g() {
  return typeof g;
};

console.log(typeof f, f(), typeof g);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
function function undefined
```

In a **named function expression**, the name (`g`) is bound only *inside* the function body, which lets a
function refer to itself (for recursion) without making the name visible outside. So `f()` can see `g`
(`"function"`), but the outer scope cannot — and `typeof` on an undeclared name gives `"undefined"` instead
of throwing.

Compare with a function *declaration* (`function g() {}`), which creates `g` in the enclosing scope. See
[function-declarations-and-expressions.md](../functions/function-declarations-and-expressions.md).

</details>

### Puzzle 10 — Default parameters have their own scope

*Difficulty: ⭐⭐⭐ Tricky*

```js
let x = "outer";

function f(a = x, x = "param") {
  return a;
}

try {
  console.log(f());
} catch (e) {
  console.log(e.name + ": " + e.message);
}
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
ReferenceError: Cannot access 'x' before initialization
```

Parameters are declared left to right, and each default expression runs in a scope where the *other
parameters* already exist. The parameter `x` shadows the outer `x` throughout the parameter list, but when
`a = x` is evaluated, parameter `x` has not been initialised yet — it is in its temporal dead zone. So the
engine does **not** fall back to the outer `"outer"`; it throws.

Swap the order — `function f(x = "param", a = x)` — and `a` becomes `"param"`. The rule to remember:
parameters behave like `let` bindings, and a default can only use parameters to its *left*. See
[hoisting-and-the-temporal-dead-zone.md](../execution-context-and-hoisting/hoisting-and-the-temporal-dead-zone.md).

The variation shows a second subtlety. When a function has default-parameter expressions, the parameters
live in their own scope, separate from the body's `var` declarations. The body's `var a = 10` starts out
with the parameter's value (`1`) and then changes only the **body's** `a`; the arrow function `read`, written
in the parameter list, still sees the **parameter** `a`, which is still `1`. So the function returns the
body's `10` and `read()`'s `1`.

**Variation — Defaults see the parameter, not a `var` in the body**

```js
function g(a, read = () => a) {
  var a = 10;
  return [a, read()];
}

console.log(g(1));
```

```text
[ 10, 1 ]
```

</details>

### Puzzle 11 — A function that runs only once

*Difficulty: ⭐⭐ Interview standard*

```js
function once(fn) {
  let called = false;
  let result;
  return (...args) => {
    if (!called) {
      called = true;
      result = fn(...args);
    }
    return result;
  };
}

const init = once((x) => {
  console.log("init", x);
  return x * 2;
});

console.log(init(2), init(100));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
init 2
4 4
```

`called` and `result` live in the environment created by one call to `once`, and the returned arrow keeps
that environment alive. The first call runs `fn(2)`, logs `init 2`, and stores `4`. The second call finds
`called === true` and returns the stored `4`, ignoring its argument.

Note the order of output: `init 2` is printed *while the arguments of the outer `console.log` are being
evaluated*, so it appears before the line that logs both results. This "closure holding private state"
pattern underlies [memoization.md](../functional-javascript/memoization.md) and
[currying-and-partial-application.md](../functional-javascript/currying-and-partial-application.md).

</details>

## 🧭 Patterns to Remember

| Pattern in the question | What to check |
|-------------------------|---------------|
| `var` in a loop with a callback | One shared variable; the loop is finished before the callback runs |
| `let` in a loop with a callback | A new binding per iteration; each closure keeps its own |
| A returned or stored function | Which variables sit in the environment where it was *written*? |
| Reassignment after creating the function | Closures see the variable's *current* value, not a snapshot |
| Copies (`const snapshot = value`, `{ ...obj }`) | Independent after the copy; closures only track variables |
| Default parameters referencing other parameters | Left-to-right, with a temporal dead zone |

## 🎤 Interview Angle

- **Say the rule, then trace.** "Closures capture variables, not values, so …" gives the interviewer your
  model before you walk through the lines.
- **Always mention when a callback runs.** Most closure puzzles hide a timer or event; say that it runs
  after the synchronous code finishes.
- **Know both fixes** for the loop bug: `let` (modern) and an IIFE or helper function (legacy).
- **Be ready for "where would this leak memory?"** A closure keeps its whole captured environment alive —
  see [finding-and-fixing-memory-leaks.md](../how-javascript-runs/finding-and-fixing-memory-leaks.md).

## Common Mistakes

- **Predicting by position instead of by scope** — the order of lines matters less than where functions
  were written and when they run.
- **Forgetting that `i++` inside a `let` loop body changes the binding a closure may have captured.**
- **Assuming callbacks run immediately** instead of after the current synchronous code.
- **Treating `typeof x` as proof that `x` exists.** It returns `"undefined"` for undeclared names.

## ➡️ Next

Continue to [hoisting-and-tdz-puzzles.md](hoisting-and-tdz-puzzles.md), where the question becomes *when* a
binding exists rather than *which* binding a function sees.
