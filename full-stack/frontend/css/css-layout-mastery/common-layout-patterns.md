# Common Layout Patterns

## `overflow`

When content is larger than its container, `overflow` determines what happens to the excess:

| Value | Behavior |
|---|---|
| `visible` (default) | Content spills outside the container, uncontained |
| `hidden` | Excess content is clipped and inaccessible |
| `scroll` | Always shows scrollbars, even if content fits |
| `auto` | Shows scrollbars only when content actually overflows |

`overflow: hidden` is also commonly used as a way to contain floated children (a classic pre-Flexbox
technique) or to clip a decorative element's edges to a rounded container.

## Centering — A Historically Awkward Problem

Centering content, especially vertically, was notoriously fiddly before Flexbox and Grid existed.
A few pre-modern-layout techniques still appear in real codebases and are worth recognizing:

```css
/* Centering an absolutely positioned element */
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

This works by first positioning the element's top-left corner at the exact center (`top: 50%; left:
50%`), then shifting it back by half its own width and height (`translate(-50%, -50%)`) — necessary
because percentage offsets in `top`/`left` are relative to the *container's* size, not the
element's own size. Flexbox and Grid (covered in their own dedicated modules) solve centering far
more directly and are generally preferred for new code today.

## Floats — A Legacy Technique Worth Recognizing

Before Flexbox/Grid, `float` was frequently repurposed for multi-column layout (rather than its
original purpose of wrapping text around an image). This is now considered legacy practice for
layout purposes — floats still exist and work as originally designed (wrapping inline content
around a floated image), but multi-column and full-page layout should use Flexbox or Grid instead.
Recognizing floated layout is still useful for reading and maintaining older codebases.

## When Not to Reach for Flexbox/Grid

Not every layout need requires a full layout module. Simple, single-purpose needs are sometimes
better served by more basic tools:

- A single element that just needs to not overflow its container: `overflow`.
- An image that should wrap with text: `float` (its original, still-valid purpose).
- Positioning a small badge or tooltip relative to a parent: `position: relative`/`absolute` (see
  [positioning.md](positioning.md)).

Reaching for Flexbox or Grid for these simpler cases isn't wrong, but it's worth recognizing when a
simpler tool already solves the problem directly.

## Common Mistakes

- Using floats for a new multi-column page layout today, rather than Flexbox or Grid, which solve
  the same problem far more directly and with fewer historical workarounds (like manual "clearfix"
  hacks) required.
- Forgetting to clear or contain floated elements, causing a parent container to collapse to zero
  height around floated children.
- Using the `top: 50%; transform: translate(-50%, -50%)` centering pattern reflexively, when a
  Flexbox container (`display: flex; align-items: center; justify-content: center;`) would achieve
  the same result more simply.

## Module Summary

Across this module: normal document flow and `display` establish the default layout every other
technique modifies (see [positioning.md](positioning.md)); `position` lets specific elements opt
out of normal flow for offsetting, overlays, and sticky behavior; `z-index` only resolves
conflicts within the same stacking context, which is the source of most confusing stacking bugs
(see [stacking-context.md](stacking-context.md)); and classic pre-Flexbox/Grid techniques
(`overflow`, floats, the percentage-offset centering trick) remain useful to recognize, even as
Flexbox and Grid — covered next — are the preferred tools for genuine layout problems today.
