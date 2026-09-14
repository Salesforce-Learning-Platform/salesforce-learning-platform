# The Context API

## Creating a Context

```jsx
import { createContext } from "react";

const AuthContext = createContext(null);
```

`createContext(defaultValue)` creates a context object — `defaultValue` is only used if a
component consumes it with no matching provider above it anywhere in the tree.

## Providing a Value

```jsx
function App() {
  const [user, setUser] = useState(null);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      <Header />
      <Dashboard />
    </AuthContext.Provider>
  );
}
```

`AuthContext.Provider` wraps a part of the component tree and makes `value` available to *every*
descendant, no matter how deeply nested — `Header` and `Dashboard`, and anything they render, can
all read the current user without it being passed down as a prop through every intermediate layer.
(React 19 also supports a shorthand, rendering the context itself directly as
`<AuthContext value={...}>` — functionally identical, just less verbose; `.Provider` remains fully
supported and is what most existing codebases and tutorials use.)

## Consuming a Context

```jsx
import { useContext } from "react";

function Header() {
  const { user } = useContext(AuthContext);
  return <header>{user ? `Welcome, ${user.name}` : "Please log in"}</header>;
}
```

`useContext(AuthContext)` reads the nearest matching `Provider`'s current value, from anywhere in
the tree below it — no props were passed to `Header` at all; it reached directly into the context
for exactly the data it needed.

## The Complete Picture

```jsx
const AuthContext = createContext(null);

function App() {
  const [user, setUser] = useState(null);
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      <Header />
      <Dashboard />
    </AuthContext.Provider>
  );
}

function Header() {
  const { user } = useContext(AuthContext);
  return <header>{user ? `Welcome, ${user.name}` : "Please log in"}</header>;
}

function LoginButton() {
  const { setUser } = useContext(AuthContext);
  return <button onClick={() => setUser({ name: "Ada" })}>Log In</button>;
}
```

`Header` and `LoginButton` might be nested arbitrarily deep inside `Dashboard`, with several
intermediate components between them and `App` — none of those intermediate components need to
know `AuthContext` exists at all, exactly solving the prop-drilling problem from
[component-composition.md](../component-architecture-and-composition/component-composition.md)
for genuinely shared, cross-cutting data rather than passed-down content.

## Common Mistakes

- Wrapping the entire app in a context provider for data that's only actually needed by a small,
  localized part of the tree — unnecessarily widening the provider's scope beyond where it's
  needed.
- Calling `useContext` for a context with no matching provider above it in the tree, silently
  falling back to the (often unhelpful) default value passed to `createContext`.
- Forgetting that context updates cause every consumer to re-render, regardless of which specific
  part of the value object actually changed — covered in depth next.

## Next

Continue to [context-performance.md](context-performance.md) for exactly what that re-render
behavior means in practice.
