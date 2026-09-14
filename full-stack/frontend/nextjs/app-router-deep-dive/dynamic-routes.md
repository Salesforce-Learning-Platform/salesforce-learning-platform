# Dynamic Routes

## The Problem: One Page Per Product

Hand-creating a folder for every single product (`products/keyboard-k1/page.tsx`,
`products/mouse-m2/page.tsx`, ...) clearly doesn't scale to a catalog with thousands of items. A
**dynamic segment** solves this exactly the way `:id` did for React Router in
[route-parameters.md](../../react/client-side-routing/route-parameters.md) — one file generating
many pages from data.

## Creating a Dynamic Segment

```text
app/
└── products/
    └── [slug]/
        └── page.tsx      → matches "/products/keyboard-k1", "/products/mouse-m2", anything
```

Wrapping a folder name in square brackets (`[slug]`) tells the App Router this segment is dynamic
— it matches any value at that position in the URL.

## Reading the Segment's Value

```tsx
// app/products/[slug]/page.tsx
export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await fetch(`https://api.example.com/products/${slug}`).then(res => res.json());
  return <h1>{product.name}</h1>;
}
```

The `params` prop — an (importantly, `Promise`-wrapped) object whose keys match the dynamic
segment's name — plays the exact same role as React Router's `useParams()`, just delivered as a
prop rather than a hook, since this is a Server Component rather than a plain React component.

## Generating Static Params

```tsx
export async function generateStaticParams() {
  const products = await fetch("https://api.example.com/products").then(res => res.json());
  return products.map(product => ({ slug: product.slug }));
}
```

Exactly as introduced in
[static-site-generation.md](../rendering-strategies/static-site-generation.md),
`generateStaticParams` tells Next.js which specific `slug` values to pre-render at build time —
without it, dynamic segments are still rendered correctly, just on-demand per request rather than
ahead of time.

## Nested Dynamic Segments

```text
app/
└── orders/
    └── [orderId]/
        └── items/
            └── [itemId]/
                └── page.tsx    → "/orders/:orderId/items/:itemId"
```

Multiple dynamic segments can nest, each contributing its own key to `params` — here,
`params` resolves to `{ orderId: "...", itemId: "..." }`, exactly mirroring how React Router
handles multiple `:param` segments in one path.

## Common Mistakes

- Forgetting to `await params` (or `searchParams`) — in current Next.js, these are Promises, not
  plain objects, a genuine change worth being deliberate about rather than assuming synchronous
  access.
- Choosing an ambiguous segment name that could be confused with a static route — a folder named
  `[category]` sitting alongside a static folder named `electronics` at the same level needs
  careful routing precedence understanding, best avoided by keeping dynamic and static segments at
  clearly distinct levels.
- Omitting `generateStaticParams` when static generation was actually the intended strategy for
  that route, leaving it rendered on-demand instead of pre-built.

## Next

Continue to [layouts.md](layouts.md) for sharing UI across all of these routes without
duplicating it in every single `page.tsx`.
