# The Event Object

## Every Handler Receives an Event Object

```js
button.addEventListener("click", (event) => {
  console.log(event.type);   // "click"
  console.log(event.target); // the actual element that was clicked
});
```

The browser automatically passes an **event object** as the first argument to every event handler,
carrying details about what happened.

## Common Properties

| Property | Provides |
|---|---|
| `type` | The event name (`"click"`, `"submit"`, `"keydown"`) |
| `target` | The actual element the event originated from (see [event-propagation.md](event-propagation.md)) |
| `currentTarget` | The element the listener is attached to |
| `key` / `code` | (Keyboard events) which key was pressed |
| `clientX` / `clientY` | (Mouse events) cursor position |

## `preventDefault()` — Stopping Default Browser Behavior

Many events have a built-in default action the browser performs automatically — following a link,
submitting a form (triggering a full page navigation), or checking a checkbox. `preventDefault()`
stops that default action, letting JavaScript take over instead:

```js
form.addEventListener("submit", (event) => {
  event.preventDefault(); // stop the default full-page navigation
  // ...handle the submission with fetch() instead, as covered in
  // form-submission-and-data.md
});
```

This is exactly the mechanism behind the "intercepting form submission with JavaScript" pattern
introduced in
[form-submission-and-data.md](../../html/html-forms-and-user-input/form-submission-and-data.md) —
`preventDefault()` is the specific call that stops the browser's own navigation so custom
JavaScript logic can run instead.

## Reading Keyboard Input

```js
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    submitForm();
  }
});
```

`event.key` gives the actual character/key name ("Enter", "a", "ArrowUp"); `event.code` gives the
physical key's identifier regardless of keyboard layout — `key` is usually what's wanted for
checking a specific action like "Enter."

## Common Mistakes

- Forgetting `preventDefault()` on a form's submit handler, resulting in both the custom JavaScript
  logic running *and* an unwanted full-page navigation.
- Confusing `event.target` (what was actually interacted with) with `event.currentTarget` (what the
  listener is attached to) — critical for event delegation, covered next.
- Assuming every event has a meaningful `preventDefault()` effect — some events have no default
  action to prevent at all, making the call harmless but pointless.

## Next

Continue to [event-propagation.md](event-propagation.md) to see how an event travels through the
DOM tree before and after reaching its target.
