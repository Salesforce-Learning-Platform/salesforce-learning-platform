# What Is Node.js?

## A JavaScript Runtime, Not a New Language

```js
// This file runs identically whether it's executed by Node.js on a
// server, or (with minor API differences) inside a browser's console —
// it's the same JavaScript language either way.
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}
```

**Node.js** is a JavaScript **runtime** — an environment that executes JavaScript code — built on
Google Chrome's **V8 engine**, the same engine that runs JavaScript inside Chrome itself. Node
takes that engine out of the browser entirely and pairs it with a different set of built-in
capabilities suited to running on a server, rather than inside a web page.

## What's Different From the Browser

| In a browser | In Node.js |
|---|---|
| `window`, `document` — the DOM | No DOM at all; there's no page to manipulate |
| `fetch` to talk to a server | Built-in modules to *be* the server (`http`, `net`) |
| `localStorage` | Direct file system access (`fs`) |
| Sandboxed for security (a webpage can't read your files) | Full access to the machine it runs on |

The language itself — variables, functions, classes, promises, everything from the
[JavaScript domain](../../frontend/javascript/) — is identical. What changes entirely is the
**environment** around it: the global objects and built-in modules available, because a server has
fundamentally different responsibilities than a web page (reading files, talking to databases,
serving many simultaneous clients) than a browser does.

## Why JavaScript on the Server At All

Before Node.js (released in 2009), JavaScript existed almost exclusively in browsers, while servers
were typically written in a separate language (Java, PHP, Ruby, Python). Node.js's core appeal is
**one language across the entire stack**: the same developer, and often the same code (validation
logic, date formatting, business rules), can be shared between the frontend and backend, and a team
doesn't need to context-switch between two different languages' idioms to work on either side.

## Common Mistakes

- Assuming Node.js is a different programming language that merely resembles JavaScript — it's the
  literal same language and, largely, the same engine, just in a different environment.
- Expecting browser-only APIs (`document`, `window`, `localStorage`) to exist in Node — they don't,
  because there's no browser page for them to represent.
- Underestimating how much of your existing JavaScript knowledge transfers directly — control flow,
  functions, async/await, and the whole language work exactly the same; only the surrounding APIs
  differ.

## Next

Continue to [how-nodejs-works.md](how-nodejs-works.md) to see the architecture underneath — V8,
libuv, and the event loop — that makes Node particularly well-suited to server workloads.
