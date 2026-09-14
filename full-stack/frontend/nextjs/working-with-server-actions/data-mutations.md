# Data Mutations

## The Full Mutation Flow

Combining everything covered so far into one complete, realistic action:

```ts
// app/lib/actions.ts
"use server";

import { auth } from "@/lib/auth";
import { db } from "@/lib/db";

export async function addReview(productSlug: string, formData: FormData) {
  // 1. Authorization — required, per introduction-to-server-actions.md
  const session = await auth();
  if (!session?.user) {
    throw new Error("You must be logged in to leave a review");
  }

  // 2. Validation — required, exactly like a Route Handler
  const rating = Number(formData.get("rating"));
  const comment = formData.get("comment");
  if (!rating || rating < 1 || rating > 5 || !comment) {
    throw new Error("A rating (1–5) and comment are required");
  }

  // 3. The actual mutation
  await db.reviews.create({
    productSlug,
    userId: session.user.id,
    rating,
    comment,
  });
}
```

This is deliberately structured in the same order a Route Handler would be (from
[api-design-patterns.md](../building-apis-with-nextjs/api-design-patterns.md)): check who's
asking, validate what they sent, then perform the actual database operation — a Server Action is a
real backend boundary and deserves exactly the same rigor as a Route Handler, even though it's
invoked differently.

## Passing Additional Arguments Beyond `FormData`

```tsx
// Binding an extra argument (productSlug) ahead of the form's own data
<form action={addReview.bind(null, product.slug)}>
  <input type="number" name="rating" />
  <textarea name="comment" />
</form>
```

`.bind(null, productSlug)` pre-fills the action's first argument, so the form only needs to
supply the rest via `FormData` — useful when a Server Action needs context (like which product a
review belongs to) that isn't itself part of the submitted form fields.

## Reading Data Before Mutating It

```ts
export async function updateQuantity(itemId: string, formData: FormData) {
  const session = await auth();
  const cartItem = await db.cartItems.findUnique({ where: { id: itemId } });

  if (cartItem?.userId !== session?.user?.id) {
    throw new Error("Not authorized to modify this cart item"); // ownership check, not just login check
  }

  const newQuantity = Number(formData.get("quantity"));
  await db.cartItems.update({ where: { id: itemId }, data: { quantity: newQuantity } });
}
```

Authorization isn't always just "is someone logged in" — it's frequently "does *this specific*
logged-in user actually own *this specific* resource," a distinct and equally necessary check
before mutating anything tied to a particular user's data.

## Common Mistakes

- Performing the database mutation before checking authorization/validation, rather than failing
  fast — this can waste work and, in some cases, leave partial or inconsistent state if the
  operation is interrupted partway through.
- Checking only "is this user logged in" when the actual requirement is "does this user own this
  specific resource" — a real, distinct authorization gap.
- Forgetting `.bind()` (or an equivalent closure) when a Server Action genuinely needs context
  beyond what the form's own fields provide.

## Next

Continue to [revalidation.md](revalidation.md) to make sure the UI actually reflects this
mutation once it succeeds.
