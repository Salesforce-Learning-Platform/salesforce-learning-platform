# Nesting

## Writing Rules Inside Rules

```scss
nav {
  background: #222;

  a {
    color: white;
    text-decoration: none;
  }
}
```

```css
/* Compiled output */
nav { background: #222; }
nav a { color: white; text-decoration: none; }
```

Sass lets a style rule be written **inside** another, automatically combining the outer selector
with the inner one to produce the final, plain CSS selector (`nav a`) — directly mirroring how the
nested rule visually relates to the element it's inside, rather than repeating `nav` manually in a
separate flat rule the way plain CSS requires.

## The Parent Selector (`&`)

```scss
.button {
  padding: 8px 16px;

  &:hover {
    background: #eee;
  }

  &.is-active {
    font-weight: bold;
  }

  &--large {
    padding: 12px 24px;
  }
}
```

```css
.button { padding: 8px 16px; }
.button:hover { background: #eee; }
.button.is-active { font-weight: bold; }
.button--large { padding: 12px 24px; }
```

The `&` symbol inside a nested rule refers back to the **parent selector** exactly, letting a
pseudo-class (`:hover`), an additional class (`.is-active`), or a suffix (`--large`, a common
[BEM-style](../css-architecture-and-debugging/) modifier naming convention) attach directly to the
outer selector, with no space — impossible to express with plain nesting alone, since a bare nested
rule always produces a descendant selector (with a space), not a directly-attached one.

## Nesting Selector Lists

```scss
.alert, .warning {
  strong { color: red; }
}
```

```css
.alert strong, .warning strong { color: red; }
```

When the outer selector is itself a comma-separated list, Sass nests each one **separately**, then
recombines the results back into a single selector list — producing the same effect as writing out
`.alert strong` and `.warning strong` by hand.

## Nesting With Combinators

```scss
.card {
  > .card-header { font-weight: bold; }
  + .card { margin-top: 16px; }
}
```

```css
.card > .card-header { font-weight: bold; }
.card + .card { margin-top: 16px; }
```

CSS combinators (`>` for a direct child, `+` for an adjacent sibling, per
[css-syntax-and-selectors.md](../css-core-fundamentals/css-syntax-and-selectors.md)) work
naturally inside a nested rule, placed at the start of the inner selector.

## The Real Cost of Over-Nesting

```scss
// AVOID — nested far too deeply
.page {
  .content {
    .card {
      .card-body {
        .card-title {
          color: red; // compiles to .page .content .card .card-body .card-title
        }
      }
    }
  }
}
```

Sass's own documentation warns directly against this: deeper nesting produces a longer, more
specific compiled selector, which means more bytes served and more work for the browser to match
against every element — and, per
[specificity-and-cascade.md](../css-core-fundamentals/specificity-and-cascade.md), an
unnecessarily high-specificity selector that becomes harder to override later. A commonly cited
practical guideline is to avoid nesting more than **three levels** deep.

## Common Mistakes

- Nesting purely to mirror the HTML's own visual structure, producing deeply over-specific
  selectors that provide no real benefit over a flatter, more intentional structure.
- Forgetting `&` and writing a modifier class as if it were a descendant (`.button { .is-active {
  ... } }`, which compiles to `.button .is-active` — a completely different, incorrect selector
  from the intended `.button.is-active`).
- Relying on nesting depth alone to communicate a component's structure, rather than a deliberate
  naming convention like BEM (covered in the upcoming
  [CSS Architecture and Debugging module](../css-architecture-and-debugging/)).

## Next

Continue to [partials-and-imports.md](partials-and-imports.md) to split a growing stylesheet
across multiple files.
