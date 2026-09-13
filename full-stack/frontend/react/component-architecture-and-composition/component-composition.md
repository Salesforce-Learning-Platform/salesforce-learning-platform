# Component Composition

## The Problem: Prop Drilling

As an application grows, a piece of data or a callback often needs to travel through several
layers of components that don't actually use it themselves — only to hand it down to a
deeply-nested child that does. This is called **prop drilling**:

```jsx
function App() {
  const [user, setUser] = useState(null);
  return <Layout user={user} />;
}
function Layout({ user }) {
  return <Sidebar user={user} />; // Layout doesn't use `user` itself
}
function Sidebar({ user }) {
  return <UserBadge user={user} />; // neither does Sidebar
}
function UserBadge({ user }) {
  return <p>{user.name}</p>; // only THIS component actually needs it
}
```

Every intermediate component (`Layout`, `Sidebar`) has to accept and forward a prop purely for a
descendant's benefit — adding noise and coupling every layer to a piece of data it has no real use
for itself.

## Composition as the Fix

```jsx
function App() {
  const [user, setUser] = useState(null);
  return (
    <Layout>
      <Sidebar>
        <UserBadge user={user} />
      </Sidebar>
    </Layout>
  );
}
function Layout({ children }) { return <div className="layout">{children}</div>; }
function Sidebar({ children }) { return <aside>{children}</aside>; }
```

By passing `<UserBadge user={user} />` down through `children` instead of as a named prop at every
level, `Layout` and `Sidebar` no longer need to know `user` exists at all — they just render
whatever they're given. This is the "composition over configuration" idea introduced in
[component-reusability.md](../components-jsx-and-props/component-reusability.md), applied
specifically to the deep-nesting problem.

## Configuration vs. Composition

| | Configuration (more props) | Composition (children/slots) |
|---|---|---|
| Approach | Add a boolean/option prop for every variation | Let the parent decide what content goes where |
| Scales well when... | The variations are genuinely few and well-understood | The possible contents are open-ended or unpredictable |
| Downside | Prop list grows indefinitely as new needs appear | Slightly more indirection to read at a glance |

Neither is universally correct — a component with two or three genuinely fixed variants
(`size="small" | "large"`) is reasonably configured with props; a component whose contents could
be almost anything (a modal, a card, a layout wrapper) is better composed.

## Multiple "Slots" via Named Props

```jsx
function PageLayout({ header, sidebar, content }) {
  return (
    <div className="page">
      <header>{header}</header>
      <aside>{sidebar}</aside>
      <main>{content}</main>
    </div>
  );
}

<PageLayout
  header={<Header />}
  sidebar={<Sidebar />}
  content={<Article />}
/>
```

`children` handles a single "main content" slot well; when a component genuinely needs multiple
independent content areas, passing separate JSX elements as regular named props (not restricted to
`children`) is the standard way to express that — each prop is still just a piece of JSX, passed
exactly like any other value.

## Common Mistakes

- Adding another boolean prop to handle each new variation of a component instead of recognizing
  the pattern has outgrown configuration and needs composition instead.
- Drilling a prop through several components that don't use it, rather than restructuring with
  composition (or, for genuinely global data touched by many unrelated components, the Context API
  covered in the Global State Management module).
- Overusing multiple named JSX-element props when a single `children` slot would already express
  the same structure more simply.

## Next

Continue to [children-prop.md](children-prop.md) for a closer look at `children` specifically.
