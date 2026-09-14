# Asset Loading Strategy

## Lazy Loading Images and Iframes

```html
<!-- Above the fold: load immediately, it's visible right away -->
<img src="hero-banner.jpg" alt="Summer sale" />

<!-- Below the fold: defer loading until the user scrolls near it -->
<img src="product-2.jpg" alt="Wireless mouse" loading="lazy" />
<img src="product-3.jpg" alt="Mechanical keyboard" loading="lazy" />
<iframe src="embedded-video.html" title="Product demo" loading="lazy"></iframe>
```

The `loading="lazy"` attribute tells the browser to defer downloading an `<img>`, `<iframe>`,
`<video>`, or `<audio>` element's resource until the user scrolls near it, rather than downloading
every image on the page immediately regardless of whether it's ever seen. This directly improves
LCP for the actual above-the-fold content, since the browser isn't competing for bandwidth with
off-screen images. Never lazy-load the LCP element itself — that would delay the exact metric this
is meant to help.

## `async` vs. `defer` for Scripts

```html
<!-- async: downloads in parallel with parsing, executes the instant it's
     ready — parsing pauses for that execution. No guaranteed order. Use for
     independent scripts with no DOM or ordering dependency. -->
<script async src="analytics.js"></script>

<!-- defer: downloads in parallel with parsing, executes only after parsing
     finishes, in document order. Use for application code that depends on
     the DOM or on running after another script. -->
<script defer src="vendor-library.js"></script>
<script defer src="app.js"></script>
```

Without either attribute, a `<script>` tag blocks HTML parsing entirely until it downloads *and*
executes — the original, slowest behavior, still the default for a plain `<script src="...">`.

| Attribute | Parsing | Execution timing | Order guaranteed |
|---|---|---|---|
| (none) | Blocked | Immediately, blocking | N/A |
| `async` | Continues | As soon as downloaded | No |
| `defer` | Continues | After parsing completes | Yes, document order |

A concrete rule: an analytics or ads script that doesn't touch the page and doesn't depend on
anything else should use `async`. Application code that reads or manipulates the DOM, or that
depends on a library loaded by an earlier `<script>` tag, should use `defer`.

## `preload` and `prefetch`

```html
<!-- preload: this resource IS needed for the current page, fetch it with
     high priority right now, even though the browser hasn't reached the
     normal point of discovering it yet -->
<link rel="preload" href="/fonts/brand-sans.woff2" as="font" type="font/woff2" crossorigin />

<!-- prefetch: this resource will likely be needed for a LIKELY FUTURE
     navigation — fetch it at low priority, during idle time -->
<link rel="prefetch" href="/checkout.js" />
```

`preload` tells the browser "this resource is needed for the current page, fetch it now, at high
priority" — commonly used for a web font or a hero image that would otherwise only be discovered
late (e.g., referenced inside a CSS file, which itself has to download first). `prefetch` is the
opposite intent: "this resource probably isn't needed yet, but will likely be needed soon" — for
example, prefetching the next likely page's JavaScript bundle while the user is idle on the current
page.

## Render-Blocking CSS

```html
<!-- Blocks rendering on every page — this is correct for core layout styles -->
<link rel="stylesheet" href="core.css" />

<!-- Only blocks rendering when actually printing — doesn't block the
     normal page render at all -->
<link rel="stylesheet" href="print.css" media="print" />
```

CSS is render-blocking by default: the browser won't paint anything until it has the full
stylesheet, to avoid a flash of unstyled content. Scoping a stylesheet to a `media` query that
doesn't match the current context (like `print`) lets the browser download it without blocking the
initial render.

## Common Mistakes

- Lazy-loading the LCP element itself (a hero image, the primary heading's background image) —
  this delays exactly the metric you're trying to improve.
- Using `async` for a script another script depends on, causing intermittent bugs where the
  dependency sometimes hasn't loaded yet — `defer` is the correct choice whenever order matters.
- Overusing `preload` for resources that aren't actually needed immediately — it competes for the
  same limited early bandwidth as the resources that genuinely matter for LCP, and too many
  preloads can make the real ones slower.

## Next

Continue to [measuring-performance.md](measuring-performance.md) to verify these techniques
actually improve a real page's numbers.
