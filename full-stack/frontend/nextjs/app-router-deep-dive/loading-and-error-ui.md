# Loading and Error UI

## `loading.tsx` — Automatic Suspense

```tsx
// app/products/loading.tsx
export default function Loading() {
  return <p>Loading products...</p>;
}
```

Simply adding a `loading.tsx` file next to `products/page.tsx` automatically wraps that page in a
`<Suspense>` boundary (from
[code-splitting.md](../../react/performance-optimization-in-react/code-splitting.md)), using this
component as the fallback — shown instantly while the page's data-fetching Server Component
resolves, with **zero manual `<Suspense>` JSX required**. This is a genuine App Router convenience
over plain React, where you'd need to write the `<Suspense>` wrapper yourself.

## `error.tsx` — Automatic Error Boundary

```tsx
// app/products/error.tsx
"use client"; // error.tsx must be a Client Component

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <p>Something went wrong loading products.</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

Similarly, an `error.tsx` file automatically wraps its segment in an error boundary — directly the
same mechanism as
[react-error-boundaries.md](../../react/error-handling-and-debugging/react-error-boundaries.md),
just wired up automatically by file convention rather than manually wrapping components in a
class-based `<ErrorBoundary>`. It receives the actual `error` and a `reset` function to retry
rendering that segment.

## Scoped Per Segment

```text
app/
├── products/
│   ├── loading.tsx     # only covers /products and its children
│   ├── error.tsx         # only catches errors in /products and its children
│   └── page.tsx
└── about/
    └── page.tsx           # unaffected by products' loading/error files
```

Because these files are scoped to their own folder (and everything nested inside it), a slow or
failing `/products` page shows its own loading/error state without affecting `/about` or any other
unrelated route — directly the "smaller, targeted boundaries" reasoning from
[lazy-loading.md](../../react/performance-optimization-in-react/lazy-loading.md), now applied
automatically per route segment rather than manually placed.

## What `error.tsx` Doesn't Catch

Consistent with
[react-error-boundaries.md](../../react/error-handling-and-debugging/react-error-boundaries.md),
`error.tsx` catches rendering errors within its segment — it does not catch errors in the root
layout itself (a separate `global-error.tsx` exists for that specific case) or errors in event
handlers, which still need ordinary
[try/catch](../../javascript/error-handling-and-debugging/try-catch-finally.md).

## Common Mistakes

- Forgetting `"use client"` on `error.tsx` — error boundaries require client-side interactivity
  (the `reset` function) and must be Client Components.
- Expecting one `loading.tsx`/`error.tsx` at the root to cover every route's specific needs,
  rather than adding scoped ones at the specific segments that benefit from a tailored
  loading/error experience.
- Assuming `error.tsx` catches every possible failure in its segment, including things outside
  rendering (like an event handler) — the same scope limitation as manual error boundaries applies
  here too.

## Next

Continue to [metadata-api-and-seo.md](metadata-api-and-seo.md) for controlling what appears in a
page's `<head>`.
