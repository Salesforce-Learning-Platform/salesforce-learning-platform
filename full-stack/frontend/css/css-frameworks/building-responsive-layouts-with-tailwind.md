# Building Responsive Layouts with Tailwind

## Breakpoint Prefixes

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="card">Product 1</div>
  <div class="card">Product 2</div>
  <div class="card">Product 3</div>
</div>
```

A prefix like `sm:` or `lg:` applies its utility only starting at that breakpoint and up — `grid-
cols-1` (one column) applies by default, `sm:grid-cols-2` overrides it to two columns starting at
the small breakpoint, and `lg:grid-cols-3` overrides it again to three columns starting at large.
This is a utility-class expression of exactly the same mobile-first strategy already covered in
[mobile-first-development.md](../responsive-web-design/mobile-first-development.md), where the
unprefixed, smallest-screen styles come first and larger-screen overrides layer on top.

## Tailwind's Default Breakpoints

| Prefix | Applies at (and above) |
|---|---|
| (none) | Every screen size — the mobile-first base |
| `sm:` | 40rem (640px) |
| `md:` | 48rem (768px) |
| `lg:` | 64rem (1024px) |
| `xl:` | 80rem (1280px) |

Each prefix generates a `min-width` media query — directly the same underlying CSS mechanism
covered in
[media-queries-and-breakpoints.md](../responsive-web-design/media-queries-and-breakpoints.md), just
generated automatically from the prefix rather than written by hand.

## Combining Responsive Prefixes With Other Utilities

```html
<nav class="flex flex-col md:flex-row items-center gap-2 md:gap-6 p-4">
  <a href="/">Home</a>
  <a href="/products">Products</a>
  <a href="/cart">Cart</a>
</nav>
```

A single element can combine several responsive utilities at once — here, the nav stacks
vertically (`flex-col`) with tighter spacing on small screens, and switches to a horizontal row
(`md:flex-row`) with more spacing (`md:gap-6`) starting at the medium breakpoint. Each utility's
responsive variant is independent, so different properties can change at different breakpoints as
needed.

## Responsive Typography and Visibility

```html
<h1 class="text-2xl md:text-4xl font-bold">Welcome</h1>

<div class="hidden md:block">Desktop-only sidebar content</div>
<div class="md:hidden">Mobile-only menu button</div>
```

`hidden`/`md:block` (and its inverse, `md:hidden`) is Tailwind's utility-based way to show
genuinely different content per screen size — a common, real pattern for something like a
collapsed mobile menu button that shouldn't appear at all on a desktop-sized layout.

## Common Mistakes

- Designing "desktop-first" with Tailwind — applying complex layout at the base (unprefixed) level
  and trying to override it back down for smaller screens, working against the mobile-first
  breakpoint model instead of with it.
- Using `hidden`/`block` toggles as a substitute for a real responsive layout, when a single
  responsive grid or flex arrangement would achieve the same visual result more simply.
- Forgetting that each responsive prefix is independent per-utility — a class like
  `md:flex-row` doesn't retroactively affect an unrelated utility on the same element unless that
  utility is also given its own responsive prefix.

## Next

Continue to [bootstrap-fundamentals.md](bootstrap-fundamentals.md) to see the same responsive-design
goal solved by a component-based framework instead.
