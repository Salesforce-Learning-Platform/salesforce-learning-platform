# Client Components

## Opting In with `"use client"`

```tsx
// app/ui/add-to-cart-button.tsx
"use client"; // must be the very first line, before any imports

import { useState } from "react";

export default function AddToCartButton({ productId }: { productId: string }) {
  const [isAdding, setIsAdding] = useState(false);

  async function handleClick() {
    setIsAdding(true);
    await fetch("/api/cart", { method: "POST", body: JSON.stringify({ productId }) });
    setIsAdding(false);
  }

  return (
    <button onClick={handleClick} disabled={isAdding}>
      {isAdding ? "Adding..." : "Add to Cart"}
    </button>
  );
}
```

`"use client"` marks a **boundary** — this component (and everything it imports and directly
renders) is bundled and sent to the browser, becoming a genuine, interactive React component
exactly like everything covered throughout the [React domain](../../react/), with full access to
`useState`, `useEffect`, event handlers, and browser APIs.

## When a Client Component Is Actually Needed

Per Next.js's own guidance, mark a component `"use client"` specifically when it needs:

- **State or event handlers** (`useState`, `onClick`, `onChange`) — like the `AddToCartButton`
  above.
- **Lifecycle logic** (`useEffect`).
- **Browser-only APIs** (`localStorage`, `window`, geolocation).
- **React Context** — Context (from
  [context-api.md](../../react/global-state-management/context-api.md)) is not supported directly
  in Server Components at all; a context provider must itself be a Client Component.

## Composing Server and Client Components Together

```tsx
// app/products/[slug]/page.tsx — a Server Component
import AddToCartButton from "@/app/ui/add-to-cart-button"; // a Client Component

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await getProduct(slug); // fetched on the SERVER

  return (
    <div>
      <h1>{product.name}</h1>
      <p>${product.price}</p>
      <AddToCartButton productId={product.id} /> {/* interactive, runs in the BROWSER */}
    </div>
  );
}
```

This is the realistic, everyday pattern: a Server Component fetches data and renders mostly-static
content, while a small, specifically-marked Client Component handles just the interactive part —
directly applying the "mark only the specific interactive piece, not the whole page" guidance from
Next.js's own documentation, keeping as much of the page's JavaScript off the client bundle as
possible.

## Data Passed from Server to Client Must Be Serializable

```tsx
<AddToCartButton productId={product.id} /> {/* fine — a string */}
<AddToCartButton onAdd={() => trackEvent()} /> {/* NOT fine — functions aren't serializable across this boundary */}
```

Because a Server Component's output and a Client Component's props cross a genuine server/client
boundary, only serializable values (strings, numbers, plain objects, arrays — not functions or
class instances) can be passed from a Server Component into a Client Component as props.

## Common Mistakes

- Marking an entire page (or a large layout) `"use client"` just because one small piece of it
  needs interactivity, unnecessarily shipping far more JavaScript to the browser than needed.
- Trying to pass a function or a non-serializable value as a prop from a Server Component to a
  Client Component, which fails since it can't cross the actual server/client boundary.
- Forgetting that a context provider (from the React domain's Global State Management module)
  must itself be wrapped in `"use client"`, since Context isn't supported directly in Server
  Components.

## Next

Continue to
[choosing-a-rendering-strategy.md](choosing-a-rendering-strategy.md) to bring every strategy
covered in this module together into one practical decision framework.
