# CSS Modules

## The Problem: Global CSS Class Names

Plain CSS (from the [CSS domain](../../css/)) has one global namespace for class names — two
components anywhere in a large application both defining `.card` will collide, with whichever
stylesheet loads last silently winning, per the cascade rules from
[specificity-and-cascade.md](../../css/css-core-fundamentals/specificity-and-cascade.md). This
becomes a genuine, recurring problem as a codebase grows and more people contribute components
independently.

## CSS Modules: Locally-Scoped by Default

```css
/* ProductCard.module.css */
.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
}
```

```jsx
// ProductCard.jsx
import styles from "./ProductCard.module.css";

function ProductCard({ name, price }) {
  return (
    <div className={styles.card}>
      <h3 className={styles.title}>{name}</h3>
      <p>${price}</p>
    </div>
  );
}
```

The `.module.css` naming convention (recognized automatically by build tools like Vite) tells the
build step to rewrite every class name into something guaranteed unique — `styles.card` might
actually resolve to a class like `ProductCard_card__a1b2c` in the compiled output. Another
component's completely unrelated `.card` class in its own `.module.css` file is guaranteed never
to collide with this one.

## Conditional Classes

```jsx
import styles from "./ProductCard.module.css";

function ProductCard({ name, price, isOnSale }) {
  return (
    <div className={isOnSale ? `${styles.card} ${styles.onSale}` : styles.card}>
      <h3 className={styles.title}>{name}</h3>
      <p>${price}</p>
    </div>
  );
}
```

Combining conditional class logic with plain JavaScript string templates works, but a small
utility library like `clsx` is commonly used in real codebases to make this more readable once
more than one or two conditions are involved.

## Advantages and Tradeoffs

| Advantage | Tradeoff |
|---|---|
| Guaranteed no naming collisions | Requires a build step (works out of the box with Vite/Next.js, but isn't "just CSS" you can drop in anywhere) |
| Plain CSS syntax — no new language to learn | Dynamic, prop-driven styling (like a computed color) is more awkward than with CSS-in-JS |
| Clear separation between markup and styles | Still requires manually combining class names for conditional styles |

## Common Mistakes

- Forgetting the `.module.css` file extension convention, which is what actually triggers the
  local-scoping behavior in most build tools — a plain `.css` import doesn't get this treatment.
- Manually string-concatenating many conditional class names without a utility like `clsx`,
  producing hard-to-read conditional logic as the number of states grows.
- Assuming CSS Modules classes can be referenced by their original name (`.card`) from outside the
  component — the whole point is that the compiled name is unpredictable and local to that file.

## Next

Continue to [css-in-js.md](css-in-js.md) for an approach that defines styles directly in
JavaScript, unlocking prop-driven styling more directly.
