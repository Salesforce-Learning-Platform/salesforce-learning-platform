# Nested Routes

## The Problem: Shared Layout Between Related Pages

Many related pages share the same surrounding layout — a dashboard's sidebar and header stay the
same across `/dashboard/overview`, `/dashboard/settings`, and `/dashboard/billing`, with only the
inner content actually changing. Defining each as a fully separate top-level route would mean
duplicating that shared layout in every single one.

## Nesting Routes

```jsx
<Routes>
  <Route path="/dashboard" element={<DashboardLayout />}>
    <Route index element={<Overview />} />       {/* matches exactly /dashboard */}
    <Route path="settings" element={<Settings />} /> {/* matches /dashboard/settings */}
    <Route path="billing" element={<Billing />} />    {/* matches /dashboard/billing */}
  </Route>
</Routes>
```

Child routes' paths are automatically appended to their parent's — `path="settings"` nested under
`path="/dashboard"` matches `/dashboard/settings`, without needing to repeat the full path.

## Rendering the Matched Child with `<Outlet>`

```jsx
import { Outlet } from "react-router";

function DashboardLayout() {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>
        <Outlet /> {/* the matching child route renders here */}
      </main>
    </div>
  );
}
```

`DashboardLayout` renders the shared `Sidebar` once, and `<Outlet>` is a placeholder marking
exactly where the currently-matched child route (`Overview`, `Settings`, or `Billing`) should
render — this is the composition pattern from
[component-composition.md](../component-architecture-and-composition/component-composition.md),
applied specifically to routing.

## The `index` Route

```jsx
<Route path="/dashboard" element={<DashboardLayout />}>
  <Route index element={<Overview />} /> {/* the DEFAULT child, for exactly "/dashboard" */}
  <Route path="settings" element={<Settings />} />
</Route>
```

An `index` route (no `path` of its own) renders when the parent's path is matched exactly, with no
additional segment — the equivalent of a "default page" for that section, similar in spirit to how
a bare directory URL often serves an `index.html` by default in traditional multi-page sites.

## Common Mistakes

- Duplicating shared layout markup across multiple top-level routes instead of nesting them under
  one shared layout route with `<Outlet>`.
- Forgetting `<Outlet>` in the parent layout component — without it, child routes match correctly
  but have nowhere to actually render, silently showing nothing.
- Confusing an `index` route with a route that has `path=""` — `index` is the correct, explicit way
  to express "the default child," rather than an empty-string path.

## Module Summary

Across this module: client-side routing exists because a single-page app has only one real HTML
file, and React Router intercepts navigation to avoid full page reloads while still needing a
server-side fallback for direct visits/refreshes (see
[react-router-introduction.md](react-router-introduction.md)); routes map URL paths to components,
navigated via `Link`/`NavLink` or programmatically via `useNavigate` (see
[routes-and-navigation.md](routes-and-navigation.md)); dynamic segments captured with `useParams`
are always strings and should be included in any dependent effect's dependency array (see
[route-parameters.md](route-parameters.md)); and nested routes with `<Outlet>` let related pages
share layout without duplication.
