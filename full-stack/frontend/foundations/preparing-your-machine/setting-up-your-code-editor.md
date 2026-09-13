# Setting Up Your Code Editor

## Why Editor Configuration Matters

A well-configured editor catches mistakes before you run your code, formats it consistently
without manual effort, and surfaces documentation inline — compounding into a meaningfully faster
feedback loop over the course of a project. This file focuses on the *categories* of tooling worth
setting up, since specific products change over time; Visual Studio Code (VS Code) is used as the
concrete example because it's the most widely used editor in frontend development today.

## The Categories of Tooling Worth Configuring

| Category | What it does | Example |
|---|---|---|
| **Syntax highlighting & IntelliSense** | Colors code by meaning, and suggests completions based on actual type/API information | Built into VS Code for JavaScript/TypeScript |
| **Linting** | Flags code that's likely a mistake or violates agreed conventions, before you run it | ESLint |
| **Formatting** | Automatically rewrites code into a consistent style, removing style debates entirely | Prettier |
| **Version control integration** | Shows file changes, lets you stage/commit without leaving the editor | Built-in Git support |
| **Debugging** | Lets you pause execution, inspect variables, and step through code | Built-in debugger, browser DevTools integration |

## Linting vs. Formatting — Not the Same Thing

These are frequently bundled together but solve different problems:

- **Formatting** is purely about *appearance* — indentation, spacing, quote style. It has no
  opinion on whether code is correct.
- **Linting** is about *correctness and convention* — flagging an unused variable, a missing
  dependency in a React hook, or a pattern the team has agreed to avoid. A linter can flag real
  bugs; a formatter never does.

Most projects run both: a formatter to end style arguments entirely, and a linter to catch actual
mistakes.

## Format-on-Save

Configuring the editor to automatically apply formatting every time a file is saved removes an
entire category of manual effort and code-review nitpicking ("please fix the indentation here").
This is standard practice on essentially every professional frontend team.

## Common Mistakes

- Running a linter and formatter with conflicting rules, so each one keeps undoing the other's
  changes — most setups need a small compatibility configuration (e.g., disabling a linter's
  purely stylistic rules when a separate formatter already handles them).
- Committing editor-specific configuration that only works on one person's machine, rather than
  project-level configuration (e.g., an `.eslintrc` or `.prettierrc` file in the repository) that
  works the same for every contributor.
- Ignoring linter warnings as noise rather than treating them as an early bug-detection signal.

## Next

Continue to [browser-devtools-essentials.md](browser-devtools-essentials.md) — once code runs in
a browser, DevTools become the primary tool for understanding what it's actually doing.
