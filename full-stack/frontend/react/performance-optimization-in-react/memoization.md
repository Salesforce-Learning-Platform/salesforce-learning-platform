# Memoization: `memo`

## The Problem

As covered in [how-rerendering-works.md](../state-and-rerendering-logic/how-rerendering-works.md),
a parent re-rendering re-renders its entire subtree by default. On a dashboard with an expensive
`AnalyticsChart` component and a simple `RefreshButton` next to it, clicking refresh (updating some
unrelated piece of state) re-renders the chart too, even though nothing it actually displays
changed.

## `memo` — Skipping a Re-render When Props Haven't Changed

```jsx
import { memo } from "react";

const AnalyticsChart = memo(function AnalyticsChart({ data }) {
  console.log("AnalyticsChart rendered");
  return <canvas>{/* expensive chart rendering */}</canvas>;
});

function Dashboard() {
  const [lastRefreshed, setLastRefreshed] = useState(Date.now());
  const [chartData] = useState(generateChartData());

  return (
    <div>
      <button onClick={() => setLastRefreshed(Date.now())}>Refresh</button>
      <p>Last refreshed: {lastRefreshed}</p>
      <AnalyticsChart data={chartData} /> {/* chartData never actually changes here */}
    </div>
  );
}
```

`memo(Component)` wraps a component so React compares its new props against the previous render's
before re-rendering — if they're shallowly equal (per `Object.is`, roughly the same reference
comparison from [objects.md](../../javascript/arrays-and-objects/objects.md)), React skips
re-rendering it entirely and reuses the previous result. Clicking "Refresh" here updates
`lastRefreshed`, but `AnalyticsChart`'s only prop (`chartData`) never changes, so `memo` correctly
skips its expensive re-render.

## The Critical Gotcha: New References Defeat `memo`

```jsx
function Dashboard() {
  const [lastRefreshed, setLastRefreshed] = useState(Date.now());

  return (
    <AnalyticsChart
      data={chartData}
      onExport={() => console.log("exporting")} // a NEW function on every single render!
    />
  );
}
```

Even with `memo`, if a parent passes an inline function or object literal as a prop, that value is
a genuinely new reference on every render (per
[arrays.md](../../javascript/arrays-and-objects/arrays.md)'s reference-comparison rules) — `memo`'s
shallow comparison sees a "different" `onExport` every time and re-renders anyway, silently
defeating the entire optimization. This is exactly why `memo` is typically paired with
`useCallback` (see [usecallback.md](../react-hooks/usecallback.md)) for any function props, and
`useMemo` for any object/array props passed to a memoized child.

## When `memo` Is Actually Worth It

`memo` itself has a small cost (comparing props on every render) — it's worth applying specifically
when a component is genuinely expensive to re-render (a large chart, a complex list) *and*
receives stable, memoized props most of the time. Wrapping every component in `memo` reflexively,
including cheap ones, can add more overhead than it saves — the same "don't optimize what isn't
actually slow" principle from
[usememo.md](../react-hooks/usememo.md).

## Common Mistakes

- Wrapping a component in `memo` while its parent still passes new inline function/object literals
  as props, providing no actual benefit since those props are never reference-equal across renders.
- Applying `memo` to every component reflexively, adding comparison overhead to cheap components
  that were never actually a performance problem.
- Assuming `memo` prevents re-renders caused by the component's *own* state or context changes —
  it only skips re-renders triggered by an unchanged-props parent re-render.

## Next

Continue to [code-splitting.md](code-splitting.md) — a different kind of optimization, reducing
what code needs to be downloaded at all, rather than how often it re-renders.
