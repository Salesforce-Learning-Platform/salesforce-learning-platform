# Inheritance with @extend

## Sharing Styles Between Selectors

```scss
.button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
}

.button-danger {
  @extend .button;
  background: #d93025;
  color: white;
}
```

```css
.button, .button-danger { padding: 8px 16px; border-radius: 4px; border: none; }
.button-danger { background: #d93025; color: white; }
```

`@extend` lets one selector inherit another's declarations — rather than *copying* `.button`'s
rules into `.button-danger` (which is what a mixin, per [mixins.md](mixins.md), would do),
`@extend` **combines the selectors themselves** in the compiled output, so both share one set of
declarations for the shared styles.

## `@extend` vs. a Mixin — a Real, Consequential Difference

```css
/* @extend's output: ONE shared rule for the common declarations */
.button, .button-danger { padding: 8px 16px; }

/* A mixin's output: the declarations are DUPLICATED into every usage */
.button { padding: 8px 16px; }
.button-danger { padding: 8px 16px; }
```

This is the genuine tradeoff between the two: `@extend` produces smaller compiled CSS (the shared
declarations exist once, referenced by a combined selector), while a mixin duplicates the
declarations into every place it's included. `@extend`'s combined-selector approach, though, means
the resulting specificity and source order can become harder to predict as more selectors extend
the same base — a real cost mixins don't have, since each usage is independent.

## Placeholder Selectors — `@extend`'s Safer Default

```scss
%button-base {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
}

.button-primary { @extend %button-base; background: #1a73e8; }
.button-danger { @extend %button-base; background: #d93025; }
```

```css
.button-primary, .button-danger { padding: 8px 16px; border-radius: 4px; border: none; }
.button-primary { background: #1a73e8; }
.button-danger { background: #d93025; }
```

A **placeholder selector** (`%name`) exists purely to be extended — it never compiles into its own
standalone CSS rule on its own. This is the generally preferred pattern over extending a real class
like `.button` directly: it makes clear that `%button-base` is a shared base meant only for
`@extend`, not a class anyone would apply directly in HTML.

## Common Mistakes

- Extending a real, already-in-use class (`.button`) when a placeholder selector (`%button-base`)
  more clearly communicates that the shared styles exist purely to be extended, not applied
  directly.
- Extending across selectors with very different roles just to avoid repeating a few declarations,
  producing an unexpectedly large and hard-to-predict combined selector in the compiled output.
- Reaching for `@extend` when a mixin's independent-duplication behavior is actually the better,
  more predictable fit — there's no universally "correct" choice between them; it depends on
  whether shared, combined selectors or independent, parameterizable duplication better fits the
  actual use case.

## Next

Continue to [operators.md](operators.md) to perform real calculations directly inside Sass
expressions.
