# 🧩 Component-Based CSS

## Designing a Style Block Around One Component

```css
/* _product-card.scss — everything this ONE component needs, in one place */
.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
}

.product-card__image {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.product-card__title {
  font-size: 1.125rem;
  font-weight: 600;
}

.product-card__price {
  color: #1a73e8;
}

.product-card--out-of-stock {
  opacity: 0.6;
}
```

**Component-based CSS** means every style block is scoped to exactly one real UI component —
directly the same idea as
[reusable-component-design.md](../../react/component-architecture-and-composition/reusable-component-design.md)'s
component design, applied to CSS itself. A `.product-card`'s styles live together, are named with
BEM (per [bem-naming-convention.md](bem-naming-convention.md)) so they can't collide with anything
else, and don't reach outside their own component to style something unrelated.

## One Component, One File (or One Partial)

```
styles/
├── components/
│   ├── _product-card.scss
│   ├── _button.scss
│   └── _navbar.scss
```

Pairing one component with one [Sass partial](../working-with-sass/partials-and-imports.md) keeps
a component's entire visual definition in a single, predictable place — finding and modifying a
component's styles means opening exactly one file, not searching across a large, undifferentiated
stylesheet.

## A Component's CSS Should Never Reach Outside Itself

```css
/* AVOID — a component reaching out to style something else entirely */
.product-card h1 {
  margin-top: 0; /* affects EVERY h1 that happens to be inside a product card,
                     even ones that have nothing to do with this component */
}

/* PREFER — style only this component's own, explicitly-named elements */
.product-card__title {
  margin-top: 0;
}
```

A genuinely component-scoped stylesheet only ever targets its own BEM-named classes — never a bare
element selector, and never another component's classes. This is what actually makes a component
**safe to reuse or move**: dropping a `.product-card` into a different part of the page never risks
its styles leaking onto, or being affected by, whatever else happens to be nearby in the DOM.

## Composing Components, Not Inheriting Them

```html
<div class="product-card product-card--featured">
  <img class="product-card__image" src="..." alt="Mechanical keyboard" />
  <h3 class="product-card__title">Mechanical Keyboard</h3>
  <button class="btn btn--primary">Add to Cart</button>
</div>
```

A component's CSS can sit right alongside another, unrelated component's classes (`.btn`,
`.btn--primary`) on nearby elements without any risk of collision, precisely because each is
independently BEM-namespaced — this is composition, the same underlying idea as
[Component Composition](../../react/component-architecture-and-composition/) in React, expressed
at the CSS layer.

## Common Mistakes

- Writing a component's styles using bare element selectors (`.product-card h1`) instead of
  explicit BEM element classes, silently affecting anything else that happens to share that
  element type nearby.
- Letting one component's stylesheet reach in and override another component's classes directly,
  creating a hidden dependency between two components that should be independent.
- Splitting one component's styles across multiple unrelated files, making it harder to find and
  reason about everything that affects how it looks.

## ➡️ Next

Continue to
[utility-classes-vs-component-classes.md](utility-classes-vs-component-classes.md) to decide when
a small, one-off adjustment deserves a utility class instead of a new component class.
