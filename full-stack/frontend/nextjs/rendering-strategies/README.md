# Next.js Rendering Strategies

## Purpose

[what-is-nextjs.md](../getting-started-with-nextjs/what-is-nextjs.md) introduced server-side
rendering conceptually. This module covers Next.js's actual rendering strategies — static
generation, server-side rendering, incremental static regeneration — and Server vs. Client
Components, the mechanism the App Router uses to let you choose per-component where code actually
runs. Every example uses one realistic site: an e-commerce store with a marketing homepage, a
product catalog, and a personalized cart.

## Learning Objectives

- Explain the difference between static generation, server-side rendering, and client-side
  rendering, and when each fits.
- Use Incremental Static Regeneration to keep static pages fresh without a full rebuild.
- Explain Server Components (the App Router default) and when a Client Component is genuinely
  needed.
- Choose the right rendering strategy for a given page's actual requirements.

## Prerequisites

[Getting Started with Next.js](../getting-started-with-nextjs/).

## Files in This Module

| File | Covers |
|---|---|
| [static-site-generation.md](static-site-generation.md) | Pre-rendering pages at build time |
| [server-side-rendering.md](server-side-rendering.md) | Rendering a page fresh on every request |
| [incremental-static-regeneration.md](incremental-static-regeneration.md) | Keeping static pages fresh via `revalidate` |
| [server-components.md](server-components.md) | The App Router's default — running React on the server |
| [client-components.md](client-components.md) | Opting into browser-side interactivity with `"use client"` |
| [choosing-a-rendering-strategy.md](choosing-a-rendering-strategy.md) | A practical decision framework across the whole site |

## When to Deep-Dive vs. Skim

Deep-dive [server-components.md](server-components.md) and
[client-components.md](client-components.md) together — this Server/Client Component split is the
single most important new mental model in the entire Next.js domain, genuinely different from
plain React (where every component is, in effect, a "client component"), and it affects how every
component you write in this framework is actually structured.

## Quick Knowledge Check

<details>
<summary>In the Next.js App Router, is a component a Server Component or a Client Component by default?</summary>

A Server Component — this is the App Router's default, a genuine change from plain React. A
component only becomes a Client Component when explicitly marked with the `"use client"`
directive. See [server-components.md](server-components.md).

</details>

<details>
<summary>Your product catalog page's data changes a few times a day, and you want fast page loads without a full rebuild on every change. Which strategy fits?</summary>

Incremental Static Regeneration — a `revalidate` interval lets Next.js serve the fast, cached
static page while regenerating it in the background at most that often, without needing a full
site rebuild for each data change. See
[incremental-static-regeneration.md](incremental-static-regeneration.md).

</details>

## References

- Next.js, [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- Next.js, [Incremental Static Regeneration](https://nextjs.org/docs/app/guides/incremental-static-regeneration)

## Continue Your Learning Path

Next: [App Router Deep Dive](../app-router-deep-dive/) — see the
[Frontend learning path](../../README.md) for the full sequence.
