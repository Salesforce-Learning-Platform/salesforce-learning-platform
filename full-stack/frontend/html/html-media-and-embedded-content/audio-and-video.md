# Audio and Video

## The Basic Elements

```html
<video controls width="640" poster="preview.jpg">
  <source src="video.webm" type="video/webm">
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English">
  Your browser doesn't support video playback.
  <a href="video.mp4">Download the video</a> instead.
</video>

<audio controls>
  <source src="podcast.ogg" type="audio/ogg">
  <source src="podcast.mp3" type="audio/mpeg">
</audio>
```

## Key Attributes

| Attribute | Effect |
|---|---|
| `controls` | Shows the browser's built-in play/pause/volume UI — omitting it removes all user control unless you build custom controls with JavaScript |
| `autoplay` | Starts playback automatically; modern browsers restrict this (commonly requiring `muted` as well) specifically because unsolicited audio is a significant, well-documented usability complaint |
| `muted` | Starts with sound off |
| `loop` | Restarts automatically when finished |
| `poster` (video only) | An image shown before playback starts |
| `preload` | Hints how much to load in advance (`none`, `metadata`, `auto`) |

## Multiple `<source>` Elements

Browsers don't all support the same video/audio codecs. Listing multiple `<source>` elements lets
the browser pick the first format it supports, falling back gracefully rather than failing
outright — the same fallback pattern used by `<picture>` in
[responsive-images.md](../semantic-html-and-browser-rendering/responsive-images.md).

## Captions and Transcripts

The `<track>` element attaches a caption file (in WebVTT format) to a `<video>`, providing
synchronized text for spoken content and important sounds. This is a genuine accessibility
requirement, not an optional nicety — captions make video content accessible to deaf and
hard-of-hearing users, and are commonly relied on by hearing users as well (watching without sound
in a public or noisy space, or in a second language).

A **transcript** (a separate, complete text version of the audio/video content) complements
captions by being independently readable, searchable, and usable by screen reader users who may
prefer reading a transcript to a real-time captioned video.

## Common Mistakes

- Shipping video content with no captions or transcript, excluding deaf and hard-of-hearing users
  entirely from that content.
- Using `autoplay` with unmuted sound, which most modern browsers block outright, and which is a
  poor experience even when it succeeds.
- Providing only a single video format/codec, causing playback to fail entirely for users on a
  browser that doesn't support that specific format.

## Next

Continue to [embedding-with-iframes.md](embedding-with-iframes.md) for embedding third-party
content safely.
