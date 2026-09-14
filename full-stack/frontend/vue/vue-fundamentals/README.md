# Vue.js Fundamentals

## Purpose

Having just finished the [React domain](../../react/) and [Next.js domain](../../nextjs/), this
module introduces **Vue.js** — a second major component framework, not as a replacement for what
you've learned, but as an example of how the same underlying problems (reusable components,
reactive UI updates) can be solved with genuinely different design choices. Every comparison in
this module is made directly against React, since that's the framework you already know.

## Learning Objectives

- Explain Vue's core idea — declarative rendering driven by reactive state — and how it compares to
  React's model.
- Write Vue template syntax: interpolation, directives, and event binding.
- Use `ref()`/`reactive()` for reactive state, and explain how Vue's reactivity differs from
  React's `useState`.
- Build components with props and emitted events using Single-File Components.

## Prerequisites

The full [React domain](../../react/) — this module is written assuming that context and compares
directly against it throughout.

## Files in This Module

| File | Covers |
|---|---|
| [what-is-vue.md](what-is-vue.md) | Vue's core idea, and the Options API vs. Composition API choice |
| [template-syntax-and-reactivity.md](template-syntax-and-reactivity.md) | Template syntax, directives, and `ref()`/`reactive()` |
| [components-and-props.md](components-and-props.md) | Single-File Components, props, and emitting events |
| [vue-vs-react.md](vue-vs-react.md) | A direct, concept-by-concept comparison |

## When to Deep-Dive vs. Skim

Deep-dive [template-syntax-and-reactivity.md](template-syntax-and-reactivity.md) — Vue's
reactivity model is genuinely, not just syntactically, different from React's `useState` (covered
in [usestate.md](../../react/state-and-rerendering-logic/usestate.md)), and understanding that
difference precisely is more valuable than memorizing template syntax alone.

## Quick Knowledge Check

<details>
<summary>In React, calling a state setter triggers a re-render. What's the equivalent trigger in Vue?</summary>

Mutating a `ref`'s `.value` (or a `reactive()` object's property) directly — Vue's reactivity
system tracks which parts of the template depend on that value and updates automatically, without
a separate "setter function" the way `useState` requires. See
[template-syntax-and-reactivity.md](template-syntax-and-reactivity.md).

</details>

<details>
<summary>Does Vue use JSX like React does?</summary>

Not by default — Vue's standard approach uses HTML-based templates with special directives
(`v-if`, `v-for`, `v-bind`) rather than JavaScript expressions embedded in `{}` the way JSX works.
Vue does support a JSX-like syntax as an option, but templates are the idiomatic default. See
[template-syntax-and-reactivity.md](template-syntax-and-reactivity.md).

</details>

## References

- Vue.js, [Introduction](https://vuejs.org/guide/introduction.html)
- Vue.js, [Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)

## Continue Your Learning Path

This is the only module in the Vue.js domain. See the
[Frontend learning path](../../README.md) for what comes next.
