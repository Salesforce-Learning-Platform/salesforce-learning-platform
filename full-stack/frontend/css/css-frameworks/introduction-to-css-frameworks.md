# Introduction to CSS Frameworks

## Why Reach for a Framework At All

Writing every single style by hand — even with [Sass](../working-with-sass/) making it more
maintainable — still means designing a grid system, a spacing scale, a color palette, and a set of
common components (buttons, cards, navbars) from scratch, every single project. A **CSS framework**
provides a pre-built system for exactly this, letting a team start building an actual interface
immediately instead of first building the design system underneath it.

## Two Genuinely Different Philosophies

```html
<!-- Utility-first (Tailwind): styling composed directly from small,
     single-purpose classes, applied right in the markup -->
<button class="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium">
  Add to Cart
</button>
```

```html
<!-- Component-based (Bootstrap): a small number of ready-made,
     larger classes, each already representing a whole styled component -->
<button class="btn btn-primary">Add to Cart</button>
```

**Utility-first** frameworks (Tailwind) provide many small, single-purpose classes — one for
background color, one for padding, one for border radius — composed together directly in the
markup to build up a specific look. **Component-based** frameworks (Bootstrap) instead provide a
smaller number of larger, pre-designed classes, each already representing an entire styled
component — `.btn.btn-primary` is already a complete, styled button.

## The Real Tradeoff

| | Utility-first (Tailwind) | Component-based (Bootstrap) |
|---|---|---|
| Visual customization | Very flexible — compose exactly the look needed | Faster to start, but customizing beyond the defaults takes more effort |
| Markup | Can get visually dense with many utility classes | Stays clean; the actual styling logic lives in the framework's CSS |
| Design consistency | Comes from a shared, configured scale (spacing, colors) | Comes from the framework's own pre-designed components |
| Learning curve | Learning many utility class names | Learning a smaller set of component class names |

Neither approach is universally "better" — [comparing-tailwind-and-bootstrap.md](comparing-tailwind-and-bootstrap.md)
covers the concrete decision criteria once both are understood individually.

## Frameworks Don't Replace What You Already Know

Every concept from [CSS Core Fundamentals](../css-core-fundamentals/) and
[CSS Layout Mastery](../css-layout-mastery/) — the box model, Flexbox, Grid, specificity — still
applies underneath a framework; Tailwind's utilities and Bootstrap's components are both ultimately
generating and applying ordinary CSS rules built on exactly those same concepts. Understanding the
underlying CSS first (already covered) is what makes a framework's shortcuts make sense, rather
than feeling like unexplained magic — the same reasoning
[introduction-to-express.md](../../../backend/expressjs-fundamentals/introduction-to-express.md)
applies to Express sitting on top of Node's raw `http` module.

## Common Mistakes

- Reaching for a framework before understanding the underlying CSS it generates, making it hard to
  debug or customize anything beyond exactly what a tutorial happened to show.
- Assuming a component-based framework's default look is the final, unchangeable design — both
  Tailwind and Bootstrap are genuinely configurable and customizable, not fixed.
- Treating "utility-first" and "component-based" as the only two options — hand-written CSS/Sass
  remains a completely valid third choice for many projects, covered in
  [comparing-tailwind-and-bootstrap.md](comparing-tailwind-and-bootstrap.md).

## Next

Continue to [tailwindcss-fundamentals.md](tailwindcss-fundamentals.md) to start using Tailwind's
utility classes concretely.
