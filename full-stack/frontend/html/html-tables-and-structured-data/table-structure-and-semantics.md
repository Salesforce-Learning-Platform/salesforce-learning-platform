# Table Structure and Semantics

## Beyond `<table>` and `<tr>`

A minimal table works with just `<table>`, `<tr>`, and `<td>` — but HTML provides a fuller set of
structural elements that make a table's organization explicit, rather than implied purely by
position.

```html
<table>
  <caption>Quarterly Revenue by Region</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Q1</th>
      <th scope="col">Q2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">North America</th>
      <td>$120,000</td>
      <td>$135,000</td>
    </tr>
    <tr>
      <th scope="row">Europe</th>
      <td>$95,000</td>
      <td>$102,000</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$215,000</td>
      <td>$237,000</td>
    </tr>
  </tfoot>
</table>
```

## The Structural Elements

| Element | Role |
|---|---|
| `<caption>` | The table's title/description — always the first child of `<table>` |
| `<thead>` | Groups header rows |
| `<tbody>` | Groups the main data rows |
| `<tfoot>` | Groups summary/footer rows (like totals) |
| `<tr>` | A table row |
| `<th>` | A header cell — describes a row or column |
| `<td>` | A standard data cell |

## `<th>` vs. `<td>` — Not Interchangeable

This is the single most important distinction in this file: `<th>` marks a cell as a **header**,
which both browsers (default bold, centered styling) and assistive technology treat differently
from a regular `<td>` data cell. Using `<td>` for what's conceptually a header loses that semantic
signal entirely — a screen reader has no way to know which cells are headers if they're all marked
up as `<td>`.

## Why `<caption>` Matters

A `<caption>` gives the table an accessible name, announced by screen readers before they begin
reading the table's content — similar in purpose to how a heading introduces a section (see
[content-structure-and-heading-hierarchy.md](../semantic-html-and-browser-rendering/content-structure-and-heading-hierarchy.md)).
A table with no caption and no surrounding heading gives a screen reader user no context about
what the data represents before they start navigating it.

## Common Mistakes

- Using `<td>` for header cells that should be `<th>`, losing the header/data distinction entirely.
- Omitting `<caption>` and relying only on a nearby paragraph or heading to describe the table,
  leaving no direct programmatic association between the table and its description.
- Using `<thead>`/`<tbody>` purely for styling hooks without actually separating header rows from
  data rows correctly — `<thead>` should contain only header rows.

## Next

Continue to [accessible-tables.md](accessible-tables.md) for header association in complex tables,
and why tables should never be used for page layout.
