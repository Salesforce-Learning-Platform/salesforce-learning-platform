# Working with Sass

## Purpose

[CSS Core Fundamentals](../css-core-fundamentals/) taught plain CSS, including custom properties.
This module introduces **Sass**, a **preprocessor** — a language that compiles down to plain CSS,
adding programming-like features (variables, nesting, reusable logic) that plain CSS either lacks
entirely or only partially replicates.

## Learning Objectives

- Explain what Sass is, and why a stylesheet language needs to be "compiled" at all.
- Set up an SCSS build step for a project.
- Use Sass variables, and explain how they differ from CSS custom properties.
- Nest selectors, and use the parent selector (`&`) correctly.
- Split a stylesheet into partials, and combine them with `@use`.
- Write and use mixins and functions, and choose correctly between them.
- Use control directives and Sass's built-in color functions.

## Prerequisites

- [CSS Core Fundamentals](../css-core-fundamentals/) — specifically
  [css-variables.md](../css-core-fundamentals/css-variables.md), since this module compares Sass
  variables against CSS custom properties throughout.

## Files in This Module

| File | Covers |
|---|---|
| [what-is-sass.md](what-is-sass.md) | What a CSS preprocessor is, and why Sass exists |
| [setting-up-scss.md](setting-up-scss.md) | Installing and compiling SCSS in a real project |
| [variables.md](variables.md) | `$variable` syntax, `!default`, and Sass variables vs. CSS custom properties |
| [nesting.md](nesting.md) | Nested selectors and the parent selector (`&`) |
| [partials-and-imports.md](partials-and-imports.md) | Splitting styles into partials, and `@use` |
| [mixins.md](mixins.md) | `@mixin`/`@include`, arguments, and `@content` blocks |
| [functions.md](functions.md) | `@function`/`@return`, and choosing between a mixin and a function |
| [inheritance-and-extends.md](inheritance-and-extends.md) | `@extend`, and how it differs from a mixin |
| [operators.md](operators.md) | Math and comparison operators in Sass expressions |
| [control-directives.md](control-directives.md) | `@if`/`@else`, `@each`, `@for`, and `@while` |
| [color-functions.md](color-functions.md) | Built-in color manipulation functions |

## When to Deep-Dive vs. Skim

Deep-dive [variables.md](variables.md) — the distinction between Sass variables (compile-time,
removed entirely from the output) and CSS custom properties (runtime, live in the browser) is the
single most important, and most commonly confused, concept in this module.

## Quick Knowledge Check

<details>
<summary>Can a Sass variable's value be read or changed by JavaScript in the browser, the way a CSS custom property can?</summary>

No — a Sass variable only exists at compile time. By the time the SCSS is compiled to plain CSS,
every `$variable` has been replaced with its literal value; nothing about the variable itself
survives into the browser. A CSS custom property, by contrast, is a genuine runtime value the
browser (and JavaScript) can read and change. See [variables.md](variables.md).

</details>

<details>
<summary>Should a reusable piece of Sass logic that needs to output actual CSS rules be a mixin or a function?</summary>

A **mixin** — mixins can contain and output style rules directly via `@include`. A **function**
computes and returns a single value (used inside a property's value), and is discouraged from
having side effects like emitting CSS on its own. See [mixins.md](mixins.md) and
[functions.md](functions.md).

</details>

## References

- Sass, [Documentation Overview](https://sass-lang.com/documentation/)
- Sass, [Variables](https://sass-lang.com/documentation/variables/)
- Sass, [Style Rules (Nesting)](https://sass-lang.com/documentation/style-rules/)
- Sass, [@mixin and @include](https://sass-lang.com/documentation/at-rules/mixin/)
- Sass, [@function](https://sass-lang.com/documentation/at-rules/function/)
- Sass, [@use](https://sass-lang.com/documentation/at-rules/use/)

## Continue Your Learning Path

Continue to the [CSS Frameworks module](../css-frameworks/) to see how a utility-first framework
like Tailwind approaches the same "avoid repeating yourself in CSS" goal from a different angle.
