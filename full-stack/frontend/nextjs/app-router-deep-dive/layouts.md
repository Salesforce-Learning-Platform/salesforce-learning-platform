# Layouts

## Shared UI via `layout.tsx`

```tsx
// app/products/layout.tsx
export default function ProductsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <CategorySidebar />
      <main>{children}</main>
    </div>
  );
}
```

A `layout.tsx` wraps every `page.tsx` (and nested layout) within its folder — here, every route
under `/products` (the catalog, `/products/electronics`, an individual product page) automatically
gets the same `CategorySidebar`, without each individual page needing to render it itself. This is
`children` (from
[component-composition.md](../../react/component-architecture-and-composition/component-composition.md))
doing exactly the same composition job as React Router's `<Outlet>` from
[nested-routes.md](../../react/client-side-routing/nested-routes.md).

## Layouts Nest Automatically

```text
app/
├── layout.tsx              (root — wraps EVERYTHING)
└── products/
    ├── layout.tsx             (wraps everything under /products)
    └── [slug]/
        └── page.tsx              (an individual product page)
```

Visiting `/products/keyboard-k1` renders: root layout → products layout → the product page,
nested in that exact order — each layer wrapping the next via `children`, without any of them
needing to know about the others explicitly.

## The Genuinely Different Behavior: Layouts Don't Re-render on Navigation

This is the section flagged for deep-dive in this module's README, and it's a real, useful
distinction from plain React Router: navigating from `/products/keyboard-k1` to
`/products/mouse-m2` re-renders only the `page.tsx` content — the shared `ProductsLayout` (and its
`CategorySidebar`) is **not** re-rendered or reset. Any state held inside the layout (a sidebar's
scroll position, an expanded filter panel) persists automatically across that navigation, without
any special code required to preserve it.

```tsx
// app/products/layout.tsx
"use client";
export default function ProductsLayout({ children }: { children: React.ReactNode }) {
  const [filterOpen, setFilterOpen] = useState(false); // survives navigating between products
  return (
    <div>
      <CategorySidebar open={filterOpen} onToggle={() => setFilterOpen(!filterOpen)} />
      <main>{children}</main>
    </div>
  );
}
```

## Root Layout Is Required and Special

As covered in [project-structure.md](../getting-started-with-nextjs/project-structure.md), the
root `app/layout.tsx` is mandatory and must contain `<html>` and `<body>` — every other, nested
layout is optional, added only where a specific section of the route tree genuinely needs its own
shared UI.

## Common Mistakes

- Assuming a layout re-renders like an ordinary component would on every navigation within its
  section — it deliberately doesn't, which is a feature, not a bug, but worth knowing explicitly
  rather than discovering by surprise.
- Duplicating the same navigation or sidebar markup across multiple `page.tsx` files instead of
  extracting a shared `layout.tsx` for that section.
- Adding a nested `layout.tsx` for a route segment that doesn't actually need any shared UI beyond
  what the root layout already provides, adding an unnecessary extra file.

## Next

Continue to [loading-and-error-ui.md](loading-and-error-ui.md) for automatic loading and error
states per route segment.
