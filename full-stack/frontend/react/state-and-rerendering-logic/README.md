# State and Re-rendering Logic

## Purpose

[what-is-react.md](../introduction-to-react/what-is-react.md) introduced "UI as a function of
state" conceptually. This module makes it concrete: what state actually is in React terms, the
`useState` hook, exactly what triggers a re-render, and why state updates are batched.

## Learning Objectives

- Explain what "state" means in React, and how it differs from a plain variable or a prop.
- Use `useState` correctly, including the updater-function form.
- Explain what a re-render actually is, and what triggers one.
- Explain state batching and why it matters for predicting a component's behavior.

## Prerequisites

[Component Architecture and Composition](../component-architecture-and-composition/).

## Files in This Module

| File | Covers |
|---|---|
| [understanding-state.md](understanding-state.md) | What state is, and how it differs from props and plain variables |
| [usestate.md](usestate.md) | The `useState` hook, including the updater-function form |
| [how-rerendering-works.md](how-rerendering-works.md) | What a re-render is, and exactly what triggers one |
| [batching-state-updates.md](batching-state-updates.md) | Why multiple state updates in one handler often produce only one re-render |

## When to Deep-Dive vs. Skim

Deep-dive [how-rerendering-works.md](how-rerendering-works.md) and
[batching-state-updates.md](batching-state-updates.md) together — the combination of "what
triggers a re-render" and "why updates are batched" explains a large share of "why didn't my state
update immediately" confusion that's otherwise easy to misdiagnose as a bug.

## Quick Knowledge Check

<details>
<summary>Why can't you just use a plain `let` variable inside a component instead of `useState` to track something that changes?</summary>

A plain variable's change doesn't tell React anything happened — React has no way to know it
should re-render, and even if it did, the variable would reset to its initial value on every
re-render anyway, since the component function runs again from scratch. `useState` is what
persists a value across re-renders AND triggers one when it changes. See
[understanding-state.md](understanding-state.md).

</details>

<details>
<summary>You call `setCount(count + 1)` twice in a row in the same event handler. Does count increase by 2?</summary>

Not necessarily — if both calls read the same stale `count` value from the render that's currently
executing, both compute the same new value, and the count only increases by 1. The updater-function
form, `setCount(c => c + 1)`, avoids this by always operating on the latest value. See
[usestate.md](usestate.md).

</details>

## References

- React, [State: A Component's Memory](https://react.dev/learn/state-a-components-memory)
- React, [Queueing a Series of State Updates](https://react.dev/learn/queueing-a-series-of-state-updates)

## Continue Your Learning Path

Next: [React Hooks](../react-hooks/) — see the
[Frontend learning path](../../README.md) for the full sequence.
