# Modern JavaScript

## Purpose

This module rounds up ES6+ syntax and the features added to JavaScript since. Several — `let`/`const`,
destructuring, spread/rest — were already covered where they naturally fit earlier in this platform;
this module gives them a short, consolidated reference. Its real depth is in the topics that appear in
modern codebases and interviews but were not covered elsewhere: template literals, optional chaining and
nullish coalescing, logical assignment and numeric separators, the newer array and object methods,
top-level `await` with import attributes, and static blocks, error `cause`, and iterator helpers.

## Files in This Module

| File | Covers |
|---|---|
| [let-and-const.md](let-and-const.md) | Quick reference — full treatment in [variables.md](../introduction-to-javascript/variables.md) |
| [destructuring-and-default-parameters.md](destructuring-and-default-parameters.md) | Quick reference — full treatment in [destructuring.md](../arrays-and-objects/destructuring.md) and [parameters-and-return-values.md](../functions/parameters-and-return-values.md) |
| [spread-and-rest-operators.md](spread-and-rest-operators.md) | Quick reference — full treatment in [array-methods.md](../arrays-and-objects/array-methods.md), [object-methods.md](../arrays-and-objects/object-methods.md), and [parameters-and-return-values.md](../functions/parameters-and-return-values.md) |
| [template-literals.md](template-literals.md) | String interpolation, multi-line strings, and tagged templates |
| [optional-chaining-and-nullish-coalescing.md](optional-chaining-and-nullish-coalescing.md) | `?.` and `??` — safely accessing nested, possibly-missing values |
| [logical-assignment-and-numeric-separators.md](logical-assignment-and-numeric-separators.md) | `\|\|=`, `&&=`, `??=` (and why they short-circuit), plus `1_000_000` numeric separators and their syntax rules |
| [modern-array-and-object-methods.md](modern-array-and-object-methods.md) | `at()`, `findLast()`, `toSorted()`/`toReversed()`/`toSpliced()`/`with()`, `Object.hasOwn()`, `Object.groupBy()` and `Map.groupBy()` |
| [top-level-await-and-import-attributes.md](top-level-await-and-import-attributes.md) | `await` at module level, how it delays importers, its failure and bundling behavior, and importing JSON with `with { type: "json" }` |
| [static-blocks-error-cause-and-iterator-helpers.md](static-blocks-error-cause-and-iterator-helpers.md) | Class `static { }` blocks, `new Error(msg, { cause })`, lazy iterator helpers (`map`, `filter`, `take`, …), and a table of newer features to check before relying on them |

## When to Deep-Dive vs. Skim

Skim the first three files if you've already worked through the earlier modules they reference —
they exist purely as a consolidated index. Deep-dive
[optional-chaining-and-nullish-coalescing.md](optional-chaining-and-nullish-coalescing.md) — it
directly solves the "chaining property access onto a value that might be undefined" problem
flagged as a common mistake in [objects.md](../arrays-and-objects/objects.md).

Read the four newer files in order if you want the full picture; if you are short on time, take these
from each:

- **Logical assignment** — the `||=` vs. `??=` distinction (it prevents overwriting a legitimate `0`).
- **Array and object methods** — `toSorted()` and `Object.groupBy()` replace the most common
  workarounds in everyday code.
- **Top-level `await`** — the "applications yes, libraries cautiously" rule.
- **Iterator helpers** — laziness is the idea worth understanding, even if you don't use the methods yet.

Everything in these four files was executed in Node.js 24 and a current Chromium browser while writing.
Each file also states which features are Baseline *widely available* and which are newer, so you can
decide what is safe for your target browsers.

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

<details>
<summary>A setting `volume` can legitimately be `0`. Which should you use to give it a default — `volume ||= 50` or `volume ??= 50`?</summary>

`volume ??= 50`. `||=` replaces every falsy value, so a deliberate `0` would be overwritten with `50`;
`??=` assigns only when the value is `null` or `undefined`. See
[logical-assignment-and-numeric-separators.md](logical-assignment-and-numeric-separators.md).

</details>

<details>
<summary>How do you sort an array without changing the original, and why might `[1, 10, 2].toSorted()` surprise you?</summary>

Use `toSorted()`, which returns a new array and leaves the original untouched. Without a comparator it
sorts values as strings, so `[1, 10, 2].toSorted()` gives `[1, 10, 2]` rather than `[1, 2, 10]`; pass
`(a, b) => a - b` for numbers. See [modern-array-and-object-methods.md](modern-array-and-object-methods.md).

</details>

<details>
<summary>If module `a.mjs` uses top-level `await` and `main.mjs` imports it, when does `main.mjs` start running?</summary>

Only after `a.mjs` has finished its awaited work — and if the awaited promise rejects, `main.mjs` never
runs. Unrelated sibling modules are not blocked. See
[top-level-await-and-import-attributes.md](top-level-await-and-import-attributes.md).

</details>

<details>
<summary>Why are iterator helpers like `take()` able to work on an infinite generator when array methods cannot?</summary>

They are lazy: each value is pulled through the chain only when it is needed, so `take(5)` stops the
pipeline after five results instead of trying to collect an endless sequence into an array first. See
[static-blocks-error-cause-and-iterator-helpers.md](static-blocks-error-cause-and-iterator-helpers.md).

</details>

## References

- MDN Web Docs, [Template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)
- MDN Web Docs, [Optional chaining (`?.`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining)
- MDN Web Docs, [Logical OR assignment (`||=`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Logical_OR_assignment) and [Nullish coalescing assignment (`??=`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_assignment)
- MDN Web Docs, [Lexical grammar — numeric separators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#numeric_separators)
- MDN Web Docs, [`Array.prototype.toSorted()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted), [`Object.hasOwn()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwn), and [`Object.groupBy()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy)
- MDN Web Docs, [`await` — top level await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await#top_level_await) and [import attributes (`with`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import/with)
- MDN Web Docs, [Static initialization blocks](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Static_initialization_blocks), [`Error` `cause`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause), and [`Iterator`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator)
- W3Schools, [JavaScript 2021](https://www.w3schools.com/js/js_2021.asp), [JavaScript 2022](https://www.w3schools.com/js/js_2022.asp), and [JavaScript 2023](https://www.w3schools.com/js/js_2023.asp) — short feature summaries by release year
- javascript.info, [Nullish coalescing operator `??`](https://javascript.info/nullish-coalescing-operator) and [Custom errors, extending Error](https://javascript.info/custom-errors)

## Continue Your Learning Path

Next: [Additional JavaScript Topics](../additional-javascript-topics/) — see the
[Frontend learning path](../../README.md) for the full sequence.
