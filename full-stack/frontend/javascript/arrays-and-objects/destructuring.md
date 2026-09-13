# Destructuring

## Array Destructuring

```js
const [first, second] = ["apple", "banana", "cherry"];
// first = "apple", second = "banana" (positional — order matters)

const [, , third] = ["apple", "banana", "cherry"];
// third = "cherry" — skip elements with empty commas
```

Array destructuring unpacks values **by position** — the variable names don't need to match
anything; only their order relative to the array matters.

## Object Destructuring

```js
const user = { name: "Ada", age: 36 };
const { name, age } = user;
// name = "Ada", age = 36 (by property NAME, not position)

const { name: userName } = user; // rename while destructuring
// userName = "Ada"
```

Object destructuring unpacks values **by property name** — order in the object doesn't matter, but
the variable name must match the property key (unless explicitly renamed).

## Default Values

```js
const { name, role = "guest" } = { name: "Ada" };
// role = "guest" — the property was missing, so the default applies
```

Works the same as default parameters (see
[parameters-and-return-values.md](../functions/parameters-and-return-values.md)): the default is
used only when the extracted value is `undefined`.

## Destructuring in Function Parameters

```js
function greet({ name, role = "guest" }) {
  return `Hello, ${name} (${role})`;
}

greet({ name: "Ada", role: "admin" });
```

This is an extremely common pattern in real code (and throughout React, where component props are
almost always destructured this way) — it makes exactly which properties a function actually uses
visible directly in its signature, rather than requiring a reader to scan the whole function body.

## Nested Destructuring

```js
const { address: { city } } = user; // reaches directly into a nested object
```

## Rest in Destructuring

```js
const { name, ...rest } = { name: "Ada", age: 36, role: "admin" };
// name = "Ada", rest = { age: 36, role: "admin" }

const [head, ...tail] = [1, 2, 3, 4];
// head = 1, tail = [2, 3, 4]
```

The rest pattern collects whatever wasn't explicitly destructured into a new array or object —
useful for separating "the one thing I need" from "everything else, unchanged."

## Common Mistakes

- Using array destructuring when object destructuring was actually needed (or vice versa) —
  remember array destructuring is positional, object destructuring is by name.
- Forgetting that destructuring a property that doesn't exist produces `undefined` rather than an
  error, unless a default value is provided.
- Over-nesting destructuring patterns to the point where the code is harder to read than simply
  accessing properties directly — destructuring should improve clarity, not obscure it.

## Module Summary

Across this module: arrays are ordered, reference-compared collections with both mutating and
non-mutating manipulation methods (see [arrays.md](arrays.md)); `map`/`filter`/`reduce`/`find` are
the core non-mutating transformation methods, and distinguishing them from mutating methods like
`push`/`sort` is essential for predictable code (see
[array-methods.md](array-methods.md)); objects are key-value collections, also compared by
reference (see [objects.md](objects.md)); `Object.keys`/`values`/`entries` and the spread operator
are the standard tools for working with and immutably updating objects (see
[object-methods.md](object-methods.md)); and destructuring provides a concise syntax for
extracting values from both, used constantly in function parameters and, later, React component
props.
