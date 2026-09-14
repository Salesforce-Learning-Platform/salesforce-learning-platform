# Environment Variables

## Reading Configuration From `process.env`

```js
const port = process.env.PORT;
const databaseUrl = process.env.DATABASE_URL;

console.log(typeof port); // "string" — always, even if the value looks numeric
```

`process.env` (introduced in [nodejs-runtime.md](../starting-with-nodejs/nodejs-runtime.md)) is how
a running Node process reads its **environment variables** — configuration values supplied from
outside the code itself, by whatever started the process. Every value here is always a string,
even one that looks like a number or a boolean — a common early source of bugs when comparing
`process.env.DEBUG === true` (always false; it's the string `"true"`, not the boolean `true`).

## Why Configuration Lives Outside the Code

```js
// AVOID — hardcoded directly into source code
const databaseUrl = "postgres://admin:supersecret@prod-db.example.com/shop";

// PREFER — read from the environment
const databaseUrl = process.env.DATABASE_URL;
```

A database password, an API key, or a service URL should never be typed directly into source code
committed to git — anyone with repository access (or anyone who ever finds an old commit) would see
it, and the exact same code needs *different* values in development versus production anyway (a
local test database vs. the real one). Reading from `process.env` cleanly separates the code
(same everywhere) from its configuration (different per environment).

## Loading a `.env` File in Development

```
# .env
PORT=3000
DATABASE_URL=postgres://localhost:5432/shop_dev
```

```bash
node --env-file=.env server.js
```

```js
// Or programmatically, inside the code itself:
import { loadEnvFile } from "node:process";
loadEnvFile("./.env");
```

Manually setting environment variables on every terminal command is impractical during
development. A `.env` file holds them as simple `KEY=value` pairs, and Node's built-in
`--env-file` flag (or the `process.loadEnvFile()` function) loads them into `process.env`
automatically at startup — no separate third-party package required for this basic case.

## `.env` Must Never Be Committed

```
# .gitignore
.env
```

```
# .env.example — THIS one IS committed, as a template
PORT=3000
DATABASE_URL=postgres://localhost:5432/shop_dev
```

A real project's `.env` file typically holds genuine secrets, so it's added to `.gitignore` and
never committed. Instead, teams commit a `.env.example` — the same keys, with placeholder or empty
values — so anyone cloning the project knows exactly which variables to set, without ever exposing
the real ones.

## Precedence: Shell Variables Win Over `.env`

```bash
# The shell's own PORT value takes priority over whatever .env sets
PORT=5000 node --env-file=.env server.js
```

Variables already set directly in the shell environment take precedence over the same key loaded
from a `.env` file — deliberate, since it lets a deployment platform (which typically sets real
environment variables directly, not via a committed file) safely override local defaults without
needing to touch the `.env` file itself at all.

## Common Mistakes

- Committing a real `.env` file (with actual secrets) to version control — even a private
  repository's full history is a real exposure risk if access is ever compromised or the repo is
  later made public.
- Comparing a `process.env` value directly against a non-string (`process.env.DEBUG === true`)
  and being surprised it's always false, since the actual value is the string `"true"`.
- Forgetting to update `.env.example` when a new required variable is added, leaving teammates (or
  a future you) without a clear signal of what configuration a fresh clone actually needs.

## Next

Continue to [process-and-runtime.md](process-and-runtime.md) to control a Node process's actual
lifecycle — how it starts, exits, and shuts down cleanly.
