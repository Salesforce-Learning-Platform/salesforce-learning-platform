# Modules

## Why Split Code Across Files At All

```js
// Without modules: everything crammed into one file, growing without bound
function hashPassword(password) { /* ... */ }
function createUser(data) { /* ... */ }
function sendWelcomeEmail(user) { /* ... */ }
function calculateShipping(cart) { /* ... */ }
// ...hundreds more lines, no real separation between concerns
```

As a real backend application grows, one giant file quickly becomes impossible to navigate,
[per the same reasoning](../../frontend/frontend-architecture/reading-and-navigating-unfamiliar-codebases/understanding-project-structure.md)
that makes structured folders matter on the frontend. A **module** is simply one file, treated as
its own self-contained unit: it can keep some things private (helper functions only it needs) and
explicitly **export** the specific pieces other files are meant to use.

## The Core Idea: Export and Import

```js
// user-service.js — exports only what other files actually need
function hashPassword(password) { /* private, not exported */ }

function createUser(data) {
  // uses hashPassword internally
}

module.exports = { createUser };
```

```js
// server.js — imports only createUser, nothing else
const { createUser } = require("./user-service");
```

Every module in Node explicitly declares its public surface (what it **exports**) and every
consuming file explicitly declares what it needs (what it **imports** or `require`s). This is a
deliberate, explicit contract — unlike the single giant file above, `server.js` can see and use
`createUser` but has no access to `hashPassword` at all, since `user-service.js` never exported it.

## Two Competing Module Systems in Node

Node.js actually supports **two** different module syntaxes:

- **CommonJS** (`require`/`module.exports`) — Node's original, long-standing system.
- **ES Modules** (`import`/`export`) — the same standardized syntax already familiar from
  [ES Modules in the browser](../../frontend/javascript/asynchronous-programming-and-modules/).

Both exist, in the same runtime, for historical reasons — Node predates ES Modules being
standardized in JavaScript at all, so it built CommonJS first and added ESM support later. The next
file, [commonjs-and-es-modules.md](commonjs-and-es-modules.md), covers the real differences and how
to choose between them.

## Built-in, Third-Party, and Your Own Modules

```js
const fs = require("node:fs");        // built-in — ships with Node itself
const express = require("express");    // third-party — installed via npm
const userService = require("./user-service"); // your own — a local file
```

Every `require`/`import` falls into one of three categories: Node's own **built-in modules**
(prefixed with `node:` as the modern convention, per
[npm-and-package-management.md](../starting-with-nodejs/npm-and-package-management.md)'s coverage
of dependencies), **third-party packages** installed from npm, or **your own local files**,
referenced by a relative path starting with `./` or `../`.

## Common Mistakes

- Exporting far more than a module's consumers actually need, eroding the same "explicit public
  surface" benefit modules exist to provide.
- Reaching for a third-party npm package for something Node's own built-in modules (`fs`, `path`,
  `http`) already handle perfectly well.
- Mixing CommonJS and ES Module syntax carelessly within the same file — each file needs to
  commit to one system, as the next file explains.

## Next

Continue to [commonjs-and-es-modules.md](commonjs-and-es-modules.md) to see exactly how the two
module systems differ, and which to use.
