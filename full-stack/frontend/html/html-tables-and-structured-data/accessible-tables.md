# Accessible Tables

## The `scope` Attribute

`scope` on a `<th>` declares whether it's a header for the rest of its **row** or the rest of its
**column** — this is what lets a screen reader correctly announce "North America, Q1: $120,000"
by combining a data cell with its correct row and column headers, rather than reading the raw grid
without that context:

```html
<th scope="col">Q1</th>   <!-- header for everything below it in this column -->
<th scope="row">Europe</th> <!-- header for everything to the right of it in this row -->
```

For a simple table with a single header row and/or a single header column, `scope` alone is
sufficient and should always be included — it costs nothing and provides real accessibility value.

## Complex Tables: `id` and `headers`

Some tables have headers that don't fit a simple row/column relationship — merged header cells
spanning multiple columns, or multiple levels of headers. For these, `scope` isn't expressive
enough, and the `id`/`headers` pattern is used instead: each header gets a unique `id`, and each
data cell lists every header that applies to it via `headers`:

```html
<table>
  <tr>
    <th id="name">Name</th>
    <th id="q1-sales" colspan="2">Q1 Sales</th>
  </tr>
  <tr>
    <th></th>
    <th id="online">Online</th>
    <th id="instore">In-Store</th>
  </tr>
  <tr>
    <td headers="name">Widget A</td>
    <td headers="q1-sales online">$4,000</td>
    <td headers="q1-sales instore">$2,500</td>
  </tr>
</table>
```

This is more verbose, and appropriately reserved for tables where `scope` genuinely can't express
the relationship — most tables are simple enough that `scope` is all that's needed.

## Tables Are Never for Page Layout

Before CSS layout (Flexbox, Grid) was well-supported, developers sometimes used `<table>` purely
to arrange page content visually into columns, with no actual tabular data involved. This is now
firmly a legacy anti-pattern:

- Assistive technology announces the element as a data table (row/column counts, navigation
  commands), which is actively confusing when the content isn't actually tabular.
- Page layout is unambiguously CSS's responsibility (Flexbox/Grid, covered in the CSS domain) —
  `<table>` should be reserved exclusively for content that is genuinely rows and columns of
  related data.

## Common Mistakes

- Reaching for `id`/`headers` by default even for simple tables, adding unnecessary verbosity where
  `scope` alone would work perfectly well.
- Using `<table>` for a visual multi-column layout with no actual tabular data — always a CSS
  layout problem, never an HTML table problem.
- Merging cells with `colspan`/`rowspan` without also correctly updating the header associations
  those merges affect, leaving mismatched or ambiguous header relationships.

## Module Summary

Across this module: HTML's structural table elements (`<caption>`, `<thead>`/`<tbody>`/`<tfoot>`,
`<th>`/`<td>`) make a table's organization explicit rather than implied (see
[table-structure-and-semantics.md](table-structure-and-semantics.md)); and `scope` (for simple
tables) or `id`/`headers` (for genuinely complex ones) is what lets assistive technology correctly
associate every data cell with the headers that describe it — with tables reserved strictly for
actual tabular data, never visual page layout.
