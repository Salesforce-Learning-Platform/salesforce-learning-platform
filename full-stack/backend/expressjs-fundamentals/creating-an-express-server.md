# Creating an Express Server

## The Minimal Express App

```js
import express from "express";

const app = express();
const port = 3000;

app.get("/", (req, res) => {
  res.send("Hello, Express!");
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

`express()` creates the **app** object — everything (routes, middleware, configuration) is
attached to it. `app.get(path, handler)` registers a route: when a `GET` request matches `path`,
`handler` runs. `app.listen(port)` starts the server, exactly playing the same role
`server.listen()` played with the raw `http` module in
[creating-an-http-server.md](../creating-your-first-server/creating-an-http-server.md) — under the
hood, Express is actually using that same module to listen for connections.

## `res.send()` vs. Node's Raw `res.end()`

```js
app.get("/text", (req, res) => {
  res.send("Plain text works");                 // Content-Type set automatically
});

app.get("/json", (req, res) => {
  res.send({ message: "Objects work too" });     // Auto-detected as JSON
});

app.get("/json-explicit", (req, res) => {
  res.json({ message: "Explicit JSON" });        // Always sends JSON, even for a string
});
```

Recall [request-and-response.md](../creating-your-first-server/request-and-response.md)'s manual
`res.writeHead()` + `res.end()` pattern, including manually setting `Content-Type`. Express's
`res.send()` inspects what you pass it and sets the correct `Content-Type` header automatically —
a string becomes `text/html`, an object is automatically serialized to JSON. `res.json()` is the
more explicit choice when a route should *always* return JSON regardless of what's passed.

## The Request Handler's Signature

```js
app.get("/products/:id", (req, res) => {
  // req  — the (enhanced) request object
  // res  — the (enhanced) response object
});
```

An Express route handler receives the same conceptual `req`/`res` pair from the raw `http` module —
Express doesn't replace them, it **enhances** them with extra properties and methods, covered fully
in [request-response-objects.md](request-response-objects.md).

## A Small, Real Example: A Products Endpoint

```js
import express from "express";

const app = express();
const products = [{ id: 1, name: "Keyboard" }, { id: 2, name: "Mouse" }];

app.get("/products", (req, res) => {
  res.json(products);
});

app.listen(3000, () => console.log("Server running"));
```

Compare this directly against
[routing-basics.md](../creating-your-first-server/routing-basics.md)'s manual equivalent — the same
outcome, with no manual `req.method`/`req.url` comparison and no manual JSON serialization/header
setting required.

## Common Mistakes

- Forgetting to call `app.listen()` — exactly the same mistake as forgetting `server.listen()` with
  the raw `http` module; the app object alone doesn't start accepting connections.
- Using `res.end()` directly instead of `res.send()`/`res.json()`, losing Express's automatic
  `Content-Type` handling for no real benefit.
- Defining routes after calling `app.listen()` — routes should be registered before the server
  starts listening, as part of setting up the app.

## Next

Continue to [routing.md](routing.md) to handle more than one route, with dynamic segments and
query parameters.
