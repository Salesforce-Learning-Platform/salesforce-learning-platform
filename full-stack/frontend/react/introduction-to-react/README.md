# Introduction to React

## Purpose

React is a JavaScript library for building user interfaces out of reusable **components**. This
module opens the React domain: what problem React actually solves, why teams choose it, and how
to set up your first project.

## Learning Objectives

- Explain what React is and the core idea (components + declarative UI) it's built around.
- Articulate the concrete problems React solves compared to manipulating the DOM directly.
- Set up a new React project with a modern build tool.
- Navigate the structure of a typical React project.

## Prerequisites

The full [JavaScript domain](../../javascript/) — React is a JavaScript library, and its patterns
(functions, destructuring, arrow functions, modules) are used constantly and assumed throughout —
and [TypeScript Essentials](../../typescript/typescript-essentials/), since most modern React
codebases are written in TypeScript.

## Files in This Module

| File | Covers |
|---|---|
| [what-is-react.md](what-is-react.md) | Components, declarative UI, and the core mental model |
| [why-react.md](why-react.md) | The concrete problems React solves compared to direct DOM manipulation |
| [setting-up-a-react-project.md](setting-up-a-react-project.md) | Creating a new project with Vite |
| [react-project-structure.md](react-project-structure.md) | What the generated files and folders actually do |

## When to Deep-Dive vs. Skim

Deep-dive [what-is-react.md](what-is-react.md) even if you've used React casually before — the
"UI as a function of state" mental model introduced there is what the rest of this entire domain
(state, hooks, re-rendering) builds on, and skipping past it tends to produce a purely
pattern-matching understanding of React rather than a working mental model.

## Quick Knowledge Check

<details>
<summary>What's the core idea React organizes an application around?</summary>

Components — self-contained, reusable pieces of UI that describe what should appear on screen
*given the current state*, rather than a sequence of imperative steps for building and updating
the DOM by hand. See [what-is-react.md](what-is-react.md).

</details>

<details>
<summary>What real problem does React solve, compared to using document.querySelector and manual DOM updates from JavaScript Events?</summary>

Manually keeping the DOM in sync with changing application state (via
[dom-manipulation](../../javascript/dom-manipulation/) and
[events](../../javascript/events/)) becomes genuinely hard to manage correctly as an interface
grows — React's declarative model (describe what the UI should look like for a given state; React
handles updating the actual DOM to match) removes an entire category of manual synchronization
bugs. See [why-react.md](why-react.md).

</details>

## References

- React, [Quick Start](https://react.dev/learn)
- Vite, [Getting Started](https://vite.dev/guide/)

## Continue Your Learning Path

Next: [Components, JSX, and Props](../components-jsx-and-props/) — see the
[Frontend learning path](../../README.md) for the full sequence.
