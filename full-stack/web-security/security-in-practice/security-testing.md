# 🧪 Security Testing

## Verifying Defenses, Not Just Implementing Them

Every fix covered throughout this domain deserves the same discipline already established in
[The Testing Pyramid](../../frontend/testing/frontend-testing-fundamentals/the-testing-pyramid.md),
earlier in this repository's Frontend domain: implementing a defense and *verifying* it actually
works are two genuinely separate steps, and skipping the second leaves real, unconfirmed
assumptions in place.

## Two Genuinely Different Testing Approaches: SAST and DAST

```
SAST (Static Application Security Testing) → analyzes SOURCE
  CODE directly, without running it - catching issues like
  hardcoded secrets or known-vulnerable patterns EARLY, before
  deployment

DAST (Dynamic Application Security Testing) → tests a RUNNING
  application by sending real HTTP requests and observing actual
  responses - exactly the way a genuine attacker would probe it
```

These are complementary, not competing — SAST catches issues early, directly in the code, while
DAST catches issues that only manifest in the application's actual, running behavior, closer to
[the-testing-pyramid.md](../../frontend/testing/frontend-testing-fundamentals/the-testing-pyramid.md)'s
broader lesson that different testing approaches genuinely catch different classes of problem.

## ZAP: a Widely-Used, Free DAST Tool

```
ZAP (formerly "OWASP ZAP," now maintained under the Linux
Foundation and Checkmarx as "ZAP by Checkmarx" following a 2023-
2024 transition, though still free and open source) works as an
INTERCEPTING PROXY - recording real requests/responses and
actively probing for injection, XSS, authentication flaws, and
missing security headers, exactly this module's own coverage.
```

Worth knowing this project's exact current status explicitly, since it's commonly still referred to
by its older name — it remains genuinely free, open-source, and directly usable, just under updated
governance.

## Writing Security-Specific Tests

```js
describe("POST /orders - authorization", () => {
  it("rejects a request with no authentication token", async () => {
    const res = await request(app).post("/orders").send(validOrderData);
    expect(res.status).toBe(401);
  });

  it("rejects a request attempting to access ANOTHER user's order", async () => {
    const res = await request(app)
      .get(`/orders/${otherUsersOrderId}`)
      .set("Authorization", `Bearer ${myToken}`);
    expect(res.status).toBe(403);
  });
});
```

Directly applying the same [Supertest](../../backend/backend-testing/)-based testing patterns
already covered in this repository's Backend domain — but deliberately written from an *attacker's*
perspective (per [The Security Mindset](../the-security-mindset/understanding-web-security.md)):
does an unauthenticated request genuinely get rejected? Does one user genuinely fail to access
another's data? These are real, automatable tests, not merely manual, one-time checks.

## Integrating Security Testing Into CI

```yaml
- name: Run security-specific tests
  run: npm run test:security
- name: Dependency audit
  run: npm audit --audit-level=high
```

Directly extending [dependency-security.md](dependency-security.md)'s CI integration — running
security-specific tests as a standard, automated part of every pipeline run means a regression in a
previously-fixed vulnerability is caught immediately, on the very change that reintroduced it,
rather than discovered later during a separate, manual audit.

## Common Mistakes

- Treating a security fix as complete once implemented, without a corresponding automated test
  actually verifying it continues to hold on every future change.
- Relying exclusively on either SAST or DAST alone, missing the genuinely different class of issue
  the other approach is specifically designed to catch.
- Writing security tests only for the "happy path" of a defense, never for the actual attack
  scenario the defense exists to prevent.

## ➡️ Next

Continue to
[security-review-checklist.md](security-review-checklist.md) to bring every module in this domain
together into one practical, pre-ship checklist.
