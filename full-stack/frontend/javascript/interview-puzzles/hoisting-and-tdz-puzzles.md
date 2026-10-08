# 🏗️ Hoisting and Temporal Dead Zone Puzzles

## 🧩 What These Puzzles Test

Hoisting questions are popular because a short snippet can hide the whole two-step model of execution:
the engine first **creates the bindings** for a scope, and only then **runs the code line by line**. If you
know which bindings exist *before* the first line runs, and what value each one holds at that moment, you
can answer almost any hoisting puzzle. The twelve puzzles below range from the basic `var` case to the
subtle differences between runtimes.

Each answer was **produced by running the code** (three times, to confirm it is stable). Where a result
depends on the runtime (Node.js or browser, script or module, sloppy or strict mode), the puzzle says so and
the difference was checked in both Node.js 24 and a current Chromium browser.

## 🛠️ How to Use This File

1. **Cover the answer** and predict the output.
2. **List the bindings first.** Before reading line 1, write down every `var`, function declaration, `let`,
   `const`, `class`, and parameter in the scope, and the value each one has at the start.
3. **Then run through the lines**, updating values as assignments happen.

As in the other puzzle files, the `text` blocks show Node.js 24 output, and error wording
(`Cannot access 'x' before initialization`, `x is not a function`) is V8's.

The concept files behind these puzzles are
[hoisting-and-the-temporal-dead-zone.md](../execution-context-and-hoisting/hoisting-and-the-temporal-dead-zone.md),
[execution-contexts-and-the-scope-chain.md](../execution-context-and-hoisting/execution-contexts-and-the-scope-chain.md),
and [strict-mode.md](../execution-context-and-hoisting/strict-mode.md).

## 🧪 The Puzzles

### Puzzle 1 — Reading a variable before its line

*Difficulty: ⭐ Warm-up*

```js
console.log(a);
var a = 5;
console.log(a);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
undefined
5
```

`var a` is **hoisted and initialised to `undefined`** when the scope is set up, so the first `console.log`
finds a binding holding `undefined`. The *assignment* `= 5` is not hoisted; it runs on its own line. Only
then does `a` become `5`.

The declaration moves "up"; the value does not. See
[hoisting-and-the-temporal-dead-zone.md](../execution-context-and-hoisting/hoisting-and-the-temporal-dead-zone.md)
("`var`: Hoisted and Initialized to `undefined`").

</details>

### Puzzle 2 — One name, a function and a var

*Difficulty: ⭐⭐ Interview standard*

```js
console.log(typeof foo);
var foo = 1;
function foo() {}
console.log(typeof foo);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
function
number
```

During setup, the function declaration `foo` is created **with its body** and stored in the binding; the
`var foo` declaration does not overwrite it (a `var` without an initialiser never resets an existing
binding). So at the first line `foo` is already a function.

Then the line `var foo = 1;` runs as a normal assignment and replaces the function with the number `1`.
Function declarations win during setup; later assignments win during execution.

</details>

### Puzzle 3 — A function expression is not a declaration

*Difficulty: ⭐ Warm-up*

```js
try {
  hello();
} catch (e) {
  console.log(e.name + ": " + e.message);
}

var hello = function () {
  console.log("hi");
};

hello();
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
TypeError: hello is not a function
hi
```

Only the *declaration* `var hello` is hoisted, so before the assignment `hello` is `undefined`. Calling
`undefined` throws a `TypeError` ("is not a function") — not a `ReferenceError`, because the name *does*
exist. After the assignment line runs, the call succeeds.

Had it been `function hello() { … }` (a declaration), the first call would have worked. See
[function-declarations-and-expressions.md](../functions/function-declarations-and-expressions.md).

</details>

### Puzzle 4 — The temporal dead zone

*Difficulty: ⭐⭐ Interview standard*

```js
try {
  console.log(x);
} catch (e) {
  console.log(e.name + ": " + e.message);
}
let x = 1;

console.log(typeof notDeclared);

try {
  console.log(typeof z);
} catch (e) {
  console.log(e.name + ": " + e.message);
}
let z = 2;
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
ReferenceError: Cannot access 'x' before initialization
undefined
ReferenceError: Cannot access 'z' before initialization
```

`let` bindings **are** created during setup (the scope knows `x` and `z` exist) but are *uninitialised*
until execution reaches their declaration. Touching them in that window — the temporal dead zone — throws a
`ReferenceError`, with a message that proves the binding exists ("Cannot access … before initialization",
not "… is not defined").

The twist is `typeof`. For a name that is **not declared at all**, `typeof` safely returns `"undefined"`.
But for `z`, which is declared and in its dead zone, even `typeof` throws. So `typeof` is no longer a
universal "safe check" once `let`, `const`, or `class` are involved.

</details>

### Puzzle 5 — The dead zone is about time, not position

