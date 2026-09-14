# Server-Side Rendering (SSR)

## Rendering Fresh, on Every Request

Unlike static generation (from
[static-site-generation.md](static-site-generation.md)), **server-side rendering** computes a
page's HTML fresh, on the server, for every single incoming request — necessary when content is
genuinely personalized or must reflect the exact current moment.

```tsx
// app/cart/page.tsx — a shopping cart, genuinely different for every visitor
import { cookies } from "next/headers";

export default async function CartPage() {
  const sessionId = (await cookies()).get("session_id")?.value;
  const cart = await fetch(`https://api.example.com/cart/${sessionId}`, {
    cache: "no-store", // forces fresh data on every request — see below
  }).then(res => res.json());

  return (
    <main>
      <h1>Your Cart</h1>
      <ul>{cart.items.map(item => <li key={item.id}>{item.name}</li>)}</ul>
    </main>
  );
}
```

Reading the visitor's session cookie (per
[cookies.md](../../javascript/using-browser-functionalities/cookies.md)) makes this page
inherently per-visitor — there's no single static HTML that could correctly serve every user, so
Next.js renders it dynamically, on the server, for each request.

## What Makes a Route Dynamically Rendered

A route is rendered dynamically (server-side, per request) when it does something that can't be
determined at build time — reading cookies or headers (as above), using `cache: "no-store"` on a
fetch, or setting a `revalidate` of `0`. Otherwise, Next.js defaults toward static generation
wherever it safely can, for the performance benefit covered in
[static-site-generation.md](static-site-generation.md).

## The Tradeoff: Speed vs. Freshness

| | Static Generation | Server-Side Rendering |
|---|---|---|
| When it renders | Once, at build time | On every request |
| Speed | Fastest — pre-built HTML | Slower — real work happens per request |
| Freshness | As fresh as the last build/revalidation | Always current |
| Fits | Marketing pages, blog posts, product listings | Shopping carts, account pages, anything genuinely personalized |

This directly parallels the [server state vs. client state](../../react/server-state-and-api-integration/data-fetching-patterns.md)
distinction from the React domain — content that's fundamentally the same for everyone fits
static generation; content that's genuinely tied to a specific request or user needs SSR.

## Streaming: Not All-or-Nothing

Server-side rendering doesn't have to mean the entire page waits on the slowest piece of data —
wrapping a slow section in `<Suspense>` (from
[code-splitting.md](../../react/performance-optimization-in-react/code-splitting.md), applied
here to data rather than lazy-loaded components) lets Next.js stream the rest of the page
immediately while that specific section loads in, improving perceived performance without giving
up SSR's freshness guarantee.

## Common Mistakes

- Reaching for server-side rendering by default for every page, giving up static generation's
  speed benefit for content that was never actually personalized or time-sensitive to begin with.
- Forgetting `cache: "no-store"` (or an equivalent dynamic API like reading cookies) on a fetch that
  genuinely needs fresh, per-request data — Next.js may otherwise cache it more aggressively than
  intended.
- Not using `<Suspense>` to stream slow sections, making an entire page wait on its single slowest
  piece of data instead of showing the rest immediately.

## Next

Continue to
[incremental-static-regeneration.md](incremental-static-regeneration.md) for a middle ground
between these two extremes.
