# 🏗️ Hoisting and the Temporal Dead Zone

## The Visible Effect of "Set Up First"

[execution-contexts-and-the-scope-chain.md](execution-contexts-and-the-scope-chain.md) described how
the engine sets up a scope's bindings before running its code. **Hoisting** is the name for what
that looks like from the outside: declarations seem to be "moved to the top" of their scope.
[variables.md](../introduction-to-javascript/variables.md) and
[function-declarations-and-expressions.md](../functions/function-declarations-and-expressions.md)
each touched on a piece of this. This file puts every case in one place, and names the behavior
that governs `let`, `const`, and `class`: the **temporal dead zone**.

MDN notes that hoisting is not a formally defined term in the ECMAScript specification — it
describes observable behavior. The behavior itself is precise, so that is what to learn.

## 📋 The Whole Picture in One Table

| Declaration | Binding exists from the top of its scope? | Value before its own line runs |
|-------------|--------------------------------------------|---------------------------------|
| `function f() {}` | Yes — to the top of its enclosing function (inside a block, see below) | The complete function — callable early |
| `var x = 1` | Yes (function scope) | `undefined` |
| `let x = 1` / `const x = 1` | Yes (block scope) | **Uninitialized** — any access throws `ReferenceError` |
| `class C {}` | Yes (block scope) | **Uninitialized** — any access throws `ReferenceError` |
| `const f = function () {}` or an arrow function | Follows the rules of `var` / `let` / `const` above | Not callable before the assignment line runs |

## 🟡 `var`: Hoisted and Initialized to `undefined`

```js
console.log(city);   // undefined — no error
var city = "Berlin";
console.log(city);   // "Berlin"
```

The engine treats this as if `var city;` sat at the top of the function, while the *assignment*
stays where it is. So reading `city` early gives `undefined` rather than an error — which is
precisely why `var` bugs are hard to spot: the code runs, with a silently wrong value.

`var` is also **function-scoped**, so a `var` inside an `if` or loop is hoisted to the top of the
whole function, not the block:

```js
function f() {
  if (true) {
    var v = 1;
    let l = 2;
  }
  console.log(v);          // 1 — var ignored the block
  console.log(typeof l);   // "undefined" — l never existed out here
}
f();
```

## 🟢 Function Declarations: Hoisted With Their Body

```js
console.log(greet("Ada"));          // "Hello, Ada" — works before the declaration

function greet(name) {
  return "Hello, " + name;
}
```

Both the name and the whole function are set up first, so the call works anywhere in the enclosing
scope.

One wrinkle: a function declaration written *inside a block* (an `if`, a loop body, a bare `{ }`)
behaves differently depending on [strict mode](strict-mode.md):

```js
{ function inner() {} }
console.log(typeof inner);
// sloppy mode: "function"  — the name leaks out of the block
// strict mode: "undefined" — the declaration stays scoped to its block
```

Avoid relying on either behavior: declare helpers at the top level of a function or module, or
assign a function expression to a `const` when you need one inside a block.

## 🔴 Function *Expressions* Are Not Hoisted Like Declarations

A function expression is just a value assigned to a variable, so it behaves like that variable:

```js
greet("Ada");
var greet = function (name) { return name; };
// TypeError: greet is not a function   — var is hoisted as undefined
```

```js
greet("Ada");
const greet = function (name) { return name; };
// ReferenceError: Cannot access 'greet' before initialization   — const is in the TDZ
```

Telling these two errors apart is a reliable way to tell a `var` problem from a `let`/`const`
problem when debugging.

## ⏳ `let`, `const`, `class`: The Temporal Dead Zone

```
A variable declared with let, const or class is in its TEMPORAL DEAD ZONE (TDZ)
from the start of its block until the declaration is EVALUATED. Accessing it
anywhere in that window throws a ReferenceError.
```

```js
{
  // ┌── the TDZ for `value` starts here, at the top of the block
  // │
  console.log(value);   // ReferenceError: Cannot access 'value' before initialization
  // │
  let value = 10;       // └── the TDZ ends when this declaration runs
  console.log(value);   // 10
}
```

