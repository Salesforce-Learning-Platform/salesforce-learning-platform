# Flexbox Deep Dive

## Purpose

Flexbox is a **one-dimensional** layout model — it distributes space along a single axis at a
time (either a row or a column). It solves problems that were historically awkward with normal
flow and floats (see [common-layout-patterns.md](common-layout-patterns.md)): equal-height
columns, centering, and flexible space distribution.

## Prerequisites

[Positioning](positioning.md) and [CSS Fundamentals](../css-core-fundamentals/), particularly the
[box model](../css-core-fundamentals/box-model.md).

## The Two Axes

Flexbox thinks in terms of a **main axis** and a **cross axis**, not simply "horizontal" and
"vertical" — the main axis direction is set by `flex-direction`, and the cross axis is always
perpendicular to it.

```text
flex-direction: row (default)          flex-direction: column
┌─────────────────────────────┐        ┌───────────┐
│ [1] [2] [3]   ──▶ main axis  │        │   [1]     │
│  │                            │        │   [2]     │  │
│  ▼ cross axis                 │        │   [3]     │  ▼ cross axis
└─────────────────────────────┘        │ ──▶ main   │
                                         └───────────┘
```

## The Flex Container

Applying `display: flex` to an element makes it a **flex container**; its direct children become
**flex items**, automatically arranged along the main axis:

```css
.container {
  display: flex;
}
```

## Container Properties

| Property | Controls |
|---|---|
| `flex-direction` | Main axis direction: `row` (default), `row-reverse`, `column`, `column-reverse` |
| `flex-wrap` | Whether items wrap to new lines when they don't fit: `nowrap` (default), `wrap` |
| `justify-content` | Alignment of items along the **main** axis: `flex-start`, `center`, `space-between`, `space-around` |
| `align-items` | Alignment of items along the **cross** axis: `stretch` (default), `center`, `flex-start`, `flex-end` |
| `gap` | Spacing between items, without needing margin hacks on individual items |

```css
.container {
  display: flex;
  justify-content: space-between; /* spreads items along the main axis */
  align-items: center;             /* centers items on the cross axis */
  gap: 16px;
}
```

## Item Properties

| Property | Controls |
|---|---|
| `flex-grow` | How much an item expands to fill available extra space, relative to siblings |
| `flex-shrink` | How much an item shrinks when there isn't enough space |
| `flex-basis` | The item's starting size before growing/shrinking is applied |
| `flex` | Shorthand for `grow shrink basis` — `flex: 1` is extremely common shorthand for "grow to fill available space equally" |
| `align-self` | Overrides the container's `align-items` for one specific item |
| `order` | Changes visual order without changing DOM order |

```css
.sidebar { flex: 0 0 250px; } /* never grow, never shrink, fixed 250px basis */
.main    { flex: 1; }          /* grow to fill all remaining space */
```

This two-line pattern — a fixed-width sidebar plus a `flex: 1` main content area — is one of the
most common real-world Flexbox layouts, solving a problem that was genuinely awkward with floats
alone.

## `order` Is Visual Only

`order` changes the *visual* rendering order of flex items without touching the underlying DOM
order — which means it has real accessibility implications: keyboard tab order and screen reader
reading order follow DOM order, not `order`. Reordering visually with `order` while leaving DOM
order mismatched creates exactly the kind of visual/keyboard-order disconnect warned about in
[links-and-navigation-flow.md](../../html/semantic-html-and-browser-rendering/links-and-navigation-flow.md).

## Common Mistakes

- Confusing `justify-content` (main axis) with `align-items` (cross axis) — this swaps depending
  on `flex-direction`, which is a frequent source of "why isn't this centering" confusion.
- Using `order` to fix a visual arrangement problem that should have been fixed in the actual DOM
  order, creating a keyboard-navigation mismatch.
- Forgetting `flex-wrap: wrap` and being surprised that items shrink to fit rather than wrapping to
  a new line — `nowrap` is the default.
- Reaching for Flexbox for genuinely two-dimensional layouts (rows *and* columns that need to align
  together) — that's what Grid, covered next, is actually designed for.

## Module Note

This deep dive is the complete Flexbox module — see
[css-grid.md](css-grid.md) next for the two-dimensional layout model, and
[combining-grid-and-flex.md](combining-grid-and-flex.md) for guidance on choosing between the two
or using them together.

## References

- MDN Web Docs, [Basic concepts of flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Basic_concepts)
- [Flexbox Froggy](https://flexboxfroggy.com/) — a free, interactive game for practicing flexbox properties hands-on

## Next

Continue to [css-grid.md](css-grid.md).
