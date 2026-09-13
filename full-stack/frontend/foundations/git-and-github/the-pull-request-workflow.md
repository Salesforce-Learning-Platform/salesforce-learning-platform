# The Pull Request Workflow

## What a Pull Request Is

A **pull request (PR)** is a proposal to merge one branch into another, opened on a platform like
GitHub. Critically, a pull request is not the same as a commit or a merge — it's a *request for
review and discussion* before a merge happens, giving the team a checkpoint to catch problems
before they reach a shared branch.

```text
Issue (what needs to be done)
   ↓
Branch (isolated workspace for the change)
   ↓
Commits (the actual implementation)
   ↓
Push (branch made visible on the remote)
   ↓
Pull Request (proposal + discussion + review)
   ↓
Merge (PR's commits become part of the target branch)
```

## The Typical Lifecycle

1. Create a branch for the change (see
   [branching-and-merging.md](branching-and-merging.md)).
2. Make and commit the change.
3. Push the branch to the remote.
4. Open a pull request targeting the shared branch (commonly `main`), describing what changed and
   why.
5. Reviewers read the diff, leave comments, and request changes if needed.
6. The author addresses feedback with additional commits (pushed to the same branch — the PR
   updates automatically).
7. Once approved, the PR is merged.

## Why Code Review Exists

Review isn't a formality — it's a second set of eyes catching what the author, having just written
the code, may no longer be able to see objectively: a missed edge case, an unclear name, an
approach a reviewer has seen fail before. It also spreads knowledge of the codebase across the
team, so no single person is the only one who understands a given piece of code.

## Merge Strategies

| Strategy | Effect |
|---|---|
| **Merge commit** | Creates a new commit joining both histories; preserves the full branch history |
| **Squash and merge** | Combines all of a branch's commits into a single commit on the target branch — a clean, linear history at the cost of losing granular in-branch commit detail |
| **Rebase and merge** | Replays the branch's commits on top of the target branch, avoiding a merge commit while keeping individual commits |

Different teams and repositories standardize on different strategies; what matters is
consistency, and understanding that all three produce the *same final file content* — they differ
only in what the resulting history looks like.

## Common Mistakes

- Opening a pull request with no description, leaving reviewers to reverse-engineer *why* a change
  was made from the diff alone.
- Treating review comments as personal criticism rather than a normal, expected part of shipping
  quality code.
- Merging a PR with unresolved review comments or failing checks, rather than treating "review
  passed" as a genuine gate.

## Module Summary

Across this module: Git tracks snapshots through a staging-area-then-commit workflow (see
[git-fundamentals.md](git-fundamentals.md)); branches let multiple lines of work proceed in
parallel, with conflicts as an expected, resolvable part of merging (see
[branching-and-merging.md](branching-and-merging.md)); remotes and GitHub let that history be
shared and collaborated on beyond a single machine (see
[working-with-remotes-and-github.md](working-with-remotes-and-github.md)); and the pull request
workflow is how teams add a review checkpoint before any change reaches a shared branch.
