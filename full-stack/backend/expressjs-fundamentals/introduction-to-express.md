# Introduction to Express.js

## What Express Actually Is

**Express.js** is a minimal, unopinionated web framework for Node.js — it doesn't replace the
`http` module from [Creating Your First Server](../creating-your-first-server/); it's built
directly on top of it, adding a thin, well-designed layer of conveniences that the raw module
leaves entirely up to you to build yourself.

## What Express Adds, Concretely

| Manual `http` module | Express |
|---|---|
| Chained `if`/`else` comparing `req.method` and `req.url` | `app.get("/products", handler)` — declarative, one line per route |
| Manually parse dynamic URL segments (`/products/42`) with string splitting | `app.get("/products/:id", ...)` — `req.params.id` is parsed automatically |
| Manually collect a streamed request body with `data`/`end` events | `express.json()` middleware — `req.body` is ready to use directly |
| No shared way to run common logic across many routes | **Middleware** — a composable pipeline, covered in [middleware.md](middleware.md) |

None of what Express does is magic — every one of these is something you genuinely *could* build
yourself with the raw `http` module, exactly as
[routing-basics.md](../creating-your-first-server/routing-basics.md) demonstrated. Express's value
is having already solved these problems well, consistently, and in a way the entire Node ecosystem
recognizes and builds tooling around.

## Why "Minimal and Unopinionated" Matters

Unlike some full-stack frameworks that dictate an entire project structure, Express deliberately
stays small: it provides routing, middleware, and a few response helpers, and leaves almost
everything else — how you talk to a database, how you structure folders, which templating engine
(if any) you use — as a separate choice. This is why Express pairs so well with whichever specific
database or pattern a project needs (covered later in this domain, including
[Backend Architecture](../backend-architecture/)), rather than forcing one particular way of
doing things.

## Installing Express

```bash
npm install express
```

Express is a regular npm package — a **dependency** (not a `devDependency`, per
[npm-and-package-management.md](../starting-with-nodejs/npm-and-package-management.md)), since
the running application genuinely needs it to function, not just during development.

## Common Mistakes

- Assuming Express replaces or hides Node's `http` module entirely — it's built directly on top of
  it, and understanding the raw module (from the previous module) is exactly what makes Express's
  conveniences make sense rather than feeling like unexplained magic.
- Expecting Express to make architectural decisions (database choice, folder structure, auth
  strategy) for you — its minimalism is deliberate, and those decisions are yours to make.

## Next

Continue to [creating-an-express-server.md](creating-an-express-server.md) to set up a real
Express app and its first route.
