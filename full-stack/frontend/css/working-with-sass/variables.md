# Variables

## Declaring and Using a Sass Variable

```scss
$primary-color: #1a73e8;
$spacing-unit: 8px;

.button {
  background: $primary-color;
  padding: $spacing-unit * 2;
}
```

A Sass variable starts with `$`, is assigned once, and can be referenced anywhere afterward in the
stylesheet — immediately useful for the exact same reason
[design-systems-and-design-tokens.md](../css-core-fundamentals/design-systems-and-design-tokens.md)
values centralizing a color or spacing value: change it in one place, and every usage updates.

## `!default` — Configurable Defaults

```scss
// _config.scss — a library's own default
$button-radius: 4px !default;

// consumer's file, loaded BEFORE the library
$button-radius: 8px;
@use "config"; // the library's !default does NOT override this already-set value
```

`!default` assigns a value to a variable **only if it isn't already set**. This is specifically
useful when writing Sass meant to be reused across projects (a component library, a theme): the
library defines sensible defaults with `!default`, and any project using it can override those
specific values before the library's own file runs, without needing to edit the library's source at
all.

## The Deep-Dive: Sass Variables vs. CSS Custom Properties

```scss
// Sass variable — resolved and REMOVED at compile time
$color: blue;
.a { color: $color; }
```

```css
/* CSS custom property — a genuine, live runtime value */
:root { --color: blue; }
.a { color: var(--color); }
```

This is the single most important distinction in this module, directly building on
[css-variables.md](../css-core-fundamentals/css-variables.md):

| | Sass variable (`$x`) | CSS custom property (`--x`) |
|---|---|---|
| When it exists | Only during compilation | Live, in the actual running browser |
| Can JavaScript read/change it? | No — it's already gone by the time CSS ships | Yes, via `getComputedStyle`/`style.setProperty` |
| Scoping model | Follows Sass's own block scoping rules | Follows the CSS cascade (inherits through the DOM) |
| Theming (light/dark mode) | Can't change at runtime without recompiling | Naturally supports runtime theme switches |

A Sass variable is **imperative** — resolved once, in source order, exactly where it's used, and
completely absent from the final output. A CSS custom property is **declarative** — it stays alive
in the compiled CSS and can be read, overridden per-scope, or changed by JavaScript at any time
after the page has loaded.

## When to Reach for Each

- **Sass variables** fit values that are genuinely fixed at build time and never need to change
  once shipped — a breakpoint value used only inside `@media` queries (which CSS custom properties
  can't be used inside directly), or a value only ever used to *compute* something else at compile
  time.
- **CSS custom properties** fit anything that needs to vary at runtime — theming (light/dark mode,
  per [css-variables.md](../css-core-fundamentals/css-variables.md)'s own example), or any value
  JavaScript might need to read or change.

Real projects commonly use **both**, for genuinely different jobs — Sass variables to keep the
*authoring* of the stylesheet itself DRY, and CSS custom properties to expose the specific values
that actually need to be live and runtime-adjustable.

## Common Mistakes

- Trying to change a Sass variable's value from JavaScript at runtime — it's already compiled away;
  there's nothing left in the browser to change.
- Using a Sass variable for a value that genuinely needs to support live theming, then being
  unable to implement light/dark mode without a full separate recompile per theme.
- Forgetting `!default` when writing a reusable Sass file meant to be configured by whoever
  imports it, forcing consumers to edit the source file directly to change a value.

## Next

Continue to [nesting.md](nesting.md) to organize related selectors visually, another core Sass
convenience.
