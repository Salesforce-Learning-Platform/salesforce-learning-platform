# Color and Backgrounds

## Color Formats

| Format | Example | Notes |
|---|---|---|
| Named colors | `red`, `cornflowerblue` | Limited palette, but readable |
| Hex | `#1a73e8` | Most common; `#1a73e8ff` adds an alpha (transparency) channel |
| `rgb()` | `rgb(26, 115, 232)` | Same values as hex, in decimal; `rgb(26 115 232 / 0.5)` adds alpha |
| `hsl()` | `hsl(217, 89%, 51%)` | Hue/saturation/lightness — often more intuitive for adjusting a color (e.g., lightening by changing one number) |

`hsl()` is particularly convenient for generating consistent color variations (a hover state, a
lighter tint) by adjusting just the lightness value, without having to recompute an entirely new
hex code.

## Background Properties

```css
.hero {
  background-color: #f5f5f5;
  background-image: url("pattern.svg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
```

| Property | Controls |
|---|---|
| `background-color` | Solid fill color |
| `background-image` | An image or gradient |
| `background-size` | `cover` (fills the box, cropping if needed), `contain` (fits entirely within the box) |
| `background-position` | Where the image is anchored within the box |
| `background-repeat` | Whether/how the image tiles |

## Gradients

```css
.banner {
  background-image: linear-gradient(to right, #1a73e8, #34a853);
}
```

A `linear-gradient()` (or `radial-gradient()`) is itself a valid value for `background-image` — no
actual image file is needed for a smooth color transition.

## Color Contrast — Not Optional

Sufficient contrast between text and its background is a genuine accessibility requirement, not a
subjective design preference. WCAG defines minimum **contrast ratios**: at least 4.5:1 for normal
text, 3:1 for large text, to remain reliably readable for users with low vision or color vision
deficiencies.

```css
/* Insufficient contrast: light gray text on white - fails WCAG AA */
.subtle { color: #cccccc; background-color: #ffffff; }

/* Sufficient contrast */
.subtle { color: #595959; background-color: #ffffff; }
```

Contrast should be verified with a tool (like the
[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)), not judged purely by
eye — a color pairing that "looks fine" to someone with typical vision can still fail the actual
numeric requirement.

## `currentColor`

`currentColor` refers to the element's own resolved `color` value, and can be used anywhere a color
is expected — commonly for making an SVG icon or a border automatically match the surrounding
text color without duplicating the value:

```css
.icon-button {
  color: #1a73e8;
  border: 1px solid currentColor; /* border automatically matches the text color */
}
```

## Common Mistakes

- Choosing colors purely by visual preference without checking the actual contrast ratio, shipping
  text that's genuinely hard to read for a meaningful portion of users.
- Hardcoding raw color values throughout a stylesheet instead of centralizing them as design tokens
  (see
  [design-systems-and-design-tokens.md](../css-core-fundamentals/design-systems-and-design-tokens.md)),
  making a later color adjustment far more error-prone.
- Relying on color alone to convey information (an error shown only in red text with no icon or
  label) — a direct instance of the accessibility principle from
  [inclusive-design-principles.md](../../html/html-accessibility/inclusive-design-principles.md).

## Next

Continue to
[borders-shadows-and-visual-effects.md](borders-shadows-and-visual-effects.md) for the remaining
tools used to build visual hierarchy.
