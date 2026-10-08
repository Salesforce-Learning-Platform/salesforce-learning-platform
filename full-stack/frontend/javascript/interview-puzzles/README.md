# 🧠 JavaScript Interview Puzzles

## 📚 Overview

Interview questions about JavaScript rarely ask for definitions. They show a short snippet and ask, "What does
this print?" — because the answer exposes whether you hold an accurate mental model of scope, hoisting,
`this`, type coercion, and the event loop. This module trains that skill. It contains **61 "predict the
output" puzzles** in five files, each followed by an answer that was **produced by actually running the
code** and an explanation that links back to the concept files where the idea is taught, plus a study map
that connects common interview topic areas to every relevant file in this platform.

All 72 code snippets were executed in Node.js 24, three times each, to confirm the printed output is stable.
Where the result can depend on the runtime (browser or Node.js, script or module, sloppy or strict mode), the
puzzle says so and the difference was checked in a current Chromium browser too. The closure puzzles and the
browser-compatible event-loop puzzles were also run there, with identical results.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Trace closures, shadowing, and loop callbacks to predict which variable each function sees.
- Describe the two phases of execution and predict hoisting and temporal-dead-zone behaviour, including the
  differences between `var`, function declarations, function expressions, `let`, `const`, and `class`.
- Apply the call-site rules for `this`, explain how `bind` and `new` interact, and reason about property
  lookup and assignment on the prototype chain.
- Derive the result of coercion and equality questions from the underlying rules instead of memorising them.
- Order synchronous code, microtasks, and timers correctly, including `async`/`await` and promise-chain
  interleaving.
- Explain an answer aloud in a structured way, and find the gaps in your preparation with the topic map.

## 📋 Prerequisites

This module tests ideas taught elsewhere in the JavaScript section. Work through the relevant ones first:

- [Functions](../functions/) — scope, closures, arrow functions.
- [Execution Context, Hoisting, and Strict Mode](../execution-context-and-hoisting/) — how the engine sets up and runs code.
- [Advanced JavaScript](../advanced-javascript/) — `this`, prototypes, classes.
- [Operators and the Type System](../operators-and-type-system/) — coercion, equality, truthiness.
- [The Event Loop](../event-loop/) and [Asynchronous Programming and Modules](../asynchronous-programming-and-modules/) — promises, `async`/`await`, queues.

## 📂 Module Contents

| File | Puzzles | Description |
|------|:-------:|-------------|
| [closures-and-scope-puzzles.md](closures-and-scope-puzzles.md) | 11 | Loops and timers, independent counters, captured variables, shadowing, default-parameter scope, named function expressions |
| [hoisting-and-tdz-puzzles.md](hoisting-and-tdz-puzzles.md) | 12 | `var`, function declarations and expressions, the temporal dead zone, classes, block-level functions, redeclaration, and runtime differences |
| [this-and-prototype-puzzles.md](this-and-prototype-puzzles.md) | 12 | Detached methods, arrows, `bind` and `new`, shared prototype state, replacing prototypes, inherited read-only properties |
| [coercion-and-equality-puzzles.md](coercion-and-equality-puzzles.md) | 13 | `+` vs. `-`, `==` rules, object-to-primitive conversion, comparisons, sorting, floating point, `parseInt`, `Object.is`, `BigInt` |
| [event-loop-ordering-puzzles.md](event-loop-ordering-puzzles.md) | 13 | Microtasks vs. timers, executor timing, `async`/`await` interleaving, promise chains, `race` vs. `all`, Node.js `nextTick` |
| [interview-topic-map.md](interview-topic-map.md) | — | A study map linking interview topic areas to concept files and puzzles, with classic exercises and a self-check list |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** the puzzle files in the order above if you are preparing for interviews, or if the concept
modules felt abstract: puzzles turn abstract rules into traceable steps. Do each puzzle *before* opening the
answer, and write your trace down.

**Skim** the puzzles you answered correctly with a correct explanation, and concentrate on the ones you missed.
Use the [topic map](interview-topic-map.md) to decide which concept files to reread first.

If you are not preparing for interviews, the puzzles are still a quick way to test whether you really understand
what you learned in the earlier modules.

## 🧠 Knowledge Check

<details>
<summary>You see a snippet with a <code>for (var i …)</code> loop whose callbacks run later. What is the fastest reliable way to predict what they print?</summary>

Ask two questions: *which variable does each callback capture*, and *when does each callback run*. With
`var`, there is a single shared `i`, and the callbacks run after the loop has finished, so they all see the
final value. With `let`, each iteration has its own binding, so each callback sees its own value. Tracing
those two facts beats guessing. See [closures-and-scope-puzzles.md](closures-and-scope-puzzles.md).

</details>

<details>
<summary>In what order do synchronous code, <code>Promise.then</code> callbacks, and <code>setTimeout(fn, 0)</code> callbacks run?</summary>

Synchronous code runs first, until the call stack is empty. Then the **entire microtask queue** is drained
(promise callbacks, code after `await`, `queueMicrotask`), including microtasks added while draining. Only then
does the loop take the next macrotask such as the timer callback, and it drains microtasks again afterwards.
See [event-loop-ordering-puzzles.md](event-loop-ordering-puzzles.md).

</details>

## 📚 References

- MDN Web Docs, [Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures), [Hoisting](https://developer.mozilla.org/en-US/docs/Glossary/Hoisting), and [`let` (temporal dead zone)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let) — scope and declarations.
- MDN Web Docs, [`this`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this) and [Inheritance and the prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain).
- MDN Web Docs, [Equality comparisons and sameness](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness) and [Type coercion](https://developer.mozilla.org/en-US/docs/Glossary/Type_coercion).
- MDN Web Docs, [JavaScript execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model) and [Using microtasks](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide) — the event loop and microtask queue.
- Node.js, [The Node.js event loop, timers, and `process.nextTick()`](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) and [`process` API](https://nodejs.org/api/process.html) — the Node.js-specific ordering in the last event-loop puzzle.
- V8 blog, [Faster async functions and promises](https://v8.dev/blog/fast-async) — why `await` costs one microtask turn.
- javascript.info, [Closure](https://javascript.info/closure), [The old `var`](https://javascript.info/var), [Object methods and `this`](https://javascript.info/object-methods), [Prototypal inheritance](https://javascript.info/prototype-inheritance), [Type conversions](https://javascript.info/type-conversions), [Event loop](https://javascript.info/event-loop), and [Microtasks](https://javascript.info/microtask-queue) — widely used tutorials on the same topics.
- W3Schools, [Scope](https://www.w3schools.com/js/js_scope.asp), [Hoisting](https://www.w3schools.com/js/js_hoisting.asp), [`this`](https://www.w3schools.com/js/js_this.asp), [Closures](https://www.w3schools.com/js/js_function_closures.asp), and [Type conversion](https://www.w3schools.com/js/js_type_conversion.asp) — short beginner references.

## ➡️ Continue Your Learning Path

This module closes the JavaScript section. Next: [TypeScript Essentials](../../typescript/typescript-essentials/README.md),
which adds static types to the JavaScript you now know — see the [Frontend learning path](../../README.md) for
the full sequence.
