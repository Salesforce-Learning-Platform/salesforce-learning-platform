# Fluid Layouts and Responsive Units

## Breakpoints Are Discrete; Real Screens Are Continuous

Media queries (see
[media-queries-and-breakpoints.md](media-queries-and-breakpoints.md)) jump between fixed states at
specific widths — a heading might be `1.5rem` right up until `768px`, then suddenly `2rem`. Fluid
techniques scale *continuously* with the viewport instead, avoiding both the abrupt jump and the
need to define a breakpoint for every possible in-between size.

## Relative Units Recap

Choosing `%`, `rem`, `vw`/`vh` deliberately (covered in
[css-units.md](../css-core-fundamentals/css-units.md)) is the foundation of fluid layout — a
container sized with `%` or a font sized with `vw` already scales with its context, without any
media query at all.

## `clamp()` for Fluid Scaling

```css
h1 {
  font-size: clamp(1.5rem, 4vw + 1rem, 3rem);
}

.container {
  width: clamp(300px, 90%, 1200px);
}
```

As introduced in
[modern-css-functions.md](../css-core-fundamentals/modern-css-functions.md), `clamp()` expresses a
value that scales fluidly between a floor and a ceiling — replacing what would otherwise require
several breakpoints to approximate a similar continuous effect.

## Fluid Grids

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
```

As introduced in [css-grid.md](../css-layout-mastery/css-grid.md), this pattern automatically
adjusts the number of columns based on available space, with no breakpoint at all — the grid
itself is fluid.

## When Breakpoints Are Still Necessary

Fluid techniques don't eliminate the need for media queries entirely — a genuine structural change
(going from a single column to a sidebar layout, or hiding a navigation element behind a hamburger
menu) is a discrete change in *structure*, not something that can scale continuously. The practical
approach combines both: fluid units/functions for continuous scaling of size and spacing, media
queries for the discrete structural changes that genuinely need them.

## Common Mistakes

- Reaching for a media query breakpoint to handle simple continuous scaling that `clamp()` could
  express in one line.
- Assuming fluid techniques remove the need for media queries entirely — structural layout changes
  are still fundamentally discrete, not continuous.
- Setting a `clamp()` minimum or maximum without actually testing the extremes — a fluid value can
  still look wrong at the very smallest or largest viewport if the bounds weren't chosen carefully.

## Next

Continue to [container-queries.md](container-queries.md) for styling based on a component's own
size, independent of the viewport entirely.
