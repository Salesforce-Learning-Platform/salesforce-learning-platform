# The File System Module

## Three Ways to Read a File

```js
import { readFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { readFile as readFileCallback } from "node:fs";

// 1. Synchronous — blocks everything else until done
const data1 = readFileSync("./config.json", "utf8");

// 2. Callback-based — the original, non-blocking style
readFileCallback("./config.json", "utf8", (err, data) => {
  if (err) throw err;
  console.log(data);
});

// 3. Promise-based — non-blocking, works with async/await
const data3 = await readFile("./config.json", "utf8");
```

Node's `fs` module offers the **same underlying operation** in three different styles, echoing
[how-nodejs-works.md](../starting-with-nodejs/how-nodejs-works.md)'s non-blocking I/O model applied
concretely: a **synchronous** version that blocks the entire process until it finishes, a
**callback-based** version (the module's original API), and a **promise-based** version (via
`node:fs/promises`) that pairs naturally with `async`/`await`.

## Choosing the Right One

| Style | Blocks the event loop? | When to use |
|---|---|---|
| `readFileSync` | Yes | Startup-time config loading only, before the server starts handling requests |
| `readFile` (callback) | No | Legacy code, or matching an existing codebase's style |
| `readFile` (`fs/promises`) | No | The default choice for new code |

The sync variant should almost never run while a server is actively handling requests — blocking
the single JavaScript thread means *every other request* has to wait, directly undermining the
concurrency benefit Node's whole architecture is built around. It's genuinely fine at startup,
before the server begins accepting traffic at all, when there's nothing else competing for that
thread yet.

## Writing Files

```js
import { writeFile } from "node:fs/promises";

async function saveOrderLog(order) {
  await writeFile(
    `./logs/order-${order.id}.json`,
    JSON.stringify(order, null, 2),
    "utf8"
  );
}
```

`writeFile` follows the same three-style pattern as reading. Passing a third argument (`"utf8"`)
tells Node to treat the data as text; omitting it writes raw binary data instead — worth being
deliberate about, since a mismatch produces garbled output.

## Checking Whether a File Exists, Safely

```js
import { access } from "node:fs/promises";
import { constants } from "node:fs";

async function fileExists(path) {
  try {
    await access(path, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}
```

There's no direct "does this file exist" boolean check — `access()` either resolves (the file
exists and is accessible) or rejects (it doesn't, or isn't). This mirrors a broader pattern in
real backend code: expecting many file operations to potentially fail, and always handling that
failure explicitly rather than assuming a path is always valid.

## Common Mistakes

- Using `readFileSync`/`writeFileSync` inside a request handler — blocking every other
  simultaneously-connected user while one file operation completes.
- Forgetting to `await` a promise-based `fs` call, silently continuing execution before the file
  operation has actually finished.
- Assuming a relative path (`"./config.json"`) always resolves from the project's root — it
  actually resolves relative to the current working directory the process was *started* from,
  which isn't always the same thing. [path-module.md](path-module.md) covers building reliable
  paths instead.

## Next

Continue to [path-module.md](path-module.md) to build file paths that work correctly regardless of
the operating system or where the process was started from.
