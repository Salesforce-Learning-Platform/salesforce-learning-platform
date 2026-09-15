# 🔗 The use() Hook

## Reading a Promise Directly During Render

```jsx
import { use, Suspense } from "react";

function Comments({ commentsPromise }) {
  const comments = use(commentsPromise); // suspends until the promise resolves
  return comments.map((comment) => <p key={comment.id}>{comment}</p>);
}

function Page({ commentsPromise }) {
  return (
    <Suspense fallback={<div>Loading comments…</div>}>
      <Comments commentsPromise={commentsPromise} />
    </Suspense>
  );
}
```

`use(promise)` reads a promise's eventual value directly during render — if the promise hasn't
resolved yet, the component **suspends**, and the nearest
[`<Suspense>` boundary](suspense-deep-dive.md) shows its fallback until it does. This is the actual
mechanism underneath Suspense's promise-based triggering already introduced in
[suspense-deep-dive.md](suspense-deep-dive.md) — `use()` is how a component actually hands React a
promise to wait on.

## `use()` Is Not a Regular Hook — It Can Be Called Conditionally

```jsx
function Heading({ children }) {
  if (children == null) {
    return null; // an early return BEFORE the hook call
  }
  const theme = use(ThemeContext); // reading context AFTER a conditional return
  return <h1 style={{ color: theme.color }}>{children}</h1>;
}
```

Every other hook (`useState`, `useEffect`) must be called unconditionally, at the top of a
component, per [the rules of hooks](../react-hooks/) — calling one conditionally or after an
early return is a real, well-known bug. `use()` is a deliberate, explicit exception: it **can** be
called conditionally or after an early return, specifically because of how it's designed to
integrate with control flow.

## Reading Context With `use()`

```jsx
const theme = use(ThemeContext);
```

`use()` can also read a [Context](../global-state-management/) value directly, working exactly
like the existing `useContext(ThemeContext)` — but, per the point above, usable conditionally in a
way `useContext` itself never could be.

## Why the Promise Must Be Cached, Not Recreated Every Render

```jsx
// WRONG — a NEW promise is created on every single render, so `use()`
// suspends forever, never actually settling on a stable value
function Albums({ artistId }) {
  const albums = use(fetchAlbums(artistId)); // fetchAlbums() called fresh, every render
}
```

`use()` needs to read the **same** promise instance across re-renders to work correctly — a promise
freshly created on every render never lets React "remember" that it already started waiting on it.
In practice, the promise passed to `use()` is typically created once, further up the tree (often in
a Server Component, or from a caching layer a framework provides), and passed down as a stable
prop — not created fresh inside the component that calls `use()` itself.

## Common Mistakes

- Creating a new promise on every render and passing it to `use()`, causing the component to
  suspend indefinitely instead of ever settling.
- Assuming `use()` is interchangeable with `useState`/`useEffect` for every data-fetching case —
  it specifically requires a promise (or context) and Suspense integration, not a general-purpose
  replacement for existing patterns.
- Forgetting that `use()`'s ability to be called conditionally is a deliberate, unique exception —
  applying that same conditional-calling pattern to `useState` or `useEffect` remains a real bug.

## ➡️ Next

Continue to [react-compiler-introduction.md](react-compiler-introduction.md) to see where React is
heading next: automating away manual memoization entirely.
