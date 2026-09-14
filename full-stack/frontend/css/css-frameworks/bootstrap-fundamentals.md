# Bootstrap Fundamentals

## The Container/Row/Column Structure

```html
<div class="container">
  <div class="row">
    <div class="col-8">Main content</div>
    <div class="col-4">Sidebar</div>
  </div>
</div>
```

Bootstrap's grid is built from three nested pieces: `.container` centers content on the page and
adds horizontal padding (or `.container-fluid` for a full-width, unpadded version); `.row` wraps a
set of columns; and `.col-*` classes define how much of the row's width each column occupies.

## The 12-Column Model

```html
<div class="row">
  <div class="col-8">col-8 — two-thirds width</div>
  <div class="col-4">col-4 — one-third width</div>
</div>

<div class="row">
  <div class="col">Equal</div>
  <div class="col">Equal</div>
  <div class="col">Equal</div>
</div>
```

Every row is divided into **12 template columns** — `col-8` spans 8 of those 12 (two-thirds of the
row), `col-4` spans the remaining 4 (one-third). A bare `.col` with no number automatically splits
the available space equally among however many `.col` elements share the row.

## Responsive Breakpoint Classes

```html
<div class="row">
  <div class="col-12 col-md-6 col-lg-4">Product Card</div>
  <div class="col-12 col-md-6 col-lg-4">Product Card</div>
  <div class="col-12 col-md-6 col-lg-4">Product Card</div>
</div>
```

Like Tailwind's prefixes (per
[building-responsive-layouts-with-tailwind.md](building-responsive-layouts-with-tailwind.md)),
Bootstrap's breakpoint classes are `min-width`-based: `col-md-6` applies starting at the medium
breakpoint (and continues to apply at every larger breakpoint too, unless overridden by a more
specific class like `col-lg-4`). This example stacks each card full-width on mobile (`col-12`), two
per row starting at medium (`col-md-6`), and three per row starting at large (`col-lg-4`).

## Common Pre-Built Components

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="/">Shop</a>
</nav>

<div class="card">
  <div class="card-body">
    <h5 class="card-title">Product Name</h5>
    <p class="card-text">$79.99</p>
    <button class="btn btn-primary">Add to Cart</button>
  </div>
</div>
```

Unlike Tailwind's utility classes, Bootstrap ships entire pre-styled components — `.navbar`,
`.card`, `.btn` — that already look like a finished, cohesive UI element with a single class (or a
small, documented combination of classes), no custom CSS required to get a reasonable starting
look.

## Common Mistakes

- Nesting `.row`/`.col` incorrectly — a `.col-*` should always be a direct child of a `.row`, and a
  `.row` should always be inside a `.container`/`.container-fluid`, or the grid's spacing and
  alignment break in confusing ways.
- Forgetting that Bootstrap's breakpoint classes are `min-width`-based, and being surprised that a
  `col-md-6` still applies at a much larger screen size unless a larger-breakpoint class overrides
  it.
- Trying to heavily customize Bootstrap's default component look through excessive class
  overriding, rather than using Bootstrap's own supported Sass variable customization (per
  [Working with Sass](../working-with-sass/)) meant for exactly that.

## Next

Continue to [comparing-tailwind-and-bootstrap.md](comparing-tailwind-and-bootstrap.md) to decide
which approach — or neither — actually fits a given project.
