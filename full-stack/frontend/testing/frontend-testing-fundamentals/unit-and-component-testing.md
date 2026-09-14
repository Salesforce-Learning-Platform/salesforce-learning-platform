# Unit and Component Testing

## A Unit Test With Vitest

```js
// formatPrice.js
export function formatPrice(cents) {
  return `$${(cents / 100).toFixed(2)}`;
}
```

```js
// formatPrice.test.js
import { expect, test } from "vitest";
import { formatPrice } from "./formatPrice";

test("formats 7999 cents as $79.99", () => {
  expect(formatPrice(7999)).toBe("$79.99");
});

test("formats 0 cents as $0.00", () => {
  expect(formatPrice(0)).toBe("$0.00");
});
```

**Vitest** is a test runner built for Vite-based projects — it reads the project's existing Vite
config automatically, so it needs almost no separate setup. `test()` names one test case, and
`expect(actual).toBe(expected)` is an **assertion** — it fails the test if `actual` doesn't equal
`expected`. This test is a pure unit test: `formatPrice` has no dependencies, so nothing needs
mocking — the base layer of [the-testing-pyramid.md](the-testing-pyramid.md).

## A Component Test With React Testing Library

```jsx
// AddToCartButton.jsx
export function AddToCartButton({ onAddToCart }) {
  return <button onClick={onAddToCart}>Add to Cart</button>;
}
```

```jsx
// AddToCartButton.test.jsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";
import { AddToCartButton } from "./AddToCartButton";

test("calls onAddToCart when clicked", async () => {
  const handleClick = vi.fn();
  render(<AddToCartButton onAddToCart={handleClick} />);

  const button = screen.getByRole("button", { name: "Add to Cart" });
  await userEvent.click(button);

  expect(handleClick).toHaveBeenCalledOnce();
});
```

`render()` mounts the component into a test DOM. `screen.getByRole("button", { name: "Add to
Cart" })` finds the button the same way an assistive-technology user or a sighted user scanning
for that label would — not by a CSS class or an implementation detail. `userEvent.click()`
simulates a real user interaction more faithfully than firing a raw DOM event directly.

## Why Query by Role/Text, Not Implementation Details

```jsx
// AVOID — brittle: breaks the instant the class name changes, even if
// the button still behaves identically for a real user
container.querySelector(".btn-primary");

// PREFER — resilient: matches how a real user actually finds the button
screen.getByRole("button", { name: "Add to Cart" });
```

React Testing Library's guiding principle: **"the more your tests resemble the way your software
is used, the more confidence they can give you."** Querying by an accessible role and visible text
means a test only breaks when something a real user would actually notice changes — an internal
refactor (renaming a CSS class, restructuring the component's internal JSX) doesn't break it,
since none of that is part of what a user experiences.

## Common Mistakes

- Querying by `data-testid` as a first choice instead of a last resort — Testing Library's
  documented hierarchy prefers accessible roles and visible text first, since a `data-testid`
  isn't something a real user interacts with, and over-relying on it can mask components with poor
  accessibility (nothing forces a `data-testid`-based test to have a real accessible name at all).
- Testing a component's internal state directly (e.g., reaching into a component instance) instead
  of asserting on what's actually rendered — the whole point of a component test is to verify
  user-visible behavior, not implementation.
- Writing a unit test for something that's really testing UI behavior (a click, a rendered label) —
  that belongs at the component-test layer, where `render()` and `screen` actually apply.

## Next

Continue to [end-to-end-testing.md](end-to-end-testing.md) to test a full, real user flow across
the whole running application.
