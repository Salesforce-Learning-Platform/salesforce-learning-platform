# TypeScript Essentials

## Purpose

TypeScript adds a static type system on top of JavaScript — catching a category of bugs (wrong
argument types, typos in property names, forgetting a `null` check) at compile time rather than at
runtime. This module is the complete introduction: from why static types help, through the type
system's core building blocks, to generics and the utility types used constantly in real code.

## Learning Objectives

- Explain what problem TypeScript solves that plain JavaScript cannot catch on its own.
- Annotate variables, function parameters, and return values with basic types.
- Define shapes with interfaces and type aliases, and know when to reach for each.
- Model "one of several possibilities" with unions, and combine shapes with intersections.
- Use enums appropriately, and understand their tradeoffs.
- Write generic functions and types that work across multiple types without losing type safety.
- Use the most common built-in utility types to transform existing types.
- Add TypeScript incrementally to an existing JavaScript project.

## Prerequisites

The full [JavaScript domain](../../javascript/), especially
[Arrays and Objects](../../javascript/arrays-and-objects/) and
[Object-Oriented Programming](../../javascript/object-oriented-programming/).

## Files in This Module

| File | Covers |
|---|---|
| [introduction-to-typescript.md](introduction-to-typescript.md) | What TypeScript is, and the problem static typing solves |
| [basic-types.md](basic-types.md) | Annotating variables, parameters, and return values |
| [interfaces.md](interfaces.md) | Defining object shapes with `interface` |
| [type-aliases.md](type-aliases.md) | `type`, and when it's preferred over `interface` |
| [unions-and-intersections.md](unions-and-intersections.md) | `\|` for "one of," `&` for "combined with" |
| [enums.md](enums.md) | Named constant sets, and their real tradeoffs |
| [generics.md](generics.md) | Writing reusable, type-safe functions and types |
| [utility-types.md](utility-types.md) | `Partial`, `Pick`, `Omit`, `Record`, and more |
| [typescript-with-javascript-projects.md](typescript-with-javascript-projects.md) | Adopting TypeScript incrementally in an existing codebase |

## When to Deep-Dive vs. Skim

Deep-dive [interfaces.md](interfaces.md) and [generics.md](generics.md) — object shapes and
generics are used constantly once you reach React (nearly every component's props are typed with
an interface, and many hooks and utilities are generic). Skim
[enums.md](enums.md) if you're short on time; unions are frequently the more idiomatic modern
choice, as the file itself explains.

## Quick Knowledge Check

<details>
<summary>Does TypeScript's type checking do anything at runtime, in the browser?</summary>

No — types are checked at compile time and then completely erased; the JavaScript that actually
runs has no trace of them. TypeScript catches type errors before the code ever runs, but provides
zero runtime type checking on its own. See [introduction-to-typescript.md](introduction-to-typescript.md).

</details>

<details>
<summary>You need a type representing "either a string or a number." Should you use a union, an intersection, or an enum?</summary>

A union: `string | number`. Intersections (`&`) combine requirements (must satisfy both), the
opposite of what's needed here. See [unions-and-intersections.md](unions-and-intersections.md).

</details>

## References

- TypeScript Handbook, [The Basics](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)
- TypeScript Handbook, [Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- TypeScript Handbook, [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)

## Continue Your Learning Path

Next: [Introduction to React](../../react/introduction-to-react/) — see the
[Frontend learning path](../../README.md) for the full sequence.
