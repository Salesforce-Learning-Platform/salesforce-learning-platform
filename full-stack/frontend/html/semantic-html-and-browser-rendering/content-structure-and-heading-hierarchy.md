# Content Structure and Heading Hierarchy

## The Document Outline

Headings (`<h1>` through `<h6>`) don't just create visually large text — they define the
document's **outline**, a hierarchical structure that assistive technology and search engines use
to understand how content is organized, independent of visual styling.

## Heading Rules That Actually Matter

- **Use exactly one `<h1>` per page**, describing the page's main content (not the site name —
  that belongs in a logo/header, not necessarily an `<h1>`).
- **Don't skip levels** going down (`<h1>` → `<h3>` with no `<h2>`) — screen reader users navigate
  by heading level, and a skipped level reads as a structural gap.
- **Nest headings to reflect actual content hierarchy**, not desired font size — if a subsection
  is a child of a section, its heading should be one level deeper.

```text
<h1>Blog Post Title</h1>
  <h2>Introduction</h2>
  <h2>Main Argument</h2>
    <h3>First Point</h3>
    <h3>Second Point</h3>
  <h2>Conclusion</h2>
```

## Sectioning Content Correctly

Pair headings with the sectioning elements from
[semantic-tags.md](semantic-tags.md): each `<section>` or `<article>` should typically have its
own heading describing what it contains — this is what lets a screen reader user pull up a list of
headings and jump directly to the section they want, without reading the whole page linearly.

## Common Mistakes

- Choosing a heading level for its default font size rather than its correct place in the
  document's structure — this should be controlled with CSS, not by picking the "wrong" semantic
  level for visual reasons.
- Using multiple `<h1>` elements to represent unrelated top-level sections instead of an `<h1>`
  plus properly nested `<h2>`s.
- Wrapping a heading in a `<div>` styled to look like a heading instead of using an actual `<h1>`–`<h6>` element — this breaks the outline entirely for assistive technology.

## Next

Continue to [lists.md](lists.md) to see the semantic elements for grouped, ordered, and described
content.
