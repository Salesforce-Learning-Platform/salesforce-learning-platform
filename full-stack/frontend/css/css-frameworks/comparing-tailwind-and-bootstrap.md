# Comparing Tailwind and Bootstrap

## Recap: Two Different Philosophies

[introduction-to-css-frameworks.md](introduction-to-css-frameworks.md) introduced the core
distinction: Tailwind composes a design from small utilities directly in markup;
[Bootstrap](bootstrap-fundamentals.md) provides larger, pre-styled components. Having now used both
concretely, the actual decision criteria are worth making explicit.

## When Tailwind Tends to Fit Better

- **A highly custom visual design** — a real product with its own distinct brand identity, where
  the goal is a specific, non-generic look rather than a recognizably "default Bootstrap" feel.
- **A component-based frontend framework already in use** — Tailwind's utility classes compose
  naturally inside [React](../../react/) or [Next.js](../../nextjs/) components, where the styling
  and markup already live together in the same file.
- **A team that wants design consistency enforced by a shared, configured scale** (spacing, color,
  type), without needing to write and maintain custom CSS class names for it.

## When Bootstrap Tends to Fit Better

- **Speed to a working, reasonable-looking UI** — an internal admin tool, an MVP, or a prototype
  where visual distinctiveness matters far less than getting something functional and presentable
  built quickly.
- **A team less comfortable writing CSS at all** — Bootstrap's pre-built components require far
  less CSS knowledge to use correctly than composing a look from Tailwind's utilities.
- **A project that genuinely doesn't need a highly custom visual identity** — many internal tools
  and dashboards are perfectly well served by Bootstrap's solid, familiar defaults.

## When Hand-Written CSS/Sass Is Still the Right Call

Neither framework is a mandatory default. [Working with Sass](../working-with-sass/) and
[CSS Core Fundamentals](../css-core-fundamentals/) remain the right choice when a project needs
something neither utility classes nor pre-built components handle well — deeply custom, unusual
visual effects; a very small project where a whole framework's learning curve and dependency isn't
worth the payoff; or a team that specifically wants full, unconstrained control over every rule.

## They Aren't Mutually Exclusive

A real project can — and often does — combine approaches: using Bootstrap's grid for overall page
structure while writing custom Sass for a few genuinely unique components, or using Tailwind
alongside a small amount of hand-written CSS for something Tailwind's utilities don't cleanly
express. The goal is picking the right tool for each specific part of the UI, not treating "which
framework" as a single, all-or-nothing decision for an entire project.

## A Practical Decision Framework

1. Does the project need a highly custom, brand-specific visual identity? → **Tailwind** (or
   hand-written CSS/Sass) gives more control.
2. Does the team need to move fast with a smaller CSS-writing burden? → **Bootstrap**'s pre-built
   components get there faster.
3. Is the project small, or does it need something neither framework handles well? →
   **Hand-written CSS/Sass** remains completely valid.
4. Is the team already deep in a component-based frontend framework? → **Tailwind** tends to
   compose more naturally alongside component code.

## Common Mistakes

- Treating this as a permanent, ideological choice ("Tailwind is always better," "Bootstrap is
  outdated") rather than a genuine tradeoff decision made per project, based on its actual
  requirements and team.
- Adding a framework dependency to a genuinely tiny project where a handful of hand-written CSS
  rules would have been simpler and lighter-weight.
- Assuming a choice made for one project should apply unconditionally to every future project — the
  right framework depends on that specific project's actual needs, not on habit.

## Module Summary

Across this module: **CSS frameworks** solve the "don't rebuild a design system from scratch every
project" problem, via two genuinely different philosophies — utility-first and component-based (see
[introduction-to-css-frameworks.md](introduction-to-css-frameworks.md)); **TailwindCSS** composes a
design from small, single-purpose utility classes directly in markup, drawing from a consistent,
pre-configured scale (see [tailwindcss-fundamentals.md](tailwindcss-fundamentals.md)), with
`min-width`-based breakpoint prefixes for responsive design (see
[building-responsive-layouts-with-tailwind.md](building-responsive-layouts-with-tailwind.md));
**Bootstrap** provides a 12-column grid and ready-made, pre-styled components, using the same
`min-width` breakpoint model (see [bootstrap-fundamentals.md](bootstrap-fundamentals.md)); and
choosing between Tailwind, Bootstrap, and hand-written CSS/Sass comes down to a project's actual
need for visual customization, team CSS comfort, and development speed — not blanket preference.
