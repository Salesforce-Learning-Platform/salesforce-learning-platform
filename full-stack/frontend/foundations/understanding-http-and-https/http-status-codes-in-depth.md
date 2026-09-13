# HTTP Status Codes in Depth

## The Five Classes

Every HTTP response carries a three-digit status code. The first digit tells you the class of
outcome before you even read the specific code:

| Class | Meaning | Who is "responsible" |
|---|---|---|
| 1xx Informational | The request was received, processing continues | Neither — transitional |
| 2xx Success | The request was received, understood, and accepted | — |
| 3xx Redirection | Further action is needed to complete the request | — |
| 4xx Client Error | The request has a problem the client caused | Client |
| 5xx Server Error | The server failed to fulfill a valid request | Server |

This first-digit triage is the single most useful habit for fast debugging: a 4xx means *check
what you sent*; a 5xx means *the problem is on the other side*, regardless of how correct your
request was.

## The Codes Worth Knowing by Name

| Code | Name | When it's used |
|---|---|---|
| `200` | OK | Standard success |
| `201` | Created | A `POST`/`PUT` successfully created a new resource |
| `204` | No Content | Success, but there's nothing to return in the body (common after a `DELETE`) |
| `301` | Moved Permanently | The resource now lives at a different URL, permanently — clients should update their reference |
| `302` | Found | A temporary redirect |
| `304` | Not Modified | The client's cached copy is still valid — sent in response to a conditional request (e.g., using `If-None-Match`) |
| `400` | Bad Request | The request is malformed or fails validation |
| `401` | Unauthorized | The client is not authenticated (despite the name, this is about *identity*, not permission) |
| `403` | Forbidden | The client is authenticated but not allowed to perform this action |
| `404` | Not Found | No resource exists at this URL |
| `409` | Conflict | The request conflicts with the current state of the resource (e.g., a duplicate) |
| `422` | Unprocessable Entity | The request is well-formed but fails semantic/business validation |
| `429` | Too Many Requests | The client has been rate-limited |
| `500` | Internal Server Error | An unhandled failure on the server |
| `502` | Bad Gateway | A server acting as a proxy/gateway got an invalid response from an upstream server |
| `503` | Service Unavailable | The server is temporarily unable to handle the request (overloaded, in maintenance) |
| `504` | Gateway Timeout | A proxy/gateway didn't get a timely response from an upstream server |

## 401 vs. 403 — Precisely

This pair is one of the most consistently misused in real APIs:

- **401 Unauthorized** really means "unauthenticated" — the server doesn't know who you are (a
  missing or invalid credential/token).
- **403 Forbidden** means the server knows exactly who you are, and the answer is still no — you
  don't have permission for this specific action or resource.

A request with no auth token at all should typically get `401`; a request from a properly
authenticated user trying to access another user's private data should get `403`.

## Why the Distinction Matters for Debugging

Given the first-digit triage above, seeing a `500` when you expected a `404` tells you immediately
that the problem is server-side logic, not a URL typo — you'd go look at server logs, not your
request. Seeing a `429` tells you to slow down and implement backoff, not to assume your code is
broken. Reasoning from the status code first, before diving into logs or code, consistently
narrows down where to look.

## Common Mistakes

- Returning `200 OK` with an error described only in the response body. This breaks tooling and
  caching that reasonably assumes `2xx` means success, and hides real errors from monitoring.
- Confusing `401` and `403`, which leads to confusing client-side error handling (e.g., redirecting
  an authenticated-but-unauthorized user to a login page instead of an appropriate "access denied"
  message).
- Treating every 4xx as "my fault as the developer." A `429` is often just normal, expected
  throttling behavior to handle gracefully, not a bug.

## Next

Continue to [http-headers-in-depth.md](http-headers-in-depth.md) to see the metadata that rides
alongside every request and response.
