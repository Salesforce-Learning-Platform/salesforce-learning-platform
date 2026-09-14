# Forms and Server Actions

## Wiring a Server Action to a Form

```tsx
// app/lib/actions.ts
"use server";

export async function addReview(formData: FormData) {
  const rating = formData.get("rating");
  const comment = formData.get("comment");
  await db.reviews.create({ rating, comment });
}
```

```tsx
// app/products/[slug]/review-form.tsx
import { addReview } from "@/app/lib/actions";

export default function ReviewForm() {
  return (
    <form action={addReview}>
      <input type="number" name="rating" min="1" max="5" />
      <textarea name="comment" />
      <button type="submit">Submit Review</button>
    </form>
  );
}
```

Passing a Server Action directly to a `<form>`'s `action` prop — a React extension of the plain
HTML `action` attribute from
[form-submission-and-data.md](../../html/html-forms-and-user-input/form-submission-and-data.md) —
is the primary, most common way Server Actions are invoked. React automatically calls the action
with the form's data as a `FormData` object, no manual `event.preventDefault()` or `fetch` call
needed at all.

## Progressive Enhancement — A Genuine Benefit

Next.js's own documentation highlights this: a form using a Server Action, rendered from a Server
Component, **still submits correctly even if the page's JavaScript hasn't finished loading yet, or
is disabled entirely** — the browser falls back to a real HTML form submission, and Next.js
handles it server-side regardless. This is a meaningfully different (and more resilient) behavior
than the JavaScript-dependent `fetch`-based form submission covered in
[controlled-forms.md](../../react/advanced-forms-and-validation/controlled-forms.md), which
requires JavaScript to have loaded and run at all.

## Calling a Server Action from a Client Component

```tsx
"use client";
import { addToCart } from "@/app/lib/actions";

export default function AddToCartButton({ productId }: { productId: string }) {
  return (
    <button formAction={() => addToCart(productId)}>
      Add to Cart
    </button>
  );
}
```

A Client Component can't *define* a Server Action (per
[introduction-to-server-actions.md](introduction-to-server-actions.md)), but it can *import and
call* one — here, via a plain `onClick`-style invocation, exactly the pattern from
[client-components.md](../rendering-strategies/client-components.md), just calling a
server-defined function instead of a local one.

## Extracting Values with `FormData`

```ts
export async function addReview(formData: FormData) {
  const rating = Number(formData.get("rating")); // FormData values are always strings — convert explicitly
  const comment = formData.get("comment") as string;
  // ...
}
```

Exactly like the route parameter values in
[route-parameters.md](../../react/client-side-routing/route-parameters.md), `FormData` values are
always strings — a numeric field like `rating` needs an explicit `Number()` conversion before use.

## Common Mistakes

- Manually calling `event.preventDefault()` and building a `fetch` request for a form that a
  Server Action could handle directly — this is exactly the boilerplate Server Actions exist to
  remove.
- Forgetting that `FormData.get()` always returns a string (or `null`), leading to comparing a
  numeric field against a number without converting it first.
- Assuming a form using a Server Action requires client-side JavaScript to function at all — this
  is precisely the progressive-enhancement benefit that sets it apart from a `fetch`-based
  submission.

## Next

Continue to [data-mutations.md](data-mutations.md) for what actually happens inside the action
once it receives the form's data.
