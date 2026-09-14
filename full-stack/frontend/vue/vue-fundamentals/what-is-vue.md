# What Is Vue.js?

## Declarative Rendering Driven by Reactive State

Vue's core idea will sound immediately familiar from
[what-is-react.md](../../react/introduction-to-react/what-is-react.md): the UI is a declarative
function of state, and the framework handles updating the actual DOM when that state changes,
rather than you manipulating it manually via
[dom-manipulation](../../javascript/dom-manipulation/). This is the shared foundation both
frameworks are built on — what differs is *how* each one implements it, covered throughout the
rest of this module.

## "The Progressive Framework"

Vue describes itself this way deliberately: it can be adopted incrementally, from enhancing a
single element on an otherwise-static HTML page (with no build step at all) up to a full
single-page application with routing, state management, and server-side rendering — comparable to
the full spectrum this platform's own React and Next.js domains cover, but with Vue offering a
lower floor for adoption than React typically does in practice.

## Two Ways to Write a Vue Component

Vue offers two syntaxes for the same underlying capability:

- **Options API**: organizes a component as an object with distinct `data`, `methods`, and
  lifecycle-hook properties — closer in spirit to the pre-hooks class-component era of React
  (briefly referenced in
  [react-error-boundaries.md](../../react/error-handling-and-debugging/react-error-boundaries.md)),
  and considered more approachable for newcomers.
- **Composition API**: declares reactive state and logic directly as function-scoped variables,
  commonly with `<script setup>` — closer in spirit to React's hooks-based function components,
  and Vue's own documentation recommends it for building full, non-trivial applications.

This module uses the **Composition API** throughout, specifically because it maps most directly
onto the function-component-plus-hooks patterns already covered in depth in the React domain.

## Why Learn a Second Framework at All

The value here isn't "Vue instead of React" — it's recognizing which ideas are genuinely
*framework-agnostic* (declarative rendering, component composition, the need for explicit state
management) versus which are *React-specific implementation choices* (JSX, the `useState`
setter-function pattern, the rules of hooks). Seeing the same underlying problems solved
differently sharpens your understanding of *why* React works the way it does, not just *that* it
does.

## Common Mistakes

- Assuming Vue and React are fundamentally, philosophically different — the core "UI as a function
  of state" idea is genuinely shared; the syntax and specific mechanisms differ.
- Learning Vue's Options API from an older tutorial when the Composition API is the currently
  recommended approach for building full applications, per Vue's own documentation.
- Treating this module as "wasted" time away from React — the comparative understanding it builds
  is a real, transferable skill for evaluating any future framework or library.

## Next

Continue to
[template-syntax-and-reactivity.md](template-syntax-and-reactivity.md) to see Vue's actual syntax
and its different reactivity model.
