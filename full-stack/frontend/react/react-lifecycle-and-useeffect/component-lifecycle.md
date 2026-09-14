# Component Lifecycle

## Three Phases

Every component instance moves through three conceptual phases over its life:

```text
Mount              Update                Unmount
(first appears)    (re-renders due to    (removed from
                    state/prop changes)   the UI entirely)
     │                    │                     │
     ▼                    ▼                     ▼
render()            render() again          (component instance
                     (see how-rerendering-    is discarded)
                      works.md)
```

- **Mount**: the component is created and rendered for the first time — its state is initialized
  (`useState`'s initial value is used exactly once, here).
- **Update**: the component re-renders in response to a state or prop change (see
  [how-rerendering-works.md](../state-and-rerendering-logic/how-rerendering-works.md)) — this can
  happen any number of times, including zero.
- **Unmount**: the component is removed from the UI (its parent stops rendering it) — its state is
  discarded entirely; if the same component type renders again later in the same location, it's a
  fresh mount with fresh state.

## Why This Matters for Effects

`useEffect` (covered in [understanding-useeffect.md](understanding-useeffect.md)) is defined in
terms of these phases: by default, an effect's setup logic runs after each render where a
dependency changed (covering both mount and relevant updates), and its cleanup function runs
before the component unmounts (or before the effect runs again with new dependency values).
Understanding the three phases is what makes the setup/cleanup timing in the rest of this module
make sense, rather than needing to be memorized as an arbitrary rule.

## Class Components — Historical Context

Before hooks existed (React 16.8, 2019), lifecycle logic was expressed through named methods on
class components — `componentDidMount`, `componentDidUpdate`, `componentWillUnmount` — matching
these same three phases explicitly. `useEffect` unifies mount, relevant updates, and unmount
handling into a single hook rather than three separate methods; you'll still encounter class
components and these lifecycle method names in older React codebases and documentation, worth
recognizing even though function components with hooks are now the standard, recommended approach
for new code.

## Common Mistakes

- Assuming "mount" and "update" require fundamentally different code paths in modern React —
  `useEffect`'s dependency array (see [dependency-array.md](dependency-array.md)) handles both
  uniformly, without needing separate logic for each phase the way class lifecycle methods did.
- Forgetting that unmounting discards a component's state entirely — a component that mounts again
  later (even with the same props) starts completely fresh, not from where it left off.
- Encountering `componentDidMount`/`componentWillUnmount` in older code or tutorials and being
  confused about how they map to hooks — they correspond to the setup and cleanup portions of
  `useEffect`, covered next.

## Next

Continue to
[understanding-useeffect.md](understanding-useeffect.md) for the hook that implements this
lifecycle-driven behavior in function components.
