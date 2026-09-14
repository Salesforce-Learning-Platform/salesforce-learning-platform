# CSS Frameworks — TailwindCSS and Bootstrap

## Purpose

Every prior CSS module — [Core Fundamentals](../css-core-fundamentals/),
[Layout Mastery](../css-layout-mastery/), [Working with Sass](../working-with-sass/) — taught you
to write CSS (or Sass) yourself. This module introduces **CSS frameworks**: pre-built systems that
provide either ready-made utility classes (Tailwind) or ready-made components and a grid
(Bootstrap), letting you build a real interface without writing custom CSS for every single
element.

## Learning Objectives

- Explain the difference between utility-first and component-based CSS frameworks.
- Set up and use TailwindCSS utility classes for layout, spacing, color, and typography.
- Build a responsive layout using Tailwind's breakpoint prefixes.
- Use Bootstrap's grid system and common pre-built components.
- Decide between Tailwind, Bootstrap, and hand-written CSS/Sass for a given project.

## Prerequisites

- [CSS Core Fundamentals](../css-core-fundamentals/) and
  [CSS Layout Mastery](../css-layout-mastery/) — this module assumes you can already achieve the
  same layouts by hand, and compares each framework's approach against that baseline.

## Files in This Module

| File | Covers |
|---|---|
| [introduction-to-css-frameworks.md](introduction-to-css-frameworks.md) | What a CSS framework is, and utility-first vs. component-based approaches |
| [tailwindcss-fundamentals.md](tailwindcss-fundamentals.md) | Setting up Tailwind, and using utility classes for layout/spacing/color/typography |
| [building-responsive-layouts-with-tailwind.md](building-responsive-layouts-with-tailwind.md) | Tailwind's breakpoint prefixes, applied to a real responsive layout |
| [bootstrap-fundamentals.md](bootstrap-fundamentals.md) | Bootstrap's grid system, and common components (navbar, cards, buttons) |
| [comparing-tailwind-and-bootstrap.md](comparing-tailwind-and-bootstrap.md) | When to reach for which — and when hand-written CSS/Sass is still the right call |

## When to Deep-Dive vs. Skim

Deep-dive [tailwindcss-fundamentals.md](tailwindcss-fundamentals.md) — Tailwind's utility-first
model is the more widely adopted approach in modern frontend work, and the mental shift it requires
(styling directly in markup, rather than in a separate stylesheet) is worth understanding
precisely, not just superficially.

## Quick Knowledge Check

<details>
<summary>Does Tailwind generate CSS for every utility class it defines, even ones a project never actually uses?</summary>

No — modern Tailwind scans the project's actual markup and only generates CSS for the utility
classes genuinely used, keeping the final CSS output small regardless of how large Tailwind's full
utility set is. See [tailwindcss-fundamentals.md](tailwindcss-fundamentals.md).

</details>

<details>
<summary>In Bootstrap's grid, does col-md-6 apply only at the medium breakpoint, or at medium and larger?</summary>

Medium and larger — Bootstrap's breakpoint classes are `min-width`-based, so `col-md-6` applies
starting at the medium breakpoint and continues to apply at every larger breakpoint too, unless
overridden by a more specific class like `col-lg-4`. See
[bootstrap-fundamentals.md](bootstrap-fundamentals.md).

</details>

## References

- Tailwind CSS, [Styling with utility classes](https://tailwindcss.com/docs/styling-with-utility-classes)
- Bootstrap, [Grid system](https://getbootstrap.com/docs/5.3/layout/grid/)

## Continue Your Learning Path

Continue to the [CSS Architecture and Debugging module](../css-architecture-and-debugging/) to
organize hand-written CSS (or a mix of hand-written and utility classes) at scale.
