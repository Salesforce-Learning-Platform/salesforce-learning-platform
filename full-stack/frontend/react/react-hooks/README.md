# React Hooks

## Purpose

`useState` (from the previous module) is one of several **hooks** — functions letting a function
component "hook into" React features like state and lifecycle behavior. This module covers the
rules every hook must follow, three more built-in hooks (`useCallback`, `useMemo`, `useRef`), and
writing your own custom hooks.

## Learning Objectives

- Apply the two rules of hooks, and explain why React actually needs them.
- Use `useRef` to persist a mutable value across renders without triggering a re-render.
- Use `useCallback`/`useMemo` to memoize values and functions, and know when it's actually worth it.
- Extract a custom hook to share stateful logic between components.

## Prerequisites

[State and Re-rendering Logic](../state-and-rerendering-logic/).

## Files in This Module

| File | Covers |
|---|---|
| [rules-of-hooks.md](rules-of-hooks.md) | The two rules every hook must follow, and why |
| [useref.md](useref.md) | Persisting a mutable value across renders without triggering one |
| [usememo.md](usememo.md) | Memoizing an expensive computed value |
| [usecallback.md](usecallback.md) | Memoizing a function reference itself |
| [custom-hooks.md](custom-hooks.md) | Extracting and sharing your own reusable stateful logic |

## When to Deep-Dive vs. Skim

Deep-dive [rules-of-hooks.md](rules-of-hooks.md) before anything else in this module — violating
these rules produces genuinely confusing bugs (state that seems to belong to the wrong render), and
understanding *why* the rules exist (not just what they are) makes them much easier to follow
correctly by instinct.

## Quick Knowledge Check

<details>
<summary>Why can't a hook be called inside an `if` statement?</summary>

React tracks hooks by the *order* they're called in, not by name — calling a hook conditionally
means that order can change between renders, which breaks React's ability to correctly match each
hook call to its persisted state. See [rules-of-hooks.md](rules-of-hooks.md).

</details>

<details>
<summary>Does updating a `useRef` value trigger a re-render, the way updating `useState` does?</summary>

No — this is `useRef`'s defining difference from `useState`: its value persists across renders,
but changing it never triggers a re-render on its own. See [useref.md](useref.md).

</details>

## References

- React, [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
- React, [Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)

## Continue Your Learning Path

Next: [React Lifecycle and useEffect](../react-lifecycle-and-useeffect/) — see the
[Frontend learning path](../../README.md) for the full sequence.