*Difficulty: ⭐⭐⭐ Tricky*

```js
function show() {
  return value;
}

try {
  show();
} catch (e) {
  console.log(e.name);
}

let value = "ready";
console.log(show());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
ReferenceError
ready
```

`show` is written *above* `let value`, but whether `value` is usable depends on **when `show` is called**,
not where it is written. The first call happens before the `let` line has run, so `value` is still
uninitialised and the call throws. After `let value = "ready"` executes, the same function works.

This is why function declarations that reference later `let`/`const` values are safe as long as nothing
calls them early. See
[hoisting-and-the-temporal-dead-zone.md](../execution-context-and-hoisting/hoisting-and-the-temporal-dead-zone.md)
("Where the TDZ Surprises People").

</details>

### Puzzle 6 — A hoisted var shadows the outer one

*Difficulty: ⭐⭐ Interview standard*

```js
var city = "Paris";

function visit() {
  console.log(city);
  var city = "Rome";
  console.log(city);
}

visit();
console.log(city);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
undefined
Rome
Paris
```

Inside `visit`, `var city` creates a **local** binding for the entire function body, initialised to
`undefined`. So the first line prints `undefined` instead of falling back to the global `"Paris"` — the local
binding already shadows it. After the local assignment, the second line prints `"Rome"`. The global `city`
was never touched, which the last line confirms.

</details>

### Puzzle 7 — A branch that never runs

*Difficulty: ⭐ Warm-up*

```js
function check() {
  if (false) {
    var hidden = 1;
  }
  return hidden;
}

console.log(check());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
undefined
```

Hoisting is decided when the scope is *created*, by reading the code — not by which branches run. The
`var hidden` declaration inside the dead `if` branch still creates the function-wide binding. It holds
`undefined` because the assignment never ran. With `let hidden` the function would throw a `ReferenceError`
at the `return`, because the binding would not be visible outside the block.

</details>

### Puzzle 8 — Classes sit in the dead zone too

*Difficulty: ⭐⭐ Interview standard*

```js
try {
  new Animal();
} catch (e) {
  console.log(e.name + ": " + e.message);
}

class Animal {}

console.log(typeof Animal, new Animal() instanceof Animal);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
ReferenceError: Cannot access 'Animal' before initialization
function true
```

A `class` declaration behaves like `let`: the binding exists from the start of the scope, but it cannot be
used until the declaration has been evaluated. A `class` is *not* hoisted like a function declaration,
which is why code that works with `function Animal() {}` can fail after being converted to a `class`.
After the declaration runs, everything works normally.

</details>

### Puzzle 9 — Parameter, var, and function with the same name

*Difficulty: ⭐⭐⭐ Tricky*

```js
function f(a) {
  console.log(a);
  var a = 2;
  console.log(a);
  function a() {}
}

f(1);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
[Function: a]
2
```

The three declarations share one binding named `a`. Setup runs in this order: the parameter `a` is bound to
`1`; the `var a` declaration changes nothing (it never overwrites an existing binding); and the function
declaration `function a() {}` **replaces** the value with the function. So the first `console.log(a)` prints
the function, not `1`. Then `var a = 2;` executes as an ordinary assignment and the second log prints `2`.

The variation shows the narrower point: a `var a;` with no initialiser leaves the parameter's value alone,
so `g(1)` prints `1`. The general rule: **function declarations override earlier bindings during setup;
`var` declarations never do.**

**Variation — A bare `var` does not reset the parameter**

```js
function g(a) {
  var a;
  console.log(a);
}

g(1);
```

```text
1
```

</details>

### Puzzle 10 — Functions declared in blocks

*Difficulty: ⭐⭐⭐ Tricky*

```js
console.log(typeof inBlock);
{
  function inBlock() {}
}
console.log(typeof inBlock);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
undefined
function
```

In **sloppy mode** (the default for classic scripts and CommonJS), a function declared inside a block gets a
`var`-like binding visible in the enclosing function or script, initialised to `undefined`. When execution
reaches the declaration, the function is assigned to that outer binding. So the first `typeof` prints
`"undefined"` and the second prints `"function"`.

In **strict mode** (and in ES modules and class bodies) a block-level function is scoped to its block, like
`let`. Outside the block no `inBlock` exists, so both `typeof` calls print `"undefined"`. The behaviour
above was identical in a browser classic script (`undefined`, `function`) and a strict script
(`undefined`, `undefined`). Because the sloppy behaviour is a compatibility quirk, avoid declaring
functions in blocks; use `const fn = () => {}` instead. See
[strict-mode.md](../execution-context-and-hoisting/strict-mode.md).

**Variation — The same code in strict mode**

```js
"use strict";
console.log(typeof inBlock);
{
  function inBlock() {}
}
console.log(typeof inBlock);
```

```text
undefined
undefined
```

