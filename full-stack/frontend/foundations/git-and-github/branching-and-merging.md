# Branching and Merging

## What a Branch Actually Is

A **branch** is simply a movable pointer to a commit. Creating a branch doesn't copy any files —
it creates a new named pointer, letting you make a new sequence of commits without touching the
commit history other branches point to. This is what makes branching in Git cheap and instant,
regardless of project size.

```text
main:     A ─── B ─── C
                 \
feature:          D ─── E     (branched from B, diverging independently)
```

## The Typical Workflow

```bash
git checkout -b feature/add-search   # create and switch to a new branch
# ... make commits on this branch ...
git checkout main                    # switch back
git merge feature/add-search         # bring those commits into main
```

Working on a dedicated branch per feature or fix keeps `main` (or another shared branch) always in
a known-good state, and lets multiple people work on unrelated changes simultaneously without
interfering with each other's in-progress work.

## Merging

**Merging** combines the changes from one branch into another. Git attempts this automatically by
comparing the changed lines; when two branches modified *different* parts of a file, or the same
part in compatible ways, the merge completes cleanly with no input needed.

## Merge Conflicts

A **conflict** occurs when two branches changed the *same lines* of the *same file* in
incompatible ways — Git cannot decide which version is correct, so it pauses the merge and asks
you to resolve it manually. Git marks the conflicting section directly in the file:

```text
<<<<<<< HEAD
const greeting = "Hello there";
=======
const greeting = "Hi!";
>>>>>>> feature/add-search
```

Resolving a conflict means editing the file to the version you actually want (which might be one
side, the other, a combination, or something new entirely), removing the conflict markers, then
staging and committing the resolution:

```bash
git add file.js
git commit
```

A conflict is not an error or a sign something went wrong — it's Git correctly refusing to guess
when two changes genuinely disagree, and handing the decision back to a human.

## Common Mistakes

- Panicking at a merge conflict rather than reading it — the markers precisely show both competing
  versions; the resolution is a normal editing task, not a special recovery procedure.
- Resolving a conflict by keeping "your" side without actually reading what the other side changed
  — silently discarding a teammate's work.
- Letting a long-lived branch drift far from `main` before merging, which makes eventual conflicts
  larger and harder to resolve than if the branch had merged (or at least synced) more frequently.

## Next

Continue to
[working-with-remotes-and-github.md](working-with-remotes-and-github.md) to see how this local
history is shared with other people.
