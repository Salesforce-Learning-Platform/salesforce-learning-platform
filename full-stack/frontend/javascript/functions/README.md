# Functions

## Purpose

Functions are how JavaScript packages reusable behavior. This module covers the different ways to
define a function, how parameters and return values work, scope (which determines what a function
can actually see), and closures — one of JavaScript's most powerful, and most commonly
misunderstood, features.

## Learning Objectives

- Choose between function declarations, function expressions, and arrow functions correctly.
- Use default parameters, and understand the `arguments` object vs. rest parameters.
- Explain lexical scope and the scope chain.
- Explain what a closure is and recognize practical uses for one.

## Prerequisites

[JavaScript Conditionals and Loops](../conditionals-and-loops/).

## Files in This Module

| File | Covers |
|---|---|
| [function-declarations-and-expressions.md](function-declarations-and-expressions.md) | Declarations vs. expressions, and hoisting differences |
| [arrow-functions.md](arrow-functions.md) | Arrow function syntax and lexical `this` |
| [parameters-and-return-values.md](parameters-and-return-values.md) | Default parameters, rest parameters, and return values |
| [scope.md](scope.md) | Lexical scope and the scope chain |
| [closures.md](closures.md) | What a closure actually is, and practical uses |

## When to Deep-Dive vs. Skim

Deep-dive [closures.md](closures.md) — closures underlie React hooks, event handlers, and much of
idiomatic JavaScript; genuinely understanding them (not just reciting the definition) pays off
across the rest of this platform's React and JavaScript content.

## Quick Knowledge Check

<details>
<summary>Why can a function declaration be called before its definition appears in the file, but a function expression assigned to a const cannot?</summary>

Function declarations are fully hoisted (name and body both available before execution reaches
them); a `const`/`let` variable holding a function expression is only initialized when that line
actually executes — accessing it earlier throws a ReferenceError. See
[function-declarations-and-expressions.md](function-declarations-and-expressions.md).

</details>

<details>
<summary>What is a closure, in one sentence?</summary>

A function bundled together with references to the variables from the scope it was created in,
which it can still access even after that outer scope has finished executing. See
[closures.md](closures.md).

</details>

## References

- MDN Web Docs, [Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions)
- MDN Web Docs, [Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)

## Continue Your Learning Path

Next: [JavaScript Arrays and Objects](../arrays-and-objects/) — see the
[Frontend learning path](../../README.md) for the full sequence.
