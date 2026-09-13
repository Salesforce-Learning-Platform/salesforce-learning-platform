# Using Browser Functionalities

## Purpose

Beyond the DOM, the browser exposes JavaScript APIs for things a web application commonly needs:
persisting small amounts of data client-side, and reading/writing cookies. This module covers the
three main mechanisms and, critically, when to use which.

## Learning Objectives

- Explain the difference between `localStorage`, `sessionStorage`, and cookies, and choose
  correctly between them.
- Read, write, and remove data using the Web Storage API.
- Read and write cookies, and explain the security attributes that matter for them.
- Recognize why none of these mechanisms are appropriate for storing sensitive data unprotected.

## Prerequisites

[JavaScript Events](../events/) and
[state-management-across-the-boundary.md](../../foundations/client-server-architecture/state-management-across-the-boundary.md).

## Files in This Module

| File | Covers |
|---|---|
| [browser-apis.md](browser-apis.md) | An overview of what "browser APIs" means, beyond the DOM |
| [local-storage.md](local-storage.md) | `localStorage`: persistent, origin-scoped key-value storage |
| [session-storage.md](session-storage.md) | `sessionStorage`: tab-scoped storage cleared on close |
| [cookies.md](cookies.md) | Reading/writing cookies, and their security attributes |

## When to Deep-Dive vs. Skim

Deep-dive [cookies.md](cookies.md)'s security section before storing anything sensitive
client-side in any of these mechanisms — none of `localStorage`, `sessionStorage`, or
JavaScript-readable cookies are safe places for secrets, and understanding exactly why matters for
building anything handling authentication.

## Quick Knowledge Check

<details>
<summary>You need to remember a user's draft comment if they accidentally close the tab and reopen it later. Which storage should you use?</summary>

`localStorage` — it persists across tabs and browser restarts, unlike `sessionStorage`, which
clears when the tab closes. See [local-storage.md](local-storage.md) and
[session-storage.md](session-storage.md).

</details>

<details>
<summary>Is it safe to store an authentication token in localStorage?</summary>

Not without real caveats — anything in localStorage is readable by any JavaScript running on that
origin, including malicious script injected via an XSS vulnerability (see
[manipulating-elements.md](../dom-manipulation/manipulating-elements.md)). An `HttpOnly` cookie,
which JavaScript cannot read at all, is the more defensible choice for genuinely sensitive tokens.
See [cookies.md](cookies.md).

</details>

## References

- MDN Web Docs, [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API)
- MDN Web Docs, [Using HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies)

## Continue Your Learning Path

Next: [JavaScript Error Handling and Debugging](../error-handling-and-debugging/) — see the
[Frontend learning path](../../README.md) for the full sequence.
