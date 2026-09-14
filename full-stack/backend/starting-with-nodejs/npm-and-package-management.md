# npm and Package Management

## What npm Actually Is

**npm** is three connected things: the world's largest JavaScript package **registry** (a public
database of published packages), the **CLI** you run from the terminal to install and manage them,
and the website (npmjs.com) for discovering packages and viewing their documentation. It ships
bundled with every Node.js installation.

## Installing a Package

```bash
npm install express
npm install --save-dev nodemon
```

```json
{
  "dependencies": {
    "express": "^4.19.2"
  },
  "devDependencies": {
    "nodemon": "^3.1.0"
  }
}
```

`dependencies` are packages the running application actually needs (a web framework like Express,
covered in the upcoming [Express.js Fundamentals module](../../backend/expressjs-fundamentals/)).
`devDependencies` are tools only needed *while developing* — a tool that auto-restarts the server
on file changes, a test runner, a linter — that have no reason to be installed wherever the
finished application actually runs in production.

## `package.json` — The Project's Manifest

```json
{
  "name": "shop-api",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": { "express": "^4.19.2" },
  "devDependencies": { "nodemon": "^3.1.0" }
}
```

`package.json` is the single source of truth for a Node project: its name, version, the exact
dependencies it needs, and `scripts` — named shortcuts (`npm run dev`, or `npm start` for the
special `start` script) so every developer on a team runs the project the same documented way,
instead of everyone remembering their own slightly different command.

## `node_modules` and `package-lock.json`

```bash
npm install
```

Running `npm install` with no package name reads `package.json`'s dependency list and downloads
everything into a `node_modules` folder — never committed to version control, since it can always
be regenerated from `package.json`. `package-lock.json`, by contrast, **is** committed: it records
the *exact* resolved version of every dependency (and every dependency's own dependencies),
guaranteeing that everyone on a team, and the production server, installs the identical dependency
tree — not just something matching the same loose version range.

## Semantic Versioning (`^4.19.2`)

| Prefix | Meaning |
|---|---|
| `^4.19.2` | Allows updates that don't change the first non-zero number (here, stays on `4.x.x`) |
| `~4.19.2` | Allows only patch updates (stays on `4.19.x`) |
| `4.19.2` (exact) | Only that exact version, ever |

npm packages follow **Semantic Versioning** — `MAJOR.MINOR.PATCH` — where a major version bump
signals a breaking change, a minor version adds backward-compatible functionality, and a patch is a
backward-compatible bug fix. The `^` and `~` prefixes in `package.json` control how much automatic
flexibility a project allows when `npm install` resolves a compatible version.

## Common Mistakes

- Committing `node_modules` to version control — it's large, fully regenerable from
  `package.json`/`package-lock.json`, and bloats every clone of the repository for no benefit.
- Deleting or ignoring `package-lock.json` — without it, two different installs of the same
  `package.json` can silently resolve to different dependency versions, undermining the
  reproducibility it exists to guarantee.
- Installing a tool only needed during development as a regular `dependency` instead of a
  `devDependency`, unnecessarily bloating what actually ships to production.

## Module Summary

Across this module: Node.js is a **JavaScript runtime** built on V8, running the same language you
already know outside any browser (see [what-is-nodejs.md](what-is-nodejs.md)); its **event-driven,
non-blocking I/O model**, powered by libuv alongside V8, lets a single process handle many
concurrent, slow operations efficiently, extending the same async patterns already familiar from
browser JavaScript (see [how-nodejs-works.md](how-nodejs-works.md)); Node's **runtime globals** —
`process`, `__dirname`, `global` — replace the browser's `window`/`document` with tools suited to a
server environment (see [nodejs-runtime.md](nodejs-runtime.md)); setting up a real environment
means installing the LTS release, ideally through a version manager (see
[setting-up-nodejs.md](setting-up-nodejs.md)); and **npm**, driven by `package.json` and locked by
`package-lock.json`, manages a project's dependencies reproducibly across every machine that runs
it.
