# Modern JavaScript

## Purpose

This module rounds up ES6+ syntax features. Several — `let`/`const`, destructuring, spread/rest —
were already covered where they naturally fit earlier in this platform; this module gives them a
short, consolidated reference and focuses its real depth on two genuinely new topics not yet
covered: template literals and optional chaining/nullish coalescing.

## Files in This Module

| File | Covers |
|---|---|
| [let-and-const.md](let-and-const.md) | Quick reference — full treatment in [variables.md](../introduction-to-javascript/variables.md) |
| [destructuring-and-default-parameters.md](destructuring-and-default-parameters.md) | Quick reference — full treatment in [destructuring.md](../arrays-and-objects/destructuring.md) and [parameters-and-return-values.md](../functions/parameters-and-return-values.md) |
| [spread-and-rest-operators.md](spread-and-rest-operators.md) | Quick reference — full treatment in [array-methods.md](../arrays-and-objects/array-methods.md), [object-methods.md](../arrays-and-objects/object-methods.md), and [parameters-and-return-values.md](../functions/parameters-and-return-values.md) |
| [template-literals.md](template-literals.md) | String interpolation, multi-line strings, and tagged templates |
| [optional-chaining-and-nullish-coalescing.md](optional-chaining-and-nullish-coalescing.md) | `?.` and `??` — safely accessing nested, possibly-missing values |

## When to Deep-Dive vs. Skim

Skim the first three files if you've already worked through the earlier modules they reference —
they exist purely as a consolidated index. Deep-dive
[optional-chaining-and-nullish-coalescing.md](optional-chaining-and-nullish-coalescing.md) — it
directly solves the "chaining property access onto a value that might be undefined" problem
flagged as a common mistake in [objects.md](../arrays-and-objects/objects.md).

## Quick Knowledge Check

<details>
<summary>What does `user.address?.city` return if `user.address` is `undefined`?</summary>

`undefined` — safely, without throwing a TypeError. Without `?.`, accessing `.city` on `undefined`
would throw. See [optional-chaining-and-nullish-coalescing.md](optional-chaining-and-nullish-coalescing.md).

</details>

<details>
<summary>Why prefer a template literal over string concatenation with `+`?</summary>

Interpolated expressions are more readable inline, and template literals support genuine multi-line
strings without escape characters — both a readability and a correctness improvement over chained
`+` concatenation. See [template-literals.md](template-literals.md).

</details>

## References

- MDN Web Docs, [Template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)
- MDN Web Docs, [Optional chaining (`?.`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining)

## Continue Your Learning Path

Next: [Additional JavaScript Topics](../additional-javascript-topics/) — see the
[Frontend learning path](../../README.md) for the full sequence.
