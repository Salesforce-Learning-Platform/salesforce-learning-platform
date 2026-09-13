# Semantic Tags

## What "Semantic" Means

A **semantic** HTML element is one whose name describes the *meaning* of its content, not just its
visual appearance. `<div>` and `<span>` are non-semantic — they carry no information about what
they contain. `<nav>`, `<article>`, and `<button>` are semantic — their names alone tell a
developer, a browser, a screen reader, or a search engine what role that content plays.

## Structural Semantic Elements

| Element | Represents |
|---|---|
| `<header>` | Introductory content for a page or section (often a logo, title, nav) |
| `<nav>` | A block of primary navigation links |
| `<main>` | The dominant, unique content of the document (one per page) |
| `<article>` | Self-contained content that would make sense distributed on its own (a blog post, a news story) |
| `<section>` | A thematic grouping of content, usually with its own heading |
| `<aside>` | Content tangentially related to the surrounding content (a sidebar, a pull quote) |
| `<footer>` | Footer content for a page or section (copyright, related links) |

```text
<body>
  <header>...</header>
  <nav>...</nav>
  <main>
    <article>
      <section>...</section>
    </article>
    <aside>...</aside>
  </main>
  <footer>...</footer>
</body>
```

## Inline Semantic Elements

Semantics apply at the inline level too, not just page structure:

| Element | Meaning |
|---|---|
| `<strong>` | Strong importance (not just bold — screen readers announce it differently than `<b>`) |
| `<em>` | Stressed emphasis (not just italic) |
| `<time>` | A specific date/time, optionally machine-readable via `datetime` |
| `<code>` | A fragment of computer code |
| `<blockquote>`/`<q>` | A quoted passage |

`<strong>` and `<b>` (or `<em>` and `<i>`) can look visually identical by default, but only the
semantic version communicates actual importance/emphasis to assistive technology — the
presentational versions (`<b>`, `<i>`) are purely visual with no implied meaning.

## `<div>` and `<span>` Still Have a Job

Semantic HTML doesn't mean `<div>` and `<span>` are wrong — they're the correct choice precisely
when there's no meaningful relationship to express, and you only need an element to apply styling
or scripting to a group of content (e.g., a generic wrapper for a CSS Grid layout with no
independent semantic meaning of its own).

## Common Mistakes

- Using `<div>` for everything out of habit, even when a semantic element (`<nav>`, `<button>`)
  exists and fits exactly.
- Choosing an element purely for its default visual style (using `<h3>` because you like its font
  size, rather than because it's the correct heading level) — see
  [content-structure-and-heading-hierarchy.md](content-structure-and-heading-hierarchy.md).
- Using more than one `<main>` per page, or nesting `<main>` inside `<article>`/`<aside>` — `<main>`
  must be a single, top-level landmark for the page's primary content.

## Next

Continue to
[content-structure-and-heading-hierarchy.md](content-structure-and-heading-hierarchy.md) to see
how these elements combine into a correctly structured document outline.
