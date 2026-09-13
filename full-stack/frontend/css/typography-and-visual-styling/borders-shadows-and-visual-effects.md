# Borders, Shadows, and Visual Effects

## Borders

```css
.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}
```

`border` is shorthand for `border-width`, `border-style`, and `border-color`; each side can also
be set individually (`border-top`, etc.). `border-radius` rounds corners, and can take two values
per corner for an elliptical (rather than circular) curve.

## `box-shadow`

```css
.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /*          x  y  blur  color */
}
```

`box-shadow` accepts horizontal offset, vertical offset, blur radius, (optionally) spread radius,
and a color — commonly used with a low-opacity color (via `rgba()` or a hex alpha channel) to
create a soft, subtle shadow rather than a harsh, fully opaque one. Multiple shadows can be
comma-separated to layer several effects (a soft ambient shadow plus a sharper close shadow, for
instance).

## `box-shadow` vs. `border` for Establishing Hierarchy

Both borders and shadows are common tools for visually separating a card or panel from its
background, but they read differently: a border is a hard, immediate edge; a shadow implies
elevation — the element visually "lifts" off the page. Consistent use of one or the other (or a
deliberate combination) throughout an interface, rather than mixing arbitrarily, is what makes an
interface's visual hierarchy feel coherent instead of ad hoc.

## Building Visual Hierarchy Without Clutter

Visual hierarchy — guiding a viewer's eye to what matters most — comes from a small number of
deliberately applied tools working together: size and weight (from
[typography-fundamentals.md](typography-fundamentals.md)), color and contrast (from
[color-and-backgrounds.md](color-and-backgrounds.md)), and spacing/elevation (borders, shadows,
and the box model's margin/padding). The most common failure mode isn't using too few of these
tools — it's using too many inconsistently (five different shadow styles, four different border
colors), which produces visual noise rather than clear hierarchy.

## Common Mistakes

- Using heavy, high-opacity shadows applied inconsistently across a design, producing visual
  clutter rather than a coherent sense of elevation.
- Mixing borders and shadows on similar elements without a consistent rule for when each is used,
  making the interface feel visually inconsistent.
- Reaching for more visual effects to fix a hierarchy problem that's actually a spacing or content
  problem — adding a shadow rarely fixes a layout that's already visually crowded.

## Module Summary

Across this module: font stacks with generic fallbacks, deliberate size/weight choices, and
unitless `line-height` build readable, predictable typography (see
[typography-fundamentals.md](typography-fundamentals.md)); color choices must meet real contrast
requirements, not just look acceptable by eye, and raw values should be centralized as design
tokens (see [color-and-backgrounds.md](color-and-backgrounds.md)); and borders and shadows are
complementary, distinct tools for establishing visual hierarchy — most effective when applied
consistently and sparingly rather than piled on ad hoc.
