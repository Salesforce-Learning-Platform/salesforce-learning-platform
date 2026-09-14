# Route Handlers

## Creating One

```ts
// app/api/products/route.ts
export async function GET() {
  const products = await fetch("https://api.example.com/products").then(res => res.json());
  return Response.json(products);
}
```

A `route.ts` (or `.js`) file, placed anywhere inside `app` following the same
[file-based routing](../app-router-deep-dive/file-based-routing.md) conventions as `page.tsx`,
creates a genuine HTTP endpoint — here, `/api/products`. Unlike a `page.tsx`, which returns JSX, a
`route.ts` exports functions named after HTTP methods and returns a `Response`.

## One Export Per HTTP Method

```ts
// app/api/products/route.ts
export async function GET() {
  const products = await getProducts();
  return Response.json(products);
}

export async function POST(request: Request) {
  const newProduct = await request.json();
  const created = await createProduct(newProduct);
  return Response.json(created, { status: 201 });
}
```

This directly mirrors [http-methods-in-depth.md](../../foundations/understanding-http-and-https/http-methods-in-depth.md)
— `GET` for retrieval, `POST` for creation — each method gets its own named export, and a method
with no matching export automatically responds with `405 Method Not Allowed`.

## Route Handlers Coexist with Pages

```text
app/
├── products/
│   └── page.tsx          # renders the HTML product listing page — "/products"
└── api/
    └── products/
        └── route.ts         # a genuine JSON API endpoint — "/api/products"
```

A folder can contain either a `page.tsx` (rendering UI) or a `route.ts` (returning raw responses),
but not both at the same segment — the conventional `app/api/` prefix, while not strictly
required, is a widely-used pattern for clearly separating actual API endpoints from UI routes.

## Dynamic Segments Work Identically

```ts
// app/api/products/[slug]/route.ts
export async function GET(request: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await getProductBySlug(slug);
  return Response.json(product);
}
```

This is the exact same `[slug]` dynamic segment mechanism from
[dynamic-routes.md](../app-router-deep-dive/dynamic-routes.md), applied to an API endpoint instead
of a page — `params` is delivered the same way, as a `Promise`.

## Common Mistakes

- Adding both a `page.tsx` and a `route.ts` at the exact same route segment, which Next.js doesn't
  support — pick one purpose per segment.
- Forgetting that an unhandled method automatically returns `405`, and being surprised a `DELETE`
  request fails when only `GET`/`POST` were exported.
- Using `app/api/` inconsistently — while not mandatory, picking one convention and following it
  project-wide keeps API routes easy to find.

## Next

Continue to [request-and-response.md](request-and-response.md) for actually reading incoming data
and shaping what's sent back.
