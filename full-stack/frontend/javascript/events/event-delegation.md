# Event Delegation

## The Problem: Many Elements, Many Listeners

```js
// Naive approach: one listener per item
document.querySelectorAll("li").forEach(li => {
  li.addEventListener("click", handleClick);
});
```

This works, but has two real downsides: it attaches a separate listener to every single element
(wasteful at scale), and it does nothing for elements added to the list **later** — a new `<li>`
added after this code runs would have no listener attached at all.

## The Delegation Pattern

```js
document.querySelector("ul").addEventListener("click", (event) => {
  if (event.target.matches("li")) {
    handleClick(event);
  }
});
```

Instead of attaching a listener to every `<li>`, attach **one** listener to their shared parent
(`<ul>`) and rely on bubbling (see
[event-propagation.md](event-propagation.md)): a click on any `<li>`, including ones added after
this code runs, bubbles up to the `<ul>`, where `event.target` tells you exactly which `<li>` was
actually clicked.

## Why This Solves Both Problems

- **One listener instead of many**: a single listener on the parent handles clicks for every
  current *and future* child, at a fraction of the memory/setup cost of one listener per item.
- **Works automatically for dynamically added elements**: since the listener lives on the parent
  (which already exists), any new child added later is automatically covered — no need to
  remember to attach a new listener every time the list changes.

## Filtering with `matches()` or `closest()`

```js
list.addEventListener("click", (event) => {
  const item = event.target.closest("li"); // finds the nearest <li> ancestor (or itself)
  if (item) {
    handleClick(item);
  }
});
```

`event.target` might be a nested element *inside* the `<li>` (an icon, a span) rather than the
`<li>` itself — `.closest("li")` reliably finds the nearest matching ancestor (or the element
itself, if it already matches), which is more robust than `matches()` alone for markup with nested
child elements.

## When Delegation Is (and Isn't) the Right Choice

Delegation shines for lists of similar, repeatable, or dynamically changing elements. It's
unnecessary — and adds a small layer of indirection for no benefit — for a single, static element
that will never be added or removed, where a direct listener is simpler and just as effective.

## Common Mistakes

- Attaching individual listeners to every item in a large or frequently changing list, missing the
  efficiency and "works for future elements" benefits delegation provides.
- Using `event.target` directly for filtering when the actual click could land on a nested child
  element inside the intended target, instead of using `.closest()` to reliably find the right
  ancestor.
- Applying delegation to every single event handler reflexively, even for a single static element
  where the added indirection provides no real benefit.

## Module Summary

Across this module: `addEventListener` supports multiple listeners per element and must be paired
with a named function reference if later removal is needed (see
[event-listeners.md](event-listeners.md)); every handler receives an event object carrying details
like `type`, `target`, and `key`, with `preventDefault()` stopping the browser's own default
behavior (see [event-object.md](event-object.md)); events travel through capturing and bubbling
phases, with `target` (what was interacted with) distinct from `currentTarget` (where the listener
lives) (see [event-propagation.md](event-propagation.md)); and event delegation exploits bubbling
to handle many — including future — elements with a single listener on a shared ancestor.
