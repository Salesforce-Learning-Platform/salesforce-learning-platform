# 🎯 What to Test First

## Real Projects Never Have Time to Test Everything Immediately

Even with the testing pyramid's guidance, a real project rarely has the time to write exhaustive
tests for every single line of code right away. Deciding **what to test first** — with limited
time — is itself a real, practical skill.

## Priority 1: Code With Real, Consequential Business Logic

```
HIGH PRIORITY: order total calculation, stock/inventory checks,
authorization rules, payment amount computation — code where a
bug has a REAL, costly consequence.

LOWER PRIORITY: a simple pass-through route with no real logic of
its own, a trivial getter.
```

The service-layer business logic covered in
[unit-testing-business-logic.md](unit-testing-business-logic.md) — especially anything touching
money (per [Payments Integration](../payments-integration/)) or access control (per
[Authentication and Authorization](../authentication-and-authorization/)) — deserves testing first,
precisely because a bug there is genuinely costly, not just embarrassing.

## Priority 2: Code That Changes Often

Code that gets modified frequently is exactly where a regression is most likely to be silently
introduced — a test suite covering that code catches exactly the kind of "this used to work"
breakage that's otherwise easy to miss until a user reports it.

## Priority 3: Code That's Already Broken Before, or Genuinely Complex

A piece of logic that's already caused a real bug once is statistically more likely to cause
another — writing a test that specifically reproduces a past bug (a **regression test**) both
verifies the fix and prevents the exact same bug from silently returning later. Genuinely complex
logic (many branches, edge cases) is also worth prioritizing, since it's the hardest to verify
correct just by reading it.

## What to Deliberately Deprioritize

```
LOWER PRIORITY (not "never," just not FIRST):
- Simple, stable, rarely-changing utility functions
- Thin route handlers with essentially no logic of their own
- Third-party library behavior (that's the library's own job to test)
```

Testing everything with equal priority wastes real, limited time on low-value coverage — a trivial
function that simply returns a fixed value, or a route that does nothing but call a
well-already-tested service function, provides comparatively little additional confidence for the
time it costs to write and maintain its test.

## A Practical Rule of Thumb

When genuinely unsure where to start: **test the code you'd be most afraid to change without a
safety net.** That fear is usually a direct, honest signal of real complexity or real consequence —
precisely the code most worth covering first.

## Common Mistakes

- Trying to achieve high test coverage as a number, rather than deliberately prioritizing the
  genuinely consequential and complex code first.
- Never writing a regression test for a bug that's already happened once, leaving the door open
  for the exact same mistake to silently return later.
- Spending significant testing effort on simple, stable utility code while genuinely
  consequential business logic (payments, authorization) remains untested.

## Module Summary

Across this module: backend testing matters specifically because backend bugs are often silent and
more consequential than frontend ones, and the same testing pyramid from the Frontend domain
applies directly here (see
[why-backend-testing-matters.md](why-backend-testing-matters.md)); **unit testing** the service
layer in isolation, with a mocked repository, verifies real business logic fast and independently
of the database (see [unit-testing-business-logic.md](unit-testing-business-logic.md)); **mocking**
with `vi.fn()` and `vi.mock()` isolates genuinely slow, external, or non-deterministic dependencies
without ever mocking the actual code under test (see
[mocking-dependencies.md](mocking-dependencies.md)); **integration tests**, run against a real,
dedicated test database, verify that separately-correct pieces genuinely work together (see
[integration-testing.md](integration-testing.md)); **Supertest** tests a real Express app's
observable HTTP behavior directly, without needing a genuinely running server (see
[api-testing-with-supertest.md](api-testing-with-supertest.md)); and **prioritizing** genuinely
consequential, frequently-changed, or previously-broken code makes limited testing time count for
the most.
