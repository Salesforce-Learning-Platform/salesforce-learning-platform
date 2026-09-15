# 🤖 React Compiler — An Introduction

## What Manual Memoization Looked Like Before

```jsx
// The pattern from performance-optimization-in-react.md
const total = useMemo(() => calculateTotal(items), [items]);
const handleClick = useCallback(() => onSelect(id), [id, onSelect]);
const MemoizedRow = React.memo(ProductRow);
```

[Performance Optimization in React](../performance-optimization-in-react/) taught `useMemo`,
`useCallback`, and `React.memo` as the manual tools for preventing unnecessary recalculation and
re-rendering — each one requiring a developer to correctly identify *what* needs memoizing and
*which* dependencies to track by hand.

## What the Compiler Automates

The **React Compiler** analyzes a component's actual code at build time and automatically applies
the equivalent of `useMemo`, `useCallback`, and `React.memo` wherever it determines they'd help —
without a developer writing any of those calls, or maintaining their dependency arrays by hand at
all.

```jsx
// With the compiler: write this...
function ProductList({ items }) {
  const total = calculateTotal(items);
  const handleClick = () => onSelect(id);
  return <ProductRow onClick={handleClick} total={total} />;
}

// ...and the compiler behaves as if you'd manually written the
// useMemo/useCallback/React.memo version, without you writing it
```

## Why This Is a Genuine Shift in How Performance Is Taught

Manual memoization is a real, well-known source of subtle bugs: a forgotten or incorrect dependency
in a `useMemo`/`useCallback` array silently produces a stale value or a broken optimization, exactly
the class of mistake
[performance-optimization-in-react.md](../performance-optimization-in-react/) already warns
about. The compiler's entire premise is removing that error-prone manual bookkeeping — the
optimization concepts from that module remain conceptually correct and worth understanding, but the
*hand-written implementation* of them becomes largely unnecessary once the compiler is in use.

## Current Status: Experimental and Opt-In

The React Compiler is currently **experimental** and **opt-in** — it requires deliberate build-tool
setup, and can be adopted **incrementally** across an existing codebase rather than needing to be
turned on everywhere at once. It doesn't replace `useState`, `useEffect`, or any other hook
covered throughout this domain — its scope is specifically memoization, nothing broader.

## Why Understanding Manual Memoization Still Matters

Even once the compiler becomes standard, understanding *why* memoization exists — the actual
problem of unnecessary recalculation and re-rendering, per
[performance-optimization-in-react.md](../performance-optimization-in-react/) — remains valuable:
it's what lets a developer reason correctly about a component's performance, debug an issue the
compiler doesn't (or can't yet) catch, and understand legacy code still written the manual way.

## Common Mistakes

- Assuming the React Compiler eliminates the need to understand memoization conceptually — it
  automates the *manual implementation*, not the underlying reasoning about why unnecessary
  re-renders happen in the first place.
- Assuming the compiler is already a stable, default-on part of React — it remains experimental
  and opt-in as of this module's writing, requiring explicit setup.
- Expecting the compiler to optimize things outside its actual scope (state management, data
  fetching) — it specifically targets memoization, not every possible performance concern.

## Module Summary

Across this module: **`<Suspense>`** provides declarative, component-level loading states,
triggered specifically by `use()`-based promise reading rather than `useEffect`-based fetching (see
[suspense-deep-dive.md](suspense-deep-dive.md)); **Server Components vs. Client Components** is a
React-level architectural shift making server-only rendering the default, covered in full by the
existing Next.js content this module cross-links to rather than repeats (see
[server-components-vs-client-components.md](server-components-vs-client-components.md)); **Actions**
simplify form submission by wrapping async work in a transition, automatically tracking pending
state (see [actions-and-form-handling.md](actions-and-form-handling.md)); **`useActionState`** and
**`useFormStatus`** remove further manual state and prop-drilling for form results and pending
status (see [useactionstate-and-useformstatus.md](useactionstate-and-useformstatus.md));
**`useOptimistic`** shows an assumed result immediately for instant-feeling, usually-successful
interactions (see [optimistic-ui-with-useoptimistic.md](optimistic-ui-with-useoptimistic.md)); the
**`use()`** hook reads a promise or context directly during render, uniquely callable
conditionally unlike every other hook (see [the-use-hook.md](the-use-hook.md)); and the
**React Compiler** automates the manual memoization taught in the Performance module, currently as
an experimental, opt-in, incrementally-adoptable tool.
