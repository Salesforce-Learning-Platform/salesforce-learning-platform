# Understanding State

## What State Actually Is

**State** is data that a component owns and that can change over time in response to user
interaction or other events, where a change should cause the UI to update. It's the concrete
mechanism behind the "UI as a function of state" model from
[what-is-react.md](../introduction-to-react/what-is-react.md).

## Why a Plain Variable Doesn't Work

```jsx
function Counter() {
  let count = 0; // looks reasonable, but doesn't work as intended

  function handleClick() {
    count = count + 1;
    console.log(count); // this DOES update...
  }

  return <button onClick={handleClick}>Count: {count}</button>; // ...but this never re-renders
}
```

Two separate problems: first, changing `count` gives React no signal that anything happened —
there's no re-render, so the displayed "Count: {count}" text never updates on screen even though
the variable's value did change. Second, even if a re-render somehow happened, a plain `let`
variable is reset to its initial value (`0`) every time, since the component function runs again
from scratch on every render — normal local variables don't persist between renders at all.

## What `useState` Actually Solves

State (via `useState`, covered in [usestate.md](usestate.md)) solves both problems at once: React
persists the value across re-renders on its own (outside the component function's own execution),
and updating it explicitly tells React to re-render the component so the UI reflects the new
value.

## State vs. Props vs. Plain Variables

| | Plain variable | Props | State |
|---|---|---|---|
| Persists across re-renders? | No — reset every render | Yes (owned by parent) | Yes (owned by this component) |
| Who can change it? | Anyone, but pointlessly (see above) | Only the parent (read-only here, see [props.md](../components-jsx-and-props/props.md)) | This component itself |
| Changing it triggers a re-render? | No | N/A — changes when the parent re-renders it | Yes |

## Each Component Instance Has Its Own State

```jsx
function App() {
  return (
    <>
      <Counter /> {/* has its own independent count */}
      <Counter /> {/* a completely separate independent count */}
    </>
  );
}
```

Two instances of the same component, rendered separately, each maintain their own completely
independent state — clicking one `Counter`'s button never affects the other's count, even though
they're both running the exact same component function.

## Common Mistakes

- Using a plain variable for something that should trigger a UI update when it changes, and being
  confused when the screen doesn't reflect the change.
- Assuming state is somehow shared globally by default — each component instance's state is
  private to that instance unless deliberately shared (via lifting state up, or Context, covered
  later in this domain).
- Directly mutating a piece of state (`user.name = "new"`) instead of using the setter function —
  covered in depth in [usestate.md](usestate.md), this silently fails to trigger a re-render.

## Next

Continue to [usestate.md](usestate.md) for the actual hook that implements all of this.
