# Global State Management

## Purpose

[component-composition.md](../component-architecture-and-composition/component-composition.md)
solved prop drilling for content, using `children`. This module covers the Context API — React's
built-in solution for prop drilling with *data* (like the currently logged-in user, or a chosen
theme) that many components genuinely need, regardless of how deeply nested they are.

## Learning Objectives

- Explain what problem Context solves, and when it's the right tool (and when it isn't).
- Create, provide, and consume a context correctly.
- Explain why every consumer of a context re-renders when its value changes, and the practical
  performance implications.
- Structure global state with patterns that avoid unnecessary re-renders.

## Prerequisites

[Component Architecture and Composition](../component-architecture-and-composition/) and
[React Hooks](../react-hooks/).

## Files in This Module

| File | Covers |
|---|---|
| [context-api.md](context-api.md) | Creating, providing, and consuming a context |
| [context-performance.md](context-performance.md) | Why every consumer re-renders on change, and what that costs |
| [global-state-patterns.md](global-state-patterns.md) | Splitting contexts, and choosing Context vs. a dedicated state library |

## When to Deep-Dive vs. Skim

Deep-dive [context-performance.md](context-performance.md) before reaching for Context as a
default solution for every piece of shared data — its re-render behavior is genuinely different
from `useState`'s in a way that matters for anything updated frequently (like real-time data),
and understanding it upfront avoids a real performance problem discovered too late.

## Quick Knowledge Check

<details>
<summary>A theme context's value changes. Which components re-render?</summary>

Every component that calls `useContext` for that specific context, regardless of how deeply nested
it is or whether it visually uses the value that actually changed — this is a genuinely different
re-render behavior from ordinary props/state and is exactly why Context isn't automatically the
right tool for frequently-changing values. See [context-performance.md](context-performance.md).

</details>

<details>
<summary>Should Context be the default choice for all shared state in a React app?</summary>

No — React's own documentation recommends trying plain props and composition first, reaching for
Context only once those genuinely don't fit. See [global-state-patterns.md](global-state-patterns.md).

</details>

## References

- React, [Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context)
- React, [Scaling Up with Reducer and Context](https://react.dev/learn/scaling-up-with-reducer-and-context)

## Continue Your Learning Path

Next: [State Management Using Redux](../state-management-using-redux/) — see the
[Frontend learning path](../../README.md) for the full sequence.
