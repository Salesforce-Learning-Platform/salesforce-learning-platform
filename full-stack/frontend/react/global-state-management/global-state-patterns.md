# Global State Patterns

## Context Is Not the Automatic Default

React's own documentation is explicit about this, and it's worth internalizing: before reaching
for Context, first consider whether plain props, or composition via `children`
(from [component-composition.md](../component-architecture-and-composition/component-composition.md)),
would solve the problem just as well. Context adds real re-render behavior (from
[context-performance.md](context-performance.md)) that plain prop-passing doesn't — it's the right
tool specifically once data is genuinely needed by many, unpredictably-nested components, not a
default first choice for any shared value.

## A Practical Decision Framework

| Situation | Recommended approach |
|---|---|
| A value used by one component and maybe its direct children | Plain props |
| A generic wrapper needing to render arbitrary content | `children` (composition) |
| Data genuinely needed by many components at unpredictable depths (logged-in user, theme) | Context |
| Frequently-changing, complex global state needing time-travel debugging, middleware, or strict update patterns across a large team | A dedicated library (Redux, covered next) |

## Colocating Context with a Custom Hook

```jsx
// AuthContext.jsx
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
}
```

```jsx
// Usage anywhere in the app
function Header() {
  const { user } = useAuth(); // no need to import AuthContext or call useContext directly
}
```

This pattern — a provider component plus a custom hook (from
[custom-hooks.md](../react-hooks/custom-hooks.md)) wrapping `useContext` — is the standard,
idiomatic way to package a context for reuse: consumers never interact with `AuthContext` or
`useContext` directly, and the hook can throw a clear, helpful error if it's ever called outside
its provider, rather than silently returning the default value from
[context-api.md](context-api.md).

## When Context Genuinely Isn't Enough

For state that's updated very frequently, needs middleware (logging every change, for instance),
or benefits from strict, centralized update patterns across a large team working on the same
application, a dedicated state-management library provides guarantees Context alone doesn't —
covered next in [State Management Using Redux](../state-management-using-redux/).

## Common Mistakes

- Reaching for Context as the default solution to any shared-state need, before genuinely
  considering whether plain props or composition would already solve it more simply.
- Exposing the raw `AuthContext` and requiring every consumer to call `useContext(AuthContext)`
  directly, instead of wrapping it in a purpose-built custom hook.
- Assuming Context alone is a full state-management solution equivalent to a dedicated library —
  it provides a way to *share* state, not built-in tooling for debugging, middleware, or
  centralized update logic.

## Module Summary

Across this module: Context solves prop drilling for cross-cutting data by making a value
available to any descendant without passing it through every intermediate component (see
[context-api.md](context-api.md)); every consumer of a context re-renders when its value changes,
regardless of which part of that value actually changed, which is why splitting large, mixed-update
contexts into smaller ones matters for performance (see [context-performance.md](context-performance.md));
and Context should be reached for deliberately — after plain props and composition genuinely don't
fit — typically wrapped in a provider-plus-custom-hook pattern, with a dedicated library reserved
for state needing more than Context alone provides.
