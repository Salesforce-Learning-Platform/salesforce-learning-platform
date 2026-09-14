# 🔍 Debugging with DevTools

## The Styles Pane — Seeing Every Rule Affecting an Element

```
Right-click an element → Inspect → the Styles pane lists EVERY CSS
rule currently matching it, in cascade order, with overridden
declarations shown crossed out.
```

Rather than guessing which of several stylesheets (or which BEM component, per
[component-based-css.md](component-based-css.md)) is responsible for a given style, the Styles
pane shows the actual, complete list of matching rules — including which ones lost the
[cascade](../css-core-fundamentals/specificity-and-cascade.md) and were overridden. This turns "why
is this element styled this way" from a guess into a direct, observable fact.

## The Box Model Visualization — Diagnosing Overflow

```
content → padding → border → margin
   (the box model, per box-model.md, shown as a literal
    nested diagram with real pixel values for THIS element)
```

DevTools renders the [box model](../css-core-fundamentals/box-model.md) as an interactive diagram
with the element's actual, current pixel values for content, padding, border, and margin. This is
the fastest way to diagnose a genuinely common real bug: an element unexpectedly overflowing its
container, usually traceable directly to a padding or margin value that's larger than expected once
seen in the actual box model diagram, rather than in the abstract.

## Toggling Classes and Pseudo-States Live

```
The .cls button — toggle a class (like a BEM modifier, e.g.
.product-card--featured) on/off and see the visual effect immediately

The :hov button — simulate :hover, :focus, or :active without
actually triggering the real user interaction
```

Toggling a BEM modifier class on and off live is a direct, fast way to confirm a modifier is
actually doing what's intended — and simulating `:hover`/`:focus` lets a hover or focus style be
inspected and adjusted without needing to keep the mouse physically positioned over the element the
whole time.

## Computed Styles — The Final, Resolved Value

```
The Computed tab shows the ACTUAL final value of every property,
after the cascade has already resolved which rule wins
```

While the Styles pane shows every *rule* that applies, the **Computed** tab shows the single,
final, resolved *value* for every property on the element — useful when several rules are competing
and it's not immediately obvious which one's value actually won.

## A Practical Debugging Workflow for a Layout Bug

1. Inspect the affected element and check the Styles pane for any crossed-out (overridden)
   declaration that looks like it shouldn't have lost.
2. Open the box model diagram to check for unexpected padding, margin, or border values causing
   overflow.
3. Toggle relevant classes (a BEM modifier, a utility class) on and off to isolate which one is
   actually responsible for the unwanted effect.
4. Check the Computed tab if it's still unclear which of several competing rules is winning.
5. Fix the actual source file — never leave a fix only in DevTools' live-editing, which resets on
   reload.

## Common Mistakes

- "Fixing" a bug only inside DevTools' live style editor and forgetting to bring the actual change
  back into the real source file — it vanishes completely on the next page reload.
- Guessing which stylesheet or component is responsible for a style instead of checking the Styles
  pane directly, wasting time on a manual search DevTools can answer immediately.
- Overlooking the Computed tab when several competing rules make it genuinely unclear which
  declaration is actually winning the cascade.

## Module Summary

Across this module: **BEM** namespaces CSS class names by block, element, and modifier, turning
global CSS naming into a predictable, low-specificity, collision-resistant social contract (see
[bem-naming-convention.md](bem-naming-convention.md)); **component-based CSS** scopes every style
block to exactly one real UI component, never reaching outside itself (see
[component-based-css.md](component-based-css.md)); choosing between **utility classes and
component classes** comes down to whether something has genuine, repeating, nameable meaning or is
a one-off adjustment (see
[utility-classes-vs-component-classes.md](utility-classes-vs-component-classes.md)); a **real-world
folder structure** (`base/`, `layout/`, `components/`, `utilities/`) makes a project's CSS
architecture visible directly from its file tree (see
[real-world-css-folder-structure.md](real-world-css-folder-structure.md)); and browser **DevTools**
— the Styles pane, the box model diagram, and the Computed tab — turns diagnosing a real layout or
cascade problem from guesswork into direct observation.
