# Inheritance and Computed Styles

## Inheritance Is Per-Property, Not Universal

Some CSS properties automatically pass their value down to descendant elements unless explicitly
overridden; others never do. This is defined individually by the CSS specification for each
property — there's no single rule like "everything inherits" or "nothing inherits."

| Typically inherits | Typically does not inherit |
|---|---|
| `color` | `border` |
| `font-family`, `font-size` | `margin`, `padding` |
| `line-height` | `background` |
| `text-align` | `width`, `height` |

The pattern: text-related properties tend to inherit (it would be tedious to reset `font-family`
on every single element); box-model and layout properties tend not to (a `border` on a container
inheriting to every nested element would rarely be desired).

## Forcing or Blocking Inheritance

Every property accepts a few universal keyword values that override its default inheritance
behavior:

| Value | Effect |
|---|---|
| `inherit` | Forces the property to take its parent's computed value, even if it doesn't inherit by default |
| `initial` | Resets the property to its specification-defined default, ignoring inheritance entirely |
| `unset` | Acts like `inherit` for properties that naturally inherit, and `initial` for those that don't |

```css
.reset-border {
  border: inherit; /* forces this element to match its parent's border, even though border doesn't inherit by default */
}
```

## The Computed Value

The **computed value** is the final value the browser actually uses for a property on a specific
element, after resolving the cascade (see
[specificity-and-cascade.md](specificity-and-cascade.md)), inheritance, and any relative units
(percentages, `em`) into an absolute result. Browser DevTools' "Computed" tab (alongside the
"Styles" tab covered in
[browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md))
shows this final resolved value directly, which is often faster for debugging than manually tracing
every applicable rule and inherited value.

## Common Mistakes

- Assuming a property like `border` or `padding` will inherit like `color` does, and being
  surprised it needs to be set explicitly on each element.
- Confusing `inherit` (take the parent's value) with `initial` (reset to specification default) —
  these frequently produce different results.
- Debugging by reading the stylesheet alone instead of checking the browser's Computed tab, which
  shows the actual final resolved value directly.

## Next

Continue to [box-model.md](box-model.md) to see the model every element's size and spacing is
actually calculated from.
