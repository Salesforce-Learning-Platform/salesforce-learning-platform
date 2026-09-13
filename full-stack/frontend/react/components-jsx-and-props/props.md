# Props

## Passing Data Into a Component

**Props** ("properties") are how a parent component passes data to a child — conceptually similar
to HTML attributes, but capable of holding any JavaScript value: strings, numbers, objects, arrays,
even functions.

```jsx
function Avatar({ name, size }) {
  return <img src={`/avatars/${name}.png`} width={size} height={size} />;
}

<Avatar name="ada" size={100} />
```

## Destructuring Props

```jsx
function Avatar({ name, size }) { /* ... */ }        // destructured directly in the parameter
function Avatar(props) { return props.name; }          // equivalent, without destructuring
```

Destructuring props directly in the function signature (see
[destructuring.md](../../javascript/arrays-and-objects/destructuring.md)) is the overwhelmingly
common convention in real React code — it makes exactly which props a component actually uses
visible at a glance, without reading the whole function body.

## Default Values

```jsx
function Avatar({ name, size = 100 }) {
  return <img src={`/avatars/${name}.png`} width={size} height={size} />;
}

<Avatar name="ada" />        // size defaults to 100
<Avatar name="ada" size={50} /> // size is 50
```

This is the identical default-parameter pattern from
[parameters-and-return-values.md](../../javascript/functions/parameters-and-return-values.md),
applied to a destructured props object.

## Props Are Read-Only

```jsx
function Avatar({ size }) {
  size = 200; // WRONG — never reassign a prop
  return <img width={size} />;
}
```

This is the single most important rule in this file: **a component must never modify the props it
receives.** Props represent data owned by the parent; a child that mutates them creates
inconsistent, hard-to-predict behavior. If a value genuinely needs to change over time in response
to user interaction, that's precisely what **state** (covered in the next module) is for — props
flow down, and are treated as an immutable snapshot from the receiving component's perspective.

## The `children` Prop

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>;
}

<Card>
  <h2>Title</h2>
  <p>Content goes here.</p>
</Card>
```

Anything nested between a component's opening and closing tags is automatically passed as a
special `children` prop — this is what enables composition patterns like a generic `Card` or
`Modal` wrapper that has no idea in advance what content it will actually contain.

## Spreading Props

```jsx
<Avatar {...userProps} />
```

The spread operator (from
[object-methods.md](../../javascript/arrays-and-objects/object-methods.md)) can forward an entire
object of props at once — convenient when passing along many props unchanged, though explicit
individual props remain more readable and are generally preferred when only a few are actually
needed.

## Common Mistakes

- Mutating a prop directly inside a component — this is a genuine bug source, not just a style
  issue; use state for any value that needs to change.
- Forgetting the `children` prop exists and building custom "content" props for every wrapper
  component instead of using the standard, built-in pattern.
- Over-using prop spreading, obscuring exactly which props a component actually expects and uses.

## Next

Continue to [component-reusability.md](component-reusability.md) to design components that use
these tools well.
