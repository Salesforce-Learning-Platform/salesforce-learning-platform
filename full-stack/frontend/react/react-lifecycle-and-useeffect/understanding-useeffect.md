# Understanding `useEffect`

## What an Effect Actually Is

An **effect** is code that synchronizes a component with something *outside* React's own
rendering system — a browser API, a subscription, a timer, fetching data from a server. It's code
that needs to run *because rendering happened*, not because a user clicked something specific.

```jsx
function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.connect();
    return () => connection.disconnect(); // cleanup, covered in cleanup-functions.md
  }, [roomId]); // dependency array, covered in dependency-array.md

  return <div>Welcome to {roomId}</div>;
}
```

## Effects vs. Event Handlers — A Critical Distinction

| | Event handler | Effect |
|---|---|---|
| Runs because... | A specific user interaction happened (a click, a keystroke) | Rendering happened (the component appeared, or a dependency changed) |
| Example | Submitting a form when the button is clicked | Connecting to a chat room when `roomId` changes |

This distinction determines where code belongs: **"fetch data when the user clicks Search"**
belongs in an event handler (`onClick`); **"keep this component's chat connection in sync with the
current `roomId`"** belongs in an effect, since it needs to happen whenever `roomId` changes,
regardless of *why* it changed (a click, a prop update from a parent, anything else).

## The Three Parts of `useEffect`

```jsx
useEffect(() => {
  // 1. Setup — runs after the render, when a dependency has changed
  const connection = createConnection(roomId);
  connection.connect();

  return () => {
    // 3. Cleanup — runs before the NEXT effect run, and on unmount
    connection.disconnect();
  };
}, [roomId]); // 2. Dependencies — what should cause this effect to re-run
```

1. **Setup function**: the actual effect logic.
2. **Dependency array**: the values this effect depends on — covered in
   [dependency-array.md](dependency-array.md).
3. **Cleanup function** (optional, returned from the setup function): undoes the setup — covered in
   [cleanup-functions.md](cleanup-functions.md).

## Effects Run *After* the DOM Updates

Unlike the component function body itself (which runs during rendering, before anything is
displayed), an effect's setup function runs **after** React has updated the actual DOM to match
the new render — this is deliberate: an effect that needs to measure a rendered element's size, for
instance, needs that element to actually exist in the DOM first.

## Common Mistakes

- Using an effect for something that should be an event handler instead — e.g., fetching data
  "when the button is clicked" by watching a state flag inside an effect, when directly calling
  the fetch in the button's `onClick` handler is simpler and more direct.
- Assuming effects run *during* rendering, the way the component body does — they run afterward,
  which matters for anything depending on the DOM already being updated.
- Forgetting effects exist specifically for *synchronization with something external* — reaching
  for one to compute a value that could simply be calculated directly during render instead (a
  common, avoidable overuse of `useEffect`).

## Next

Continue to [dependency-array.md](dependency-array.md) — the part of `useEffect` most responsible
for real bugs when misunderstood.
