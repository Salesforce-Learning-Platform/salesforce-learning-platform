# Operators

## Math Operators

```scss
$base-spacing: 8px;

.card {
  padding: $base-spacing * 2;   // 16px
  margin: $base-spacing + 4px;  // 12px
}
```

Sass supports `+`, `-`, `*` directly on numeric values (including ones with units, like `8px`),
letting a stylesheet express a relationship between values — "this spacing is always double the
base unit" — instead of hardcoding an already-computed number that silently drifts out of sync if
the base value ever changes.

## Division: `math.div()`, Not `/`

```scss
@use "sass:math";

$container-width: 1200px;
$columns: 12;

.column {
  width: math.div($container-width, $columns); // 100px
}
```

Sass's division story is a genuine exception worth calling out explicitly: the plain `/` operator's
division behavior is **deprecated** — it's being reserved purely as a separator character (matching
how CSS Grid's own shorthand already uses `/`, e.g. `grid-column: 1 / 3`). The current, correct way
to divide in Sass is `math.div()`, from Sass's built-in `sass:math` module (loaded with
`@use "sass:math"`), or wrapping the expression in a plain CSS `calc()`, which Sass simplifies to a
single value at compile time.

## Comparison and Logical Operators

```scss
@mixin text-color($size) {
  @if $size > 20px {
    font-size: $size;
    font-weight: bold;
  } @else {
    font-size: $size;
  }
}
```

`==`, `!=`, `<`, `>`, `<=`, `>=` compare values, and `and`/`or`/`not` combine boolean conditions —
used constantly inside `@if` statements, covered fully in
[control-directives.md](control-directives.md).

## String Operations

```scss
$name: "button";
.#{$name}-primary { color: blue; } // interpolation: .button-primary
```

`+` also works on strings, concatenating them, and **interpolation** (`#{...}`) lets a Sass
expression be inserted directly into a selector, property name, or string — necessary anywhere a
plain variable reference alone wouldn't be valid Sass/CSS syntax, such as building a dynamic
selector name.

## Common Mistakes

- Using the plain `/` operator for division in new Sass code — it's deprecated specifically for
  that purpose; `math.div()` (or a `calc()` expression) is the current, correct approach.
- Forgetting `@use "sass:math"` before calling `math.div()` — Sass's built-in modules, including
  `sass:math`, still need to be explicitly loaded before their functions are available.
- Mixing values with incompatible units in a math operation (like adding a plain number to a `px`
  value without accounting for units) and being surprised by the resulting unit in the output.

## Next

Continue to [control-directives.md](control-directives.md) to add real conditional and loop logic
to a stylesheet.
