# React Query (TanStack Query)

## The Same Order History, with React Query

```jsx
import { useQuery } from "@tanstack/react-query";

function OrderHistory({ userId }) {
  const { data: orders, status, error } = useQuery({
    queryKey: ["orders", userId],
    queryFn: () => fetch(`/api/users/${userId}/orders`).then(res => res.json()),
  });

  if (status === "pending") return <p>Loading orders...</p>;
  if (status === "error") return <p role="alert">Failed to load orders: {error.message}</p>;
  return (
    <ul>
      {orders.map(order => <li key={order.id}>{order.date}: ${order.total}</li>)}
    </ul>
  );
}
```

Compare this directly to the hand-built version from
[loading-and-error-states.md](loading-and-error-states.md): `useQuery` replaces the manual
`useState`/`useEffect`/race-condition-guard/status-tracking entirely — one hook call, given a
unique **query key** and a function that fetches the data, returns exactly the same
loading/error/success information the hand-built version tracked manually.

## The `queryKey` Enables Automatic Deduplication and Caching

```jsx
// Component A
useQuery({ queryKey: ["orders", userId], queryFn: fetchOrders });

// Component B, rendered simultaneously
useQuery({ queryKey: ["orders", userId], queryFn: fetchOrders });
```

Both components requesting the exact same `queryKey` share **one single underlying request and
cache entry** — directly solving the duplicate-request problem from
[data-fetching-patterns.md](data-fetching-patterns.md), automatically, with no manual coordination
required.

## Automatic Refetching and Cache Invalidation

```jsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function PlaceOrderButton({ userId, cart }) {
  const queryClient = useQueryClient();

  const { mutate } = useMutation({
    mutationFn: (order) => fetch("/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(order),
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orders", userId] }); // triggers a refetch everywhere
    },
  });

  return <button onClick={() => mutate({ userId, items: cart })}>Place Order</button>;
}
```

`useMutation` handles write operations (creating/updating data on the server), and
`invalidateQueries` tells React Query a specific cached query is now stale — every component
currently displaying that `queryKey`'s data (the order history list, a header's order count badge,
anywhere else) automatically refetches, solving the "every component needs to be told
individually" consistency problem from
[data-fetching-patterns.md](data-fetching-patterns.md) without manually tracking who needs to know.

## When React Query Is (and Isn't) the Right Tool

React Query is specifically for **server state** — data whose source of truth lives outside your
application. It's not a replacement for `useState`/`useReducer` managing purely local UI state (a
form's current input, whether a dropdown is open) — those remain client state, appropriately
managed by the tools covered in earlier modules, with React Query reserved for the genuinely
server-owned data.

## Common Mistakes

- Using React Query to manage purely local UI state that has no actual server source of truth —
  that's still `useState`'s job.
- Choosing an inconsistent `queryKey` structure for the same logical data across a codebase,
  accidentally defeating the automatic deduplication/caching this entire library exists to
  provide.
- Forgetting to invalidate the relevant queries after a mutation, leaving stale cached data
  displayed even though the underlying server data has actually changed.

## Module Summary

Across this module: fetching data with `useEffect` requires explicit protection against race
conditions when a fast-changing dependency triggers overlapping requests (see
[fetching-data.md](fetching-data.md)); a request has (at least) loading, success, error, and empty
states, all needing explicit representation (see
[loading-and-error-states.md](loading-and-error-states.md)); server state is a genuinely distinct
category from client state — owned externally, capable of going stale, and often needed by
multiple components (see [data-fetching-patterns.md](data-fetching-patterns.md)); and React Query
solves deduplication, caching, and cross-component consistency for exactly this category of
problem, rather than requiring it to be hand-built and re-solved per project.
