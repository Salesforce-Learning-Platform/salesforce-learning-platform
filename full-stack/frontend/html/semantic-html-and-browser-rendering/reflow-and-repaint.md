# Reflow and Repaint

## Two Different Costs

Not every visual update costs the same. Understanding the difference between **reflow** and
**repaint** — both introduced in
[how-browsers-render-pages.md](how-browsers-render-pages.md) — is the foundation of reasoning about
rendering performance.

## Reflow (Layout)

**Reflow** recalculates the position and size of elements in the render tree. Because elements can
affect their neighbors' layout (a taller box pushes content below it down), a reflow can cascade —
changing one element may force the browser to recompute layout for a large portion of the page, or
in the worst case, the whole document.

Triggers include:

- Changing an element's dimensions, margin, padding, or border.
- Adding or removing DOM elements.
- Changing text content that affects wrapping.
- Reading certain layout properties from JavaScript (like `offsetHeight`), which can force the
  browser to complete a pending layout calculation immediately rather than deferring it — this is
  called **layout thrashing** when done repeatedly in a tight loop.

## Repaint

**Repaint** redraws pixels — updating how something looks (color, background, visibility) without
changing its position or size. It's cheaper than reflow because it doesn't require recalculating
layout for anything.

Triggers include:

- Changing `background-color`, `color`, or `visibility`.
- Any visual change that doesn't affect the box's dimensions or position.

## The Cheapest Tier: Composite-Only

Some properties — most notably `transform` and `opacity` — can often be animated using only the
compositing step, skipping both layout and paint entirely, because the browser can move or fade an
already-painted layer without recalculating anything underneath it. This is why animating
`transform: translateX(...)` is dramatically cheaper than animating `left`/`margin-left` to achieve
the same visual movement, even though both can look identical to the user.

| Change type | Reflow | Repaint | Composite |
|---|---|---|---|
| Changing `width`/`height`/`margin` | Yes | Yes | Yes |
| Changing `background-color` | No | Yes | Yes |
| Changing `transform`/`opacity` | No | No | Yes (often) |

## Practical Implications

- Batch DOM reads and writes separately rather than interleaving them, to avoid forcing repeated
  layout recalculation (layout thrashing).
- Prefer animating `transform`/`opacity` over properties that trigger reflow, for smoother
  animation.
- Adding/removing many elements one at a time in a loop can trigger a reflow per operation; batching
  the change (e.g., building a fragment off-DOM, then inserting it once) avoids this.

## Common Mistakes

- Reading a layout property (`offsetHeight`) immediately after writing a style change, repeatedly,
  in a loop — this forces synchronous layout recalculation on every iteration instead of once.
- Assuming all CSS property changes cost the same amount of rendering work.
- Optimizing prematurely without measuring — the browser's Performance panel (part of DevTools,
  see [browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md))
  shows actual reflow/repaint activity, which is far more reliable than guessing.

## Next

Continue to [responsive-images.md](responsive-images.md) to see how images specifically are served
efficiently across different screen sizes and resolutions.
