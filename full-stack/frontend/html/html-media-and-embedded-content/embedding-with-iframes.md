# Embedding with Iframes

## What `<iframe>` Actually Is

An `<iframe>` embeds an entire separate HTML document inside the current page — a genuinely
distinct browsing context with its own DOM, its own JavaScript environment, and (depending on its
source) its own origin. This is fundamentally different from `<img>` or `<video>`, which embed
media, not a whole separate interactive document.

```html
<iframe
  src="https://example.com/widget"
  title="Interactive pricing widget"
  sandbox="allow-scripts">
</iframe>
```

## Why `title` Is Required for Accessibility

Every `<iframe>` should have a descriptive `title` attribute — this is what a screen reader
announces to identify the embedded content, similar in purpose to `alt` text on an image (see
[accessibility-basics.md](../semantic-html-and-browser-rendering/accessibility-basics.md)). Without
it, a screen reader user has no way to know what an embedded frame contains before entering it.

## The `sandbox` Attribute

`sandbox` restricts what an embedded document is allowed to do — by default, applying `sandbox`
with no value disables nearly everything (scripts, forms, top-level navigation, and more), and
individual permissions are re-enabled explicitly as needed:

| Token | Re-enables |
|---|---|
| `allow-scripts` | JavaScript execution inside the iframe |
| `allow-forms` | Form submission from inside the iframe |
| `allow-popups` | Opening new windows/tabs |
| `allow-same-origin` | Treating the iframe's content as being from its actual origin (rather than treated as opaque/restricted) |

## A Critical Security Nuance

Per MDN's own documentation, combining `allow-scripts` and `allow-same-origin` on a same-origin
iframe is strongly discouraged: together, they let the embedded document's own JavaScript remove
the `sandbox` attribute from itself, which makes the sandboxing provide no real restriction at all
in that specific combination. This is a subtle but important trap — adding `sandbox` doesn't
guarantee genuine isolation unless the specific combination of permissions is actually considered
carefully.

## Why Sandboxing Third-Party Content Matters

An embedded iframe from a source you don't control can, without restriction, run arbitrary
JavaScript in a context associated with your page. Sandboxing (and preferring to serve genuinely
untrusted embedded content from a separate origin entirely) limits the damage a malicious or
compromised third-party embed could do — this is a direct, practical application of the "the
client is never fully trustworthy" reasoning from
[frontend-and-backend-responsibilities.md](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md),
extended to third-party content you embed rather than code you write yourself.

## Common Mistakes

- Omitting `title` on an iframe, leaving it unidentified for screen reader users.
- Adding `sandbox` but including `allow-scripts allow-same-origin` together for a same-origin
  frame, believing it's providing protection it actually isn't.
- Embedding third-party content with no sandbox restriction at all, out of convenience, when the
  embedded source isn't fully trusted.

## Module Summary

Across this module: `<video>`/`<audio>` need multiple source formats for compatibility and
captions/transcripts for genuine accessibility, not just a nicety (see
[audio-and-video.md](audio-and-video.md)); and `<iframe>` embeds a full separate browsing context,
requiring a descriptive `title` for accessibility and a carefully chosen `sandbox` configuration for
security — with the `allow-scripts` + `allow-same-origin` combination being a specific, well-known
trap that silently defeats the sandbox's purpose.

This closes the HTML domain — continue to
[CSS Fundamentals](../../css/css-core-fundamentals/), or see the
[Frontend learning path](../../README.md) for the full sequence.
