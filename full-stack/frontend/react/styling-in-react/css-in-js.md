# CSS-in-JS

## Defining Styles as JavaScript

**CSS-in-JS** (using a library like styled-components) defines styles using JavaScript template
literals (see
[template-literals.md](../../javascript/modern-javascript/template-literals.md)), producing a
genuine React component with styles attached:

```jsx
import styled from "styled-components";

const Card = styled.div`
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
`;

const Title = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
`;

function ProductCard({ name, price }) {
  return (
    <Card>
      <Title>{name}</Title>
      <p>${price}</p>
    </Card>
  );
}
```

`styled.div` returns a real React component that renders a `<div>` with the given styles applied,
via a uniquely-generated class name — solving the same naming-collision problem as CSS Modules,
but through a JavaScript-first API instead of separate `.css` files.

## The Real Advantage: Styles as a Function of Props

```jsx
const Card = styled.div`
  border: 1px solid ${props => (props.$isOnSale ? "#e53935" : "#e0e0e0")};
  border-radius: 8px;
  padding: 16px;
`;

function ProductCard({ name, price, isOnSale }) {
  return (
    <Card $isOnSale={isOnSale}>
      <h3>{name}</h3>
      <p>${price}</p>
    </Card>
  );
}
```

This is CSS-in-JS's genuine advantage over CSS Modules: because the style definition is JavaScript,
it can directly interpolate a component's actual prop values into the computed CSS — a red border
when a product is on sale, computed directly from the `isOnSale` prop, without needing to manually
toggle a separate CSS class name the way CSS Modules requires. This extends the "UI as a function
of state/props" model from
[what-is-react.md](../introduction-to-react/what-is-react.md) to visual appearance itself.

## Extending Styles

```jsx
const HighlightedCard = styled(Card)`
  border-color: #1a73e8;
  box-shadow: 0 2px 8px rgba(26, 115, 232, 0.2);
`;
```

`styled(Card)` creates a new styled component that inherits `Card`'s styles and adds to or
overrides them — a composition pattern similar in spirit to CSS class inheritance, but expressed
through actual component composition.

## Advantages and Tradeoffs

| Advantage | Tradeoff |
|---|---|
| Styling is genuinely a function of props, directly | Adds a runtime library dependency (unlike CSS Modules or Tailwind, which add no JS at runtime) |
| Colocation — styles live right next to the component using them | Historically had a real performance cost injecting styles at runtime, though modern versions have improved this significantly |
| Full JavaScript power available in style definitions | A team unfamiliar with the specific library has another API to learn beyond plain CSS |

## Common Mistakes

- Defining a styled component *inside* another component's function body, which recreates the
  styled component on every render — styled components should be defined once, at module scope
  (outside any component function), exactly like the styled-components documentation itself warns.
- Overusing prop-driven dynamic styles for values that could be a plain conditional CSS class
  instead, adding unnecessary runtime computation for no real benefit.
- Forgetting the `$` prefix convention (or an equivalent "transient prop" mechanism) for
  style-only props, which otherwise get passed through to the underlying DOM element and can
  produce invalid HTML attribute warnings.

## Next

Continue to [tailwind-with-react.md](tailwind-with-react.md) for a third, utility-first approach.
