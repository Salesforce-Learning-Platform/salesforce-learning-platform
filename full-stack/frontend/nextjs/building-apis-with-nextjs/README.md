# Building APIs with Next.js

## Purpose

Server Components (from
[server-components.md](../rendering-strategies/server-components.md)) can fetch data directly,
but sometimes an application needs a genuine HTTP endpoint — for a mobile app calling the same
backend, a webhook receiver, or a third-party integration. **Route Handlers** let you build these
directly inside a Next.js project, without a separate backend service. Every example continues the
e-commerce store used throughout this domain.

## Learning Objectives

- Create a Route Handler and export functions for the HTTP methods it should support.
- Read a request's body, query parameters, and headers using standard Web APIs.
- Return correctly-structured JSON responses with appropriate status codes.
- Handle errors in a Route Handler the same way a dedicated backend would.

## Prerequisites

[App Router Deep Dive](../app-router-deep-dive/) and
[Understanding HTTP and HTTPS](../../foundations/understanding-http-and-https/).

## Files in This Module

| File | Covers |
|---|---|
| [route-handlers.md](route-handlers.md) | Creating a `route.ts` file and its HTTP method exports |
| [request-and-response.md](request-and-response.md) | Reading request data and returning a `Response` |
| [api-design-patterns.md](api-design-patterns.md) | Structuring endpoints, dynamic segments, and query params |
| [api-error-handling.md](api-error-handling.md) | Consistent error responses and status codes |

## When to Deep-Dive vs. Skim

Deep-dive [api-error-handling.md](api-error-handling.md) — this directly reapplies the status-code
taxonomy from
[http-status-codes-in-depth.md](../../foundations/understanding-http-and-https/http-status-codes-in-depth.md),
and getting it right is what makes an API genuinely usable by any client, not just the specific
frontend it was originally built alongside.

## Quick Knowledge Check

<details>
<summary>Does a Route Handler use the same Request/Response objects covered in the Fetch API module, or a Next.js-specific format?</summary>

The standard Web `Request` and `Response` APIs — the same ones from
[fetch-api.md](../../javascript/asynchronous-programming-and-modules/fetch-api.md), just used on
the receiving end this time instead of the calling end. `NextRequest` extends `Request` with a few
Next.js-specific conveniences, but the underlying objects are the same web-standard ones. See
[route-handlers.md](route-handlers.md).

</details>

<details>
<summary>A POST request to your Route Handler is missing a required field. What status code should the response use?</summary>

`400 Bad Request` — the client sent a malformed request; this is a direct application of
[http-status-codes-in-depth.md](../../foundations/understanding-http-and-https/http-status-codes-in-depth.md)'s
first-digit triage (4xx means check what the client sent). See
[api-error-handling.md](api-error-handling.md).

</details>

## References

- Next.js, [route.js](https://nextjs.org/docs/app/api-reference/file-conventions/route)

## Continue Your Learning Path

Next: [Working with Server Actions](../working-with-server-actions/) — see the
[Frontend learning path](../../README.md) for the full sequence.
