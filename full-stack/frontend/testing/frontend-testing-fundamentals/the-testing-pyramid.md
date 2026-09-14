# The Testing Pyramid

## The Three Layers

```
        /\
       /  \      End-to-End (few) — full real system, through the UI
      /----\
     /      \    Integration / Component (some) — a real component +
    /--------\   some real collaborators
   /          \  Unit (lots) — one function or module, isolated
  /____________\
```

The **testing pyramid** organizes automated tests into three layers, each testing a broader slice
of the real system than the one below it:

- **Unit tests** (base): test one function, one module, or one small piece of logic in complete
  isolation — external dependencies are replaced with mocks or stubs.
- **Integration / component tests** (middle): test a real component together with some of its
  real collaborators — for instance, a React component rendering with real child components and
  real state updates, but without a real backend.
- **End-to-end (e2e) tests** (top): test the entire, real system — a real browser driving the
  actual running application, exactly the way a real user would.

## Why a Pyramid Shape, Specifically

The shape is a deliberate recommendation, not just a description: **write lots of unit tests, some
integration tests, and very few end-to-end tests.** This isn't arbitrary — it follows directly from
a real tradeoff at each layer.

| Layer | Speed | Confidence given | Maintenance cost |
|---|---|---|---|
| Unit | Very fast — thousands can run in minutes | Narrow — only proves the isolated piece works | Low |
| Integration/Component | Slower | Moderate — proves pieces work together | Moderate |
| End-to-end | Slow, and often flaky | Highest — proves the real system actually works | High |

Unit tests are cheap enough to write *many* of, catching the bulk of logic bugs quickly and early.
End-to-end tests give the strongest possible confidence — nothing is mocked, so a passing e2e test
means the real thing actually works — but that confidence is expensive: e2e tests are slow to run,
brittle in the face of unrelated UI changes, and prone to intermittent failures unrelated to real
bugs (a slightly slow network response, an animation still in progress).

## The "Inverted" Anti-Pattern

Teams that skip writing unit tests and instead rely mostly on end-to-end tests to catch everything
end up with what's sometimes called an "ice cream cone" shape — the inverse of the pyramid. The
result in practice: a slow, flaky test suite that takes many minutes (or hours) to run, discourages
developers from running it often, and makes a real bug hard to pin down, since an e2e failure only
tells you *that* something broke somewhere in a large real system, not precisely *what*.

## Choosing the Right Layer for a Given Test

A practical rule: test a piece of logic at the *lowest* layer that can actually catch the bug you
care about.

- A pure function (formatting a price, validating an email pattern) → **unit test**. No UI, no
  rendering needed.
- A component's behavior in response to user interaction (does clicking "Add to Cart" update the
  displayed count?) → **component test**. Needs real rendering, but not a real browser or backend.
- A critical, multi-step user journey (can a user actually complete checkout end-to-end?) →
  **end-to-end test**, reserved for the flows where the extra cost and confidence are genuinely
  worth it.

## Common Mistakes

- Writing an end-to-end test for something a fast unit test could have verified just as well —
  paying the highest cost for confidence you didn't actually need.
- Treating "100% test coverage" as the goal, rather than deliberately choosing where tests provide
  real, cost-effective confidence.
- Building an inverted pyramid by under-investing in unit tests, then discovering the resulting
  suite is too slow and flaky for anyone to want to run it regularly.

## Next

Continue to [unit-and-component-testing.md](unit-and-component-testing.md) to write the base and
middle layers of the pyramid concretely.
