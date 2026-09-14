# Server Components

## The App Router's Default

This is the single biggest mental-model shift from plain React: in the Next.js App Router, **every
component is a Server Component by default** — it runs only on the server, never shipped to the
browser as JavaScript at all, unless explicitly marked otherwise (covered next in
[client-components.md](client-components.md)).

```tsx
// app/products/[slug]/page.tsx — a Server Component (the default, no directive needed)
async function getProduct(slug: string) {
  const res = await fetch(`https://api.example.com/products/${slug}`);
  return res.json();
}

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await getProduct(slug);
  return (
    <div>
      <h1>{product.name}</h1>
      <p>${product.price}</p>
    </div>
  );
}
```

Notice this component's function is `async` and directly `await`s a fetch — something a plain
React component (from the [React domain](../../react/)) could never do; a regular React component
function can't be `async`. Server Components genuinely change what's possible in a component
function, precisely because they run in a Node.js environment on the server, not in the browser.

## Why This Is Genuinely Useful

- **Fetch data directly, closer to its source** — no `useEffect`/loading-state dance from
  [fetching-data.md](../../react/server-state-and-api-integration/fetching-data.md) is needed;
  the component just `await`s the data before rendering.
- **Keep secrets on the server** — an API key used inside a Server Component's fetch call never
  reaches the browser bundle at all, a stronger guarantee than the `NEXT_PUBLIC_` convention from
  [nextjs-configuration.md](../getting-started-with-nextjs/nextjs-configuration.md), since the
  component's code itself never ships to the client.
- **Reduce JavaScript sent to the browser** — a Server Component's rendered output becomes part of
  the page's HTML; its own code is never included in the client-side JavaScript bundle at all.

## Server Components Cannot Use Browser-Only Features

```tsx
// This will NOT work in a Server Component:
export default function Widget() {
  const [count, setCount] = useState(0); // Error — useState needs a Client Component
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

Because Server Components run only on the server, they have no access to `useState`, `useEffect`,
event handlers like `onClick`, or any browser API (`window`, `localStorage`) — none of these make
sense in an environment with no actual browser present. Anything requiring interactivity or
browser APIs needs a Client Component instead, covered next.

## Common Mistakes

- Trying to use `useState`/`useEffect`/`onClick` in a Server Component, hitting a build error —
  these require `"use client"`, covered in [client-components.md](client-components.md).
- Assuming Server Components are a completely new, unfamiliar way of writing React — the JSX and
  component structure are identical to what's covered throughout the [React domain](../../react/);
  what's different is *where* the component executes and what capabilities that implies.
- Forgetting that a Server Component's fetch calls run on the server, meaning any URL used there
  (an internal API, a database connection) doesn't need to be reachable from the public internet
  the way a client-side fetch would.

## Next

Continue to [client-components.md](client-components.md) for opting into browser-side
interactivity where it's actually needed.
