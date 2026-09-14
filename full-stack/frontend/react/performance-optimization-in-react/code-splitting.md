# Code Splitting

## The Problem: One Giant Bundle

By default, a build tool (like Vite, from
[setting-up-a-react-project.md](../introduction-to-react/setting-up-a-react-project.md)) bundles
an entire application's JavaScript into one file — including an admin-only settings panel that
99% of visitors will never open, and a heavy charting library used on only one rarely-visited
report page. Every visitor downloads all of it before the app can even start, regardless of which
parts they'll actually use.

## `lazy()` and `Suspense`

```jsx
import { lazy, Suspense } from "react";

const AdminPanel = lazy(() => import("./AdminPanel"));

function App() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <AdminPanel />
    </Suspense>
  );
}
```

`lazy(() => import("./AdminPanel"))` tells the build tool to put `AdminPanel`'s code in its own
separate file, fetched only when it's actually needed — not included in the initial bundle at all.
`<Suspense fallback={...}>` provides the UI shown while that separate file is being fetched, the
first time `AdminPanel` is actually rendered.

## Why It Must Be Declared at Module Scope

```jsx
// WRONG — creates a new lazy component on every render, resetting its state each time
function Dashboard() {
  const AdminPanel = lazy(() => import("./AdminPanel"));
  return <AdminPanel />;
}

// CORRECT — declared once, at module top level
const AdminPanel = lazy(() => import("./AdminPanel"));
function Dashboard() {
  return <AdminPanel />;
}
```

This is explicitly warned against in React's own documentation: declaring `lazy()` inside a
component function creates a *new* lazy-loaded component reference on every single render — React
treats it as an entirely different component each time, discarding and re-mounting it (see
[component-lifecycle.md](../react-lifecycle-and-useeffect/component-lifecycle.md)) instead of
reusing the one already loaded.

## What Actually Happens on the Network

The first time `<AdminPanel />` renders, the browser fetches the separate chunk file over the
network — exactly the request/response cycle from
[what-happens-when-you-enter-a-url.md](../../foundations/how-the-internet-works/what-happens-when-you-enter-a-url.md),
just triggered by React rendering rather than an initial page navigation. Once fetched, React
caches both the loading promise and the resolved component — a second render of the same
`AdminPanel` reference doesn't refetch it.

## Common Mistakes

- Declaring a `lazy()` component inside another component's function body, causing it to reload
  and reset on every parent re-render instead of once.
- Forgetting the `<Suspense>` boundary entirely — a `lazy` component with no ancestor `Suspense`
  throws an error rather than rendering a loading state.
- Code-splitting something genuinely needed immediately on first load (like the main navigation),
  which just adds an unnecessary extra network round trip for something users always need right
  away.

## Next

Continue to [lazy-loading.md](lazy-loading.md) to apply this specifically to routes and
conditionally-shown heavy UI.
