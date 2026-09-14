# Request Validation

## Why Validate at the Boundary

```js
// WITHOUT validation — business logic has to defensively check
// everything itself, at every single point it touches the data
app.post("/products", (req, res) => {
  if (typeof req.body.name !== "string") { /* ... */ }
  if (typeof req.body.price !== "number") { /* ... */ }
  // ...and every function downstream has to trust this was done correctly
});
```

Request data from a client can never be trusted to arrive in the expected shape — a missing field,
a string where a number belongs, or outright malicious input are all realistic possibilities.
**Validating once, at the boundary** — immediately when a request arrives, before any business
logic runs — means everything downstream (database calls, calculations) can simply trust the data's
shape is correct, rather than every individual function needing to defensively re-check it.

## Schema-Based Validation With Zod

```js
import { z } from "zod";

const createProductSchema = z.object({
  name: z.string().min(1),
  price: z.number().positive(),
  category: z.enum(["electronics", "clothing", "books"]),
});

app.post("/products", (req, res) => {
  const result = createProductSchema.safeParse(req.body);

  if (!result.success) {
    return res.status(422).json({ error: result.error.issues });
  }

  const newProduct = createProduct(result.data); // guaranteed correctly-shaped
  res.status(201).json(newProduct);
});
```

**Zod** is a schema-based validation library: `z.object({...})` declares exactly what a valid
request body looks like — the required fields, their types, and any extra constraints (`.min(1)`,
`.positive()`, an `.enum()` of allowed values). `.safeParse(data)` checks `data` against that
schema and returns a result object rather than throwing, letting the route handler decide exactly
how to respond to invalid input (here, a `422`, per
[status-codes.md](status-codes.md)'s coverage of that code).

## `.parse()` vs. `.safeParse()`

```js
// .parse() — throws on invalid input; combine with Express's automatic
// error catching (per error-handling.md) rather than a manual check
const data = createProductSchema.parse(req.body); // throws ZodError if invalid

// .safeParse() — never throws; returns { success, data } or { success, error }
const result = createProductSchema.safeParse(req.body);
```

`.parse()` throws an error on invalid input — convenient when paired with Express's automatic
error-catching (per [error-handling.md](../expressjs-fundamentals/error-handling.md)), since a
thrown `ZodError` can be caught by a shared error-handling middleware. `.safeParse()` never throws,
instead returning an explicit success/failure result — often preferred when a route wants to build
a custom, specific response for validation failures itself.

## An Alternative: `express-validator`

```js
import { body, validationResult } from "express-validator";

app.post(
  "/products",
  body("name").isString().notEmpty(),
  body("price").isFloat({ min: 0 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(422).json({ errors: errors.array() });
    }
    // ... proceed with validated req.body
  }
);
```

**express-validator** takes a different approach: validation rules are expressed as Express
middleware functions themselves (`body("name").isString()`), chained directly into the route's
middleware list, with `validationResult(req)` collecting any failures. Both Zod and
express-validator solve the same problem; Zod's schema-first style (define the shape once, reuse
it) is generally favored for new [TypeScript](../../frontend/typescript/) projects, while
express-validator's middleware-chain style fits naturally into an Express-centric codebase.

## Common Mistakes

- Validating only some fields and trusting the rest, leaving a gap an attacker or a buggy client
  could exploit.
- Performing validation logic scattered throughout business code instead of once, explicitly, at
  the request boundary — making it easy to accidentally skip in one code path.
- Returning a generic `400` for every validation failure instead of the more precise `422`
  (well-formed request, fails business-rule validation) covered in
  [status-codes.md](status-codes.md).

## Next

Continue to [pagination-filtering-and-sorting.md](pagination-filtering-and-sorting.md) to design
collection endpoints that stay fast and usable as the underlying data grows large.
