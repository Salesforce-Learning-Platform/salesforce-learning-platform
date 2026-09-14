# Color Functions

## Loading the `sass:color` Module

```scss
@use "sass:color";
```

Sass's built-in color-manipulation functions live in the `sass:color` module and must be explicitly
loaded with `@use "sass:color"` before they're available — the same explicit-loading pattern
[operators.md](operators.md) already covered for `sass:math`.

## `color.scale()` — Proportional Adjustment

```scss
$primary: #1a73e8;

.button:hover {
  background: color.scale($primary, $lightness: -15%);
}
```

`color.scale()` adjusts a color's property **proportionally**, toward its minimum or maximum —
`$lightness: -15%` moves the color 15% of the way from its current lightness toward black, rather
than subtracting a fixed amount. This proportional behavior is why it's the current recommended
approach: adjusting an already-dark color and an already-light color by the same proportional
amount produces visually consistent results in a way a fixed-amount adjustment doesn't.

## `color.adjust()` — Fixed-Amount Adjustment

```scss
color.adjust(#6b717f, $red: 15); // adds exactly 15 to the red channel
```

`color.adjust()` increases or decreases a specific color channel by a fixed amount, rather than
proportionally — the right tool when an adjustment genuinely needs to be an exact, absolute change,
not a relative one.

## `color.mix()` — Blending Two Colors

```scss
$brand-blue: #036;
$brand-teal: #d2e1dd;

.gradient-stop {
  background: color.mix($brand-blue, $brand-teal, 60%);
}
```

`color.mix()` blends two colors together, with `$weight` (here `60%`) controlling how much of the
*first* color contributes to the result — useful for generating a consistent set of intermediate
tones between two brand colors, rather than picking each one by eye.

## `lighten()`/`darken()` Are Deprecated — Use `color.scale()` Instead

```scss
// AVOID — deprecated; adjusts lightness by a fixed, not proportional, amount
$hover-color: darken($primary, 15%);

// PREFER — the current, recommended approach
$hover-color: color.scale($primary, $lightness: -15%);
```

The older global `lighten()`/`darken()` functions are no longer recommended, specifically because a
*fixed* lightness adjustment often doesn't produce the visually intended effect consistently across
different starting colors. `color.scale()` is the direct, current replacement for both.

## Common Mistakes

- Using the older `lighten()`/`darken()` functions in new code instead of `color.scale()` — they
  still technically work, but produce less visually consistent results and are the outdated
  approach.
- Forgetting `@use "sass:color"` before calling any `color.*` function — like `sass:math`, Sass's
  built-in modules must be explicitly loaded.
- Confusing `color.scale()`'s proportional adjustment with `color.adjust()`'s fixed-amount
  adjustment — they solve genuinely different problems and aren't interchangeable.

## Module Summary

Across this module: **Sass** is a preprocessor that compiles to plain CSS, with SCSS as its
CSS-compatible syntax (see [what-is-sass.md](what-is-sass.md) and
[setting-up-scss.md](setting-up-scss.md)); **variables** (`$x`) are a compile-time-only tool,
genuinely distinct from CSS custom properties, which stay alive at runtime (see
[variables.md](variables.md)); **nesting** and the parent selector (`&`) organize related rules
visually without over-specifying selectors (see [nesting.md](nesting.md)); **partials** and `@use`
split a growing stylesheet into namespaced, collision-safe files (see
[partials-and-imports.md](partials-and-imports.md)); **mixins** emit reusable style rules, with
`@content` accepting a caller-supplied block, while **functions** compute and return a single value
with no side effects (see [mixins.md](mixins.md) and [functions.md](functions.md)); **`@extend`**
shares styles by combining selectors rather than duplicating declarations, with placeholder
selectors (`%name`) as the safer default (see
[inheritance-and-extends.md](inheritance-and-extends.md)); **operators**, including the modern
`math.div()` replacing deprecated `/` division, and **control directives**
(`@if`/`@each`/`@for`/`@while`) add real computation and iteration to a stylesheet (see
[operators.md](operators.md) and [control-directives.md](control-directives.md)); and Sass's
**built-in color functions**, led by `color.scale()`, replace the older, less consistent
`lighten()`/`darken()` functions.
