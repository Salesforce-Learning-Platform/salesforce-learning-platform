# Static Site Generation (SSG)

## Rendering at Build Time

**Static generation** renders a page's HTML once, during `next build`, rather than on each
request. The result is plain, pre-built HTML files — served instantly, with no server-side work
needed per visitor.

```tsx
// app/about/page.tsx — a marketing "About Us" page with no per-visitor data
export default function AboutPage() {
  return (
    <main>
      <h1>About Our Store</h1>
      <p>We've been selling great products since 2015.</p>
    </main>
  );
}
```

Because this page fetches no dynamic, per-request data, Next.js renders it once at build time and
serves that same static HTML to every visitor — the fastest possible response, since there's
genuinely no server-side computation happening at request time at all.

## Static Generation for Dynamic Routes

```tsx
// app/products/[slug]/page.tsx
export async function generateStaticParams() {
  const products = await fetch("https://api.example.com/products").then(res => res.json());
  return products.map(product => ({ slug: product.slug }));
}

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await fetch(`https://api.example.com/products/${slug}`).then(res => res.json());
  return <h1>{product.name}</h1>;
}
```

`generateStaticParams` tells Next.js exactly which dynamic route values to pre-render at build
time — here, every product's page is generated once during `next build`, from the current product
list, rather than computed fresh on every single visit.

## When Static Generation Fits

Static generation is the right default for content that's the same for every visitor and doesn't
change on every request: marketing pages, blog posts, product pages where a small delay before new
products appear is acceptable. It's the wrong fit for content that must reflect the exact current
moment for every single request — a shopping cart's live contents, or a personalized "recommended
for you" section, covered next in
[server-side-rendering.md](server-side-rendering.md).

## The Real Tradeoff: Freshness

The cost of static generation's speed is that the page's content is only as fresh as the last
build — if a product's price changes right after `next build` ran, visitors keep seeing the old
price until the site is rebuilt. This exact tradeoff is what
[incremental-static-regeneration.md](incremental-static-regeneration.md) exists to soften, without
giving up static generation's speed entirely.

## Common Mistakes

- Using static generation for content that's genuinely personalized per visitor (a logged-in
  user's account page) — a statically generated page is the *same* HTML for every single visitor,
  which is fundamentally incompatible with per-user content.
- Forgetting `generateStaticParams` for a dynamic route, leaving Next.js with no list of which
  specific pages to actually pre-render at build time.
- Assuming static generation means "never updates" — it updates on the next `next build`, or via
  ISR's background regeneration, not literally never.

## Next

Continue to [server-side-rendering.md](server-side-rendering.md) for content that genuinely needs
to be computed fresh on every request.
