# 🧱 The BEM Naming Convention

## The Problem: CSS Has No Real Namespacing

```css
/* Two different developers, two different components,
   the SAME class name — a silent collision */
.title { font-size: 24px; }   /* meant for a product card */
.title { font-size: 14px; }   /* meant for a sidebar widget — overwrites the above! */
```

Plain CSS class names are all global — there's no built-in way to scope `.title` to just one
component the way [Node's module system](../../../backend/nodejs-core-concepts/modules.md) scopes
a variable to one file. On a large project with many contributors, this leads to exactly the
collision above: two unrelated components accidentally sharing a class name, each unknowingly
overwriting the other.

## Block, Element, Modifier

```css
/* Block — a standalone, meaningful component on its own */
.card { }

/* Element — a part of the block, meaningless on its own (double underscore) */
.card__title { }
.card__price { }

/* Modifier — a variation of the block or an element (double hyphen) */
.card--featured { }
.card__price--discounted { }
```

```html
<div class="card card--featured">
  <h3 class="card__title">Mechanical Keyboard</h3>
  <span class="card__price card__price--discounted">$59.99</span>
</div>
```

**BEM** stands for **Block, Element, Modifier** — a naming methodology, not a technology: it's just
a consistent, disciplined way of naming plain CSS classes.

- A **Block** is a standalone, meaningful component (`card`) — it makes sense on its own.
- An **Element** (`card__title`, with a double underscore) is a part *of* that block — it has no
  meaning outside the block it belongs to.
- A **Modifier** (`card--featured`, with a double hyphen) describes a variation of a block or an
  element — the same underlying idea as
  [modifier props in a React design system](../../react/component-architecture-and-composition/reusable-component-design.md),
  expressed as a naming pattern instead of a component prop.

## 🔒 Why BEM Actually Solves the Collision Problem

`.card__title` is far less likely to collide with anything than a bare `.title` — the block prefix
effectively **namespaces** every element's class name to the specific component it belongs to.
This isn't a technical guarantee the way JavaScript module scoping is; it's a **social
contract** — a shared convention every contributor follows, which is precisely why consistency
matters more here than almost any other CSS discipline in this platform.

## Flat Specificity, By Design

```css
/* BEM avoids this entirely */
.card .title { }              /* nested — specificity (0,0,2,0) */

/* BEM prefers this */
.card__title { }              /* flat — specificity (0,0,1,0) */
```

BEM classes are deliberately written as single, flat class selectors rather than nested descendant
selectors — directly avoiding the specificity escalation
[specificity-and-cascade.md](../css-core-fundamentals/specificity-and-cascade.md) already warned
about. Every BEM class carries the *same*, predictable, low specificity, which means later styles
can reliably override earlier ones without a specificity fight.

## Common Mistakes

- Nesting BEM elements to mirror deep HTML structure (`card__header__title`) — an element belongs
  to its block directly; it doesn't need to encode every level of HTML nesting in its name.
- Using a single hyphen for a modifier (`card-featured`) instead of the double-hyphen convention
  (`card--featured`), breaking the visual distinction between a multi-word block/element name and
  an actual modifier.
- Applying BEM inconsistently across a codebase — a naming convention's entire value comes from
  everyone following it; a codebase that's "BEM in some files, ad hoc in others" gets little of the
  real benefit.

## ➡️ Next

Continue to [component-based-css.md](component-based-css.md) to apply this naming discipline
toward genuinely reusable style blocks.
