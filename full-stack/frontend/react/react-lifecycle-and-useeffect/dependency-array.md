# The Dependency Array

## What It Controls

The dependency array (the second argument to `useEffect`) tells React exactly when the effect's
setup function needs to run again — specifically, whenever any value listed in it has changed
since the last render.

```jsx
useEffect(() => { /* ... */ }, [roomId]);   // re-runs only when `roomId` changes
useEffect(() => { /* ... */ }, []);            // runs ONCE, after the first render only
useEffect(() => { /* ... */ });                   // runs after EVERY render, with no dependency check at all
```

| Dependency array | Effect re-runs... |
|---|---|
| `[roomId]` | Whenever `roomId`'s value actually changes |
| `[]` (empty) | Only once, after the initial mount — matching `componentDidMount` from [component-lifecycle.md](component-lifecycle.md) |
| Omitted entirely | After every single render, with no dependency check at all — rarely what's actually wanted |

## The Rule: Include Everything the Effect Actually Uses

```jsx
function ChatRoom({ roomId, serverUrl }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId); // uses BOTH roomId and serverUrl
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // BUG — serverUrl is used but missing from the dependency array
}
```

This is a genuine, common bug, not a style nitpick: the effect closes over (see
[closures.md](../../javascript/functions/closures.md)) whatever `serverUrl` value existed on the
render when it was created. If `serverUrl` changes on a later render but isn't in the dependency
array, the effect doesn't re-run — it keeps using the stale, outdated `serverUrl` from whenever it
last actually ran. `eslint-plugin-react-hooks` (from
[rules-of-hooks.md](../react-hooks/rules-of-hooks.md)) includes a rule (`exhaustive-deps`) that
detects exactly this class of bug automatically.

## The Empty Array — Understanding What It Actually Means

`[]` doesn't mean "this effect has no dependencies" in some special sense — it means "this effect
depends on nothing that changes across re-renders," so it only needs to run once, on mount. If the
effect's body genuinely uses a prop or state value, `[]` is almost always incorrect — it will
silently use only the very first render's value of that dependency forever, exactly the stale-value
bug above.

## Common Mistakes

- Adding `[]` to silence an ESLint warning about a missing dependency without actually
  understanding *why* it's needed — this papers over a real stale-value bug rather than fixing it.
- Including a dependency that changes on every single render (like a newly-created object or array
  literal defined inline) without memoizing it (see
  [usememo.md](../react-hooks/usememo.md)/[usecallback.md](../react-hooks/usecallback.md) first),
  which causes the effect to re-run every render — effectively the same as omitting the array
  entirely.
- Omitting the dependency array altogether when a specific, narrower set of triggers was actually
  intended, causing the effect to run far more often than necessary.

## Next

Continue to [cleanup-functions.md](cleanup-functions.md) for the part of an effect that undoes
its own setup.
