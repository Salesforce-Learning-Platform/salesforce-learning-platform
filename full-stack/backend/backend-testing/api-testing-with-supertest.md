# 🌐 API Testing with Supertest

## Testing a Real Endpoint, Without a Real Running Server

```js
import request from "supertest";
import { app } from "../app.js"; // the actual Express app object, NOT .listen()'d

it("GET /products returns a 200 with a list of products", async () => {
  const response = await request(app).get("/products");

  expect(response.status).toBe(200);
  expect(Array.isArray(response.body)).toBe(true);
});
```

**Supertest** tests a real Express app's actual HTTP behavior directly — routing, middleware, and
response formatting, all genuinely exercised — without needing to separately start the server on a
real port first. `request(app)` binds directly to the app object in memory; this is faster and
avoids port-conflict issues between test runs compared to spinning up a genuinely listening server
for every test.

## Testing a POST Endpoint With a Request Body

```js
it("POST /products creates a new product with valid input", async () => {
  const response = await request(app)
    .post("/products")
    .send({ name: "Keyboard", price: 79.99 });

  expect(response.status).toBe(201);
  expect(response.body.name).toBe("Keyboard");
});

it("POST /products returns 422 for invalid input", async () => {
  const response = await request(app)
    .post("/products")
    .send({ name: "" }); // missing required price, empty name

  expect(response.status).toBe(422);
});
```

`.send(body)` attaches a request body exactly like a real client would — this genuinely exercises
[REST API Design's request validation](../rest-api-design/request-validation.md), confirming both
that valid input succeeds *and* that invalid input is correctly rejected with the right status code
(per [status-codes.md](../rest-api-design/status-codes.md)).

## Testing Authenticated Routes

```js
it("GET /orders/mine requires authentication", async () => {
  const response = await request(app).get("/orders/mine"); // no token at all
  expect(response.status).toBe(401);
});

it("GET /orders/mine returns the authenticated user's orders", async () => {
  const token = generateTestToken({ userId: 1 }); // a real, validly-signed test JWT

  const response = await request(app)
    .get("/orders/mine")
    .set("Authorization", `Bearer ${token}`);

  expect(response.status).toBe(200);
});
```

`.set("Authorization", ...)` attaches a real header exactly as a genuine client would — directly
testing [protecting-routes.md](../authentication-and-authorization/protecting-routes.md)'s
middleware, both confirming it correctly rejects an unauthenticated request and correctly allows an
authenticated one through.

## Where This Fits: Testing the Controller Layer, End to End Within the App

Supertest tests genuinely exercise the full request path — middleware, routing, controller, and
(per [integration-testing.md](integration-testing.md)) potentially a real test database too —
without needing an actual, separately-deployed running system the way a true end-to-end browser
test would. This makes it a practical, fast way to verify an API's real, observable behavior
directly.

## Common Mistakes

- Calling `app.listen()` and testing against a real network port instead of passing the app object
  directly to `request()` — unnecessarily slower and prone to port conflicts between test runs.
- Only testing the success case for an endpoint, skipping the error responses
  (`401`, `404`, `422`) a real client also needs to handle correctly.
- Hardcoding a real, production JWT secret or real user credentials in a test — a dedicated test
  configuration (per
  [configuration-management.md](../backend-architecture/configuration-management.md)) should be
  used instead.

## ➡️ Next

Continue to [what-to-test-first.md](what-to-test-first.md) to prioritize test coverage when time
is genuinely limited.
