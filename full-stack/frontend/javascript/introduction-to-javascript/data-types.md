# Data Types

## Seven Primitives, One Object Type

JavaScript's type system, per the ECMAScript specification, has seven **primitive** types and one
**object** type:

| Primitive | Example | Notes |
|---|---|---|
| `Boolean` | `true`, `false` | |
| `Number` | `42`, `3.14`, `-1` | A single type for both integers and decimals |
| `BigInt` | `9007199254740993n` | For integers beyond `Number`'s safe precision limit |
| `String` | `"hello"`, `'hello'`, `` `hello` `` | Any of three quote styles |
| `undefined` | `undefined` | The default value of a declared-but-unassigned variable |
| `null` | `null` | Represents the deliberate absence of a value |
| `Symbol` | `Symbol("id")` | A unique, immutable identifier (less commonly used day-to-day) |

Everything else — arrays, functions, plain objects, dates — is an **object**, the one non-primitive
type.

## `typeof`

```js
typeof 42;          // "number"
typeof "hello";      // "string"
typeof true;          // "boolean"
typeof undefined;     // "undefined"
typeof null;          // "object"  — a well-known, long-standing quirk (see below)
typeof {};             // "object"
typeof [];              // "object" — arrays are objects too
typeof function(){};    // "function"
```

## `undefined` vs. `null` — Not Interchangeable

- **`undefined`** means a variable has been declared but never assigned a value — this is
  JavaScript's own default, not something a developer typically assigns deliberately.
- **`null`** represents an intentional, deliberate "no value" — something a developer explicitly
  assigns to indicate absence.

```js
let a;           // undefined — never assigned
let b = null;    // null — deliberately set to "nothing"
```

`typeof null` returning `"object"` is a famous, specification-acknowledged bug from JavaScript's
earliest implementation, preserved for backward compatibility rather than fixed — worth knowing
specifically so it doesn't cause confusion when it's inevitably encountered.

## Primitives Are Immutable and Compared by Value

Primitive values themselves can't be changed (a string's characters can't be mutated in place —
any "modification" produces a new string) and are compared by their actual value:

```js
"abc" === "abc"; // true — same value
```

Objects, by contrast, are compared by *reference*, not by their contents — covered in depth in
[arrays-and-objects](../arrays-and-objects/).

## Common Mistakes

- Treating `undefined` and `null` as interchangeable, when they represent conceptually different
  things (unassigned vs. deliberately empty).
- Being caught off guard by `typeof null === "object"` and concluding `null` is an object type —
  it remains a primitive, this is purely a long-standing quirk of `typeof`'s implementation.
- Forgetting that a string's methods (like `.toUpperCase()`) return a *new* string rather than
  modifying the original, since strings are immutable primitives.

## Module Summary

Across this module: JavaScript is a dynamically and loosely typed language that runs in both the
browser and Node.js, standardized as ECMAScript (see
[what-is-javascript.md](what-is-javascript.md)); it can be run via the browser console, a
`<script>` tag, or the `node` CLI (see
[setting-up-javascript.md](setting-up-javascript.md)); `const` should be the default variable
declaration, with `let` for genuine reassignment and `var` avoided entirely in new code (see
[variables.md](variables.md)); and the type system has seven primitive types plus one object type,
with `undefined` and `null` representing conceptually distinct kinds of "no value."
