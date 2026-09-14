# Fetching Data

## The Basic Pattern

Fetching a user's order history when a dashboard page loads:

```jsx
function OrderHistory({ userId }) {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetch(`/api/users/${userId}/orders`)
      .then(res => res.json())
      .then(data => setOrders(data));
  }, [userId]);

  return (
    <ul>
      {orders.map(order => <li key={order.id}>{order.date}: ${order.total}</li>)}
    </ul>
  );
}
```

This combines the Fetch API from
[fetch-api.md](../../javascript/asynchronous-programming-and-modules/fetch-api.md) with the
effect/dependency-array discipline from
[dependency-array.md](../react-lifecycle-and-useeffect/dependency-array.md) — the effect re-runs
whenever `userId` changes, correctly re-fetching that user's specific orders rather than showing
stale data from a previous user.

## The Race Condition Problem

```jsx
function OrderHistory({ userId }) {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetch(`/api/users/${userId}/orders`)
      .then(res => res.json())
      .then(data => setOrders(data)); // DANGEROUS if userId changes again before this resolves
  }, [userId]);
}
```

If `userId` changes quickly (a user clicking between two different customer records, for
instance), a *new* fetch starts for the new `userId` — but the *old* fetch, already in flight, is
still running. If that old, slower request happens to resolve **after** the new one, its stale
result overwrites the correct, current data — showing the wrong user's orders.

## Fixing It with the Effect's Cleanup Function

```jsx
function OrderHistory({ userId }) {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    let ignore = false;

    fetch(`/api/users/${userId}/orders`)
      .then(res => res.json())
      .then(data => {
        if (!ignore) setOrders(data); // only apply the result if this effect is still current
      });

    return () => {
      ignore = true; // cleanup runs before the NEXT effect (new userId) — marks this one stale
    };
  }, [userId]);
}
```

This directly applies [cleanup-functions.md](../react-lifecycle-and-useeffect/cleanup-functions.md):
the cleanup function runs immediately before the effect re-runs for a new `userId`, flipping
`ignore` to `true` — so if the *old* request's promise resolves after that point, its result is
correctly discarded rather than applied.

## `AbortController` — A More Direct Alternative

```jsx
useEffect(() => {
  const controller = new AbortController();

  fetch(`/api/users/${userId}/orders`, { signal: controller.signal })
    .then(res => res.json())
    .then(data => setOrders(data));

  return () => controller.abort(); // actually cancels the in-flight request
}, [userId]);
```

`AbortController` goes further than the `ignore` flag — it genuinely cancels the outdated network
request rather than just ignoring its eventual result, saving the bandwidth and server work of a
response that will never actually be used.

## Common Mistakes

- Fetching data without any race-condition protection, producing an intermittent, hard-to-reproduce
  bug that only appears when requests resolve out of order.
- Forgetting the cleanup function entirely, which is what makes the `ignore` flag (or
  `AbortController`) actually work — without it, there's no way to know a later effect run has
  superseded this one.
- Using `AbortController` but forgetting that a component's own unmount (not just a dependency
  change) also triggers the same cleanup — both cases are handled identically.

## Next

Continue to [loading-and-error-states.md](loading-and-error-states.md) to represent the full
lifecycle of this request, not just its eventual success.
