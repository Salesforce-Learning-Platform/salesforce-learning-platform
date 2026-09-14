# Middleware

## The Core Idea

```js
function logger(req, res, next) {
  console.log(`${req.method} ${req.url}`);
  next(); // hand control to whatever comes next
}

app.use(logger);
```

A **middleware** function has the signature `(req, res, next)` — it receives the request and
response, and a `next` function to call when it's done. Every single thing Express does — routing,
parsing a JSON body, serving static files — is actually implemented as middleware; an Express app
is fundamentally a **pipeline** of middleware functions, each one handling the request in sequence.

## The Request Flows Through the Stack, in Order

```js
app.use(logger);                          // 1. runs first, for every request
app.use(express.json());                  // 2. parses the body, if present
app.get("/products", (req, res) => {      // 3. the actual route handler
  res.json(products);
});
```

Middleware registered with `app.use()` runs for *every* request, in the exact order it was
registered — this is why a body-parsing middleware like `express.json()` must be registered
*before* any route that needs `req.body` to already be populated. A route handler itself
(`app.get(...)`) is really just the final middleware in the chain — the one that actually sends a
response instead of calling `next()`.

## Calling `next()` Is Not Optional

```js
// BROKEN — never calls next() and never sends a response;
// every request to this route hangs forever
app.use((req, res, next) => {
  console.log("logging, but forgot to call next()");
});
```

If a middleware function neither calls `next()` nor sends a response itself (`res.send`,
`res.json`, `res.end`), the request simply hangs — Express has no way to know the middleware
considers itself "done." This is one of the most common early Express bugs.

## Application-Level vs. Router-Level Middleware

```js
app.use(logger);                    // application-level — every request, any route

const productsRouter = Router();
productsRouter.use(requireAuth);    // router-level — only requests to this router
app.use("/products", productsRouter);
```

Application-level middleware (`app.use(...)`) applies globally. Router-level middleware
(`router.use(...)`) applies only to requests handled by that specific router — useful for scoping
logic (like an authentication check, covered in the upcoming
[Authentication and Authorization module](../authentication-and-authorization/)) to only the
routes that actually need it.

## Built-In Middleware

```js
app.use(express.json());        // parses a JSON request body into req.body
app.use(express.static("public")); // serves files directly from the "public" folder
```

Express ships a small set of built-in middleware: `express.json()` parses an incoming JSON body
(replacing [request-and-response.md](../creating-your-first-server/request-and-response.md)'s
manual `data`/`end` event collection), and `express.static()` serves files from a folder directly,
with no route needed per file.

## Third-Party Middleware

```bash
npm install cors
```

```js
import cors from "cors";
app.use(cors());
```

Beyond Express's small built-in set, the wider ecosystem provides middleware for nearly everything
else a real backend needs — `cors` for cross-origin requests, `morgan` for request logging, and
many more, each installed as a regular npm dependency and wired in with `app.use()` exactly like
custom middleware.

## Common Mistakes

- Forgetting to call `next()` in a middleware that isn't meant to end the response, causing the
  request to hang indefinitely.
- Registering `express.json()` *after* a route that reads `req.body` — the body will be
  `undefined` at that point, since the parsing middleware hasn't run yet.
- Calling `next()` *and* sending a response in the same middleware — this can trigger a "headers
  already sent" error, since only one response can ever be sent per request.

## Next

Continue to [request-response-objects.md](request-response-objects.md) to see exactly what Express
adds to `req` and `res` beyond Node's raw versions.
