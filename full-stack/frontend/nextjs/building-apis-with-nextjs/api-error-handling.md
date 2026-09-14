# API Error Handling

## Applying the Status Code Taxonomy

Every Route Handler response should use the correct status code, exactly per
[http-status-codes-in-depth.md](../../foundations/understanding-http-and-https/http-status-codes-in-depth.md):

```ts
// app/api/products/[slug]/route.ts
export async function GET(request: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const product = await getProductBySlug(slug);

  if (!product) {
    return Response.json({ error: "Product not found" }, { status: 404 });
  }

  return Response.json(product); // defaults to 200
}
```

A client calling this endpoint can rely on the standard first-digit triage — a `404` means "check
the slug," a `500` means "something's actually broken server-side" — without needing to parse the
response body just to know which category of problem occurred.

## Catching Unexpected Errors

```ts
export async function POST(request: Request) {
  try {
    const body = await request.json();
    const product = await createProduct(body);
    return Response.json(product, { status: 201 });
  } catch (error) {
    console.error("Failed to create product:", error);
    return Response.json({ error: "Internal server error" }, { status: 500 });
  }
}
```

This is the same `try`/`catch` discipline from
[try-catch-finally.md](../../javascript/error-handling-and-debugging/try-catch-finally.md), applied
at an API boundary — without it, an unexpected error (a database connection failure, a malformed
`request.json()` call) would surface as an unhandled exception rather than a clean, predictable
error response the calling client can actually handle.

## Distinguishing Client Errors from Server Errors

```ts
export async function POST(request: Request) {
  let body;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Invalid JSON" }, { status: 400 }); // client's fault
  }

  if (!body.name) {
    return Response.json({ error: "name is required" }, { status: 400 }); // client's fault
  }

  try {
    const product = await createProduct(body);
    return Response.json(product, { status: 201 });
  } catch (error) {
    console.error(error);
    return Response.json({ error: "Internal server error" }, { status: 500 }); // server's fault
  }
}
```

Separating validation failures (client sent something wrong: `400`) from unexpected internal
failures (something broke on the server's side: `500`) gives the calling client — and whoever
debugs an incident later — an immediate, accurate signal about where the actual problem lies,
directly the same distinction emphasized throughout
[http-status-codes-in-depth.md](../../foundations/understanding-http-and-https/http-status-codes-in-depth.md).

## Never Leak Internal Details in Error Responses

```ts
// WRONG — exposes internal implementation detail to any caller
return Response.json({ error: error.message, stack: error.stack }, { status: 500 });

// CORRECT — a generic message to the client; full detail only in server-side logs
console.error(error); // full detail, visible only in server logs
return Response.json({ error: "Internal server error" }, { status: 500 });
```

An error's full message or stack trace can reveal internal implementation details (database
structure, file paths, library versions) useful to an attacker — log the full detail server-side
for debugging, but return only a generic, safe message to the actual client.

## Common Mistakes

- Returning `200 OK` for a request that actually failed, with the error only described in the
  response body — this breaks any tooling or client code that reasonably assumes a `2xx` status
  means success.
- Letting an uncaught exception crash the handler with no `try`/`catch`, producing an unhelpful
  generic error rather than a clean, deliberate error response.
- Including a full stack trace or internal error message in a response sent to the client,
  leaking implementation details that should only ever appear in server-side logs.

## Module Summary

Across this module: Route Handlers (`route.ts`) create genuine HTTP endpoints using the same
web-standard `Request`/`Response` objects as the Fetch API, with one export per HTTP method (see
[route-handlers.md](route-handlers.md)); reading request bodies, query params, cookies, and
headers, and shaping a `Response`, all use standard web APIs plus a few Next.js conveniences (see
[request-and-response.md](request-and-response.md)); resource-based URL structure, query-param
filtering, and consistent response shapes make an API predictable for any client (see
[api-design-patterns.md](api-design-patterns.md)); and correct, consistent status codes plus
careful error handling — never leaking internal detail — make failures debuggable and safe (this
file).
