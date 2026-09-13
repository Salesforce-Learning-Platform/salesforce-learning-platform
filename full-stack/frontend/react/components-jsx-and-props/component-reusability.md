# Component Reusability

## Designing for Reuse

A component becomes genuinely reusable when it's parameterized by props rather than hardcoded for
one specific use — the same underlying principle as writing a general-purpose function (see
[functions](../../javascript/functions/)) instead of duplicating near-identical code for each
call site.

```jsx
// Not reusable — hardcoded for one specific case
function AdaAvatar() {
  return <img src="/avatars/ada.png" width={100} />;
}

// Reusable — parameterized via props
function Avatar({ name, size }) {
  return <img src={`/avatars/${name}.png`} width={size} />;
}
```

## Composition Over Configuration

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>;
}

<Card>
  <Avatar name="ada" size={50} />
  <h3>Ada Lovelace</h3>
</Card>
```

Rather than building a `Card` component with dozens of specific props trying to anticipate every
possible use (`showAvatar`, `avatarSize`, `title`, `showTitle`, ...), the `children` prop (from
[props.md](props.md)) lets `Card` stay simple and genuinely reusable — the parent decides exactly
what goes inside, and `Card` only handles the wrapping concern it's actually responsible for.

## When *Not* to Extract a Reusable Component

Not every repeated bit of markup needs to become its own component immediately. Extracting a
component too early, before a genuine, stable pattern of reuse has emerged, can add an extra layer
of indirection for no real benefit — and the "right" prop interface is often much clearer once
you've seen two or three real, different use cases, rather than guessing upfront.

## A Practical Signal for When to Extract

- The same JSX structure appears in multiple places with only small, parameterizable differences.
- A section of a large component is complex enough to be hard to read inline, regardless of reuse.
- A piece of UI has a clear, nameable responsibility that makes sense as its own unit (`Avatar`,
  `Card`, `PriceTag`) — this is the same "one component, one responsibility" idea from
  [components.md](components.md).

## Common Mistakes

- Extracting a "reusable" component after seeing it needed only once, guessing at a prop interface
  that doesn't actually fit once a second, genuinely different use case appears.
- Building an over-configurable component with many boolean/conditional props trying to handle
  every possible variation, when composition via `children` would be simpler and more flexible.
- Duplicating the same non-trivial JSX structure across a codebase without ever extracting it,
  making a later change need to be applied — and easy to miss — in every duplicated location.

## Module Summary

Across this module: components are ordinary JavaScript functions returning JSX, conventionally
capitalized to distinguish them from HTML elements (see [components.md](components.md)); JSX
follows three syntax rules (single root element, closed tags, camelCase attributes) and embeds
JavaScript expressions via `{}` (see [jsx.md](jsx.md)); props pass data from parent to child, are
read-only from the receiving component's perspective, and the `children` prop enables powerful
composition patterns (see [props.md](props.md)); and genuinely reusable components are
parameterized by props and built around composition, best extracted once a real, stable pattern of
reuse has actually emerged rather than guessed at in advance.
