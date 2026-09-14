# Partials and @use

## Splitting a Stylesheet Into Partials

```
styles/
├── _variables.scss     ← a PARTIAL (leading underscore)
├── _mixins.scss        ← a PARTIAL
├── _buttons.scss       ← a PARTIAL
└── main.scss           ← the entry point, NOT a partial
```

A **partial** is a Sass file meant only to be loaded by another file, never compiled on its own —
signaled by a leading underscore in its filename (`_variables.scss`). This underscore tells Sass's
tooling not to attempt to compile that file directly into its own separate CSS output, exactly the
[reusable-component-design.md](../../react/component-architecture-and-composition/reusable-component-design.md)
idea of splitting one large concern into focused, single-purpose files, applied to stylesheets.

## Loading a Partial With `@use`

```scss
// main.scss
@use "variables";
@use "mixins";
@use "buttons";
```

`@use "variables"` loads `_variables.scss` — the underscore and file extension are both omitted
when referencing it. Unlike the older `@import` rule (now deprecated in favor of `@use`), a file
loaded with `@use` is only ever included **once** in the compiled output, no matter how many other
files load it — eliminating a real class of bugs where the same rules accidentally appeared
multiple times in older Sass code.

## Namespacing — Why `@use` Is Safer Than the Old `@import`

```scss
// _colors.scss
$primary: #1a73e8;

// main.scss
@use "colors";

.button {
  background: colors.$primary; // must be qualified with the file's namespace
}
```

By default, `@use` gives every loaded file its own **namespace**, derived from its filename
(`colors`, from `_colors.scss`). Referencing anything from it — a variable, a mixin, a function —
requires that namespace prefix (`colors.$primary`). This directly solves a real problem the older
`@import` rule had: without namespacing, two different partials defining a variable with the same
name would silently collide; `@use`'s namespacing makes that collision structurally impossible,
the same reasoning
[modules.md](../../../backend/nodejs-core-concepts/modules.md) applies to JavaScript's explicit
module exports.

## Customizing or Dropping the Namespace

```scss
@use "colors" as c;          // custom, shorter namespace: c.$primary
@use "colors" as *;          // no namespace at all: $primary directly
```

`as <name>` picks a custom namespace (useful for a long or awkward default). `as *` loads a file's
members with no namespace prefix at all — convenient, but reintroduces the same collision risk
namespacing exists to prevent, so it's best reserved for files unlikely to ever define a colliding
name.

## A Realistic `main.scss`

```scss
// main.scss — the single entry point a build tool actually compiles
@use "variables";
@use "mixins";
@use "buttons";
@use "cards";
@use "layout";
```

Real Sass projects typically compile **one** entry file (`main.scss`), which itself does nothing
but `@use` every partial the project needs, in a sensible order — this is the file a build tool
(per [setting-up-scss.md](setting-up-scss.md)) actually points at; the individual partials are
never compiled directly.

## Common Mistakes

- Forgetting the leading underscore on a partial, causing a build tool to also try to compile it
  as its own separate, redundant CSS output.
- Still using the older, deprecated `@import` rule in new code instead of `@use` — losing the
  "only loaded once" guarantee and the collision protection namespacing provides.
- Using `@use "file" as *` habitually out of a preference for shorter names, quietly reintroducing
  the naming-collision risk namespacing is specifically meant to prevent.

## Next

Continue to [mixins.md](mixins.md) to package reusable style logic, not just values, into
something callable.
