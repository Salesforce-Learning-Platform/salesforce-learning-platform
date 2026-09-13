# Modern CSS Functions

## `calc()`

`calc()` lets you compute a value from a mix of units — something CSS couldn't do natively before
it existed:

```css
.sidebar {
  width: calc(100% - 250px); /* full width minus a fixed sidebar */
}

.spaced {
  margin-top: calc(var(--spacing-unit) * 3); /* combines with a custom property */
}
```

This solves a real, common problem: laying out an element that should fill remaining space after
subtracting a fixed amount — impossible to express with a single unit type alone.

## `min()` and `max()`

`min()` picks the smallest of its arguments; `max()` picks the largest — evaluated live, per
element, not just once:

```css
.container {
  width: min(90%, 800px); /* never wider than 800px, but shrinks on small screens */
  padding: max(16px, 2vw); /* never less than 16px, but grows on wide viewports */
}
```

`min(90%, 800px)` reads naturally: "90% of the parent, but capped at 800px" — exactly the kind of
responsive constraint that previously required a media query to express.

## `clamp()`

`clamp(minimum, preferred, maximum)` combines both ideas into one: a value that scales fluidly
between a floor and a ceiling:

```css
h1 {
  font-size: clamp(1.5rem, 4vw + 1rem, 3rem);
}
```

This heading's font size scales smoothly with viewport width, but never shrinks below `1.5rem` or
grows past `3rem` — a single declaration replacing what would otherwise need several media-query
breakpoints to approximate.

## Common Mistakes

- Forgetting that `calc()` requires whitespace around `+` and `-` operators (`calc(100% - 10px)`,
  not `calc(100%-10px)`) — this is a real, easy-to-hit syntax requirement, not a stylistic
  preference.
- Reaching for a media query to achieve fluid scaling that `clamp()` could express in one line more
  smoothly (media queries jump between fixed values at breakpoints; `clamp()` scales continuously).
- Using `min()`/`max()`/`clamp()` with mismatched unit types that don't make sense to compare in
  context, producing a confusing or unintended result.

## Next

Continue to
[design-systems-and-design-tokens.md](design-systems-and-design-tokens.md) to see how custom
properties and these functions combine into a maintainable design system.
