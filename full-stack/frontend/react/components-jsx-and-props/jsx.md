# JSX

## What JSX Is

JSX is a syntax extension that lets you write HTML-like markup directly inside JavaScript. It's
not valid JavaScript on its own — a build tool (like Vite, from
[setting-up-a-react-project.md](../introduction-to-react/setting-up-a-react-project.md)) compiles
it into plain `React.createElement()` function calls before the code ever runs in a browser.

```jsx
const element = <h1>Hello, world!</h1>;

// compiles roughly to:
const element = React.createElement("h1", null, "Hello, world!");
```

## The Three Rules of JSX

**1. Return a single root element.**

```jsx
// Invalid — two sibling elements with no common parent
return (
  <h1>Title</h1>
  <p>Text</p>
);

// Valid — wrapped in a single parent
return (
  <div>
    <h1>Title</h1>
    <p>Text</p>
  </div>
);

// Valid — a Fragment, when an extra wrapping DOM element isn't wanted
return (
  <>
    <h1>Title</h1>
    <p>Text</p>
  </>
);
```

Since JSX compiles to a single function call, a component's return value must be a single element
— a **Fragment** (`<>...</>`) satisfies this rule without adding an unnecessary extra `<div>` to
the actual rendered DOM.

**2. Close every tag.** `<img>` must be written `<img />`; a `<div>` needs an explicit `</div>` —
JSX doesn't allow HTML's occasionally-optional closing tags.

**3. Use camelCase for most attributes.** `class` becomes `className` (since `class` is a reserved
JavaScript word), `onclick` becomes `onClick`, `stroke-width` becomes `strokeWidth` — matching
JavaScript's naming convention rather than HTML's.

## Embedding JavaScript Expressions

```jsx
const name = "Ada";
const items = ["a", "b", "c"];

return (
  <div>
    <p>Hello, {name}</p>
    <p>Item count: {items.length}</p>
    <p>{items.length > 0 ? "Has items" : "Empty"}</p>
  </div>
);
```

Curly braces `{}` embed any JavaScript **expression** (not a statement) directly into JSX —
variables, function calls, arithmetic, ternaries. This is the same expression/statement
distinction from
[conditional-statements.md](../../javascript/conditionals-and-loops/conditional-statements.md):
an `if` statement cannot go inside `{}`, but a ternary expression can.

## Rendering Lists

```jsx
<ul>
  {items.map(item => <li key={item.id}>{item.name}</li>)}
</ul>
```

`.map()` (from [array-methods.md](../../javascript/arrays-and-objects/array-methods.md)) is the
standard way to render a list of elements from an array — each transformed into JSX inline. The
`key` prop is required and covered in depth in the state-and-rerendering module; it's how React
tracks which list item is which across re-renders.

## Common Mistakes

- Trying to embed a statement (`if`, a `for` loop) directly inside `{}` — only expressions are
  valid there; use a ternary or move the logic above the `return`.
- Forgetting `className` and using `class`, which JSX silently ignores rather than erroring on.
- Returning multiple sibling elements with no Fragment or wrapping element, which is a JSX syntax
  error, not a runtime warning.

## Next

Continue to [props.md](props.md) for passing data into a component from its parent.
