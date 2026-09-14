# Mixins

## Defining and Including a Mixin

```scss
@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  @include flex-center;
}
```

```css
.card { display: flex; align-items: center; justify-content: center; }
```

A **mixin** packages a reusable block of style rules under a name — `@mixin` defines it, and
`@include` inserts its rules wherever it's used, with the compiled output containing the mixin's
actual declarations copied in, not a reference to anything.

## Mixins With Arguments

```scss
@mixin button-variant($bg-color, $text-color: white) {
  background: $bg-color;
  color: $text-color;
  padding: 8px 16px;
}

.button-primary { @include button-variant(#1a73e8); }
.button-danger { @include button-variant(#d93025, black); }
```

A mixin can accept arguments, including ones with a default value (`$text-color: white`) — making
it optional at the call site. This is what actually makes a mixin *reusable* rather than just a
fixed block of repeated declarations: `button-variant` produces genuinely different output for
each different color passed in.

## `@content` — Accepting a Block of Styles

```scss
@mixin responsive($breakpoint) {
  @media (min-width: $breakpoint) {
    @content;
  }
}

.sidebar {
  width: 100%;

  @include responsive(768px) {
    width: 250px;
  }
}
```

```css
.sidebar { width: 100%; }
@media (min-width: 768px) {
  .sidebar { width: 250px; }
}
```

`@content` is where a mixin becomes genuinely powerful: it lets the code *calling* the mixin pass
in its own block of styles, which get inserted exactly where `@content` appears inside the mixin's
definition. Here, `responsive` wraps whatever styles are passed to it in a media query — directly
comparable to breakpoint planning from the
[Responsive Design module](../responsive-web-design/), but expressed as a single, reusable named
mixin instead of repeating the same `@media` query declaration throughout the stylesheet.

## A Realistic, Combined Example

```scss
@mixin card($padding: 16px, $radius: 8px) {
  padding: $padding;
  border-radius: $radius;
  border: 1px solid #e0e0e0;

  @content;
}

.product-card {
  @include card {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
}
```

This combines arguments with defaults and a `@content` block in one mixin: `card` provides a
consistent base (padding, border radius, border), while letting each specific usage layer on its
own extra styles (a shadow, here) without needing to redefine the shared base every time.

## Common Mistakes

- Writing a mixin for something that's really a single, fixed value with no variation — a plain
  Sass variable is simpler and clearer for that case; mixins exist specifically for reusable
  *rule sets* or logic, not single values.
- Forgetting `@content` when a mixin genuinely needs to accept custom styles from its caller,
  forcing every possible variation to be hardcoded as separate mixin arguments instead.
- Overusing mixins for things a CSS class alone would already handle cleanly — a mixin's real value
  is parameterization (arguments, `@content`); a mixin with no arguments and no `@content` is
  usually just as clear as a plain reusable class.

## Next

Continue to [functions.md](functions.md) to compute and return values, rather than emit style
rules directly.
