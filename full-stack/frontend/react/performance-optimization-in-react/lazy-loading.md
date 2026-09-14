# Lazy Loading in Practice

## The Most Common Case: Route-Based Code Splitting

Combining [code-splitting.md](code-splitting.md) with routing from
[routes-and-navigation.md](../client-side-routing/routes-and-navigation.md), applied to a
realistic admin dashboard:

```jsx
import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router";

const Overview = lazy(() => import("./pages/Overview"));
const Reports = lazy(() => import("./pages/Reports")); // includes a heavy charting library
const AdminSettings = lazy(() => import("./pages/AdminSettings")); // most users never visit

function App() {
  return (
    <Suspense fallback={<p>Loading page...</p>}>
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/admin" element={<AdminSettings />} />
      </Routes>
    </Suspense>
  );
}
```

A visitor loading `/` only downloads `Overview`'s code — `Reports`'s heavy charting library and
`AdminSettings`'s admin-only code are fetched only if and when that specific route is actually
visited. This is the single most common, highest-value application of code splitting in a real
application: most users don't visit every route, so there's no reason to make everyone download
every route's code upfront.

## Lazy Loading a Heavy, Conditionally-Shown Component

```jsx
const ImageEditor = lazy(() => import("./ImageEditor")); // a large, rarely-used component

function ProductForm() {
  const [showEditor, setShowEditor] = useState(false);

  return (
    <div>
      <button onClick={() => setShowEditor(true)}>Edit Image</button>
      {showEditor && (
        <Suspense fallback={<p>Loading editor...</p>}>
          <ImageEditor />
        </Suspense>
      )}
    </div>
  );
}
```

A heavy component only shown behind a specific user action (opening an image editor) benefits from
the exact same pattern — its code is fetched only once a user actually clicks the button, not
included in the page's initial load at all.

## Placing `Suspense` Boundaries Deliberately

```jsx
// One large boundary — the whole page shows a spinner while ANY part loads
<Suspense fallback={<PageSpinner />}>
  <Header />
  <Sidebar />
  <MainContent />
</Suspense>

// Multiple smaller boundaries — each section loads/shows independently
<Header />
<Suspense fallback={<SidebarSkeleton />}><Sidebar /></Suspense>
<Suspense fallback={<ContentSkeleton />}><MainContent /></Suspense>
```

A single large `Suspense` boundary is simpler but means the entire wrapped section waits for the
*slowest* lazy component inside it; multiple smaller boundaries let independent sections load and
appear separately — a genuine UX tradeoff, not a strict rule, to decide deliberately per section
rather than defaulting to one pattern everywhere without thinking about it.

## Common Mistakes

- Applying `lazy()` to every single component in an application uniformly, rather than targeting
  it specifically at genuinely large, infrequently-needed code (whole routes, heavy
  conditionally-shown features).
- Using one giant `Suspense` boundary around an entire page when independent, differently-timed
  loading states for different sections would give a better perceived-performance experience.
- Lazy-loading something small enough that the overhead of a separate network request exceeds any
  actual bundle-size benefit.

## Next

Continue to [react-profiler.md](react-profiler.md) to actually measure whether any of this is
solving a real, existing problem before applying it.
