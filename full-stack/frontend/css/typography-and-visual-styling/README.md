# CSS Typography and Visual Styling

## Purpose

Layout (covered in [CSS Layout Mastery](../css-layout-mastery/)) determines where things sit; this
module covers how they actually look — text, color, backgrounds, borders, and shadows — and how to
apply visual styling in a way that stays maintainable rather than becoming a pile of one-off
values.

## Learning Objectives

- Choose and apply font families, sizes, and weights correctly, including fallback font stacks.
- Use color and background properties effectively, including sufficient contrast for accessibility.
- Apply borders, shadows, and other visual effects to establish clear visual hierarchy.
- Keep visual styling maintainable using the design-token approach from
  [design-systems-and-design-tokens.md](../css-core-fundamentals/design-systems-and-design-tokens.md).

## Prerequisites

[CSS Fundamentals](../css-core-fundamentals/).

## Files in This Module

| File | Covers |
|---|---|
| [typography-fundamentals.md](typography-fundamentals.md) | Font families, size, weight, line-height, and text properties |
| [color-and-backgrounds.md](color-and-backgrounds.md) | Color formats, contrast, and background properties |
| [borders-shadows-and-visual-effects.md](borders-shadows-and-visual-effects.md) | Borders, box-shadow, and building visual hierarchy without clutter |

## When to Deep-Dive vs. Skim

Deep-dive [color-and-backgrounds.md](color-and-backgrounds.md) specifically for the contrast
section before shipping any real interface — insufficient color contrast is one of the most common
accessibility failures on the web, and it's straightforward to check for.

## Quick Knowledge Check

<details>
<summary>Why does a font-family declaration usually list several fonts, like `font-family: "Inter", Arial, sans-serif;`?</summary>

This is a font stack — if the first-choice font isn't available (not installed, failed to load),
the browser falls back to the next one in the list, down to a generic family (`sans-serif`) as a
last resort. Without a fallback, an unavailable font can silently fall back to something
unpredictable. See [typography-fundamentals.md](typography-fundamentals.md).

</details>

<details>
<summary>Is choosing a "nice-looking" color combination enough to guarantee text is readable for everyone?</summary>

No — text needs a minimum contrast ratio against its background (WCAG recommends 4.5:1 for normal
text) to be reliably readable, including for users with low vision or color vision deficiencies.
Contrast should be checked with a tool, not judged purely by eye. See
[color-and-backgrounds.md](color-and-backgrounds.md).

</details>

## References

- MDN Web Docs, [Fundamental text and font styling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Text_styling/Fundamentals)
- WebAIM, [Contrast Checker](https://webaim.org/resources/contrastchecker/)

## Continue Your Learning Path

Next: [Advanced CSS and Modern Styling](../advanced-css-and-modern-styling/) — see the
[Frontend learning path](../../README.md) for the full sequence.
