# 🧱 Execution Context, Hoisting and Strict Mode

## 📚 Overview

This module explains how the JavaScript engine actually runs code, and the behaviors that follow
from it: the execution context and scope chain behind lexical scope and closures, what hoisting
really does for each kind of declaration (including the temporal dead zone), what strict mode
changes, and how automatic semicolon insertion decides where statements end. Earlier modules
introduced these ideas where they first appeared; this module is the single place that explains
*why* they behave as they do.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Describe an execution context and the scope chain, and explain why scope is fixed where code is
  written rather than where it is called.
- Predict the output of hoisting puzzles by reasoning about what is set up before code runs, for
  `var`, `let`, `const`, `class`, and function declarations and expressions.
- Explain the temporal dead zone and why `let` and `const` throw where `var` returns `undefined`.
- List the main behavior changes strict mode makes, and know where it is already on.
- Recognize the automatic semicolon insertion pitfalls (`return` plus a newline, lines starting with
  `(` or `[`) and prevent them with a consistent style.

## 📋 Prerequisites

- [Scope](../functions/scope.md) and [Closures](../functions/closures.md) — this module explains the machinery behind both.
- [Variables](../introduction-to-javascript/variables.md) and [Function Declarations and Expressions](../functions/function-declarations-and-expressions.md) — where `let`/`const`/`var` and function hoisting were first introduced.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [execution-contexts-and-the-scope-chain.md](execution-contexts-and-the-scope-chain.md) | Execution contexts, environments linked by outer references, why closures keep variables alive |
| [hoisting-and-the-temporal-dead-zone.md](hoisting-and-the-temporal-dead-zone.md) | A per-keyword hoisting table, the temporal dead zone, and classic puzzles |
| [strict-mode.md](strict-mode.md) | How to enable it, where it is automatic, and what it changes, each demonstrated |
| [automatic-semicolon-insertion.md](automatic-semicolon-insertion.md) | The three ASI rules and their failure cases; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you are preparing for JavaScript interviews — hoisting, the temporal dead zone,
closures, and `this` in strict mode are among the most frequently asked topics, and the two-step
"set up, then run" method taught here solves most output-prediction puzzles.

**Skim** if you already reason confidently about scope chains and hoisting — but read the strict mode
file's table of changes, which is a quick way to check what you might be missing.

## 🧠 Knowledge Check

<details>
<summary>What does <code>console.log(a); var a = 1; console.log(b); let b = 2;</code> do, and why?</summary>

The first `console.log(a)` prints `undefined`: the `var` binding is set up at the top of the scope and
initialized to `undefined`, and only the assignment stays on its own line. The second
`console.log(b)` throws `ReferenceError: Cannot access 'b' before initialization`: a `let` binding
also exists from the top of its block, but it is uninitialized — in the temporal dead zone — until
the `let` declaration actually runs.

</details>

<details>
<summary>Why does a function that does <code>return</code> on one line and an object literal on the next return <code>undefined</code>?</summary>

`return` is a restricted production: the grammar does not allow a line break right after it, so
automatic semicolon insertion ends the statement there and the function returns `undefined`. The
object literal on the next line is then parsed as a separate (unreachable) block. Writing the value
on the same line as `return` avoids it.

</details>

## 📚 References

- [MDN: Hoisting](https://developer.mozilla.org/en-US/docs/Glossary/Hoisting) — the observable behaviors, and the note that hoisting is not a formal specification term.
- [MDN: `let` — Temporal dead zone](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let) — the definition and the `typeof` behavior.
- [MDN: Strict mode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode) — how to enable it, where it is automatic, and the full list of changes.
- [MDN: Lexical grammar — Automatic semicolon insertion](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar) — the three rules and the common pitfalls.
- [ECMAScript specification: Executable Code and Execution Contexts](https://tc39.es/ecma262/multipage/executable-code-and-execution-contexts.html) — the formal definition of execution contexts and environment records.
- [javascript.info: Variable scope, closure](https://javascript.info/closure) — a widely used walkthrough of lexical environments and the outer reference.
- [W3Schools: JavaScript Hoisting](https://www.w3schools.com/js/js_hoisting.asp) and [JavaScript Use Strict](https://www.w3schools.com/js/js_strict.asp) — beginner-friendly overviews.
- [ESLint: `no-use-before-define`](https://eslint.org/docs/latest/rules/no-use-before-define), [ESLint: `no-unexpected-multiline`](https://eslint.org/docs/latest/rules/no-unexpected-multiline), and [Prettier: Semicolons](https://prettier.io/docs/options#semicolons) — tooling that enforces the habits taught here.

## ➡️ Continue Your Learning Path

Continue to the Functional JavaScript Patterns module, the next module in this section, which builds
on closures and scope to cover higher-order functions, currying, and memoization.
