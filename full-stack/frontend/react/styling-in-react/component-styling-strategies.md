# Component Styling Strategies

## The Same `ProductCard`, Three Ways

| Approach | What it looks like |
|---|---|
| CSS Modules | `<div className={styles.card}>` — separate `.module.css` file |
| CSS-in-JS | `<Card>` — a `styled.div` component, styles as a template literal |
| Tailwind | `<div className="border rounded-lg p-4">` — utility classes directly in JSX |

All three fully solve the original problem from [css-modules.md](css-modules.md) — global CSS
class name collisions — through genuinely different mechanisms.

## A Practical Decision Framework

| Question | Favors |
|---|---|
| Does the team already know plain CSS well, with no interest in a new syntax? | CSS Modules |
| Does styling need to vary heavily and directly based on props/state? | CSS-in-JS |
| Is rapid prototyping and visual consistency across a large team the priority? | Tailwind |
| Does the project already use one of these? | Whichever it already uses — consistency within a codebase usually matters more than any single approach's specific merits |

## Consistency Within a Project Matters More Than the Specific Choice

All three approaches are used successfully in real, large production applications — there is no
single objectively "correct" choice. What matters far more in practice: a codebase mixing all
three approaches inconsistently is measurably harder to work in than a codebase that has committed
to just one, even if that one isn't every individual developer's personal favorite. This mirrors
the "consistency over cleverness" theme from
[naming-conventions](../components-jsx-and-props/component-reusability.md) — predictability across
a codebase is itself a real value, independent of which specific tool is used.

## Design Tokens Apply Regardless of Approach

Whichever styling approach a project uses, the design-token discipline from
[design-systems-and-design-tokens.md](../../css/css-core-fundamentals/design-systems-and-design-tokens.md)
still applies — CSS Modules and CSS-in-JS can both reference shared CSS custom properties for
colors/spacing, and Tailwind's own configuration can be customized to match a project's specific
design tokens rather than using its defaults unmodified. The styling *mechanism* differs; the
underlying discipline of centralizing design decisions does not.

## Common Mistakes

- Introducing a new styling approach into an existing, established codebase without a strong,
  deliberate reason — the resulting inconsistency usually costs more than any specific approach's
  individual benefits are worth.
- Choosing a styling approach based purely on personal preference or unfamiliarity with the
  alternatives, rather than the team's actual skills and the project's actual needs.
- Ignoring design tokens regardless of styling approach, leading to inconsistent spacing, colors,
  and typography even within one single approach.

## Module Summary

Across this module, the same `ProductCard` component was styled three ways: CSS Modules provide
plain CSS syntax with guaranteed local scoping via a build step (see
[css-modules.md](css-modules.md)); CSS-in-JS (styled-components) defines styles as JavaScript,
directly unlocking prop-driven dynamic styling (see [css-in-js.md](css-in-js.md)); Tailwind applies
small utility classes directly in JSX with zero runtime cost (see
[tailwind-with-react.md](tailwind-with-react.md)); and choosing between them is a genuine tradeoff
decision best made once per project and then followed consistently, rather than mixed arbitrarily.
