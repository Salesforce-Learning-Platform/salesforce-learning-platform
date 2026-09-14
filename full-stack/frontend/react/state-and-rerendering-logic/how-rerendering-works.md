# How Re-rendering Works

## What "Re-render" Actually Means

A **render** is React calling a component function to figure out what it should currently display.
A **re-render** is that same process happening again — the component function runs again, from
top to bottom, computing a fresh description of the UI based on its current props and state.

## What Triggers a Re-render

| Trigger | Example |
|---|---|
| A component's own state changes | Calling a `useState` setter |
| A component receives new props | Its parent re-rendered and passed a different value |
| Its parent re-renders at all | Even with unchanged props, by default (see below) |

## Re-rendering Cascades Downward

```jsx
function App() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <Display count={count} />
      <StaticFooter /> {/* receives no relevant props at all */}
    </div>
  );
}
```

When `count` changes and `App` re-renders, **every child it renders also re-renders by default** —
including `StaticFooter`, which doesn't even use `count` or receive any prop that changed. This is
React's default, intentionally simple behavior: a parent re-rendering re-renders its entire
subtree, not just the parts that "obviously" need it. (Performance techniques to avoid this
unnecessary cascade — like `memo` — are covered in the Performance Optimization module later in
this domain.)

## Re-render ≠ DOM Update

This distinction matters: a re-render is React calling your component function and computing a new
description of the UI — it does **not** necessarily mean the actual browser DOM changes at all.
React compares the newly computed description against the previous one and updates only the parts
of the real DOM that actually differ (a process informally called "reconciliation"). A component
can re-render (its function runs again) while producing an identical result, in which case no real
DOM mutation happens — this is why re-renders, while not free, are considerably cheaper than a full
manual [reflow](../../html/semantic-html-and-browser-rendering/reflow-and-repaint.md) of the whole
page.

## A Concrete Trace

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  console.log("Counter rendered"); // logs on EVERY render, including the first
  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```

Clicking the button: `setCount` is called → React schedules a re-render → `Counter` runs again
(the `console.log` fires again) → React computes the new JSX → React compares it to the previous
render's output → only the changed text node in the DOM is actually updated.

## Common Mistakes

- Assuming a re-render always means a visible page update — many re-renders produce identical
  output and never touch the actual DOM at all.
- Not realizing that a parent's re-render cascades to every child by default, regardless of whether
  that child's own props actually changed — a common source of "why is this unrelated component
  re-rendering" confusion, addressed later with `memo`.
- Confusing "re-render" (React recalculating what the UI should look like) with the earlier,
  network-level concept of a full page reload — they're unrelated; a React re-render never involves
  refetching the page or restarting the JavaScript from scratch.

## Next

Continue to [batching-state-updates.md](batching-state-updates.md) to see how React groups
multiple state updates together rather than re-rendering after each individual one.
