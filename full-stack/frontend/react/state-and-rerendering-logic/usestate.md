# `useState`

## Basic Syntax

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

`useState(initialValue)` returns a pair — the current value and a function to update it —
conventionally destructured (see
[destructuring.md](../../javascript/arrays-and-objects/destructuring.md)) via array destructuring
into `[value, setValue]`. Calling `setCount` both updates the stored value *and* triggers a
re-render, solving both problems identified in
[understanding-state.md](understanding-state.md).

## Never Mutate State Directly

```jsx
const [user, setUser] = useState({ name: "Ada" });

user.name = "Grace"; // WRONG — mutates the object directly; React never notices
setUser({ ...user, name: "Grace" }); // correct — a NEW object, triggers a re-render
```

This is a direct application of the immutability discipline from
[object-methods.md](../../javascript/arrays-and-objects/object-methods.md): React determines
whether to re-render partly by comparing whether the state value changed, and it does this
comparison efficiently, by reference — mutating the existing object in place doesn't produce a new
reference, so React has no reliable way to detect that anything changed at all. Always create a
new object/array (via spread, `map`, `filter`, etc.) rather than mutating the existing one.

## The Updater-Function Form

```jsx
setCount(count + 1);        // "direct" form — uses the value of `count` at render time
setCount(c => c + 1);         // "updater function" form — always operates on the LATEST value
```

```jsx
function handleClick() {
  setCount(count + 1); // both calls read the SAME `count` from this render
  setCount(count + 1); // → count only increases by 1, not 2
}

function handleClickFixed() {
  setCount(c => c + 1); // each call operates on the latest value, including
  setCount(c => c + 1); // the result of the previous call → increases by 2
}
```

This exact scenario is why the README's knowledge check flags it: when queuing multiple updates to
the same piece of state within one handler, the updater-function form is the reliable choice —
covered in full in
[batching-state-updates.md](batching-state-updates.md).

## Lazy Initial State

```jsx
const [value, setValue] = useState(() => expensiveComputation());
```

Passing a function instead of a plain value defers the expensive computation so it only runs once,
on the component's first render — passing `expensiveComputation()` directly would re-run it on
every single re-render, even though only the very first result is ever actually used as the
initial state.

## Common Mistakes

- Mutating state directly instead of creating a new value — this is the single most common
  `useState` bug, and it fails silently (no error, just a UI that doesn't update).
- Reaching for the direct form (`setCount(count + 1)`) when queuing multiple updates to the same
  state in one handler, and being confused when they don't stack as expected.
- Passing an already-invoked expensive computation (`useState(expensiveComputation())`) instead of
  a function reference (`useState(() => expensiveComputation())`) for lazy initialization.

## Next

Continue to [how-rerendering-works.md](how-rerendering-works.md) to see exactly what happens after
`setCount` is called.
