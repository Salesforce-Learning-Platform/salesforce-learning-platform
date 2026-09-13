# React Project Structure

## What Vite Generates

A typical Vite + React project's key files and folders:

```text
my-app/
├── index.html          # the single real HTML file — the app's entry point
├── src/
│   ├── main.tsx          # bootstraps React into the page
│   ├── App.tsx             # the root component
│   └── App.css               # component-scoped or global styles
├── package.json               # dependencies and npm scripts
├── vite.config.ts               # Vite's own configuration
└── tsconfig.json                  # TypeScript configuration (for a TypeScript template)
```

## `index.html` — Just One Element Matters

```html
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.tsx"></script>
</body>
```

Unlike the multi-page HTML applications covered in the [HTML domain](../../html/), a React
single-page application's `index.html` is nearly empty — just one `<div id="root">`, which React
takes over entirely. Every visible piece of UI is subsequently rendered by React into that single
div.

## `main.tsx` — Where React Actually Starts

```tsx
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")!).render(<App />);
```

This is the bridge between the DOM (from
[dom-introduction.md](../../javascript/dom-manipulation/dom-introduction.md)) and React:
`createRoot` takes over the `#root` element, and `.render(<App />)` tells React to render the root
`App` component — and everything it in turn renders — inside it.

## `App.tsx` — The Root Component

Every other component in the application is, directly or indirectly, rendered from `App` — it's
the top of the component tree introduced in [what-is-react.md](what-is-react.md).

## Common Mistakes

- Trying to add significant static HTML content directly to `index.html`, when almost everything
  should be expressed as React components rendered into the single root element instead.
- Confusing Vite's own configuration (`vite.config.ts`) with the application's actual logic — it
  controls the build tool's behavior, not the app itself.
- Expecting a multi-page-style file structure (a separate `.html` file per page) — a single-page
  React application typically has one `index.html`, with different "pages" handled by client-side
  routing (covered in its own module later in this domain) rather than separate HTML files.

## Module Summary

Across this module: React organizes UI into reusable components and follows a declarative "UI as a
function of state" model, rather than imperative DOM manipulation (see
[what-is-react.md](what-is-react.md)); this solves real, growing difficulty in manually
synchronizing complex, interdependent UI state, though it comes with genuine tradeoffs and isn't
the right tool for every project (see [why-react.md](why-react.md)); Vite is the current standard
tool for starting a new React project (see
[setting-up-a-react-project.md](setting-up-a-react-project.md)); and a generated project's
structure centers on a nearly-empty `index.html`, a `main.tsx` bootstrap file, and an `App.tsx`
root component at the top of the entire component tree.
