# Tailwind with React

## Utility-First Styling

**Tailwind CSS** takes a fundamentally different approach from both CSS Modules and CSS-in-JS: no
separate stylesheet, no `styled.div` wrapper — just small, single-purpose utility classes applied
directly in JSX:

```jsx
function ProductCard({ name, price }) {
  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <h3 className="text-xl font-semibold">{name}</h3>
      <p>${price}</p>
    </div>
  );
}
```

Each class does one specific thing (`border`, `rounded-lg` for border-radius, `p-4` for padding) —
rather than naming a CSS class and defining what it means separately (as both CSS Modules and
CSS-in-JS require), you compose the final appearance directly from small, pre-defined pieces.

## Installing Tailwind in a Vite Project

```bash
npm install tailwindcss @tailwindcss/vite
```

```ts
// vite.config.ts
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

```css
/* index.css */
@import "tailwindcss";
```

This mirrors the same project-setup pattern from
[setting-up-a-react-project.md](../introduction-to-react/setting-up-a-react-project.md) — a plugin
added to Vite's configuration, processing utility classes at build time into an optimized,
minimal CSS file containing only the classes actually used.

## Conditional Styling

```jsx
function ProductCard({ name, price, isOnSale }) {
  return (
    <div className={`border rounded-lg p-4 ${isOnSale ? "border-red-500" : "border-gray-200"}`}>
      <h3 className="text-xl font-semibold">{name}</h3>
      <p>${price}</p>
    </div>
  );
}
```

Conditional styling here is plain JavaScript string interpolation — exactly the same pattern used
for conditional CSS Modules classes, since Tailwind classes are, underneath, still just CSS class
names.

## Advantages and Tradeoffs

| Advantage | Tradeoff |
|---|---|
| No naming decisions needed — no `.card`, no `styled.div`, just direct utility classes | JSX can become visually dense with many classes on one element |
| No runtime cost — pure CSS, generated at build time | A real learning curve for the specific utility class vocabulary |
| Extremely fast to prototype and adjust | Deviating from a project's design system is easy if not paired with deliberate constraints (matching the design-token discipline from [design-systems-and-design-tokens.md](../../css/css-core-fundamentals/design-systems-and-design-tokens.md)) |

## Common Mistakes

- Writing very long class strings inline without extracting a shared component for a repeated
  pattern, duplicating the same combination of utility classes across many places.
- Reaching for arbitrary one-off values (`p-[13px]`) routinely instead of Tailwind's built-in
  scale, undermining the design-system consistency Tailwind's constrained utility set is meant to
  encourage.
- Assuming Tailwind adds any runtime JavaScript cost — it's a build-time tool; the actual shipped
  CSS is plain, static CSS with no library code included at all.

## Next

Continue to
[component-styling-strategies.md](component-styling-strategies.md) to compare all three approaches
and choose deliberately for a real project.
