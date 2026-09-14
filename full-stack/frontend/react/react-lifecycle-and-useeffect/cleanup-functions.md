# Cleanup Functions

## Why Cleanup Is Necessary

Many effects set up something ongoing — a subscription, an event listener (see
[event-listeners.md](../../javascript/events/event-listeners.md)), a timer, a network connection —
that needs to be explicitly torn down, or it keeps running even after it's no longer relevant,
leaking resources and potentially causing bugs (like a callback firing for a component that's no
longer even displayed).

## Returning a Cleanup Function

```jsx
useEffect(() => {
  function handleResize() {
    console.log(window.innerWidth);
  }
  window.addEventListener("resize", handleResize);

  return () => {
    window.removeEventListener("resize", handleResize); // cleanup
  };
}, []);
```

The function *returned* from an effect's setup function is its **cleanup function** — React calls
it automatically at two points: right before the effect runs again (if its dependencies changed),
and when the component unmounts entirely (see [component-lifecycle.md](component-lifecycle.md)).

## Cleanup Runs Before Every Re-run, Not Just on Unmount

This is worth being precise about, since it's a common point of confusion: cleanup isn't only for
"the component is going away" — it also runs immediately before the *next* setup, whenever the
effect's dependencies have changed:

```text
Mount (roomId="general")
  → setup runs: connect to "general"

roomId changes to "random"
  → cleanup runs: disconnect from "general"
  → setup runs again: connect to "random"

Component unmounts
  → cleanup runs: disconnect from "random"
```

This setup → cleanup → setup pattern is exactly what keeps the effect correctly synchronized as
`roomId` changes — without cleanup, changing rooms would leave the old connection open
indefinitely alongside the new one.

## A Concrete Example: Subscriptions

```jsx
useEffect(() => {
  const subscription = dataSource.subscribe(handleData);
  return () => subscription.unsubscribe();
}, [dataSource]);
```

Every subscription-style effect follows this same shape: subscribe in setup, unsubscribe in
cleanup — the pairing should always be symmetric (whatever setup started, cleanup should undo).

## Common Mistakes

- Omitting a cleanup function for an effect that genuinely needs one (a subscription, an event
  listener, a timer), leaking it every time the effect re-runs or the component unmounts.
- Writing a cleanup function that doesn't correctly mirror the setup (removing the wrong listener,
  or forgetting a parameter that must match exactly what was added) — this can silently fail to
  clean up anything at all.
- Being surprised that an effect appears to run twice in development — React intentionally
  mounts, cleans up, and re-mounts components once in development specifically to verify cleanup
  is implemented correctly; this is a deliberate development-only check, not a production bug or a
  sign something is wrong.

## Module Summary

Across this module: every component moves through mount, update, and unmount phases, and
`useEffect` unifies handling for all three into one hook (see
[component-lifecycle.md](component-lifecycle.md)); an effect synchronizes a component with
something external in response to rendering, distinct from an event handler responding to a
specific user action (see [understanding-useeffect.md](understanding-useeffect.md)); the
dependency array must include everything the effect's body actually uses, or it silently operates
on stale, outdated values (see [dependency-array.md](dependency-array.md)); and a cleanup function
undoes an effect's setup, running before every re-run and on unmount — essential for
subscriptions, listeners, and timers to avoid leaking them.
