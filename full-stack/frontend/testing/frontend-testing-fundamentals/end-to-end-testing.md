# End-to-End Testing

## What Makes a Test "End-to-End"

An end-to-end (e2e) test drives a **real browser** against the **real, running application** —
navigating pages, clicking real buttons, filling real forms — the way an actual user would,
without mocking anything. It's the top layer of
[the-testing-pyramid.md](the-testing-pyramid.md): the fewest tests, but the highest confidence,
since nothing about the real system is faked.

## A Playwright Test

```js
// checkout.spec.js
import { test, expect } from "@playwright/test";

test("a user can add an item to the cart and see it in checkout", async ({ page }) => {
  await page.goto("https://shop.example.com/products/mechanical-keyboard");

  await page.getByRole("button", { name: "Add to Cart" }).click();
  await page.getByRole("link", { name: "Cart" }).click();

  await expect(page.getByText("Mechanical Keyboard")).toBeVisible();
  await expect(page.getByText("1 item")).toBeVisible();
});
```

**Playwright** bundles a test runner, assertions, and browser automation together, and can run the
same test across Chromium, WebKit, and Firefox. The structure mirrors the three-step pattern every
e2e test follows: **navigate** (`page.goto`), **interact** (`.click()`), and **assert** (`expect(...).toBeVisible()`)
— proving the actual user-facing outcome happened, not just that some internal function ran
correctly.

## When an E2E Test Is Actually Worth It

Given the cost described in [the-testing-pyramid.md](the-testing-pyramid.md) — slow, occasionally
flaky, expensive to maintain — e2e tests earn their place specifically for:

- **Critical business flows**: checkout, account creation, login — the paths where a silent
  regression would directly cost the business real users or revenue.
- **Genuine cross-system integration**: verifying the frontend actually talks correctly to a real
  backend and database, something no unit or component test (which mocks those dependencies) can
  prove on its own.
- **Flows spanning multiple pages or a full user journey**: a single component test can't verify
  that navigating from a product page to checkout actually carries the cart state correctly across
  page transitions.

## When Not To

A single component's internal behavior — does a form show a validation error for an invalid email,
does a dropdown open on click — is almost always better and more cheaply verified at the component
layer with [React Testing Library](unit-and-component-testing.md), reserving the far more
expensive e2e layer only for what genuinely requires a real, full system to verify.

## Reducing Flakiness

```js
// AVOID — a fixed wait guesses at timing and is a common source of
// both flakiness (too short) and wasted time (too long)
await page.waitForTimeout(2000);

// PREFER — Playwright's assertions auto-retry until the condition is
// true or a timeout elapses, waiting exactly as long as actually needed
await expect(page.getByText("Added to cart")).toBeVisible();
```

Playwright's built-in assertions (`expect(locator).toBeVisible()`, etc.) automatically retry until
the expected state appears, which is the primary defense against the flakiness e2e tests are
otherwise prone to — a fixed, arbitrary wait is almost always the wrong tool.

## Common Mistakes

- Writing e2e tests for every feature by default, rather than reserving them for flows that
  genuinely need full-system confidence — quickly leading to the slow, flaky "ice cream cone"
  anti-pattern from [the-testing-pyramid.md](the-testing-pyramid.md).
- Using fixed-duration waits (`waitForTimeout`) instead of Playwright's auto-retrying assertions,
  producing tests that are simultaneously slower than necessary and still occasionally flaky.
- Letting e2e tests depend on shared, mutable test data (the same test account, the same product
  inventory) that other tests running in parallel might modify, causing intermittent, hard-to-
  reproduce failures unrelated to any real bug.

## Module Summary

Across this module: the **testing pyramid** — unit (base), integration/component (middle), and
end-to-end (top) — recommends writing many fast, narrow tests and very few slow, broad ones,
because of a direct speed-vs-confidence tradeoff at each layer (see
[the-testing-pyramid.md](the-testing-pyramid.md)); **Vitest** covers fast unit tests for isolated
logic, while **React Testing Library**'s `render`/`screen`/`userEvent` test components by querying
the way a real user would — role and visible text, not implementation details (see
[unit-and-component-testing.md](unit-and-component-testing.md)); and **Playwright** drives a real
browser against the real running application for end-to-end tests, reserved for critical,
full-system user flows where their higher cost is genuinely worth the confidence they provide.
