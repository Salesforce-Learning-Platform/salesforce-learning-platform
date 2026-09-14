# The Path Module

## The Problem With Manual String Concatenation

```js
// AVOID — hardcodes a forward slash, breaking on Windows (which uses \)
const configPath = "config" + "/" + "settings.json";
```

Windows and POSIX systems (macOS, Linux) use different path separators (`\` vs `/`). Code that
builds a file path by manually concatenating strings with a hardcoded separator works on exactly
one type of operating system and silently breaks on the other — a real, common bug in codebases
that assume a single platform.

## `path.join()` — Cross-Platform Path Building

```js
import { join } from "node:path";

const configPath = join("config", "settings.json");
// "config/settings.json" on macOS/Linux, "config\settings.json" on Windows
```

`path.join()` combines segments using whatever separator the current operating system actually
uses, and normalizes the result — collapsing redundant segments (`join("a", "..", "b")` becomes
`"b"`) automatically, rather than requiring that logic to be handled by hand.

## `path.resolve()` — Getting an Absolute Path

```js
import { resolve } from "node:path";

const absolutePath = resolve("config", "settings.json");
// e.g. "/Users/you/project/config/settings.json"
```

`path.resolve()` produces a genuine **absolute** path, resolving relative segments against the
current working directory when no leading absolute segment is given. This directly solves
[file-system.md](file-system.md)'s "which directory does a relative path actually resolve
from" problem — `resolve()` makes that resolution explicit and predictable instead of implicit and
easy to get wrong.

## Combining With `__dirname` for Reliability

```js
import { join } from "node:path";

// Resolves relative to THIS FILE's own location, not the process's
// working directory — reliable no matter where the script was started from
const configPath = join(__dirname, "config", "settings.json");
```

The most robust real-world pattern combines `path.join()` with `__dirname` (covered in
[nodejs-runtime.md](../starting-with-nodejs/nodejs-runtime.md)) — building a path relative to
*where this specific file lives on disk*, rather than relative to whatever directory the process
happened to be started from, which can vary depending on how the script is actually invoked.

## `path.basename()` and `path.extname()`

```js
import { basename, extname } from "node:path";

basename("/uploads/profile-photo.jpg"); // "profile-photo.jpg"
extname("/uploads/profile-photo.jpg");  // ".jpg"
```

`basename()` extracts just the file name from a full path — useful for displaying an uploaded
file's name without exposing its full server-side storage path. `extname()` extracts the file
extension — commonly used to validate an upload's type before accepting it.

## Common Mistakes

- Concatenating path segments with a hardcoded `/` or `\`, producing code that only works
  correctly on one operating system.
- Using a bare relative path (`"./config.json"`) in file operations without realizing it depends
  on the process's current working directory rather than the file's own location.
- Forgetting that `path.join()` normalizes the path but does **not** make it absolute — `resolve()`
  is the function for that; the two solve related but different problems.

## Next

Continue to [environment-variables.md](environment-variables.md) to configure a real application
without hardcoding sensitive values directly into the source code.
