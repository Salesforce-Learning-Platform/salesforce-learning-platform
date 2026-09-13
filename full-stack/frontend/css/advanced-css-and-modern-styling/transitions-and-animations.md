# Transitions and Animations

## `transition`: Animating a State Change

A **transition** smooths the change between two values of a property, in response to something
that already changes that property — like a `:hover` pseudo-class or a class toggled by
JavaScript:

```css
.button {
  background-color: #1a73e8;
  transition: background-color 0.2s ease-in-out;
}

.button:hover {
  background-color: #1557b0;
}
```

Without `transition`, this color change would happen instantly on hover; with it, the browser
smoothly interpolates between the two colors over the specified duration.

| Property | Controls |
|---|---|
| `transition-property` | Which property(ies) to animate |
| `transition-duration` | How long the change takes |
| `transition-timing-function` | The easing curve (`ease`, `linear`, `ease-in-out`) |
| `transition-delay` | Wait time before starting |

A transition only has something to animate *between* — it needs an actual state change (a hover,
a class toggle) to trigger it. It cannot run on its own or loop automatically.

## `@keyframes` and `animation`: Defined Sequences

For a self-contained sequence — including one that loops, or has more than a simple start/end
state — use `@keyframes` combined with the `animation` property:

```css
@keyframes pulse {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.badge {
  animation: pulse 2s ease-in-out infinite;
}
```

`@keyframes` defines the sequence of states (as percentages of the total duration); `animation`
applies it with a duration, timing function, and (as shown here) `infinite` for continuous looping.

## Transition vs. Animation — Choosing the Right One

| | Transition | Animation |
|---|---|---|
| Trigger | A state change (hover, class toggle) | Runs on its own, or on element load |
| Steps | Exactly two (start, end) | Any number of keyframe steps |
| Looping | No | Yes, via `animation-iteration-count: infinite` |

If a design calls for "smoothly change when X happens," reach for a transition; if it calls for "a
sequence that plays automatically or repeats," reach for `@keyframes`/`animation`.

## Performance: Prefer `transform` and `opacity`

As covered in
[reflow-and-repaint.md](../../html/semantic-html-and-browser-rendering/reflow-and-repaint.md),
animating `transform` and `opacity` can often be handled by compositing alone, skipping layout and
paint entirely — while animating `width`, `top`, or similar layout-affecting properties forces a
full reflow on every frame. Preferring `transform`/`opacity` for animated effects is directly
responsible for the difference between a smooth animation and a visibly janky one.

## Respecting `prefers-reduced-motion`

As introduced in
[media-queries-and-breakpoints.md](../responsive-web-design/media-queries-and-breakpoints.md), some
users have genuinely requested reduced motion at the OS level — this isn't a stylistic preference to
optionally accommodate, but a real accessibility need for users who experience discomfort from
motion:

```css
@media (prefers-reduced-motion: reduce) {
  .badge {
    animation: none;
  }
}
```

## Common Mistakes

- Using `@keyframes`/`animation` for a simple two-state hover effect that a `transition` would
  express more simply.
- Animating `width`/`height`/`top`/`left` for effects that `transform` could achieve, causing
  unnecessary reflow on every animation frame.
- Shipping animations with no `prefers-reduced-motion` handling at all.

## Module Summary

Across this module: pseudo-classes style elements by state or structural position, while
pseudo-elements target generated content that has no real DOM node — with a real caveat that
generated content isn't reliably exposed to assistive technology (see
[pseudo-classes-and-pseudo-elements.md](pseudo-classes-and-pseudo-elements.md)); and transitions
smooth a two-state change while `@keyframes`/`animation` define self-running or looping sequences —
both should prefer `transform`/`opacity` for performance and respect `prefers-reduced-motion` for
accessibility.

This completes the CSS domain. Continue to
[Introduction to JavaScript](../../javascript/introduction-to-javascript/), or see the
[Frontend learning path](../../README.md) for the full sequence.
