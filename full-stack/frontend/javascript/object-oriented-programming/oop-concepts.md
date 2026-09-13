# OOP Concepts

## What OOP Is Trying to Achieve

Object-oriented programming organizes code around **objects** that bundle related data and
behavior together, rather than keeping data and the functions that operate on it entirely separate.
The goal is modeling real-world (or application-domain) entities — a `User`, a `ShoppingCart` — as
self-contained units with a clear interface.

## Core Concepts, in JavaScript's Context

- **Encapsulation**: bundling data (properties) and behavior (methods) together in one object, and
  controlling what's exposed externally versus kept as internal detail. JavaScript supports this
  directly via classes, including genuinely private fields (prefixed with `#`, covered in
  [classes-and-inheritance.md](classes-and-inheritance.md)).
- **Abstraction**: exposing a simple interface while hiding complex implementation detail behind
  it — a `user.save()` method might involve significant internal logic the caller never needs to
  see.
- **Inheritance**: one class building on another, inheriting its behavior and extending or
  overriding parts of it — covered in depth in
  [classes-and-inheritance.md](classes-and-inheritance.md).
- **Polymorphism**: different objects responding to the same method call in their own
  type-appropriate way — e.g., a `speak()` method that behaves differently for a `Dog` object
  versus a `Cat` object, without the calling code needing to know which specific type it has.

## JavaScript Is Not a "Classical OOP" Language at Its Core

This is worth being precise about: JavaScript's underlying object model is **prototype-based** (see
[advanced-javascript/prototypes.md](../advanced-javascript/prototypes.md)), not class-based the way
Java or C++ are natively. The modern `class` syntax (covered in
[classes-and-inheritance.md](classes-and-inheritance.md)) is a more convenient, familiar-looking
layer built *on top of* that prototype system — genuinely useful, but worth recognizing as syntax
sugar rather than a fundamentally different underlying mechanism, especially once inheritance
starts behaving in ways that surprise developers coming from purely classical-OOP backgrounds.

## Common Mistakes

- Assuming JavaScript's OOP behaves identically to a classical, class-based language just because
  the `class` keyword looks similar — some behaviors (particularly around prototypes and `this`)
  genuinely differ.
- Over-applying OOP patterns to problems that don't actually need them — JavaScript supports
  multiple paradigms (functional patterns are extremely common too), and forcing every problem into
  a class hierarchy isn't always the simplest solution.
- Confusing encapsulation (bundling data and behavior) with genuine privacy — before private class
  fields existed, JavaScript objects had no real way to hide internal data at all.

## Next

Continue to [constructors.md](constructors.md) to see the original mechanism for creating
multiple similar objects, which classes are built on top of.
