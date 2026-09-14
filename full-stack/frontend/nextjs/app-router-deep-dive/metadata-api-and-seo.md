# The Metadata API and SEO

## Why This Matters

Recall [seo-impact-of-semantic-html.md](../../html/semantic-html-and-browser-rendering/seo-impact-of-semantic-html.md):
a page's `<title>` and meta description are read directly by search engines to generate result
listings. The Metadata API is Next.js's built-in, type-safe way to set these per route, without
manually writing `<head>` tags into JSX yourself.

## Static Metadata

```tsx
// app/about/page.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About Our Store",
  description: "Learn about our mission and values.",
};

export default function AboutPage() {
  return <h1>About Us</h1>;
}
```

Exporting a `metadata` object from a `page.tsx` or `layout.tsx` — only supported in Server
Components — is all that's needed; Next.js generates the corresponding `<title>` and `<meta>` tags
automatically.

## Dynamic Metadata with `generateMetadata`

```tsx
// app/products/[slug]/page.tsx
import type { Metadata } from "next";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const product = await fetch(`https://api.example.com/products/${slug}`).then(res => res.json());
  return {
    title: product.name,
    description: product.description,
  };
}

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await fetch(`https://api.example.com/products/${slug}`).then(res => res.json());
  return <h1>{product.name}</h1>;
}
```

For metadata that depends on data (like each product's actual name), `generateMetadata` fetches
and returns it dynamically — receiving the same `params` as the page component itself, since each
product genuinely needs its own distinct title and description for SEO to work correctly per
product.

## Avoiding a Duplicate Fetch

Notice the example above fetches the same product twice — once for metadata, once for the page
body. React's `cache()` function memoizes a fetch so it only actually executes once per request,
even when called from both `generateMetadata` and the page component:

```ts
// lib/data.ts
import { cache } from "react";

export const getProduct = cache(async (slug: string) => {
  return fetch(`https://api.example.com/products/${slug}`).then(res => res.json());
});
```

Both `generateMetadata` and the page component call `getProduct(slug)`, but the underlying fetch
runs only once per request — directly the request-deduplication benefit React Query provided in
the React domain's
[react-query.md](../../react/server-state-and-api-integration/react-query.md), here achieved with
a much smaller, built-in tool since it's scoped to one request rather than a whole client-side
cache.

## File-Based Metadata

```text
app/
├── favicon.ico              # automatically used as the site's favicon
├── opengraph-image.jpg        # the default social-media preview image
└── products/
    └── opengraph-image.jpg      # overrides the default, specifically for /products
```

Certain filenames (`favicon.ico`, `opengraph-image.jpg`, `robots.txt`, `sitemap.xml`) are
recognized automatically by their presence alone — placing a more specific one deeper in the route
tree overrides a more general one above it, following the same nesting logic as layouts.

## Common Mistakes

- Fetching the same data separately in both `generateMetadata` and the page component without
  `cache()`, doubling the actual network/database work for no benefit.
- Forgetting that `metadata`/`generateMetadata` only work in Server Components — a page marked
  `"use client"` cannot export either.
- Leaving every page with the same generic title/description, missing the actual SEO value of
  giving each meaningfully different page its own specific, accurate metadata.

## Module Summary

Across this module: the App Router recognizes a specific set of special filenames — `page`,
`layout`, `loading`, `error` — layered onto an otherwise ordinary folder structure (see
[file-based-routing.md](file-based-routing.md)); nested folders build out real route structures
just like React Router, but through the filesystem itself (see
[pages-and-nested-routes.md](pages-and-nested-routes.md)); dynamic segments (`[slug]`) generate
many pages from one file, with `params` delivered as a Promise (see
[dynamic-routes.md](dynamic-routes.md)); layouts share UI across nested routes and — genuinely
differently from plain React Router — don't re-render on navigation within their section (see
[layouts.md](layouts.md)); `loading.tsx`/`error.tsx` provide automatic Suspense and error
boundaries per segment, with zero manual JSX (see
[loading-and-error-ui.md](loading-and-error-ui.md)); and the Metadata API sets per-route SEO
metadata, statically or dynamically, with `cache()` avoiding duplicate fetches between metadata
and page content.
