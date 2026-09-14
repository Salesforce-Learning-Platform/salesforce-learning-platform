# Common React Errors

## "Cannot update state on an unmounted component"

```jsx
function OrderHistory({ userId }) {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetch(`/api/users/${userId}/orders`)
      .then(res => res.json())
      .then(data => setOrders(data)); // may run AFTER the component unmounts
  }, [userId]);
}
```

**Cause**: an async operation resolves after the component that started it has already been
removed from the UI, and its callback tries to update state that no longer applies to anything.
**Fix**: exactly the cleanup-based `ignore` flag or `AbortController` pattern from
[fetching-data.md](../server-state-and-api-integration/fetching-data.md).

## "Too many re-renders"

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  setCount(count + 1); // called directly during render, not inside a handler — infinite loop
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Cause**: calling a state setter directly during rendering (not inside an event handler or
effect) triggers a re-render, which calls the setter again, forever. **Fix**: move the state
update into an event handler or `useEffect` — state should never be set unconditionally in a
component's main render body.

## "Objects are not valid as a React child"

```jsx
function UserCard({ user }) {
  return <p>{user}</p>; // user is an object, e.g. { name: "Ada", email: "..." }
}
```

**Cause**: trying to render a plain object directly in JSX — JSX can render strings, numbers, and
elements, but not an arbitrary object. **Fix**: render a specific property (`{user.name}`), or
explicitly convert it (`JSON.stringify(user)`, though rarely what's actually wanted for real UI).

## Missing `key` Prop Warning

```jsx
{orders.map(order => <li>{order.date}</li>)} // Warning: each child needs a unique "key" prop
```

**Cause**: rendering a list (see
[jsx.md](../components-jsx-and-props/jsx.md)) without a `key`, which React needs to correctly
track which item is which across re-renders. **Fix**: add a stable, unique `key`
(`<li key={order.id}>`) — using the array index as a fallback is acceptable only when the list is
never reordered, filtered, or has items inserted/removed from the middle.

## "React Hook useEffect has a missing dependency"

Covered in full in
[dependency-array.md](../react-lifecycle-and-useeffect/dependency-array.md) — an ESLint warning
from `eslint-plugin-react-hooks`'s `exhaustive-deps` rule, flagging a value used inside an effect
that's missing from its dependency array, risking a stale-closure bug.

## Common Mistakes

- Treating error messages as opaque noise to silence rather than reading them carefully — React's
  error and warning messages are generally specific and point directly at the actual cause.
- Adding a random, unstable `key` (like `Math.random()`) purely to silence the missing-key
  warning, which defeats the entire purpose of `key` and can cause worse bugs than having no key
  at all.
- Ignoring the `exhaustive-deps` warning by adding `// eslint-disable-next-line` reflexively,
  rather than understanding and fixing the actual underlying stale-value risk it's flagging.

## Next

Continue to [react-error-boundaries.md](react-error-boundaries.md) for catching rendering errors
gracefully rather than crashing the entire page.
