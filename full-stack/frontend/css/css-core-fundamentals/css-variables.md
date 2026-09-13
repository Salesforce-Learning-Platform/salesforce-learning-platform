# CSS Variables (Custom Properties)

## Declaring and Using a Custom Property

CSS custom properties (informally "CSS variables") let you name a value once and reuse it
throughout a stylesheet:

```css
:root {
  --primary-color: #1a73e8;
  --spacing-unit: 8px;
}

.button {
  background-color: var(--primary-color);
  padding: calc(var(--spacing-unit) * 2);
}
```

- Custom property names must start with `--`.
- `var(--name)` reads the value.
- `var(--name, fallback)` provides a fallback used if the variable isn't defined.

## Why `:root`?

`:root` targets the document's root element (`<html>`), making a variable declared there available
everywhere on the page — this is the standard place to declare global design values, since every
other element can read from it through normal inheritance.

## Custom Properties Are Real, Live Values — Not a Preprocessor Trick

Unlike a preprocessor's variables (which are resolved once, at build time, into plain CSS), native
CSS custom properties are resolved by the browser at render time and can be changed dynamically —
including from JavaScript:

```js
document.documentElement.style.setProperty('--primary-color', '#e91e63');
```

This immediately updates every rule using `var(--primary-color)`, live, with no rebuild step —
useful for features like runtime theme switching (light/dark mode) that a build-time-only
preprocessor variable can't achieve on its own.

## Scoping

Custom properties follow normal CSS inheritance and cascade rules — redeclaring a variable inside
a more specific selector overrides it for that scope and its descendants only, without affecting
the rest of the page:

```css
:root { --card-bg: white; }

.dark-theme {
  --card-bg: #1e1e1e; /* overrides --card-bg only within .dark-theme and its descendants */
}
```

## Common Mistakes

- Assuming custom properties resolve once at build time like a preprocessor's variables — they're
  live and inherit/cascade like any other CSS value, resolved by the browser at render time.
- Forgetting the `--` prefix, which is required and is what distinguishes a custom property from a
  standard CSS property name.
- Declaring color/spacing values ad hoc throughout a stylesheet instead of centralizing them as
  variables — see
  [design-systems-and-design-tokens.md](design-systems-and-design-tokens.md) for why this
  centralization matters at scale.

## Next

Continue to [modern-css-functions.md](modern-css-functions.md) to see functions that compute
values dynamically, often combined with custom properties.
