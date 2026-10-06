# 🧩 Functional JavaScript Patterns

## 📚 Overview

This module covers the functional-programming toolkit that JavaScript's first-class functions make
possible: writing higher-order functions, controlling `this` and arguments with `call`, `apply`, and
`bind`, building specialized functions with currying and partial application, composing small
functions into pipelines, keeping functions pure and data immutable, caching results with
memoization, and using IIFEs and the module pattern for private state. These are the patterns behind
much of everyday JavaScript — and a large share of JavaScript interview questions.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Write higher-order functions that accept, return, and wrap other functions without losing `this`
  or arguments.
- Use `call`, `apply`, and `bind` correctly, and explain why a bound function cannot be rebound.
- Implement and distinguish currying and partial application, including the `fn.length` caveat.
- Build `compose` and `pipe`, and debug a pipeline with a pass-through helper.
- Identify pure and impure functions, and update data immutably (including nested data) without
  relying on shallow `Object.freeze`.
- Implement memoization with sound cache keys and a bounded cache, and know when not to use it.
- Explain the IIFE and module pattern, and what replaced them in modern JavaScript.

## 📋 Prerequisites

- [Closures](../functions/closures.md) and [Scope](../functions/scope.md) — nearly every pattern here is a closure in disguise.
- [The `this` Keyword](../advanced-javascript/this-keyword.md) — `call`, `apply`, and `bind` build on its binding rules.
- [Array Methods](../arrays-and-objects/array-methods.md) — `map`, `filter`, and `reduce` are the higher-order functions you already use.
- [Execution Context, Hoisting and Strict Mode](../execution-context-and-hoisting/) — explains the environments that closures keep alive.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [higher-order-functions.md](higher-order-functions.md) | Functions as values; taking, returning, and wrapping functions; the `map(parseInt)` trap |
| [call-apply-and-bind.md](call-apply-and-bind.md) | How the three differ, everyday uses, surprising behaviors, and a simplified `bind` |
| [currying-and-partial-application.md](currying-and-partial-application.md) | The two techniques, a general `curry`, and the `fn.length` caveat |
| [function-composition-and-pipelines.md](function-composition-and-pipelines.md) | `compose`, `pipe`, `tap`, and async pipelines |
| [pure-functions-and-immutability.md](pure-functions-and-immutability.md) | Purity, side effects, immutable updates, and shallow `Object.freeze` |
| [memoization.md](memoization.md) | Caching results, cache-key pitfalls, and an LRU cache |
| [iife-and-the-module-pattern.md](iife-and-the-module-pattern.md) | IIFEs, private state through closures, and modern equivalents; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you are preparing for JavaScript interviews — "implement `bind`", "implement
`curry`", "implement `memoize`", "what is a pure function", and "what is an IIFE" are all standard
questions, and every one has a worked answer here.

**Skim** if you already write functional-style JavaScript daily — but read the memoization cache-key
section and the `Object.freeze` shallowness section, which cover the mistakes experienced developers
still make.

## 🧠 Knowledge Check

<details>
<summary>What does <code>["1", "2", "3"].map(parseInt)</code> return, and why?</summary>

`[1, NaN, NaN]`. `map` calls its callback with three arguments — the element, the index, and the
array — and `parseInt` treats its second argument as the radix. So the calls are `parseInt("1", 0)`,
`parseInt("2", 1)`, and `parseInt("3", 2)`; radixes 1 and 2 are invalid for these inputs, giving
`NaN`. Passing `Number`, or wrapping it as `(s) => parseInt(s, 10)`, avoids the problem.

</details>

<details>
<summary>Why must a function be pure for memoization to be correct?</summary>

A memoized function returns the *stored* result when it sees the same arguments again. That is only
valid if the same arguments always produce the same result and the call has no side effects that need
to happen each time. With an impure function — one depending on the current time, randomness, or
outside state — the cache would serve stale or wrong values.

</details>

## 📚 References

- [MDN: First-class Function](https://developer.mozilla.org/en-US/docs/Glossary/First-class_Function) — the property that makes higher-order functions possible.
- [MDN: `Function.prototype.bind()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind) — bound functions, preset arguments, and `new`.
- [MDN: `Function.length`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/length) — how declared parameters are counted.
- [MDN: `Array.prototype.map()` — using `parseInt()` with `map()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) — the classic callback-arguments gotcha.
- [MDN: `Object.freeze()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze) — shallow freezing and the `deepFreeze` pattern.
- [MDN: IIFE](https://developer.mozilla.org/en-US/docs/Glossary/IIFE) — the definition and common uses.
- [javascript.info: Decorators and forwarding, call/apply](https://javascript.info/call-apply-decorators), [Function binding](https://javascript.info/bind), and [Currying](https://javascript.info/currying-partials) — widely used walkthroughs of the same patterns.
- [React: Keeping Components Pure](https://react.dev/learn/keeping-components-pure) — why purity matters in a real framework.
- [Immer](https://immerjs.github.io/immer/) — a library for writing immutable updates as if mutating a draft.

## ➡️ Continue Your Learning Path

Continue to the Objects in Depth module, the next module in this section, which examines property
descriptors, freezing, copying, JSON, private fields, and `Proxy`.
