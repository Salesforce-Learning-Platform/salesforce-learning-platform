# File-Based Routing

## Folders Define URL Segments, Special Files Define UI

As introduced in
[project-structure.md](../getting-started-with-nextjs/project-structure.md), a folder inside `app`
becomes a URL segment. What actually renders for that segment comes from a set of **special
files** the App Router recognizes by name:

| File | Purpose |
|---|---|
| `page.tsx` | The actual UI for this route — required to make a segment publicly reachable |
| `layout.tsx` | Shared UI wrapping this segment and its children (see [layouts.md](layouts.md)) |
| `loading.tsx` | Automatic loading UI (see [loading-and-error-ui.md](loading-and-error-ui.md)) |
| `error.tsx` | Automatic error boundary for this segment |
| `not-found.tsx` | Shown when `notFound()` is called or no route matches |

## A Folder Without `page.tsx` Isn't a Route

```text
app/
├── products/
│   ├── layout.tsx      # shared layout for everything under /products
│   └── page.tsx           # makes "/products" itself reachable
```

This is worth being precise about: a folder alone doesn't create a navigable page — only a
`page.tsx` inside it does. A folder can exist purely to hold a shared `layout.tsx` or group related
routes together, without being reachable as a URL itself, unless it also contains its own
`page.tsx`.

## Colocating Non-Route Files

```text
app/
├── products/
│   ├── page.tsx
│   ├── ProductCard.tsx    # a component used only by this route — safe to colocate
│   └── utils.ts
```

Only files with the specific recognized names (`page`, `layout`, `loading`, `error`, etc.) are
treated as routing files — any other file (a component, a utility function) can be placed directly
alongside them in the same folder with no special meaning, letting route-specific code live close
to the route that uses it, rather than in a separate, disconnected `components/` tree.

## Common Mistakes

- Expecting a folder to be reachable as a route just because it exists, without adding a
  `page.tsx` inside it.
- Naming a component file exactly `page.tsx`/`layout.tsx` when it isn't actually meant to be a
  route's UI — the App Router treats these names as reserved, routing-specific conventions.
- Assuming every file inside `app` is treated specially — only the specific recognized filenames
  are; everything else is an ordinary file you can organize however you like.

## Next

Continue to [pages-and-nested-routes.md](pages-and-nested-routes.md) to build out the store's
actual route structure.
