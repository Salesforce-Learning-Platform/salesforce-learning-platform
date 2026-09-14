# Request and Response

## Reading a JSON Body

```ts
// app/api/cart/route.ts
export async function POST(request: Request) {
  const { productId, quantity } = await request.json();
  const updatedCart = await addToCart(productId, quantity);
  return Response.json(updatedCart);
}
```

`request.json()` parses the request body — the exact same standard `Request` object and method
used on the *calling* side back in
[fetch-api.md](../../javascript/asynchronous-programming-and-modules/fetch-api.md); a Route
Handler is simply the receiving end of that same web-standard interface.

## Reading Query Parameters

```ts
// app/api/products/route.ts
import { type NextRequest } from "next/server";

export function GET(request: NextRequest) {
  const category = request.nextUrl.searchParams.get("category");
  const products = category ? getProductsByCategory(category) : getAllProducts();
  return Response.json(products);
}
```

For `/api/products?category=electronics`, `request.nextUrl.searchParams.get("category")` returns
`"electronics"` — `NextRequest`'s `nextUrl` is a Next.js-specific convenience over the standard
`URL` object, parsing the query string for you.

## Reading Headers and Cookies

```ts
import { cookies, headers } from "next/headers";

export async function GET() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get("session_id")?.value;

  const headersList = await headers();
  const userAgent = headersList.get("user-agent");

  // ...
}
```

This directly reuses the cookie concepts from
[cookies.md](../../javascript/using-browser-functionalities/cookies.md) — here read on the server
side, from the actual incoming request, rather than via `document.cookie` in the browser.

## Returning a Response

```ts
// Simple JSON shorthand
return Response.json({ message: "Success" });

// With an explicit status code
return Response.json({ error: "Product not found" }, { status: 404 });

// With custom headers
return new Response(JSON.stringify(data), {
  status: 200,
  headers: { "Content-Type": "application/json" },
});
```

`Response.json(...)` is a convenient shorthand that automatically sets the `Content-Type` header
and serializes the body — for anything beyond a simple JSON response (custom headers, a non-JSON
body), constructing a `new Response(...)` directly gives full control, exactly matching the
[http-headers-in-depth.md](../../foundations/understanding-http-and-https/http-headers-in-depth.md)
concepts from earlier in this platform.

## Reading Form Data

```ts
export async function POST(request: Request) {
  const formData = await request.formData();
  const email = formData.get("email");
  return Response.json({ email });
}
```

For a form submitted with `enctype="multipart/form-data"` or a plain HTML form post (rather than
JSON), `request.formData()` parses it — directly relevant if a Route Handler receives a submission
from the plain HTML forms covered in
[form-submission-and-data.md](../../html/html-forms-and-user-input/form-submission-and-data.md).

## Common Mistakes

- Calling `request.json()` on a request that isn't actually JSON (a form submission or webhook
  payload in a different format), which throws a parsing error.
- Forgetting `await` on `cookies()`/`headers()` — these are asynchronous functions in the current
  Next.js API, not synchronous property access.
- Manually setting `Content-Type: application/json` when using `Response.json()`, which already
  sets it automatically — redundant, though harmless.

## Next

Continue to [api-design-patterns.md](api-design-patterns.md) for structuring a coherent set of
endpoints, not just individual handlers.
