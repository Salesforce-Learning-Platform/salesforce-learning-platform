# The Node.js Runtime

## Globals Available Without Importing Anything

```js
console.log("works exactly like the browser console");

setTimeout(() => console.log("also works, same as the browser"), 1000);

console.log(__dirname);  // the absolute path of the current file's folder
console.log(__filename); // the absolute path of the current file itself
```

Some globals are shared with the browser (`console`, `setTimeout`, `setInterval`) — familiar from
the [JavaScript domain](../../frontend/javascript/). Others are Node-specific: `__dirname` and
`__filename` exist because a Node script, unlike a browser page, always runs from a real location
on a real file system, and frequently needs to know exactly where.

## The `process` Object

```js
console.log(process.argv);      // command-line arguments the script was run with
console.log(process.env.NODE_ENV); // environment variables (see the dedicated
                                     // environment-variables.md in the next module)
console.log(process.platform);  // "darwin", "linux", "win32" — the OS running this

process.exit(1); // exit the program immediately, with an error status code
```

`process` is Node's window into the currently running program itself and its environment — how it
was started, what environment variables it has access to, what operating system it's running on,
and the ability to end the program with a specific exit code (used by process managers and CI
systems to detect success or failure).

## No `window`, No `document` — And Why That's Correct, Not a Bug

```js
console.log(typeof window);   // "undefined" — there is no window
console.log(typeof document); // "undefined" — there is no page to represent
```

A Node.js script has no browser tab, no page, and nothing to render — so there's genuinely nothing
for `window` or `document` to represent. This isn't a missing feature; it's the runtime correctly
reflecting that it's built for a different job.

## `global`, Node's Equivalent of the Browser's `window`

```js
global.myAppVersion = "1.0.0"; // rarely done deliberately, but demonstrates
                                 // that `global` plays the same structural
                                 // role `window` does in a browser
```

Just as browser JavaScript implicitly has access to `window` as its top-level global object, Node
provides `global` — though in practice, relying on it directly is uncommon and generally
discouraged in favor of Node's module system (covered in the next module,
[Node.js Core Concepts](../nodejs-core-concepts/)), which keeps values properly scoped to the files
that actually need them.

## Common Mistakes

- Expecting `window` or `document` to exist in a Node script and being confused by a resulting
  `ReferenceError` — there's no browser context for those objects to describe.
- Reaching for `global` to share values between files, instead of using Node's module system
  (`require`/`module.exports`, or ES Modules' `import`/`export`) — the idiomatic and far more
  maintainable approach, covered next.
- Forgetting that `process.env` values are always strings, even for something that looks like a
  number or boolean (`process.env.PORT` is the string `"3000"`, not the number `3000`) — a common
  source of subtle bugs when comparing or using them directly.

## Next

Continue to [setting-up-nodejs.md](setting-up-nodejs.md) to actually install Node and run your
first script.
