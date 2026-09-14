# Frontend Testing Fundamentals

## Purpose

Every module up to this point has taught you to build a UI. This module teaches you to trust that
it keeps working — the discipline of automated frontend testing, framework-agnostic in its core
ideas but illustrated concretely with the tools ([Vitest](https://vitest.dev/),
[React Testing Library](https://testing-library.com/docs/react-testing-library/intro/), and
[Playwright](https://playwright.dev/)) most commonly paired with the [React](../../react/) and
[Next.js](../../nextjs/) domains you've already completed.

## Learning Objectives

- Explain the testing pyramid: its three layers, why the shape is a pyramid, and the speed-vs-confidence
  tradeoff at each layer.
- Write a unit test and a component test, including React Testing Library's user-centric querying
  philosophy.
- Write a basic end-to-end test with Playwright, and explain when an e2e test is worth its cost.
- Decide which layer of the pyramid a given piece of new functionality actually needs tested.

## Prerequisites

- The [React domain](../../react/) — component tests in this module test real React components.
- [Asynchronous Programming and Modules](../../javascript/asynchronous-programming-and-modules/) —
  test code frequently deals with promises and asynchronous UI updates.

## Files in This Module

| File | Covers |
|---|---|
| [the-testing-pyramid.md](the-testing-pyramid.md) | The three layers, the pyramid shape, and the speed-vs-confidence tradeoff |
| [unit-and-component-testing.md](unit-and-component-testing.md) | Vitest for unit tests, React Testing Library for component tests |
| [end-to-end-testing.md](end-to-end-testing.md) | Playwright, real user-flow tests, and when e2e tests are worth it |

## When to Deep-Dive vs. Skim

Deep-dive [the-testing-pyramid.md](the-testing-pyramid.md) — the pyramid is a *decision framework*,
not trivia: understanding *why* the shape is a pyramid (and what goes wrong in its "inverted"
form) is what actually helps you decide which layer to test something at, on every future feature
you build.

## Quick Knowledge Check

<details>
<summary>Why does the testing pyramid recommend far more unit tests than end-to-end tests, rather than an even split?</summary>

Because of a direct speed-vs-confidence tradeoff: unit tests are fast and cheap to write and run
(thousands can run in minutes), so they're the efficient place to catch the bulk of logic bugs.
End-to-end tests give the highest confidence — they exercise the real system — but are slow,
expensive to maintain, and prone to flakiness, so they're reserved for the critical user flows
that genuinely need that level of assurance. See [the-testing-pyramid.md](the-testing-pyramid.md).

</details>

<details>
<summary>Why does React Testing Library encourage querying by text or accessible role instead of a CSS class or component internals?</summary>

Because a real user doesn't know or care about a component's internal implementation, class names,
or state — they see visible text and interact via accessible roles (a button, a text field). A test
written the same way keeps passing through internal refactors that don't change user-facing
behavior, and a test that breaks means something a real user would actually notice broke too. See
[unit-and-component-testing.md](unit-and-component-testing.md).

</details>

## References

- Martin Fowler, [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- Vitest, [Getting Started](https://vitest.dev/guide/)
- Testing Library, [React Testing Library Introduction](https://testing-library.com/docs/react-testing-library/intro/)
- Playwright, [Getting Started](https://playwright.dev/docs/intro)

## Continue Your Learning Path

See the [Frontend learning path](../../README.md) for the remaining modules and what comes next.
