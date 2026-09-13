# Installing a Package Manager and Node.js

## What Node.js Is

**Node.js** is a JavaScript runtime that executes JavaScript outside a browser — on your machine
directly. Frontend tooling (build tools, dev servers, linters, test runners) is almost universally
written in JavaScript and run via Node, which is why installing Node is a prerequisite for
essentially every modern frontend project, even ones that ultimately ship code that only runs in
a browser.

## What a Package Manager Does

A **package manager** (`npm`, which ships with Node.js, or alternatives like `yarn`/`pnpm`) does
three related jobs:

1. **Installs dependencies** — downloads the libraries your project needs (React, a CSS
   framework, testing tools) from a public registry, based on a manifest file.
2. **Tracks versions** — records exactly which versions of which packages your project depends
   on, in `package.json`, so the project is reproducible on another machine.
3. **Runs scripts** — `package.json` can define named commands (`npm run dev`, `npm run build`)
   that wrap the actual tool invocations, so the whole team runs the same command regardless of
   what's happening underneath.

## `package.json` and `node_modules`

- **`package.json`** is the project's manifest: its name, version, dependencies, and scripts.
- **`node_modules/`** is where actual downloaded dependency code lives once installed. It's large,
  fully regenerable from `package.json`, and is why every real project's `.gitignore` excludes it
  — committing it would bloat the repository with something `npm install` can always recreate.
- **`package-lock.json`** (or `yarn.lock`/`pnpm-lock.yaml`) pins the *exact* resolved version of
  every dependency (including dependencies of dependencies), so that "it works on my machine" is
  less likely to mean "it fails on someone else's" due to a silently different version.

## Verifying Your Installation

After installing Node.js (via an installer, a version manager like `nvm`, or a system package
manager), two commands confirm it worked:

```bash
node --version
npm --version
```

Using a **version manager** (such as `nvm` on macOS/Linux, or `nvm-windows`) rather than a single
system-wide install is standard practice — it lets you switch Node versions per project, since
different projects may require different Node versions.

## Common Mistakes

- Committing `node_modules/` to version control — bloats the repository and defeats the purpose
  of the lock file.
- Deleting `package-lock.json` "to fix an issue" without understanding that this can silently
  upgrade dependencies to newer versions than what the rest of the team is using.
- Installing a global package when a project-local one was intended (or vice versa), leading to
  "it works from the terminal but not when the project runs it."

## Next

Continue to [setting-up-your-code-editor.md](setting-up-your-code-editor.md) to configure the
editor you'll use to write the code these tools will run.
