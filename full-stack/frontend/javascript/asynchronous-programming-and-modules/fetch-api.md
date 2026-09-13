# The Fetch API

## Making a Basic Request

```js
async function loadUser(id) {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  return data;
}
```

`fetch()` returns a Promise that resolves to a `Response` object once the response headers have
arrived — the body itself is read separately (via `.json()`, `.text()`, etc.), which is itself
another asynchronous step returning its own Promise.

## The Critical Gotcha: `fetch()` Doesn't Reject on HTTP Errors

```js
async function loadUser(id) {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}
```

This is genuinely easy to miss: `fetch()`'s Promise only **rejects** for network-level failures
(no connection at all, DNS failure, CORS being blocked) — a `404` or `500` response is still a
"successful" fetch as far as the Promise is concerned, since the request genuinely got a response.
Checking `response.ok` (true for status codes 200–299, per
[http-status-codes-in-depth.md](../../foundations/understanding-http-and-https/http-status-codes-in-depth.md))
explicitly is required to detect an HTTP-level error and handle it deliberately.

## Sending Data

```js
async function createUser(userData) {
  const response = await fetch("/api/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });
  return response.json();
}
```

This directly applies [http-methods-in-depth.md](../../foundations/understanding-http-and-https/http-methods-in-depth.md)
and [http-headers-in-depth.md](../../foundations/understanding-http-and-https/http-headers-in-depth.md) —
the method, headers, and body are configured explicitly as an options object, since `fetch()`
defaults to a `GET` request with no body otherwise.

## Handling Both Network and HTTP Failures

```js
async function loadUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    // catches BOTH network-level failures (fetch() rejected)
    // AND the HTTP-error case thrown explicitly above
    console.error("Failed to load user:", error);
    throw error;
  }
}
```

## Common Mistakes

- Assuming a resolved `fetch()` Promise means success, without checking `response.ok` — silently
  treating a `404` or `500` response as if the data it "returned" were valid.
- Forgetting `Content-Type: application/json` when sending a JSON body — many servers rely on this
  header to correctly parse the incoming request.
- Calling `.json()` on a response that isn't actually JSON (an error page, an empty body), which
  throws its own separate parsing error that needs its own handling.

## Next

Continue to [javascript-modules.md](javascript-modules.md) for organizing code like this across
multiple files.
