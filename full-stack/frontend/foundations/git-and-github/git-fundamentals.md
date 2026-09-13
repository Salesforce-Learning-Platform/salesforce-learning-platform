# Git Fundamentals

## What Git Actually Tracks

Git is a **distributed version control system**: it records snapshots of a project's files over
time, and every developer's local copy holds the *entire* history, not just the current state
(unlike older, centralized version control systems where history lived only on a central server).
This is why most Git operations — viewing history, creating branches, committing — work instantly
and offline; only synchronizing with others (`push`/`pull`) needs a network connection.

## The Three Areas

Understanding Git's day-to-day commands requires knowing the three places a change can sit:

```text
Working Directory  ──git add──▶  Staging Area  ──git commit──▶  Repository (history)
  (your edited files)              (what will go               (permanent, committed
                                     into the next commit)        snapshots)
```

- **Working directory**: your actual files, as you're editing them.
- **Staging area** (the "index"): a preparation zone — `git add <file>` moves a specific change
  here, letting you build up exactly what should go into the next commit, even if you have other,
  unrelated changes sitting in your working directory that you're not ready to commit yet.
- **Repository**: the permanent, immutable history of committed snapshots.

## Commits

A **commit** is a saved snapshot of the staged changes, along with a message describing them, an
author, and a timestamp. Each commit points to its parent commit(s), which is what forms the
project's history as a chain (or, with branching, a graph) rather than a flat list.

```bash
git add file.js          # stage a specific change
git commit -m "Fix off-by-one error in pagination"
```

A good commit message explains *why* a change was made, not just what changed (the diff already
shows what changed) — this is the single habit that makes a project's history actually useful
months later.

## Checking State

| Command | Shows |
|---|---|
| `git status` | Which files are staged, modified, or untracked |
| `git diff` | Exact line-by-line changes not yet staged |
| `git diff --staged` | Exact line-by-line changes that are staged |
| `git log` | Commit history |

Running `git status` before *and after* staging is a habit worth building early — it's the
fastest way to catch an accidental unrelated change from being swept into a commit.

## `.gitignore`

A `.gitignore` file lists patterns for files Git should never track — build output, dependency
folders (`node_modules/`), environment files containing secrets, editor-specific settings. This
keeps the repository focused on source code and prevents large, regenerable, or sensitive files
from ever being committed.

## Common Mistakes

- Committing everything with `git add .` without reviewing what's actually being staged first —
  easy to accidentally include debug code, secrets, or unrelated files.
- Writing commit messages like "fix" or "update" that carry no information for future readers of
  the history (including your future self).
- Committing generated or dependency files that belong in `.gitignore` instead.

## Next

Continue to [branching-and-merging.md](branching-and-merging.md) to see how Git supports multiple
parallel lines of work.
