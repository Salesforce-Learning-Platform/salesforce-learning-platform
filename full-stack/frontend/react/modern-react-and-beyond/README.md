# ⚛️ Modern React — React 19 & Beyond

## Purpose

Every prior React module — from [Introduction to React](../introduction-to-react/) through
[Performance Optimization](../performance-optimization-in-react/) — taught React's established,
stable patterns. This module covers what's genuinely new in **React 19**: Actions for form
handling, the `use()` API, optimistic UI updates, and the React Compiler — each one changing a
pattern you already know into a simpler, more direct version of itself.

## 🎯 Learning Objectives

- Use `<Suspense>` for declarative, component-level loading states.
- Explain Server Components vs. Client Components as React's newest architectural model.
- Handle form submissions the React 19 way, using Actions.
- Use `useActionState` and `useFormStatus` to manage form state without manual boilerplate.
- Build optimistic UI with `useOptimistic`.
- Use the `use()` hook to read a promise or context value directly during render.
- Explain what the React Compiler automates, and why it changes how memoization is taught.

## 📋 Prerequisites

- [React Hooks](../react-hooks/) and
  [State and Re-rendering Logic](../state-and-rerendering-logic/) — this module assumes solid
  footing with `useState`, `useEffect`, and the existing hooks model, and shows how React 19
  extends it.
- [Performance Optimization in React](../performance-optimization-in-react/) — specifically
  `useMemo`/`useCallback`/`React.memo`, since the React Compiler directly automates what that
  module teaches to do manually.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [suspense-deep-dive.md](suspense-deep-dive.md) | `<Suspense>`, fallbacks, and nested boundaries for progressive loading |
| [server-components-vs-client-components.md](server-components-vs-client-components.md) | React's newest mental model — building on, not repeating, the Next.js coverage |
| [actions-and-form-handling.md](actions-and-form-handling.md) | Handling form submissions the React 19 way, with Actions |
| [useactionstate-and-useformstatus.md](useactionstate-and-useformstatus.md) | Form state without manual `useState`/`useTransition` boilerplate |
| [optimistic-ui-with-useoptimistic.md](optimistic-ui-with-useoptimistic.md) | Instant-feeling interfaces with `useOptimistic` |
| [the-use-hook.md](the-use-hook.md) | Reading a promise or context directly during render with `use()` |
| [react-compiler-introduction.md](react-compiler-introduction.md) | Automatic memoization, and where React is heading |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [actions-and-form-handling.md](actions-and-form-handling.md) — Actions are the single
change in React 19 most likely to replace a pattern you already use constantly (manual form
`useState` plus a submit handler), and understanding exactly what they automate is worth getting
precisely right.

## ✅ Quick Knowledge Check

<details>
<summary>Does the React Compiler replace useState or useEffect?</summary>

No — it specifically automates **memoization** (what `useMemo`, `useCallback`, and `React.memo`
already do manually), not state management or side effects. `useState` and `useEffect` remain
exactly as they are. See [react-compiler-introduction.md](react-compiler-introduction.md).

</details>

<details>
<summary>Can useOptimistic be used outside of a form submission?</summary>

Its most common use is paired with a form Action, but the underlying idea — showing an assumed,
"optimistic" result immediately while a real async update is still in flight — applies to any
async update triggered from user interaction, not only forms. See
[optimistic-ui-with-useoptimistic.md](optimistic-ui-with-useoptimistic.md).

</details>

## 📚 References

- React, [React v19](https://react.dev/blog/2024/12/05/react-19)
- React, [`<Suspense>`](https://react.dev/reference/react/Suspense)
- React, [React Compiler](https://react.dev/learn/react-compiler)

## ➡️ Continue Your Learning Path

See the [Frontend learning path](../../README.md) for the remaining modules and what comes next.
