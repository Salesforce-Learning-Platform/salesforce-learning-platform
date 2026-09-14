# Incremental Static Regeneration (ISR)

## The Middle Ground

[static-site-generation.md](static-site-generation.md) is fast but can go stale until the next
full rebuild; [server-side-rendering.md](server-side-rendering.md) is always fresh but pays a
per-request cost. **Incremental Static Regeneration** gets most of both: pages are served from a
fast, static cache, but Next.js automatically regenerates them in the background after a
specified time — no full site rebuild required.

## Time-Based Revalidation

```tsx
// app/products/page.tsx — the product catalog, updated a few times a day
export const revalidate = 3600; // regenerate at most once per hour

export default async function ProductsPage() {
  const products = await fetch("https://api.example.com/products").then(res => res.json());
  return (
    <ul>{products.map(p => <li key={p.id}>{p.name} — ${p.price}</li>)}</ul>
  );
}
```

The exact sequence: a request within the first hour gets the cached static page instantly. Once
an hour has passed, the *next* request still gets that same cached (now stale) page immediately —
but Next.js simultaneously starts regenerating a fresh version in the background. Once that
finishes, subsequent requests get the updated version, cached again for the next hour. Visitors
never wait for regeneration themselves; they always get an instant response, occasionally a few
minutes staler than the absolute latest data.

## On-Demand Revalidation

```tsx
// app/actions.ts — a Server Action, run after an admin updates a product
"use server";
import { revalidatePath } from "next/cache";

export async function updateProduct(productId: string, data: object) {
  await fetch(`https://api.example.com/products/${productId}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
  revalidatePath("/products"); // invalidate the cached page immediately, rather than waiting an hour
}
```

For cases where waiting for the next scheduled revalidation isn't acceptable — an admin updates a
product and expects the catalog to reflect it right away — `revalidatePath` (or the more granular
`revalidateTag`) invalidates the cache immediately, so the *next* request regenerates the page
right away instead of waiting out the full `revalidate` interval.

## Choosing a `revalidate` Interval

Next.js's own documentation recommends a relatively long interval (an hour, rather than a few
seconds) as the default, reserving on-demand revalidation for cases needing more precision — a
very short time-based interval defeats much of ISR's caching benefit, approaching the per-request
cost of plain server-side rendering without the guarantee of always-current data that SSR actually
provides.

## Common Mistakes

- Setting an extremely short `revalidate` value (a few seconds) for content that doesn't actually
  need that precision, undermining the caching benefit ISR exists to provide.
- Relying solely on time-based revalidation for a change that needs to appear immediately (like an
  admin's own edit), when on-demand revalidation via `revalidatePath`/`revalidateTag` is the
  correct tool for that specific need.
- Confusing ISR with plain static generation — ISR pages *do* update over time automatically;
  they're not frozen at their build-time content the way pure SSG (without any `revalidate`) is.

## Next

Continue to [server-components.md](server-components.md) — a different, complementary dimension
of the App Router's rendering model: not *when* a page renders, but *where* each piece of it runs.
