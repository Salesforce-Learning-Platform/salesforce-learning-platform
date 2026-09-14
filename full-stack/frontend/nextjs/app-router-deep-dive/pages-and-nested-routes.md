# Pages and Nested Routes

## Building the Store's Route Structure

```text
app/
├── page.tsx                          → "/"                    (homepage)
├── products/
│   ├── page.tsx                        → "/products"            (full catalog)
│   └── electronics/
│       └── page.tsx                      → "/products/electronics" (one category)
└── about/
    └── page.tsx                          → "/about"
```

Each nested folder adds one more URL segment — `products/electronics/page.tsx` is reachable at
`/products/electronics`, exactly mirroring the folder structure itself, no separate routes
configuration file involved at all.

## A Route Segment's `page.tsx`

```tsx
// app/products/page.tsx
export default async function ProductsPage() {
  const products = await fetch("https://api.example.com/products").then(res => res.json());
  return (
    <ul>
      {products.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  );
}
```

This is an ordinary Server Component (from
[server-components.md](../rendering-strategies/server-components.md)) — nothing about `page.tsx`
itself is special beyond its filename and location; it's simply the component the App Router
renders for that specific route.

## Comparing Directly to React Router

| | React Router (from [routes-and-navigation.md](../../react/client-side-routing/routes-and-navigation.md)) | Next.js App Router |
|---|---|---|
| Where routes are defined | A `<Routes>`/`<Route>` tree, explicitly in code | The `app` folder's own structure |
| Adding a new route | Add a `<Route path="...">` | Add a folder with a `page.tsx` inside it |
| Navigation component | `<Link to="...">` | `<Link href="...">`, from `next/link` |

The underlying *concept* — mapping a URL to a component — is identical to what was covered in the
React domain; the App Router just expresses that mapping through the filesystem itself rather than
an explicit routes tree written in code.

## Linking Between Pages

```tsx
import Link from "next/link";

<Link href="/products/electronics">Shop Electronics</Link>
```

`next/link`'s `<Link>` plays the same role as React Router's `<Link>` — client-side navigation
without a full page reload — plus automatic prefetching of the linked page's code and data ahead
of time, a Next.js-specific optimization not present in plain React Router.

## Common Mistakes

- Trying to define routes in a separate configuration file out of React Router habit — the App
  Router has no such file; the folder structure itself is the configuration.
- Forgetting `next/link`'s `<Link>` and using a plain `<a>` for in-app navigation, losing
  prefetching and triggering an unwanted full page reload — exactly the same mistake flagged for
  React Router in [routes-and-navigation.md](../../react/client-side-routing/routes-and-navigation.md).
- Nesting folders more deeply than the actual desired URL structure requires, when a flatter
  structure would express the same routes more simply.

## Next

Continue to [dynamic-routes.md](dynamic-routes.md) to generate pages from data — like one page per
product — rather than hand-creating a folder for every single one.
