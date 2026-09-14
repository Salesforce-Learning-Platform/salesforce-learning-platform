# Dependency Management

## Beyond `npm install` — a Deliberate Practice at Scale

[npm-and-package-management.md](../starting-with-nodejs/npm-and-package-management.md) covered the
mechanics: `dependencies` vs. `devDependencies`, `package-lock.json`, semantic versioning. As a
project and its team grow, dependency management becomes a deliberate, ongoing practice, not a
one-time setup step.

## Every Dependency Is a Liability, Not Just a Convenience

```bash
npm install left-pad  # a real, tiny package that once broke a huge portion
                        # of the JavaScript ecosystem when it was unpublished
```

Every dependency added to a project is code the team didn't write, doesn't fully control, and is
now implicitly trusting — for correctness, for security, and for continuing to exist and be
maintained. This isn't an argument against using dependencies (reimplementing bcrypt or Express
from scratch would be far worse) — it's a reason to add each one **deliberately**, weighing what it
actually provides against the real risk and maintenance burden it introduces.

## Auditing for Known Vulnerabilities

```bash
npm audit
npm audit fix
```

`npm audit` checks a project's installed dependencies against a database of known security
vulnerabilities, and `npm audit fix` attempts to automatically upgrade affected packages to a
patched version where possible. Running this regularly — not just once at project setup — is a
basic, essential part of keeping a real production backend secure over its actual lifetime.

## Keeping Dependencies Updated, Deliberately

```
Falling too far behind on updates:
- Security patches pile up, unapplied
- A future "catch-up" upgrade becomes a large, risky, all-at-once change

Updating too aggressively, with no review:
- A breaking change (a major version bump) can silently break the
  application in production
```

Neither extreme is healthy. A deliberate cadence — reviewing and applying updates regularly, in
small increments, rather than either ignoring them indefinitely or blindly auto-updating
everything — keeps a dependency tree both secure and stable, echoing
[npm-and-package-management.md](../starting-with-nodejs/npm-and-package-management.md)'s semantic
versioning discipline: a patch or minor update is usually safe to apply readily; a major version
bump deserves deliberate review.

## Minimizing Dependency Footprint

```js
// A small utility easily written in a few lines of plain JavaScript
// doesn't need an entire external package as a dependency
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
```

Not every small piece of functionality needs a dedicated npm package — each added dependency
increases the application's attack surface (per the `npm audit` point above), its `node_modules`
size, and the number of external maintainers the project now implicitly relies on. A genuinely
trivial utility is often better written directly than imported.

## Common Mistakes

- Never running `npm audit` (or an equivalent tool) at all, letting known, patchable
  vulnerabilities accumulate silently in production dependencies.
- Adding a large, feature-rich dependency for one small piece of functionality it happens to
  provide, when a few lines of plain code would have sufficed.
- Blindly running a bulk "update everything" command without reviewing what actually changed,
  risking an unreviewed breaking change reaching production.

## Next

Continue to [error-handling-architecture.md](error-handling-architecture.md) to design a
consistent, centralized error-handling strategy across the entire application.
