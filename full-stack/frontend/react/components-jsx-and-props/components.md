# Components

## A Component Is a Function

```jsx
function Greeting() {
  return <h1>Hello, world!</h1>;
}
```

The most fundamental fact about React: a component is just a JavaScript function (see
[Functions](../../javascript/functions/)) that returns JSX describing what should render. React
components are conventionally named with a capital first letter — this is how React (and JSX's
compiler) distinguishes a custom component (`<Greeting />`) from a plain HTML element (`<div>`).

## Using a Component

```jsx
function App() {
  return (
    <div>
      <Greeting />
      <Greeting />
    </div>
  );
}
```

A component is used (rendered) by writing it as a tag — `<Greeting />` — exactly as introduced in
[what-is-react.md](../introduction-to-react/what-is-react.md). Each usage creates an independent
instance of that component.

## Components Can Contain Logic

```jsx
function TemperatureMessage({ celsius }) {
  const isHot = celsius > 30;
  return <p>{isHot ? "It's hot today!" : "Nice weather."}</p>;
}
```

Because a component is an ordinary function, it can contain any regular JavaScript — variables,
conditionals, calculations — before returning its JSX. This is a direct application of the
conditional/ternary patterns from
[conditional-statements.md](../../javascript/conditionals-and-loops/conditional-statements.md).

## One Component, One Responsibility

A well-designed component typically does one clear thing — displays a user's avatar, renders a
button, shows a list item. Complex UI is built by composing many small, focused components
together (introduced in [what-is-react.md](../introduction-to-react/what-is-react.md) as the
component tree), rather than writing one large component that tries to handle an entire page's
logic and markup at once.

## Common Mistakes

- Naming a component starting with a lowercase letter — JSX interprets a lowercase tag name as a
  plain HTML element, not your custom component, causing a confusing failure.
- Writing one enormous component handling an entire page, rather than breaking it into smaller,
  focused pieces — this makes the component harder to read, test, and reuse.
- Forgetting a component must always return something renderable (or `null`) — a component that
  falls through without an explicit `return` produces `undefined`, which React will complain
  about.

## Next

Continue to [jsx.md](jsx.md) for the syntax rules governing what a component actually returns.
