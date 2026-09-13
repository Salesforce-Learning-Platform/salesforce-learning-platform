# Combining Grid and Flexbox

## They're Not Competing Tools

Grid and Flexbox solve different, complementary problems — treating them as rival technologies to
pick "the winner" from misses the point. The practical decision is about dimensionality, not which
tool is generally better.

## The Deciding Question

**Does this layout need to align things in one direction, or in two directions at once?**

| Need | Use |
|---|---|
| A row of nav links, a toolbar, distributing space along one line | Flexbox |
| A card's internal layout: image, then title, then button, stacked or in a row | Flexbox |
| A page-level layout: header, sidebar, main, footer, all aligning to shared columns/rows | Grid |
| A photo gallery where items should align into a consistent row/column structure | Grid |
| Centering one item inside a container (either axis) | Either works; Flexbox is typically simpler for this single case |

## Using Them Together

The most common real-world pattern is **Grid for the page's overall structure, Flexbox for the
internal layout of individual components** within that structure:

```css
/* Grid: overall page layout */
.page {
  display: grid;
  grid-template-columns: 220px 1fr;
  grid-template-areas: "sidebar main";
}

/* Flexbox: layout within one grid area's component */
.card {
  display: flex;
  align-items: center;
  gap: 12px;
}
```

This isn't a compromise — it reflects that the page-level structure is genuinely two-dimensional
(rows and columns of major regions), while a single card's internal arrangement (an icon next to a
label) is genuinely one-dimensional.

## A Practical Decision Process

1. Sketch the layout. Does it need row *and* column alignment simultaneously, or just one
   direction?
2. If two-dimensional structure matters (things need to line up both across and down), reach for
   Grid.
3. If it's fundamentally a single row or column of items that need to distribute or align along
   one line, reach for Flexbox.
4. Most real interfaces use both, nested — Grid for the outer structure, Flexbox for components
   within it.

## Common Mistakes

- Treating this as a binary "which is better" choice rather than a question of dimensionality —
  most non-trivial interfaces genuinely need both, at different levels of nesting.
- Building a whole page with nested Flexbox containers to approximate a two-dimensional grid,
  when `display: grid` would express the same layout more directly and with fewer wrapper elements.
- Using Grid for something as simple as a single row of evenly spaced buttons, where Flexbox is
  simpler and sufficient.

## Module Summary

Across this module: Grid is the two-dimensional layout model, using tracks, grid lines, and named
template areas to align content across rows and columns simultaneously (see
[css-grid.md](css-grid.md)); and the practical choice between Grid and Flexbox comes down to
dimensionality — one direction favors Flexbox, two directions at once favors Grid, and most real
interfaces nest both together rather than choosing exclusively.

This completes CSS Layout Mastery — see
[Positioning](positioning.md), [Stacking Context](stacking-context.md), and
[Common Layout Patterns](common-layout-patterns.md) for the foundational layout concepts this
module builds on, or continue to
[Responsive Web Design](../responsive-web-design/) — see the
[Frontend learning path](../../README.md) for the full sequence.
