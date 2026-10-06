# 🧱 Execution Contexts and the Scope Chain

## From "What Scope Means" to "How the Engine Does It"

[scope.md](../functions/scope.md) explained *what* lexical scope and the scope chain mean.
[closures.md](../functions/closures.md) showed what happens when an inner function outlives its
outer one. This file looks at the machinery underneath both: the **execution context** the engine
creates every time code runs, and the chain of **environments** that variable lookup walks. With
that model, hoisting, closures, and `this` stop being separate rules to memorize and become
consequences of one design.

## 📦 What an Execution Context Is

```
An EXECUTION CONTEXT is the engine's bookkeeping record for a piece of
code that is currently running: which variables it can see, what
`this` is, and where execution has reached.
```

The ECMAScript specification defines an execution context as the runtime evaluation state of
executable code, and it lists the pieces tracked for each one — among them the function being run,
the realm (the set of built-in objects and the global environment), and two environment fields
named `LexicalEnvironment` and `VariableEnvironment`. You do not need every field. Day to day, three
ideas are enough:

| Part | What it holds |
|------|---------------|
| **Environment** | The variables, parameters, and function declarations of this scope |
| **Outer link** | A reference to the enclosing scope's environment (`[[OuterEnv]]` in the spec) |
| **`this` binding** | The value of `this` for this call (not for arrow functions, see below) |

Contexts come in two everyday kinds: the **global** context, created once when a script starts, and
a **function** context, created *every time a function is called*. Running contexts are tracked on
the **execution context stack** — in practice, the call stack described in
[call-stack.md](../event-loop/call-stack.md).

## 🔗 The Scope Chain Is a Linked List of Environments

```js
const language = "JavaScript";        // lives in the global environment

function outer() {
  const framework = "React";           // lives in outer's environment

  function inner() {
    const feature = "hooks";           // lives in inner's environment
    console.log(feature, framework, language);
  }

  inner();
}

outer();   // hooks React JavaScript
```

While `inner` runs, the environments are chained through their outer links:

```
inner's environment   { feature }              ──outer──▶
outer's environment   { framework, inner }     ──outer──▶
global environment    { language, outer }      ──outer──▶  null
```

Looking up a name starts in the innermost environment and follows the outer links until the name is
found. If the chain ends without a match, the lookup fails with a `ReferenceError`. That is the
**scope chain** — nothing more than environments linked outward.

(Many tutorials, including [javascript.info's closure chapter](https://javascript.info/closure), call
each environment a *Lexical Environment* and describe the same outer-reference mechanism.)

## 📍 The Outer Link Is Fixed Where a Function Is *Written*

The outer link is set when a function is **created**, pointing at the environment surrounding its
definition — not at whoever happens to call it. This is what "lexical scope" means in practice:

```js
const label = "global";

function show() {
  console.log(label);
}

function run() {
  const label = "run's local";
  show();
}

run();   // global
```

`show` is called from inside `run`, where a different `label` exists — but `show`'s outer link points
at the global environment, where it was written, so it prints `"global"`.

This also separates two ideas that are easy to blur. When `show()` runs, the **call stack** holds
`[global, run, show]` — the history of who called whom. But `show`'s **scope chain** is only
`[show, global]`. `run`'s environment is on the stack, yet it is not on `show`'s chain. The call
stack answers "which function is running and who called it"; the scope chain answers "which
variables can this code see".

## 🔄 Two Steps: Set Up, Then Run

Before a scope's code runs, the engine first **sets up that scope's bindings**: parameters, `var`
variables, and function declarations are created, while `let`, `const`, and `class` bindings are
created but left uninitialized. Only then does the code run line by line. Tutorials often label this
the "creation phase" and the "execution phase" — a useful teaching model rather than formal
specification vocabulary — and its visible consequences are what people call hoisting:

```js
function demo() {
  console.log(typeof helper);   // "function"  — set up before any line runs
  console.log(early);           // undefined   — the var binding exists, not yet assigned
  var early = 1;

  function helper() {}
}

demo();
```

The next file, [hoisting-and-the-temporal-dead-zone.md](hoisting-and-the-temporal-dead-zone.md),
turns this model into a precise per-keyword table.

## 🧳 Why Closures Work: Environments Outlive Contexts

When a function returns, its execution context is popped off the stack and is gone. Its
*environment*, however, is just an object other things can point to. If an inner function still
holds an outer link to it, the environment stays alive:

```js
function makeCounter() {
  let count = 0;
  return function () {
    count += 1;
    return count;
  };
}

const next = makeCounter();
console.log(next(), next(), next());   // 1 2 3
```

The context for `makeCounter()` finished long ago, but the returned function's outer link still
points at the environment holding `count`, so every call to `next` finds and updates the same
variable. A closure is simply a function plus the environment it was created in — see
[closures.md](../functions/closures.md) for patterns built on this, and the How JavaScript Runs
module, later in this section, for what it means for memory.

## 🎯 `this` Belongs to the Call, Not the Chain

Variables are resolved **lexically**, through the chain. For regular functions, `this` is different:
it is fixed per **call**, depending on how the function is invoked (see
[this-keyword.md](../advanced-javascript/this-keyword.md)). Arrow functions are the exception — they
have no `this` of their own and use the one from the surrounding context
([arrow-functions.md](../functions/arrow-functions.md)).

## 🌍 One Environment Detail: the Top Level Depends on Where You Run

At the top level of a *classic script* (a plain `<script>` tag), `var` declarations and function
declarations become properties of the global object, but `let`, `const`, and `class` do not:

```js
var a = 1;
let b = 2;
function f() {}

console.log(globalThis.a);        // 1
console.log(globalThis.b);        // undefined
console.log(typeof globalThis.f); // "function"
```

(The output shown is from evaluating the code as a classic script.) In **ES modules** and in
Node.js CommonJS files, top-level declarations stay local to the module and never reach the global
object — in a CommonJS file, `var cjsVar = 1` leaves `globalThis.cjsVar` as `undefined`.

## 🎤 Interview Angle

- **"What is an execution context?"** The runtime record for running code: its environment
  (variables and functions), a link to the outer environment, and the `this` value. There is one
  global context, and one new context per function call, tracked on the call stack.
- **"What is the scope chain?"** The chain of environments linked through outer references, searched
  from innermost to outermost when resolving a name. It is fixed by where code is *written*.
- **"Why can a closure still read a variable after its outer function returned?"** The function
  keeps a reference to the environment it was created in, so that environment is not discarded when
  the outer function's context is popped.

## Common Mistakes

- **Believing scope depends on where a function is called** — it depends on where it is *defined*.
- **Mixing up the call stack and the scope chain** — the stack records who called whom; the chain
  records which variables are visible. They are different structures.
- **Using "scope" and "execution context" as synonyms** — an environment is one part of an
  execution context, and an environment can outlive the context that created it.
- **Assuming top-level `var` creates a global property everywhere** — only in classic scripts, not
  in modules or Node.js CommonJS files.

## ➡️ Next

Continue to [hoisting-and-the-temporal-dead-zone.md](hoisting-and-the-temporal-dead-zone.md) to see
exactly what the "set up first" step does for each kind of declaration.
