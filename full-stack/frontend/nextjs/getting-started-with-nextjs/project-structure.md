# Project Structure

## The Generated Layout

```text
my-app/
├── app/
│   ├── layout.tsx      # the root layout — required, wraps every page
│   ├── page.tsx          # the home page, rendered at "/"
│   └── globals.css
├── public/               # static assets, served from the root path
├── next.config.js          # Next.js configuration (see nextjs-configuration.md)
├── package.json
└── tsconfig.json
```

## File-System Routing: The Core Idea

Unlike React Router (from
[routes-and-navigation.md](../../react/client-side-routing/routes-and-navigation.md)), which
defines routes explicitly with `<Route>` components, the **App Router** determines an
application's routes directly from the folder structure inside `app`:

```text
app/
├── page.tsx              → "/"
├── about/
│   └── page.tsx            → "/about"
└── products/
    ├── page.tsx              → "/products"
    └── [id]/
        └── page.tsx            → "/products/:id" (a dynamic segment, like React Router's :id)
```

A folder becomes a URL segment; a `page.tsx` file inside it makes that segment an actual,
navigable route. This is covered in full depth in the App Router Deep Dive module later in this
domain — this file establishes just the core mental model.

## `layout.tsx` — The Required Root Layout

```tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

Every Next.js App Router project requires a root `layout.tsx`, which must contain the `<html>` and
`<body>` tags — this replaces the single, mostly-empty `index.html` from a plain Vite React
project (see
[react-project-structure.md](../../react/introduction-to-react/react-project-structure.md)); in a
Next.js app, the root layout *is* the equivalent top-level HTML shell, just expressed as a React
component instead of a static file. `{children}` renders whichever page currently matches the
URL — directly the same composition pattern as React Router's `<Outlet>` from
[nested-routes.md](../../react/client-side-routing/nested-routes.md).

## `public/` for Static Assets

Files placed in `public/` (images, fonts) are served directly from the site's root path —
`public/logo.png` is reachable at `/logo.png`. This is Next.js's own convention for static assets
that need no processing, handled automatically in both development and production.

## Common Mistakes

- Deleting or significantly restructuring the required root `layout.tsx`, breaking every route in
  the application since it's the mandatory top-level wrapper.
- Assuming routes need to be manually registered somewhere (a routes config file) — in the App
  Router, the folder structure itself *is* the routing configuration.
- Placing files needing server-side processing (rather than being served as-is) inside `public/`,
  where they're served completely statically with no processing at all.

## Next

Continue to [nextjs-configuration.md](nextjs-configuration.md) for the project's main
configuration file.
