# State Management Using Redux

## Purpose

[Global State Management](../global-state-management/) covered Context and when it stops being
enough. This module covers **Redux** — a dedicated state-management library providing centralized,
predictable state updates, strict update patterns, and tooling (like time-travel debugging) that
Context alone doesn't offer. Every example in this module manages the same realistic feature: a
shopping cart shared across an e-commerce application.

## Learning Objectives

- Explain Redux's core principles: a single store, read-only state, and pure-function updates.
- Define actions, reducers, and a store, and connect them to React components.
- Use Redux Toolkit to write the same logic with dramatically less boilerplate.
- Handle asynchronous logic (an API call) correctly with async thunks.

## Prerequisites

[Global State Management](../global-state-management/).

## Files in This Module

| File | Covers |
|---|---|
| [redux-fundamentals.md](redux-fundamentals.md) | Redux's core principles, and when it's the right tool over Context |
| [actions-reducers-and-store.md](actions-reducers-and-store.md) | Building the cart with plain Redux — actions, reducers, the store |
| [redux-toolkit.md](redux-toolkit.md) | The same cart, rebuilt with Redux Toolkit's `createSlice` |
| [async-thunks.md](async-thunks.md) | Handling an async API call (checkout) within Redux's synchronous model |

## When to Deep-Dive vs. Skim

Read [redux-fundamentals.md](redux-fundamentals.md) in full even if your team already uses Redux
Toolkit exclusively (the modern standard, covered in [redux-toolkit.md](redux-toolkit.md)) — the
underlying principles (immutable updates, pure reducers) are what Redux Toolkit still enforces
underneath its friendlier API, and understanding them makes debugging a real Redux issue far
easier.

## Quick Knowledge Check

<details>
<summary>Can a Redux reducer make an API call or mutate its state argument directly?</summary>

No — a reducer must be a pure function: no side effects (like an API call), and it must return a
new state object rather than mutating the existing one, exactly the never-mutate-state discipline
from [usestate.md](../state-and-rerendering-logic/usestate.md). Async logic belongs in a thunk,
covered in [async-thunks.md](async-thunks.md), not the reducer itself.

</details>

<details>
<summary>What's the main practical reason Redux Toolkit is now the recommended way to use Redux, rather than plain Redux?</summary>

It dramatically reduces boilerplate (no more hand-written action type constants and switch
statements) while still enforcing the same core Redux principles underneath, via `createSlice`.
See [redux-toolkit.md](redux-toolkit.md).

</details>

## References

- Redux Toolkit, [Getting Started](https://redux-toolkit.js.org/introduction/getting-started)

## Continue Your Learning Path

Next: [Performance Optimization in React](../performance-optimization-in-react/) — see the
[Frontend learning path](../../README.md) for the full sequence.
