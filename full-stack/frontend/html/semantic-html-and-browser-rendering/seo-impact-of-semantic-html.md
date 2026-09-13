# SEO Impact of Semantic HTML

## Why Markup Choices Affect Search Visibility

Search engines don't render a page the way a human sees it — they parse the underlying HTML to
understand what content exists and how it's structured, using much of the same information covered
throughout this module for accessibility. Search engine crawlers and screen readers are, in this
specific respect, solving a similar problem: extracting meaning and structure from markup without
relying on visual layout alone.

## What Concretely Contributes

- **A correct heading hierarchy** (see
  [content-structure-and-heading-hierarchy.md](content-structure-and-heading-hierarchy.md)) helps
  search engines identify the page's main topic (`<h1>`) and its subtopics, which factors into how
  a page is summarized and matched to search queries.
- **Semantic sectioning elements** (`<article>`, `<nav>`, `<main>`) help distinguish primary
  content from navigation and boilerplate, so crawlers don't weight repeated site-wide navigation
  text as if it were unique page content.
- **Descriptive link text** (see
  [links-and-navigation-flow.md](links-and-navigation-flow.md)) contributes to how a linked page
  is understood, since link text is itself a signal about the destination's content — "click here"
  provides none.
- **`alt` text on meaningful images** makes image content discoverable through image search and
  gives crawlers information they cannot extract from pixels alone.
- **A single, descriptive `<title>` and a `<meta name="description">`** are read directly by search
  engines to generate the title and snippet shown in search results.

## Semantic HTML vs. "SEO Tricks"

It's worth being precise about what this module is *not* claiming: writing semantic HTML is not a
substitute for actual content quality, page performance, or backlinks — all of which matter more to
ranking. What semantic HTML provides is the structural foundation that lets search engines (and
assistive technology) correctly interpret genuinely good content in the first place; it doesn't
manufacture relevance that isn't there.

## Common Mistakes

- Stuffing headings or `alt` text with keywords rather than accurate descriptions — search engines
  actively penalize this, and it degrades the accessibility value of the same markup for real
  users.
- Using generic, repeated link text ("read more") across a page, which weakens the descriptive
  signal search engines can extract from links.
- Treating semantic HTML as a checklist to satisfy a crawler, rather than the same accurate,
  meaningful structure that also benefits real users — the two goals are largely the same
  underlying practice, not separate efforts.

## Module Summary

Across this module: choosing semantic elements over generic containers gives structure real
meaning (see [semantic-tags.md](semantic-tags.md)); a correct heading hierarchy and semantic
sectioning create a navigable document outline (see
[content-structure-and-heading-hierarchy.md](content-structure-and-heading-hierarchy.md)); lists,
links, and forms each have dedicated semantic elements worth using correctly rather than
reinventing with generic containers; semantic HTML is the foundation accessibility is built on (see
[accessibility-basics.md](accessibility-basics.md)); browsers turn this markup into pixels through
a defined pipeline where not every change costs the same (see
[how-browsers-render-pages.md](how-browsers-render-pages.md) and
[reflow-and-repaint.md](reflow-and-repaint.md)); responsive images let the browser pick the right
file for each device; and the same semantic structure that helps assistive technology also helps
search engines correctly interpret a page.
