# Loading and Error States

## A Request Has (at Least) Three States

The order-history example so far only handled the success case. A real request genuinely has
three distinct states a UI needs to represent: **loading** (in progress), **success** (data
arrived), and **error** (it failed) — silently ignoring the other two leaves a user staring at a
blank list with no explanation, whether the request is still running or has actually failed.

```jsx
function OrderHistory({ userId }) {
  const [orders, setOrders] = useState([]);
  const [status, setStatus] = useState("idle"); // "idle" | "loading" | "success" | "error"
  const [error, setError] = useState(null);

  useEffect(() => {
    let ignore = false;
    setStatus("loading");

    fetch(`/api/users/${userId}/orders`)
      .then(res => {
        if (!res.ok) throw new Error(`Request failed: ${res.status}`); // per fetch-api.md
        return res.json();
      })
      .then(data => {
        if (!ignore) {
          setOrders(data);
          setStatus("success");
        }
      })
      .catch(err => {
        if (!ignore) {
          setError(err);
          setStatus("error");
        }
      });

    return () => { ignore = true; };
  }, [userId]);

  if (status === "loading") return <p>Loading orders...</p>;
  if (status === "error") return <p role="alert">Failed to load orders: {error.message}</p>;
  return (
    <ul>
      {orders.map(order => <li key={order.id}>{order.date}: ${order.total}</li>)}
    </ul>
  );
}
```

This directly applies the `response.ok` gotcha from
[fetch-api.md](../../javascript/asynchronous-programming-and-modules/fetch-api.md) — without
explicitly checking it and throwing, a `404`/`500` response would silently fall into the success
branch with an unhelpful error-page body.

## Empty States Are a Fourth, Often-Forgotten Case

```jsx
if (status === "success" && orders.length === 0) {
  return <p>You haven't placed any orders yet.</p>;
}
```

A successful request that legitimately returns zero results is a distinct case from both loading
and error — a new customer with no order history yet shouldn't see a bare, ambiguous empty list
with no explanation.

## A Reducer for More Complex State Machines

For a request with genuinely many possible states and transitions, `useReducer` (a hook not
covered in depth in this platform's core sequence, but worth knowing exists) can express this more
explicitly than several separate `useState` calls — worth reaching for once the state combinations
become hard to reason about as independent booleans.

## Common Mistakes

- Handling only the success case and leaving loading/error states entirely unrepresented, showing
  a blank or broken-looking UI during a slow request or an actual failure.
- Forgetting the empty-success case, leaving a legitimately empty result indistinguishable from a
  still-loading or broken state.
- Using multiple independent boolean flags (`isLoading`, `isError`, `isSuccess`) that can
  contradictorily all be `true` or `false` simultaneously, rather than one single `status` value
  that can only ever be one thing at a time — directly the discriminated-union thinking from
  [unions-and-intersections.md](../../typescript/typescript-essentials/unions-and-intersections.md).

## Next

Continue to
[data-fetching-patterns.md](data-fetching-patterns.md) to see why this entire category of problem
is called "server state," and why that distinction matters.
