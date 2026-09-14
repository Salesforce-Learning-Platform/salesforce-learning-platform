# Data Fetching Patterns: Why "Server State" Is Different

## Server State vs. Client State

[understanding-state.md](../state-and-rerendering-logic/understanding-state.md) covered state
owned entirely by a component (a form field, a toggle). Data fetched from a server — a user's
order history — is fundamentally different in ways that matter for how it should be managed:

| | Client state (e.g., form input) | Server state (e.g., order history) |
|---|---|---|
| Who owns the actual data? | This component | The server/database |
| Can it change without this component doing anything? | No | Yes — another user, another tab, or a background process can change it |
| Is it ever "out of date"? | No — it's the current, authoritative value | Yes — it can go stale the moment it's fetched |
| Might multiple components need the exact same data? | Rarely | Commonly (a header's cart count and a cart page both need the same cart data) |

## The Problems This Creates in Practice

Given these differences, naively fetching the same server data in every component that needs it
(as done so far in this module) creates real, observable problems in an application of any size:

- **Duplicate requests**: if both a page's header (showing an order count) and its main content
  (showing the full order list) fetch `/api/users/:id/orders` independently, that's two identical
  network requests for the exact same data.
- **Inconsistent data**: if a user places a new order, every component holding a separate copy of
  the "orders" server state needs to be told individually to refetch — easy to miss one.
- **No caching**: navigating away from a page and back re-fetches everything from scratch, even if
  the data almost certainly hasn't changed in the last few seconds.

## The Manual Fix Gets Complicated Fast

You could hand-build a shared cache (a `Map` keyed by URL, shared via Context — covered in the
next module), manually track staleness, and coordinate refetching across every component that
needs the same server data — but this is exactly the well-understood, repeatedly-solved problem
that dedicated libraries exist for, covered next in
[react-query.md](react-query.md), rather than something worth re-inventing per project.

## Common Mistakes

- Treating server-fetched data identically to local UI state, missing that it can go stale or be
  needed by multiple unrelated components simultaneously.
- Duplicating the same fetch logic (and the same network request) across multiple components that
  happen to need overlapping server data.
- Manually building an ad hoc caching/deduplication layer from scratch, reinventing what a
  well-tested library like React Query already solves correctly.

## Next

Continue to [react-query.md](react-query.md) for the dedicated tool built specifically for this
category of problem.
