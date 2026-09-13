# HTML Tables and Structured Data

## Purpose

Tables are the correct element for genuinely tabular data — anything with meaningful rows and
columns, like a pricing comparison or a schedule. This module covers building tables that are
both correctly structured and accessible, since tables have a well-documented history of being
either misused (for page layout) or built without the structure that makes them usable with
assistive technology.

## Learning Objectives

- Build a table using the full set of structural elements, not just `<table>` and `<tr>`.
- Correctly associate header cells with the data cells they describe, including in tables with
  multiple header levels.
- Explain why tables should never be used for visual page layout.

## Prerequisites

[Semantic HTML and Browser Rendering](../semantic-html-and-browser-rendering/).

## Files in This Module

| File | Covers |
|---|---|
| [table-structure-and-semantics.md](table-structure-and-semantics.md) | `<table>`, `<caption>`, `<thead>`/`<tbody>`/`<tfoot>`, `<tr>`, `<th>`, `<td>` |
| [accessible-tables.md](accessible-tables.md) | The `scope` attribute, headers for complex tables, and why tables are never for layout |

## When to Deep-Dive vs. Skim

If you've only ever built simple tables, deep-dive
[accessible-tables.md](accessible-tables.md) the first time you need a table with a genuinely
complex header structure (merged cells, multiple header rows) — this is where accessible markup
stops being obvious and needs deliberate attention.

## Quick Knowledge Check

<details>
<summary>Why shouldn't you use a `<table>` purely to lay out a page visually (like a three-column layout)?</summary>

A `<table>` tells assistive technology "this is tabular data" — a screen reader will announce row
and column counts and navigate it as data, which is confusing and wrong for content that isn't
actually a table. Page layout is CSS's job (Flexbox/Grid), not HTML's. See
[accessible-tables.md](accessible-tables.md).

</details>

<details>
<summary>What does the `scope` attribute on a `<th>` actually do?</summary>

It declares whether that header describes the rest of its row (`scope="row"`) or the rest of its
column (`scope="col"`), letting a screen reader correctly announce which header applies to any
given data cell — without it, that association can be ambiguous, especially in complex tables. See
[accessible-tables.md](accessible-tables.md).

</details>

## References

- MDN Web Docs, [`<table>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/table)
- W3C WAI, [Tables Tutorial](https://www.w3.org/WAI/tutorials/tables/)

## Continue Your Learning Path

Next: [HTML Media and Embedded Content](../html-media-and-embedded-content/) — see the
[Frontend learning path](../../README.md) for the full sequence.
