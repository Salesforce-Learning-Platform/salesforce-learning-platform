# 🎭 Mocking Dependencies

## What a Mock Actually Is

A **mock** is a fake, controlled stand-in for a real dependency — a database call, an external
API request, a file read — replaced specifically so a test can run fast, deterministically, and
without needing that real dependency to actually exist or be reachable.

## `vi.fn()` — a Mock Function

```js
import { vi, expect } from "vitest";

const mockFn = vi.fn();
mockFn("hello");

expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledWith("hello");
expect(mockFn).toHaveBeenCalledTimes(1);
```

`vi.fn()` creates a function that tracks everything about how it was called — its arguments, how
many times, and in what order — letting a test assert on exactly how the code under test actually
used it, exactly as
[unit-testing-business-logic.md](unit-testing-business-logic.md)'s `expect(fakeRepository.
decrementStock).toHaveBeenCalledWith(1, 2)` did.

## Controlling What a Mock Returns

```js
const mockFindProduct = vi.fn().mockResolvedValue({ id: 1, stock: 10 }); // for an async function
const mockCalculateTax = vi.fn().mockReturnValue(7.99); // for a sync function
const mockFailingCall = vi.fn().mockRejectedValue(new Error("Connection failed"));
```

`.mockResolvedValue()`/`.mockReturnValue()` let a test **control** exactly what a mocked dependency
produces — including simulating a **failure** (`.mockRejectedValue()`), which is often the only
practical way to reliably test how code handles a real database going down or a network call
failing, without needing to actually break something to trigger it.

## Mocking an Entire Module

```js
import { vi } from "vitest";
vi.mock("./emailService.js", () => ({
  sendConfirmationEmail: vi.fn().mockResolvedValue(true),
}));
```

`vi.mock()` replaces an entire imported module with a fake version for the duration of a test —
useful when a dependency (like a real email-sending service) genuinely shouldn't run during a test
at all, rather than being something conveniently passed in as a parameter the way
`fakeRepository` was.

## What Should — and Shouldn't — Be Mocked

```
MOCK: a database call, an external API (a payment gateway, an email
service), the current date/time if a test depends on it, anything
genuinely slow or non-deterministic

DON'T MOCK: the actual function/logic under test itself, or a plain,
fast, pure helper function with no real external dependency
```

The general rule: mock things that are slow, external, non-deterministic, or that a test simply
shouldn't have a real side effect on (sending a real email during a test run). Never mock the
actual code being tested — that would test the mock instead of the real logic, defeating the entire
purpose.

## Common Mistakes

- Mocking so much of a function's own internals that the test ends up verifying the mock's
  behavior instead of the real code's actual logic.
- Forgetting to reset or clear mocks between tests (`vi.clearAllMocks()`), letting a call count or
  return value from one test accidentally leak into and affect another.
- Mocking a fast, pure, dependency-free helper function unnecessarily — mocking exists to isolate
  genuinely slow or external dependencies, not to avoid calling ordinary, safe functions.

## ➡️ Next

Continue to [integration-testing.md](integration-testing.md) to see the layer where mocking is
deliberately used less, to verify real modules genuinely work together.
