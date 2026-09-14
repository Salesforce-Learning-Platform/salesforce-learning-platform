# Next.js Configuration

## `next.config.js`

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [{ hostname: "example-cdn.com" }],
  },
};

module.exports = nextConfig;
```

`next.config.js` (or `.ts`, if the project uses TypeScript for configuration files too) is the
central place to customize Next.js's built-in behavior — image optimization domains, redirects,
custom headers, and various build-time options. Unlike `vite.config.ts` from
[setting-up-a-react-project.md](../../react/introduction-to-react/setting-up-a-react-project.md),
which configures a general-purpose build tool, `next.config.js` configures Next.js's own
opinionated, framework-specific behavior.

## Common Configuration Needs

| Setting | Purpose |
|---|---|
| `images.remotePatterns` | Allow-lists external domains Next.js's built-in image optimization is permitted to fetch from |
| `redirects()` | Server-level URL redirects, configured centrally rather than per-page |
| `headers()` | Custom HTTP response headers — directly related to [http-headers-in-depth.md](../../foundations/understanding-http-and-https/http-headers-in-depth.md) |
| `env` | Exposing specific environment variables to the browser bundle |

## Environment Variables

```bash
# .env.local
DATABASE_URL=postgres://...
NEXT_PUBLIC_API_URL=https://api.example.com
```

Next.js has a specific, important convention: only environment variables prefixed with
`NEXT_PUBLIC_` are ever included in the browser-side JavaScript bundle — anything without that
prefix stays server-only. This is a genuine security boundary, not just a naming convention: a
database connection string or an API secret key must **never** be prefixed with `NEXT_PUBLIC_`,
since doing so would ship it directly to every visitor's browser, fully readable in the compiled
JavaScript — a direct real-world instance of the "never trust or expose secrets to the client"
principle from
[frontend-and-backend-responsibilities.md](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md).

## Common Mistakes

- Accidentally prefixing a genuinely secret value with `NEXT_PUBLIC_`, shipping it directly to
  every visitor's browser.
- Confusing `next.config.js` (Next.js framework configuration) with `.env`/`.env.local`
  (environment-specific values) — they serve different, complementary purposes.
- Forgetting that `next.config.js` changes require restarting the development server to take
  effect, unlike most source file changes, which hot-reload automatically.

## Module Summary

Across this module: Next.js is a framework built on React, adding routing, server-side rendering,
and integrated build tooling that plain React doesn't provide on its own (see
[what-is-nextjs.md](what-is-nextjs.md)); `create-next-app` scaffolds a new project with the App
Router as the modern, recommended default (see
[creating-a-nextjs-project.md](creating-a-nextjs-project.md)); the `app` directory's folder
structure directly determines the application's routes, with a required root `layout.tsx`
replacing plain React's single `index.html` (see [project-structure.md](project-structure.md));
and `next.config.js` configures framework-specific behavior, with the `NEXT_PUBLIC_` prefix
convention forming a genuine, security-relevant boundary between server-only and browser-exposed
environment variables.
