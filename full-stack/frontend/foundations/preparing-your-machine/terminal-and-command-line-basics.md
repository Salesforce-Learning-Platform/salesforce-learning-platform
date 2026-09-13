# Terminal and Command Line Basics

## Why the Terminal Matters

Graphical file browsers hide most of what a development toolchain actually does. Build tools,
package managers, Git, and deployment scripts are all designed to be run from a **shell** (a
command-line interpreter — `bash`/`zsh` on macOS/Linux, PowerShell or WSL on Windows). Comfort
here isn't optional trivia; nearly every setup guide in software engineering assumes it.

## Core Navigation Commands

| Command | Does |
|---|---|
| `pwd` | Print the current directory ("print working directory") |
| `ls` (`dir` on Windows) | List files in the current directory |
| `cd <path>` | Change directory |
| `cd ..` | Move up one directory |
| `mkdir <name>` | Create a new directory |
| `touch <file>` (macOS/Linux) | Create an empty file |

## Paths: Absolute vs. Relative

An **absolute path** starts from the filesystem root (`/Users/you/projects/app` on macOS/Linux,
`C:\Users\you\projects\app` on Windows) and always means the same location regardless of where
you currently are. A **relative path** (`./src/index.js`, `../config`) is interpreted relative to
your current directory — `.` means "here," `..` means "one level up." Scripts and configuration
files frequently mix both, and misreading which kind a path is is a common source of "file not
found" confusion.

## Running Programs and Passing Arguments

A typical command has the shape `command [options] [arguments]` — for example, `npm install
react` runs the `npm` program with the argument `install` (a subcommand) and `react` (what to
install). Options are usually prefixed with `-` (short form, e.g. `-v`) or `--` (long form, e.g.
`--version`).

## Common Mistakes

- Running a project-specific command (like `npm run dev`) from the wrong directory — most tools
  assume you're inside the project root, and will fail confusingly (or run against the wrong
  project) otherwise.
- Confusing a relative path for an absolute one when copying a command from documentation written
  for a different starting directory.
- Being unable to tell whether a failed command is a shell problem (command not found — the
  program isn't installed or isn't on your `PATH`) versus a program-level error (the command ran,
  but reported its own failure).

## Next

Continue to
[installing-a-package-manager-and-node.md](installing-a-package-manager-and-node.md) to set up
the JavaScript tooling you'll run from this shell.
