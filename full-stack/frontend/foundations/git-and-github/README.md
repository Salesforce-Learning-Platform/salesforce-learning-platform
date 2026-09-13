# Git and GitHub

## Purpose

Version control is how software teams change code safely, in parallel, with a full history of
who changed what and why. **Git** is the version control system; **GitHub** is a hosting platform
built around it that adds collaboration features (pull requests, issues, code review). This module
covers both, since almost no professional Git usage happens without a hosting platform alongside
it.

## Learning Objectives

- Explain what a Git repository, commit, and branch actually are.
- Perform the core local Git workflow: stage, commit, branch, merge.
- Explain what a "remote" is and how `push`/`pull`/`fetch` relate to it.
- Explain the pull request workflow and why code review exists.
- Recognize and resolve a merge conflict.

## Files in This Module

| File | Covers |
|---|---|
| [git-fundamentals.md](git-fundamentals.md) | Repositories, the staging area, commits, and the mental model behind them |
| [branching-and-merging.md](branching-and-merging.md) | Branches, merging, and merge conflicts |
| [working-with-remotes-and-github.md](working-with-remotes-and-github.md) | Remotes, push/pull/fetch, and what GitHub adds on top of Git |
| [the-pull-request-workflow.md](the-pull-request-workflow.md) | How teams actually collaborate: PRs, code review, and merge strategies |

## Salesforce Relevance

Modern Salesforce development (using Salesforce CLI and source-tracked orgs) is built entirely on
this same Git workflow — metadata changes are tracked as files in a repository, developed on
branches, and merged via pull requests exactly as described in this module, rather than being
edited directly in a single shared production org.
