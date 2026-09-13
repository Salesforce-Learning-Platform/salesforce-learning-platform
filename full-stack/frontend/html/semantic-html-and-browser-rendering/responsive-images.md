# Responsive Images

## The Problem

A single image file is rarely the right size for every device. Serving one large image to every
visitor wastes bandwidth on small screens; serving one small image looks blurry when stretched on
a large, high-density display. HTML provides dedicated mechanisms to let the browser choose the
right image, rather than forcing one-size-fits-all.

## `srcset` and `sizes`

```html
<img
  src="photo-800w.jpg"
  srcset="photo-400w.jpg 400w, photo-800w.jpg 800w, photo-1600w.jpg 1600w"
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="A description of the photo">
```

- **`srcset`** lists available image files, each annotated with its actual pixel width (`400w`
  means "this file is 400 pixels wide").
- **`sizes`** tells the browser how much of the viewport the image will actually occupy at
  different viewport widths, so it can calculate which `srcset` candidate is the best fit *before*
  downloading anything.
- **`src`** remains as a fallback for browsers that don't support `srcset`.

The browser — not the developer — picks the best candidate at load time, accounting for the
device's screen density and the image's actual rendered size.

## `<picture>` for Art Direction

`srcset`/`sizes` picks between different *resolutions* of the same image. `<picture>` goes further,
letting you serve genuinely *different* images (different crops, different formats) depending on
conditions:

```html
<picture>
  <source media="(max-width: 600px)" srcset="photo-cropped-mobile.jpg">
  <source type="image/avif" srcset="photo.avif">
  <img src="photo.jpg" alt="A description of the photo">
</picture>
```

The browser evaluates `<source>` elements in order and uses the first one whose conditions match
and whose format it supports, falling back to the `<img>` if none match.

## Common Mistakes

- Using `srcset` with only file size in mind and ignoring `sizes` — without `sizes`, the browser
  can't accurately judge which candidate fits its actual layout and may guess conservatively
  (often assuming full viewport width), downloading a larger image than necessary.
- Forgetting the `alt` attribute on a responsive image — every accessibility requirement from
  [accessibility-basics.md](accessibility-basics.md) still applies regardless of how many source
  candidates are provided.
- Serving unnecessarily large images "just in case," ignoring the actual rendered size on the page
  — defeating the entire purpose of responsive images.

## Next

Continue to [seo-impact-of-semantic-html.md](seo-impact-of-semantic-html.md) to see how the
markup choices throughout this module affect search engine visibility.
