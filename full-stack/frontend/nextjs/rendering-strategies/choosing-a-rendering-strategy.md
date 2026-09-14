# Choosing a Rendering Strategy

## Two Independent Decisions

This module actually covers two separate, independent choices that combine on every page:

1. **When does it render?** — static generation, server-side rendering, or ISR (from
   [static-site-generation.md](static-site-generation.md),
   [server-side-rendering.md](server-side-rendering.md), and
   [incremental-static-regeneration.md](incremental-static-regeneration.md)).
2. **Where does each piece run?** — Server Component (default) or Client Component (from
   [server-components.md](server-components.md) and [client-components.md](client-components.md)).

A page can genuinely mix both dimensions — a statically-generated Server Component page containing
one small Client Component button, for instance.

## The Example Store, Page by Page

| Page | Rendering strategy | Why |
|---|---|---|
| `/about` (marketing) | Static generation | Identical for every visitor, rarely changes |
| `/products` (catalog) | ISR, `revalidate: 3600` | Changes a few times a day; fast responses matter more than instant freshness |
| `/products/[slug]` (product detail) | Static generation + `generateStaticParams` | Same content for every visitor; the "Add to Cart" button is a small Client Component within an otherwise static Server Component page |
| `/cart` | Server-side rendering | Genuinely different per visitor (their session's cart); must be fresh on every visit |
| `/account` | Server-side rendering | Personalized, needs the current user's session |

## A Decision Framework

**For "when does it render":**

- Is the content identical for every visitor and doesn't need to reflect this exact instant? →
  Static generation.
- Does content change periodically, where being a few minutes/hours stale is genuinely acceptable
  in exchange for speed? → ISR.
- Is content genuinely personalized, or must it reflect the literal current moment (a live cart, a
  logged-in session)? → Server-side rendering.

**For "where does it run":**

- Default to a Server Component — this is the App Router's actual default, and the right starting
  point for most content.
- Mark a component `"use client"` only for the specific piece that genuinely needs state, event
  handlers, browser APIs, or Context — not the whole containing page.

## Why This Matters More Than Memorizing APIs

The actual skill this module builds isn't memorizing `revalidate` syntax or the exact `"use
client"` rules — it's recognizing, for a real page, what its actual requirements are (freshness,
personalization, interactivity) and choosing the strategy that matches, exactly the same "match
the tool to the actual requirement" reasoning applied throughout this platform — to styling
approaches, state-management libraries, and now rendering strategies.

## Common Mistakes

- Choosing a rendering strategy for a new page reflexively (always SSR "to be safe," or always
  static "for speed") rather than reasoning from that specific page's actual freshness and
  personalization requirements.
- Marking large sections of a page as Client Components by default, rather than defaulting to
  Server Components and opting into client-side rendering only where genuinely needed.
- Treating this as a one-time, page-level decision rather than recognizing most real pages combine
  both dimensions — a statically-generated page with one small, interactive Client Component
  button is a completely normal, common pattern.

## Module Summary

Across this module: static generation pre-renders once at build time for maximum speed at the
cost of freshness (see [static-site-generation.md](static-site-generation.md)); server-side
rendering computes fresh HTML per request for genuinely personalized or time-sensitive content
(see [server-side-rendering.md](server-side-rendering.md)); ISR combines both, serving a fast
cached page while regenerating it in the background on a schedule or on-demand (see
[incremental-static-regeneration.md](incremental-static-regeneration.md)); Server Components are
the App Router's default, running only on the server with no browser-side JavaScript cost (see
[server-components.md](server-components.md)); Client Components opt into interactivity via
`"use client"`, ideally scoped to the smallest piece that actually needs it (see
[client-components.md](client-components.md)); and choosing correctly across both dimensions comes
from reasoning about a page's actual requirements, not applying one default everywhere.
