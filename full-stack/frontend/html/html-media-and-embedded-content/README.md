# HTML Media and Embedded Content

## Purpose

This module covers embedding rich content directly in a page: images (building on
[responsive-images.md](../semantic-html-and-browser-rendering/responsive-images.md)), audio,
video, and third-party embedded content via `<iframe>` — plus the accessibility and security
considerations each one carries. This is the last module in the HTML domain.

## Learning Objectives

- Choose between `<img>`, `<picture>`, `<video>`, and `<audio>` correctly for a given media type.
- Provide captions and transcripts for accessible media.
- Embed third-party content via `<iframe>` without introducing unnecessary security exposure.

## Prerequisites

[Semantic HTML and Browser Rendering](../semantic-html-and-browser-rendering/), especially
[responsive-images.md](../semantic-html-and-browser-rendering/responsive-images.md) and
[accessibility-basics.md](../semantic-html-and-browser-rendering/accessibility-basics.md).

## Files in This Module

| File | Covers |
|---|---|
| [audio-and-video.md](audio-and-video.md) | `<audio>`/`<video>`, controls, formats, captions/transcripts |
| [embedding-with-iframes.md](embedding-with-iframes.md) | `<iframe>`, the `sandbox` attribute, and embedding security |

## When to Deep-Dive vs. Skim

Deep-dive [embedding-with-iframes.md](embedding-with-iframes.md) before embedding any third-party
content (a video, a payment widget, a map) in a production application — the `sandbox` attribute's
behavior is easy to misconfigure in a way that silently provides no real protection.

## Quick Knowledge Check

<details>
<summary>Why does a `<video>` need captions in addition to (or instead of) just having audio?</summary>

Captions make video content accessible to deaf and hard-of-hearing users, and also help anyone
watching without sound (a common situation on mobile, in public, or in noisy environments) — the
same "helps more than the one group it targets" pattern seen throughout accessibility work. See
[audio-and-video.md](audio-and-video.md).

</details>

<details>
<summary>Is the `sandbox` attribute on an `<iframe>` always a real security boundary?</summary>

Not automatically — combining `allow-scripts` and `allow-same-origin` on a same-origin iframe lets
the embedded content remove its own sandbox restrictions, making the sandbox attribute provide no
real protection in that specific combination. See
[embedding-with-iframes.md](embedding-with-iframes.md).

</details>

## References

- MDN Web Docs, [`<video>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video)
- MDN Web Docs, [`<iframe>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe)

## Continue Your Learning Path

This is the last module in the HTML domain. Continue to
[CSS Fundamentals](../../css/css-core-fundamentals/) — see the
[Frontend learning path](../../README.md) for the full sequence.
