# Advanced CSS and Modern Styling

## Purpose

This is the final CSS module: pseudo-classes and pseudo-elements for styling states and generated
content without extra markup, and transitions/animations for motion — plus a closing look at
choosing the right tool from everything covered across the CSS domain.

## Learning Objectives

- Use pseudo-classes to style interactive and structural states, and pseudo-elements to style
  generated content, without adding extra HTML.
- Choose between a transition and a keyframe animation based on what's actually needed.
- Respect `prefers-reduced-motion` in any animation work.
- Reason about which CSS layout/styling tool from this domain fits a given problem.

## Prerequisites

[CSS Fundamentals](../css-core-fundamentals/) and
[CSS Typography and Visual Styling](../typography-and-visual-styling/).

## Files in This Module

| File | Covers |
|---|---|
| [pseudo-classes-and-pseudo-elements.md](pseudo-classes-and-pseudo-elements.md) | `:hover`, `:focus`, `:nth-child()`, `::before`/`::after` |
| [transitions-and-animations.md](transitions-and-animations.md) | `transition`, `@keyframes`/`animation`, and respecting reduced motion |

## When to Deep-Dive vs. Skim

Deep-dive the reduced-motion section of
[transitions-and-animations.md](transitions-and-animations.md) before shipping any animation to
production — it's a small addition with a real accessibility impact for users who've requested
reduced motion at the OS level.

## Quick Knowledge Check

<details>
<summary>What's the difference between a pseudo-class and a pseudo-element?</summary>

A pseudo-class (`:hover`, `:nth-child()`) targets an element in a particular state or structural
position. A pseudo-element (`::before`, `::first-line`) targets a specific, generated part of an
element that doesn't correspond to an actual DOM node. See
[pseudo-classes-and-pseudo-elements.md](pseudo-classes-and-pseudo-elements.md).

</details>

<details>
<summary>When should you use a CSS transition instead of a keyframe animation?</summary>

A transition is for animating between two states in response to a change (like a hover) — a
simple A-to-B. A keyframe animation is for a defined sequence with multiple steps, that can run
automatically or loop, independent of a state change. See
[transitions-and-animations.md](transitions-and-animations.md).

</details>

## References

- MDN Web Docs, [Using CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Transitions/Using)
- MDN Web Docs, [Using CSS animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Animations/Using)

## Continue Your Learning Path

This is the last module in the CSS domain. Continue to
[Introduction to JavaScript](../../javascript/introduction-to-javascript/) — see the
[Frontend learning path](../../README.md) for the full sequence.
