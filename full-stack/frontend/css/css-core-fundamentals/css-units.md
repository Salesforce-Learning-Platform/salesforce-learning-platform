# CSS Units

## Absolute vs. Relative

CSS units fall into two categories with a fundamentally different behavior: **absolute** units
always represent the same physical size regardless of context; **relative** units are computed
based on something else — a parent's size, the root font size, or the viewport.

## Absolute Units

| Unit | Represents |
|---|---|
| `px` | A pixel — the de facto standard absolute unit for screen design |

Other absolute units exist (`cm`, `in`, `pt`) but are rarely used for screen UI, being oriented
toward print.

## Relative Units

| Unit | Relative to |
|---|---|
| `%` | The relevant dimension of the parent element |
| `em` | The font size of the *current* element (or its parent's, for properties other than `font-size` itself) |
| `rem` | The font size of the root (`<html>`) element — unaffected by nesting |
| `vw` / `vh` | 1% of the viewport's width / height |
| `vmin` / `vmax` | The smaller / larger of `vw` and `vh` |

## `em` vs. `rem` — A Frequent Point of Confusion

`em` compounds with nesting: if a parent has `font-size: 1.2em` and a child also uses `1.2em`, the
child's actual computed size multiplies against its parent's already-scaled size, which can produce
unexpectedly large or small text several levels deep. `rem` always resolves against the root
element's font size, regardless of nesting depth, which is why `rem` is generally preferred for
consistent, predictable sizing across a whole page, while `em` remains useful for sizing something
*relative to its own component's local font size* (like padding that should scale with a button's
own text).

```css
html { font-size: 16px; }

.card { font-size: 1.5em; }       /* 24px (1.5 × 16px parent context) */
.card .badge { font-size: 1.5em; } /* 36px (1.5 × 24px — compounds!) */
.card .badge-fixed { font-size: 1.5rem; } /* 24px (always 1.5 × root, ignores nesting) */
```

## Choosing the Right Unit

| Use case | Common choice |
|---|---|
| Font sizes | `rem` |
| Spacing that should scale with local text size (button padding) | `em` |
| A container's width relative to its parent | `%` |
| Full-viewport sections | `vh`/`vw` |
| Border widths, fine details unlikely to need scaling | `px` |

## Common Mistakes

- Using `em` for global font sizing without realizing nested components compound the scaling
  unexpectedly.
- Using `vh` for a container's height without accounting for mobile browsers' dynamic toolbar,
  which can make `100vh` taller than the actually visible area (a well-known real-world quirk).
- Hardcoding `px` everywhere, losing the benefit of users' browser-level font-size preferences
  (`rem`-based sizing respects a user's changed default font size; fixed `px` values don't).

## Next

Continue to [css-variables.md](css-variables.md) to see how repeated values (including units) are
centralized and reused.
