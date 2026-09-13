# JavaScript Object-Oriented Programming

## Purpose

This module introduces object-oriented programming (OOP) in JavaScript: the core concepts,
constructor functions (the mechanism classes are built on), and the modern `class` syntax with
inheritance. [advanced-javascript](../advanced-javascript/) goes deeper into what's actually
happening underneath (prototypes).

## Learning Objectives

- Explain the core OOP concepts: encapsulation, and how JavaScript approximates them.
- Create objects with constructor functions, and explain what `new` actually does.
- Write classes using modern `class` syntax, including inheritance with `extends`/`super`.

## Prerequisites

[JavaScript Arrays and Objects](../arrays-and-objects/) and [JavaScript Functions](../functions/).

## Files in This Module

| File | Covers |
|---|---|
| [oop-concepts.md](oop-concepts.md) | What OOP is trying to achieve, in JavaScript's specific context |
| [constructors.md](constructors.md) | Constructor functions and what `new` actually does |
| [classes-and-inheritance.md](classes-and-inheritance.md) | Modern `class` syntax, `extends`, and `super` |

## When to Deep-Dive vs. Skim

If you have OOP experience in another language (Java, Python), skim
[oop-concepts.md](oop-concepts.md) but read
[classes-and-inheritance.md](classes-and-inheritance.md) closely — JavaScript's classes are
genuinely just a more convenient syntax over its underlying prototype system (covered in
[advanced-javascript](../advanced-javascript/)), which behaves differently from classical
inheritance in other languages in ways worth knowing explicitly rather than assuming.

## Quick Knowledge Check

<details>
<summary>What does the `new` keyword actually do when calling a constructor function?</summary>

It creates a new empty object, sets that object as `this` inside the constructor, links the
object's prototype to the constructor's `prototype` property, and returns the object automatically
(unless the constructor explicitly returns a different object). See [constructors.md](constructors.md).

</details>

<details>
<summary>What does `super()` do inside a subclass's constructor?</summary>

Calls the parent class's constructor, which must happen before `this` can be used in the
subclass's own constructor — JavaScript enforces this ordering. See
[classes-and-inheritance.md](classes-and-inheritance.md).

</details>

## References

- MDN Web Docs, [Using classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_classes)

## Continue Your Learning Path

Next: [Advanced JavaScript](../advanced-javascript/) — see the
[Frontend learning path](../../README.md) for the full sequence.
