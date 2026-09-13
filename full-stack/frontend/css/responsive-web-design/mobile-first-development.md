# Mobile-First Development

## Two Directions to Approach Responsive Design

You can write your base (unqualified) CSS for the largest screen and use media queries to strip
complexity away for smaller ones ("desktop-first"), or write your base CSS for the smallest screen
and use media queries to add complexity for larger ones ("mobile-first"). These sound symmetric,
but they produce meaningfully different results in practice.

## Why Mobile-First Tends to Win

```css
/* Mobile-first: base styles are the simple, single-column mobile layout */
.layout {
  display: block;
}

@media (min-width: 768px) {
  .layout {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}
```

```css
/* Desktop-first: base styles are the complex layout, undone for mobile */
.layout {
  display: grid;
  grid-template-columns: 200px 1fr;
}

@media (max-width: 767px) {
  .layout {
    display: block;
    grid-template-columns: none; /* has to explicitly undo the desktop rule */
  }
}
```

The mobile-first version only ever *adds* capability as screens get larger (`min-width` queries);
the desktop-first version has to *undo* prior declarations for smaller screens (`max-width`
queries), which tends to accumulate overrides and become harder to reason about as a design grows
in complexity.

## It's Also a Design Discipline, Not Just a CSS Technique

Starting from the most constrained context forces prioritization: what's the one most important
thing on this screen, given the least space and (often) a slower mobile connection? This tends to
produce clearer information hierarchy than starting with a spacious desktop canvas where everything
can fit, and only afterward asking what to remove for mobile.

## Performance Implications

A mobile-first approach pairs naturally with performance-conscious loading: base (mobile) styles
can be the entire CSS needed for a small-screen visitor, with more elaborate desktop styles loaded
or applied only when a `min-width` query actually matches — avoiding forcing every visitor,
including phone users on a slower connection, to download and process styles for a layout they'll
never see.

## Common Mistakes

- Writing desktop-first CSS out of habit (common if the developer primarily tests on a laptop) and
  discovering mobile-specific bugs late, since mobile was never the primary design target during
  development.
- Using `max-width` queries as the *only* strategy, accumulating override-on-override complexity as
  more breakpoints are added over a project's lifetime.
- Treating "mobile-first" as purely a media-query direction, missing the underlying design
  discipline of prioritizing content for the most constrained context first.

## Next

Continue to
[media-queries-and-breakpoints.md](media-queries-and-breakpoints.md) for the actual media query
syntax and how to choose breakpoints.
