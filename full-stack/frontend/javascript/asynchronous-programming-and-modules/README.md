# Asynchronous Programming and Modules

## Purpose

Real applications wait on things — network requests, timers, user input — without freezing the
rest of the page while they do. This module covers JavaScript's evolution of asynchronous patterns
(callbacks → Promises → async/await), the Fetch API for network requests, and JavaScript modules
for organizing code across files.

## Learning Objectives

- Explain why callbacks alone don't scale well, and what Promises improve.
- Use `.then()`/`.catch()` and `async`/`await` correctly and interchangeably in understanding.
- Make and handle network requests with the Fetch API, including error handling.
- Use `import`/`export` to organize code across modules.

## Prerequisites

[JavaScript Error Handling and Debugging](../error-handling-and-debugging/) and
[Understanding HTTP and HTTPS](../../foundations/understanding-http-and-https/).

## Files in This Module

| File | Covers |
|---|---|
| [callbacks.md](callbacks.md) | The original async pattern, and why it doesn't scale ("callback hell") |
| [promises.md](promises.md) | Promise states, `.then()`/`.catch()`, and `Promise.all()` |
| [async-await.md](async-await.md) | Syntactic sugar over Promises that reads like synchronous code |
| [fetch-api.md](fetch-api.md) | Making HTTP requests from JavaScript |
| [javascript-modules.md](javascript-modules.md) | `import`/`export`, named vs. default exports |

## When to Deep-Dive vs. Skim

Deep-dive [promises.md](promises.md) even if you plan to write only `async`/`await` day to day —
`async`/`await` is built directly on Promises, and understanding what's actually happening
underneath (especially error propagation and `Promise.all()`) prevents a category of confusing
bugs `async`/`await`'s clean syntax can otherwise hide.

## Quick Knowledge Check

<details>
<summary>Is `async`/`await` a completely different mechanism from Promises, or built on top of them?</summary>

Built directly on top — `async`/`await` is syntactic sugar that makes Promise-based code read like
synchronous code. An `async` function always returns a Promise, and `await` unwraps a Promise's
resolved value. See [async-await.md](async-await.md).

</details>

<details>
<summary>Why does `fetch()` not throw an error (via a rejected promise) for a 404 or 500 response?</summary>

`fetch()` only rejects for network-level failures (the request couldn't complete at all) — an HTTP
error status is still a "successful" fetch as far as the Promise is concerned. Checking
`response.ok` explicitly is required to detect an error status. See [fetch-api.md](fetch-api.md).

</details>

## References

- MDN Web Docs, [Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
- MDN Web Docs, [Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- MDN Web Docs, [JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)

## Continue Your Learning Path

Next: [JavaScript Event Loop](../event-loop/) — see the
[Frontend learning path](../../README.md) for the full sequence.
