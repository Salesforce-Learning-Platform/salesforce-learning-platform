# What Is Sass?

## A Language That Compiles to CSS

**Sass** ("Syntactically Awesome Style Sheets") is a **preprocessor**: a language that isn't
directly understood by the browser, but is instead **compiled** into plain CSS before it's ever
served. Every feature Sass adds — variables, nesting, mixins — exists only in the source `.scss`
file; by the time a browser sees the output, it's ordinary CSS, exactly like anything covered in
[CSS Core Fundamentals](../css-core-fundamentals/).

## Two Syntaxes: Sass and SCSS

```scss
// SCSS syntax — CSS-like braces and semicolons; the syntax this module uses throughout
.card {
  padding: 16px;
  &:hover {
    padding: 20px;
  }
}
```

```sass
// Sass syntax — indentation-based, no braces or semicolons
.card
  padding: 16px
  &:hover
    padding: 20px
```

Sass actually offers two interchangeable syntaxes. **SCSS** (`.scss` files) is a strict superset of
CSS — any valid CSS file is already valid SCSS — using the same familiar braces and semicolons.
The original **Sass syntax** (`.sass` files) uses indentation instead. SCSS is by far the more
common choice in real projects, specifically because its CSS compatibility makes it far easier to
adopt incrementally in an existing codebase; this module uses SCSS throughout.

## Why a Preprocessor Exists At All

Plain CSS genuinely lacks (or, via custom properties, only partially replicates) several things
real stylesheets benefit from: reusable, named values; the ability to nest related rules together
visually; reusable blocks of style logic; and basic computation. Sass's own documentation puts its
purpose directly: it "helps keep large stylesheets well-organized and makes it easy to share design
within and across projects" — the same underlying motivation behind
[css-core-fundamentals's design-systems-and-design-tokens.md](../css-core-fundamentals/design-systems-and-design-tokens.md),
approached with a more powerful toolset.

## What Survives Into the Final CSS, and What Doesn't

```scss
// SCSS source
$primary-color: #1a73e8;
.button { background: $primary-color; }
```

```css
/* Compiled CSS output — the variable itself is gone entirely */
.button { background: #1a73e8; }
```

This is the single most important thing to internalize before going further: everything Sass adds
is a **compile-time** tool. The `$primary-color` variable, the nesting, any mixin — none of it
exists once compilation finishes; only the final, plain CSS rules remain, which is exactly what the
browser receives and renders.

## Common Mistakes

- Assuming Sass changes what browsers actually support — it doesn't add any new browser
  capability; it only makes *writing* the same eventual CSS more convenient and maintainable.
- Choosing the indented Sass syntax for a project that already has existing CSS to migrate
  incrementally — SCSS was specifically designed to preserve CSS compatibility for exactly that
  case, per the syntax comparison above.
- Expecting a Sass feature (like a variable) to behave like a runtime CSS feature (like a custom
  property) — they solve related but genuinely different problems, covered precisely in
  [variables.md](variables.md).

## Next

Continue to [setting-up-scss.md](setting-up-scss.md) to actually get SCSS compiling in a real
project.
