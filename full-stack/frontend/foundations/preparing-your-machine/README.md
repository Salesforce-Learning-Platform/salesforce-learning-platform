# Preparing Your Machine

## Purpose

Before writing frontend code, you need a working local development environment: a way to run
commands, a JavaScript runtime and package manager, an editor configured for productive feedback,
and familiarity with the browser tools you'll use to inspect what you build. This module sets that
baseline so every later module can assume it.

## Learning Objectives

- Perform basic navigation and file operations from the command line.
- Explain what Node.js and a package manager (npm) actually do, and install them correctly.
- Configure a code editor for a productive frontend workflow.
- Locate and use the core panels of browser DevTools (Elements, Console, Network).

## Files in This Module

| File | Covers |
|---|---|
| [terminal-and-command-line-basics.md](terminal-and-command-line-basics.md) | Navigating the filesystem and running commands from a shell |
| [installing-a-package-manager-and-node.md](installing-a-package-manager-and-node.md) | Node.js, npm, and what "installing a dependency" actually does |
| [setting-up-your-code-editor.md](setting-up-your-code-editor.md) | Configuring an editor for frontend development |
| [browser-devtools-essentials.md](browser-devtools-essentials.md) | The DevTools panels you'll use constantly, and what each is for |

## When to Deep-Dive vs. Skim

If you're already an experienced developer switching to frontend work, skim this whole module as a
setup checklist rather than reading it linearly — but don't skip
[browser-devtools-essentials.md](browser-devtools-essentials.md) even if you know a different
editor and terminal well; the Network panel specifically is used throughout every later module in
this platform.

## Quick Knowledge Check

<details>
<summary>Why shouldn't node_modules/ be committed to version control?</summary>

It's large and fully regenerable from package.json and the lock file — committing it bloats the
repository and defeats the purpose of dependency management. See
[installing-a-package-manager-and-node.md](installing-a-package-manager-and-node.md).

</details>

<details>
<summary>What's the difference between a linter and a formatter?</summary>

A formatter only changes appearance (spacing, indentation) and has no opinion on correctness. A
linter flags actual likely mistakes or convention violations — it can catch real bugs, a formatter
never does. See [setting-up-your-code-editor.md](setting-up-your-code-editor.md).

</details>

## References

- [Node.js downloads](https://nodejs.org/en/download) — official installers and version manager guidance
- [Visual Studio Code documentation](https://code.visualstudio.com/docs)
- [ESLint](https://eslint.org/) — the standard JavaScript/TypeScript linter
- [Prettier](https://prettier.io/) — the standard code formatter referenced in this module

## Continue Your Learning Path

Next in the [Foundations sequence](../README.md): [Git and GitHub](../git-and-github/).