</details>

### Puzzle 11 — Redeclaring a name

*Difficulty: ⭐⭐ Interview standard*

```js
var v = 1;
var v = 2;
console.log(v);

try {
  eval("let q = 1; let q = 2;");
} catch (e) {
  console.log(e.name + ": " + e.message);
}

try {
  eval("var w = 1; let w = 2;");
} catch (e) {
  console.log(e.name + ": " + e.message);
}
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
2
SyntaxError: Identifier 'q' has already been declared
SyntaxError: Identifier 'w' has already been declared
```

`var` allows redeclaring the same name in the same scope; the second declaration is just another
assignment. `let` and `const` do not: redeclaring a name in the same scope is a **`SyntaxError`**, detected
before any of the code runs. That is why the puzzle uses `eval` — written directly in the file, those lines
would stop the whole program from starting.

Mixing `var` and `let` for the same name in one scope is also an error, which the third case shows. This
early error is deliberate: it catches accidental name clashes that `var` silently allowed.

</details>

### Puzzle 12 — Same file, different runtimes

*Difficulty: ⭐⭐⭐ Tricky*

```js
var topLevel = "var";
let alsoTop = "let";
function fn() {}

console.log(typeof globalThis.topLevel, typeof globalThis.alsoTop, typeof globalThis.fn);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
undefined undefined undefined
```

Where the code lives decides whether top-level declarations become properties of the global object:

| Environment | `var topLevel` | `let alsoTop` | `function fn` |
|-------------|:--------------:|:-------------:|:-------------:|
| Browser **classic** `<script>` | global property (`"string"`) | not a property | global property (`"function"`) |
| Browser **module** `<script type="module">` | not a property | not a property | not a property |
| Node.js CommonJS (`.js` default) | not a property | not a property | not a property |
| Node.js ES module (`.mjs`) | not a property | not a property | not a property |

In Node.js, each CommonJS file is wrapped in a function, so top-level `var` is local to the file; in ES
modules the top level is a module scope. Only a browser classic script puts `var` and function
declarations on the global object (`window`). The browser column was checked by running this exact code in
a classic script and a module script on a real page: the classic script reported `string undefined
function`, the module script `undefined undefined undefined`. `let`, `const`, and `class` never become
global properties in any environment. See
[javascript-runtimes-browser-vs-nodejs.md](../how-javascript-runs/javascript-runtimes-browser-vs-nodejs.md).

**Variation — The same code as an ES module (`.mjs`)**

```js
var topLevel = "var";
let alsoTop = "let";
function fn() {}

console.log(typeof globalThis.topLevel, typeof globalThis.alsoTop, typeof globalThis.fn);
```

```text
undefined undefined undefined
```

</details>

## 🧭 Patterns to Remember

| Pattern in the question | What happens |
|-------------------------|--------------|
| Read a `var` before its line | `undefined` (binding exists, value not yet assigned) |
| Call a function declaration before its line | Works (hoisted with its body) |
| Call a function *expression* (`var f = function…`) before its line | `TypeError: f is not a function` |
| Read `let`/`const`/`class` before its line | `ReferenceError` (temporal dead zone) |
| `typeof` on an undeclared name | `"undefined"` — but `typeof` on a name in its TDZ **throws** |
| Same name as parameter, `var`, and function | Function declaration wins during setup; `var` without a value does not reset |
| Function declared inside a block | Sloppy: `var`-like leak to the outside; strict/modules: block scoped |
| Top-level `var` | Global property only in a browser classic script |

## 🎤 Interview Angle

- **Describe the two phases.** "First the engine creates bindings (`var` → `undefined`, functions → their
  body, `let`/`const`/`class` → uninitialised); then it runs the code." This one sentence answers most
  questions.
- **Avoid saying "hoisting moves code to the top."** Nothing moves; the bindings are created early. The
  precise statement impresses more and avoids wrong predictions.
- **Know the practical advice**: prefer `const`/`let`, declare before use, and keep functions out of blocks.
- **Expect the follow-up**: "Is `let` hoisted?" — see the terminology discussion in
  [hoisting-and-the-temporal-dead-zone.md](../execution-context-and-hoisting/hoisting-and-the-temporal-dead-zone.md).

## Common Mistakes

- **Saying `var` is "moved to the top with its value."** Only the declaration is hoisted.
- **Expecting a `ReferenceError` for `var`** — you get `undefined`.
- **Expecting a `ReferenceError` for a function expression** — you get a `TypeError`.
- **Using `typeof` as a universal safety check** in code that has `let`/`const` declared later in the same scope.
- **Assuming top-level `var` always creates a global property.**

## ➡️ Next

Continue to [this-and-prototype-puzzles.md](this-and-prototype-puzzles.md), where the answer depends on
*how a function is called* rather than where its bindings were created.
