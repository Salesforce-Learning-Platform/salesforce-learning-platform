# Additional JavaScript Topics

## Purpose

This module rounds out the JavaScript domain with three topics that don't fit elsewhere but are
worth knowing: Symbols (a distinct primitive type), iterators and generators (the mechanism behind
`for...of`, from first principles), and regular expressions (pattern matching in strings).

## Learning Objectives

- Explain what a Symbol is and its main practical use case.
- Explain the iterator protocol, and write a generator function.
- Write and use basic regular expressions for common string-matching tasks.

## Prerequisites

[JavaScript Arrays and Objects](../arrays-and-objects/) and
[JavaScript Conditionals and Loops](../conditionals-and-loops/).

## Files in This Module

| File | Covers |
|---|---|
| [symbols.md](symbols.md) | The `Symbol` primitive type and its main use case |
| [iterators-and-generators.md](iterators-and-generators.md) | The iterator protocol, and `function*`/`yield` |
| [regular-expressions.md](regular-expressions.md) | Pattern syntax, flags, and common string methods that use them |

## When to Deep-Dive vs. Skim

[iterators-and-generators.md](iterators-and-generators.md) explains *why* `for...of` (from
[loops.md](../conditionals-and-loops/loops.md)) works on arrays, strings, Maps, and Sets uniformly
— worth reading in full once, even if you never write a generator function yourself day to day.
[regular-expressions.md](regular-expressions.md) is better treated as a reference to return to
when you actually need a specific pattern, rather than read and memorized upfront.

## Quick Knowledge Check

<details>
<summary>What makes an object "iterable" — usable with `for...of`?</summary>

Implementing the iterator protocol: having a `[Symbol.iterator]()` method that returns an object
with a `next()` method, which itself returns `{ value, done }` on each call. Arrays, strings, Maps,
and Sets all implement this already; plain objects don't, by default. See
[iterators-and-generators.md](iterators-and-generators.md).

</details>

<details>
<summary>What's the main practical use case for a Symbol?</summary>

Creating a guaranteed-unique property key — since every Symbol is unique even if created with the
same description, it can be used as an object key that will never accidentally collide with a
string key from another part of the codebase. See [symbols.md](symbols.md).

</details>

## References

- MDN Web Docs, [Iterators and generators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Iterators_and_generators)
- MDN Web Docs, [Regular expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)

## Continue Your Learning Path

This is the last module in the JavaScript domain. Continue to
[TypeScript Essentials](../../typescript/typescript-essentials/) — see the
[Frontend learning path](../../README.md) for the full sequence.
