# Role-Based Access Control (RBAC)

## Beyond "Is This User Logged In At All"

[protecting-routes.md](protecting-routes.md) established **authentication** — every route there
either requires a valid, logged-in user or it doesn't. That's a single yes/no gate; it says
nothing about *what kind* of user is allowed to do *what*. **Role-Based Access Control (RBAC)** is
the standard pattern for exactly that finer-grained **authorization** question, per
[authentication-vs-authorization.md](authentication-vs-authorization.md).

## The Core Idea: Roles, Not Individual Permissions Per User

```js
const users = [
  { id: 1, email: "alice@example.com", role: "customer" },
  { id: 2, email: "bob@example.com", role: "admin" },
];
```

Rather than tracking individual permissions per user directly, RBAC assigns each user a **role**
(`customer`, `admin`, `moderator`, ...), and permissions are defined in terms of roles. Adding a new
admin is then as simple as setting their `role` field — no need to individually configure a long
list of permissions for every single user.

## Authorization Middleware, Building on `requireAuth`

```js
function requireRole(role) {
  return (req, res, next) => {
    if (req.user.role !== role) {
      return res.status(403).json({ error: "Insufficient permissions" });
    }
    next();
  };
}
```

```js
app.delete("/products/:id", requireAuth, requireRole("admin"), (req, res) => {
  // only an authenticated admin ever reaches this handler
});
```

`requireRole` is a **middleware factory** — a function that returns a middleware function,
configured with the specific role required for this route. It runs *after* `requireAuth` (since it
depends on `req.user` already being set) and returns `403 Forbidden` — not `401` — since the user
is genuinely authenticated; they're just not authorized for this particular action, exactly the
distinction [authentication-vs-authorization.md](authentication-vs-authorization.md) establishes.

## Beyond a Single Role: Permission Checks

```js
const rolePermissions = {
  customer: ["orders:read:own"],
  admin: ["orders:read:any", "orders:delete:any", "products:write"],
};

function requirePermission(permission) {
  return (req, res, next) => {
    const allowed = rolePermissions[req.user.role] || [];
    if (!allowed.includes(permission)) {
      return res.status(403).json({ error: "Insufficient permissions" });
    }
    next();
  };
}
```

A single "role" is sometimes too coarse — a real application might need many distinct permissions,
and mapping *roles to sets of permissions* (rather than checking a role name directly on every
route) makes the system easier to extend: adding a new, more specific permission means updating one
central `rolePermissions` mapping, not hunting down every route that might need to know about it.

## Resource Ownership: A Different Kind of Authorization Check

```js
app.delete("/orders/:id", requireAuth, async (req, res) => {
  const order = await Order.findById(req.params.id);
  if (!order) return res.status(404).json({ error: "Not found" });

  if (order.userId !== req.user.userId && req.user.role !== "admin") {
    return res.status(403).json({ error: "Not your order" });
  }
  // proceed with deletion
});
```

Not every authorization check is about a fixed role — "can this user delete *this specific order*"
depends on whether they actually **own** it (or are an admin, who can act on any order). This kind
of check genuinely needs to run inside the route handler itself, after the specific resource has
been loaded, rather than as a simple role-name check in middleware alone.

## Common Mistakes

- Checking a user's role from client-supplied data (a request body or query parameter) instead of
  the server's own verified `req.user.role`, established during authentication — a client claiming
  `"role": "admin"` in a request body must never be trusted.
- Applying only a coarse role check when the real requirement is ownership ("is this the user's own
  resource") — a `customer` role check alone doesn't prevent one customer from acting on another
  customer's data.
- Hardcoding role checks scattered across many individual routes instead of centralizing them in
  reusable middleware, making the actual permission structure hard to audit as an application
  grows.

## Module Summary

Across this module: **authentication** establishes who's making a request, while **authorization**
separately decides what that now-known identity is allowed to do — a distinction that directly maps
onto `401` vs. `403` (see
[authentication-vs-authorization.md](authentication-vs-authorization.md)); passwords are never
stored in plain text or with a fast general-purpose hash, but with **bcrypt**, deliberately slow and
automatically salted (see [password-hashing.md](password-hashing.md)); **session-based
authentication** keeps state server-side, trading scaling complexity for instant revocability (see
[sessions.md](sessions.md)); **JWTs** invert that tradeoff — stateless and scalable, signed but
never encrypted, with revocation genuinely hard once issued (see [jwt.md](jwt.md)); authentication
is implemented as reusable Express **middleware**, attaching a verified `req.user` for every later
handler to trust (see [protecting-routes.md](protecting-routes.md)); and **role-based access
control**, plus resource-ownership checks where a role alone isn't precise enough, is the standard
pattern for the authorization layer on top of it.
