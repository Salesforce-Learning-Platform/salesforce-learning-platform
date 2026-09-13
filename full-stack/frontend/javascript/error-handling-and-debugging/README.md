# JavaScript Error Handling and Debugging

## Purpose

Code fails — a network request times out, a user enters invalid input, a variable is unexpectedly
`undefined`. This module covers handling failures deliberately with `try`/`catch`/`finally`,
JavaScript's built-in error types, and systematic debugging techniques beyond scattered
`console.log` calls.

## Learning Objectives

- Use `try`/`catch`/`finally` correctly, and know when it's actually the right tool.
- Recognize the built-in error types and what each typically indicates.
- Throw custom, meaningful errors rather than generic ones.
- Use browser DevTools' debugger effectively, beyond `console.log`.

## Prerequisites

[JavaScript Functions](../functions/).

## Files in This Module

| File | Covers |
|---|---|
| [errors.md](errors.md) | Built-in error types, and throwing custom errors |
| [try-catch-finally.md](try-catch-finally.md) | Handling exceptions, and what `finally` guarantees |
| [debugging-techniques.md](debugging-techniques.md) | Using the debugger and breakpoints systematically |

## When to Deep-Dive vs. Skim

Deep-dive [debugging-techniques.md](debugging-techniques.md) — most developers rely on
`console.log` far longer than necessary before learning to use breakpoints, which are frequently
faster for anything beyond a trivial bug.

## Quick Knowledge Check

<details>
<summary>Does code inside a `finally` block run if the `try` block throws an error that's not caught?</summary>

Yes — `finally` runs regardless of whether the `try` block succeeded, failed, or even returned
early, making it the correct place for cleanup that must always happen (closing a connection,
hiding a loading spinner). See [try-catch-finally.md](try-catch-finally.md).

</details>

<details>
<summary>What's the difference between a TypeError and a ReferenceError?</summary>

A `ReferenceError` means code referenced a variable that doesn't exist at all; a `TypeError` means
a value exists but an operation was attempted that its actual type doesn't support (like calling a
non-function, or reading a property of `undefined`). See [errors.md](errors.md).

</details>

## References

- MDN Web Docs, [`try...catch`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)
- MDN Web Docs, [`Error`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

## Continue Your Learning Path

Next: [Asynchronous Programming and Modules](../asynchronous-programming-and-modules/) — see the
[Frontend learning path](../../README.md) for the full sequence.
