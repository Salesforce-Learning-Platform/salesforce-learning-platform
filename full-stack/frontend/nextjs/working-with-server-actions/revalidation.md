# Revalidation

## Why a Successful Mutation Might Not Appear Immediately

A product's page might be served from Next.js's cache — via static generation or ISR, from
[incremental-static-regeneration.md](../rendering-strategies/incremental-static-regeneration.md).
A Server Action mutating that data (adding a new review) doesn't automatically know to invalidate
that cached page — without explicitly telling Next.js, a visitor could keep seeing the old,
review-less version even though the new review was successfully saved to the database.

## `revalidatePath`

```ts
"use server";
import { revalidatePath } from "next/cache";

export async function addReview(productSlug: string, formData: FormData) {
  // ...authorization, validation, and the mutation itself, from data-mutations.md...

  revalidatePath(`/products/${productSlug}`); // invalidate this specific product's cached page
}
```

`revalidatePath` tells Next.js a specific route's cached content is now stale — the *next* request
to that path regenerates it with fresh data, exactly the on-demand ISR mechanism introduced in
[incremental-static-regeneration.md](../rendering-strategies/incremental-static-regeneration.md),
now triggered directly from the mutation that actually invalidated it, rather than waiting for a
scheduled interval.

## `revalidateTag` for More Granular Control

```ts
// When fetching the data initially:
const products = await fetch("https://api.example.com/products", {
  next: { tags: ["products"] },
});

// After a mutation, in the Server Action:
import { revalidateTag } from "next/cache";
revalidateTag("products"); // invalidates every cached fetch tagged "products", across any route
```

Where `revalidatePath` invalidates one specific route, `revalidateTag` invalidates every cached
fetch carrying a matching tag — useful when the same underlying data (a product list) appears on
multiple different pages simultaneously (a homepage's "featured products," the full catalog, a
category page) and all of them need to reflect the change together.

## Redirecting After a Mutation

```ts
"use server";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

export async function createProduct(formData: FormData) {
  // ...authorization, validation, mutation...
  revalidatePath("/products");
  redirect("/products"); // send the admin back to the now-updated catalog
}
```

A critical ordering detail, directly from Next.js's own documentation: `redirect()` throws a
special control-flow signal internally — **any code placed after it will never run**. Always call
`revalidatePath`/`revalidateTag` *before* `redirect`, never after.

## Common Mistakes

- Forgetting to revalidate at all after a mutation, leaving cached pages showing stale data
  indefinitely (or until the next scheduled ISR interval, if one exists).
- Calling `revalidatePath`/`revalidateTag` *after* `redirect()`, where it silently never executes
  because `redirect` has already thrown and stopped execution.
- Using `revalidatePath` when the same data appears across several different routes — `revalidateTag`
  is the more appropriate, comprehensive tool for that specific situation.

## Next

Continue to [error-handling.md](error-handling.md) for showing pending and error states while a
Server Action is in flight or fails.
