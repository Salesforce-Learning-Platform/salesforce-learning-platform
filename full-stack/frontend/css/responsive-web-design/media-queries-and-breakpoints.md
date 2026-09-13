# Media Queries and Breakpoints

## Basic Syntax

`@media` applies a block of CSS only when a specified condition about the browsing environment is
true:

```css
@media (min-width: 768px) {
  .sidebar {
    display: block;
  }
}
```

Following the mobile-first approach from
[mobile-first-development.md](mobile-first-development.md), `min-width` queries ("apply this when
the viewport is at least this wide") are generally preferred over `max-width` queries for a
project's primary breakpoint structure.

## Media Features Beyond Width

Width is the most common condition, but far from the only one:

| Feature | Tests |
|---|---|
| `min-width`/`max-width` | Viewport width |
| `orientation` | `portrait` or `landscape` |
| `prefers-color-scheme` | The user's OS-level light/dark mode preference |
| `prefers-reduced-motion` | Whether the user has requested reduced animation |
| `hover` | Whether the primary input can hover (helps distinguish touch from mouse) |

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Respecting `prefers-reduced-motion` is a genuine accessibility consideration — some users
experience discomfort or even vestibular symptoms from motion, and this query lets a site respect
that OS-level preference directly.

## Choosing Breakpoints: Content, Not Devices

The historically common approach — picking breakpoints to match specific popular device widths
(exactly 375px for one phone model, 768px for one tablet) — becomes a maintenance burden as new
devices with new dimensions constantly appear. The more durable approach: **let the content decide
the breakpoint**. Resize the browser window and add a breakpoint exactly where the current layout
starts to look cramped or broken — regardless of which device happens to have that width.

## Combining Conditions

```css
@media (min-width: 768px) and (orientation: landscape) {
  /* both conditions must be true */
}

@media (min-width: 768px), (orientation: landscape) {
  /* either condition being true is sufficient (comma = "or") */
}
```

## Common Mistakes

- Picking breakpoints from a list of specific device screen widths rather than from where the
  actual content and layout need to adapt.
- Using only `max-width` queries throughout a project, accumulating the override complexity
  discussed in [mobile-first-development.md](mobile-first-development.md).
- Ignoring `prefers-reduced-motion` and `prefers-color-scheme`, missing meaningful, low-effort
  accessibility and user-preference wins.

## Next

Continue to
[fluid-layouts-and-responsive-units.md](fluid-layouts-and-responsive-units.md) to see how modern
CSS reduces how often a breakpoint is even needed.
