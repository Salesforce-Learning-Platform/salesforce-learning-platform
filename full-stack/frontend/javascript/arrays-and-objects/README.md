# Arrays and Objects

## Purpose

Arrays and objects are JavaScript's two core data structures — covered as a single type,
"Object," in [data-types.md](../introduction-to-javascript/data-types.md). This module goes deep
on both: how to create and manipulate them, the methods that make working with them practical, and
destructuring, the syntax for extracting values from them concisely.

## Learning Objectives

- Create, access, and modify arrays and objects using the correct syntax.
- Use the most common array methods (`map`, `filter`, `reduce`, `find`) fluently, and distinguish
  mutating from non-mutating methods.
- Use `Object.keys()`, `Object.values()`, `Object.entries()`, and spread/merge objects correctly.
- Use destructuring to extract values from arrays and objects concisely.

## Prerequisites

[JavaScript Functions](../functions/), since several array methods take a function as an argument.

## Files in This Module

| File | Covers |
|---|---|
| [arrays.md](arrays.md) | Creating, indexing, and basic mutation of arrays |
| [array-methods.md](array-methods.md) | `map`, `filter`, `reduce`, `find`, and mutating vs. non-mutating methods |
| [objects.md](objects.md) | Object literals, property access, and nested objects |
| [object-methods.md](object-methods.md) | `Object.keys`/`values`/`entries`, and the spread operator for objects |
| [destructuring.md](destructuring.md) | Extracting values from arrays and objects concisely |

## When to Deep-Dive vs. Skim

Deep-dive [array-methods.md](array-methods.md), specifically the mutating-vs-non-mutating
distinction — this single misunderstanding is responsible for a large share of "why did my other
variable change too" bugs in real code, especially once React (which depends on immutability for
correct re-rendering) enters the picture.

## Quick Knowledge Check

<details>
<summary>Does `array.map(fn)` change the original array?</summary>

No — `map()` returns a brand-new array and leaves the original untouched. `push()`, `splice()`, and
`sort()`, by contrast, mutate the array in place. Knowing which category a method falls into is
essential for predicting whether other code holding a reference to the same array will be
affected. See [array-methods.md](array-methods.md).

</details>

<details>
<summary>What does `const { name, age } = user;` actually do?</summary>

It's object destructuring — it declares two new variables, `name` and `age`, extracting their
values directly from the matching properties on `user`, rather than accessing `user.name` and
`user.age` separately. See [destructuring.md](destructuring.md).

</details>

## References

- MDN Web Docs, [Array instance methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#instance_methods)
- MDN Web Docs, [Destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring)

## Continue Your Learning Path

Next: [DOM Manipulation](../dom-manipulation/) — see the
[Frontend learning path](../../README.md) for the full sequence.
