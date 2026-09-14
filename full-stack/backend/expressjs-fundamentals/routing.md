# Routing

## A Route for Every Method

```js
app.get("/products", (req, res) => res.json(products));
app.post("/products", (req, res) => { /* create one */ });
app.put("/products/:id", (req, res) => { /* replace one */ });
app.delete("/products/:id", (req, res) => { /* remove one */ });
```

Express provides one method per HTTP verb — `app.get`, `app.post`, `app.put`, `app.delete`, and
more — directly replacing
[routing-basics.md](../creating-your-first-server/routing-basics.md)'s manual `req.method ===
"..."` conditionals with one declarative line per route.

## Route Parameters — `req.params`

```js
app.get("/products/:id", (req, res) => {
  const product = products.find((p) => p.id === Number(req.params.id));
  res.json(product);
});
```

A `:id` segment in a route path is a **route parameter** — Express matches it against whatever the
client actually sent (`GET /products/42` → `req.params.id === "42"`) and parses it out
automatically. This directly replaces the manual `req.url.split("/products/")[1]` approach from
[routing-basics.md](../creating-your-first-server/routing-basics.md).

## Query Strings — `req.query`

```
GET /products?category=electronics&sort=price
```

```js
app.get("/products", (req, res) => {
  console.log(req.query.category); // "electronics"
  console.log(req.query.sort);     // "price"
});
```

A **query string** (everything after `?` in a URL) is not part of the route path itself — it's for
optional parameters like filtering or sorting. Express parses it automatically into `req.query`, an
object of key-value pairs.

## Route Params vs. Query Strings — Choosing Correctly

| | Route parameter (`:id`) | Query string (`?key=value`) |
|---|---|---|
| Identifies | A specific resource | Options/filters on a request |
| Example | `/products/42` — *which* product | `/products?sort=price` — how to sort *the collection* |
| Required? | Typically, part of the URL structure | Typically optional |

A common design mistake is putting something that should be a query parameter into the route path
(or vice versa) — a product's ID genuinely identifies *which resource* the request is about, so it
belongs in the path; a sort order is an optional modifier on a request for a collection, so it
belongs in the query string.

## Modular Routing With `express.Router`

```js
// routes/products.js
import { Router } from "express";
const router = Router();

router.get("/", (req, res) => res.json(products));
router.get("/:id", (req, res) => res.json(findById(req.params.id)));

export default router;
```

```js
// app.js
import productsRouter from "./routes/products.js";
app.use("/products", productsRouter);
```

As an application grows past a handful of routes, defining every single one directly on `app`
becomes unwieldy — the same "doesn't scale" problem
[routing-basics.md](../creating-your-first-server/routing-basics.md) raised, one level up.
`express.Router()` creates a self-contained, mountable set of routes: `router.get("/")` here
actually handles `GET /products` once mounted with `app.use("/products", router)` — keeping each
resource's routes in their own file.

## Common Mistakes

- Reading a route parameter (`req.params.id`) as if it were already a number — it's always a
  string, exactly like `process.env` values, and needs explicit conversion (`Number(...)`) before
  numeric comparison.
- Defining a more specific route (`/products/featured`) *after* a route parameter pattern
  (`/products/:id`) that would greedily match it first — Express matches routes in the order
  they're registered, so specific routes generally need to come before parameterized ones.
- Putting something that should be a query parameter directly into the route path, producing an
  explosion of route variations instead of one route with optional query options.

## Next

Continue to [middleware.md](middleware.md) to see the mechanism that actually powers routing,
request parsing, and everything else Express does.
