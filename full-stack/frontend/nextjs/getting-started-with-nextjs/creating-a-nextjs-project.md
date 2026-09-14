# Creating a Next.js Project

## Using `create-next-app`

```bash
npx create-next-app@latest my-app
cd my-app
npm run dev
```

This mirrors the same scaffolding pattern from
[setting-up-a-react-project.md](../../react/introduction-to-react/setting-up-a-react-project.md) —
`create-next-app` is Next.js's equivalent of `npm create vite@latest`, generating a complete,
working project with sensible defaults.

## The Setup Prompts

```text
Would you like to use TypeScript?           Yes (recommended default)
Which linter would you like to use?         ESLint
Would you like to use Tailwind CSS?         Yes/No — see the Tailwind module in the CSS domain
Would you like your code inside a src/ directory?  Yes/No
Would you like to use App Router? (recommended)     Yes
```

The recommended defaults enable TypeScript (from the
[TypeScript domain](../../../typescript/typescript-essentials/)), ESLint, and the **App Router** —
the modern, currently-recommended routing system covered throughout this domain (an older "Pages
Router" exists in legacy Next.js projects, but the App Router is the standard choice for new
projects today).

## Running the Development Server

```bash
npm run dev
```

Starts a local development server (using Turbopack, Next.js's default bundler) at
`http://localhost:3000`, with the same hot-reloading behavior introduced for Vite in
[setting-up-a-react-project.md](../../react/introduction-to-react/setting-up-a-react-project.md) —
editing a file updates the running app automatically, without a manual refresh.

## Other Generated Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint"
  }
}
```

| Script | Purpose |
|---|---|
| `next dev` | Local development server with hot reloading |
| `next build` | Produces an optimized production build |
| `next start` | Runs that production build (used for actual deployment, not local development) |
| `eslint` | Runs the linter, per [setting-up-your-code-editor.md](../../foundations/preparing-your-machine/setting-up-your-code-editor.md) |

## Common Mistakes

- Running `next start` without first running `next build` — `start` runs a *production build* that
  must already exist; it doesn't build the app itself.
- Choosing the older Pages Router for a brand-new project out of familiarity with older tutorials,
  rather than the currently-recommended App Router covered throughout this domain.
- Confusing `next dev`'s local development server with a genuine production deployment — `next dev`
  includes development-only conveniences (detailed error overlays, unoptimized builds) never meant
  for production traffic.

## Next

Continue to [project-structure.md](project-structure.md) to understand what was actually
generated.
