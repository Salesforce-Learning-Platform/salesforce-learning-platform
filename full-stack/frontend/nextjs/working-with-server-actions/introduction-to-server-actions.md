# Introduction to Server Actions

## What a Server Action Is

A **Server Action** (technically a "Server Function" used for a mutation) is an `async` function
marked with `"use server"` that runs exclusively on the server, but can be called directly from
client-side code — a form submission, a button click — without you hand-building a separate API
endpoint and `fetch` call to reach it.

```ts
// app/lib/actions.ts
"use server";

export async function addToCart(productId: string, quantity: number) {
  await db.cart.addItem(productId, quantity);
}
```

## Two Ways to Mark a Function as a Server Action

```ts
// Option 1: the whole file is server-only
"use server";
export async function addToCart(productId: string) { /* ... */ }
```

```tsx
// Option 2: inline, inside a Server Component
export default function ProductPage() {
  async function addToCart(productId: string) {
    "use server";
    // ...
  }
  return <form action={addToCart}>{/* ... */}</form>;
}
```

Either the top of a separate file (marking every export in it) or the top of an individual
`async` function body (inside a Server Component) works — the file-level form is more common once
several related actions accumulate.

## The Critical Security Note

This is the section flagged for deep-dive in this module's README, directly from Next.js's own
documentation: **"Server Functions are reachable via direct POST requests, not just through your
application's UI."** A Server Action called from one specific form is *not* protected by that
form's existence — anyone can construct a POST request to invoke it directly, bypassing your UI,
your client-side validation, and any assumption about how it's "supposed" to be called.

```ts
"use server";

export async function deleteProduct(productId: string) {
  const session = await auth();
  if (!session?.user?.isAdmin) {
    throw new Error("Unauthorized"); // MUST be checked here, every single time
  }
  await db.products.delete(productId);
}
```

This is exactly the "the client is never trustworthy" principle from
[frontend-and-backend-responsibilities.md](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md),
made concrete for Server Actions specifically: authorization must be checked *inside* the action
itself, not assumed from which button in the UI happened to trigger it.

## Server Actions Cannot Be Defined in Client Components

```tsx
"use client";

// This does NOT work — Server Actions can't be defined directly in a Client Component
async function addToCart() {
  "use server";
}
```

A Client Component can *call* a Server Action (by importing one from a `"use server"` file), but
cannot *define* one inline — exactly parallel to how a Client Component can *use* data from a
Server Component but can't itself run server-only code, from
[client-components.md](../rendering-strategies/client-components.md).

## Common Mistakes

- Assuming a Server Action is safe from unauthorized calls simply because the UI only exposes it
  behind an admin-only button — the button is a UI convenience, not a security boundary.
- Trying to define a Server Action inline inside a Client Component's function body, which isn't
  supported — it must be imported from a separate `"use server"` file instead.
- Treating "the frontend already validated this" as sufficient reason to skip validation inside
  the action itself — the exact same reasoning as
  [html-validation-and-constraints.md](../../html/html-forms-and-user-input/html-validation-and-constraints.md).

## Next

Continue to [forms-and-server-actions.md](forms-and-server-actions.md) to see the most common way
Server Actions are actually invoked.
