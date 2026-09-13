# Component Architecture and Composition

## Purpose

[Component Reusability](../components-jsx-and-props/component-reusability.md) introduced the
signals for when to extract a component. This module goes further: concrete composition patterns
that avoid over-configured, hard-to-maintain components, a deep dive on the `children` prop, and
the controlled-vs-uncontrolled distinction for form inputs.

## Learning Objectives

- Use composition (not just configuration via props) to build flexible component hierarchies.
- Use the `children` prop for genuinely generic wrapper components.
- Explain the difference between a controlled and an uncontrolled component, and when to use each.
- Recognize and avoid "prop drilling" using composition.

## Prerequisites

[Components, JSX, and Props](../components-jsx-and-props/).

## Files in This Module

| File | Covers |
|---|---|
| [component-composition.md](component-composition.md) | Composition patterns, and avoiding prop drilling |
| [children-prop.md](children-prop.md) | `children` in depth, including passing multiple named slots |
| [controlled-and-uncontrolled-components.md](controlled-and-uncontrolled-components.md) | Who owns a form input's value — React state or the DOM |
| [reusable-component-design.md](reusable-component-design.md) | Concrete patterns for designing a component's prop interface |

## When to Deep-Dive vs. Skim

Deep-dive [controlled-and-uncontrolled-components.md](controlled-and-uncontrolled-components.md) —
this distinction is directly responsible for a very common category of React form bugs (an input
that won't update, or a warning about switching between controlled/uncontrolled), and is assumed
knowledge once you reach the dedicated Advanced Forms module later in this domain.

## Quick Knowledge Check

<details>
<summary>What problem does composition (passing components as children/props) solve that configuration (more and more boolean props) doesn't?</summary>

Configuration requires anticipating every future variation upfront, growing a component's prop
list indefinitely; composition lets the parent decide what actually goes inside, keeping the
wrapper component simple regardless of how varied its contents become. See
[component-composition.md](component-composition.md).

</details>

<details>
<summary>In React, is an `<input>`'s displayed value ever the DOM's own responsibility?</summary>

Yes — an "uncontrolled" input lets the DOM manage its own value internally, read only when needed
(e.g., via a ref). A "controlled" input instead has its value fully driven by React state on every
keystroke. Mixing the two approaches on the same input is what triggers React's
controlled/uncontrolled warning. See
[controlled-and-uncontrolled-components.md](controlled-and-uncontrolled-components.md).

</details>

## References

- React, [Passing Props to a Component](https://react.dev/learn/passing-props-to-a-component)
- React, [Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)

## Continue Your Learning Path

Next: [State and Re-rendering Logic](../state-and-rerendering-logic/) — see the
[Frontend learning path](../../README.md) for the full sequence.
