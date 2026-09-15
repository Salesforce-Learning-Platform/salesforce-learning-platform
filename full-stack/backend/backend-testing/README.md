# 🧪 Backend Testing

## Purpose

[Frontend Testing Fundamentals](../../frontend/testing/frontend-testing-fundamentals/) already
covered the testing pyramid, unit testing, and Playwright — those foundational concepts apply
equally here and aren't repeated. This module applies them specifically to the **Backend**
domain: testing business logic in isolation, mocking a database, and actually testing real HTTP
endpoints with Supertest.

## 🎯 Learning Objectives

- Explain why companies specifically expect backend engineers who can test their own code.
- Unit test business logic (a service layer) in isolation from the database.
- Write an integration test verifying multiple modules work correctly together.
- Mock a dependency to isolate the unit actually under test.
- Test real API endpoints directly with Supertest.
- Decide what to test first when a project has limited time for tests.

## 📋 Prerequisites

- [Frontend Testing Fundamentals](../../frontend/testing/frontend-testing-fundamentals/) —
  specifically [the-testing-pyramid.md](../../frontend/testing/frontend-testing-fundamentals/the-testing-pyramid.md),
  since this module assumes that framework and applies it to the backend rather than re-explaining
  it.
- [Backend Architecture](../backend-architecture/) — specifically the
  [controller-service-repository pattern](../backend-architecture/controllers-services-and-repositories.md),
  which is exactly what makes backend business logic genuinely testable in isolation.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [why-backend-testing-matters.md](why-backend-testing-matters.md) | Why engineers are expected to test their own backend code |
| [unit-testing-business-logic.md](unit-testing-business-logic.md) | Testing a service layer in isolation, with a mocked repository |
| [mocking-dependencies.md](mocking-dependencies.md) | `vi.fn()`, mocking a database call, and what makes a good mock |
| [integration-testing.md](integration-testing.md) | Verifying real modules work correctly together |
| [api-testing-with-supertest.md](api-testing-with-supertest.md) | Testing real HTTP endpoints directly, without a separately running server |
| [what-to-test-first.md](what-to-test-first.md) | Prioritizing test coverage with limited time |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [mocking-dependencies.md](mocking-dependencies.md) — knowing exactly what to mock (and
what not to) is the single skill that determines whether a backend test suite is fast and reliable,
or slow and constantly breaking for unrelated reasons.

## ✅ Quick Knowledge Check

<details>
<summary>Should a unit test for a service function that calls a repository actually hit a real database?</summary>

No — a unit test should mock the repository, testing only the service's own logic (per
[Backend Architecture](../backend-architecture/controllers-services-and-repositories.md)'s
layering) in isolation. Hitting a real database belongs to an integration test, a layer up. See
[unit-testing-business-logic.md](unit-testing-business-logic.md).

</details>

<details>
<summary>Does Supertest require the Express app to actually be listening on a real port during a test?</summary>

No — Supertest can bind directly to an Express app object in-memory, without it ever calling
`.listen()` on a real port, making endpoint tests fast and avoiding port-conflict issues between
test runs. See [api-testing-with-supertest.md](api-testing-with-supertest.md).

</details>

## 📚 References

- Supertest, [GitHub repository](https://github.com/ladjs/supertest)
- Vitest, [Mocking](https://vitest.dev/api/mock.html)

## ➡️ Continue Your Learning Path

This is the final module in the Backend domain's gap-fill expansion. See the platform's root
[README](../../../README.md) for the full repository structure and what comes next.
