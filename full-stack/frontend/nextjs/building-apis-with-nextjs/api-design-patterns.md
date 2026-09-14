# API Design Patterns

## Structuring Resource-Based Endpoints

Applying [rest-api-design](../../../backend/rest-api-design/) principles (covered in depth in the
Backend domain) to the store's catalog:

```text
app/api/
├── products/
│   ├── route.ts              GET  /api/products        (list all)
│   │                         POST /api/products        (create one)
│   └── [slug]/
│       └── route.ts              GET    /api/products/:slug    (read one)
│                                  PATCH  /api/products/:slug    (update one)
│                                  DELETE /api/products/:slug    (delete one)
└── cart/
    └── route.ts               GET  /api/cart            (current cart)
                                POST /api/cart            (add an item)
```

This mirrors [http-methods-in-depth.md](../../foundations/understanding-http-and-https/http-methods-in-depth.md)
directly: the collection endpoint (`/api/products`) handles listing and creation; the item endpoint
(`/api/products/:slug`) handles operations on one specific resource — a consistent, predictable
structure any API client can learn once and reuse.

## Combining with Dynamic Segments for Filtering

```ts
// app/api/products/route.ts
export function GET(request: NextRequest) {
  const category = request.nextUrl.searchParams.get("category");
  const minPrice = request.nextUrl.searchParams.get("minPrice");
  // ...filter products based on whichever params were actually provided
}
```

Query parameters (from
[request-and-response.md](request-and-response.md)) are the conventional way to express
filtering, sorting, and pagination on a collection endpoint — `/api/products?category=electronics&minPrice=50`
— while dynamic segments (`[slug]`) identify one specific resource.

## Validating Input Before Processing It

```ts
export async function POST(request: Request) {
  const body = await request.json();

  if (!body.name || typeof body.price !== "number") {
    return Response.json({ error: "name and price are required" }, { status: 400 });
  }

  const product = await createProduct(body);
  return Response.json(product, { status: 201 });
}
```

This is the server-side validation half of the discipline established in
[frontend-and-backend-responsibilities.md](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md)
and revisited throughout the Advanced Forms module — a Route Handler is a genuine backend
boundary, and it must never trust that incoming data is well-formed just because a trusted
frontend usually sends it correctly.

## Consistent Response Shapes

```json
// Success
{ "data": { "id": "p1", "name": "Keyboard" } }

// Error
{ "error": { "message": "Product not found", "code": "NOT_FOUND" } }
```

Adopting one consistent envelope shape across every endpoint (rather than each one improvising its
own success/error format) makes an API's responses predictable for any client consuming it — a
small, deliberate design decision worth making explicitly and applying consistently project-wide.

## Common Mistakes

- Designing an API's URL structure and methods ad hoc per feature, rather than following a
  consistent resource-based convention across the whole project.
- Skipping input validation because "the frontend already validates it" — a Route Handler is a
  real network boundary, reachable by any client, not only the frontend it was built alongside.
- Using inconsistent response shapes across different endpoints, forcing every consumer to handle
  each one's format as a special case.

## Next

Continue to [api-error-handling.md](api-error-handling.md) for handling failures consistently
across every endpoint.
