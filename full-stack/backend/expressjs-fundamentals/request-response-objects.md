# Request and Response Objects

## Express Enhances, Doesn't Replace

Express's `req` and `res` are the exact same underlying `http.IncomingMessage` and
`http.ServerResponse` objects from
[request-and-response.md](../creating-your-first-server/request-and-response.md) — Express just
adds convenience properties and methods directly onto them. Everything you already know
(`req.method`, `req.headers`) still works identically; Express only adds to it.

## What Express Adds to `req`

```js
app.get("/products/:id", (req, res) => {
  req.params;  // { id: "42" } — route parameters, per routing.md
  req.query;   // { sort: "price" } — parsed query string, per routing.md
  req.body;    // { name: "New Product" } — parsed by express.json() middleware
  req.get("Content-Type"); // convenience method for reading a header
});
```

`req.params` and `req.query` (covered in [routing.md](routing.md)) and `req.body` (populated by the
`express.json()` middleware from [middleware.md](middleware.md)) are the three Express additions
you'll use constantly — each replacing a piece of manual parsing that the raw `http` module left
entirely up to you.

## What Express Adds to `res`

```js
app.get("/products", (req, res) => {
  res.json(products);              // send JSON, correct Content-Type set automatically
  res.status(201).json(newProduct); // set the status code, then send JSON — chainable
  res.redirect("/products/42");    // send a redirect response
  res.sendFile("/path/to/file.pdf"); // stream a file as the response
});
```

`res.json()`, `res.send()`, `res.status()`, `res.redirect()`, and `res.sendFile()` all replace
manual `res.writeHead()`/`res.end()` combinations from
[request-and-response.md](../creating-your-first-server/request-and-response.md) with single,
purpose-built methods. `res.status()` is commonly **chained** directly with `res.json()` — a
frequent, idiomatic Express pattern worth recognizing.

## A Realistic Example, Putting It Together

```js
app.post("/products", (req, res) => {
  const { name, price } = req.body;

  if (!name || typeof price !== "number") {
    return res.status(422).json({ error: "name and numeric price are required" });
  }

  const newProduct = { id: nextId++, name, price };
  products.push(newProduct);
  res.status(201).json(newProduct);
});
```

This single route handler reads a parsed body (`req.body`), validates it, and sends back either a
`422` (per [http-status-codes.md](../creating-your-first-server/http-status-codes.md)'s coverage
of validation failures) or a `201 Created` with the new resource — all using Express's enhanced
`req`/`res`, with none of the manual stream-collecting or header-writing the raw `http` module
would have required.

## Common Mistakes

- Reading `req.body` without first registering `express.json()` — it will be `undefined`, since
  nothing actually parsed the incoming stream into a usable object.
- Calling `res.status(201).json(...)` in the wrong order (`res.json(...).status(201)`) — `res.json`
  already sends the response, so a `.status()` call afterward has no effect; the status must be set
  *before* the body is sent.
- Forgetting that `req.params` values are always strings, even when the route parameter looks
  numeric (`req.params.id === "42"`, not `42`).

## Next

Continue to [error-handling.md](error-handling.md) to see what happens — and what should happen —
when a route handler fails.
