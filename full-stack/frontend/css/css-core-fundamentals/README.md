# CSS Fundamentals

## Purpose

This module covers how CSS actually works underneath any specific property you might look up:
syntax, selectors, the cascade, specificity, inheritance, units, variables, and modern functions.
Understanding these mechanics is what lets you predict *why* a style applies (or doesn't) instead
of guessing and adding `!important` until something works.

## Learning Objectives

- Write correct CSS syntax and choose the right selector for a given target.
- Predict which rule wins when multiple rules target the same element, using the cascade and
  specificity — not trial and error.
- Explain which properties inherit by default and which don't, and why.
- Choose appropriate CSS units for a given context.
- Use CSS custom properties (variables) and modern CSS functions (`calc()`, `clamp()`, `min()`/`max()`).
- Explain what a design token is and how it relates to CSS variables.

## Prerequisites

[HTML domain](../../html/semantic-html-and-browser-rendering/) — CSS styles HTML elements, so
comfort with HTML structure is assumed throughout.

## Files in This Module

| File | Covers |
|---|---|
| [css-syntax-and-selectors.md](css-syntax-and-selectors.md) | Rule syntax and the full range of selector types |
| [specificity-and-cascade.md](specificity-and-cascade.md) | How the browser decides which conflicting rule wins |
| [inheritance-and-computed-styles.md](inheritance-and-computed-styles.md) | Which properties inherit, and how computed values work |
| [box-model.md](box-model.md) | Content, padding, border, margin, and `box-sizing` |
| [css-units.md](css-units.md) | Absolute vs. relative units, and when to use each |
| [css-variables.md](css-variables.md) | Custom properties: declaring, using, and scoping them |
| [modern-css-functions.md](modern-css-functions.md) | `calc()`, `clamp()`, `min()`, `max()` |
| [design-systems-and-design-tokens.md](design-systems-and-design-tokens.md) | How CSS variables underpin a consistent design system |

## When to Deep-Dive vs. Skim

Deep-dive [specificity-and-cascade.md](specificity-and-cascade.md) the first time you fight a style
that "should" apply but doesn't — this is the single most common source of real CSS debugging time,
and understanding it precisely replaces guesswork with a predictable answer.

## Quick Knowledge Check

<details>
<summary>Two CSS rules target the same element and set different colors. How does the browser decide which one wins?</summary>

It's not "last one written always wins" — the browser first compares specificity (how precisely
each selector targets the element), and only falls back to source order when specificity is tied.
An ID selector beats a class selector even if the class rule appears later in the file. See
[specificity-and-cascade.md](specificity-and-cascade.md).

</details>

<details>
<summary>Why does setting `color` on a parent element affect its children, but setting `border` on a parent doesn't?</summary>

`color` is one of the properties that inherits by default; `border` does not. Inheritance is
defined per-property by the CSS specification, not a universal behavior — see
[inheritance-and-computed-styles.md](inheritance-and-computed-styles.md).

</details>

## References

- MDN Web Docs, [Introduction to the CSS cascade](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction)
- MDN Web Docs, [Introduction to the CSS box model](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Box_model/Introduction)
- web.dev, [Learn CSS](https://web.dev/learn/css)

## Continue Your Learning Path

Next: [CSS Layout and Positioning](../css-layout-mastery/) — see the
[Frontend learning path](../../README.md) for the full sequence.
