# 🔗 Integration Testing

## Verifying Real Pieces Actually Work Together

[unit-testing-business-logic.md](unit-testing-business-logic.md) deliberately mocked the
repository — proving the *service's* logic works, but never actually proving the service and a
*real* database genuinely work together correctly. An **integration test** verifies exactly that:
multiple real modules, combined, doing what they're supposed to.

## A Real Database, Scoped Specifically for Testing

```js
// A separate, dedicated TEST database — never the real production one
const TEST_DATABASE_URL = process.env.TEST_DATABASE_URL;

beforeEach(async () => {
  await db.query("TRUNCATE products, orders RESTART IDENTITY CASCADE"); // reset to a clean state
});

it("actually persists a new order to the real database", async () => {
  await db.query("INSERT INTO products (id, name, stock) VALUES (1, 'Keyboard', 10)");

  const order = await orderService.placeOrder(1, 2, realRepository); // the REAL repository this time

  const rows = await db.query("SELECT * FROM orders WHERE id = $1", [order.id]);
  expect(rows.length).toBe(1);
});
```

This test uses the **real** repository (per
[Backend Architecture's controller-service-repository pattern](../backend-architecture/controllers-services-and-repositories.md)),
connected to a genuinely real — but dedicated, test-only — database, reset to a known clean state
before each test. This is deliberately slower and more involved than a unit test, but proves
something a mocked test structurally cannot: that the real SQL/MongoDB queries
([SQL Fundamentals](../sql-fundamentals/)/[MongoDB Fundamentals](../mongodb-fundamentals/)) are
actually correct.

## Why a Genuinely Separate Test Database Matters

```
NEVER run tests against the real production database — a test that
truncates a table, or a bug in the code under test, could destroy
genuine, real data.
```

A test database must be completely separate from production (and ideally from local development
data too) — tests routinely create, modify, and delete data as part of normal operation, and
running that against real, valuable data would be a serious, avoidable mistake.

## Where Integration Tests Fit in the Pyramid

Recall
[the-testing-pyramid.md](../../frontend/testing/frontend-testing-fundamentals/the-testing-pyramid.md):
integration tests sit in the middle — more expensive and slower than a unit test, but far cheaper
and faster than a genuine end-to-end test running against a fully deployed system. They earn their
place specifically for verifying that real, separately-correct pieces (a service, a repository, an
actual database) are also correctly **wired together**.

## Common Mistakes

- Running integration tests against a shared development database instead of a dedicated,
  disposable test database, causing test runs to interfere with each other or with real work.
- Forgetting to reset the database to a known state before each test, letting one test's leftover
  data silently affect another test's result.
- Writing every test as an integration test "to be safe," losing the speed benefit unit tests
  specifically provide — most logic should still be covered by fast unit tests first.

## ➡️ Next

Continue to [api-testing-with-supertest.md](api-testing-with-supertest.md) to test a real HTTP
endpoint — the controller layer, and everything beneath it — end to end within the application
itself.
