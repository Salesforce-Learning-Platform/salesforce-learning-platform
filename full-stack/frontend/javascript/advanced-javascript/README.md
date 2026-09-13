# Advanced JavaScript

## Purpose

[Object-Oriented Programming](../object-oriented-programming/) covered classes at a practical
level. This module goes underneath: the `this` binding rules that explain a lot of confusing
behavior seen earlier in this platform (especially around arrow functions), the prototype chain
that classes are actually built on, and prototypal inheritance without class syntax at all.

## Learning Objectives

- Determine what `this` refers to in any given function call, using the actual binding rules.
- Explain the prototype chain and how property/method lookup walks it.
- Create inheritance directly via prototypes, without `class` syntax.
- Explain precisely how `class` desugars to the prototype system underneath.

## Prerequisites

[JavaScript Object-Oriented Programming](../object-oriented-programming/).

## Files in This Module

| File | Covers |
|---|---|
| [this-keyword.md](this-keyword.md) | The four binding rules that determine what `this` refers to |
| [prototypes.md](prototypes.md) | The prototype chain and how property lookup actually works |
| [prototypal-inheritance.md](prototypal-inheritance.md) | Inheritance via `Object.create()`, without classes |
| [classes.md](classes.md) | How `class`/`extends` desugar to the prototype system underneath |

## When to Deep-Dive vs. Skim

Deep-dive [this-keyword.md](this-keyword.md) — confusion about `this` is one of the most common,
recurring sources of JavaScript bugs, and the four binding rules resolve nearly all of that
confusion once genuinely internalized rather than guessed at case by case.

## Quick Knowledge Check

<details>
<summary>Why did arrow functions need to exist at all, given regular functions already had `this`?</summary>

Regular functions determine `this` dynamically based on how they're *called* (see the binding
rules), which is often not what's wanted inside a callback. Arrow functions instead capture `this`
lexically from their surrounding scope at definition time — solving a genuinely common,
frustrating class of bugs. See [this-keyword.md](this-keyword.md) and revisit
[arrow-functions.md](../functions/arrow-functions.md).

</details>

<details>
<summary>When JavaScript looks up a property on an object and doesn't find it directly on that object, what happens next?</summary>

It walks up the prototype chain — checking the object's prototype, then that prototype's own
prototype, and so on, until it either finds the property or reaches the end of the chain (`null`),
at which point it returns `undefined`. See [prototypes.md](prototypes.md).

</details>

## References

- MDN Web Docs, [`this`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this)
- MDN Web Docs, [Inheritance and the prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain)

## Continue Your Learning Path

Next: [Modern JavaScript](../modern-javascript/) — see the
[Frontend learning path](../../README.md) for the full sequence.
