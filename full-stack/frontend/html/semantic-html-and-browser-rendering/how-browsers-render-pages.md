# How Browsers Render Pages

## From HTML Text to Pixels

[what-happens-when-you-enter-a-url.md](../../foundations/how-the-internet-works/what-happens-when-you-enter-a-url.md)
stopped at "the browser receives the HTML response." This file picks up exactly there: what the
browser does with that response to produce what you actually see.

## The Rendering Pipeline

```text
HTML  ──parse──▶  DOM (Document Object Model)
                                          │
CSS   ──parse──▶  CSSOM (CSS Object Model)│
                                          ▼
                              Render Tree (DOM + CSSOM combined,
                                excluding non-visible elements)
                                          │
                                          ▼
                                       Layout
                              (compute exact size/position of
                                every visible element)
                                          │
                                          ▼
                                        Paint
                              (fill in pixels: colors, text, images)
                                          │
                                          ▼
                                     Composite
                              (combine painted layers onto the screen)
```

## The Stages, Briefly

- **DOM**: the browser parses HTML into a tree of node objects — the live, in-memory representation
  JavaScript actually interacts with (`document.querySelector`, etc.), which can differ from the
  original HTML source once scripts run.
- **CSSOM**: the browser parses all CSS (external stylesheets, `<style>` blocks, inline styles)
  into a tree of style rules, resolving the cascade and inheritance for every element.
- **Render tree**: the DOM and CSSOM are combined into a tree containing only what will actually
  be visible — elements with `display: none` are excluded entirely (they generate no render tree
  node), which is a meaningful distinction from `visibility: hidden`, which stays in the render
  tree but produces no visible pixels.
- **Layout (also called "reflow")**: the browser calculates the exact position and size of every
  element in the render tree, given the viewport size and the CSS box model.
- **Paint**: the browser fills in actual pixels — text, colors, borders, images — for each element.
- **Composite**: separately painted layers are combined in the correct order onto the screen,
  which is what makes certain CSS properties (like `transform` and `opacity`) cheaper to animate
  than others that require a full layout recalculation.

## Why This Matters Practically

Understanding this pipeline is what lets you reason about *why* some changes are expensive and
others are cheap — covered concretely in
[reflow-and-repaint.md](reflow-and-repaint.md). It's also why a page can be fully downloaded (per
[what-happens-when-you-enter-a-url.md](../../foundations/how-the-internet-works/what-happens-when-you-enter-a-url.md))
and still show a blank screen briefly — rendering is real, additional work that happens after the
network request completes.

## Common Mistakes

- Assuming "the page loaded" and "the page is fully rendered and interactive" are the same moment
  — a large or render-blocking resource can visibly delay rendering well after the initial HTML
  response arrives.
- Confusing the DOM (live, current state) with "the HTML I wrote" — JavaScript can and often does
  modify the DOM after the initial parse, without changing the original source file at all.
- Not distinguishing `display: none` (removed from the render tree entirely, no layout space)
  from `visibility: hidden` (still occupies layout space, just isn't painted).

## Next

Continue to [reflow-and-repaint.md](reflow-and-repaint.md) for what specifically triggers each
stage of this pipeline to re-run, and why that's a real performance concern.
