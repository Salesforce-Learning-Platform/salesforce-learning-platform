# Positioning

## Normal Document Flow

By default, elements lay out in **normal flow**: block-level elements (`<div>`, `<p>`) stack
vertically, one after another; inline elements (`<span>`, `<a>`) flow horizontally within their
line, wrapping as needed. Every layout technique in this module — `position`, Flexbox, Grid — is
ultimately a way of *opting out* of some or all of this default behavior for specific elements.

## `display`

`display` determines how an element generates boxes and participates in layout:

| Value | Behavior |
|---|---|
| `block` | Takes the full available width, starts on a new line |
| `inline` | Flows within the surrounding text, ignores `width`/`height` |
| `inline-block` | Flows inline but respects `width`/`height`/vertical margin like a block |
| `none` | Removed from the render tree entirely (see [how-browsers-render-pages.md](../../html/semantic-html-and-browser-rendering/how-browsers-render-pages.md)) |
| `flex` / `grid` | Establishes a flex/grid formatting context for children (covered in their own files) |

## The `position` Property

| Value | Behavior |
|---|---|
| `static` (default) | Normal flow; `top`/`right`/`bottom`/`left` have no effect |
| `relative` | Stays in normal flow, but can be visually offset via `top`/`left`/etc. *relative to where it would normally sit* — other elements are unaffected by the offset |
| `absolute` | Removed from normal flow entirely; positioned relative to the nearest **positioned** ancestor |
| `fixed` | Removed from normal flow; positioned relative to the viewport, staying in place during scroll |
| `sticky` | Behaves like `relative` until a scroll threshold is crossed, then behaves like `fixed` within its containing block |

## The Critical Rule for `absolute`

An element with `position: absolute` positions itself relative to its nearest ancestor that is
**not** `static` (i.e., has `position: relative`, `absolute`, `fixed`, or `sticky`) — not
necessarily its direct parent. If no ancestor is positioned, it falls back to the document's
initial containing block, which is almost never the intended result. This is why a very common,
deliberate pattern is adding `position: relative` to a parent purely to establish it as the
"positioning context" for an absolutely positioned child, even when the parent itself needs no
visual offset:

```css
.card {
  position: relative; /* establishes positioning context — no visual change itself */
}
.card .badge {
  position: absolute;
  top: 8px;
  right: 8px;
}
```

## `sticky` in Practice

`position: sticky` is commonly used for headers that should scroll normally until reaching the top
of the viewport, then remain fixed there — a hybrid impossible to achieve with `relative` or
`fixed` alone. It requires at least one offset property (`top`, for the usual case) to define the
threshold at which the sticky behavior engages.

## Common Mistakes

- Setting `position: absolute` and expecting it to position relative to the direct parent, without
  realizing the parent needs `position: relative` (or another non-static value) for that to work.
- Using `position: fixed` for an element intended to scroll with a specific section, when `sticky`
  is what was actually needed.
- Forgetting that `position: absolute`/`fixed` remove the element from normal flow — surrounding
  elements collapse into the space it would have occupied, which can visually break a layout that
  wasn't designed to account for it.

## Next

Continue to [stacking-context.md](stacking-context.md) to see how positioned (and other) elements
are layered on top of one another.
