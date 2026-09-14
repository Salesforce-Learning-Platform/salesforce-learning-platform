# `useRef`

## Persisting a Value Without Triggering a Re-render

```jsx
function Timer() {
  const intervalRef = useRef(null);

  function start() {
    intervalRef.current = setInterval(() => console.log("tick"), 1000);
  }
  function stop() {
    clearInterval(intervalRef.current);
  }

  return (
    <>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </>
  );
}
```

`useRef(initialValue)` returns a plain object with a single `.current` property, which persists
across re-renders exactly like state does — but changing `.current` **never** triggers a
re-render on its own. This is `useRef`'s defining difference from `useState`, and exactly why it's
the right tool for values a component needs to remember (like an interval ID) but that have no
bearing on what's actually rendered.

## Accessing a DOM Element Directly

```jsx
function TextInput() {
  const inputRef = useRef(null);

  function focusInput() {
    inputRef.current.focus(); // direct DOM access
  }

  return (
    <>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus the input</button>
    </>
  );
}
```

This is the mechanism behind the "uncontrolled component" pattern from
[controlled-and-uncontrolled-components.md](../component-architecture-and-composition/controlled-and-uncontrolled-components.md):
passing a ref as an element's `ref` prop gives you direct access to the actual underlying DOM node
(from [dom-manipulation](../../javascript/dom-manipulation/)) once it's mounted — useful for
imperative actions React doesn't have a declarative API for, like focusing an input or measuring
an element's size.

## `useRef` vs. `useState` — Choosing Correctly

| | `useState` | `useRef` |
|---|---|---|
| Persists across renders? | Yes | Yes |
| Changing it triggers a re-render? | Yes | No |
| Use for... | Anything that should visibly affect the UI | Values the component needs to remember, with no rendering implication (a timer ID, a DOM reference, a previous value for comparison) |

A common, genuinely useful signal: if changing a value should update what's on screen, it belongs
in state; if it's purely "bookkeeping" the component needs internally, a ref is the more correct
(and slightly more efficient) tool.

## Common Mistakes

- Using `useState` for a value that never actually needs to trigger a re-render (like an interval
  ID), causing unnecessary re-renders every time it's updated.
- Reading or writing `ref.current` during rendering itself (rather than in an event handler or
  effect) — refs are meant for imperative code paths, and reading a ref's value during render can
  produce inconsistent results since it doesn't participate in React's rendering model at all.
- Expecting a UI update after changing `.current` — since it doesn't trigger a re-render, any
  visible change based on a ref's value has to come from something else (like a subsequent state
  update).

## Next

Continue to [usememo.md](usememo.md) for memoizing an expensive computed value.
