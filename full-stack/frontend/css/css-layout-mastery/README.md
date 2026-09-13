# CSS Layout Mastery

## Purpose

This folder covers CSS layout across three OPS modules that ship incrementally and build on each
other: normal flow and positioning (OPS-055), Flexbox (OPS-056), and Grid (OPS-057). They share a
folder because they're one continuous topic — modern CSS layout — but are scoped as separate
learning modules so each can be absorbed on its own.

## Files in This Module

| File | Covers | Module |
|---|---|---|
| [positioning.md](positioning.md) | Normal document flow, `display`, and the `position` property | CSS Layout and Positioning |
| [stacking-context.md](stacking-context.md) | `z-index` and how stacking contexts actually work | CSS Layout and Positioning |
| [common-layout-patterns.md](common-layout-patterns.md) | Overflow handling and classic layout problems solved without Flexbox/Grid | CSS Layout and Positioning |
| [flexbox-deep-dive.md](flexbox-deep-dive.md) | Flex containers, items, alignment, direction, wrapping | CSS Flexbox |
| [css-grid.md](css-grid.md) | Grid containers, tracks, areas, alignment | CSS Grid |
| [combining-grid-and-flex.md](combining-grid-and-flex.md) | When to reach for Grid vs. Flexbox, and using both together | CSS Grid |

## Prerequisites

[CSS Fundamentals](../css-core-fundamentals/), especially
[box-model.md](../css-core-fundamentals/box-model.md).

## When to Deep-Dive vs. Skim

Read [positioning.md](positioning.md) and [stacking-context.md](stacking-context.md) closely even
if you already know Flexbox/Grid well — `position` and `z-index` are used constantly *alongside*
modern layout methods (a modal, a tooltip, a sticky header) and are a common source of confusing,
hard-to-debug overlap bugs when misunderstood.

## Quick Knowledge Check

<details>
<summary>An absolutely positioned element isn't positioning relative to where you expected. What's the most likely cause?</summary>

`position: absolute` positions relative to the nearest *positioned* ancestor (any ancestor with a
`position` other than `static`) — if no ancestor is positioned, it falls back to the initial
containing block, which is usually not what was intended. See [positioning.md](positioning.md).

</details>

<details>
<summary>Two elements have `z-index: 999` and `z-index: 1` respectively, but the one with 999 still renders behind the other. How is that possible?</summary>

`z-index` values only compare within the same stacking context — if the two elements belong to
different stacking contexts (each created by a positioned ancestor, for example), their z-index
values are compared to their siblings within their own context, not directly against each other.
See [stacking-context.md](stacking-context.md).

</details>

## References

- MDN Web Docs, [`position`](https://developer.mozilla.org/en-US/docs/Web/CSS/position)
- MDN Web Docs, [Stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context)

## Continue Your Learning Path

Next: [Responsive Web Design](../responsive-web-design/) — see the
[Frontend learning path](../../README.md) for the full sequence.
