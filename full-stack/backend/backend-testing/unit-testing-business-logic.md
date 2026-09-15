# 🔬 Unit Testing Business Logic

## Why the Service Layer Is Exactly What Should Be Unit Tested

Recall [controllers-services-and-repositories.md](../backend-architecture/controllers-services-and-repositories.md)'s
layering: the **service** layer holds real business logic, entirely independent of HTTP and
entirely independent of the actual database — it only ever calls a repository's *interface*. This
is exactly what makes it unit-testable: a test can supply a fake repository and verify the
service's own logic in complete isolation, with no real database involved at all.

## A Real Example

```js
// services/orderService.js — the code being tested (from Backend Architecture)
export const orderService = {
  async placeOrder(productId, quantity, repository) {
    const product = await repository.findProductById(productId);
    if (!product) throw new NotFoundError("Product not found");
    if (product.stock < quantity) throw new ConflictError("Insufficient stock");

    const order = await repository.createOrder({ productId, quantity });
    await repository.decrementStock(productId, quantity);
    return order;
  },
};
```

```js
// orderService.test.js
import { describe, it, expect, vi } from "vitest";
import { orderService } from "./orderService.js";

describe("orderService.placeOrder", () => {
  it("throws ConflictError when stock is insufficient", async () => {
    const fakeRepository = {
      findProductById: vi.fn().mockResolvedValue({ id: 1, stock: 2 }),
    };

    await expect(
      orderService.placeOrder(1, 5, fakeRepository) // asking for MORE than the 2 in stock
    ).rejects.toThrow("Insufficient stock");
  });

  it("creates an order and decrements stock when stock is sufficient", async () => {
    const fakeRepository = {
      findProductById: vi.fn().mockResolvedValue({ id: 1, stock: 10 }),
      createOrder: vi.fn().mockResolvedValue({ id: 99, productId: 1, quantity: 2 }),
      decrementStock: vi.fn().mockResolvedValue(undefined),
    };

    const order = await orderService.placeOrder(1, 2, fakeRepository);

    expect(order.id).toBe(99);
    expect(fakeRepository.decrementStock).toHaveBeenCalledWith(1, 2);
  });
});
```

This test never touches a real database — `fakeRepository` is a plain object with mocked functions
(per [mocking-dependencies.md](mocking-dependencies.md)) standing in for the real repository. It
runs in milliseconds, tests the service's actual decision-making logic precisely, and stays
completely unaffected by whatever database technology the real repository happens to use.

## Testing the Actual Business Rule, Not Just "It Doesn't Crash"

Notice the second test doesn't just check that `placeOrder` runs without throwing — it verifies
`decrementStock` was actually **called with the correct arguments**. A genuinely useful unit test
verifies the real behavior a business rule depends on, not merely that the function executed
without error.

## Common Mistakes

- Testing a controller (HTTP-handling code) as if it were the actual business logic — per
  [layered-architecture.md](../backend-architecture/layered-architecture.md), the controller
  should be thin, and the genuinely valuable logic to unit test lives in the service.
- Writing a unit test that accidentally still depends on a real database connection, making the
  test slow and fragile for no real benefit — that dependency should be mocked.
- Only testing the "happy path" (sufficient stock, valid input) and skipping the failure cases
  (insufficient stock, a missing product) that are often where real bugs actually hide.

## ➡️ Next

Continue to [mocking-dependencies.md](mocking-dependencies.md) to understand precisely what makes
`fakeRepository` above work, and how to build one correctly.
