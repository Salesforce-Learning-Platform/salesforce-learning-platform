# `useMemo`

## The Problem: Recomputing on Every Render

As covered in [how-rerendering-works.md](../state-and-rerendering-logic/how-rerendering-works.md),
a component function runs again — completely from scratch — on every re-render. Any expensive
computation inside it runs again too, even if the inputs it depends on haven't actually changed:

```jsx
function ProductList({ products, filter }) {
  const filtered = expensiveFilter(products, filter); // reruns on EVERY render
  return <ul>{filtered.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

If `ProductList` re-renders for a reason unrelated to `products` or `filter` (say, its parent
re-rendered for some other reason entirely), `expensiveFilter` still runs again, recomputing an
identical result for no benefit.

## `useMemo` — Memoizing a Value

```jsx
function ProductList({ products, filter }) {
  const filtered = useMemo(
    () => expensiveFilter(products, filter),
    [products, filter] // dependency array
  );
  return <ul>{filtered.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

`useMemo(calculateValue, dependencies)` only re-runs `calculateValue` when one of the values in the
dependency array has actually changed since the last render — otherwise, it returns the previously
computed, cached result directly, skipping the expensive recomputation entirely.

## When `useMemo` Is (and Isn't) Worth Using

This is genuinely important: `useMemo` itself isn't free — it has to compare the dependency array
on every render and store the cached result. For a cheap computation (adding two numbers,
formatting a short string), the overhead of `useMemo` can exceed the cost of just recomputing it
plainly — memoization is worth reaching for specifically when the computation is **actually
expensive** (filtering/sorting a large array, a complex calculation) or when its **result's
reference identity matters** for another optimization (like preventing a child component wrapped
in `memo`, covered in the Performance Optimization module, from re-rendering unnecessarily).

## Common Mistakes

- Wrapping every computed value in `useMemo` reflexively, adding overhead without any actual
  performance benefit for genuinely cheap calculations.
- Forgetting a value in the dependency array that the calculation actually depends on, causing
  `useMemo` to return a stale, outdated result after that value changes.
- Assuming `useMemo` guarantees the calculation never re-runs — React may, in some circumstances,
  discard a memoized value and recompute it anyway; `useMemo` is a performance optimization, not a
  strict, unconditional guarantee.

## Next

Continue to [usecallback.md](usecallback.md) for the equivalent pattern applied to function
references rather than computed values.
