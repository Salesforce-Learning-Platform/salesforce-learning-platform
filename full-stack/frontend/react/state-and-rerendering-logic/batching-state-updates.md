# Batching State Updates

## The Problem Batching Solves

```jsx
function handleClick() {
  setCount(count + 1);
  setFlag(true);
  setName("Ada");
}
```

Without batching, each of these three `set` calls could trigger its own separate re-render — three
re-renders for one click, most of them showing a transiently incomplete, inconsistent state (count
updated but not flag yet, for instance) that was never actually meant to be visible.

## What React Actually Does

React **batches** multiple state updates that occur within the same event handler (and, in modern
React, within most other contexts too) into a single re-render, applied once all the handler's
synchronous code has finished running:

```jsx
function handleClick() {
  setCount(count + 1); // queued, not applied yet
  setFlag(true);          // queued
  setName("Ada");           // queued
  // → React performs exactly ONE re-render here, with all three updates applied together
}
```

This is directly analogous to the microtask/macrotask batching behavior from
[the event loop](../../javascript/event-loop/) — React groups related work together rather than
processing each piece the instant it's requested, for both correctness (never showing a
half-updated state) and performance (avoiding redundant re-renders).

## Why the Updater-Function Form Matters Here

As introduced in [usestate.md](usestate.md), calling `setCount(count + 1)` twice in the same
batched handler uses the *same* `count` value both times (the one from the current render), so the
count only increases by 1 — not because batching itself is the direct cause, but because the
direct form captures a value that doesn't change between the two calls within that same render:

```jsx
function handleClick() {
  setCount(count + 1); // reads count from THIS render — say, 0 → queues "set to 1"
  setCount(count + 1); // reads the SAME count (still 0 in this render) → queues "set to 1" again
}
// final count: 1, not 2

function handleClickFixed() {
  setCount(c => c + 1); // queues: "take whatever the latest value is, add 1"
  setCount(c => c + 1); // queues the same instruction again, but it will run against the
}                          // result of the first queued update
// final count: 2
```

The updater-function form queues an *instruction* ("add 1 to whatever it ends up being") rather
than a computed *value* based on a single render's stale snapshot — which is exactly why it
produces the correct cumulative result when multiple updates to the same state are queued
together.

## Common Mistakes

- Expecting to read an updated state value immediately after calling its setter, within the same
  function — the update is queued, and the current render's `count` variable still holds the old
  value until the next render actually happens.
- Using the direct form (`setCount(count + 1)`) when queuing several updates to the same state
  variable in one handler, producing a smaller total change than intended.
- Assuming batching means updates are lost or skipped — they're all applied, just together, in one
  consolidated re-render rather than one re-render per call.

## Module Summary

Across this module: state is data a component owns that persists across re-renders and triggers
one when changed — solving the two problems a plain variable can't (see
[understanding-state.md](understanding-state.md)); `useState` implements this, and must never be
mutated directly, with the updater-function form needed to reliably queue multiple updates to the
same value (see [usestate.md](usestate.md)); a re-render is React recalculating a component's
output, cascading to children by default, but not necessarily touching the real DOM at all (see
[how-rerendering-works.md](how-rerendering-works.md)); and React batches multiple state updates
within a handler into one re-render, for both correctness and performance (this file).
