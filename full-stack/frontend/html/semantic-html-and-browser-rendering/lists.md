# Lists

## Why Use List Elements at All

Any visually list-like content (navigation items, steps, a set of options) should usually be
marked up as an actual list element, not a series of `<div>`s or `<p>`s with manual bullet
characters. List elements announce their structure to assistive technology (e.g., "list, 5 items")
and make the semantic grouping explicit in the markup itself.

## The Three List Types

| Element | Use for |
|---|---|
| `<ul>` (unordered list) | Items with no meaningful sequence — a set of features, tags, or navigation links |
| `<ol>` (ordered list) | Items where sequence matters — steps in a process, a ranking |
| `<dl>` (description list) | Name/value or term/definition pairs — a glossary, metadata key-value pairs |

```html
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
</ul>

<ol>
  <li>Preheat the oven</li>
  <li>Mix the ingredients</li>
  <li>Bake for 20 minutes</li>
</ol>

<dl>
  <dt>HTTP</dt>
  <dd>HyperText Transfer Protocol</dd>
  <dt>DNS</dt>
  <dd>Domain Name System</dd>
</dl>
```

## Choosing Between `<ul>` and `<ol>`

Ask whether reordering the items would change their meaning. Ingredients in a recipe are usually
order-independent (`<ul>`); steps in that same recipe are not (`<ol>`) — a screen reader announces
`<ol>` items with their position ("step 2 of 5"), which is meaningfully different information from
an unordered list.

## Navigation Menus as Lists

A common, correct pattern: wrap navigation links in a `<ul>` inside a `<nav>` — combining the
structural landmark (`<nav>`) with the semantic grouping (`<ul>`) of the individual links:

```html
<nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

## Common Mistakes

- Using `<br>` tags or manual `•` characters to fake a list visually instead of using an actual
  list element — this loses all the semantic/accessibility benefit.
- Using `<ol>` for content where order genuinely doesn't matter, implying a sequence that isn't
  real.
- Nesting a list incorrectly — a nested `<ul>`/`<ol>` must be placed inside an `<li>` of the parent
  list, not as a sibling of it.

## Next

Continue to [links-and-navigation-flow.md](links-and-navigation-flow.md) to see how to make
navigation links themselves accessible and predictable.
