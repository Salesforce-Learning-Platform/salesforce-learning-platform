# Controllers, Services, and Repositories

## The Repository Layer — Only Data Access

```js
// repositories/orderRepository.js
export const orderRepository = {
  async findProductById(id) {
    const result = await db.query("SELECT * FROM products WHERE id = $1", [id]);
    return result.rows[0];
  },
  async createOrder(order) {
    const result = await db.query(
      "INSERT INTO orders (product_id, quantity) VALUES ($1, $2) RETURNING *",
      [order.productId, order.quantity]
    );
    return result.rows[0];
  },
  async decrementStock(productId, quantity) {
    await db.query("UPDATE products SET stock = stock - $1 WHERE id = $2", [quantity, productId]);
  },
};
```

A **repository**, per Martin Fowler's original pattern, mediates between the rest of the
application and the actual data store — exposing collection-like operations
(`findProductById`, `createOrder`) rather than exposing raw SQL or MongoDB queries directly. Every
single database query in the entire application lives here, and only here — no other layer ever
talks to the database directly.

## The Service Layer — Business Logic Only

```js
// services/orderService.js
import { orderRepository } from "../repositories/orderRepository.js";

export const orderService = {
  async placeOrder(productId, quantity) {
    const product = await orderRepository.findProductById(productId);
    if (!product) throw new NotFoundError("Product not found");
    if (product.stock < quantity) throw new ConflictError("Insufficient stock");

    const order = await orderRepository.createOrder({ productId, quantity });
    await orderRepository.decrementStock(productId, quantity);
    return order;
  },
};
```

The **service** layer contains the actual business rules — "an order can't be placed if stock is
insufficient" is a genuine business rule, not an HTTP concern or a data-access concern. Notice the
service throws plain JavaScript errors (`NotFoundError`, `ConflictError`) rather than knowing
anything about HTTP status codes at all — that translation happens one layer up, in the controller,
keeping the service layer reusable outside of any HTTP context entirely (a background job placing
an order automatically, for instance, per
[layered-architecture.md](layered-architecture.md)'s reusability point).

## The Controller Layer — Only HTTP

```js
// controllers/orderController.js
import { orderService } from "../services/orderService.js";

export async function createOrder(req, res, next) {
  try {
    const order = await orderService.placeOrder(req.body.productId, req.body.quantity);
    res.status(201).json(order);
  } catch (err) {
    if (err instanceof NotFoundError) return res.status(404).json({ error: err.message });
    if (err instanceof ConflictError) return res.status(409).json({ error: err.message });
    next(err); // an unexpected error — hand off to centralized error handling
  }
}
```

```js
// routes/orders.js
import { Router } from "express";
import { createOrder } from "../controllers/orderController.js";

const router = Router();
router.post("/", createOrder);
export default router;
```

The **controller** is the thinnest layer: read what the HTTP request needs
(`req.body.productId`), call the service, and translate the outcome (success or a specific error)
into the correct HTTP response — this is exactly where
[REST's status-codes.md](../rest-api-design/status-codes.md)'s conventions actually get applied,
and nowhere else.

## Why This Specific Split, and Not Some Other One

Each layer depends only on the one directly below it, never skips a layer, and never depends
"upward": a controller calls a service; a service calls a repository; a repository never calls back
up into a service or controller. This one-directional dependency is what makes each layer
genuinely independently testable and replaceable — swapping the repository's implementation (a
different database, per [SQL vs. NoSQL](../database-design-and-modeling/sql-vs-nosql.md)) never
requires touching the service or controller layers at all, since they only ever depended on the
repository's method names and return shapes, not its internals.

## Common Mistakes

- Putting a raw database query directly inside a controller "just this once," gradually eroding the
  entire separation the pattern exists to provide.
- Putting HTTP-specific logic (reading `req.headers`, setting a status code) inside a service —
  services should be entirely HTTP-agnostic, callable from anywhere, not just from an Express route.
- Having a repository function return data already shaped for a specific HTTP response, rather than
  a clean, HTTP-agnostic representation the service layer can use for any purpose.

## Next

Continue to [configuration-management.md](configuration-management.md) to manage how each layer
gets its own configuration correctly across different environments.
