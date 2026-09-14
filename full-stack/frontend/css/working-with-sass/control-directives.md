# Control Directives

## `@if` / `@else if` / `@else`

```scss
@mixin button-size($size) {
  @if $size == small {
    padding: 4px 8px;
  } @else if $size == large {
    padding: 12px 24px;
  } @else {
    padding: 8px 16px; // the default/medium case
  }
}

.button-sm { @include button-size(small); }
.button-lg { @include button-size(large); }
```

`@if` controls whether a block of Sass runs at all, based on a condition — using the comparison
operators from [operators.md](operators.md). This is a genuinely programmatic capability plain CSS
has no equivalent for; a mixin like `button-size` behaves differently depending on its actual
argument, rather than always producing identical output.

## `@each` — Iterating Over a List or a Map

```scss
$sizes: small, medium, large;

@each $size in $sizes {
  .button-#{$size} {
    @if $size == large {
      font-size: 18px;
    } @else {
      font-size: 14px;
    }
  }
}
```

```scss
$theme-colors: (
  "primary": #1a73e8,
  "danger": #d93025,
  "success": #34a853,
);

@each $name, $color in $theme-colors {
  .text-#{$name} { color: $color; }
}
```

`@each` runs its block once per item in a list, or once per key-value pair in a **map** (Sass's
associative-array-like structure, written `(key: value, ...)`) — this second form is the practical
way to generate a whole family of related utility classes (`.text-primary`, `.text-danger`,
`.text-success`) from one centralized data structure, directly echoing the same
[design-tokens](../css-core-fundamentals/design-systems-and-design-tokens.md) idea: define the
values once, generate every usage from that single source.

## `@for` — a Fixed Number of Iterations

```scss
@for $i from 1 through 12 {
  .col-#{$i} {
    width: math.div(100%, 12) * $i;
  }
}
```

`@for` runs its block a specific number of times, with `$i` taking each value in the range in
turn. `through` is **inclusive** of the end value (`1 through 12` runs 12 times, ending at 12);
`to` is **exclusive** (`1 to 12` runs 11 times, stopping just before 12) — a distinction easy to
get wrong and worth double-checking whenever an off-by-one result appears.

## `@while` — Looping Until a Condition Is False

```scss
$i: 1;
@while $i <= 3 {
  .delay-#{$i} { transition-delay: $i * 100ms; }
  $i: $i + 1; // MUST update the condition variable, or this loops forever
}
```

`@while` repeats its block for as long as a condition stays true — genuinely necessary only in the
rarer case where the number of iterations isn't known upfront the way `@for`'s range is; `@each`
and `@for` cover the vast majority of real, practical looping needs in a stylesheet.

## Common Mistakes

- Confusing `through` (inclusive) and `to` (exclusive) in a `@for` loop, producing a range one
  short (or one too many) of what was intended.
- Writing a `@while` loop without updating its condition variable inside the loop body, producing
  an infinite loop that hangs the Sass compiler entirely.
- Reaching for a manual `@each`/`@for` loop to generate a small, fixed handful of variants that
  would be just as clear (and easier to read) written out directly as plain CSS rules.

## Next

Continue to [color-functions.md](color-functions.md) to manipulate color values programmatically.
