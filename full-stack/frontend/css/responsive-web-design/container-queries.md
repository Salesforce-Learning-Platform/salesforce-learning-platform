# Container Queries

## The Problem Media Queries Can't Solve

A media query only knows one thing: the viewport's size. But a genuinely reusable component (a
card, say) might be placed in a wide main content area on one page and a narrow sidebar on
another, in the exact same viewport — media queries have no way to distinguish these two
situations, because from the viewport's perspective, nothing has changed. **Container queries**
solve exactly this: styling based on the size of a component's own containing element, not the
viewport.

## Setting Up a Query Container

```css
.card-wrapper {
  container-type: inline-size;
}

@container (width > 400px) {
  .card {
    display: flex;
    align-items: center;
  }
}

.card {
  display: block; /* the default, narrow-container layout */
}
```

`container-type: inline-size` marks `.card-wrapper` as a container other elements can query
against; the `@container` rule then applies styles to `.card` based on `.card-wrapper`'s actual
width — regardless of the viewport's width.

## Named Containers

For pages with multiple nested containers, naming avoids ambiguity about which container a query
refers to:

```css
.sidebar {
  container-type: inline-size;
  container-name: sidebar;
}

@container sidebar (width > 300px) {
  .card { flex-direction: row; }
}
```

## Container Query Units

Alongside `@container`, dedicated units let you size content *relative to the container itself*
rather than the viewport:

| Unit | Relative to |
|---|---|
| `cqw` | 1% of the container's width |
| `cqh` | 1% of the container's height |
| `cqi` | 1% of the container's inline size |

```css
.card h2 {
  font-size: clamp(1rem, 5cqi, 1.5rem); /* scales with the card's own width */
}
```

## Container Queries vs. Media Queries

| | Media queries | Container queries |
|---|---|---|
| Responds to | The viewport | A specific ancestor container |
| Best for | Page-level structural changes | Reusable components used in varying contexts |
| Introduced | Long-established | More recently added to CSS — verify browser support requirements for your project |

These aren't competing tools any more than Grid and Flexbox are (see
[combining-grid-and-flex.md](../css-layout-mastery/combining-grid-and-flex.md)) — a well-built
responsive site typically uses media queries for overall page structure and container queries for
components that need to adapt to wherever they're actually placed.

## Common Mistakes

- Reaching for a media query to solve a genuinely per-component sizing problem, producing a
  component that looks right in one placement but wrong in another.
- Forgetting to declare `container-type` on the intended ancestor — `@container` rules have no
  effect without an actual query container established first.
- Assuming container query browser support matches long-established media query support without
  checking current compatibility for the project's target audience.

## Module Summary

Across this module: mobile-first development builds up complexity for larger screens rather than
stripping it down for smaller ones, producing more maintainable CSS (see
[mobile-first-development.md](mobile-first-development.md)); media queries should be driven by
where content actually breaks, not by specific device widths (see
[media-queries-and-breakpoints.md](media-queries-and-breakpoints.md)); fluid units and `clamp()`
handle continuous scaling that would otherwise need many breakpoints to approximate (see
[fluid-layouts-and-responsive-units.md](fluid-layouts-and-responsive-units.md)); and container
queries solve the specific problem media queries structurally cannot — styling a reusable component
based on its own container's size rather than the viewport.
