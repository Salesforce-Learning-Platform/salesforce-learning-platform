# Components, JSX, and Props

## Purpose

This module covers the three building blocks of every React application: components (the unit of
reuse), JSX (the syntax describing what a component renders), and props (how data flows from a
parent component into a child).

## Learning Objectives

- Write a function component that returns JSX.
- Follow JSX's three syntax rules correctly.
- Embed JavaScript expressions inside JSX.
- Pass and destructure props, including default values and the `children` prop.

## Prerequisites

[Introduction to React](../introduction-to-react/).

## Files in This Module

| File | Covers |
|---|---|
| [components.md](components.md) | Function components as the fundamental unit of React UI |
| [jsx.md](jsx.md) | JSX syntax rules and embedding JavaScript expressions |
| [props.md](props.md) | Passing data into components, defaults, and `children` |
| [component-reusability.md](component-reusability.md) | Designing components genuinely reusable across contexts |

## When to Deep-Dive vs. Skim

Deep-dive [props.md](props.md)'s section on props being read-only — this single rule, once broken,
is one of the most common sources of subtle React bugs for newcomers.

## Quick Knowledge Check

<details>
<summary>Can a component modify a prop it receives?</summary>

No — props are read-only from the receiving component's perspective. A component should never
reassign or mutate a prop directly; if a value needs to change over time, that's what state
(covered in the next module) is for. See [props.md](props.md).

</details>

<details>
<summary>Why does JSX require a single root element per component (or a Fragment)?</summary>

Under the hood, JSX compiles to function calls that must return one value — a Fragment (`<>...</>`)
lets you group multiple elements without introducing an unnecessary extra wrapping DOM element.
See [jsx.md](jsx.md).

</details>

## References

- React, [Writing Markup with JSX](https://react.dev/learn/writing-markup-with-jsx)
- React, [Passing Props to a Component](https://react.dev/learn/passing-props-to-a-component)

## Continue Your Learning Path

Next: [Component Architecture and Composition](../component-architecture-and-composition/) — see
the [Frontend learning path](../../README.md) for the full sequence.
