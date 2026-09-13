# CSS Grid

## The Two-Dimensional Layout Model

Where [Flexbox](flexbox-deep-dive.md) distributes space along a single axis, **Grid** is
**two-dimensional** — it lays out rows and columns together, letting items align across both axes
simultaneously. This is the tool for layouts Flexbox genuinely struggles with: a page layout with
a header, sidebar, main content, and footer that all need to align to the same underlying grid.

## The Grid Container and Tracks

```css
.wrapper {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  grid-template-rows: auto 1fr auto;
  gap: 16px;
}
```

- `display: grid` establishes the grid container; direct children become **grid items**.
- `grid-template-columns`/`grid-template-rows` define the **tracks** — the actual rows and columns
  and their sizes.
- `fr` (a fraction unit unique to Grid) distributes remaining space proportionally — `1fr 1fr`
  splits remaining space evenly between two tracks, regardless of their content.

## Grid Lines and Placing Items

Every track boundary is a numbered **grid line**, which items can be explicitly placed against:

```css
.header { grid-column: 1 / -1; } /* spans from the first line to the last (full width) */
.sidebar { grid-row: 2 / 3; grid-column: 1 / 2; }
```

`-1` refers to the last line, regardless of how many tracks exist — a common, convenient way to
span an item across the full width without knowing the exact track count in advance.

## Named Template Areas — The Most Readable Approach

`grid-template-areas` lets you describe a layout visually, in the CSS itself, by naming regions and
assigning items to them:

```css
.wrapper {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-areas:
    "header  header"
    "sidebar main"
    "footer  footer";
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

The CSS literally looks like the layout it produces — this is often the most maintainable way to
express a page-level grid, since the structure is legible at a glance rather than requiring mental
translation from line numbers.

## Alignment

Grid shares `justify-content`/`align-items` with Flexbox for aligning content within the grid as a
whole, plus item-level equivalents (`justify-self`, `align-self`) for overriding a single item's
alignment within its own cell.

## `repeat()` and `minmax()` for Responsive Grids

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
```

This single line creates a responsive grid of at-least-200px columns that automatically adds or
removes columns as the container's width changes — no media query required, because `auto-fill`
and `minmax()` let the browser compute the column count dynamically.

## Common Mistakes

- Reaching for Grid for a simple one-dimensional list of items (a navigation bar, a row of
  buttons) where Flexbox is the simpler, more appropriate tool.
- Manually counting grid lines for complex layouts instead of using `grid-template-areas`, which is
  usually far more readable and maintainable.
- Forgetting `gap` and reaching for margin-based spacing hacks on individual grid items instead.

## Next

Continue to
[combining-grid-and-flex.md](combining-grid-and-flex.md) to see how to decide between Grid and
Flexbox, and when using both together makes sense.

## References

- MDN Web Docs, [Basic concepts of grid layout](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts)
- [Grid Garden](https://cssgridgarden.com/) — a free, interactive game for practicing Grid properties hands-on
