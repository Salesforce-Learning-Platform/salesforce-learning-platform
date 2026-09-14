# Functions

## Defining and Calling a Function

```scss
@use "sass:math";

@function rem($pixels, $base: 16px) {
  @return math.div($pixels, $base) * 1rem;
}

.title {
  font-size: rem(24px); // → 1.5rem
}
```

Note the `math.div()` call rather than a plain `/` — the `/` operator's division behavior is
deprecated in modern Sass (it's being reserved as a plain separator, matching how CSS Grid already
uses `/`), so `math.div()`, from Sass's built-in `sass:math` module, is the current, correct way to
divide.

`@function` defines a reusable computation, and `@return` provides its result. Unlike a mixin —
which is *included* and emits style rules directly — a function is **called** as part of an
expression, exactly like a built-in function such as `calc()`, and its return value is used inline
wherever it's called.

## Mixins vs. Functions — the Real Distinction

| | Mixin | Function |
|---|---|---|
| Invoked with | `@include name(...)` | `name(...)`, directly in a value |
| Produces | CSS rules/declarations | A single computed value |
| Typical use | A reusable block of styles ([mixins.md](mixins.md)) | A reusable calculation |

Sass's own guidance is explicit here: functions should be used purely to **compute values**, with
no side effects (like defining CSS rules or setting a global variable) — that job belongs to
mixins. Keeping this boundary clear makes both tools easier to reason about: seeing `@include` in a
stylesheet immediately signals "this inserts style rules"; seeing a bare function call signals
"this computes a value used right here."

## Arguments, Including Arbitrary Ones

```scss
@function sum($numbers...) {
  $total: 0;
  @each $n in $numbers {
    $total: $total + $n;
  }
  @return $total;
}

$total-spacing: sum(8px, 16px, 24px); // → 48px
```

The `...` after a parameter name (`$numbers...`) captures any number of positional arguments into
a single list — useful for a function meant to operate on an arbitrary, not-fixed-in-advance
collection of values, here summed together with
[control-directives.md](control-directives.md)'s `@each` loop.

## A Realistic Example: Converting Units Consistently

```scss
@use "sass:math";

@function rem($pixels, $base: 16px) {
  @return math.div($pixels, $base) * 1rem;
}

.card {
  padding: rem(16px);
  font-size: rem(14px);
  border-radius: rem(8px);
}
```

This directly parallels
[css-units.md](../css-core-fundamentals/css-units.md)'s reasoning for preferring `rem` for
predictable global sizing — a `rem()` helper function lets every declaration in the stylesheet be
authored in familiar pixel values, while the actual compiled output consistently uses `rem`,
without needing to manually calculate the conversion by hand at every single usage.

## Common Mistakes

- Writing a function that also tries to emit CSS rules directly, rather than only returning a
  value — that responsibility belongs to a mixin, and mixing the two makes the code harder to
  predict.
- Assuming a function call in Sass behaves like `@include` (i.e., inserting rules) — a function
  call is used as part of a value, not as its own statement the way `@include` is.
- Reimplementing something a built-in Sass or CSS function (like `calc()`, or Sass's own built-in
  math/color functions, per [color-functions.md](color-functions.md)) already provides.

## Next

Continue to [inheritance-and-extends.md](inheritance-and-extends.md) to see Sass's other
code-sharing mechanism, `@extend`.
