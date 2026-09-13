# Typography Fundamentals

## Font Families and Font Stacks

```css
body {
  font-family: "Inter", Arial, sans-serif;
}
```

A **font stack** lists fonts in order of preference. The browser tries each in turn until it finds
one actually available, falling back to a **generic family** (`sans-serif`, `serif`, `monospace`)
as a guaranteed last resort. Without a generic fallback, an unavailable custom font can fall back
to an unpredictable browser default instead of a deliberately chosen one.

## Font Size, Weight, and Style

| Property | Controls |
|---|---|
| `font-size` | Text size — see [css-units.md](../css-core-fundamentals/css-units.md) for `rem` vs. `em` guidance |
| `font-weight` | Boldness — numeric (`400` normal, `700` bold) or keywords (`normal`, `bold`) |
| `font-style` | `normal`, `italic`, `oblique` |
| `text-transform` | `uppercase`, `lowercase`, `capitalize` — transforms *display* only, not the underlying text content |

## Line Height and Spacing

```css
p {
  line-height: 1.5;
  letter-spacing: 0.01em;
}
```

`line-height` set as a **unitless number** (like `1.5`) is generally preferred over a fixed
`px`/`rem` value — a unitless value scales proportionally with that element's own font size,
including for nested elements with different sizes, while a fixed value doesn't adjust
automatically. Comfortable body text typically uses a `line-height` between about 1.4 and 1.6;
tighter values suit large display headings better.

## The `font` Shorthand

```css
h1 {
  font: italic 700 2rem/1.2 "Inter", sans-serif;
  /*    style   weight size/line-height family */
}
```

The shorthand is compact but strict about property order — getting it wrong silently produces
unexpected results rather than an error, so many teams prefer the explicit longhand properties for
clarity, reserving the shorthand for cases where brevity is clearly worth the trade-off.

## Text Alignment and Decoration

| Property | Controls |
|---|---|
| `text-align` | Horizontal alignment: `left`, `center`, `right`, `justify` |
| `text-decoration` | Underline, strikethrough, etc. |

`text-align: justify` (stretching text to fill the full line width on both edges) can create
uneven word spacing, especially in narrow columns — it's used far less often on the web than in
print for this reason.

## Common Mistakes

- Specifying a custom font with no generic fallback at the end of the stack, leaving font choice
  to an unpredictable default if every listed font fails to load.
- Using `text-transform: uppercase` for styling while assuming it also changes what a screen reader
  announces — screen readers generally still read the original text content, not the visually
  transformed version.
- Setting a fixed `line-height` in `px` globally, which doesn't scale correctly when nested
  elements use different font sizes.

## Next

Continue to [color-and-backgrounds.md](color-and-backgrounds.md) for color formats and ensuring
sufficient contrast.
