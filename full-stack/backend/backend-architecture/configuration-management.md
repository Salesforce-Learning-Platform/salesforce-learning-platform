# Configuration Management

## Building on What Environment Variables Already Cover

[environment-variables.md](../nodejs-core-concepts/environment-variables.md) already covered the
mechanics: `process.env`, `.env` files, and never committing secrets. This file is about the
**architectural discipline** around configuration at a real project's scale — how to organize it,
and the Twelve-Factor App's specific reasoning for why configuration belongs in the environment at
all.

## The Twelve-Factor App's Config Principle

The [Twelve-Factor App](https://12factor.net/config) methodology — a widely referenced set of
principles for building real, deployable web applications — defines **config** as "everything
that is likely to vary between deploys": database credentials, API keys, and any other
environment-specific value. Its central rule: **strict separation of config from code**.

## The Litmus Test: Could This Codebase Be Open-Sourced Right Now?

```js
// FAILS the test — a real secret is directly readable in the source code
const dbUrl = "postgres://admin:realpassword123@prod-db.example.com/shop";

// PASSES the test — no secret is present in the code at all
const dbUrl = process.env.DATABASE_URL;
```

The Twelve-Factor App proposes a genuinely useful practical test: **could this codebase be made
open source at any moment, without compromising any credentials?** If a secret is typed directly
into a source file, the answer is no — and that's true even for a private repository, since access
controls change, backups leak, and history persists. Every value that would fail this test belongs
in the environment, never in a file tracked by git.

## Why Environment Variables Specifically, Not Config Files

Config files (even ones excluded from git) are still an easy target for accidental leaks — copied
into a Docker image, uploaded somewhere they shouldn't be, or simply forgotten about. Environment
variables, set directly by whatever platform runs the process, don't have this same accidental-file
risk, and work identically across virtually every language and hosting platform — a genuinely
portable, language-agnostic standard.

## Avoid Named, Hardcoded "Environments"

```js
// AVOID — hardcoding a fixed, closed set of named environments
const configs = {
  development: { dbUrl: "postgres://localhost/dev" },
  production: { dbUrl: "postgres://prod-server/shop" },
};
const config = configs[process.env.NODE_ENV];
```

```js
// PREFER — each deploy independently supplies its own environment variables,
// with NO fixed, hardcoded list of "known" environments in the code at all
const dbUrl = process.env.DATABASE_URL;
```

The Twelve-Factor App specifically warns against grouping configuration into a small, fixed set of
named environments (`development`, `staging`, `production`) hardcoded into the application itself.
This pattern doesn't scale cleanly — every new deploy target (a second staging environment, a
per-developer preview environment) forces a code change just to add a new named bucket. Reading
each value independently from the environment, with no fixed list of "known" environments baked
into the code, scales to any number of deploy targets without ever touching the application's
source.

## A Config Module as a Single Source of Truth

```js
// config/index.js — one file, read once, that every other module imports from
export const config = {
  port: process.env.PORT || 3000,
  databaseUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
};
```

Rather than scattering `process.env.X` reads throughout the codebase, a single config module reads
every environment variable once, in one place — making it immediately obvious exactly what
configuration the entire application depends on, and giving every other module (including each
[repository](controllers-services-and-repositories.md)) one consistent source to import
configuration from.

## Common Mistakes

- Committing a config file (even a `.env.production`) that contains real secrets, rather than
  supplying them purely through the deployment platform's own environment variable mechanism.
- Hardcoding a fixed set of named environments into the application's own logic, forcing a code
  change every time a new deploy target is added.
- Scattering direct `process.env.X` reads throughout many files instead of centralizing them in one
  config module, making it hard to audit exactly what configuration the application actually needs.

## Next

Continue to [dependency-management.md](dependency-management.md) to manage a growing dependency
tree with the same deliberate discipline.