The word *temporal* matters: the dead zone is defined by **time** (execution order), not by where
the text sits. A function written above a `let` can legally refer to it, provided it only *runs*
after the declaration has been evaluated:

```js
function readLater() {
  return later;       // fine to write this here
}

let later = "ready";
console.log(readLater());   // "ready"
```

Calling `readLater()` one line earlier — before `let later` runs — would throw
`ReferenceError: Cannot access 'later' before initialization`.

### Is `let` Hoisted? A Terminology Debate With a Clear Answer

MDN's `let` reference says `let` declarations are commonly regarded as non-hoisted, while its
hoisting glossary classifies `let`, `const`, and `class` as hoisted-with-a-dead-zone. The two pages
disagree about the *word*, not the behavior. This snippet settles what actually happens:

```js
const x = "outer";
{
  console.log(x);   // ReferenceError: Cannot access 'x' before initialization
  let x = "inner";
}
```

If the inner `let x` had no effect before its line, `console.log(x)` would simply find the outer
`"outer"`. Instead it throws — the inner binding already exists for the whole block, shadowing the
outer one, but cannot be used until initialized. That is the observable truth to rely on.

### Where the TDZ Surprises People

```js
console.log(typeof neverDeclared);   // "undefined" — safe for an undeclared name
console.log(typeof tz);              // ReferenceError — tz is in its dead zone
let tz = 1;
```

`typeof` was once the "safe" way to test an undeclared name; it no longer is for a name that is in
the TDZ. Default parameter values are evaluated left to right, and later parameters are in the TDZ
for earlier ones:

```js
function f(a = b, b = 1) { return [a, b]; }
f();   // ReferenceError: Cannot access 'b' before initialization

function g(a = 1, b = a + 1) { return [a, b]; }
g();   // [1, 2]
```

Classes behave the same way — `new Dog()` above `class Dog {}` throws
`ReferenceError: Cannot access 'Dog' before initialization`.

## 🥊 A Classic Interview Trap: Function and `var` With the Same Name

```js
console.log(typeof thing);   // "function"
var thing = "string now";
function thing() {}
console.log(typeof thing);   // "string"
```

During set-up the function declaration wins the name `thing`; then, when the code runs, the
assignment `thing = "string now"` replaces it. Two declarations, one name, and the order of events
explains the output. In real code, simply never reuse a name this way.

## ✅ Practical Rules

- **Declare before you use.** Reading top to bottom should match execution order.
- **Prefer `const`, then `let`; avoid `var`.** The dead zone turns a silent `undefined` into an
  immediate, descriptive error — a bug caught at its source.
- **Rely on function-declaration hoisting deliberately or not at all.** Putting helpers below the
  code that calls them is a legitimate style, but make it a team choice.
- **Let tools enforce it.** ESLint's
  [`no-use-before-define`](https://eslint.org/docs/latest/rules/no-use-before-define) flags uses
  that come before their declaration, with options for functions, classes, and variables.

## 🎤 Interview Angle

- **"What is hoisting?"** Declarations are processed before the code in their scope runs, so they
  can be referenced earlier in the text. What you *see* depends on the keyword: `function` gives
  the full function, `var` gives `undefined`, `let`/`const`/`class` give a `ReferenceError` until
  initialized.
- **"Are `let` and `const` hoisted?"** Their bindings exist for the whole block (proved by the
  shadowing example) but are uninitialized until the declaration runs — the TDZ.
- **"What does this print?"** Walk the two steps aloud: first what the set-up creates, then what the
  code does line by line. Most hoisting puzzles fall apart under that method.

## Common Mistakes

- **Expecting `var` and `let` to fail the same way** — `var` returns `undefined`; `let`/`const`
  throw.
- **Calling a function expression before its assignment** and assuming it is hoisted like a
  declaration.
- **Treating `typeof` as universally safe** — it throws for names in the TDZ.
- **Reading a block-scoped variable from an earlier line "because it's declared below"** — the
  dead zone applies from the top of the block until the declaration runs.

## ➡️ Next

Continue to [strict-mode.md](strict-mode.md) to see how one directive turns several silent mistakes —
including accidental globals — into real errors.
