# ⏳ Suspense Deep Dive

## Declarative Loading States, at the Component Level

```jsx
<Suspense fallback={<Loading />}>
  <Comments commentsPromise={commentsPromise} />
</Suspense>
```

`<Suspense>` lets a component "wait" for something — data still loading, a lazily-loaded component
still downloading — showing its `fallback` in the meantime, then automatically swapping in the real
content once ready. This directly replaces the manual `isLoading` state and conditional rendering
pattern already familiar from
[loading-and-error-states.md](../server-state-and-api-integration/loading-and-error-states.md),
expressing the same intent declaratively instead of imperatively tracking a boolean.

## What Actually Triggers Suspense

A `<Suspense>` boundary reacts specifically to:

- Reading a Promise with the [`use()` hook](the-use-hook.md), including data coming from a
  [Server Component](server-components-vs-client-components.md).
- Lazily loading a component with `lazy()`.
- Streaming server rendering, waiting for HTML to arrive.

Crucially, Suspense does **not** detect data fetched inside a `useEffect` or an event handler — only
data read directly during render (via `use()`) actually suspends a boundary. This is a real,
easy-to-miss distinction: converting an existing `useEffect`-based fetch to work with Suspense
requires actually reading the data through `use()`, not just wrapping the component in `<Suspense>`
and hoping.

## Nested Boundaries — Progressive Loading

```jsx
<Suspense fallback={<BigSpinner />}>
  <Biography />
  <Suspense fallback={<AlbumsGlimmer />}>
    <Albums />
  </Suspense>
</Suspense>
```

Nesting `<Suspense>` boundaries creates a **progressive** loading sequence: `BigSpinner` shows until
`Biography` is ready; once `Biography` appears, `AlbumsGlimmer` shows specifically for `Albums`
while `Biography` itself stays visible. This lets a page reveal content in the order it's actually
ready, rather than blocking the entire page behind the single slowest piece of data.

## Avoiding a Jarring Flash Back to the Fallback

```jsx
function navigate(url) {
  startTransition(() => {
    setPage(url);
  });
}
```

Wrapping a state update that triggers new suspended content inside `startTransition()` (already
introduced conceptually in
[performance-optimization-in-react.md](../performance-optimization-in-react/)) tells React to keep
the *currently visible* content on screen until the new content is actually ready, rather than
immediately reverting to the fallback and creating a jarring flash.

## Common Mistakes

- Wrapping a component in `<Suspense>` while it still fetches data inside a `useEffect` — the
  boundary never actually triggers, since Suspense only reacts to data read via `use()` during
  render.
- Nesting Suspense boundaries in a way that doesn't reflect the page's real, meaningful loading
  priority — nesting should mirror which content genuinely should appear first.
- Forgetting `startTransition` when navigating to newly-suspended content, causing an
  unnecessarily jarring flash back to a fallback for content that was already visible.

## ➡️ Next

Continue to
[server-components-vs-client-components.md](server-components-vs-client-components.md) to see the
architectural model Suspense is built to support.
