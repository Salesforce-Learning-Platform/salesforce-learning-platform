# Event Propagation

## An Event Travels Through the Tree

When an event fires on an element, it doesn't just happen there in isolation — it travels through
the DOM tree in three phases:

```text
1. Capturing phase:  document → html → body → ... → target's ancestors, top-down
2. Target phase:     the event reaches the actual element interacted with
3. Bubbling phase:   target → ... → body → html → document, bottom-up
```

By default, `addEventListener` listens during the **bubbling phase** — a click on a deeply nested
`<button>` also triggers any click listeners on its ancestors, in order from the button outward to
`document`, unless something stops it.

## `target` vs. `currentTarget`

```js
list.addEventListener("click", (event) => {
  console.log(event.target);        // the actual element clicked (could be a child <li>)
  console.log(event.currentTarget); // always the <ul> — where the listener is attached
});
```

- **`event.target`**: the actual, specific element the event originated from — this can be a
  descendant of the element the listener is attached to.
- **`event.currentTarget`**: the element the listener is currently executing on — stays fixed
  regardless of which descendant was actually interacted with.

This distinction is precisely what makes event delegation (see
[event-delegation.md](event-delegation.md)) possible: a single listener on a parent can still tell
exactly which child was interacted with, via `event.target`.

## Stopping Propagation

```js
child.addEventListener("click", (event) => {
  event.stopPropagation(); // prevents the event from bubbling further up
});
```

`stopPropagation()` prevents an event from continuing to travel to ancestor elements — useful when
a nested interactive element (like a button inside a clickable card) shouldn't also trigger the
outer card's own click handler.

## Common Mistakes

- Assuming an event only affects the exact element clicked, missing that it also bubbles through
  every ancestor with a listener for the same event type.
- Confusing `target` and `currentTarget` inside a delegated listener, using the wrong one to
  identify which specific element was actually interacted with.
- Overusing `stopPropagation()` reflexively, which can silently break other, legitimate listeners
  higher up the tree that expected to receive the event.

## Next

Continue to [event-delegation.md](event-delegation.md) to see how bubbling becomes a genuinely
useful pattern rather than just background behavior to be aware of.
