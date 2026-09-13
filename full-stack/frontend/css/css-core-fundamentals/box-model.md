# The Box Model

## Every Element Is a Box

CSS represents every rendered element as a rectangular box, made of four concentric areas —
this is the **box model**, and it's what actually determines an element's final size and how much
space it occupies on the page.

```text
┌─────────────────────────────────────┐
│               margin                 │
│   ┌───────────────────────────────┐ │
│   │            border              │ │
│   │   ┌───────────────────────┐   │ │
│   │   │        padding         │   │ │
│   │   │   ┌───────────────┐   │   │ │
│   │   │   │    content     │   │   │ │
│   │   │   └───────────────┘   │   │ │
│   │   └───────────────────────┘   │ │
│   └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

| Area | Controlled by |
|---|---|
| Content | `width`, `height` |
| Padding | `padding` (and `padding-top`/`right`/`bottom`/`left`) |
| Border | `border` (and its sub-properties) |
| Margin | `margin` (and its sub-properties) |

Padding sits *inside* the border and is part of the element's own background; margin sits
*outside* the border and is always transparent space separating the element from its neighbors.

## `box-sizing`: The Property That Changes Everything

By default (`box-sizing: content-box`), `width`/`height` apply only to the **content** area —
padding and border are added on top, making the element's actual rendered size larger than the
`width` you set. `box-sizing: border-box` changes this so `width`/`height` include padding and
border, making the element's total size exactly match what you specified:

```css
/* content-box (default): a 200px-wide box with 20px padding renders at 240px total */
.content-box { box-sizing: content-box; width: 200px; padding: 20px; }

/* border-box: a 200px-wide box with 20px padding renders at exactly 200px total */
.border-box { box-sizing: border-box; width: 200px; padding: 20px; }
```

Because `border-box` sizing is far more predictable when combining fixed widths with padding, it's
extremely common to see it applied globally as a reset:

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

## Margin Collapsing

Vertical margins between two adjacent block-level elements can **collapse** — rather than adding
together, the browser uses only the larger of the two margins as the actual gap between them. This
is a real, specification-defined behavior (not a bug), and one of the more surprising box-model
behaviors for newcomers, since horizontal margins never collapse the same way.

## Common Mistakes

- Setting a fixed `width` with `content-box` sizing and being surprised the element renders wider
  than expected once padding and border are added.
- Not applying a `border-box` reset project-wide, leading to inconsistent, hard-to-predict sizing
  across components with different padding values.
- Expecting two stacked elements' margins to add together, and being confused when the visible gap
  is smaller than the sum due to margin collapsing.

## Next

Continue to [css-units.md](css-units.md) to see how the actual numbers in these box-model
properties should be chosen.
