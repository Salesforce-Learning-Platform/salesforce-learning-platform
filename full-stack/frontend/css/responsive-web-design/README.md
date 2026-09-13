# Responsive Web Design

## Purpose

A page has to work on a phone, a tablet, and an ultrawide monitor — often within the same session,
as a user resizes a window or rotates a device. This module covers the principles and tools for
building layouts that adapt, rather than building one fixed design and hoping it degrades
gracefully.

## Learning Objectives

- Explain the mobile-first approach and why it produces more robust CSS than designing desktop-first.
- Write effective media queries and choose breakpoints based on content, not specific devices.
- Use responsive units (covered in [css-units.md](../css-core-fundamentals/css-units.md)) and
  modern functions (`clamp()`) to reduce reliance on fixed breakpoints entirely.
- Use container queries when a component's own size — not the viewport's — should drive its
  layout.

## Prerequisites

[CSS Fundamentals](../css-core-fundamentals/) and [CSS Layout Mastery](../css-layout-mastery/).

## Files in This Module

| File | Covers |
|---|---|
| [mobile-first-development.md](mobile-first-development.md) | Why mobile-first, and how it changes how you write CSS |
| [media-queries-and-breakpoints.md](media-queries-and-breakpoints.md) | `@media` syntax, choosing breakpoints, and common features beyond width |
| [fluid-layouts-and-responsive-units.md](fluid-layouts-and-responsive-units.md) | Building layouts that scale continuously instead of jumping between fixed breakpoints |
| [container-queries.md](container-queries.md) | Styling a component based on its own container's size, not the viewport |

## When to Deep-Dive vs. Skim

Deep-dive [container-queries.md](container-queries.md) the first time you build a genuinely
reusable component (a card that might appear in a wide main area or a narrow sidebar) — this is
exactly the problem media queries can't solve, since they only know about the viewport.

## Quick Knowledge Check

<details>
<summary>Why start with mobile styles and use media queries to add complexity for larger screens, rather than the reverse?</summary>

Mobile-first CSS starts from the simplest, most constrained layout and progressively enhances it —
this tends to produce simpler, more robust styles than starting complex and trying to strip
features away for small screens, which is a harder direction to work in reliably. See
[mobile-first-development.md](mobile-first-development.md).

</details>

<details>
<summary>A card component needs to look different when placed in a narrow sidebar vs. a wide main content area — on the same page, same viewport. Can a media query solve this?</summary>

No — a media query only knows about the viewport, not where a component happens to sit within the
page. This is precisely what container queries solve: styling based on the component's own
container size. See [container-queries.md](container-queries.md).

</details>

## References

- MDN Web Docs, [Using media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Using)
- MDN Web Docs, [Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries)

## Continue Your Learning Path

Next: [CSS Typography and Visual Styling](../typography-and-visual-styling/) — see the
[Frontend learning path](../../README.md) for the full sequence.
