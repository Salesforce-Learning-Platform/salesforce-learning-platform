# JavaScript Operators and Type System

## Purpose

Building on [data-types.md](../introduction-to-javascript/data-types.md), this module covers how
values are combined and compared — operators — and the type system's most notorious behavior:
automatic type coercion, and how conditions decide whether a value counts as "true."

## Learning Objectives

- Use arithmetic, comparison, logical, and assignment operators correctly.
- Explain when and why JavaScript automatically coerces types, and predict common coercion results.
- Explain truthy/falsy values and correctly use them in conditions.
- Always choose `===`/`!==` over `==`/`!=` and explain why.

## Prerequisites

[Introduction to JavaScript](../introduction-to-javascript/).

## Files in This Module

| File | Covers |
|---|---|
| [operators.md](operators.md) | Arithmetic, comparison, logical, and assignment operators |
| [type-coercion.md](type-coercion.md) | Implicit vs. explicit type conversion, and `==` vs. `===` |
| [truthy-and-falsy.md](truthy-and-falsy.md) | Which values are falsy, and how conditions evaluate them |

## When to Deep-Dive vs. Skim

Deep-dive [type-coercion.md](type-coercion.md) — JavaScript's automatic type coercion is
responsible for a disproportionate share of confusing bugs and "JavaScript is weird" jokes, and
understanding it precisely removes most of that confusion.

## Quick Knowledge Check

<details>
<summary>Why does `"5" + 3` produce `"53"` but `"5" - 3` produces `2`?</summary>

`+` is overloaded for both addition and string concatenation — when either operand is a string, it
concatenates. `-` has no string meaning, so JavaScript coerces the string to a number first. See
[type-coercion.md](type-coercion.md).

</details>

<details>
<summary>Is an empty array `[]` truthy or falsy in a condition?</summary>

Truthy — the only falsy values are `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, and `NaN`.
An empty array and empty object are both objects, and all objects are truthy regardless of their
contents. See [truthy-and-falsy.md](truthy-and-falsy.md).

</details>

## References

- MDN Web Docs, [Expressions and operators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators)
- MDN Web Docs, [Truthy](https://developer.mozilla.org/en-US/docs/Glossary/Truthy)

## Continue Your Learning Path

Next: [JavaScript Conditionals and Loops](../conditionals-and-loops/) — see the
[Frontend learning path](../../README.md) for the full sequence.
