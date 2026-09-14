# Core Web Vitals

## Why These Three Metrics Specifically

Google's **Core Web Vitals** are a standardized, small set of metrics chosen because each
represents a real, user-perceptible dimension of "does this page feel fast and stable" —
independent of what framework or stack built the page. They're measured at the **75th
percentile** of real page loads, separately for mobile and desktop, so a page is judged by what
most real users actually experience, not by a single best-case test run.

## Largest Contentful Paint (LCP) — Loading

```html
<!-- The LCP element is whichever visible element is largest when it renders —
     often a hero image or the main heading -->
<img src="hero-product.jpg" alt="Featured product" />
<h1>Shop the New Collection</h1>
```

**LCP measures loading performance**: the time from navigation start until the largest visible
content element (an image, a block of text, a video poster) finishes rendering.

| Rating | Threshold |
|---|---|
| Good | ≤ 2.5 seconds |
| Needs Improvement | 2.5 – 4 seconds |
| Poor | > 4 seconds |

A slow LCP is most commonly caused by a slow server response, render-blocking CSS/JS delaying when
the browser can even start painting, or an unoptimized image being the largest element — all
addressed directly in [asset-loading-strategy.md](asset-loading-strategy.md).

## Interaction to Next Paint (INP) — Interactivity

**INP measures interactivity**: how long the page takes to visually respond after a user
interaction (a click, a tap, a key press) — measured across every interaction during the page's
lifetime, not just the first one.

| Rating | Threshold |
|---|---|
| Good | ≤ 200 milliseconds |
| Needs Improvement | 200 – 500 milliseconds |
| Poor | > 500 milliseconds |

A poor INP usually means JavaScript is blocking the main thread for too long in response to an
interaction — a long-running event handler, a large synchronous state update, or excessive
re-rendering (the exact problem
[performance-optimization-in-react](../../react/performance-optimization-in-react/) addresses for
React specifically, one layer above this framework-agnostic concept).

## Cumulative Layout Shift (CLS) — Visual Stability

```html
<!-- WITHOUT explicit dimensions: the image's real size is unknown until it
     downloads, so everything below it jumps down once it loads -->
<img src="banner.jpg" alt="Promotional banner" />

<!-- WITH explicit dimensions: the browser reserves the exact space up front,
     so nothing shifts when the image finishes loading -->
<img src="banner.jpg" alt="Promotional banner" width="1200" height="400" />
```

**CLS measures visual stability**: it quantifies how much visible content unexpectedly shifts
position during the page's lifetime — the frustrating experience of a button moving right as you're
about to tap it, because an ad or image above it just finished loading.

| Rating | Threshold |
|---|---|
| Good | ≤ 0.1 |
| Needs Improvement | 0.1 – 0.25 |
| Poor | > 0.25 |

The single most common fix is reserving space for content before it loads — explicit `width` and
`height` on images and embeds, and a fixed `min-height` for dynamically-inserted content like ads
or late-loading banners.

## Common Mistakes

- Optimizing for a single "lab" test run (e.g., one Lighthouse report) instead of understanding
  that Core Web Vitals are meant to be judged at the 75th percentile of real, varied user sessions.
- Treating LCP as "overall page load time" — it specifically tracks the *largest* visible element,
  not every resource on the page finishing.
- Omitting `width`/`height` on images because "the CSS handles the sizing" — the browser still
  needs those attributes early, before any CSS or image data has loaded, to reserve the correct
  space and prevent a CLS-triggering shift.

## Next

Continue to [asset-loading-strategy.md](asset-loading-strategy.md) to see the concrete techniques
that improve these metrics.
