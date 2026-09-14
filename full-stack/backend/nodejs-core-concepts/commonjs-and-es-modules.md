# CommonJS and ES Modules

## CommonJS — Node's Original System

```js
// math.js
const PI = 3.14159;

function circleArea(radius) {
  return PI * radius ** 2;
}

module.exports = { circleArea };
```

```js
// app.js
const { circleArea } = require("./math");
console.log(circleArea(4));
```

**CommonJS** is Node's original module system: `require()` loads a module, and `module.exports`
declares what it makes available. `require()` calls are **synchronous** — execution genuinely
pauses until the required file has fully loaded — which works because CommonJS was designed
specifically for a server's local file system, where loading a file is fast, unlike a browser
loading a module over the network.

## ES Modules — the Standardized System

```js
// math.mjs
export const PI = 3.14159;

export function circleArea(radius) {
  return PI * radius ** 2;
}
```

```js
// app.mjs
import { circleArea } from "./math.mjs";
console.log(circleArea(4));
```

**ES Modules (ESM)** use the same `import`/`export` syntax already familiar from
[the browser](../../frontend/javascript/asynchronous-programming-and-modules/) — this is the
officially standardized JavaScript module format, not a Node-specific invention. Node supports it
alongside CommonJS, not as a replacement (yet) — real Node code today still frequently uses both,
depending on the project's age and choices.

## Telling Node Which System a File Uses

```json
{
  "type": "module"
}
```

By default, a `.js` file in Node is treated as CommonJS. Adding `"type": "module"` to
`package.json` switches every `.js` file in that package to ES Modules instead. The `.mjs`
extension always forces ES Modules regardless of that setting, and `.cjs` always forces CommonJS —
useful when a project needs to mix both intentionally.

## Concrete Differences That Matter

| | CommonJS | ES Modules |
|---|---|---|
| Import syntax | `require("./math")` | `import { circleArea } from "./math.mjs"` |
| File extension in the import | Optional | **Required** |
| Loading | Synchronous | Can be asynchronous (supports top-level `await`) |
| `__dirname`/`__filename` | Available directly | Not available — use `import.meta.dirname` instead |
| Top-level `await` | Not supported | Supported |

The file-extension requirement is a common early surprise: `import { circleArea } from "./math"`
(without `.mjs`) throws an error in ESM, whereas the equivalent CommonJS `require("./math")` works
fine without an extension.

## Which to Choose for a New Project

ES Modules is the better default for new projects: it's the same standard syntax used across
browsers and the wider JavaScript ecosystem (no separate mental model needed switching between
frontend and backend code), and it's fully stable in modern Node. CommonJS remains essential to
*recognize*, though — a huge amount of existing, real-world Node code (and many older or
still-actively-maintained npm packages) is written in it.

## Common Mistakes

- Forgetting the file extension in an ES Module `import` path — required, unlike CommonJS's
  optional extension.
- Trying to use `require()` inside a file Node treats as an ES Module (or vice versa) without the
  interop mechanisms — each file, and often each whole package, needs to commit to one system.
- Assuming `__dirname` is available in ESM — it isn't; `import.meta.dirname` is the ESM
  replacement, following the same reasoning as
  [nodejs-runtime.md](../starting-with-nodejs/nodejs-runtime.md)'s coverage of Node's runtime
  globals.

## Next

Continue to [file-system.md](file-system.md) to use Node's built-in modules for something concrete
— reading and writing real files.
