# Working with Remotes and GitHub

## What a Remote Is

Everything in [git-fundamentals.md](git-fundamentals.md) and
[branching-and-merging.md](branching-and-merging.md) happens entirely on your own machine. A
**remote** is a reference to a copy of the repository hosted somewhere else — most commonly on
**GitHub**, a platform that hosts Git repositories and adds collaboration tooling (pull requests,
issues, project boards) on top of plain Git. `origin` is the conventional name for a project's
primary remote.

## The Core Remote Commands

| Command | Does |
|---|---|
| `git clone <url>` | Downloads a full copy of a remote repository, including its history, to your machine |
| `git fetch` | Downloads new commits from the remote, without changing your current branch |
| `git pull` | Fetches, then merges the remote's changes into your current branch (a combination of `fetch` + `merge`) |
| `git push` | Uploads your local commits to the remote |

```text
Your local repository                     Remote (GitHub)
        │── git push ────────────────────────▶ │
        │◀──────────────────── git pull ────── │
```

## Fetch vs. Pull — A Common Point of Confusion

`git fetch` updates your knowledge of what's on the remote (new branches, new commits) without
touching your current working files at all — it's always safe to run. `git pull` goes further: it
immediately merges those remote changes into your current branch, which can trigger a merge
conflict if you have local, unpushed changes that overlap. When in doubt about what a pull will
do, fetching first and reviewing (`git log origin/main`) before merging is the safer sequence.

## What GitHub Adds Beyond Git

Git itself has no concept of issues, pull requests, or project boards — those are GitHub-specific
features built around a plain Git repository:

- **Issues** track a piece of work or a reported problem.
- **Pull requests** propose merging one branch into another, with a place for discussion and
  review before it happens (see
  [the-pull-request-workflow.md](the-pull-request-workflow.md)).
- **Project boards** track the status of issues and pull requests across a Kanban-style workflow.

Other Git-hosting platforms (GitLab, Bitbucket) provide similar features under different names —
none of it is part of Git itself, which only defines the underlying version-control operations.

## Common Mistakes

- Assuming `git pull` is always safe to run without checking for local uncommitted work first —
  an unexpected merge can be triggered mid-task.
- Confusing "pushed to GitHub" with "merged into the main branch." Pushing a feature branch makes
  it visible on the remote; it doesn't affect `main` until a merge (typically via a reviewed pull
  request) actually happens.
- Force-pushing (`git push --force`) to a shared branch without understanding it can overwrite and
  discard commits a teammate already pushed.

## Next

Continue to
[the-pull-request-workflow.md](the-pull-request-workflow.md) to see how teams actually use
branches and remotes together to collaborate safely.
