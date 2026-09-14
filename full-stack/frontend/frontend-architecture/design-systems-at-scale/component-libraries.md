# Component Libraries

## What a Component Library Actually Is

A **component library** is a shared, versioned package of implemented UI components — buttons,
inputs, modals, cards — built once by a dedicated team (or a rotating set of contributors) and
consumed by every feature team building the product, instead of each team implementing its own
version of a button. This is
[reusable-component-design.md](../../react/component-architecture-and-composition/reusable-component-design.md)'s
component-design discipline, applied at the scale of an entire organization rather than a single
app.

## Why Not Let Every Team Build Its Own

```jsx
// Team A's button
<button className="btn-primary">Save</button>

// Team B's button — slightly different padding, different hover color,
// built independently without knowing Team A's already exists
<button className="primary-btn">Submit</button>
```

Without a shared library, the same component gets reinvented slightly differently by every team —
each with its own small inconsistencies in spacing, color, focus behavior, and accessibility
handling. The cost isn't just visual inconsistency: every team also re-solves the same
accessibility and edge-case work (see
[inclusive-design-principles.md](../../html/html-accessibility/inclusive-design-principles.md))
independently, multiplying both the effort and the chance of getting it wrong somewhere.

## Building and Documenting Components in Isolation: Storybook

```jsx
// Button.stories.jsx
import { Button } from "./Button";

export default { component: Button };

export const Primary = { args: { variant: "primary", children: "Save" } };
export const Danger = { args: { variant: "danger", children: "Delete Account" } };
export const Disabled = { args: { variant: "primary", disabled: true, children: "Save" } };
```

**Storybook** is a development tool for building and viewing components in an isolated environment
— separate from the full application, its routing, and its business logic. A **story** captures one
specific state or variation of a component (a primary button, a disabled button, a danger-styled
button) with a declarative set of props. This serves two purposes at once:

- **Development**: a component can be built and visually verified without running the entire app
  around it.
- **Documentation**: Storybook becomes a living, browsable catalog of every component and every
  state it supports — the single source of truth designers, developers, and QA can all reference,
  showing what the UI actually does in production, not a design mockup of what it's supposed to do.

## A Component Library's Real Surface Area

A production component library typically includes, beyond just the components themselves:

- **Prop-level API documentation** — exactly which props each component accepts and what they do.
- **Accessibility built in by default** — correct ARIA attributes, keyboard behavior, and focus
  management shipped inside the component itself, so consuming teams get it for free rather than
  having to reimplement it.
- **Automated visual and interaction tests** — often built directly on top of Storybook's stories,
  since each story is already a reproducible scenario a test can run against.

## Common Mistakes

- Treating a component library as "just the JSX" — the documentation, accessibility defaults, and
  test coverage are what actually make it safe and fast for other teams to adopt.
- Letting a component library grow without any review process, so it accumulates the same
  inconsistency problem it was built to solve, just one level higher up.
- Building components for hypothetical future use cases no consuming team has actually asked for
  yet, rather than the concrete needs of real feature teams.

## Next

Continue to [design-tokens-in-practice.md](design-tokens-in-practice.md) to see how the values a
component library's components use stay consistent across an entire, often multi-platform, system.
