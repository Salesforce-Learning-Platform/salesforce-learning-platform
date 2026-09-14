# Context Performance

## Every Consumer Re-renders on Change

This is the single most important thing to understand about Context, and it directly affects
architecture decisions: when a context's value changes, **every component consuming that context
re-renders** — not just the ones that visually display the part of the value that actually
changed.

```jsx
const AuthContext = createContext(null);

function App() {
  const [user, setUser] = useState({ name: "Ada", notificationCount: 3 });
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      <NotificationBadge /> {/* uses notificationCount */}
      <UserAvatar />           {/* uses only user.name — but STILL re-renders when notificationCount changes */}
    </AuthContext.Provider>
  );
}
```

If `notificationCount` updates every few seconds, `UserAvatar` re-renders every single time too,
even though it never displays `notificationCount` at all — because from Context's perspective, the
*entire* `value` object changed (a new object reference, per
[objects.md](../../javascript/arrays-and-objects/objects.md)'s reference-comparison rules), and
every consumer of that context is notified, with no built-in way to subscribe to just part of it.

## Why This Differs from Ordinary Props

Recall [how-rerendering-works.md](../state-and-rerendering-logic/how-rerendering-works.md): a
component only re-renders when its *own* props or state change. Context sidesteps that mechanism
entirely — a consumer re-renders in response to the context's value changing, independent of
whether it receives any props from the component holding that state at all.

## Mitigating This: Splitting Contexts

```jsx
const UserContext = createContext(null);
const NotificationContext = createContext(null);

function App() {
  const [user, setUser] = useState({ name: "Ada" });
  const [notificationCount, setNotificationCount] = useState(3);

  return (
    <UserContext.Provider value={user}>
      <NotificationContext.Provider value={notificationCount}>
        <NotificationBadge /> {/* only re-renders when notificationCount changes */}
        <UserAvatar />           {/* only re-renders when user changes */}
      </NotificationContext.Provider>
    </UserContext.Provider>
  );
}
```

Splitting one large, frequently-changing context into several smaller, independently-updating
ones directly solves the over-re-rendering problem — each consumer now only re-renders when the
*specific* context it actually reads from changes, exactly the granularity the single combined
context lacked.

## Common Mistakes

- Bundling frequently-changing data (a live notification count, real-time data) into the same
  context as rarely-changing data (the logged-in user's identity), causing unrelated components to
  re-render far more often than necessary.
- Assuming `memo` (from the Performance Optimization module) automatically prevents this — `memo`
  compares props, not context values; a component consuming a changed context re-renders
  regardless of whether it's wrapped in `memo`.
- Splitting every conceivable value into its own separate context reflexively, adding unnecessary
  complexity for values that genuinely always change together anyway.

## Next

Continue to
[global-state-patterns.md](global-state-patterns.md) to see when Context is the right tool at all,
versus a dedicated state-management library.
