# Setting Up Node.js

## Installing Node.js

The recommended way to install Node is via its official installer or a version manager, choosing
the **LTS (Long-Term Support)** release line rather than the "Current" line for any real project —
LTS versions receive stability and security updates for a much longer window and are what
production applications and most tutorials assume.

```bash
node --version
npm --version
```

Running both commands after installation confirms Node itself, and npm (which ships bundled with
Node), installed correctly.

## Why a Version Manager Is Worth Using

```bash
# Using nvm (Node Version Manager) as an example
nvm install --lts
nvm use --lts
nvm install 20
nvm use 20
```

A **version manager** (like `nvm` on macOS/Linux, or `nvm-windows` on Windows) lets a machine hold
multiple Node versions side by side and switch between them per project. This matters in practice
because different projects — especially older ones you might join, echoing
[understanding-project-structure.md](../../frontend/frontend-architecture/reading-and-navigating-unfamiliar-codebases/understanding-project-structure.md)
— can require different, specific Node versions, and a version manager avoids the friction of a
single, global, one-size-fits-all install.

## Running Your First Script

```js
// hello.js
console.log("Hello from Node.js!");
```

```bash
node hello.js
```

Unlike browser JavaScript, which needs an HTML page and a `<script>` tag to run at all, a Node
script runs directly from the command line — `node` followed by the file path executes it
immediately, printing output straight to the terminal.

## A Minimal `package.json`

```bash
npm init -y
```

```json
{
  "name": "my-first-node-project",
  "version": "1.0.0",
  "main": "hello.js"
}
```

`npm init -y` generates a starting `package.json` with sensible defaults, skipping the interactive
prompts. This file is the project's manifest — covered in full in
[npm-and-package-management.md](npm-and-package-management.md) — and is the very next thing worth
understanding once Node itself runs.

## Common Mistakes

- Installing the "Current" release line instead of LTS for a real project, and running into less
  stable, more frequently changing behavior than a production codebase generally wants.
- Not using a version manager, then hitting a confusing error on a project that assumes a
  different Node version than the one globally installed.
- Trying to run a `.js` file with `node` and expecting browser-only globals (`window`, `alert`) to
  work — they don't exist in this environment, as covered in
  [nodejs-runtime.md](nodejs-runtime.md).

## Next

Continue to [npm-and-package-management.md](npm-and-package-management.md) to manage a real
project's dependencies properly.
