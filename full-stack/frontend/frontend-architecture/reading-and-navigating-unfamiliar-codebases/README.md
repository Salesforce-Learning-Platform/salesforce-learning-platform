# Reading and Navigating Unfamiliar Codebases

## Purpose

Every module so far has taught you to *build*, starting from an empty file. In a real job, the far
more common task is joining a project someone else already built — a codebase with its own
structure, conventions, and history — and needing to understand it fast enough to make a safe
change. This module is the deliberate skill of reading code you didn't write, applicable to any
codebase built with anything covered in the [Frontend domain](../../README.md) so far.

## Learning Objectives

- Read an unfamiliar project's structure to form a mental map before touching any code.
- Identify a codebase's entry points — where execution, and where the UI, actually begins.
- Trace how data flows through a feature, from its source to where it's rendered.
- Debug existing code you didn't write, using browser DevTools rather than guesswork.

## Prerequisites

- The [React domain](../../react/) and [Next.js domain](../../nextjs/) — this module's examples
  assume familiarity with the project shapes those domains established.

## Files in This Module

| File | Covers |
|---|---|
| [understanding-project-structure.md](understanding-project-structure.md) | Forming a mental map of an unfamiliar project's folders and files before changing anything |
| [identifying-entry-points.md](identifying-entry-points.md) | Finding where a codebase actually starts — the app's root, and a feature's root |
| [tracing-data-flow.md](tracing-data-flow.md) | Following a piece of data from where it originates to where it's rendered |
| [debugging-existing-code.md](debugging-existing-code.md) | Using breakpoints, source maps, and DevTools to understand code you didn't write |

## When to Deep-Dive vs. Skim

Deep-dive [tracing-data-flow.md](tracing-data-flow.md) — understanding project structure and entry
points gets you *oriented*; tracing data flow is the skill that actually lets you answer the
question you're facing on your first real task: "where does this value on the screen actually come
from, and what do I need to change to fix it?"

## Quick Knowledge Check

<details>
<summary>You've just joined a project. Should your first move be reading the README, or opening a random component file and starting to trace logic?</summary>

Neither extreme is ideal, but starting from the project's structure (README, folder layout, entry
point) before diving into any one file's logic is the right order — you want a mental map of
*where things live* before investing time understanding *how one specific piece works in detail*.
See [understanding-project-structure.md](understanding-project-structure.md).

</details>

<details>
<summary>You want to know why a value on the screen is wrong. Is reading the component that renders it the best place to start?</summary>

Not necessarily — the bug may be in the component that renders it, but it could just as easily be
upstream, in wherever that value's data originally came from. Tracing the data flow backward from
the rendered output to its source is usually more reliable than guessing which single file to
read first. See [tracing-data-flow.md](tracing-data-flow.md).

</details>

## References

- Chrome for Developers, [Breakpoints in DevTools](https://developer.chrome.com/docs/devtools/javascript/breakpoints)

## Continue Your Learning Path

See the [Frontend learning path](../../README.md) for the remaining modules and what comes next.
