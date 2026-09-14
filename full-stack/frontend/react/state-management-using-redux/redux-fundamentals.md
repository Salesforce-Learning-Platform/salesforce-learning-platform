# Redux Fundamentals

## The Core Principles

Redux organizes application state around three strict rules:

1. **A single store**: the entire application's state lives in one object tree, rather than
   scattered across many separate `useState` calls or contexts.
2. **State is read-only**: the only way to change state is to dispatch an **action** — a plain
   object describing what happened (never mutating state directly).
3. **Changes are made with pure functions**: a **reducer** takes the current state and an action,
   and returns a *new* state — no side effects, no mutation, exactly the never-mutate discipline
   from [usestate.md](../state-and-rerendering-logic/usestate.md), enforced strictly.

```text
Component dispatches an action (e.g., "add item to cart")
              │
              ▼
Reducer: (currentState, action) → newState (a pure function, no side effects)
              │
              ▼
Store updates, notifying every subscribed component
              │
              ▼
Components re-render with the new state
```

## Why These Strict Rules Exist

Unlike Context (from [context-api.md](../global-state-management/context-api.md)), which simply
shares a value, Redux's strictness buys real, concrete guarantees: because reducers are pure
functions with no side effects, Redux DevTools can record every single action and let a developer
literally step backward and forward through an application's entire state history ("time-travel
debugging") — something that's only possible because state changes are guaranteed predictable and
side-effect-free.

## When Redux Is (and Isn't) the Right Tool

| Situation | Fits |
|---|---|
| A small app with a handful of shared values | Context, or even plain props — Redux adds real overhead for a genuinely simple need |
| A large team needing a strict, consistent, auditable pattern for state changes | Redux |
| Complex, deeply interrelated state changing frequently (a shopping cart, a multi-step order flow with many possible transitions) | Redux |
| State that's mostly server data (an order history) | React Query (from
[react-query.md](../server-state-and-api-integration/react-query.md)), not Redux — Redux is for
client-owned application state, not caching server responses |

Redux and Context aren't strictly competing tools — many real applications use Context for a few
simple, rarely-changing values (like a theme) and Redux for genuinely complex, frequently-updated
application state (like a shopping cart), matching each tool to the specific need it's actually
suited for.

## Common Mistakes

- Reaching for Redux by default for every project, adding real complexity and boilerplate to an
  application simple enough that Context or plain state would have been sufficient.
- Using Redux to cache and manage server-fetched data, duplicating what React Query already does
  correctly and more simply for exactly that category of state.
- Assuming Redux and Context are mutually exclusive choices — many real applications use both,
  each for the specific category of state it's best suited for.

## Next

Continue to [actions-reducers-and-store.md](actions-reducers-and-store.md) to build a real
feature — a shopping cart — with these principles.
