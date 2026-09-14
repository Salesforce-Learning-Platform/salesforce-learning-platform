# Consistency at Scale

## Why This Is the Hard Part

[component-libraries.md](component-libraries.md) and
[design-tokens-in-practice.md](design-tokens-in-practice.md) cover the technical mechanics of a
design system. Neither one, alone, guarantees the system actually stays consistent once dozens of
teams depend on it, the component library itself needs to change, and the product keeps evolving
underneath everyone. That ongoing consistency is a *process* problem as much as a technical one.

## Semantic Versioning for a Component Library

```
1.4.2 → 1.4.3   Patch: a bug fix, no visible API or behavior change for consumers
1.4.2 → 1.5.0   Minor: a new component or a new, backward-compatible prop added
1.4.2 → 2.0.0   Major: a breaking change — a prop removed, renamed, or its meaning changed
```

A component library is a dependency, exactly like any npm package, and should follow the same
Semantic Versioning discipline consuming teams already rely on for every other dependency: a
**major** version bump for any breaking change, so teams can safely auto-update on patch and minor
releases and only need to deliberately review major ones.

## Deprecation, Not Deletion

```jsx
/**
 * @deprecated Use `<Button variant="primary">` instead. Will be removed in v3.0.0.
 */
export function PrimaryButton(props) {
  return <Button variant="primary" {...props} />;
}
```

Removing an old component or prop the instant a better one exists breaks every consuming team still
using it, often without warning. The standard pattern is **deprecation**: keep the old API working
(often by having it delegate to the new implementation internally), mark it clearly as deprecated
with guidance on what to use instead, and remove it only in a later major version — giving every
consuming team a real window to migrate on their own schedule.

## Governance: Who Can Change the System

A design system used by many teams needs an explicit answer to "who approves a change to a shared
button every other team depends on" — commonly a dedicated design-system team, or a rotating group
of representatives from consuming teams, reviewing proposed changes before they ship. Without this,
either the system stagnates (nobody feels empowered to improve it) or it fragments (multiple teams
change it inconsistently, recreating the exact problem
[component-libraries.md](component-libraries.md) exists to prevent).

## Adoption Is Not Automatic

Publishing a well-built component library doesn't guarantee teams actually use it instead of
reaching for a one-off custom component under deadline pressure. Real design systems sustain
adoption through:

- **Visibility**: a searchable, well-documented Storybook (from
  [component-libraries.md](component-libraries.md)) that's genuinely faster to use than building a
  component from scratch.
- **Linting/tooling**: automated checks that flag raw hex colors or one-off buttons in application
  code, nudging developers back toward the shared tokens and components.
- **Feedback loops**: an easy path for consuming teams to request a missing component or report an
  inconsistency, so the system evolves to fit real needs rather than staying frozen.

## Common Mistakes

- Shipping a breaking change as a minor or patch version, silently breaking every team that trusted
  semantic versioning to update safely.
- Deleting a deprecated component immediately instead of giving consuming teams a real migration
  window.
- Assuming a design system is "done" once version 1.0 ships — in practice it needs the same
  ongoing governance and maintenance investment as any other piece of shared infrastructure.
- Building a design system with no feedback channel, so teams quietly route around it with one-off
  components instead of requesting what they actually need.

## Module Summary

Across this module: a **component library** is a shared, versioned set of implemented components
built once for many consuming teams, built and documented in isolation with tools like Storybook
(see [component-libraries.md](component-libraries.md)); **design tokens in practice**, at
real-organization scale, means a platform-neutral source of truth (like the W3C DTCG JSON format)
transformed into each platform's native output, rather than hand-maintained, parallel copies per
platform (see [design-tokens-in-practice.md](design-tokens-in-practice.md)); and genuine
**consistency at scale** depends as much on process — semantic versioning, deliberate deprecation,
clear governance, and real adoption incentives — as it does on the components and tokens
themselves.
