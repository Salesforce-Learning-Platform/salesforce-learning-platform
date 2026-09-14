# Styling in React

## Purpose

React itself has no opinion on how you write CSS — there are several genuinely mainstream
approaches, each with real tradeoffs. This module covers the four most common: CSS Modules,
CSS-in-JS, Tailwind, and a comparison of when each fits best. Every example in this module styles
the same realistic component — a `ProductCard` in an e-commerce product listing — so you can see
each approach applied to an identical, concrete need.

## Learning Objectives

- Use CSS Modules for locally-scoped styles with plain CSS syntax.
- Use a CSS-in-JS library (styled-components) to define styles as JavaScript, including
  prop-driven variation.
- Use Tailwind's utility classes directly in JSX.
- Choose the right approach for a given team and project context.

## Prerequisites

[CSS domain](../../css/) and [Components, JSX, and Props](../components-jsx-and-props/).

## Files in This Module

| File | Covers |
|---|---|
| [css-modules.md](css-modules.md) | Locally-scoped CSS files, imported directly into a component |
| [css-in-js.md](css-in-js.md) | Defining styled components with styled-components |
| [tailwind-with-react.md](tailwind-with-react.md) | Utility-first styling directly in JSX |
| [component-styling-strategies.md](component-styling-strategies.md) | Comparing the approaches, and choosing one for a real project |

## When to Deep-Dive vs. Skim

Read [component-styling-strategies.md](component-styling-strategies.md) even if your team has
already settled on one approach — understanding the genuine tradeoffs of the alternatives makes it
easier to work in a codebase using a different one, and to make an informed case if the current
choice stops fitting the project's needs.

## Quick Knowledge Check

<details>
<summary>Why does a CSS Modules class name like `styles.card` compile to something like `ProductCard_card__a1b2c`?</summary>

To guarantee the class name is unique across the entire application — this is what "locally
scoped" means: two components can both define a `.card` class with no risk of one accidentally
overriding the other's styles. See [css-modules.md](css-modules.md).

</details>

<details>
<summary>How does CSS-in-JS let a component's styles change based on its props, something plain CSS classes can't do directly?</summary>

The style definition is itself a JavaScript template literal, which can interpolate the
component's actual prop values directly into the resulting CSS — turning styling into a genuine
function of props, extending the "UI as a function of state" model to appearance itself. See
[css-in-js.md](css-in-js.md).

</details>

## References

- CSS Modules, [GitHub — css-modules/css-modules](https://github.com/css-modules/css-modules)
- styled-components, [The Basics](https://styled-components.com/docs/basics)
- Tailwind CSS, [Installing Tailwind CSS with Vite](https://tailwindcss.com/docs/installation/using-vite)

## Continue Your Learning Path

Next: [Advanced Forms and Validation](../advanced-forms-and-validation/) — see the
[Frontend learning path](../../README.md) for the full sequence.
