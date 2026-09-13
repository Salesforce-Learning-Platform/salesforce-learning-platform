# Stacking Context

## The Problem `z-index` Solves

When elements overlap, something has to determine which one renders on top. `z-index` lets you
control this explicitly — but only works predictably once you understand **stacking contexts**,
which is where most `z-index` confusion actually comes from.

## What Creates a Stacking Context

A stacking context is created by (among others):

- The root `<html>` element.
- Any element with `position: relative`/`absolute` **and** a `z-index` other than `auto`.
- Any element with `position: fixed` or `sticky`.
- Any element with `opacity` less than 1.
- Any element with a non-`none` `transform`, `filter`, or similar.

## The Rule That Actually Matters

**`z-index` values only compare *within* the same stacking context.** An element with a huge
`z-index` inside one stacking context cannot appear above an element in a *different, later-painted*
stacking context — the comparison never happens at that level. Each stacking context is stacked as
one atomic unit relative to its siblings; what happens *inside* it is invisible to that outer
comparison.

```html
<div class="context-a" style="position: relative; z-index: 1;">
  <div style="position: relative; z-index: 999;">A</div>
</div>
<div class="context-b" style="position: relative; z-index: 2;">
  <div style="position: relative; z-index: 1;">B</div>
</div>
```

Here, `B` renders above `A`, even though `A`'s inner element has `z-index: 999` and `B`'s inner
element only has `z-index: 1` — because `context-a` (z-index 1) is stacked below `context-b`
(z-index 2) as whole units, and nothing inside `context-a` can escape above `context-b` regardless
of its own internal `z-index` value.

## Debugging Stacking Issues

When an element unexpectedly renders behind (or in front of) another despite a "correct-looking"
`z-index`, the actual question is almost always: *are these two elements even in the same stacking
context?* Browser DevTools' Elements panel (see
[browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md))
can show computed styles and ancestor positioning to help trace which stacking context each
element actually belongs to, rather than guessing by trial-and-error `z-index` increases.

## Common Mistakes

- Repeatedly increasing `z-index` (`999`, `9999`, `99999`) to "win" a stacking conflict, when the
  actual problem is that the elements are in different stacking contexts entirely — no `z-index`
  value fixes that.
- Not realizing that properties like `opacity` and `transform` create a new stacking context as a
  side effect, unexpectedly changing how a `z-index` inside that element behaves relative to
  outside elements.
- Assuming `z-index` works on any element — it only has an effect on positioned elements
  (`position` other than `static`) or flex/grid items.

## Next

Continue to
[common-layout-patterns.md](common-layout-patterns.md) for classic layout problems and how
`overflow` and normal-flow techniques address them.
