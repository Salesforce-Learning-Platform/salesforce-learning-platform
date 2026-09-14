# Understanding Project Structure

## Start From the Outside In

```
my-shop-app/
├── README.md               ← Start here
├── package.json             ← What does this project actually depend on?
├── src/
│   ├── app/                 ← Next.js App Router routes (or pages/, for other setups)
│   ├── components/          ← Shared, reusable UI
│   ├── features/            ← Feature-specific code, grouped by domain
│   ├── lib/                 ← Shared utilities, API clients
│   └── styles/
└── tests/
```

Before reading any single file's logic in detail, build a rough mental map of *where things live*.
The fastest way in is almost never "open a random component" — it's the project's own
self-description: the `README.md`, and `package.json`'s `dependencies` (which frameworks and
libraries is this actually built on?) and `scripts` (how is it run, built, and tested?).

## Read the README First — Even a Stale One

A project's README is written by people who already have the mental map you're trying to build.
Even an outdated README (a common reality on real projects) usually still gets the broad strokes
right — which framework, roughly how things are organized — and is worth the five minutes it takes
to read before touching any code.

## Recognize the Framework's Own Conventions

```
# A Next.js App Router project signals its own structure:
app/products/[id]/page.tsx   → the file-based route for /products/:id
app/layout.tsx               → the root layout wrapping every page
```

Every framework in this platform imposes its own predictable folder conventions —
[Next.js App Router's file-based routing](../../nextjs/getting-started-with-nextjs/) or
[React's typical component/feature organization](../../react/component-architecture-and-composition/).
Recognizing *which* convention a project follows immediately tells you where to look for a given
piece of functionality, without needing to read the whole codebase first.

## Look for a Grouping Pattern: By Type or By Feature

```
# Grouped by TYPE — everything of one kind lives together
src/components/Button.jsx
src/components/ProductCard.jsx
src/hooks/useCart.js
src/hooks/useAuth.js

# Grouped by FEATURE — everything for one feature lives together
src/features/cart/CartList.jsx
src/features/cart/useCart.js
src/features/auth/LoginForm.jsx
src/features/auth/useAuth.js
```

Most real projects group code either by *type* (all components together, all hooks together) or by
*feature* (everything related to "cart" lives in one folder, regardless of type). Identifying which
pattern a project uses tells you exactly where to look for anything related to a given feature —
and, just as importantly, where a new file you add should go to match the existing convention.

## Common Mistakes

- Diving straight into a specific component's logic before having any sense of the project's
  overall shape — leading to a change that technically works but doesn't fit the codebase's
  existing conventions.
- Assuming a project follows the "textbook" structure for its framework without checking — real
  projects frequently deviate, and trusting an assumption over five minutes of actual verification
  wastes far more time later.
- Ignoring `package.json` — it's often the fastest way to learn a project's real technology stack,
  faster than inferring it from file extensions alone.

## Next

Continue to [identifying-entry-points.md](identifying-entry-points.md) to find exactly where
execution — and the UI itself — actually begins.
