# React Error Handling and Debugging

## Purpose

[JavaScript Error Handling and Debugging](../../javascript/error-handling-and-debugging/) covered
`try`/`catch` and browser debugging generally. This module covers what's specific to React:
recognizable, common error messages, error boundaries (React's own mechanism for catching rendering
errors), and debugging techniques using React-specific tools. This closes out the React domain.

## Learning Objectives

- Recognize and correctly diagnose the most common React error messages.
- Use an error boundary to catch a rendering error and show a fallback UI instead of a blank,
  crashed page.
- Explain what error boundaries do *not* catch, and why.
- Use React Developer Tools to debug component state, props, and structure.

## Prerequisites

[JavaScript Error Handling and Debugging](../../javascript/error-handling-and-debugging/) and
[React Lifecycle and useEffect](../react-lifecycle-and-useeffect/).

## Files in This Module

| File | Covers |
|---|---|
| [common-react-errors.md](common-react-errors.md) | Recognizable error messages and what actually causes each |
| [react-error-boundaries.md](react-error-boundaries.md) | Catching rendering errors with a fallback UI |
| [debugging-react-applications.md](debugging-react-applications.md) | React Developer Tools, and a systematic debugging approach |

## When to Deep-Dive vs. Skim

Deep-dive [react-error-boundaries.md](react-error-boundaries.md)'s section on what error
boundaries *don't* catch — assuming an error boundary protects against every kind of failure (an
event handler throwing, an async error) is a common, consequential misunderstanding.

## Quick Knowledge Check

<details>
<summary>Does an error boundary catch an error thrown inside a button's onClick handler?</summary>

No — error boundaries only catch errors thrown during rendering (and in lifecycle methods and
constructors of the tree below them). An error inside an event handler needs ordinary
`try`/`catch`, exactly as covered in
[try-catch-finally.md](../../javascript/error-handling-and-debugging/try-catch-finally.md). See
[react-error-boundaries.md](react-error-boundaries.md).

</details>

<details>
<summary>What does "Cannot update state on an unmounted component" usually mean?</summary>

An async operation (a fetch) resolved after the component that started it was removed from the
UI, and its `.then()` callback tried to call a state setter that no longer applies to anything —
directly the race-condition/cleanup problem from
[fetching-data.md](../server-state-and-api-integration/fetching-data.md). See
[common-react-errors.md](common-react-errors.md).

</details>

## References

- React, [Catching Rendering Errors with an Error Boundary](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)

## Continue Your Learning Path

This is the last module in the React domain. Continue to
[Getting Started with Next.js](../../nextjs/getting-started-with-nextjs/) — see the
[Frontend learning path](../../README.md) for the full sequence.
