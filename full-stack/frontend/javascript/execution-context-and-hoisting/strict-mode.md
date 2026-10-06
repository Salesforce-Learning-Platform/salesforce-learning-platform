# 🔒 Strict Mode

## An Opt-In Mode That Turns Silent Mistakes Into Errors

JavaScript was designed to be forgiving, and for years its leniency covered some genuine mistakes:
assigning to a variable you forgot to declare quietly created a global, writing to a read-only
property was silently ignored, and a stand-alone function call got the global object as `this`.
**Strict mode**, introduced in ES5, is an opt-in variant of the language that converts those silent
problems into thrown errors and removes a few confusing features. The core behavior of
[scope](execution-contexts-and-the-scope-chain.md) and
[hoisting](hoisting-and-the-temporal-dead-zone.md) from the previous two files is the same in both
modes (function declarations inside blocks are the notable exception); the differences are in the
cases below.

## 🔛 Turning It On

```js
"use strict";             // whole script: must be the first statement

function f() {
  "use strict";           // or one function: must be the first statement in its body
  // ...
}
```

Two rules from MDN's strict mode reference:

- The directive must come **first**; it cannot be applied to a block statement (`{ }`).
- A directive that is *not* first is just an unused string expression — silently ignored:

```js
function f() {
  var a = 1;
  "use strict";           // too late — this line does nothing
  undeclared = 5;         // still allowed
  return typeof undeclared;
}
console.log(f());          // "number"
```

## ✅ Where It Is Already On

You often get strict mode without writing the directive. All code in **ES modules** is strict, and
so is everything inside a **class body**. In an ES module (a `.mjs` file in Node.js, or
`<script type="module">` in a browser):

```js
function f() { return this; }
console.log(f());               // undefined

undeclaredInModule = 1;         // ReferenceError: undeclaredInModule is not defined
```

Since modern code is mostly written as modules and classes, strict mode is the everyday default;
understanding it explains behaviors you would otherwise find mysterious.

## 🔍 What Changes

| Mistake | Sloppy mode (default for classic scripts) | Strict mode |
|---------|--------------------------------------------|-------------|
| Assigning to an undeclared variable | Creates a global | `ReferenceError` |
| `this` in a plain function call | The global object | `undefined` |
| Writing to a read-only property | Silently ignored | `TypeError` |
| Adding a property to a frozen object | Silently ignored | `TypeError` |
| Duplicate parameter names | Allowed | `SyntaxError` |
| Legacy octal literal such as `010` | Means 8 | `SyntaxError` |
| Assigning through `arguments[0]` | Also changes the named parameter | Independent copy |
| `with` statement | Allowed | `SyntaxError` |

Each of the main rows, run for real:

### Accidental globals

```js
function addTotal() {
  total = 5;                       // forgot const or let
}
addTotal();
console.log(typeof total, total);  // sloppy: "number" 5 — an accidental global leaked out
```

With `"use strict"` inside `addTotal`, the assignment throws
`ReferenceError: total is not defined` at the exact line of the typo.

### `this` in a plain function call

```js
function whoAmI() { return this; }

// sloppy mode:  whoAmI() === globalThis   → true
// strict mode:  whoAmI()                  → undefined
```

This is the root of a very common bug. Class bodies are strict, so a method pulled off its object
loses its `this`:

```js
class Counter {
  count = 0;
  inc() { this.count++; }
}

const c = new Counter();
const inc = c.inc;
inc();   // TypeError: Cannot read properties of undefined (reading 'count')
```

Handing `c.inc` to an event listener or timer triggers the same error; the fixes (an arrow function,
`bind`) are covered in [this-keyword.md](../advanced-javascript/this-keyword.md).

### Silent failures become errors

```js
"use strict";
const config = Object.freeze({ retries: 3 });

config.retries = 5;   // TypeError: Cannot assign to read only property 'retries' of object '#<Object>'
config.timeout = 10;  // TypeError: Cannot add property timeout, object is not extensible
```

Without strict mode, both lines do nothing and the program carries on with stale data — a bug
that surfaces far from its cause. (The error wording shown is V8's, as in Chrome and Node.js; other
engines phrase it differently.)

### Syntax that is no longer allowed

```js
"use strict";
function add(a, a) { return a; }    // SyntaxError: Duplicate parameter name not allowed in this context
console.log(010);                    // SyntaxError: Octal literals are not allowed in strict mode.
console.log(0o10);                   // 8 — the explicit octal syntax is fine
with ({ a: 1 }) { console.log(a); }  // SyntaxError: Strict mode code may not include a with statement
```

### `arguments` stops aliasing parameters

```js
function sloppy(a)  { arguments[0] = 99; return a; }
function strict(a)  { "use strict"; arguments[0] = 99; return a; }

console.log(sloppy(1));   // 99 — writing arguments[0] changed `a`
console.log(strict(1));   // 1  — they are independent
```

## ⚠️ One Placement Restriction

A function whose parameter list is not "simple" — one that uses default values, rest parameters, or
destructuring — cannot contain its own `"use strict"` directive:

```js
function f(a = 1) {
  "use strict";   // SyntaxError: Illegal 'use strict' directive in function with non-simple parameter list
  return a;
}
```

Put the directive at the top of the file, or use a module, instead.

## 🧭 Should You Write `"use strict"`?

- **In modules and classes:** no need — it is already on.
- **In a classic script:** put it at the very top of the file so the whole script is strict.
- **When in doubt:** prefer failing loudly over carrying on with a silent mistake — which is exactly
  what strict mode trades for.

## 🎤 Interview Angle

- **"What does `"use strict"` do?"** It opts the code into a stricter variant of JavaScript that
  throws on several silent mistakes (accidental globals, writes to read-only properties) and
  removes confusing features (`with`, octal literals, duplicate parameters).
- **"What is `this` inside a regular function called on its own?"** The global object in sloppy
  mode, `undefined` in strict mode — and always `undefined` for code in a module or class.
- **"Which code is strict automatically?"** ES modules and class bodies.

## Common Mistakes

- **Placing the directive after other statements** — it is then ignored without a warning.
- **Expecting a block-level `"use strict"`** — it works only at the start of a script or function.
- **Adding `"use strict"` to a function with default or destructured parameters** — a `SyntaxError`.
- **Treating the `this` error in a detached class method as a mysterious engine bug** — it is strict
  mode doing its job; bind the method or use an arrow function.

## ➡️ Next

Continue to [automatic-semicolon-insertion.md](automatic-semicolon-insertion.md) for the last piece
of this module: the parsing rule that decides where one statement ends and the next begins.
