# Protecting Routes

## Authentication as Middleware

```js
function requireAuth(req, res, next) {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(401).json({ error: "No token provided" });

  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET); // per jwt.md
    next();
  } catch {
    res.status(401).json({ error: "Invalid or expired token" });
  }
}
```

This is precisely [Express's middleware.md](../expressjs-fundamentals/middleware.md)'s pattern,
applied to authentication specifically: a function with the `(req, res, next)` signature that
either calls `next()` to let the request continue (attaching `req.user` for every later handler to
use) or short-circuits with a `401` response if authentication fails.

## Applying It to Specific Routes

```js
// Only this ONE route requires authentication
app.get("/products", (req, res) => { /* public — no auth needed */ });
app.post("/products", requireAuth, (req, res) => { /* protected */ });
```

```js
// Every route on this router requires authentication
const ordersRouter = Router();
ordersRouter.use(requireAuth);
ordersRouter.get("/", (req, res) => { /* ... */ });
ordersRouter.post("/", (req, res) => { /* ... */ });
app.use("/orders", ordersRouter);
```

Middleware can be applied per-route (passed directly as an extra argument, as with `POST
/products`) or router-wide (via `router.use()`, per
[Express's middleware.md](../expressjs-fundamentals/middleware.md)'s coverage of router-level
middleware) — the right choice depends on whether an entire resource is private, or only specific
operations on an otherwise-public resource are.

## Using `req.user` Downstream

```js
app.get("/orders/mine", requireAuth, async (req, res) => {
  const orders = await Order.find({ userId: req.user.userId });
  res.json(orders);
});
```

Once `requireAuth` has run and attached `req.user`, every later handler in the chain can safely use
it — this is exactly how a "my orders" endpoint scopes its query to the authenticated user, without
ever trusting a user ID the client might have sent directly in the request body (which, per
[authentication-vs-authorization.md](authentication-vs-authorization.md), can never be trusted on
its own).

## Optional Authentication

```js
function optionalAuth(req, res, next) {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return next(); // no token — proceed as an anonymous user

  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
  } catch {
    // an invalid token is treated the same as no token — proceed anonymously
  }
  next();
}
```

Not every route requires authentication to work at all — a product listing might show extra
personalized data (like whether an item is in the current user's wishlist) *if* logged in, while
still working normally for an anonymous visitor. `optionalAuth` calls `next()` unconditionally,
only attaching `req.user` when a valid token happens to be present.

## Common Mistakes

- Forgetting to apply authentication middleware to a route that genuinely needs it, leaving
  sensitive data or actions unintentionally public.
- Trusting a client-supplied user ID (from `req.body` or `req.query`) instead of the server's own
  verified `req.user`, letting a malicious client impersonate another user simply by changing a
  request parameter.
- Applying `requireAuth` (which always rejects an unauthenticated request) to a route that should
  actually behave differently — but still work — for anonymous users, where `optionalAuth` is the
  correct choice instead.

## Next

Continue to [role-based-access-control.md](role-based-access-control.md) to go beyond "is this
user logged in" and check what a specific, now-known user is actually allowed to do.
