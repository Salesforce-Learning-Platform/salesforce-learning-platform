# ⚖️ Utility Classes vs. Component Classes

## Two Tools From Earlier Modules, Revisited Together

[component-based-css.md](component-based-css.md) covered BEM-named component classes.
[CSS Frameworks](../css-frameworks/tailwindcss-fundamentals.md) covered Tailwind's utility
classes. Real projects routinely need both — this file is about deciding which one fits a given
situation, rather than treating the choice as all-or-nothing.

## What Each Is Actually Good At

```html
<!-- Component class: the card's own identity and structure -->
<div class="product-card product-card--featured">
  <h3 class="product-card__title">Mechanical Keyboard</h3>

  <!-- Utility classes: a one-off spacing adjustment, not worth a new named class -->
  <p class="mt-2 text-sm text-gray-500">In stock</p>
</div>
```

A **component class** (`.product-card__title`) names something with real, reusable meaning — it's
worth a name because the same structure and styling genuinely repeats across the app. A **utility
class** (`mt-2`, `text-sm`) is for a small, specific adjustment that doesn't deserve its own name —
creating `.product-card__stock-label { margin-top: 8px; font-size: 0.875rem; }` purely to express
"a bit of top margin and smaller text" is arguably more ceremony than the adjustment warrants.

## 🚦 A Practical Decision Rule

| Situation | Reach for |
|---|---|
| A structure/style that repeats across many places | **Component class** (BEM) |
| A one-off spacing, color, or sizing tweak | **Utility class** |
| Something with real semantic meaning worth naming | **Component class** |
| An adjustment specific to exactly one instance | **Utility class** |

The underlying test: would a future developer reading this class name learn something meaningful
about *what this is* (component class), or only about *how it looks* (utility class)? Both answers
are legitimate — they're just answering different questions.

## The Real Tradeoff of Each, Revisited

Overusing utility classes for everything reproduces the exact downside
[introduction-to-css-frameworks.md](../css-frameworks/introduction-to-css-frameworks.md) already
noted: markup can become visually dense and harder to scan, and genuinely reusable structure gets
scattered as repeated utility combinations instead of named once. Overusing component classes for
every tiny variation produces the opposite problem: a proliferation of narrow, single-use
modifier classes (`.card--slightly-more-padding`) that add ceremony without real reuse value.

## Common Mistakes

- Creating a new BEM modifier class for a one-off, single-instance adjustment that a utility class
  would express just as clearly with far less ceremony.
- Reaching for utility classes to express something that's actually a real, repeating, meaningful
  component — losing the self-documenting value a well-named BEM class would have provided.
- Treating this as a fixed, universal rule rather than a judgment call — the right balance
  genuinely depends on the specific project, team, and how much repetition an adjustment actually
  has.

## ➡️ Next

Continue to
[real-world-css-folder-structure.md](real-world-css-folder-structure.md) to organize both kinds of
styles in a real project.
