# Server State and API Integration

## Purpose

Data that lives on a server — a user's order history, a product catalog — is fundamentally
different from the local UI state covered in earlier modules: it can change without your
component doing anything, it needs to be fetched asynchronously, and multiple components might
need the same data simultaneously. This module covers fetching it correctly by hand, then React
Query, the library most real projects reach for once this gets genuinely complex.

## Learning Objectives

- Fetch data in a component using `useEffect` and the Fetch API, correctly handling loading and
  error states.
- Handle the race-condition risk of a fast-changing fetch (e.g., a rapidly-typed search).
- Explain what "server state" means as a distinct category from local UI state.
- Use React Query for caching, deduplication, and automatic refetching.

## Prerequisites

[React Lifecycle and useEffect](../react-lifecycle-and-useeffect/) and
[Asynchronous Programming and Modules](../../javascript/asynchronous-programming-and-modules/).

## Files in This Module

| File | Covers |
|---|---|
| [fetching-data.md](fetching-data.md) | Fetching data with `useEffect`, including the cleanup-based race-condition fix |
| [loading-and-error-states.md](loading-and-error-states.md) | Representing and displaying the full lifecycle of a request |
| [data-fetching-patterns.md](data-fetching-patterns.md) | Why "server state" is a distinct category from local state |
| [react-query.md](react-query.md) | Caching, deduplication, and automatic refetching with React Query |

## When to Deep-Dive vs. Skim

Deep-dive [fetching-data.md](fetching-data.md)'s race-condition section — a fast typist in a
search box, or a user navigating quickly between two data-heavy pages, can trigger a genuine,
observable bug (an old response overwriting a newer one) that's easy to miss until it happens in
front of a real user.

## Quick Knowledge Check

<details>
<summary>A user types quickly in a search box, each keystroke triggering a new fetch. Why might the search results briefly show something wrong?</summary>

If an earlier, slower request resolves *after* a later, faster one, its now-stale result can
overwrite the correct, more recent one — a race condition. The fix uses the effect's cleanup
function to ignore a request's result if it's no longer the current one. See
[fetching-data.md](fetching-data.md).

</details>

<details>
<summary>Why is "server state" treated as a genuinely different category from ordinary React state?</summary>

It's owned by something outside your application, can go stale, might be needed by multiple
unrelated components, and can be updated by other users or processes — none of which apply to a
plain `useState` counter. This is exactly what React Query is purpose-built to manage. See
[data-fetching-patterns.md](data-fetching-patterns.md).

</details>

## References

- TanStack Query, [Overview](https://tanstack.com/query/latest/docs/framework/react/overview)
- MDN Web Docs, [Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)

## Continue Your Learning Path

Next: [Global State Management](../global-state-management/) — see the
[Frontend learning path](../../README.md) for the full sequence.
