# Design Systems and Design Tokens

## What a Design Token Is

A **design token** is a named, centralized value representing a single design decision — a color,
a spacing unit, a font size — used consistently across an entire product instead of being
hardcoded repeatedly wherever it's needed. Design tokens are a design-tooling concept (they often
originate in a design tool like Figma), and CSS custom properties (see
[css-variables.md](css-variables.md)) are the natural way to implement them in code.

```css
:root {
  /* Color tokens */
  --color-primary: #1a73e8;
  --color-danger: #d93025;

  /* Spacing tokens */
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 32px;

  /* Typography tokens */
  --font-size-body: 1rem;
  --font-size-heading: 2rem;
}
```

## Why Centralize Values at All

Without tokens, the same shade of blue might be typed as `#1a73e8` in a dozen different files —
looking identical today, but becoming a maintenance liability the moment the brand color needs to
change: every occurrence must be found and updated individually, and it's easy to miss one. A
single token, referenced everywhere via `var(--color-primary)`, needs updating in exactly one
place.

## Semantic vs. Raw Tokens

Mature design systems commonly use two layers of tokens:

- **Raw/primitive tokens**: the actual values (`--blue-600: #1a73e8`).
- **Semantic tokens**: named by *purpose*, referencing the raw tokens (`--color-primary:
  var(--blue-600)`).

```css
:root {
  --blue-600: #1a73e8;
  --red-600: #d93025;

  --color-primary: var(--blue-600);
  --color-danger: var(--red-600);
}
```

This extra layer means a rebrand (changing what "primary" means) only requires updating the
semantic layer's mapping, without touching every component that correctly refers to "primary,"
regardless of which raw color currently backs it.

## Theming with Tokens

Because CSS custom properties resolve live and respect scoping (see
[css-variables.md](css-variables.md)), swapping an entire theme (light/dark mode, a white-label
brand variant) is often just a matter of redefining the same semantic token names within a
different scope:

```css
:root { --color-background: white; --color-text: black; }
[data-theme="dark"] { --color-background: #121212; --color-text: white; }
```

## Common Mistakes

- Hardcoding raw values throughout components "just this once," gradually eroding the whole point
  of having tokens in the first place.
- Naming tokens after their raw value rather than their purpose (`--blue` instead of
  `--color-primary`), which breaks down the moment the underlying color needs to change for a
  rebrand.
- Building a two-layer semantic/raw token system prematurely for a small project where a single,
  flat set of well-named tokens would be simpler and entirely sufficient.

## Module Summary

Across this module: CSS rules pair selectors with declarations, and selector choice determines
precisely what's targeted (see
[css-syntax-and-selectors.md](css-syntax-and-selectors.md)); conflicts between rules are resolved
by the cascade and specificity, evaluated before source order (see
[specificity-and-cascade.md](specificity-and-cascade.md)); inheritance is defined per-property, not
universally (see
[inheritance-and-computed-styles.md](inheritance-and-computed-styles.md)); every element is sized
according to the box model, with `box-sizing` determining whether padding/border are included in a
declared width (see [box-model.md](box-model.md)); units should be chosen deliberately — `rem` for
predictable global sizing, `em` for local scaling, `%`/`vh`/`vw` for relative and viewport-based
sizing (see [css-units.md](css-units.md)); custom properties provide live, runtime-updatable
variables (see [css-variables.md](css-variables.md)); modern functions like `clamp()` express fluid
responsive values in a single declaration (see
[modern-css-functions.md](modern-css-functions.md)); and design tokens built on custom properties
are what make a design system's values consistent and maintainable at scale.
