# App Router Deep Dive

## Purpose

[project-structure.md](../getting-started-with-nextjs/project-structure.md) introduced file-system
routing briefly. This module goes deep: the full set of special files the App Router recognizes,
nested layouts, dynamic segments, loading/error UI, and the Metadata API for SEO. Every example
continues the same e-commerce store used throughout this domain.

## Learning Objectives

- Use `page.tsx` and `layout.tsx` to build nested routes with shared, non-re-rendering layout UI.
- Create dynamic route segments and read their values.
- Provide automatic loading and error UI for a route segment.
- Add per-route metadata for SEO using both static and dynamic approaches.

## Prerequisites

[Next.js Rendering Strategies](../rendering-strategies/).

## Files in This Module

| File | Covers |
|---|---|
| [file-based-routing.md](file-based-routing.md) | The special files the App Router recognizes, and what each does |
| [pages-and-nested-routes.md](pages-and-nested-routes.md) | Building `/products`, `/products/electronics`, etc. |
| [dynamic-routes.md](dynamic-routes.md) | `[slug]` segments for pages generated from data |
| [layouts.md](layouts.md) | Shared UI that persists and doesn't re-render across navigation |
| [loading-and-error-ui.md](loading-and-error-ui.md) | `loading.tsx` and `error.tsx` — automatic Suspense and error boundaries |
| [metadata-api-and-seo.md](metadata-api-and-seo.md) | Static and dynamic per-route `<head>` metadata |

## When to Deep-Dive vs. Skim

Deep-dive [layouts.md](layouts.md)'s explanation of why layouts don't re-render on navigation —
this is a genuine, useful behavior difference from a plain React Router layout (from
[nested-routes.md](../../react/client-side-routing/nested-routes.md)) that affects where you put
state and side effects in a real Next.js application.

## Quick Knowledge Check

<details>
<summary>Does a shared layout's component function re-run every time you navigate between pages that use it?</summary>

No — this is a deliberate App Router optimization: layouts persist across navigations within their
segment, preserving their own state and avoiding unnecessary re-renders, unlike a full page reload
or even a React Router layout being fully re-evaluated. See [layouts.md](layouts.md).

</details>

<details>
<summary>What file would you add to automatically show a loading spinner while a slow Server Component's data fetch resolves?</summary>

`loading.tsx` in the same route segment — the App Router automatically wraps the segment in a
`Suspense` boundary using it as the fallback, with no manual `<Suspense>` JSX required. See
[loading-and-error-ui.md](loading-and-error-ui.md).

</details>

## References

- Next.js, [Layouts and Pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages)
- Next.js, [Metadata and OG Images](https://nextjs.org/docs/app/getting-started/metadata-and-og-images)

## Continue Your Learning Path

Next: [Building APIs with Next.js](../building-apis-with-nextjs/) — see the
[Frontend learning path](../../README.md) for the full sequence.
