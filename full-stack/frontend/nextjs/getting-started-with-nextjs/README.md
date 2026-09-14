# Getting Started with Next.js

## Purpose

React (the domain you just finished) is a UI library — it renders components, but has no built-in
opinion on routing, data fetching on the server, or how a production app is actually built and
deployed. **Next.js** is a framework built on React that adds all of that. This module opens the
Next.js domain: what it actually adds, creating a project, and its generated structure.

## Learning Objectives

- Explain what Next.js adds on top of plain React, and why a framework is often preferred over
  assembling these pieces manually.
- Create a new Next.js project with `create-next-app`.
- Navigate a generated project's structure, especially the `app` directory.
- Understand Next.js's core configuration file.

## Prerequisites

The full [React domain](../../react/).

## Files in This Module

| File | Covers |
|---|---|
| [what-is-nextjs.md](what-is-nextjs.md) | What Next.js adds on top of React, and why |
| [creating-a-nextjs-project.md](creating-a-nextjs-project.md) | Using `create-next-app` |
| [project-structure.md](project-structure.md) | The `app` directory and file-system routing basics |
| [nextjs-configuration.md](nextjs-configuration.md) | `next.config.js` and what it's for |

## When to Deep-Dive vs. Skim

Deep-dive [what-is-nextjs.md](what-is-nextjs.md) — understanding *why* a framework exists on top
of React (rather than just memorizing Next.js's specific APIs) makes every later module in this
domain (rendering strategies, the App Router, API routes) feel like a natural answer to a real
problem, rather than an arbitrary set of new concepts to learn.

## Quick Knowledge Check

<details>
<summary>Is Next.js a replacement for React, or built on top of it?</summary>

Built on top of it — Next.js is a framework that uses React for its actual component rendering,
adding routing, server-side capabilities, and build tooling around it. Everything covered in the
React domain (components, hooks, state) still applies directly inside a Next.js app. See
[what-is-nextjs.md](what-is-nextjs.md).

</details>

<details>
<summary>How does Next.js's App Router decide what routes exist in an application?</summary>

File-system routing — the folder structure inside the `app` directory directly determines the
application's URL routes, rather than a routes configuration file like React Router's. See
[project-structure.md](project-structure.md).

</details>

## References

- Next.js, [Installation](https://nextjs.org/docs/app/getting-started/installation)

## Continue Your Learning Path

Next: [Next.js Rendering Strategies](../rendering-strategies/) — see the
[Frontend learning path](../../README.md) for the full sequence.
