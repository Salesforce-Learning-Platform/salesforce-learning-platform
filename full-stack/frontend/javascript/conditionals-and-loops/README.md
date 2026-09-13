# Conditionals and Loops

## Purpose

With variables, operators, and truthy/falsy evaluation covered, this module introduces control
flow: making decisions (conditionals) and repeating work (loops) — the two mechanisms that turn a
flat sequence of statements into a program that actually branches and repeats.

## Learning Objectives

- Use `if`/`else if`/`else` and the ternary operator correctly, choosing the right one for a given
  case.
- Use `switch` where it's a genuinely better fit than a long `if`/`else if` chain.
- Choose the correct loop type (`for`, `while`, `for...of`, `for...in`) for a given task.
- Use `break` and `continue` correctly, and understand their scope within nested loops.

## Prerequisites

[JavaScript Operators and Type System](../operators-and-type-system/).

## Files in This Module

| File | Covers |
|---|---|
| [conditional-statements.md](conditional-statements.md) | `if`/`else if`/`else` and the ternary operator |
| [switch-statements.md](switch-statements.md) | `switch`, fall-through behavior, and when to prefer it |
| [loops.md](loops.md) | `for`, `while`, `do...while`, `for...of`, `for...in`, `break`/`continue` |

## Quick Knowledge Check

<details>
<summary>What happens if you forget a `break` inside a `switch` case?</summary>

Execution "falls through" into the next case, running its code too, regardless of whether that
case's condition matches — this is a real, specification-defined behavior, not a bug, but it's a
common source of accidental mistakes. See [switch-statements.md](switch-statements.md).

</details>

<details>
<summary>You need to loop over an array's values. Should you use `for...in` or `for...of`?</summary>

`for...of` — it iterates over an array's actual values. `for...in` iterates over an object's
enumerable property *keys*, which for an array means its numeric indices as strings — rarely what's
actually wanted for array iteration. See [loops.md](loops.md).

</details>

## References

- MDN Web Docs, [`for`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for)

## Continue Your Learning Path

Next: [JavaScript Functions](../functions/) — see the
[Frontend learning path](../../README.md) for the full sequence.
