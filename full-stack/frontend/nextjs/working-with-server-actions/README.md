# Working with Server Actions

## Purpose

[Building APIs with Next.js](../building-apis-with-nextjs/) covered Route Handlers — genuine HTTP
endpoints. **Server Actions** solve a related but distinct problem: mutating data directly from a
form or component, without hand-building a separate API endpoint and a `fetch` call to reach it.
This is the final module in the Next.js domain.

## Learning Objectives

- Explain what a Server Action is, and create one with the `"use server"` directive.
- Wire a Server Action directly to a `<form>`'s `action` prop.
- Show pending and error state for a Server Action using `useActionState`.
- Revalidate cached data after a mutation, and understand why authorization must be checked inside
  every Server Action itself.

## Prerequisites

[Building APIs with Next.js](../building-apis-with-nextjs/) and
[Advanced Forms and Validation](../../react/advanced-forms-and-validation/).

## Files in This Module

| File | Covers |
|---|---|
| [introduction-to-server-actions.md](introduction-to-server-actions.md) | What a Server Action is, and the critical security note about it |
| [forms-and-server-actions.md](forms-and-server-actions.md) | Wiring a Server Action directly to a form's `action` prop |
| [data-mutations.md](data-mutations.md) | Mutating data server-side and reading form values |
| [revalidation.md](revalidation.md) | `revalidatePath`/`revalidateTag` and redirecting after a mutation |
| [error-handling.md](error-handling.md) | Showing pending and error state with `useActionState` |

## When to Deep-Dive vs. Skim

Deep-dive [introduction-to-server-actions.md](introduction-to-server-actions.md)'s security
section — Next.js's own documentation explicitly warns that a Server Action is reachable via a
direct POST request, not only through your form's UI, which makes this a direct, practical
instance of the "never trust the client" principle from
[frontend-and-backend-responsibilities.md](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md).

## Quick Knowledge Check

<details>
<summary>If a Server Action is only ever called from one specific form in your UI, is checking authorization inside it optional?</summary>

No — a Server Action is a real network-reachable endpoint, exactly like a Route Handler. It can be
invoked directly with a POST request, bypassing your form and UI entirely. Authorization must be
checked inside the action itself, every time. See
[introduction-to-server-actions.md](introduction-to-server-actions.md).

</details>

<details>
<summary>After a Server Action successfully creates a new product, why might the product list page still show stale data?</summary>

Next.js's cache doesn't know the underlying data changed until told to — calling
`revalidatePath`/`revalidateTag` inside the action after the mutation invalidates the relevant
cached page, exactly the ISR concept from
[incremental-static-regeneration.md](../rendering-strategies/incremental-static-regeneration.md).
See [revalidation.md](revalidation.md).

</details>

## References

- Next.js, [Mutating Data](https://nextjs.org/docs/app/getting-started/mutating-data)

## Continue Your Learning Path

This is the last module in the Next.js domain. See the
[Frontend learning path](../../README.md) for what comes next.
