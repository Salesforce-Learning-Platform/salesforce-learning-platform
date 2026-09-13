# JavaScript Events

## Purpose

Interactivity comes from responding to events — clicks, key presses, form submissions. This
module covers registering event handlers, the event object they receive, how events travel through
the DOM tree, and event delegation — a pattern that turns that travel behavior into a genuine
performance and simplicity advantage.

## Learning Objectives

- Register and remove event listeners correctly.
- Use the event object to inspect what happened and control default browser behavior.
- Explain event propagation (capturing and bubbling) and `target` vs. `currentTarget`.
- Use event delegation to handle events for many elements with a single listener.

## Prerequisites

[DOM Manipulation](../dom-manipulation/).

## Files in This Module

| File | Covers |
|---|---|
| [event-listeners.md](event-listeners.md) | `addEventListener`, removing listeners, and listener options |
| [event-object.md](event-object.md) | The event object, `preventDefault()`, and common event properties |
| [event-propagation.md](event-propagation.md) | Bubbling, capturing, `stopPropagation()`, and `target` vs. `currentTarget` |
| [event-delegation.md](event-delegation.md) | Handling many elements' events with one listener on a shared ancestor |

## When to Deep-Dive vs. Skim

Deep-dive [event-propagation.md](event-propagation.md) and
[event-delegation.md](event-delegation.md) together — delegation only makes sense once bubbling is
genuinely understood, and it's one of the most practically useful patterns in this entire module
for handling dynamic lists of elements efficiently.

## Quick Knowledge Check

<details>
<summary>You attach a click listener to a `<ul>`, but the user actually clicked an `<li>` inside it. Inside the handler, what does `event.target` refer to?</summary>

The actual element that was clicked (the `<li>`), not the element the listener is attached to.
`event.currentTarget` refers to the element the listener is attached to (the `<ul>`). This
distinction is exactly what makes event delegation possible. See
[event-propagation.md](event-propagation.md) and [event-delegation.md](event-delegation.md).

</details>

<details>
<summary>Why call `event.preventDefault()` on a form's submit event?</summary>

To stop the browser's default behavior (a full page navigation/reload on form submission) so
JavaScript can handle the submission instead — e.g., sending it via `fetch()` without a page
reload. See [event-object.md](event-object.md).

</details>

## References

- MDN Web Docs, [`EventTarget.addEventListener()`](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)
- MDN Web Docs, [Event bubbling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling)

## Continue Your Learning Path

Next: [Using Browser Functionalities](../using-browser-functionalities/) — see the
[Frontend learning path](../../README.md) for the full sequence.
