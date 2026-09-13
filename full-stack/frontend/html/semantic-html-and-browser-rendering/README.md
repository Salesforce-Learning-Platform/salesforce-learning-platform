# Semantic HTML and Browser Rendering

## Purpose

HTML is the structure every web page is built on. This module covers writing HTML that describes
*what content means*, not just how it looks — and what the browser actually does with that markup
between receiving it and painting pixels on screen. This is the first module after
[Foundations](../../foundations/); it assumes you're comfortable with how a browser fetches a page
at all (see [What Happens When You Enter a URL](../../foundations/how-the-internet-works/what-happens-when-you-enter-a-url.md))
but not yet with what's inside the page itself.

## Learning Objectives

- Choose semantic elements over generic `<div>`/`<span>` when a meaningful element exists.
- Structure a document with a correct heading hierarchy and appropriate sectioning elements.
- Build accessible lists, links, and an introductory understanding of forms.
- Explain, at a foundational level, how a browser turns HTML/CSS into pixels, and what triggers
  reflow and repaint.
- Serve responsive images correctly and explain why semantic HTML materially affects SEO.

## Prerequisites

[Foundations](../../foundations/), particularly
[How the Internet Works](../../foundations/how-the-internet-works/).

## Files in This Module

- [ ] [semantic-tags.md](semantic-tags.md) — meaningful elements vs. generic containers
- [ ] [content-structure-and-heading-hierarchy.md](content-structure-and-heading-hierarchy.md) — document outline and heading levels
- [ ] [lists.md](lists.md) — ordered, unordered, and description lists
- [ ] [links-and-navigation-flow.md](links-and-navigation-flow.md) — anchors, navigation, and link accessibility
- [ ] [forms-introduction.md](forms-introduction.md) — the basic form elements (deep dive in the dedicated HTML Forms module)
- [ ] [accessibility-basics.md](accessibility-basics.md) — how semantic HTML is the foundation of accessibility (deep dive in the dedicated HTML Accessibility module)
- [ ] [how-browsers-render-pages.md](how-browsers-render-pages.md) — DOM, CSSOM, render tree, layout, paint
- [ ] [reflow-and-repaint.md](reflow-and-repaint.md) — what triggers each, and why it matters for performance
- [ ] [responsive-images.md](responsive-images.md) — `srcset`, `sizes`, and `<picture>`
- [ ] [seo-impact-of-semantic-html.md](seo-impact-of-semantic-html.md) — why markup choices affect search visibility

## When to Deep-Dive vs. Skim

If you've only ever built pages with `<div>`s, read
[semantic-tags.md](semantic-tags.md) and
[content-structure-and-heading-hierarchy.md](content-structure-and-heading-hierarchy.md) closely —
this habit affects accessibility, SEO, and code readability for every page you build afterward.
[how-browsers-render-pages.md](how-browsers-render-pages.md) and
[reflow-and-repaint.md](reflow-and-repaint.md) matter most once you're optimizing real performance
issues — worth a first read now, but expect to return to them later with a concrete slow page to
diagnose.

## Quick Knowledge Check

<details>
<summary>Why choose `<article>` or `<nav>` over `<div>` when either would look identical on screen?</summary>

Semantic elements communicate meaning to browsers, assistive technology, and search engines that a
`<div>` cannot — a screen reader can jump directly to `<nav>`, and a `<div>` gives it nothing to
work with. Visual appearance is controlled by CSS regardless of which element you choose; the
element choice is about meaning. See [semantic-tags.md](semantic-tags.md).

</details>

<details>
<summary>What's the difference between reflow and repaint, and which is more expensive?</summary>

Reflow recalculates layout (position and size of elements) and cascades to affected elements;
repaint only redraws pixels without recalculating layout. Reflow is more expensive because it can
affect the whole page's layout, while repaint (e.g., a color change) does not. See
[reflow-and-repaint.md](reflow-and-repaint.md).

</details>

## References

- MDN Web Docs, [HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements)
- WHATWG, [HTML Living Standard](https://html.spec.whatwg.org/multipage/)
- W3C WAI, [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)

## Continue Your Learning Path

Next: [HTML Forms and User Input](../html-forms-and-user-input/) — see the
[Frontend learning path](../../README.md) for the full sequence.
