# `useCallback`

## The Problem: Functions Are Recreated Every Render

```jsx
function Parent() {
  const [count, setCount] = useState(0);

  function handleClick() { // a brand-new function, created fresh on EVERY render
    console.log("clicked");
  }

  return <Child onClick={handleClick} />;
}
```

Every time `Parent` re-renders, `handleClick` is a genuinely new function — even though it does
the exact same thing every time. Recall from
[arrays.md](../../javascript/arrays-and-objects/arrays.md) that objects (and functions, which are
objects) are compared by reference — this means `Child` receives a *different* `onClick` prop
value on every render, even though nothing meaningful about it actually changed.

## `useCallback` — Memoizing a Function Reference

```jsx
function Parent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    console.log("clicked");
  }, []); // empty dependency array — this function never needs to change

  return <Child onClick={handleClick} />;
}
```

`useCallback(fn, dependencies)` returns the *same* function reference across re-renders, as long as
the dependency array's values haven't changed — solving exactly the reference-identity problem
above.

## Why This Matters Specifically for `memo`-Wrapped Children

```jsx
const Child = memo(function Child({ onClick }) {
  console.log("Child rendered");
  return <button onClick={onClick}>Click</button>;
});
```

`memo` (covered in the Performance Optimization module) skips a child's re-render when its props
are reference-equal to the previous render's — but this only works if `onClick` is actually the
same function reference each time. Without `useCallback`, a new `handleClick` function on every
`Parent` render defeats `memo`'s optimization entirely, since `Child`'s props are never
reference-equal across renders. This is the single most common, legitimate reason to reach for
`useCallback`.

## `useCallback` vs. `useMemo` — The Same Idea, Different Target

```jsx
const memoizedValue = useMemo(() => computeValue(a, b), [a, b]);     // memoizes a VALUE
const memoizedFn = useCallback(() => doSomething(a, b), [a, b]);       // memoizes a FUNCTION
```

`useCallback(fn, deps)` is functionally equivalent to `useMemo(() => fn, deps)` — they're the same
underlying mechanism, just with `useCallback` as a more convenient, purpose-built form
specifically for memoizing functions.

## Common Mistakes

- Wrapping every event handler in `useCallback` reflexively, even ones never passed to a
  `memo`-wrapped child or otherwise depended on for reference stability — this adds overhead with
  no actual benefit, exactly the `useMemo` mistake from [usememo.md](usememo.md), applied to
  functions.
- Forgetting a genuinely used variable in the dependency array, causing the memoized function to
  close over (see [closures.md](../../javascript/functions/closures.md)) a stale value from an
  earlier render.
- Using `useCallback` without also wrapping the receiving child in `memo` — without that pairing,
  memoizing the function provides no actual re-render-skipping benefit at all.

## Next

Continue to [custom-hooks.md](custom-hooks.md) to combine hooks into your own reusable, named
logic.
