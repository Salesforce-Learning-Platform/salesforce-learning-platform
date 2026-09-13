# Setting Up a React Project

## Using Vite

**Vite** is the current standard tool for starting a new React project — a fast build tool and
development server, replacing older tools like Create React App (no longer actively recommended).

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

This scaffolds a complete, working React + TypeScript project (see `react-ts`; a plain `react`
template is also available for JavaScript-only projects, though TypeScript is the more common
modern default — see [TypeScript Essentials](../../typescript/typescript-essentials/)), installs
its dependencies (per
[installing-a-package-manager-and-node.md](../../foundations/preparing-your-machine/installing-a-package-manager-and-node.md)),
and starts a local development server with hot module reloading.

## What `npm run dev` Actually Does

This runs the `dev` script defined in the project's `package.json` (see
[installing-a-package-manager-and-node.md](../../foundations/preparing-your-machine/installing-a-package-manager-and-node.md)
for how npm scripts work) — starting Vite's development server, which serves the application
locally and automatically updates the browser as source files change, without a full page reload
in most cases.

## Choosing Next.js Instead

For applications needing server-side rendering, file-based routing, or built-in API routes,
**Next.js** (covered in its own domain later in this platform) provides a more complete,
opinionated framework built on top of React. Vite is the better starting point for learning React
itself, and for projects that are genuinely client-side single-page applications without those
additional needs.

## Common Mistakes

- Using older tutorials that reference Create React App (`npx create-react-app`) — it's no longer
  the recommended starting point; Vite (or a framework like Next.js) is the current standard.
- Running `npm run dev` from the wrong directory (outside the actual project folder), producing a
  confusing "script not found" error — a direct instance of the mistake flagged in
  [terminal-and-command-line-basics.md](../../foundations/preparing-your-machine/terminal-and-command-line-basics.md).
- Choosing Next.js for a simple project that doesn't need server-side rendering or file-based
  routing, adding unnecessary framework overhead for no actual benefit.

## Next

Continue to [react-project-structure.md](react-project-structure.md) to understand what Vite
actually generated.
