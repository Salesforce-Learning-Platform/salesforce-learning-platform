# Introduction to JavaScript

## Purpose

JavaScript is the language that makes web pages interactive — every button click handler, every
dynamic UI update, and (via Node.js) much of the tooling covered in
[Preparing Your Machine](../../foundations/preparing-your-machine/) is JavaScript. This module
starts from zero: what the language is, how to run it, and its most basic building blocks.

## Learning Objectives

- Explain what JavaScript is and where it runs (browser and Node.js).
- Set up a working JavaScript environment and run a script both in the browser and via Node.
- Declare variables correctly using `let`, `const`, and know why `var` is now avoided.
- Identify JavaScript's data types and explain the difference between primitive and object types.

## Prerequisites

[Preparing Your Machine](../../foundations/preparing-your-machine/), particularly
[installing a package manager and Node](../../foundations/preparing-your-machine/installing-a-package-manager-and-node.md).

## Files in This Module

| File | Covers |
|---|---|
| [what-is-javascript.md](what-is-javascript.md) | What JavaScript is, its history, and where it runs |
| [setting-up-javascript.md](setting-up-javascript.md) | Running JavaScript in the browser console, an HTML file, and Node.js |
| [variables.md](variables.md) | `let`, `const`, `var`, and why modern code avoids `var` |
| [data-types.md](data-types.md) | Primitive types and the object type |

## When to Deep-Dive vs. Skim

If you have programming experience in another language, skim
[what-is-javascript.md](what-is-javascript.md) and [setting-up-javascript.md](setting-up-javascript.md),
but read [variables.md](variables.md) and [data-types.md](data-types.md) closely — JavaScript's
type system has real, non-obvious behaviors (like dynamic and loose typing) that differ from many
statically-typed languages.

## Quick Knowledge Check

<details>
<summary>Why do modern JavaScript codebases avoid `var` in favor of `let`/`const`?</summary>

`var` is function-scoped and hoisted in ways that create subtle bugs (accessible before
declaration, no block scoping); `let`/`const` are block-scoped and behave more predictably. See
[variables.md](variables.md).

</details>

<details>
<summary>Is an array a primitive type or an object in JavaScript?</summary>

An object — JavaScript has seven primitive types (Boolean, null, undefined, Number, BigInt,
String, Symbol) and one non-primitive type, Object, which includes arrays, functions, and plain
objects. See [data-types.md](data-types.md).

</details>

## References

- MDN Web Docs, [JavaScript Guide: Grammar and Types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types)
- TC39, [ECMAScript Language Specification](https://tc39.es/ecma262/)

## Continue Your Learning Path

Next: [JavaScript Operators and Type System](../operators-and-type-system/) — see the
[Frontend learning path](../../README.md) for the full sequence.
