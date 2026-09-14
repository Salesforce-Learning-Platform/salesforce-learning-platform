# Frontend Performance Fundamentals

## Purpose

Every domain so far has taught you to build the UI correctly. This module teaches you to build it
*fast* — the framework-agnostic performance discipline that applies whether the page is built with
plain HTML, [React](../../react/), [Vue](../../vue/vue-fundamentals/), or nothing but
[Web Components](../../web-components/web-components-fundamentals/). React's own memoization and
code-splitting techniques (covered in
[performance-optimization-in-react](../../react/performance-optimization-in-react/)) are a *layer
on top of* the concepts here, not a replacement for them.

## Learning Objectives

- Define the three Core Web Vitals (LCP, INP, CLS), what each measures, and their "good" thresholds.
- Choose an asset loading strategy: `loading="lazy"`, `async`/`defer`, and `preload`/`prefetch`.
- Measure real page performance using Chrome DevTools' Performance panel and the Lighthouse report.
- Explain how the concepts in this module relate to, but are distinct from, React-specific
  optimization techniques.

## Prerequisites

- [HTML domain](../../html/) and [CSS domain](../../css/) — this module assumes you can already
  build a page; it focuses on making that page load and respond quickly.
- [How the Internet Works](../../foundations/how-the-internet-works/) — particularly
  [CDNs, Caching, and Performance](../../foundations/how-the-internet-works/cdns-caching-and-performance.md),
  which covers the network layer this module builds on top of.

## Files in This Module

| File | Covers |
|---|---|
| [core-web-vitals.md](core-web-vitals.md) | LCP, INP, and CLS — what each measures and why it matters to real users |
| [asset-loading-strategy.md](asset-loading-strategy.md) | `loading="lazy"`, `async`/`defer`, and `preload`/`prefetch` |
| [measuring-performance.md](measuring-performance.md) | Chrome DevTools' Performance panel and Lighthouse |

## When to Deep-Dive vs. Skim

Deep-dive [core-web-vitals.md](core-web-vitals.md) — these three metrics are the industry-standard
vocabulary for discussing frontend performance (including in real interviews and real incident
reports), and getting their definitions and thresholds precise matters more than memorizing every
loading-attribute's exact syntax.

## Quick Knowledge Check

<details>
<summary>A page's main content takes 5 seconds to become visible. Which Core Web Vital does this affect, and is it "good"?</summary>

**Largest Contentful Paint (LCP)** — it measures how long the largest visible content element takes
to render. 5 seconds is in the "poor" range (anything over 4 seconds); "good" is 2.5 seconds or
less. See [core-web-vitals.md](core-web-vitals.md).

</details>

<details>
<summary>Should an analytics script that doesn't touch the DOM use `async` or `defer`?</summary>

`async` — it's independent of the page's other scripts and the DOM, so there's no reason to wait
for HTML parsing to finish before running it. `defer` is for scripts that depend on the DOM being
fully parsed or on running in a guaranteed order relative to other scripts. See
[asset-loading-strategy.md](asset-loading-strategy.md).

</details>

## References

- web.dev, [Web Vitals](https://web.dev/articles/vitals)
- MDN, [Lazy loading](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Lazy_loading)
- MDN, [The Script element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script)
- Chrome for Developers, [Performance panel overview](https://developer.chrome.com/docs/devtools/performance)

## Continue Your Learning Path

This is the only module in the Performance domain. See the
[Frontend learning path](../../README.md) for what comes next.
