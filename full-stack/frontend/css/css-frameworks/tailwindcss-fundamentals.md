# TailwindCSS Fundamentals

## What "Utility-First" Actually Looks Like

```html
<div class="mx-auto flex max-w-sm items-center gap-x-4 rounded-xl bg-white p-6 shadow-lg">
  <img class="size-12 shrink-0" src="/logo.svg" alt="Company logo" />
  <div>
    <div class="text-xl font-medium text-black">ChitChat</div>
    <p class="text-gray-500">You have a new message!</p>
  </div>
</div>
```

Every class here is a **utility**: `flex` sets `display: flex`, `p-6` sets padding, `rounded-xl`
sets `border-radius`, `shadow-lg` sets `box-shadow`. None of them do anything alone that plain CSS
couldn't — the entire point is composing many small, single-purpose utilities together, directly in
the markup, instead of writing a separate CSS rule with a custom class name for this exact
combination.

## Only the Utilities Actually Used Ship in the Final CSS

Tailwind scans a project's real markup (every `.html`/`.jsx`/`.tsx` file, per
[Modern Frontend Tooling](../../foundations/preparing-your-machine/)'s broader build-tooling
context) and generates CSS only for the utility classes genuinely present somewhere in that
markup — Tailwind's full utility set is enormous, but a project's actual compiled CSS stays small,
containing only what's used.

## Layout and Spacing Utilities

```html
<div class="flex items-center justify-between gap-4 p-4">
  <span>Left</span>
  <span>Right</span>
</div>
```

`flex`, `items-center`, `justify-between`, and `gap-4` map directly onto the Flexbox properties
already covered in [CSS Layout Mastery](../css-layout-mastery/) — Tailwind doesn't introduce a new
layout model; it gives every CSS property from `display: flex` through `padding` a corresponding,
consistently-named utility class.

## A Consistent Design Scale, Not Arbitrary Values

```html
<div class="p-4">   <!-- padding: 1rem, from Tailwind's spacing scale -->
<div class="p-6">   <!-- padding: 1.5rem -->
<div class="p-[18px]"> <!-- an arbitrary, one-off value — used sparingly -->
```

Tailwind's numeric utilities (`p-4`, `p-6`, `text-xl`) come from a pre-configured, consistent
**scale** — directly the same underlying goal as
[design-systems-and-design-tokens.md](../css-core-fundamentals/design-systems-and-design-tokens.md)'s
centralized spacing/color values, just expressed as ready-made utility classes instead of custom
CSS variables. Reaching for an arbitrary value (`p-[18px]`) works but bypasses that consistency, and
is best reserved for genuine one-off exceptions.

## Colors and Typography

```html
<h1 class="text-2xl font-bold text-gray-900">Product Details</h1>
<p class="text-base text-gray-600 leading-relaxed">A detailed description...</p>
```

`text-2xl`/`font-bold` control font size and weight; `text-gray-900`/`text-gray-600` apply colors
from Tailwind's built-in, pre-designed color palette (a full range of shades per color, already
tuned for accessible contrast) — directly usable without needing to hand-pick hex values the way
plain CSS or Sass would require.

## Common Mistakes

- Reaching for an arbitrary value (`p-[18px]`) as a first choice instead of the nearest value on
  Tailwind's built-in scale, gradually eroding the visual consistency utility classes are meant to
  provide.
- Writing extremely long utility class strings on a single element without any organization,
  making the markup hard to scan — extracting a repeated combination into a reusable component (in
  whichever framework, per [the React domain](../../react/)) is usually the better fix.
- Assuming Tailwind ships all its utility CSS regardless of usage — modern Tailwind specifically
  avoids this by scanning actual markup, keeping the real output lean.

## Next

Continue to
[building-responsive-layouts-with-tailwind.md](building-responsive-layouts-with-tailwind.md) to
apply these utilities responsively, across different screen sizes.
