# Event Listeners

## `addEventListener`

```js
const button = document.querySelector("button");

button.addEventListener("click", () => {
  console.log("Button clicked");
});
```

`addEventListener(eventType, handlerFunction)` is the standard way to respond to an event. Unlike
an inline `onclick="..."` HTML attribute (an older pattern, now discouraged since it mixes
JavaScript into markup and only supports one handler per event), `addEventListener` supports
**multiple independent listeners** on the same element for the same event, and cleanly separates
behavior from structure.

## Removing a Listener

```js
function handleClick() {
  console.log("clicked");
}

button.addEventListener("click", handleClick);
button.removeEventListener("click", handleClick); // must reference the SAME function
```

`removeEventListener` requires a reference to the *exact same function* that was originally
passed — an anonymous inline arrow function (as in the first example) can never be removed, since
there's no way to refer back to it later. Any listener that might need removal should be defined
as a named function first.

## Listener Options

```js
button.addEventListener("click", handleClick, { once: true }); // auto-removes after firing once
window.addEventListener("scroll", handleScroll, { passive: true }); // improves scroll performance
```

| Option | Effect |
|---|---|
| `once: true` | Automatically removes the listener after it fires a single time |
| `passive: true` | Tells the browser the listener won't call `preventDefault()`, letting it optimize (particularly for scroll/touch performance) |
| `capture: true` | Registers the listener for the capturing phase rather than bubbling (see [event-propagation.md](event-propagation.md)) |

## Multiple Listeners on the Same Event

```js
button.addEventListener("click", () => console.log("Listener A"));
button.addEventListener("click", () => console.log("Listener B"));
// clicking logs both "Listener A" and "Listener B", in registration order
```

Both run — `addEventListener` doesn't replace a previous listener the way reassigning
`button.onclick = ...` twice would (the second assignment overwrites the first).

## Common Mistakes

- Passing a new anonymous function to `removeEventListener`, which never matches the original
  listener and silently does nothing.
- Using the older `element.onclick = fn` pattern when multiple independent listeners are actually
  needed on the same element.
- Forgetting to remove listeners on elements that get removed from the DOM in a long-lived
  application, which can contribute to memory not being released as expected.

## Next

Continue to [event-object.md](event-object.md) to see what information a handler actually
receives when it runs.
