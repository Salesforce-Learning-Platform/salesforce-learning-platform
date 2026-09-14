# React Lifecycle and useEffect

## Purpose

Rendering (covered in the previous two modules) describes what a component looks like for a given
state. This module covers the other half: **effects** — code that needs to run in response to
rendering itself, to synchronize a component with something outside React entirely (a
subscription, a timer, fetching data).

## Learning Objectives

- Explain what an "effect" is, and how it differs from an event handler.
- Use `useEffect` correctly, including its three parts (setup, dependencies, cleanup).
- Choose the correct dependency array for a given effect, and explain the consequences of getting
  it wrong.
- Write cleanup functions that correctly undo what an effect set up.

## Prerequisites

[React Hooks](../react-hooks/).

## Files in This Module

| File | Covers |
|---|---|
| [component-lifecycle.md](component-lifecycle.md) | Mount, update, and unmount — the three lifecycle phases |
| [understanding-useeffect.md](understanding-useeffect.md) | What an effect is, and how `useEffect` differs from an event handler |
| [dependency-array.md](dependency-array.md) | Choosing the dependency array, and the consequences of getting it wrong |
| [cleanup-functions.md](cleanup-functions.md) | Undoing an effect's setup — required for subscriptions, timers, and connections |

## When to Deep-Dive vs. Skim

Deep-dive [dependency-array.md](dependency-array.md) — an incorrect dependency array is one of the
single most common sources of real React bugs (stale data, infinite loops, effects that never
re-run when they should), and getting genuinely comfortable with it pays off across every
component you'll ever write with `useEffect`.

## Quick Knowledge Check

<details>
<summary>Is an effect the right place to handle a button's onClick?</summary>

No — a button click is a direct response to user interaction, handled by an event handler passed
to `onClick`. Effects are for synchronizing with something external in response to rendering
itself (a component appearing, or specific values changing) — not for responding to a specific
user action. See [understanding-useeffect.md](understanding-useeffect.md).

</details>

<details>
<summary>Why does forgetting a value in an effect's dependency array cause a real bug, not just a lint warning?</summary>

The effect's function closes over (see [closures.md](../../javascript/functions/closures.md))
whatever values were in scope when it was created — if a used value is missing from the dependency
array, the effect won't re-run when that value changes, and will keep using its stale, outdated
value indefinitely. See [dependency-array.md](dependency-array.md).

</details>

## References

- React, [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)
- React, [Lifecycle of Reactive Effects](https://react.dev/learn/lifecycle-of-reactive-effects)

## Continue Your Learning Path

Next: [Client-Side Routing](../client-side-routing/) — see the
[Frontend learning path](../../README.md) for the full sequence.
