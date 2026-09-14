# Identifying Entry Points

## The App's Root Entry Point

```jsx
// A plain React (Vite/CRA-style) project
// src/main.jsx
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")).render(<App />);
```

```
# A Next.js App Router project
app/layout.tsx    ← the root layout every page renders inside
app/page.tsx      ← the entry point for the "/" route
```

An **entry point** is where execution genuinely begins — not necessarily the file you'll spend the
most time in, but the file that starts everything else. In a plain React project, that's typically
`main.jsx`/`main.tsx`, which mounts the root `<App />` component into the page. In a
[Next.js App Router](../../nextjs/app-router-deep-dive/) project, there's no single mount call to
find — the entry point is structural: `app/layout.tsx` (the root layout, per
[layouts.md](../../nextjs/app-router-deep-dive/layouts.md)) and the root `app/page.tsx`.

## `package.json`'s Scripts as a Map to Real Entry Points

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

Before hunting for an entry point manually, check `package.json`'s `scripts` — the `dev` script
often reveals the framework's own tooling (here, `next`), which tells you to look for that
framework's own conventional entry point structure, rather than searching blindly.

## A Feature's Entry Point, Not Just the App's

```
src/features/checkout/
├── CheckoutPage.jsx     ← where this specific feature starts
├── useCheckoutForm.js
└── CheckoutSummary.jsx
```

Once you're oriented at the app level, most real tasks are scoped to one feature, not the whole
app. The same question applies one level down: within the `checkout` feature, which file is the
one everything else in that folder is reached from? Usually it's the file matching the route or
page name (`CheckoutPage.jsx`) — start reading there, then follow its imports outward rather than
reading every file in the folder in an arbitrary order.

## Following Routes to Their Rendered Components

```
app/products/[id]/page.tsx
```

In a file-based router (per
[dynamic-routes.md](../../nextjs/app-router-deep-dive/dynamic-routes.md)), the URL structure itself
is a map: knowing the route a bug was reported on (`/products/42`) tells you exactly which file to
open first, without needing to search the codebase at all.

## Common Mistakes

- Opening a deeply nested component first and trying to work "upward" to understand context, when
  starting from the actual entry point and reading "downward" through its real dependency chain is
  almost always faster.
- Assuming a single `index.js`/`main.js` file must exist as the entry point, even in frameworks
  (like Next.js) where the entry point is a structural file-based convention, not a single mount
  call.
- Ignoring what a route's URL already tells you about which file to open, in a codebase that uses
  file-based routing.

## Next

Continue to [tracing-data-flow.md](tracing-data-flow.md) to follow how a piece of data actually
moves through a feature, starting from an entry point you can now find.
