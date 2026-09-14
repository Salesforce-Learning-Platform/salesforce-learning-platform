# Performance Optimization in React

## Purpose

Earlier modules mentioned `memo`, `useMemo`, and `useCallback` in passing. This module covers them
properly, plus code splitting and lazy loading for reducing initial bundle size, and the React
Profiler for actually measuring performance rather than guessing at it.

## Learning Objectives

- Use `memo` to skip a component's re-render when its props haven't genuinely changed.
- Explain code splitting, and use `lazy`/`Suspense` to defer loading a component's code.
- Apply lazy loading to routes and heavy, conditionally-shown components.
- Use the React Profiler to identify a genuine performance problem before optimizing.

## Prerequisites

[React Hooks](../react-hooks/) and [Client-Side Routing](../client-side-routing/).

## Files in This Module

| File | Covers |
|---|---|
| [memoization.md](memoization.md) | `memo`, and pairing it correctly with `useCallback`/`useMemo` |
| [code-splitting.md](code-splitting.md) | `lazy`/`Suspense` for splitting the JavaScript bundle |
| [lazy-loading.md](lazy-loading.md) | Applying code splitting to routes and heavy conditional UI |
| [react-profiler.md](react-profiler.md) | Measuring actual re-render cost before optimizing |

## When to Deep-Dive vs. Skim

Deep-dive [react-profiler.md](react-profiler.md) — the single most important idea in this module
isn't any specific optimization technique, it's **measuring before optimizing**. Applying `memo`
or `useMemo` reflexively without profiling first, as flagged repeatedly in earlier modules, adds
real overhead for often negligible or nonexistent benefit.

## Quick Knowledge Check

<details>
<summary>Does wrapping a component in `memo` guarantee it never re-renders unnecessarily?</summary>

No — `memo` only skips a re-render when props are shallowly equal to the previous render's. If a
parent passes a new object, array, or function literal on every render (without `useMemo`/
`useCallback`), `memo` provides no benefit at all, since those props are never actually equal by
reference. See [memoization.md](memoization.md).

</details>

<details>
<summary>Why would you wrap a route's component in `lazy()` rather than importing it normally?</summary>

So its JavaScript code isn't included in the initial bundle at all — it's only fetched when a user
actually navigates to that route, reducing what everyone has to download just to load the app's
first page. See [code-splitting.md](code-splitting.md).

</details>

## References

- React, [`memo`](https://react.dev/reference/react/memo)
- React, [`lazy`](https://react.dev/reference/react/lazy)

## Continue Your Learning Path

Next: [React Error Handling and Debugging](../error-handling-and-debugging/) — see the
[Frontend learning path](../../README.md) for the full sequence.
